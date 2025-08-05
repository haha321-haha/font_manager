#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Font Manager Platform Adapters

平台适配器模块，处理不同操作系统的字体差异。
"""

from .base import PlatformAdapter
from .factory import get_platform_adapter, get_supported_platforms, is_platform_supported

__all__ = [
    "PlatformAdapter",
    "get_platform_adapter",
    "get_supported_platforms", 
    "is_platform_supported"
]