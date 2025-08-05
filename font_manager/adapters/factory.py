#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Platform Adapter Factory

平台适配器工厂，根据当前平台自动创建相应的适配器实例。
"""

from typing import Optional

from ..core.models import Platform
from ..core.exceptions import PlatformNotSupportedError
from ..utils.helpers import get_platform
from ..utils.logger import get_logger

from .base import PlatformAdapter

# 延迟导入具体的适配器类，避免循环导入
_adapter_cache: Optional[PlatformAdapter] = None

logger = get_logger("adapter_factory")


def get_platform_adapter(platform: Optional[Platform] = None, force_reload: bool = False) -> PlatformAdapter:
    """
    获取平台适配器实例
    
    Args:
        platform: 指定平台，None表示自动检测
        force_reload: 是否强制重新创建适配器
        
    Returns:
        PlatformAdapter: 平台适配器实例
        
    Raises:
        PlatformNotSupportedError: 不支持的平台
    """
    global _adapter_cache
    
    # 检查缓存
    if not force_reload and _adapter_cache is not None:
        if platform is None or _adapter_cache.platform == platform:
            return _adapter_cache
    
    # 确定平台
    if platform is None:
        platform = get_platform()
    
    logger.info(f"创建平台适配器: {platform.value}")
    
    # 创建适配器实例
    try:
        if platform == Platform.MACOS:
            from .macos import MacOSAdapter
            adapter = MacOSAdapter()
        elif platform == Platform.WINDOWS:
            from .windows import WindowsAdapter
            adapter = WindowsAdapter()
        elif platform == Platform.LINUX:
            from .linux import LinuxAdapter
            adapter = LinuxAdapter()
        else:
            supported_platforms = [Platform.MACOS.value, Platform.WINDOWS.value, Platform.LINUX.value]
            raise PlatformNotSupportedError(
                platform.value,
                supported_platforms
            )
        
        # 缓存适配器
        _adapter_cache = adapter
        
        logger.info(f"平台适配器创建成功: {adapter.__class__.__name__}")
        return adapter
        
    except ImportError as e:
        logger.error(f"导入平台适配器失败: {e}")
        raise PlatformNotSupportedError(
            platform.value,
            ["macOS (部分支持)"]
        )
    except Exception as e:
        logger.error(f"创建平台适配器失败: {e}")
        raise


def clear_adapter_cache():
    """清除适配器缓存"""
    global _adapter_cache
    if _adapter_cache:
        _adapter_cache.clear_cache()
    _adapter_cache = None
    logger.info("适配器缓存已清除")


def get_supported_platforms() -> list[str]:
    """
    获取支持的平台列表
    
    Returns:
        List[str]: 支持的平台名称列表
    """
    return [Platform.MACOS.value, Platform.WINDOWS.value, Platform.LINUX.value]


def is_platform_supported(platform: Platform) -> bool:
    """
    检查平台是否支持
    
    Args:
        platform: 平台类型
        
    Returns:
        bool: 是否支持
    """
    return platform in [Platform.MACOS, Platform.WINDOWS, Platform.LINUX]