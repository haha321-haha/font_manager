#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Font Manager Utils Module

工具模块包含日志、辅助函数等通用功能。
"""

from .logger import get_logger, setup_logging
from .helpers import (
    get_platform,
    is_font_file,
    get_file_size,
    calculate_font_score,
    normalize_font_name
)

__all__ = [
    "get_logger",
    "setup_logging", 
    "get_platform",
    "is_font_file",
    "get_file_size",
    "calculate_font_score",
    "normalize_font_name"
]