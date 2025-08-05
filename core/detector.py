#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Font Detector

字体检测器，负责扫描系统字体并进行质量评估。
"""

import os
import time
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple
import re

from .models import FontInfo, FontWeight, FontStyle, Platform
from .exceptions import FontNotFoundError, FontValidationError
from ..utils.logger import LoggerMixin
from ..utils.helpers import (
    get_platform, is_font_file, get_file_size, 
    calculate_font_score, get_system_font_directories,
    normalize_font_name, find_files_by_pattern
)
from ..adapters import get_platform_adapter


class FontDetector(LoggerMixin):
    """
    字体检测器
    
    负责扫描系统字体文件，提取字体信息，并进行质量评估。
    """
    
    def __init__(self, cache_enabled: bool = True):
        """
        初始化字体检测器
        
        Args:
            cache_enabled: 是否启用字体缓存
        """
        self.platform = get_platform()
        self.cache_enabled = cache_enabled
        self._font_cache: Dict[str, FontInfo] = {}
        self._scan_cache: Dict[str, List[Path]] = {}
        self._last_scan_time: float = 0
        
        # 获取平台适配器
        self.adapter = get_platform_adapter(self.platform)
        
        # 从适配器获取配置
        self.font_extensions = self.adapter.get_font_extensions()
        self.chinese_font_keywords = self.adapter.get_chinese_font_keywords()
        
        self.logger.info(f"FontDetector initialized for platform: {self.platform.value}")
    
    def detect_system_fonts(self, force_rescan: bool = False) -> List[FontInfo]:
        """
        检测系统字体
        
        Args:
            force_rescan: 是否强制重新扫描
            
        Returns:
            List[FontInfo]: 检测到的字体列表
        """
        start_time = time.time()
        self.logger.info("开始检测系统字体...")
        
        # 检查缓存
        if not force_rescan and self.cache_enabled and self._font_cache:
            cache_age = time.time() - self._last_scan_time
            if cache_age < 3600:  # 缓存1小时
                self.logger.info(f"使用缓存的字体信息 ({len(self._font_cache)} 个字体)")
                return list(self._font_cache.values())
        
        # 获取系统字体目录
        font_directories = self.adapter.get_font_directories()
        self.logger.info(f"扫描 {len(font_directories)} 个字体目录")
        
        # 扫描字体文件
        font_files = self._scan_font_files(font_directories, force_rescan)
        self.logger.info(f"找到 {len(font_files)} 个字体文件")
        
        # 提取字体信息
        fonts = []
        for font_file in font_files:
            try:
                font_info = self._extract_font_info(font_file)
                if font_info:
                    fonts.append(font_info)
                    if self.cache_enabled:
                        self._font_cache[font_info.name] = font_info
            except Exception as e:
                self.logger.warning(f"提取字体信息失败 {font_file}: {e}")
        
        # 更新缓存时间
        self._last_scan_time = time.time()
        
        scan_time = time.time() - start_time
        self.logger.info(f"字体检测完成，找到 {len(fonts)} 个字体，耗时 {scan_time:.2f}秒")
        
        return fonts
    
    def _scan_font_files(self, directories: List[Path], force_rescan: bool = False) -> List[Path]:
        """
        扫描字体文件
        
        Args:
            directories: 字体目录列表
            force_rescan: 是否强制重新扫描
            
        Returns:
            List[Path]: 字体文件路径列表
        """
        cache_key = "|".join(str(d) for d in directories)
        
        # 检查扫描缓存
        if not force_rescan and self.cache_enabled and cache_key in self._scan_cache:
            return self._scan_cache[cache_key]
        
        font_files = []
        
        for directory in directories:
            if not directory.exists():
                self.logger.warning(f"字体目录不存在: {directory}")
                continue
            
            try:
                # 扫描字体文件
                for ext in self.font_extensions:
                    pattern = f"*{ext}"
                    files = find_files_by_pattern(directory, pattern, recursive=True)
                    font_files.extend(files)
                    
                self.logger.debug(f"扫描目录 {directory}: 找到 {len([f for f in font_files if str(f).startswith(str(directory))])} 个文件")
                
            except Exception as e:
                self.logger.error(f"扫描目录失败 {directory}: {e}")
        
        # 去重并排序
        font_files = list(set(font_files))
        font_files.sort()
        
        # 缓存结果
        if self.cache_enabled:
            self._scan_cache[cache_key] = font_files
        
        return font_files
    
    def _extract_font_info(self, font_path: Path) -> Optional[FontInfo]:
        """
        提取字体信息
        
        Args:
            font_path: 字体文件路径
            
        Returns:
            Optional[FontInfo]: 字体信息，提取失败返回None
        """
        try:
            # 基本信息
            file_size = get_file_size(font_path)
            if file_size == 0:
                return None
            
            # 从文件名推断字体信息
            font_name = self._extract_font_name(font_path)
            font_family = self._extract_font_family(font_name)
            font_weight = self._extract_font_weight(font_name)
            font_style = self._extract_font_style(font_name)
            
            # 检测中文支持
            supports_chinese = self.adapter.is_chinese_font(font_name, font_path)
            
            # 计算质量评分
            preferred_fonts = self.adapter.get_preferred_fonts()
            quality_score = calculate_font_score(
                font_name, supports_chinese, file_size, 
                self.platform, preferred_fonts
            )
            
            # 计算平台优先级
            platform_priority = self.adapter.get_font_priority(font_name)
            
            # 创建FontInfo对象
            font_info = FontInfo(
                name=font_name,
                path=str(font_path),
                family=font_family,
                style=font_style,
                weight=font_weight,
                supports_chinese=supports_chinese,
                quality_score=quality_score,
                platform_priority=platform_priority,
                file_size=file_size,
                version=self._extract_font_version(font_path)
            )
            
            return font_info
            
        except Exception as e:
            self.logger.error(f"提取字体信息失败 {font_path}: {e}")
            return None
    
    def _extract_font_name(self, font_path: Path) -> str:
        """
        从文件路径提取字体名称
        
        Args:
            font_path: 字体文件路径
            
        Returns:
            str: 字体名称
        """
        # 从文件名提取
        name = font_path.stem
        
        # 移除常见的后缀
        suffixes_to_remove = [
            'Regular', 'Bold', 'Italic', 'Light', 'Medium', 'Heavy',
            'Thin', 'Black', 'Condensed', 'Extended', 'Narrow'
        ]
        
        for suffix in suffixes_to_remove:
            if name.endswith(suffix):
                name = name[:-len(suffix)].strip('-_ ')
                break
        
        # 标准化名称
        name = normalize_font_name(name)
        
        # 如果名称为空，使用文件名
        if not name:
            name = font_path.stem
        
        return name
    
    def _extract_font_family(self, font_name: str) -> str:
        """
        提取字体族名
        
        Args:
            font_name: 字体名称
            
        Returns:
            str: 字体族名
        """
        # 简单实现：使用字体名称作为族名
        # 实际实现中可以通过解析字体文件获取更准确的信息
        return font_name
    
    def _extract_font_weight(self, font_name: str) -> FontWeight:
        """
        从字体名称提取字体粗细
        
        Args:
            font_name: 字体名称
            
        Returns:
            FontWeight: 字体粗细
        """
        name_lower = font_name.lower()
        
        if any(keyword in name_lower for keyword in ['thin', 'ultralight']):
            return FontWeight.THIN
        elif any(keyword in name_lower for keyword in ['extralight', 'ultralight']):
            return FontWeight.EXTRA_LIGHT
        elif any(keyword in name_lower for keyword in ['light']):
            return FontWeight.LIGHT
        elif any(keyword in name_lower for keyword in ['medium']):
            return FontWeight.MEDIUM
        elif any(keyword in name_lower for keyword in ['semibold', 'demibold']):
            return FontWeight.SEMI_BOLD
        elif any(keyword in name_lower for keyword in ['bold']):
            return FontWeight.BOLD
        elif any(keyword in name_lower for keyword in ['extrabold', 'ultrabold']):
            return FontWeight.EXTRA_BOLD
        elif any(keyword in name_lower for keyword in ['black', 'heavy']):
            return FontWeight.BLACK
        else:
            return FontWeight.NORMAL
    
    def _extract_font_style(self, font_name: str) -> FontStyle:
        """
        从字体名称提取字体样式
        
        Args:
            font_name: 字体名称
            
        Returns:
            FontStyle: 字体样式
        """
        name_lower = font_name.lower()
        
        if 'italic' in name_lower:
            return FontStyle.ITALIC
        elif 'oblique' in name_lower:
            return FontStyle.OBLIQUE
        else:
            return FontStyle.NORMAL
    

    
    def _extract_font_version(self, font_path: Path) -> str:
        """
        提取字体版本信息
        
        Args:
            font_path: 字体文件路径
            
        Returns:
            str: 字体版本
        """
        # 简单实现：返回空字符串
        # 实际实现中可以通过解析字体文件获取版本信息
        return ""
    

    
    def rank_fonts(self, fonts: List[FontInfo]) -> List[FontInfo]:
        """
        按质量和兼容性排序字体
        
        Args:
            fonts: 字体列表
            
        Returns:
            List[FontInfo]: 排序后的字体列表
        """
        self.logger.info(f"对 {len(fonts)} 个字体进行排序...")
        
        # 多维度排序
        def sort_key(font: FontInfo) -> Tuple[bool, int, float, int]:
            return (
                not font.supports_chinese,  # 中文支持优先
                font.platform_priority,     # 平台优先级
                -font.quality_score,        # 质量评分（降序）
                len(font.name)              # 名称长度（简短优先）
            )
        
        sorted_fonts = sorted(fonts, key=sort_key)
        
        self.logger.info("字体排序完成")
        if sorted_fonts:
            top_font = sorted_fonts[0]
            self.logger.info(f"最佳字体: {top_font.name} (评分: {top_font.quality_score:.2f})")
        
        return sorted_fonts
    
    def verify_font(self, font_path: str) -> bool:
        """
        验证字体文件
        
        Args:
            font_path: 字体文件路径
            
        Returns:
            bool: 字体文件是否有效
        """
        try:
            path = Path(font_path)
            
            # 检查文件存在性
            if not path.exists():
                self.logger.warning(f"字体文件不存在: {font_path}")
                return False
            
            # 检查文件类型
            if not is_font_file(path):
                self.logger.warning(f"不是有效的字体文件: {font_path}")
                return False
            
            # 检查文件大小
            file_size = get_file_size(path)
            if file_size < 1024:  # 小于1KB
                self.logger.warning(f"字体文件太小: {font_path} ({file_size} bytes)")
                return False
            
            # 检查文件可读性
            try:
                with open(path, 'rb') as f:
                    header = f.read(4)
                    if not header:
                        self.logger.warning(f"无法读取字体文件: {font_path}")
                        return False
            except IOError as e:
                self.logger.warning(f"字体文件读取失败: {font_path} - {e}")
                return False
            
            self.logger.debug(f"字体文件验证通过: {font_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"字体文件验证出错: {font_path} - {e}")
            return False
    
    def find_font_by_name(self, font_name: str, fonts: Optional[List[FontInfo]] = None) -> Optional[FontInfo]:
        """
        按名称查找字体
        
        Args:
            font_name: 字体名称
            fonts: 字体列表，None表示使用检测到的字体
            
        Returns:
            Optional[FontInfo]: 找到的字体，未找到返回None
        """
        if fonts is None:
            fonts = self.detect_system_fonts()
        
        normalized_target = normalize_font_name(font_name).lower()
        
        # 精确匹配
        for font in fonts:
            if normalize_font_name(font.name).lower() == normalized_target:
                return font
        
        # 模糊匹配
        for font in fonts:
            if normalized_target in normalize_font_name(font.name).lower():
                return font
        
        return None
    
    def get_chinese_fonts(self, fonts: Optional[List[FontInfo]] = None) -> List[FontInfo]:
        """
        获取支持中文的字体
        
        Args:
            fonts: 字体列表，None表示使用检测到的字体
            
        Returns:
            List[FontInfo]: 支持中文的字体列表
        """
        if fonts is None:
            fonts = self.detect_system_fonts()
        
        chinese_fonts = [font for font in fonts if font.supports_chinese]
        return self.rank_fonts(chinese_fonts)
    
    def clear_cache(self):
        """清除字体缓存"""
        self._font_cache.clear()
        self._scan_cache.clear()
        self._last_scan_time = 0
        self.logger.info("字体缓存已清除")
    
    @property
    def cache_size(self) -> int:
        """获取缓存大小"""
        return len(self._font_cache)
    
    @property
    def cache_age(self) -> float:
        """获取缓存年龄（秒）"""
        if self._last_scan_time == 0:
            return float('inf')
        return time.time() - self._last_scan_time