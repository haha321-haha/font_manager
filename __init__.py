#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Font Manager - 中文字体管理库

一个专门用于处理matplotlib中文字体显示的Python库。
提供自动字体检测、跨平台兼容性、配置管理和验证测试等功能。

主要功能:
- 自动检测和配置中文字体
- 跨平台兼容 (macOS/Windows/Linux)
- 字体样式管理
- 配置持久化
- 字体验证和测试

基本用法:
    from font_manager import FontManager
    
    # 一键设置中文字体
    fm = FontManager()
    result = fm.setup()
    
    if result.success:
        print(f"字体设置成功: {result.font_used.name}")
    else:
        print("字体设置失败，使用默认字体")

版本: 1.0.0
作者: Font Manager Team
许可: MIT License
"""

from .core.manager import FontManager
from .core.detector import FontDetector
from .core.config import ConfigManager
from .core.styles import StyleManager, FontStyleConfig
from .core.models import FontInfo, FontSetupResult, ValidationReport
from .core.exceptions import (
    FontManagerError,
    FontNotFoundError, 
    FontConfigError,
    PlatformNotSupportedError
)

# 版本信息
__version__ = "1.0.0"
__author__ = "Font Manager Team"
__license__ = "MIT"

# 公开API
__all__ = [
    # 主要类
    "FontManager",
    "FontDetector",
    "ConfigManager",
    "StyleManager",
    
    # 数据模型
    "FontInfo",
    "FontSetupResult", 
    "ValidationReport",
    "FontStyleConfig",
    
    # 异常类
    "FontManagerError",
    "FontNotFoundError",
    "FontConfigError", 
    "PlatformNotSupportedError",
    
    # 便捷函数
    "setup_chinese_font",
    "setup_matplotlib_chinese",
    "setup_matplotlib_chinese_robust",
    "get_available_fonts",
    "validate_font_config"
]

# 便捷函数
def setup_chinese_font(force_rebuild: bool = False) -> FontSetupResult:
    """
    便捷函数：一键设置中文字体
    
    Args:
        force_rebuild: 是否强制重建字体缓存
        
    Returns:
        FontSetupResult: 字体设置结果
    """
    manager = FontManager()
    return manager.setup(force_rebuild=force_rebuild)

def get_available_fonts():
    """
    便捷函数：获取可用字体列表
    
    Returns:
        List[FontInfo]: 可用字体列表
    """
    manager = FontManager()
    return manager.get_available_fonts()

def validate_font_config() -> ValidationReport:
    """
    便捷函数：验证当前字体配置
    
    Returns:
        ValidationReport: 验证报告
    """
    manager = FontManager()
    return manager.validate()

def setup_matplotlib_chinese(font_name: str = None, force_rebuild: bool = False) -> FontSetupResult:
    """
    便捷函数：设置matplotlib中文字体（兼容旧版API）
    
    Args:
        font_name: 指定字体名称，None表示自动选择最佳字体
        force_rebuild: 是否强制重建字体缓存
        
    Returns:
        FontSetupResult: 字体设置结果
    """
    manager = FontManager()
    return manager.setup_matplotlib_chinese(font_name=font_name, force_rebuild=force_rebuild)

def setup_matplotlib_chinese_robust(force_rebuild: bool = False) -> FontSetupResult:
    """
    便捷函数：健壮版matplotlib中文字体设置
    
    特点：
    - 强制使用Agg后端避免GUI问题
    - 智能字体检测和缓存
    - 内存安全的配置方式
    - 一次设置永久生效
    
    Args:
        force_rebuild: 是否强制重建字体缓存
        
    Returns:
        FontSetupResult: 字体设置结果
    """
    manager = FontManager()
    return manager.setup_matplotlib_chinese_robust(force_rebuild=force_rebuild)