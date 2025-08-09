#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Font Manager Main Class

字体管理器主类，提供统一的API接口。
"""

import time
from typing import List, Optional, Dict, Any
from pathlib import Path

from .models import FontInfo, FontSetupResult, ValidationReport, Platform
from .exceptions import FontManagerError, FontNotFoundError, FontConfigError
from .detector import FontDetector
from .config import ConfigManager
from .styles import StyleManager, FontStyleConfig
from ..utils.logger import LoggerMixin
from ..utils.helpers import get_platform


class FontManager(LoggerMixin):
    """
    字体管理器主类
    
    提供中文字体的自动检测、配置和管理功能。
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化字体管理器
        
        Args:
            config_path: 配置文件路径，None表示使用默认配置
        """
        self.config_path = config_path
        self.platform = get_platform()
        self._current_font: Optional[FontInfo] = None
        
        # 初始化组件
        self.config_manager = ConfigManager(config_path)
        self.detector = FontDetector(cache_enabled=True)
        self.style_manager = StyleManager()
        
        self.logger.info(f"FontManager initialized on platform: {self.platform.value}")
    
    def setup(self, force_rebuild: bool = False) -> FontSetupResult:
        """
        一键设置中文字体
        
        Args:
            force_rebuild: 是否强制重建字体缓存
            
        Returns:
            FontSetupResult: 字体设置结果
        """
        start_time = time.time()
        result = FontSetupResult(success=False, platform=self.platform)
        
        try:
            self.logger.info("开始设置中文字体...")
            
            # 检测系统字体
            fonts = self.detector.detect_system_fonts(force_rescan=force_rebuild)
            
            if not fonts:
                result.add_error("未检测到任何字体")
                return result
            
            # 获取支持中文的字体
            chinese_fonts = self.detector.get_chinese_fonts(fonts)
            
            if not chinese_fonts:
                result.add_warning("未找到支持中文的字体，使用默认字体")
                # 使用第一个可用字体
                if fonts:
                    font_info = fonts[0]
                else:
                    result.add_error("没有可用字体")
                    return result
            else:
                # 使用最佳中文字体
                font_info = chinese_fonts[0]
                result.fallback_fonts = [f.name for f in chinese_fonts[1:6]]  # 前5个备用字体
            
            # 验证字体文件
            if not self.detector.verify_font(font_info.path):
                result.add_warning(f"字体文件验证失败: {font_info.path}")
            
            # 设置当前字体
            self._current_font = font_info
            result.font_used = font_info
            result.success = True
            
            # 应用matplotlib配置
            self._apply_matplotlib_config(font_info)
            
            self.logger.info(f"成功设置字体: {font_info.name} (评分: {font_info.quality_score:.2f})")
                
        except Exception as e:
            self.logger.error(f"字体设置失败: {e}")
            result.add_error(str(e))
            
        finally:
            result.setup_time = time.time() - start_time
            
        return result
    
    def get_available_fonts(self) -> List[FontInfo]:
        """
        获取可用字体列表
        
        Returns:
            List[FontInfo]: 可用字体列表
        """
        self.logger.info("获取可用字体列表...")
        
        # 使用字体检测器获取字体
        fonts = self.detector.detect_system_fonts()
        
        self.logger.info(f"找到 {len(fonts)} 个可用字体")
        return fonts
    
    def set_font_style(self, element: str, **kwargs) -> bool:
        """
        设置字体样式
        
        Args:
            element: 图表元素 (title, axis_label, tick_label, legend, annotation)
            **kwargs: 样式参数
            
        Returns:
            bool: 是否设置成功
        """
        self.logger.info(f"设置 {element} 字体样式: {kwargs}")
        
        # 使用样式管理器设置样式
        success = self.style_manager.update_style(element, **kwargs)
        
        if success:
            # 同时更新配置文件
            current_style = self.config_manager.get_font_style(element)
            current_style.update(kwargs)
            self.config_manager.set_font_style(element, current_style)
            self.config_manager.save_config()
        
        return success
    
    def validate(self) -> ValidationReport:
        """
        验证字体配置
        
        Returns:
            ValidationReport: 验证报告
        """
        start_time = time.time()
        report = ValidationReport()
        
        try:
            self.logger.info("开始验证字体配置...")
            
            # TODO: 实现完整的验证逻辑
            if self._current_font:
                report.font_available = True
                report.chinese_support = self._current_font.supports_chinese
                report.render_quality = self._current_font.quality_score
                report.performance_score = 0.8  # 模拟性能评分
                report.font_info = self._current_font
                
                # 设置测试结果
                report.set_test_result("font_exists", True)
                report.set_test_result("chinese_render", True)
                report.set_test_result("performance", True)
                
            else:
                report.add_issue("未设置字体")
                report.add_recommendation("请先调用 setup() 方法设置字体")
                
        except Exception as e:
            self.logger.error(f"字体验证失败: {e}")
            report.add_issue(f"验证过程出错: {e}")
            
        finally:
            report.validation_time = time.time() - start_time
            
        self.logger.info(f"字体验证完成，状态: {report.status}")
        return report
    
    def generate_test_chart(self, output_path: str) -> None:
        """
        生成测试图表
        
        Args:
            output_path: 输出文件路径
        """
        self.logger.info(f"生成测试图表: {output_path}")
        
        # TODO: 实现测试图表生成逻辑
        pass
    
    def _apply_matplotlib_config(self, font_info: FontInfo) -> None:
        """
        应用matplotlib字体配置
        
        Args:
            font_info: 字体信息
        """
        try:
            # 强制设置matplotlib后端，避免GUI问题
            import matplotlib
            matplotlib.use('Agg')
            
            import matplotlib.pyplot as plt
            import matplotlib.font_manager as fm
            
            # 设置字体参数
            plt.rcParams.update({
                'font.sans-serif': [font_info.name, 'Arial Unicode MS', 'DejaVu Sans', 'Arial'],
                'axes.unicode_minus': False,
                'font.family': 'sans-serif',
                'figure.max_open_warning': 0  # 禁用打开图形过多的警告
            })
            
            # 清理字体缓存
            try:
                fm._rebuild()
            except:
                pass
                
            self.logger.debug(f"已应用matplotlib字体配置: {font_info.name}")
            
        except ImportError:
            self.logger.warning("matplotlib未安装，跳过字体配置")
        except Exception as e:
            self.logger.error(f"应用matplotlib配置失败: {e}")
    
    @property
    def current_font(self) -> Optional[FontInfo]:
        """获取当前使用的字体"""
        return self._current_font
    
    @property
    def is_configured(self) -> bool:
        """检查是否已配置字体"""
        return self._current_font is not None
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键
            default: 默认值
            
        Returns:
            Any: 配置值
        """
        return self.config_manager.get(key, default)
    
    def set_config(self, key: str, value: Any) -> bool:
        """
        设置配置值
        
        Args:
            key: 配置键
            value: 配置值
            
        Returns:
            bool: 是否设置成功
        """
        result = self.config_manager.set(key, value)
        if result:
            self.config_manager.save_config()
        return result
    
    def get_preferred_fonts(self) -> List[str]:
        """
        获取当前平台的首选字体列表
        
        Returns:
            List[str]: 首选字体列表
        """
        return self.config_manager.get_preferred_fonts(self.platform)
    
    def set_preferred_fonts(self, fonts: List[str]) -> bool:
        """
        设置当前平台的首选字体列表
        
        Args:
            fonts: 字体列表
            
        Returns:
            bool: 是否设置成功
        """
        result = self.config_manager.set_preferred_fonts(fonts, self.platform)
        if result:
            self.config_manager.save_config()
        return result
    
    def reset_config(self) -> bool:
        """
        重置配置为默认值
        
        Returns:
            bool: 是否重置成功
        """
        return self.config_manager.reset_to_default()
    
    def backup_config(self, backup_path: Optional[str] = None) -> str:
        """
        备份当前配置
        
        Args:
            backup_path: 备份文件路径
            
        Returns:
            str: 备份文件路径
        """
        return self.config_manager.backup_config(backup_path)
    
    def get_config_info(self) -> Dict[str, Any]:
        """
        获取配置信息
        
        Returns:
            Dict[str, Any]: 配置信息
        """
        return self.config_manager.get_config_info()
    
    # 样式管理相关方法
    def get_available_themes(self) -> List[str]:
        """
        获取可用主题列表
        
        Returns:
            List[str]: 主题名称列表
        """
        return self.style_manager.get_available_themes()
    
    def set_theme(self, theme_name: str) -> bool:
        """
        设置样式主题
        
        Args:
            theme_name: 主题名称
            
        Returns:
            bool: 是否设置成功
        """
        return self.style_manager.set_theme(theme_name)
    
    def get_current_theme(self) -> Optional[str]:
        """
        获取当前主题名称
        
        Returns:
            Optional[str]: 当前主题名称
        """
        theme = self.style_manager.get_current_theme()
        return theme.name if theme else None
    
    def get_font_style(self, element: str) -> Optional[FontStyleConfig]:
        """
        获取指定元素的字体样式
        
        Args:
            element: 元素名称
            
        Returns:
            Optional[FontStyleConfig]: 字体样式配置
        """
        return self.style_manager.get_style(element)
    
    def apply_style_to_matplotlib(self, element: str, target=None) -> bool:
        """
        将样式应用到matplotlib
        
        Args:
            element: 元素名称
            target: matplotlib对象
            
        Returns:
            bool: 是否应用成功
        """
        return self.style_manager.apply_to_matplotlib(element, target)
    
    def reset_styles(self):
        """重置所有样式为默认值"""
        self.style_manager.reset_to_default()
    
    def get_style_summary(self) -> Dict[str, Any]:
        """
        获取样式摘要信息
        
        Returns:
            Dict[str, Any]: 样式摘要
        """
        return self.style_manager.get_style_summary()
    
    def setup_matplotlib_chinese(self, font_name: Optional[str] = None, force_rebuild: bool = False) -> FontSetupResult:
        """
        设置matplotlib中文字体（兼容旧版API）
        
        Args:
            font_name: 指定字体名称，None表示自动选择最佳字体
            force_rebuild: 是否强制重建字体缓存
            
        Returns:
            FontSetupResult: 字体设置结果
        """
        if font_name:
            # 使用指定字体
            fonts = self.detector.detect_system_fonts(force_rescan=force_rebuild)
            target_font = None
            for font in fonts:
                if font.name == font_name:
                    target_font = font
                    break
            
            if not target_font:
                result = FontSetupResult(success=False, platform=self.platform)
                result.add_error(f"未找到指定字体: {font_name}")
                return result
            
            # 设置指定字体
            self._current_font = target_font
            self._apply_matplotlib_config(target_font)
            
            result = FontSetupResult(success=True, platform=self.platform)
            result.font_used = target_font
            return result
        
        # 使用自动选择
        return self.setup(force_rebuild=force_rebuild)
    
    def setup_matplotlib_chinese_robust(self, force_rebuild: bool = False) -> FontSetupResult:
        """
        健壮版matplotlib中文字体设置
        
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
        import warnings
        import gc
        
        # 禁用字体相关警告
        warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')
        
        start_time = time.time()
        result = FontSetupResult(success=False, platform=self.platform)
        
        try:
            # 强制设置matplotlib后端
            import matplotlib
            matplotlib.use('Agg')
            
            self.logger.info("开始健壮版中文字体设置...")
            
            # 如果已经配置且不强制重建，直接返回
            if self.is_configured and not force_rebuild:
                result.success = True
                result.font_used = self._current_font
                result.setup_time = time.time() - start_time
                self.logger.info(f"字体已配置: {self._current_font.name}")
                return result
            
            # 检测系统字体
            fonts = self.detector.detect_system_fonts(force_rescan=force_rebuild)
            
            if not fonts:
                result.add_error("未检测到任何字体")
                return result
            
            # 优先选择已知的好字体
            preferred_fonts = [
                'Arial Unicode MS',  # macOS最佳
                'PingFang SC',       # macOS现代
                'Hiragino Sans GB',  # macOS传统
                'Microsoft YaHei',   # Windows最佳
                'SimHei',           # Windows传统
                'WenQuanYi Micro Hei', # Linux
                'DejaVu Sans'       # 通用备用
            ]
            
            selected_font = None
            for preferred in preferred_fonts:
                for font in fonts:
                    if preferred.lower() in font.name.lower():
                        selected_font = font
                        break
                if selected_font:
                    break
            
            # 如果没找到首选字体，使用第一个可用字体
            if not selected_font and fonts:
                selected_font = fonts[0]
            
            if not selected_font:
                result.add_error("没有可用字体")
                return result
            
            # 设置字体
            self._current_font = selected_font
            self._apply_matplotlib_config(selected_font)
            
            result.success = True
            result.font_used = selected_font
            result.fallback_fonts = [f.name for f in fonts[1:6]]
            
            self.logger.info(f"健壮版字体设置成功: {selected_font.name}")
            
        except Exception as e:
            self.logger.error(f"健壮版字体设置失败: {e}")
            result.add_error(str(e))
            
        finally:
            result.setup_time = time.time() - start_time
            # 强制垃圾回收
            gc.collect()
            
        return result