#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test emoji configuration functionality
"""

import os
import tempfile
import json
from pathlib import Path
from unittest.mock import patch

from font_manager.core.config import ConfigManager


def test_default_emoji_config():
    """测试默认emoji配置"""
    print("Testing default emoji configuration...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir) / "test_config.json"
        config_manager = ConfigManager(str(config_path))
        
        # 加载配置（会创建默认配置）
        config = config_manager.load_config()
        
        # 验证默认值
        assert config_manager.get_emoji_fallback() == False
        assert config_manager.get_emoji_prefer_color() == True
        assert config_manager.get_emoji_fonts() == []
        
        # 验证配置结构
        assert "emoji_fallback" in config["font_config"]
        assert "emoji_prefer_color" in config["font_config"]
        assert "emoji_fonts" in config["font_config"]
        
        print("✓ Default emoji configuration test passed")


def test_emoji_config_methods():
    """测试emoji配置方法"""
    print("Testing emoji configuration methods...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir) / "test_config.json"
        config_manager = ConfigManager(str(config_path))
        
        # 测试设置emoji_fallback
        assert config_manager.set_emoji_fallback(True) == True
        assert config_manager.get_emoji_fallback() == True
        
        # 测试设置emoji_prefer_color
        assert config_manager.set_emoji_prefer_color(False) == True
        assert config_manager.get_emoji_prefer_color() == False
        
        # 测试设置emoji_fonts
        test_fonts = ["Apple Color Emoji", "Noto Color Emoji"]
        assert config_manager.set_emoji_fonts(test_fonts) == True
        assert config_manager.get_emoji_fonts() == test_fonts
        
        # 保存并重新加载
        config_manager.save_config()
        config_manager._config_loaded = False
        config_manager.load_config()
        
        # 验证持久化
        assert config_manager.get_emoji_fallback() == True
        assert config_manager.get_emoji_prefer_color() == False
        assert config_manager.get_emoji_fonts() == test_fonts
        
        print("✓ Emoji configuration methods test passed")


def test_environment_variable_overrides():
    """测试环境变量覆盖"""
    print("Testing environment variable overrides...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir) / "test_config.json"
        
        # 设置环境变量
        test_env = {
            'FM_EMOJI_FALLBACK': 'true',
            'FM_EMOJI_COLOR': 'false'
        }
        
        with patch.dict(os.environ, test_env):
            config_manager = ConfigManager(str(config_path))
            config_manager.load_config()
            
            # 验证环境变量覆盖生效
            assert config_manager.get_emoji_fallback() == True
            assert config_manager.get_emoji_prefer_color() == False
            
        print("✓ Environment variable overrides test passed")


def test_bool_env_parsing():
    """测试布尔环境变量解析"""
    print("Testing boolean environment variable parsing...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir) / "test_config.json"
        config_manager = ConfigManager(str(config_path))
        
        # 测试各种真值
        true_values = ['true', 'True', 'TRUE', '1', 'yes', 'Yes', 'on', 'ON']
        for value in true_values:
            assert config_manager._parse_bool_env(value) == True, f"Failed for: {value}"
        
        # 测试各种假值
        false_values = ['false', 'False', 'FALSE', '0', 'no', 'No', 'off', 'OFF']
        for value in false_values:
            assert config_manager._parse_bool_env(value) == False, f"Failed for: {value}"
        
        # 测试无效值
        invalid_values = ['invalid', 'maybe', '2', '']
        for value in invalid_values:
            assert config_manager._parse_bool_env(value) is None, f"Failed for: {value}"
        
        print("✓ Boolean environment variable parsing test passed")


def test_invalid_env_values():
    """测试无效环境变量值的处理"""
    print("Testing invalid environment variable values...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir) / "test_config.json"
        
        # 设置无效环境变量
        test_env = {
            'FM_EMOJI_FALLBACK': 'invalid_value',
            'FM_EMOJI_COLOR': 'maybe'
        }
        
        with patch.dict(os.environ, test_env):
            config_manager = ConfigManager(str(config_path))
            config_manager.load_config()
            
            # 应该使用默认值，不受无效环境变量影响
            assert config_manager.get_emoji_fallback() == False  # 默认值
            assert config_manager.get_emoji_prefer_color() == True  # 默认值
            
        print("✓ Invalid environment variable values test passed")


def test_config_backward_compatibility():
    """测试配置向后兼容性"""
    print("Testing configuration backward compatibility...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir) / "test_config.json"
        
        # 创建旧版本配置（不包含emoji字段）
        old_config = {
            "font_config": {
                "auto_detect": True,
                "preferred_fonts": {
                    "macos": ["Hiragino Sans GB"]
                },
                "fallback_fonts": ["Arial"]
            },
            "version": "1.0.0"
        }
        
        # 保存旧配置
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(old_config, f, indent=2)
        
        # 加载配置
        config_manager = ConfigManager(str(config_path))
        config_manager.load_config()
        
        # 验证新字段使用默认值
        assert config_manager.get_emoji_fallback() == False
        assert config_manager.get_emoji_prefer_color() == True
        assert config_manager.get_emoji_fonts() == []
        
        # 验证旧字段保持不变
        assert config_manager.get("font_config.auto_detect") == True
        assert "Hiragino Sans GB" in config_manager.get_preferred_fonts()
        
        print("✓ Configuration backward compatibility test passed")


def test_config_persistence():
    """测试配置持久化"""
    print("Testing configuration persistence...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir) / "test_config.json"
        
        # 第一次：创建并保存配置
        config_manager1 = ConfigManager(str(config_path))
        config_manager1.load_config()
        config_manager1.set_emoji_fallback(True)
        config_manager1.set_emoji_prefer_color(False)
        config_manager1.set_emoji_fonts(["Test Emoji"])
        config_manager1.save_config()
        
        # 第二次：重新加载配置
        config_manager2 = ConfigManager(str(config_path))
        config_manager2.load_config()
        
        # 验证配置被正确持久化
        assert config_manager2.get_emoji_fallback() == True
        assert config_manager2.get_emoji_prefer_color() == False
        assert config_manager2.get_emoji_fonts() == ["Test Emoji"]
        
        # 验证配置文件包含新字段
        with open(config_path, 'r', encoding='utf-8') as f:
            saved_config = json.load(f)
        
        assert "emoji_fallback" in saved_config["font_config"]
        assert "emoji_prefer_color" in saved_config["font_config"]
        assert "emoji_fonts" in saved_config["font_config"]
        assert saved_config["font_config"]["emoji_fallback"] == True
        assert saved_config["font_config"]["emoji_prefer_color"] == False
        assert saved_config["font_config"]["emoji_fonts"] == ["Test Emoji"]
        
        print("✓ Configuration persistence test passed")


def test_env_override_priority():
    """测试环境变量优先级"""
    print("Testing environment variable priority...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir) / "test_config.json"
        
        # 创建配置文件
        file_config = {
            "font_config": {
                "emoji_fallback": False,
                "emoji_prefer_color": True
            }
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(file_config, f, indent=2)
        
        # 设置环境变量（与文件配置相反）
        test_env = {
            'FM_EMOJI_FALLBACK': 'true',
            'FM_EMOJI_COLOR': 'false'
        }
        
        with patch.dict(os.environ, test_env):
            config_manager = ConfigManager(str(config_path))
            config_manager.load_config()
            
            # 环境变量应该覆盖文件配置
            assert config_manager.get_emoji_fallback() == True  # 环境变量值
            assert config_manager.get_emoji_prefer_color() == False  # 环境变量值
            
        print("✓ Environment variable priority test passed")


if __name__ == "__main__":
    test_default_emoji_config()
    test_emoji_config_methods()
    test_environment_variable_overrides()
    test_bool_env_parsing()
    test_invalid_env_values()
    test_config_backward_compatibility()
    test_config_persistence()
    test_env_override_priority()
    print("\n🎉 All emoji configuration tests passed!")