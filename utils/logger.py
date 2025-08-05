#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Font Manager Logging Utilities

提供统一的日志记录功能。
"""

import logging
import sys
from typing import Optional
from pathlib import Path


class ColoredFormatter(logging.Formatter):
    """带颜色的日志格式化器"""
    
    # ANSI颜色代码
    COLORS = {
        'DEBUG': '\033[36m',    # 青色
        'INFO': '\033[32m',     # 绿色
        'WARNING': '\033[33m',  # 黄色
        'ERROR': '\033[31m',    # 红色
        'CRITICAL': '\033[35m', # 紫色
        'RESET': '\033[0m'      # 重置
    }
    
    def format(self, record):
        """格式化日志记录"""
        # 添加颜色
        if record.levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[record.levelname]}"
                f"{record.levelname}"
                f"{self.COLORS['RESET']}"
            )
        
        return super().format(record)


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    enable_color: bool = True,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    设置日志配置
    
    Args:
        level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: 日志文件路径，None表示不写入文件
        enable_color: 是否启用彩色输出
        format_string: 自定义格式字符串
        
    Returns:
        logging.Logger: 配置好的日志器
    """
    # 默认格式
    if format_string is None:
        format_string = (
            "%(asctime)s - %(name)s - %(levelname)s - "
            "%(filename)s:%(lineno)d - %(message)s"
        )
    
    # 获取根日志器
    logger = logging.getLogger("font_manager")
    logger.setLevel(getattr(logging, level.upper()))
    
    # 清除现有处理器
    logger.handlers.clear()
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    
    if enable_color and sys.stdout.isatty():
        console_formatter = ColoredFormatter(format_string)
    else:
        console_formatter = logging.Formatter(format_string)
    
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(getattr(logging, level.upper()))
        
        file_formatter = logging.Formatter(format_string)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    获取日志器实例
    
    Args:
        name: 日志器名称，None表示使用默认名称
        
    Returns:
        logging.Logger: 日志器实例
    """
    if name is None:
        name = "font_manager"
    elif not name.startswith("font_manager"):
        name = f"font_manager.{name}"
    
    logger = logging.getLogger(name)
    
    # 如果没有处理器，使用默认配置
    if not logger.handlers and not logger.parent.handlers:
        setup_logging()
    
    return logger


class LoggerMixin:
    """日志器混入类"""
    
    @property
    def logger(self) -> logging.Logger:
        """获取当前类的日志器"""
        class_name = self.__class__.__name__
        return get_logger(class_name.lower())


# 创建默认日志器
default_logger = get_logger()