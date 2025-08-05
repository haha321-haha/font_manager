#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Font Manager Core Module

核心模块包含字体管理的主要功能组件。
"""

from .manager import FontManager
from .models import FontInfo, FontSetupResult, ValidationReport
from .exceptions import (
    FontManagerError,
    FontNotFoundError,
    FontConfigError,
    PlatformNotSupportedError
)

__all__ = [
    "FontManager",
    "FontInfo",
    "FontSetupResult", 
    "ValidationReport",
    "FontManagerError",
    "FontNotFoundError",
    "FontConfigError",
    "PlatformNotSupportedError"
]