#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Platform Adapter Base Class

平台适配器基类，定义了不同操作系统字体处理的统一接口。
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Set
from pathlib import Path

from ..core.models import FontInfo, Platform
from ..utils.logger import LoggerMixin


class PlatformAdapter(ABC, LoggerMixin):
    """
    平台适配器抽象基类
    
    定义了不同操作系统字体处理的统一接口。
    每个平台的具体实现需要继承此类并实现抽象方法。
    """
    
    def __init__(self, platform: Platform):
        """
        初始化平台适配器
        
        Args:
            platform: 平台类型
        """
        self.platform = platform
        self._font_cache: Dict[str, FontInfo] = {}
        
        self.logger.info(f"PlatformAdapter initialized for {platform.value}")
    
    @abstractmethod
    def get_system_fonts(self) -> List[str]:
        """
        获取系统字体路径列表
        
        Returns:
            List[str]: 系统字体文件路径列表
        """
        pass
    
    @abstractmethod
    def get_preferred_fonts(self) -> List[str]:
        """
        获取当前平台推荐的中文字体列表
        
        Returns:
            List[str]: 推荐字体名称列表，按优先级排序
        """
        pass
    
    @abstractmethod
    def get_font_directories(self) -> List[Path]:
        """
        获取系统字体目录列表
        
        Returns:
            List[Path]: 字体目录路径列表
        """
        pass
    
    @abstractmethod
    def get_font_config_paths(self) -> List[Path]:
        """
        获取字体配置文件路径
        
        Returns:
            List[Path]: 字体配置文件路径列表
        """
        pass
    
    def get_font_extensions(self) -> Set[str]:
        """
        获取支持的字体文件扩展名
        
        Returns:
            Set[str]: 字体文件扩展名集合
        """
        return {'.ttf', '.otf', '.ttc', '.otc', '.woff', '.woff2'}
    
    def get_chinese_font_keywords(self) -> Set[str]:
        """
        获取中文字体识别关键词
        
        Returns:
            Set[str]: 中文字体关键词集合
        """
        # 通用关键词
        base_keywords = {
            'chinese', 'cjk', 'han', 'zh', 'cn', 'sc', 'tc',
            'unicode', 'fallback'
        }
        
        # 平台特定关键词
        platform_keywords = self.get_platform_specific_keywords()
        
        return base_keywords.union(platform_keywords)
    
    @abstractmethod
    def get_platform_specific_keywords(self) -> Set[str]:
        """
        获取平台特定的中文字体关键词
        
        Returns:
            Set[str]: 平台特定关键词集合
        """
        pass
    
    def validate_font_path(self, font_path: Path) -> bool:
        """
        验证字体路径是否有效
        
        Args:
            font_path: 字体文件路径
            
        Returns:
            bool: 路径是否有效
        """
        try:
            if not font_path.exists():
                return False
            
            if not font_path.is_file():
                return False
            
            # 检查文件扩展名
            if font_path.suffix.lower() not in self.get_font_extensions():
                return False
            
            # 检查文件大小
            if font_path.stat().st_size < 1024:  # 小于1KB
                return False
            
            return True
            
        except (OSError, IOError):
            return False
    
    def extract_font_metadata(self, font_path: Path) -> Optional[Dict[str, str]]:
        """
        提取字体元数据
        
        Args:
            font_path: 字体文件路径
            
        Returns:
            Optional[Dict[str, str]]: 字体元数据，提取失败返回None
        """
        # 基础实现：从文件名提取信息
        try:
            metadata = {
                'name': font_path.stem,
                'family': font_path.stem,
                'style': 'normal',
                'weight': 'normal',
                'path': str(font_path),
                'size': str(font_path.stat().st_size)
            }
            
            # 平台特定的元数据提取
            platform_metadata = self.extract_platform_metadata(font_path)
            if platform_metadata:
                metadata.update(platform_metadata)
            
            return metadata
            
        except Exception as e:
            self.logger.warning(f"提取字体元数据失败 {font_path}: {e}")
            return None
    
    def extract_platform_metadata(self, font_path: Path) -> Optional[Dict[str, str]]:
        """
        提取平台特定的字体元数据
        
        Args:
            font_path: 字体文件路径
            
        Returns:
            Optional[Dict[str, str]]: 平台特定元数据
        """
        # 默认实现：返回空字典
        return {}
    
    def is_chinese_font(self, font_name: str, font_path: Path) -> bool:
        """
        判断是否为中文字体
        
        Args:
            font_name: 字体名称
            font_path: 字体文件路径
            
        Returns:
            bool: 是否为中文字体
        """
        # 通过关键词判断
        keywords = self.get_chinese_font_keywords()
        name_lower = font_name.lower()
        path_lower = str(font_path).lower()
        
        for keyword in keywords:
            if keyword in name_lower or keyword in path_lower:
                return True
        
        # 通过文件大小判断（中文字体通常较大）
        try:
            file_size = font_path.stat().st_size
            if file_size > 5 * 1024 * 1024:  # 大于5MB
                return True
        except (OSError, IOError):
            pass
        
        # 平台特定的判断逻辑
        return self.is_chinese_font_platform_specific(font_name, font_path)
    
    def is_chinese_font_platform_specific(self, font_name: str, font_path: Path) -> bool:
        """
        平台特定的中文字体判断逻辑
        
        Args:
            font_name: 字体名称
            font_path: 字体文件路径
            
        Returns:
            bool: 是否为中文字体
        """
        # 默认实现：返回False
        return False
    
    def get_font_priority(self, font_name: str) -> int:
        """
        获取字体在当前平台的优先级
        
        Args:
            font_name: 字体名称
            
        Returns:
            int: 优先级（数字越小优先级越高）
        """
        preferred_fonts = self.get_preferred_fonts()
        
        # 标准化字体名称进行比较
        normalized_name = self.normalize_font_name(font_name)
        
        for i, preferred in enumerate(preferred_fonts):
            normalized_preferred = self.normalize_font_name(preferred)
            if normalized_preferred in normalized_name:
                return i + 1
        
        # 不在首选列表中的字体返回较低优先级
        return 999
    
    def normalize_font_name(self, font_name: str) -> str:
        """
        标准化字体名称
        
        Args:
            font_name: 原始字体名称
            
        Returns:
            str: 标准化后的字体名称
        """
        if not font_name:
            return ""
        
        # 移除多余空格并转换为小写
        normalized = ' '.join(font_name.split()).lower()
        
        # 移除常见的样式后缀
        suffixes = ['regular', 'bold', 'italic', 'light', 'medium', 'heavy']
        for suffix in suffixes:
            if normalized.endswith(f' {suffix}'):
                normalized = normalized[:-len(suffix)-1]
                break
        
        return normalized
    
    def get_fallback_fonts(self) -> List[str]:
        """
        获取备用字体列表
        
        Returns:
            List[str]: 备用字体名称列表
        """
        return [
            'DejaVu Sans',
            'Liberation Sans', 
            'Arial',
            'Helvetica',
            'sans-serif'
        ]
    
    def configure_matplotlib(self, font_name: str) -> bool:
        """
        配置matplotlib使用指定字体
        
        Args:
            font_name: 字体名称
            
        Returns:
            bool: 配置是否成功
        """
        try:
            import matplotlib.pyplot as plt
            import matplotlib.font_manager as fm
            
            # 设置字体
            font_list = [font_name] + self.get_fallback_fonts()
            plt.rcParams['font.sans-serif'] = font_list
            plt.rcParams['axes.unicode_minus'] = False
            
            # 清理字体缓存
            try:
                fm._rebuild()
            except:
                pass
            
            self.logger.info(f"matplotlib字体配置成功: {font_name}")
            return True
            
        except ImportError:
            self.logger.warning("matplotlib未安装，跳过字体配置")
            return False
        except Exception as e:
            self.logger.error(f"matplotlib字体配置失败: {e}")
            return False
    
    def get_system_info(self) -> Dict[str, str]:
        """
        获取系统信息
        
        Returns:
            Dict[str, str]: 系统信息字典
        """
        import platform
        
        return {
            'platform': self.platform.value,
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor()
        }
    
    def clear_cache(self):
        """清除字体缓存"""
        self._font_cache.clear()
        self.logger.info("平台适配器缓存已清除")
    
    @property
    def cache_size(self) -> int:
        """获取缓存大小"""
        return len(self._font_cache)