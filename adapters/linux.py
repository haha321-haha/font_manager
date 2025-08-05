#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Linux Platform Adapter

Linux平台字体适配器，处理Linux系统特定的字体管理。
"""

import os
import subprocess
from typing import List, Dict, Optional, Set
from pathlib import Path

from ..core.models import Platform
from .base import PlatformAdapter


class LinuxAdapter(PlatformAdapter):
    """
    Linux平台适配器
    
    处理Linux系统的字体检测、配置和管理。
    """
    
    def __init__(self):
        """初始化Linux适配器"""
        super().__init__(Platform.LINUX)
        
        # Linux字体目录
        self._system_font_dirs = [
            Path("/usr/share/fonts"),
            Path("/usr/local/share/fonts"),
            Path("/usr/X11R6/lib/X11/fonts"),
            Path.home() / ".fonts",
            Path.home() / ".local/share/fonts"
        ]
        
        # fontconfig配置路径
        self._font_config_paths = [
            Path("/etc/fonts"),
            Path("/usr/share/fontconfig"),
            Path.home() / ".config/fontconfig"
        ]
    
    def get_system_fonts(self) -> List[str]:
        """
        获取Linux系统字体路径列表
        
        Returns:
            List[str]: 系统字体文件路径列表
        """
        font_paths = []
        
        # 尝试使用fc-list命令
        fc_list_fonts = self._get_fonts_from_fc_list()
        if fc_list_fonts:
            font_paths.extend(fc_list_fonts)
        else:
            # 备用方案：直接扫描字体目录
            for font_dir in self.get_font_directories():
                if not font_dir.exists():
                    continue
                
                try:
                    for ext in self.get_font_extensions():
                        pattern = f"**/*{ext}"
                        font_files = font_dir.glob(pattern)
                        font_paths.extend([str(f) for f in font_files if f.is_file()])
                        
                except Exception as e:
                    self.logger.warning(f"扫描字体目录失败 {font_dir}: {e}")
        
        # 去重并排序
        font_paths = list(set(font_paths))
        font_paths.sort()
        
        self.logger.info(f"Linux系统找到 {len(font_paths)} 个字体文件")
        return font_paths
    
    def _get_fonts_from_fc_list(self) -> List[str]:
        """
        使用fc-list命令获取字体列表
        
        Returns:
            List[str]: fc-list返回的字体路径列表
        """
        font_paths = []
        
        try:
            # 执行fc-list命令
            result = subprocess.run(
                ['fc-list', '--format=%{file}\n'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # 解析输出
                for line in result.stdout.strip().split('\n'):
                    font_path = line.strip()
                    if font_path and os.path.exists(font_path):
                        font_paths.append(font_path)
                        
                self.logger.info(f"fc-list找到 {len(font_paths)} 个字体")
            else:
                self.logger.warning(f"fc-list命令失败: {result.stderr}")
                
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
            self.logger.warning("fc-list命令不可用，使用备用方案")
        
        return font_paths
    
    def get_preferred_fonts(self) -> List[str]:
        """
        获取Linux推荐的中文字体列表
        
        Returns:
            List[str]: 推荐字体名称列表，按优先级排序
        """
        return [
            'Noto Sans CJK SC',      # Google Noto字体
            'Noto Sans CJK TC',      # 繁体中文
            'Source Han Sans SC',    # Adobe思源黑体
            'Source Han Sans TC',    # 繁体版本
            'WenQuanYi Zen Hei',     # 文泉驿正黑
            'WenQuanYi Micro Hei',   # 文泉驿微米黑
            'Droid Sans Fallback',   # Android字体
            'AR PL UMing CN',        # 文鼎字体
            'AR PL UKai CN',         # 文鼎楷体
            'DejaVu Sans'            # 备用字体
        ]
    
    def get_font_directories(self) -> List[Path]:
        """
        获取Linux字体目录列表
        
        Returns:
            List[Path]: 字体目录路径列表
        """
        return [d for d in self._system_font_dirs if d.exists()]
    
    def get_font_config_paths(self) -> List[Path]:
        """
        获取Linux字体配置文件路径
        
        Returns:
            List[Path]: 字体配置文件路径列表
        """
        config_paths = []
        
        for config_dir in self._font_config_paths:
            if config_dir.exists():
                # 查找.conf文件
                conf_files = config_dir.glob("**/*.conf")
                config_paths.extend(conf_files)
        
        return config_paths
    
    def get_platform_specific_keywords(self) -> Set[str]:
        """
        获取Linux特定的中文字体关键词
        
        Returns:
            Set[str]: Linux特定关键词集合
        """
        return {
            'noto', 'source', 'han', 'wenquanyi', 'zen', 'hei', 'micro',
            'droid', 'fallback', 'ar', 'pl', 'uming', 'ukai',
            'liberation', 'dejavu', 'gnu', 'freefont'
        }
    
    def is_chinese_font_platform_specific(self, font_name: str, font_path: Path) -> bool:
        """
        Linux特定的中文字体判断逻辑
        
        Args:
            font_name: 字体名称
            font_path: 字体文件路径
            
        Returns:
            bool: 是否为中文字体
        """
        # Linux特定的中文字体
        linux_chinese_fonts = {
            'noto sans cjk', 'source han sans', 'wenquanyi',
            'droid sans fallback', 'ar pl uming', 'ar pl ukai',
            'fireflysung', 'wqy'
        }
        
        name_lower = font_name.lower()
        for chinese_font in linux_chinese_fonts:
            if chinese_font in name_lower:
                return True
        
        return False
    
    def get_fontconfig_info(self) -> Dict[str, str]:
        """
        获取fontconfig配置信息
        
        Returns:
            Dict[str, str]: fontconfig信息
        """
        info = {}
        
        try:
            # 获取fontconfig版本
            result = subprocess.run(
                ['fc-list', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                info['fontconfig_version'] = result.stdout.strip()
            
            # 获取字体缓存信息
            result = subprocess.run(
                ['fc-cache', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                info['fc_cache_version'] = result.stdout.strip()
                
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
            pass
        
        return info
    
    def rebuild_font_cache(self) -> bool:
        """
        重建Linux字体缓存
        
        Returns:
            bool: 是否成功
        """
        try:
            result = subprocess.run(
                ['fc-cache', '-f', '-v'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                self.logger.info("Linux字体缓存重建成功")
                return True
            else:
                self.logger.warning(f"字体缓存重建失败: {result.stderr}")
                return False
                
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
            self.logger.warning("fc-cache命令不可用")
            return False
    
    def get_system_language(self) -> str:
        """
        获取Linux系统语言设置
        
        Returns:
            str: 系统语言代码
        """
        try:
            # 检查环境变量
            for var in ['LANG', 'LC_ALL', 'LC_MESSAGES']:
                lang = os.environ.get(var)
                if lang:
                    return lang.split('.')[0]  # 移除编码部分
            
            # 备用方案
            import locale
            return locale.getdefaultlocale()[0] or 'en_US'
            
        except:
            return 'en_US'
    
    def is_chinese_system(self) -> bool:
        """
        检查是否为中文Linux系统
        
        Returns:
            bool: 是否为中文系统
        """
        system_lang = self.get_system_language()
        return system_lang.startswith(('zh', 'cn'))
    
    def get_desktop_environment(self) -> str:
        """
        获取桌面环境信息
        
        Returns:
            str: 桌面环境名称
        """
        # 检查常见的桌面环境变量
        desktop_vars = [
            'XDG_CURRENT_DESKTOP',
            'DESKTOP_SESSION',
            'GDMSESSION'
        ]
        
        for var in desktop_vars:
            desktop = os.environ.get(var)
            if desktop:
                return desktop.lower()
        
        # 检查进程
        try:
            result = subprocess.run(
                ['ps', '-e'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                processes = result.stdout.lower()
                if 'gnome' in processes:
                    return 'gnome'
                elif 'kde' in processes or 'plasma' in processes:
                    return 'kde'
                elif 'xfce' in processes:
                    return 'xfce'
                elif 'lxde' in processes:
                    return 'lxde'
                    
        except (subprocess.TimeoutExpired, subprocess.SubprocessError):
            pass
        
        return 'unknown'
    
    def get_system_info(self) -> Dict[str, str]:
        """
        获取Linux系统信息
        
        Returns:
            Dict[str, str]: 系统信息字典
        """
        info = super().get_system_info()
        
        try:
            info['system_language'] = self.get_system_language()
            info['is_chinese_system'] = str(self.is_chinese_system())
            info['desktop_environment'] = self.get_desktop_environment()
            
            # fontconfig信息
            fontconfig_info = self.get_fontconfig_info()
            info.update(fontconfig_info)
            
            # 发行版信息
            try:
                with open('/etc/os-release', 'r') as f:
                    for line in f:
                        if line.startswith('NAME='):
                            info['distribution'] = line.split('=')[1].strip().strip('"')
                            break
            except FileNotFoundError:
                pass
                
        except Exception as e:
            self.logger.debug(f"获取Linux系统信息失败: {e}")
        
        return info