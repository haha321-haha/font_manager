#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration Manager

配置管理器，负责字体配置的读取、保存和验证。
"""

import json
import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from dataclasses import asdict
import time

from .models import Platform, FontStyleConfig
from .exceptions import FontConfigError
from ..utils.logger import LoggerMixin
from ..utils.helpers import get_platform, ensure_directory


class ConfigManager(LoggerMixin):
    """
    配置管理器
    
    负责字体配置文件的读取、保存、验证和迁移。
    支持JSON和YAML格式。
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置管理器
        
        Args:
            config_path: 配置文件路径，None表示使用默认路径
        """
        self.platform = get_platform()
        
        # 确定配置文件路径
        if config_path:
            self.config_path = Path(config_path)
        else:
            self.config_path = self._get_default_config_path()
        
        # 配置数据
        self._config: Dict[str, Any] = {}
        self._config_loaded = False
        self._last_modified = 0.0
        
        # 默认配置
        self._default_config = self._get_default_config()
        
        self.logger.info(f"ConfigManager initialized, config path: {self.config_path}")
    
    def _get_default_config_path(self) -> Path:
        """
        获取默认配置文件路径
        
        Returns:
            Path: 默认配置文件路径
        """
        # 用户配置目录
        if self.platform == Platform.MACOS:
            config_dir = Path.home() / "Library/Application Support/FontManager"
        elif self.platform == Platform.WINDOWS:
            config_dir = Path.home() / "AppData/Roaming/FontManager"
        else:  # Linux
            config_dir = Path.home() / ".config/fontmanager"
        
        ensure_directory(config_dir)
        return config_dir / "config.json"
    
    def _get_default_config(self) -> Dict[str, Any]:
        """
        获取默认配置
        
        Returns:
            Dict[str, Any]: 默认配置字典
        """
        return {
            "font_config": {
                "auto_detect": True,
                "force_rebuild_cache": False,
                "preferred_fonts": {
                    "macos": [
                        "Hiragino Sans GB",
                        "PingFang SC",
                        "STHeiti",
                        "Arial Unicode MS"
                    ],
                    "windows": [
                        "Microsoft YaHei",
                        "SimHei",
                        "SimSun",
                        "Arial Unicode MS"
                    ],
                    "linux": [
                        "Noto Sans CJK SC",
                        "WenQuanYi Zen Hei",
                        "Droid Sans Fallback",
                        "Arial Unicode MS"
                    ]
                },
                "fallback_fonts": [
                    "DejaVu Sans",
                    "Liberation Sans",
                    "Arial",
                    "Helvetica"
                ],
                "styles": {
                    "title": {
                        "font_size": 16,
                        "font_weight": 700,
                        "font_style": "normal",
                        "color": "black"
                    },
                    "axis_label": {
                        "font_size": 12,
                        "font_weight": 600,
                        "font_style": "normal",
                        "color": "black"
                    },
                    "tick_label": {
                        "font_size": 10,
                        "font_weight": 400,
                        "font_style": "normal",
                        "color": "black"
                    },
                    "legend": {
                        "font_size": 10,
                        "font_weight": 400,
                        "font_style": "normal",
                        "color": "black"
                    },
                    "annotation": {
                        "font_size": 9,
                        "font_weight": 400,
                        "font_style": "normal",
                        "color": "gray"
                    }
                }
            },
            "validation": {
                "enable_chinese_test": True,
                "enable_render_test": True,
                "enable_performance_test": True,
                "test_characters": "中文字体测试 Chinese Font Test 测试图表",
                "performance_threshold": 1.0
            },
            "logging": {
                "level": "INFO",
                "enable_file_logging": False,
                "log_file": None,
                "enable_color": True
            },
            "cache": {
                "enable_cache": True,
                "cache_ttl": 3600,
                "max_cache_size": 100
            },
            "version": "1.0.0",
            "created_at": time.time(),
            "updated_at": time.time()
        }
    
    def load_config(self, force_reload: bool = False) -> Dict[str, Any]:
        """
        加载配置文件
        
        Args:
            force_reload: 是否强制重新加载
            
        Returns:
            Dict[str, Any]: 配置字典
            
        Raises:
            FontConfigError: 配置加载失败
        """
        # 检查是否需要重新加载
        if not force_reload and self._config_loaded:
            if self.config_path.exists():
                current_modified = self.config_path.stat().st_mtime
                if current_modified <= self._last_modified:
                    return self._config
        
        try:
            if not self.config_path.exists():
                self.logger.info("配置文件不存在，使用默认配置")
                self._config = self._default_config.copy()
                self.save_config()  # 保存默认配置
            else:
                # 读取配置文件
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    if self.config_path.suffix.lower() == '.yaml' or self.config_path.suffix.lower() == '.yml':
                        self._config = yaml.safe_load(f) or {}
                    else:
                        self._config = json.load(f)
                
                # 验证配置
                self._validate_config(self._config)
                
                # 合并默认配置（处理新增的配置项）
                self._config = self._merge_config(self._default_config, self._config)
                
                # 更新时间戳
                self._last_modified = self.config_path.stat().st_mtime
                
                self.logger.info(f"配置文件加载成功: {self.config_path}")
            
            self._config_loaded = True
            return self._config
            
        except (json.JSONDecodeError, yaml.YAMLError) as e:
            error_msg = f"配置文件格式错误: {e}"
            self.logger.error(error_msg)
            raise FontConfigError(str(self.config_path), error_msg)
        except Exception as e:
            error_msg = f"加载配置文件失败: {e}"
            self.logger.error(error_msg)
            raise FontConfigError(str(self.config_path), error_msg)
    
    def save_config(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """
        保存配置文件
        
        Args:
            config: 要保存的配置，None表示保存当前配置
            
        Returns:
            bool: 是否保存成功
            
        Raises:
            FontConfigError: 配置保存失败
        """
        if config is None:
            config = self._config
        
        try:
            # 确保目录存在
            ensure_directory(self.config_path.parent)
            
            # 更新时间戳
            config["updated_at"] = time.time()
            
            # 保存配置文件
            with open(self.config_path, 'w', encoding='utf-8') as f:
                if self.config_path.suffix.lower() == '.yaml' or self.config_path.suffix.lower() == '.yml':
                    yaml.dump(config, f, default_flow_style=False, allow_unicode=True, indent=2)
                else:
                    json.dump(config, f, indent=2, ensure_ascii=False)
            
            # 更新内部状态
            self._config = config
            self._last_modified = self.config_path.stat().st_mtime
            
            self.logger.info(f"配置文件保存成功: {self.config_path}")
            return True
            
        except Exception as e:
            error_msg = f"保存配置文件失败: {e}"
            self.logger.error(error_msg)
            raise FontConfigError(str(self.config_path), error_msg)
    
    def _validate_config(self, config: Dict[str, Any]) -> bool:
        """
        验证配置文件格式
        
        Args:
            config: 配置字典
            
        Returns:
            bool: 配置是否有效
            
        Raises:
            FontConfigError: 配置验证失败
        """
        required_sections = ["font_config"]
        
        for section in required_sections:
            if section not in config:
                raise FontConfigError(
                    str(self.config_path),
                    f"缺少必需的配置节: {section}"
                )
        
        # 验证字体配置节
        font_config = config["font_config"]
        if not isinstance(font_config, dict):
            raise FontConfigError(
                str(self.config_path),
                "font_config必须是字典类型"
            )
        
        # 验证首选字体配置
        if "preferred_fonts" in font_config:
            preferred_fonts = font_config["preferred_fonts"]
            if not isinstance(preferred_fonts, dict):
                raise FontConfigError(
                    str(self.config_path),
                    "preferred_fonts必须是字典类型"
                )
        
        return True
    
    def _merge_config(self, default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        """
        合并默认配置和用户配置
        
        Args:
            default: 默认配置
            user: 用户配置
            
        Returns:
            Dict[str, Any]: 合并后的配置
        """
        merged = default.copy()
        
        for key, value in user.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_config(merged[key], value)
            else:
                merged[key] = value
        
        return merged
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键，支持点号分隔的嵌套键
            default: 默认值
            
        Returns:
            Any: 配置值
        """
        if not self._config_loaded:
            self.load_config()
        
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> bool:
        """
        设置配置值
        
        Args:
            key: 配置键，支持点号分隔的嵌套键
            value: 配置值
            
        Returns:
            bool: 是否设置成功
        """
        if not self._config_loaded:
            self.load_config()
        
        keys = key.split('.')
        config = self._config
        
        # 导航到目标位置
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # 设置值
        config[keys[-1]] = value
        
        self.logger.debug(f"配置已更新: {key} = {value}")
        return True
    
    def get_preferred_fonts(self, platform: Optional[Platform] = None) -> List[str]:
        """
        获取指定平台的首选字体列表
        
        Args:
            platform: 平台类型，None表示当前平台
            
        Returns:
            List[str]: 首选字体列表
        """
        if platform is None:
            platform = self.platform
        
        platform_key = platform.value.lower()
        if platform_key == 'darwin':
            platform_key = 'macos'
        return self.get(f"font_config.preferred_fonts.{platform_key}", [])
    
    def set_preferred_fonts(self, fonts: List[str], platform: Optional[Platform] = None) -> bool:
        """
        设置指定平台的首选字体列表
        
        Args:
            fonts: 字体列表
            platform: 平台类型，None表示当前平台
            
        Returns:
            bool: 是否设置成功
        """
        if platform is None:
            platform = self.platform
        
        platform_key = platform.value.lower()
        if platform_key == 'darwin':
            platform_key = 'macos'
        return self.set(f"font_config.preferred_fonts.{platform_key}", fonts)
    
    def get_fallback_fonts(self) -> List[str]:
        """
        获取备用字体列表
        
        Returns:
            List[str]: 备用字体列表
        """
        return self.get("font_config.fallback_fonts", [])
    
    def set_fallback_fonts(self, fonts: List[str]) -> bool:
        """
        设置备用字体列表
        
        Args:
            fonts: 字体列表
            
        Returns:
            bool: 是否设置成功
        """
        return self.set("font_config.fallback_fonts", fonts)
    
    def get_font_style(self, element: str) -> Dict[str, Any]:
        """
        获取字体样式配置
        
        Args:
            element: 元素名称 (title, axis_label, tick_label, legend, annotation)
            
        Returns:
            Dict[str, Any]: 样式配置
        """
        return self.get(f"font_config.styles.{element}", {})
    
    def set_font_style(self, element: str, style: Dict[str, Any]) -> bool:
        """
        设置字体样式配置
        
        Args:
            element: 元素名称
            style: 样式配置
            
        Returns:
            bool: 是否设置成功
        """
        return self.set(f"font_config.styles.{element}", style)
    
    def reset_to_default(self) -> bool:
        """
        重置为默认配置
        
        Returns:
            bool: 是否重置成功
        """
        try:
            self._config = self._default_config.copy()
            self.save_config()
            self.logger.info("配置已重置为默认值")
            return True
        except Exception as e:
            self.logger.error(f"重置配置失败: {e}")
            return False
    
    def backup_config(self, backup_path: Optional[str] = None) -> str:
        """
        备份当前配置
        
        Args:
            backup_path: 备份文件路径，None表示自动生成
            
        Returns:
            str: 备份文件路径
            
        Raises:
            FontConfigError: 备份失败
        """
        if backup_path is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_path = str(self.config_path.parent / f"config_backup_{timestamp}.json")
        
        try:
            backup_path = Path(backup_path)
            ensure_directory(backup_path.parent)
            
            # 保存备份
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"配置备份成功: {backup_path}")
            return str(backup_path)
            
        except Exception as e:
            error_msg = f"配置备份失败: {e}"
            self.logger.error(error_msg)
            raise FontConfigError(str(backup_path), error_msg)
    
    def restore_config(self, backup_path: str) -> bool:
        """
        从备份恢复配置
        
        Args:
            backup_path: 备份文件路径
            
        Returns:
            bool: 是否恢复成功
            
        Raises:
            FontConfigError: 恢复失败
        """
        try:
            backup_path = Path(backup_path)
            
            if not backup_path.exists():
                raise FontConfigError(str(backup_path), "备份文件不存在")
            
            # 读取备份配置
            with open(backup_path, 'r', encoding='utf-8') as f:
                backup_config = json.load(f)
            
            # 验证备份配置
            self._validate_config(backup_config)
            
            # 恢复配置
            self.save_config(backup_config)
            
            self.logger.info(f"配置恢复成功: {backup_path}")
            return True
            
        except Exception as e:
            error_msg = f"配置恢复失败: {e}"
            self.logger.error(error_msg)
            raise FontConfigError(str(backup_path), error_msg)
    
    def migrate_config(self, from_version: str, to_version: str) -> bool:
        """
        迁移配置文件版本
        
        Args:
            from_version: 源版本
            to_version: 目标版本
            
        Returns:
            bool: 是否迁移成功
        """
        self.logger.info(f"配置迁移: {from_version} -> {to_version}")
        
        # 这里可以实现具体的迁移逻辑
        # 目前只是简单地更新版本号
        self.set("version", to_version)
        
        return True
    
    def get_config_info(self) -> Dict[str, Any]:
        """
        获取配置信息
        
        Returns:
            Dict[str, Any]: 配置信息
        """
        if not self._config_loaded:
            self.load_config()
        
        info = {
            "config_path": str(self.config_path),
            "config_exists": self.config_path.exists(),
            "config_size": self.config_path.stat().st_size if self.config_path.exists() else 0,
            "last_modified": self._last_modified,
            "version": self.get("version", "unknown"),
            "created_at": self.get("created_at"),
            "updated_at": self.get("updated_at"),
            "platform": self.platform.value
        }
        
        return info
    
    @property
    def config(self) -> Dict[str, Any]:
        """获取当前配置"""
        if not self._config_loaded:
            self.load_config()
        return self._config.copy()
    
    @property
    def config_path_str(self) -> str:
        """获取配置文件路径字符串"""
        return str(self.config_path)