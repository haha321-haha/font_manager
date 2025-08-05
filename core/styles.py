#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Style Manager

样式管理器，负责字体样式的定义、应用和管理。
"""

from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, asdict
from enum import Enum

from .models import FontWeight, FontStyle
from .exceptions import FontConfigError
from ..utils.logger import LoggerMixin


class ElementType(Enum):
    """图表元素类型枚举"""
    TITLE = "title"
    SUBTITLE = "subtitle"
    AXIS_LABEL = "axis_label"
    TICK_LABEL = "tick_label"
    LEGEND = "legend"
    ANNOTATION = "annotation"
    TEXT = "text"
    WATERMARK = "watermark"


@dataclass
class FontStyleConfig:
    """
    字体样式配置
    
    定义单个图表元素的字体样式属性。
    """
    font_family: str = ""               # 字体族
    font_size: int = 12                # 字体大小
    font_weight: Union[int, str] = 400  # 字体粗细
    font_style: str = "normal"         # 字体样式
    color: str = "black"               # 字体颜色
    alpha: float = 1.0                 # 透明度
    
    def __post_init__(self):
        """数据验证"""
        if self.font_size <= 0:
            raise ValueError("font_size must be positive")
        if not (0.0 <= self.alpha <= 1.0):
            raise ValueError("alpha must be between 0.0 and 1.0")
    
    def to_matplotlib_props(self) -> Dict[str, Any]:
        """转换为matplotlib字体属性"""
        props = {
            'fontsize': self.font_size,
            'color': self.color,
            'alpha': self.alpha
        }
        
        # 添加字体族（如果指定）
        if self.font_family:
            props['fontfamily'] = self.font_family
        
        # 处理字体粗细
        if isinstance(self.font_weight, int):
            if self.font_weight >= 700:
                props['fontweight'] = 'bold'
            elif self.font_weight <= 300:
                props['fontweight'] = 'light'
            else:
                props['fontweight'] = 'normal'
        else:
            props['fontweight'] = self.font_weight
        
        # 处理字体样式
        props['fontstyle'] = self.font_style
        
        return props
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FontStyleConfig':
        """从字典创建FontStyleConfig实例"""
        return cls(**data)
    
    def copy(self) -> 'FontStyleConfig':
        """创建副本"""
        return FontStyleConfig(**asdict(self))
    
    def update(self, **kwargs) -> 'FontStyleConfig':
        """更新样式属性"""
        data = asdict(self)
        data.update(kwargs)
        return FontStyleConfig(**data)


class StyleTheme:
    """
    样式主题
    
    定义一套完整的字体样式主题。
    """
    
    def __init__(self, name: str, styles: Dict[str, FontStyleConfig]):
        """
        初始化样式主题
        
        Args:
            name: 主题名称
            styles: 样式配置字典
        """
        self.name = name
        self.styles = styles
    
    def get_style(self, element: str) -> Optional[FontStyleConfig]:
        """获取指定元素的样式"""
        return self.styles.get(element)
    
    def set_style(self, element: str, style: FontStyleConfig):
        """设置指定元素的样式"""
        self.styles[element] = style
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'name': self.name,
            'styles': {k: v.to_dict() for k, v in self.styles.items()}
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StyleTheme':
        """从字典创建StyleTheme实例"""
        styles = {k: FontStyleConfig.from_dict(v) for k, v in data['styles'].items()}
        return cls(data['name'], styles)


class StyleManager(LoggerMixin):
    """
    样式管理器
    
    负责字体样式的定义、应用和管理。
    """
    
    def __init__(self):
        """初始化样式管理器"""
        self._current_theme: Optional[StyleTheme] = None
        self._custom_styles: Dict[str, FontStyleConfig] = {}
        self._themes: Dict[str, StyleTheme] = {}
        
        # 初始化默认主题
        self._init_default_themes()
        
        self.logger.info("StyleManager initialized")
    
    def _init_default_themes(self):
        """初始化默认主题"""
        # 默认主题
        default_styles = {
            ElementType.TITLE.value: FontStyleConfig(
                font_size=16, font_weight=700, color="black"
            ),
            ElementType.SUBTITLE.value: FontStyleConfig(
                font_size=14, font_weight=600, color="darkgray"
            ),
            ElementType.AXIS_LABEL.value: FontStyleConfig(
                font_size=12, font_weight=600, color="black"
            ),
            ElementType.TICK_LABEL.value: FontStyleConfig(
                font_size=10, font_weight=400, color="black"
            ),
            ElementType.LEGEND.value: FontStyleConfig(
                font_size=10, font_weight=400, color="black"
            ),
            ElementType.ANNOTATION.value: FontStyleConfig(
                font_size=9, font_weight=400, color="gray"
            ),
            ElementType.TEXT.value: FontStyleConfig(
                font_size=11, font_weight=400, color="black"
            ),
            ElementType.WATERMARK.value: FontStyleConfig(
                font_size=8, font_weight=300, color="lightgray", alpha=0.5
            )
        }
        
        self._themes["default"] = StyleTheme("默认主题", default_styles)
        
        # 学术论文主题
        academic_styles = {
            ElementType.TITLE.value: FontStyleConfig(
                font_size=14, font_weight=700, color="black"
            ),
            ElementType.SUBTITLE.value: FontStyleConfig(
                font_size=12, font_weight=600, color="black"
            ),
            ElementType.AXIS_LABEL.value: FontStyleConfig(
                font_size=11, font_weight=500, color="black"
            ),
            ElementType.TICK_LABEL.value: FontStyleConfig(
                font_size=9, font_weight=400, color="black"
            ),
            ElementType.LEGEND.value: FontStyleConfig(
                font_size=9, font_weight=400, color="black"
            ),
            ElementType.ANNOTATION.value: FontStyleConfig(
                font_size=8, font_weight=400, color="darkgray"
            ),
            ElementType.TEXT.value: FontStyleConfig(
                font_size=10, font_weight=400, color="black"
            ),
            ElementType.WATERMARK.value: FontStyleConfig(
                font_size=7, font_weight=300, color="lightgray", alpha=0.3
            )
        }
        
        self._themes["academic"] = StyleTheme("学术论文", academic_styles)
        
        # 商业报告主题
        business_styles = {
            ElementType.TITLE.value: FontStyleConfig(
                font_size=18, font_weight=800, color="navy"
            ),
            ElementType.SUBTITLE.value: FontStyleConfig(
                font_size=15, font_weight=600, color="darkblue"
            ),
            ElementType.AXIS_LABEL.value: FontStyleConfig(
                font_size=13, font_weight=600, color="black"
            ),
            ElementType.TICK_LABEL.value: FontStyleConfig(
                font_size=11, font_weight=400, color="black"
            ),
            ElementType.LEGEND.value: FontStyleConfig(
                font_size=11, font_weight=500, color="black"
            ),
            ElementType.ANNOTATION.value: FontStyleConfig(
                font_size=10, font_weight=400, color="darkgreen"
            ),
            ElementType.TEXT.value: FontStyleConfig(
                font_size=12, font_weight=400, color="black"
            ),
            ElementType.WATERMARK.value: FontStyleConfig(
                font_size=9, font_weight=300, color="lightblue", alpha=0.4
            )
        }
        
        self._themes["business"] = StyleTheme("商业报告", business_styles)
        
        # 设置默认主题
        self._current_theme = self._themes["default"]
    
    def get_available_themes(self) -> List[str]:
        """获取可用主题列表"""
        return list(self._themes.keys())
    
    def get_current_theme(self) -> Optional[StyleTheme]:
        """获取当前主题"""
        return self._current_theme
    
    def set_theme(self, theme_name: str) -> bool:
        """
        设置当前主题
        
        Args:
            theme_name: 主题名称
            
        Returns:
            bool: 是否设置成功
        """
        if theme_name in self._themes:
            self._current_theme = self._themes[theme_name]
            self.logger.info(f"主题已切换到: {theme_name}")
            return True
        else:
            self.logger.warning(f"主题不存在: {theme_name}")
            return False
    
    def create_theme(self, name: str, base_theme: Optional[str] = None) -> StyleTheme:
        """
        创建新主题
        
        Args:
            name: 主题名称
            base_theme: 基础主题名称，None表示从默认主题复制
            
        Returns:
            StyleTheme: 新创建的主题
        """
        if base_theme and base_theme in self._themes:
            base = self._themes[base_theme]
            styles = {k: v.copy() for k, v in base.styles.items()}
        else:
            base = self._themes["default"]
            styles = {k: v.copy() for k, v in base.styles.items()}
        
        theme = StyleTheme(name, styles)
        self._themes[name] = theme
        
        self.logger.info(f"新主题已创建: {name}")
        return theme
    
    def delete_theme(self, theme_name: str) -> bool:
        """
        删除主题
        
        Args:
            theme_name: 主题名称
            
        Returns:
            bool: 是否删除成功
        """
        if theme_name in ["default", "academic", "business"]:
            self.logger.warning(f"无法删除内置主题: {theme_name}")
            return False
        
        if theme_name in self._themes:
            del self._themes[theme_name]
            
            # 如果删除的是当前主题，切换到默认主题
            if self._current_theme and self._current_theme.name == theme_name:
                self._current_theme = self._themes["default"]
            
            self.logger.info(f"主题已删除: {theme_name}")
            return True
        else:
            self.logger.warning(f"主题不存在: {theme_name}")
            return False
    
    def get_style(self, element: str) -> Optional[FontStyleConfig]:
        """
        获取指定元素的样式
        
        Args:
            element: 元素名称
            
        Returns:
            Optional[FontStyleConfig]: 样式配置
        """
        # 优先使用自定义样式
        if element in self._custom_styles:
            return self._custom_styles[element]
        
        # 使用当前主题的样式
        if self._current_theme:
            return self._current_theme.get_style(element)
        
        return None
    
    def set_style(self, element: str, style: Union[FontStyleConfig, Dict[str, Any]]) -> bool:
        """
        设置指定元素的样式
        
        Args:
            element: 元素名称
            style: 样式配置
            
        Returns:
            bool: 是否设置成功
        """
        try:
            if isinstance(style, dict):
                style_config = FontStyleConfig.from_dict(style)
            else:
                style_config = style
            
            self._custom_styles[element] = style_config
            self.logger.info(f"样式已设置: {element}")
            return True
            
        except Exception as e:
            self.logger.error(f"设置样式失败: {e}")
            return False
    
    def update_style(self, element: str, **kwargs) -> bool:
        """
        更新指定元素的样式属性
        
        Args:
            element: 元素名称
            **kwargs: 样式属性
            
        Returns:
            bool: 是否更新成功
        """
        current_style = self.get_style(element)
        if current_style:
            try:
                updated_style = current_style.update(**kwargs)
                self._custom_styles[element] = updated_style
                self.logger.info(f"样式已更新: {element}")
                return True
            except Exception as e:
                self.logger.error(f"更新样式失败: {e}")
                return False
        else:
            # 如果没有现有样式，创建新样式
            try:
                new_style = FontStyleConfig(**kwargs)
                self._custom_styles[element] = new_style
                self.logger.info(f"新样式已创建: {element}")
                return True
            except Exception as e:
                self.logger.error(f"创建样式失败: {e}")
                return False
    
    def remove_custom_style(self, element: str) -> bool:
        """
        移除自定义样式，恢复主题默认样式
        
        Args:
            element: 元素名称
            
        Returns:
            bool: 是否移除成功
        """
        if element in self._custom_styles:
            del self._custom_styles[element]
            self.logger.info(f"自定义样式已移除: {element}")
            return True
        else:
            self.logger.warning(f"没有自定义样式: {element}")
            return False
    
    def clear_custom_styles(self):
        """清除所有自定义样式"""
        self._custom_styles.clear()
        self.logger.info("所有自定义样式已清除")
    
    def apply_to_matplotlib(self, element: str, target=None) -> bool:
        """
        将样式应用到matplotlib对象
        
        Args:
            element: 元素名称
            target: matplotlib对象，None表示应用到rcParams
            
        Returns:
            bool: 是否应用成功
        """
        style = self.get_style(element)
        if not style:
            self.logger.warning(f"样式不存在: {element}")
            return False
        
        try:
            props = style.to_matplotlib_props()
            
            if target is None:
                # 应用到全局rcParams
                import matplotlib.pyplot as plt
                
                if element == ElementType.TITLE.value:
                    plt.rcParams.update({
                        'axes.titlesize': props['fontsize'],
                        'axes.titleweight': props.get('fontweight', 'normal'),
                        'axes.titlecolor': props['color']
                    })
                elif element == ElementType.AXIS_LABEL.value:
                    plt.rcParams.update({
                        'axes.labelsize': props['fontsize'],
                        'axes.labelweight': props.get('fontweight', 'normal'),
                        'axes.labelcolor': props['color']
                    })
                elif element == ElementType.TICK_LABEL.value:
                    plt.rcParams.update({
                        'xtick.labelsize': props['fontsize'],
                        'ytick.labelsize': props['fontsize'],
                        'xtick.color': props['color'],
                        'ytick.color': props['color']
                    })
                elif element == ElementType.LEGEND.value:
                    plt.rcParams.update({
                        'legend.fontsize': props['fontsize']
                    })
                
            else:
                # 应用到特定对象
                if hasattr(target, 'set_fontsize'):
                    target.set_fontsize(props['fontsize'])
                if hasattr(target, 'set_color'):
                    target.set_color(props['color'])
                if hasattr(target, 'set_weight'):
                    target.set_weight(props.get('fontweight', 'normal'))
                if hasattr(target, 'set_style'):
                    target.set_style(props.get('fontstyle', 'normal'))
            
            self.logger.debug(f"样式已应用到matplotlib: {element}")
            return True
            
        except Exception as e:
            self.logger.error(f"应用样式到matplotlib失败: {e}")
            return False
    
    def get_style_summary(self) -> Dict[str, Any]:
        """
        获取样式摘要信息
        
        Returns:
            Dict[str, Any]: 样式摘要
        """
        summary = {
            'current_theme': self._current_theme.name if self._current_theme else None,
            'available_themes': self.get_available_themes(),
            'custom_styles_count': len(self._custom_styles),
            'custom_styles': list(self._custom_styles.keys())
        }
        
        if self._current_theme:
            summary['theme_styles'] = list(self._current_theme.styles.keys())
        
        return summary
    
    def export_theme(self, theme_name: str) -> Optional[Dict[str, Any]]:
        """
        导出主题配置
        
        Args:
            theme_name: 主题名称
            
        Returns:
            Optional[Dict[str, Any]]: 主题配置字典
        """
        if theme_name in self._themes:
            return self._themes[theme_name].to_dict()
        else:
            self.logger.warning(f"主题不存在: {theme_name}")
            return None
    
    def import_theme(self, theme_data: Dict[str, Any]) -> bool:
        """
        导入主题配置
        
        Args:
            theme_data: 主题配置字典
            
        Returns:
            bool: 是否导入成功
        """
        try:
            theme = StyleTheme.from_dict(theme_data)
            self._themes[theme.name] = theme
            self.logger.info(f"主题已导入: {theme.name}")
            return True
        except Exception as e:
            self.logger.error(f"导入主题失败: {e}")
            return False
    
    def reset_to_default(self):
        """重置为默认状态"""
        self._custom_styles.clear()
        self._current_theme = self._themes["default"]
        self.logger.info("样式管理器已重置为默认状态")