#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test enhanced FontInfo model with emoji support
"""

from font_manager.core.models import FontInfo, FontSetupResult, FontStyle, FontWeight, Platform


def test_fontinfo_emoji_fields():
    """测试FontInfo的emoji字段"""
    print("Testing FontInfo emoji fields...")
    
    # 测试中文字体
    chinese_font = FontInfo(
        name="SimHei",
        path="/System/Library/Fonts/SimHei.ttf",
        family="SimHei",
        supports_chinese=True,
        is_emoji=False,
        is_color_emoji=False,
        priority=1
    )
    
    # 测试彩色emoji字体
    color_emoji_font = FontInfo(
        name="Apple Color Emoji",
        path="/System/Library/Fonts/Apple Color Emoji.ttc",
        family="Apple Color Emoji",
        supports_chinese=False,
        is_emoji=True,
        is_color_emoji=True,
        priority=0
    )
    
    # 测试黑白emoji字体
    mono_emoji_font = FontInfo(
        name="Noto Emoji",
        path="/usr/share/fonts/truetype/noto/NotoEmoji-Regular.ttf",
        family="Noto Emoji",
        supports_chinese=False,
        is_emoji=True,
        is_color_emoji=False,
        priority=1
    )
    
    # 验证字段
    assert chinese_font.is_emoji == False
    assert chinese_font.is_color_emoji == False
    assert chinese_font.supports_chinese == True
    
    assert color_emoji_font.is_emoji == True
    assert color_emoji_font.is_color_emoji == True
    assert color_emoji_font.priority == 0
    
    assert mono_emoji_font.is_emoji == True
    assert mono_emoji_font.is_color_emoji == False
    assert mono_emoji_font.priority == 1
    
    print("✓ FontInfo emoji fields test passed")


def test_fontinfo_serialization():
    """测试FontInfo序列化和反序列化"""
    print("Testing FontInfo serialization...")
    
    original = FontInfo(
        name="Apple Color Emoji",
        path="/System/Library/Fonts/Apple Color Emoji.ttc",
        family="Apple Color Emoji",
        is_emoji=True,
        is_color_emoji=True,
        priority=0
    )
    
    # 序列化
    data = original.to_dict()
    assert 'is_emoji' in data
    assert 'is_color_emoji' in data
    assert 'priority' in data
    assert data['is_emoji'] == True
    assert data['is_color_emoji'] == True
    assert data['priority'] == 0
    
    # 反序列化
    restored = FontInfo.from_dict(data)
    assert restored.is_emoji == original.is_emoji
    assert restored.is_color_emoji == original.is_color_emoji
    assert restored.priority == original.priority
    assert restored.name == original.name
    
    print("✓ FontInfo serialization test passed")


def test_fontsetupresult_emoji_fields():
    """测试FontSetupResult的emoji字段"""
    print("Testing FontSetupResult emoji fields...")
    
    result = FontSetupResult(
        success=True,
        emoji_fonts=["Apple Color Emoji", "Noto Emoji"],
        emoji_color_available=True,
        mplcairo_detected=False,
        platform=Platform.MACOS
    )
    
    # 验证字段
    assert len(result.emoji_fonts) == 2
    assert "Apple Color Emoji" in result.emoji_fonts
    assert "Noto Emoji" in result.emoji_fonts
    assert result.emoji_color_available == True
    assert result.mplcairo_detected == False
    
    # 测试序列化
    data = result.to_dict()
    assert 'emoji_fonts' in data
    assert 'emoji_color_available' in data
    assert 'mplcairo_detected' in data
    assert data['emoji_fonts'] == ["Apple Color Emoji", "Noto Emoji"]
    assert data['emoji_color_available'] == True
    assert data['mplcairo_detected'] == False
    
    print("✓ FontSetupResult emoji fields test passed")


def test_backward_compatibility():
    """测试向后兼容性"""
    print("Testing backward compatibility...")
    
    # 测试不包含emoji字段的旧数据
    old_data = {
        'name': 'SimHei',
        'path': '/System/Library/Fonts/SimHei.ttf',
        'family': 'SimHei',
        'style': 'normal',
        'weight': 400,
        'supports_chinese': True,
        'quality_score': 0.8,
        'platform_priority': 1,
        'file_size': 1024,
        'version': '1.0'
    }
    
    # 应该能够正常创建FontInfo，emoji字段使用默认值
    font = FontInfo.from_dict(old_data)
    assert font.is_emoji == False  # 默认值
    assert font.is_color_emoji == False  # 默认值
    assert font.priority == 0  # 默认值
    assert font.supports_chinese == True
    assert font.name == 'SimHei'
    
    print("✓ Backward compatibility test passed")


if __name__ == "__main__":
    test_fontinfo_emoji_fields()
    test_fontinfo_serialization()
    test_fontsetupresult_emoji_fields()
    test_backward_compatibility()
    print("\n🎉 All tests passed! FontInfo model enhancement completed.")