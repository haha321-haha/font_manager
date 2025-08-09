#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Font Manager Helper Functions

提供通用的辅助函数。
"""

import os
import sys
import platform
from pathlib import Path
from typing import List, Optional, Union
import re

from ..core.models import Platform


def get_platform() -> Platform:
    """
    获取当前运行平台
    
    Returns:
        Platform: 平台枚举值
    """
    system = platform.system().lower()
    
    if system == "darwin":
        return Platform.MACOS
    elif system == "windows":
        return Platform.WINDOWS
    elif system == "linux":
        return Platform.LINUX
    else:
        return Platform.UNKNOWN


def is_font_file(file_path: Union[str, Path]) -> bool:
    """
    检查文件是否为字体文件
    
    Args:
        file_path: 文件路径
        
    Returns:
        bool: 是否为字体文件
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)
    
    if not file_path.exists() or not file_path.is_file():
        return False
    
    # 支持的字体文件扩展名
    font_extensions = {
        '.ttf',   # TrueType Font
        '.otf',   # OpenType Font
        '.ttc',   # TrueType Collection
        '.otc',   # OpenType Collection
        '.woff',  # Web Open Font Format
        '.woff2', # Web Open Font Format 2
        '.eot',   # Embedded OpenType
        '.pfb',   # PostScript Font Binary
        '.pfm',   # PostScript Font Metrics
        '.afm',   # Adobe Font Metrics
    }
    
    return file_path.suffix.lower() in font_extensions


def get_file_size(file_path: Union[str, Path]) -> int:
    """
    获取文件大小
    
    Args:
        file_path: 文件路径
        
    Returns:
        int: 文件大小（字节），文件不存在返回0
    """
    try:
        if isinstance(file_path, str):
            file_path = Path(file_path)
        
        if file_path.exists() and file_path.is_file():
            return file_path.stat().st_size
        else:
            return 0
    except (OSError, IOError):
        return 0


def normalize_font_name(font_name: str) -> str:
    """
    标准化字体名称
    
    Args:
        font_name: 原始字体名称
        
    Returns:
        str: 标准化后的字体名称
    """
    if not font_name:
        return ""
    
    # 移除多余的空格
    normalized = re.sub(r'\s+', ' ', font_name.strip())
    
    # 统一大小写（保持原有大小写，只处理特殊情况）
    # 处理常见的字体名称变体
    replacements = {
        'microsoft yahei': 'Microsoft YaHei',
        'simhei': 'SimHei',
        'simsun': 'SimSun',
        'pingfang sc': 'PingFang SC',
        'hiragino sans gb': 'Hiragino Sans GB',
        'arial unicode ms': 'Arial Unicode MS',
        'noto sans cjk': 'Noto Sans CJK',
        'wenquanyi': 'WenQuanYi'
    }
    
    normalized_lower = normalized.lower()
    for old, new in replacements.items():
        if old in normalized_lower:
            normalized = normalized.replace(old, new)
            break
    
    return normalized


def calculate_font_score(
    font_name: str,
    supports_chinese: bool,
    file_size: int,
    platform: Platform,
    preferred_fonts: Optional[List[str]] = None
) -> float:
    """
    计算字体质量评分
    
    Args:
        font_name: 字体名称
        supports_chinese: 是否支持中文
        file_size: 文件大小
        platform: 当前平台
        preferred_fonts: 首选字体列表
        
    Returns:
        float: 质量评分 (0-1)
    """
    score = 0.0
    
    # 中文支持 (40%)
    if supports_chinese:
        score += 0.4
    
    # 字体名称匹配度 (30%)
    if preferred_fonts:
        normalized_name = normalize_font_name(font_name)
        for i, preferred in enumerate(preferred_fonts):
            if normalize_font_name(preferred) in normalized_name:
                # 越靠前的字体得分越高
                score += 0.3 * (1.0 - i / len(preferred_fonts))
                break
    
    # 文件大小合理性 (20%)
    # 字体文件太小可能不完整，太大可能影响性能
    if file_size > 0:
        # 理想大小范围：1MB - 20MB
        ideal_min = 1024 * 1024      # 1MB
        ideal_max = 20 * 1024 * 1024 # 20MB
        
        if ideal_min <= file_size <= ideal_max:
            score += 0.2
        elif file_size < ideal_min:
            # 文件太小，按比例扣分
            score += 0.2 * (file_size / ideal_min)
        else:
            # 文件太大，按比例扣分
            score += 0.2 * (ideal_max / file_size)
    
    # 平台兼容性 (10%)
    platform_bonus = {
        Platform.MACOS: ['Hiragino', 'PingFang', 'STHeiti'],
        Platform.WINDOWS: ['Microsoft', 'SimHei', 'SimSun'],
        Platform.LINUX: ['Noto', 'WenQuanYi', 'Droid']
    }
    
    if platform in platform_bonus:
        for keyword in platform_bonus[platform]:
            if keyword.lower() in font_name.lower():
                score += 0.1
                break
    
    # 确保评分在0-1范围内
    return min(1.0, max(0.0, score))


def find_files_by_pattern(
    directory: Union[str, Path],
    pattern: str,
    recursive: bool = True
) -> List[Path]:
    """
    按模式查找文件
    
    Args:
        directory: 搜索目录
        pattern: 文件名模式 (支持通配符)
        recursive: 是否递归搜索
        
    Returns:
        List[Path]: 匹配的文件路径列表
    """
    if isinstance(directory, str):
        directory = Path(directory)
    
    if not directory.exists() or not directory.is_dir():
        return []
    
    try:
        if recursive:
            return list(directory.rglob(pattern))
        else:
            return list(directory.glob(pattern))
    except (OSError, IOError):
        return []


def safe_path_join(*parts: str) -> Path:
    """
    安全地连接路径组件
    
    Args:
        *parts: 路径组件
        
    Returns:
        Path: 连接后的路径
    """
    if not parts:
        return Path()
    
    # 过滤空字符串和None
    valid_parts = [part for part in parts if part]
    
    if not valid_parts:
        return Path()
    
    return Path(*valid_parts)


def ensure_directory(directory: Union[str, Path]) -> Path:
    """
    确保目录存在，不存在则创建
    
    Args:
        directory: 目录路径
        
    Returns:
        Path: 目录路径对象
    """
    if isinstance(directory, str):
        directory = Path(directory)
    
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def get_home_directory() -> Path:
    """
    获取用户主目录
    
    Returns:
        Path: 用户主目录路径
    """
    return Path.home()


def get_system_font_directories() -> List[Path]:
    """
    获取系统字体目录列表
    
    Returns:
        List[Path]: 字体目录路径列表
    """
    current_platform = get_platform()
    directories = []
    
    if current_platform == Platform.MACOS:
        directories.extend([
            Path("/System/Library/Fonts"),
            Path("/Library/Fonts"),
            Path.home() / "Library/Fonts"
        ])
    elif current_platform == Platform.WINDOWS:
        windows_dir = os.environ.get('WINDIR', 'C:\\Windows')
        directories.extend([
            Path(windows_dir) / "Fonts",
            Path.home() / "AppData/Local/Microsoft/Windows/Fonts"
        ])
    elif current_platform == Platform.LINUX:
        directories.extend([
            Path("/usr/share/fonts"),
            Path("/usr/local/share/fonts"),
            Path.home() / ".fonts",
            Path.home() / ".local/share/fonts"
        ])
    
    # 过滤存在的目录
    return [d for d in directories if d.exists() and d.is_dir()]