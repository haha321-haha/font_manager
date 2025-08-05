#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Font Manager Exception Classes

定义字体管理库使用的异常类。
"""

from typing import Optional, List


class FontManagerError(Exception):
    """
    字体管理器基础异常类
    
    所有字体管理相关异常的基类。
    """
    
    def __init__(self, message: str, details: Optional[str] = None, 
                 suggestions: Optional[List[str]] = None):
        """
        初始化异常
        
        Args:
            message: 错误消息
            details: 详细信息
            suggestions: 解决建议
        """
        super().__init__(message)
        self.message = message
        self.details = details
        self.suggestions = suggestions or []
    
    def __str__(self) -> str:
        """返回格式化的错误信息"""
        result = self.message
        
        if self.details:
            result += f"\n详细信息: {self.details}"
        
        if self.suggestions:
            result += "\n解决建议:"
            for i, suggestion in enumerate(self.suggestions, 1):
                result += f"\n  {i}. {suggestion}"
        
        return result
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            'error_type': self.__class__.__name__,
            'message': self.message,
            'details': self.details,
            'suggestions': self.suggestions
        }


class FontNotFoundError(FontManagerError):
    """
    字体未找到异常
    
    当系统中找不到合适的中文字体时抛出。
    """
    
    def __init__(self, font_name: Optional[str] = None, 
                 searched_paths: Optional[List[str]] = None):
        """
        初始化字体未找到异常
        
        Args:
            font_name: 查找的字体名称
            searched_paths: 搜索过的路径列表
        """
        if font_name:
            message = f"未找到字体: {font_name}"
        else:
            message = "未找到合适的中文字体"
        
        details = None
        if searched_paths:
            details = f"已搜索路径: {', '.join(searched_paths)}"
        
        suggestions = [
            "检查系统是否安装了中文字体",
            "尝试安装推荐的中文字体 (如 Hiragino Sans GB, PingFang SC)",
            "使用 FontManager.get_available_fonts() 查看可用字体",
            "检查字体文件路径是否正确"
        ]
        
        super().__init__(message, details, suggestions)
        self.font_name = font_name
        self.searched_paths = searched_paths or []


class FontConfigError(FontManagerError):
    """
    字体配置异常
    
    当字体配置文件有问题或配置过程失败时抛出。
    """
    
    def __init__(self, config_path: Optional[str] = None, 
                 config_error: Optional[str] = None):
        """
        初始化字体配置异常
        
        Args:
            config_path: 配置文件路径
            config_error: 配置错误详情
        """
        message = "字体配置错误"
        
        details = []
        if config_path:
            details.append(f"配置文件: {config_path}")
        if config_error:
            details.append(f"错误详情: {config_error}")
        
        suggestions = [
            "检查配置文件格式是否正确",
            "验证配置文件中的字体路径",
            "尝试删除配置文件使用默认配置",
            "查看日志获取更多错误信息"
        ]
        
        super().__init__(message, "; ".join(details) if details else None, suggestions)
        self.config_path = config_path
        self.config_error = config_error


class PlatformNotSupportedError(FontManagerError):
    """
    平台不支持异常
    
    当在不支持的平台上运行时抛出。
    """
    
    def __init__(self, platform: str, supported_platforms: Optional[List[str]] = None):
        """
        初始化平台不支持异常
        
        Args:
            platform: 当前平台
            supported_platforms: 支持的平台列表
        """
        message = f"不支持的平台: {platform}"
        
        details = None
        if supported_platforms:
            details = f"支持的平台: {', '.join(supported_platforms)}"
        
        suggestions = [
            "检查是否在支持的操作系统上运行",
            "联系开发者添加对新平台的支持",
            "尝试使用通用字体配置"
        ]
        
        super().__init__(message, details, suggestions)
        self.platform = platform
        self.supported_platforms = supported_platforms or []


class FontValidationError(FontManagerError):
    """
    字体验证异常
    
    当字体验证过程失败时抛出。
    """
    
    def __init__(self, validation_errors: List[str]):
        """
        初始化字体验证异常
        
        Args:
            validation_errors: 验证错误列表
        """
        message = "字体验证失败"
        details = "; ".join(validation_errors)
        
        suggestions = [
            "检查字体文件是否损坏",
            "验证字体是否支持中文字符",
            "尝试重新安装字体",
            "使用其他字体进行测试"
        ]
        
        super().__init__(message, details, suggestions)
        self.validation_errors = validation_errors


class FontCacheError(FontManagerError):
    """
    字体缓存异常
    
    当字体缓存操作失败时抛出。
    """
    
    def __init__(self, cache_operation: str, cache_path: Optional[str] = None):
        """
        初始化字体缓存异常
        
        Args:
            cache_operation: 缓存操作类型
            cache_path: 缓存路径
        """
        message = f"字体缓存操作失败: {cache_operation}"
        
        details = None
        if cache_path:
            details = f"缓存路径: {cache_path}"
        
        suggestions = [
            "检查缓存目录的读写权限",
            "尝试清理字体缓存",
            "重启应用程序",
            "检查磁盘空间是否充足"
        ]
        
        super().__init__(message, details, suggestions)
        self.cache_operation = cache_operation
        self.cache_path = cache_path


class FontRenderError(FontManagerError):
    """
    字体渲染异常
    
    当字体渲染测试失败时抛出。
    """
    
    def __init__(self, font_name: str, render_error: str):
        """
        初始化字体渲染异常
        
        Args:
            font_name: 字体名称
            render_error: 渲染错误详情
        """
        message = f"字体渲染失败: {font_name}"
        details = f"渲染错误: {render_error}"
        
        suggestions = [
            "检查字体文件是否完整",
            "验证matplotlib版本兼容性",
            "尝试使用其他字体",
            "检查系统图形驱动"
        ]
        
        super().__init__(message, details, suggestions)
        self.font_name = font_name
        self.render_error = render_error