#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
macOS Platform Adapter

macOS平台字体适配器，处理macOS系统特定的字体管理。
"""

import os
import subprocess
from typing import List, Dict, Optional, Set
from pathlib import Path

from ..core.models import Platform
from ..utils.helpers import safe_path_join
from .base import PlatformAdapter


class MacOSAdapter(PlatformAdapter):
    """
    macOS平台适配器
    
    处理macOS系统的字体检测、配置和管理。
    """
    
    def __init__(self):
        """初始化macOS适配器"""
        super().__init__(Platform.MACOS)
        
        # macOS特定的字体目录
        self._system_font_dirs = [
            Path("/System/Library/Fonts"),
            Path("/Library/Fonts"),
            Path.home() / "Library/Fonts"
        ]
        
        # macOS字体配置路径
        self._font_config_paths = [
            Path("/System/Library/FontCollections"),
            Path("/Library/FontCollections"),
            Path.home() / "Library/FontCollections"
        ]
    
    def get_system_fonts(self) -> List[str]:
        """
        获取macOS系统字体路径列表
        
        Returns:
            List[str]: 系统字体文件路径列表
        """
        font_paths = []
        
        for font_dir in self.get_font_directories():
            if not font_dir.exists():
                continue
            
            try:
                # 递归搜索字体文件
                for ext in self.get_font_extensions():
                    pattern = f"**/*{ext}"
                    font_files = font_dir.glob(pattern)
                    font_paths.extend([str(f) for f in font_files if f.is_file()])
                    
            except Exception as e:
                self.logger.warning(f"扫描字体目录失败 {font_dir}: {e}")
        
        # 去重并排序
        font_paths = list(set(font_paths))
        font_paths.sort()
        
        self.logger.info(f"macOS系统找到 {len(font_paths)} 个字体文件")
        return font_paths
    
    def get_preferred_fonts(self) -> List[str]:
        """
        获取macOS推荐的中文字体列表
        
        Returns:
            List[str]: 推荐字体名称列表，按优先级排序
        """
        return [
            'Hiragino Sans GB',      # 最佳中文字体
            'PingFang SC',           # 苹果现代中文字体
            'STHeiti',               # 系统黑体
            'Hiragino Sans',         # 日文字体，支持部分中文
            'Arial Unicode MS',      # Unicode字体
            'Apple LiGothic',        # 苹果丽黑
            'STSong',                # 宋体
            'STKaiti',               # 楷体
            'STFangsong'             # 仿宋
        ]
    
    def get_font_directories(self) -> List[Path]:
        """
        获取macOS字体目录列表
        
        Returns:
            List[Path]: 字体目录路径列表
        """
        return [d for d in self._system_font_dirs if d.exists()]
    
    def get_font_config_paths(self) -> List[Path]:
        """
        获取macOS字体配置文件路径
        
        Returns:
            List[Path]: 字体配置文件路径列表
        """
        config_paths = []
        
        for config_dir in self._font_config_paths:
            if config_dir.exists():
                # 查找.collection文件
                collection_files = config_dir.glob("*.collection")
                config_paths.extend(collection_files)
        
        return config_paths
    
    def get_platform_specific_keywords(self) -> Set[str]:
        """
        获取macOS特定的中文字体关键词
        
        Returns:
            Set[str]: macOS特定关键词集合
        """
        return {
            'hiragino', 'pingfang', 'heiti', 'songti', 'kaiti', 'fangsong',
            'apple', 'ligothic', 'stfont', 'st', 'gb', 'sc', 'tc',
            'system', 'ui', 'sf', 'sfns'
        }
    
    def extract_platform_metadata(self, font_path: Path) -> Optional[Dict[str, str]]:
        """
        提取macOS特定的字体元数据
        
        Args:
            font_path: 字体文件路径
            
        Returns:
            Optional[Dict[str, str]]: macOS特定元数据
        """
        metadata = {}
        
        try:
            # 使用mdls命令获取字体元数据
            result = subprocess.run(
                ['mdls', '-name', 'kMDItemFonts', str(font_path)],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0 and result.stdout:
                # 解析mdls输出
                output = result.stdout.strip()
                if 'kMDItemFonts' in output and '(' in output:
                    # 提取字体名称列表
                    start = output.find('(')
                    end = output.rfind(')')
                    if start != -1 and end != -1:
                        fonts_str = output[start+1:end]
                        # 简单解析，实际可能需要更复杂的处理
                        metadata['system_fonts'] = fonts_str.strip()
            
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
            # mdls命令不可用或超时，使用备用方法
            pass
        
        # 从文件路径推断信息
        path_str = str(font_path)
        if '/System/Library/Fonts/' in path_str:
            metadata['font_type'] = 'system'
        elif '/Library/Fonts/' in path_str:
            metadata['font_type'] = 'global'
        elif '/Library/Fonts/' in path_str:
            metadata['font_type'] = 'user'
        
        return metadata if metadata else None
    
    def is_chinese_font_platform_specific(self, font_name: str, font_path: Path) -> bool:
        """
        macOS特定的中文字体判断逻辑
        
        Args:
            font_name: 字体名称
            font_path: 字体文件路径
            
        Returns:
            bool: 是否为中文字体
        """
        # macOS特定的中文字体判断
        macos_chinese_fonts = {
            'hiragino sans gb', 'pingfang sc', 'pingfang tc', 'pingfang hk',
            'stheiti', 'stsong', 'stkaiti', 'stfangsong',
            'apple ligothic', 'ligothic medium', 'ligothic light'
        }
        
        name_lower = font_name.lower()
        for chinese_font in macos_chinese_fonts:
            if chinese_font in name_lower:
                return True
        
        # 检查文件路径中的特殊标识
        path_lower = str(font_path).lower()
        if any(keyword in path_lower for keyword in ['chinese', 'cjk', 'han', 'gb', 'sc', 'tc']):
            return True
        
        return False
    
    def get_system_language(self) -> str:
        """
        获取系统语言设置
        
        Returns:
            str: 系统语言代码
        """
        try:
            result = subprocess.run(
                ['defaults', 'read', '-g', 'AppleLanguages'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0 and result.stdout:
                # 解析语言列表，取第一个
                output = result.stdout.strip()
                if '(' in output and ')' in output:
                    start = output.find('(')
                    end = output.find(',', start)
                    if end == -1:
                        end = output.find(')', start)
                    
                    if start != -1 and end != -1:
                        first_lang = output[start+1:end].strip().strip('"')
                        return first_lang
            
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
            pass
        
        return 'en'  # 默认英语
    
    def is_chinese_system(self) -> bool:
        """
        检查是否为中文系统
        
        Returns:
            bool: 是否为中文系统
        """
        system_lang = self.get_system_language()
        return system_lang.startswith(('zh', 'cn'))
    
    def get_font_book_fonts(self) -> List[str]:
        """
        获取字体册中的字体列表
        
        Returns:
            List[str]: 字体册中的字体名称列表
        """
        fonts = []
        
        try:
            # 尝试读取字体册数据库
            font_book_db = Path.home() / "Library/FontCollections/com.apple.FontBook.plist"
            
            if font_book_db.exists():
                # 这里可以解析plist文件获取字体信息
                # 简化实现：返回空列表
                pass
                
        except Exception as e:
            self.logger.debug(f"读取字体册数据失败: {e}")
        
        return fonts
    
    def configure_matplotlib(self, font_name: str) -> bool:
        """
        配置matplotlib使用指定字体（macOS优化版）
        
        Args:
            font_name: 字体名称
            
        Returns:
            bool: 配置是否成功
        """
        try:
            import matplotlib.pyplot as plt
            import matplotlib.font_manager as fm
            
            # macOS特定的字体配置
            font_list = [font_name]
            
            # 添加macOS推荐的备用字体
            preferred_fonts = self.get_preferred_fonts()
            for font in preferred_fonts:
                if font != font_name and font not in font_list:
                    font_list.append(font)
            
            # 添加通用备用字体
            font_list.extend(self.get_fallback_fonts())
            
            # 设置matplotlib字体
            plt.rcParams['font.sans-serif'] = font_list
            plt.rcParams['axes.unicode_minus'] = False
            
            # macOS特定的字体缓存清理
            try:
                # 清理matplotlib字体缓存
                fm._rebuild()
                
                # 清理系统字体缓存（如果需要）
                # 注意：这可能需要管理员权限
                # subprocess.run(['sudo', 'atsutil', 'databases', '-remove'], check=False)
                
            except Exception as e:
                self.logger.debug(f"字体缓存清理失败: {e}")
            
            self.logger.info(f"macOS matplotlib字体配置成功: {font_name}")
            return True
            
        except ImportError:
            self.logger.warning("matplotlib未安装，跳过字体配置")
            return False
        except Exception as e:
            self.logger.error(f"macOS matplotlib字体配置失败: {e}")
            return False
    
    def get_system_info(self) -> Dict[str, str]:
        """
        获取macOS系统信息
        
        Returns:
            Dict[str, str]: 系统信息字典
        """
        info = super().get_system_info()
        
        try:
            # 获取macOS版本
            result = subprocess.run(
                ['sw_vers', '-productVersion'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                info['macos_version'] = result.stdout.strip()
            
            # 获取系统语言
            info['system_language'] = self.get_system_language()
            info['is_chinese_system'] = str(self.is_chinese_system())
            
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
            pass
        
        return info