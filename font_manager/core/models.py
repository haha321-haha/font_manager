#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Font Manager Data Models

定义字体管理库使用的核心数据模型。
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum


class FontWeight(Enum):
    """字体粗细枚举"""
    THIN = 100
    EXTRA_LIGHT = 200
    LIGHT = 300
    NORMAL = 400
    MEDIUM = 500
    SEMI_BOLD = 600
    BOLD = 700
    EXTRA_BOLD = 800
    BLACK = 900


class FontStyle(Enum):
    """字体样式枚举"""
    NORMAL = "normal"
    ITALIC = "italic"
    OBLIQUE = "oblique"


class Platform(Enum):
    """支持的平台枚举"""
    MACOS = "darwin"
    WINDOWS = "win32"
    LINUX = "linux"
    UNKNOWN = "unknown"


@dataclass
class FontInfo:
    """
    字体信息数据模型
    
    包含字体的基本信息、路径、样式属性和质量评分等。
    """
    name: str                           # 字体名称
    path: str                           # 字体文件路径
    family: str                         # 字体族名
    style: FontStyle = FontStyle.NORMAL # 字体样式
    weight: FontWeight = FontWeight.NORMAL # 字体粗细
    supports_chinese: bool = False      # 是否支持中文
    quality_score: float = 0.0         # 质量评分 (0-1)
    platform_priority: int = 0         # 平台优先级 (数字越小优先级越高)
    file_size: int = 0                 # 文件大小 (字节)
    version: str = ""                  # 字体版本
    
    def __post_init__(self):
        """数据验证"""
        if not (0.0 <= self.quality_score <= 1.0):
            raise ValueError("quality_score must be between 0.0 and 1.0")
        if self.platform_priority < 0:
            raise ValueError("platform_priority must be non-negative")
    
    @property
    def is_bold(self) -> bool:
        """是否为粗体"""
        return self.weight.value >= FontWeight.SEMI_BOLD.value
    
    @property
    def is_italic(self) -> bool:
        """是否为斜体"""
        return self.style in (FontStyle.ITALIC, FontStyle.OBLIQUE)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'name': self.name,
            'path': self.path,
            'family': self.family,
            'style': self.style.value,
            'weight': self.weight.value,
            'supports_chinese': self.supports_chinese,
            'quality_score': self.quality_score,
            'platform_priority': self.platform_priority,
            'file_size': self.file_size,
            'version': self.version
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FontInfo':
        """从字典创建FontInfo实例"""
        return cls(
            name=data['name'],
            path=data['path'],
            family=data['family'],
            style=FontStyle(data.get('style', 'normal')),
            weight=FontWeight(data.get('weight', 400)),
            supports_chinese=data.get('supports_chinese', False),
            quality_score=data.get('quality_score', 0.0),
            platform_priority=data.get('platform_priority', 0),
            file_size=data.get('file_size', 0),
            version=data.get('version', '')
        )


@dataclass
class FontSetupResult:
    """
    字体设置结果数据模型
    
    包含字体设置操作的结果信息。
    """
    success: bool                       # 设置是否成功
    font_used: Optional[FontInfo] = None # 使用的字体
    fallback_fonts: List[str] = field(default_factory=list) # 备用字体列表
    warnings: List[str] = field(default_factory=list)       # 警告信息
    errors: List[str] = field(default_factory=list)         # 错误信息
    setup_time: float = 0.0            # 设置耗时 (秒)
    platform: Platform = Platform.UNKNOWN # 检测到的平台
    
    @property
    def has_warnings(self) -> bool:
        """是否有警告"""
        return len(self.warnings) > 0
    
    @property
    def has_errors(self) -> bool:
        """是否有错误"""
        return len(self.errors) > 0
    
    def add_warning(self, message: str):
        """添加警告信息"""
        self.warnings.append(message)
    
    def add_error(self, message: str):
        """添加错误信息"""
        self.errors.append(message)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'success': self.success,
            'font_used': self.font_used.to_dict() if self.font_used else None,
            'fallback_fonts': self.fallback_fonts,
            'warnings': self.warnings,
            'errors': self.errors,
            'setup_time': self.setup_time,
            'platform': self.platform.value
        }


@dataclass
class ValidationReport:
    """
    字体验证报告数据模型
    
    包含字体配置验证的详细结果。
    """
    font_available: bool = False        # 字体是否可用
    chinese_support: bool = False       # 是否支持中文
    render_quality: float = 0.0        # 渲染质量评分 (0-1)
    performance_score: float = 0.0     # 性能评分 (0-1)
    issues: List[str] = field(default_factory=list)           # 发现的问题
    recommendations: List[str] = field(default_factory=list)  # 改进建议
    test_results: Dict[str, bool] = field(default_factory=dict) # 测试结果
    font_info: Optional[FontInfo] = None # 当前使用的字体信息
    validation_time: float = 0.0       # 验证耗时 (秒)
    
    @property
    def overall_score(self) -> float:
        """综合评分"""
        scores = []
        if self.font_available:
            scores.append(0.3)  # 字体可用性权重30%
        if self.chinese_support:
            scores.append(0.3)  # 中文支持权重30%
        scores.append(self.render_quality * 0.2)  # 渲染质量权重20%
        scores.append(self.performance_score * 0.2)  # 性能权重20%
        
        return sum(scores)
    
    @property
    def status(self) -> str:
        """验证状态"""
        score = self.overall_score
        if score >= 0.8:
            return "优秀"
        elif score >= 0.6:
            return "良好"
        elif score >= 0.4:
            return "一般"
        else:
            return "需要改进"
    
    def add_issue(self, issue: str):
        """添加问题"""
        self.issues.append(issue)
    
    def add_recommendation(self, recommendation: str):
        """添加建议"""
        self.recommendations.append(recommendation)
    
    def set_test_result(self, test_name: str, result: bool):
        """设置测试结果"""
        self.test_results[test_name] = result
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'font_available': self.font_available,
            'chinese_support': self.chinese_support,
            'render_quality': self.render_quality,
            'performance_score': self.performance_score,
            'issues': self.issues,
            'recommendations': self.recommendations,
            'test_results': self.test_results,
            'font_info': self.font_info.to_dict() if self.font_info else None,
            'validation_time': self.validation_time,
            'overall_score': self.overall_score,
            'status': self.status
        }


@dataclass
class FontStyleConfig:
    """
    字体样式配置数据模型
    
    定义图表元素的字体样式。
    """
    font_family: str = ""               # 字体族
    font_size: int = 12                # 字体大小
    font_weight: FontWeight = FontWeight.NORMAL # 字体粗细
    font_style: FontStyle = FontStyle.NORMAL    # 字体样式
    color: str = "black"               # 字体颜色
    
    def to_matplotlib_props(self) -> Dict[str, Any]:
        """转换为matplotlib字体属性"""
        return {
            'fontfamily': self.font_family,
            'fontsize': self.font_size,
            'fontweight': self.font_weight.value,
            'fontstyle': self.font_style.value,
            'color': self.color
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'font_family': self.font_family,
            'font_size': self.font_size,
            'font_weight': self.font_weight.value,
            'font_style': self.font_style.value,
            'color': self.color
        }