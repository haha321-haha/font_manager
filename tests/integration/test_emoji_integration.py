#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test emoji integration with FontManager
"""

import os
from unittest.mock import patch

from font_manager import setup_matplotlib_chinese, FontManager


def test_setup_matplotlib_chinese_basic():
    """测试基本的setup_matplotlib_chinese功能"""
    print("Testing basic setup_matplotlib_chinese...")
    
    # 测试默认参数（不启用emoji）
    result = setup_matplotlib_chinese()
    
    assert result.success == True
    assert len(result.emoji_fonts) == 0  # 默认不启用emoji
    assert result.emoji_color_available == False
    
    print(f"✓ 基本设置成功: {result.font_used.name if result.font_used else 'None'}")
    print(f"  - emoji字体数量: {len(result.emoji_fonts)}")
    print(f"  - 设置耗时: {result.setup_time:.3f}秒")


def test_setup_matplotlib_chinese_with_emoji():
    """测试启用emoji的setup_matplotlib_chinese功能"""
    print("\nTesting setup_matplotlib_chinese with emoji...")
    
    # 测试启用emoji
    result = setup_matplotlib_chinese(emoji_fallback=True, emoji_prefer_color=True)
    
    assert result.success == True
    
    print(f"✓ emoji设置完成")
    print(f"  - 中文字体: {result.font_used.name if result.font_used else 'None'}")
    print(f"  - emoji字体数量: {len(result.emoji_fonts)}")
    print(f"  - emoji字体: {result.emoji_fonts}")
    print(f"  - 彩色emoji可用: {result.emoji_color_available}")
    print(f"  - mplcairo检测: {result.mplcairo_detected}")
    print(f"  - 设置耗时: {result.setup_time:.3f}秒")
    
    if result.warnings:
        print(f"  - 警告: {result.warnings}")


def test_emoji_preference():
    """测试emoji颜色偏好"""
    print("\nTesting emoji color preference...")
    
    # 测试优先彩色
    result_color = setup_matplotlib_chinese(emoji_fallback=True, emoji_prefer_color=True)
    print(f"✓ 优先彩色: emoji字体={result_color.emoji_fonts}")
    
    # 测试优先黑白
    result_mono = setup_matplotlib_chinese(emoji_fallback=True, emoji_prefer_color=False)
    print(f"✓ 优先黑白: emoji字体={result_mono.emoji_fonts}")


def test_config_integration():
    """测试配置集成"""
    print("\nTesting configuration integration...")
    
    # 创建FontManager实例测试配置
    manager = FontManager()
    
    # 测试配置读取
    emoji_fallback = manager.config_manager.get_emoji_fallback()
    emoji_prefer_color = manager.config_manager.get_emoji_prefer_color()
    
    print(f"✓ 配置读取成功")
    print(f"  - emoji_fallback: {emoji_fallback}")
    print(f"  - emoji_prefer_color: {emoji_prefer_color}")
    
    # 测试配置设置
    manager.config_manager.set_emoji_fallback(True)
    manager.config_manager.set_emoji_prefer_color(False)
    
    assert manager.config_manager.get_emoji_fallback() == True
    assert manager.config_manager.get_emoji_prefer_color() == False
    
    print("✓ 配置设置成功")


def test_environment_variable_integration():
    """测试环境变量集成"""
    print("\nTesting environment variable integration...")
    
    # 设置环境变量
    test_env = {
        'FM_EMOJI_FALLBACK': 'true',
        'FM_EMOJI_COLOR': 'false'
    }
    
    with patch.dict(os.environ, test_env):
        result = setup_matplotlib_chinese()
        
        # 环境变量应该覆盖默认设置
        print(f"✓ 环境变量集成测试完成")
        print(f"  - emoji字体数量: {len(result.emoji_fonts)}")
        print(f"  - 应该启用emoji（通过环境变量）")


def test_matplotlib_rcparams():
    """测试matplotlib rcParams设置"""
    print("\nTesting matplotlib rcParams...")
    
    try:
        import matplotlib.pyplot as plt
        
        # 记录设置前的状态
        original_fonts = plt.rcParams['font.sans-serif'].copy()
        
        # 设置字体
        result = setup_matplotlib_chinese(emoji_fallback=True)
        
        # 检查rcParams
        current_fonts = plt.rcParams['font.sans-serif']
        
        print(f"✓ matplotlib rcParams设置成功")
        print(f"  - 原始字体: {original_fonts}")
        print(f"  - 当前字体: {current_fonts}")
        print(f"  - 中文字体: {current_fonts[0] if current_fonts else 'None'}")
        
        if len(result.emoji_fonts) > 0:
            print(f"  - emoji字体已添加到后备列表")
        
    except ImportError:
        print("⚠️  matplotlib未安装，跳过rcParams测试")


def test_error_handling():
    """测试错误处理"""
    print("\nTesting error handling...")
    
    # 测试强制重建缓存
    result = setup_matplotlib_chinese(force_rebuild=True, emoji_fallback=True)
    
    print(f"✓ 错误处理测试完成")
    print(f"  - 设置成功: {result.success}")
    print(f"  - 错误数量: {len(result.errors)}")
    print(f"  - 警告数量: {len(result.warnings)}")
    
    if result.errors:
        print(f"  - 错误: {result.errors}")
    if result.warnings:
        print(f"  - 警告: {result.warnings}")


if __name__ == "__main__":
    test_setup_matplotlib_chinese_basic()
    test_setup_matplotlib_chinese_with_emoji()
    test_emoji_preference()
    test_config_integration()
    test_environment_variable_integration()
    test_matplotlib_rcparams()
    test_error_handling()
    print("\n🎉 All integration tests completed!")