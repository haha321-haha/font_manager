#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows Platform Adapter

Windows平台字体适配器，处理Windows系统特定的字体管理。
"""

import os
import winreg
from typing import List, Dict, Optional, Set
from pathlib import Path

from ..core.models import Platform
from .base import PlatformAdapter


class WindowsAdapter(PlatformAdapter):
    """
    Windows平台适配器
    
    处理Windows系统的字体检测、配置和管理。
    """
    
    def __init__(self):
        """初始化Windows适配器"""
        super().__init__(Platform.WINDOWS)
        
        # Windows字体目录
        windows_dir = os.environ.get('WINDIR', 'C:\\Windows')
        self._system_font_dirs = [
            Path(windows_dir) / "Fonts",
            Path.home() / "AppData/Local/Microsoft/Windows/Fonts"
        ]
        
        # Windows字体注册表路径
        self._font_registry_key = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
    
    def get_system_fonts(self) -> List[str]:
        """
        获取Windows系统字体路径列表
        
        Returns:
            List[str]: 系统字体文件路径列表
        """
        font_paths = []
        
        # 从文件系统扫描
        for font_dir in self.get_font_directories():
            if not font_dir.exists():
                continue
            
            try:
                for ext in self.get_font_extensions():
                    pattern = f"*{ext}"
                    font_files = font_dir.glob(pattern)
                    font_paths.extend([str(f) for f in font_files if f.is_file()])
                    
            except Exception as e:
                self.logger.warning(f"扫描字体目录失败 {font_dir}: {e}")
        
        # 从注册表获取字体信息
        registry_fonts = self._get_fonts_from_registry()
        font_paths.extend(registry_fonts)
        
        # 去重并排序
        font_paths = list(set(font_paths))
        font_paths.sort()
        
        self.logger.info(f"Windows系统找到 {len(font_paths)} 个字体文件")
        return font_paths
    
    def _get_fonts_from_registry(self) -> List[str]:
        """
        从Windows注册表获取字体信息
        
        Returns:
            List[str]: 注册表中的字体路径列表
        """
        font_paths = []
        
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self._font_registry_key) as key:
                i = 0
                while True:
                    try:
                        font_name, font_file, _ = winreg.EnumValue(key, i)
                        
                        # 构建完整路径
                        if not os.path.isabs(font_file):
                            windows_dir = os.environ.get('WINDIR', 'C:\\Windows')
                            font_file = os.path.join(windows_dir, 'Fonts', font_file)
                        
                        if os.path.exists(font_file):
                            font_paths.append(font_file)
                        
                        i += 1
                        
                    except WindowsError:
                        break
                        
        except Exception as e:
            self.logger.warning(f"读取字体注册表失败: {e}")
        
        return font_paths
    
    def get_preferred_fonts(self) -> List[str]:
        """
        获取Windows推荐的中文字体列表
        
        Returns:
            List[str]: 推荐字体名称列表，按优先级排序
        """
        return [
            'Microsoft YaHei',       # 微软雅黑
            'Microsoft YaHei UI',    # 微软雅黑UI
            'SimHei',                # 黑体
            'SimSun',                # 宋体
            'NSimSun',               # 新宋体
            'FangSong',              # 仿宋
            'KaiTi',                 # 楷体
            'Microsoft JhengHei',    # 微软正黑体（繁体）
            'MingLiU',               # 细明体
            'Arial Unicode MS'       # Unicode字体
        ]
    
    def get_font_directories(self) -> List[Path]:
        """
        获取Windows字体目录列表
        
        Returns:
            List[Path]: 字体目录路径列表
        """
        return [d for d in self._system_font_dirs if d.exists()]
    
    def get_font_config_paths(self) -> List[Path]:
        """
        获取Windows字体配置文件路径
        
        Returns:
            List[Path]: 字体配置文件路径列表
        """
        # Windows主要通过注册表管理字体，配置文件较少
        return []
    
    def get_platform_specific_keywords(self) -> Set[str]:
        """
        获取Windows特定的中文字体关键词
        
        Returns:
            Set[str]: Windows特定关键词集合
        """
        return {
            'microsoft', 'yahei', 'simhei', 'simsun', 'nsimsun',
            'fangsong', 'kaiti', 'jhenghei', 'mingliu',
            'sim', 'ms', 'song', 'hei', 'kai', 'fang'
        }
    
    def is_chinese_font_platform_specific(self, font_name: str, font_path: Path) -> bool:
        """
        Windows特定的中文字体判断逻辑
        
        Args:
            font_name: 字体名称
            font_path: 字体文件路径
            
        Returns:
            bool: 是否为中文字体
        """
        # Windows特定的中文字体
        windows_chinese_fonts = {
            'microsoft yahei', 'yahei', 'simhei', 'simsun', 'nsimsun',
            'fangsong', 'kaiti', 'microsoft jhenghei', 'jhenghei',
            'mingliu', 'pmingliu', 'dfkai-sb'
        }
        
        name_lower = font_name.lower()
        for chinese_font in windows_chinese_fonts:
            if chinese_font in name_lower:
                return True
        
        return False
    
    def get_system_language(self) -> str:
        """
        获取Windows系统语言设置
        
        Returns:
            str: 系统语言代码
        """
        try:
            import locale
            return locale.getdefaultlocale()[0] or 'en_US'
        except:
            return 'en_US'
    
    def is_chinese_system(self) -> bool:
        """
        检查是否为中文Windows系统
        
        Returns:
            bool: 是否为中文系统
        """
        system_lang = self.get_system_language()
        return system_lang.startswith(('zh', 'cn'))
    
    def get_system_info(self) -> Dict[str, str]:
        """
        获取Windows系统信息
        
        Returns:
            Dict[str, str]: 系统信息字典
        """
        info = super().get_system_info()
        
        try:
            info['system_language'] = self.get_system_language()
            info['is_chinese_system'] = str(self.is_chinese_system())
            
            # Windows版本信息
            import platform
            info['windows_version'] = platform.win32_ver()[0]
            info['windows_edition'] = platform.win32_edition()
            
        except Exception as e:
            self.logger.debug(f"获取Windows系统信息失败: {e}")
        
        return info