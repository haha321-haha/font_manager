#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test emoji font detection functionality
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from font_manager.core.detector import FontDetector
from font_manager.core.models import Platform


def test_emoji_font_candidates():
    """测试emoji字体候选列表生成"""
    print("Testing emoji font candidates...")
    
    detector = FontDetector()
    
    # 测试macOS候选
    with patch.object(detector, 'platform', Platform.MACOS):
        candidates = detector._get_emoji_font_candidates()
        assert len(candidates) > 0
        # 检查Apple Color Emoji是否在列表中
        apple_fonts = [c for c in candidates if "Apple Color Emoji" in c[0]]
        assert len(apple_fonts) > 0
        # 检查第一个是彩色的
        assert apple_fonts[0][2] == True  # is_color
        print("✓ macOS candidates test passed")
    
    # 测试Linux候选
    with patch.object(detector, 'platform', Platform.LINUX):
        candidates = detector._get_emoji_font_candidates()
        assert len(candidates) > 0
        # 检查Noto字体是否在列表中
        noto_fonts = [c for c in candidates if "Noto" in c[0]]
        assert len(noto_fonts) > 0
        print("✓ Linux candidates test passed")
    
    # 测试Windows候选
    with patch.object(detector, 'platform', Platform.WINDOWS):
        candidates = detector._get_emoji_font_candidates()
        assert len(candidates) > 0
        # 检查Segoe UI Emoji是否在列表中
        segoe_fonts = [c for c in candidates if "Segoe UI Emoji" in c[0]]
        assert len(segoe_fonts) > 0
        print("✓ Windows candidates test passed")


def test_emoji_font_detection_no_fonts():
    """测试没有emoji字体的情况"""
    print("Testing emoji detection with no fonts...")
    
    detector = FontDetector()
    
    # Mock os.path.exists to return False for all paths
    with patch('os.path.exists', return_value=False):
        emoji_fonts = detector.detect_emoji_fonts()
        assert len(emoji_fonts) == 0
        print("✓ No fonts detection test passed")


def test_emoji_font_detection_with_mock_fonts():
    """测试有emoji字体的情况（使用mock）"""
    print("Testing emoji detection with mock fonts...")
    
    detector = FontDetector()
    
    # 创建临时文件来模拟字体文件
    with tempfile.TemporaryDirectory() as temp_dir:
        # 创建模拟字体文件
        mock_font_path = os.path.join(temp_dir, "MockEmoji.ttf")
        with open(mock_font_path, 'wb') as f:
            f.write(b'MOCK_FONT_DATA' * 100)  # 创建足够大的文件
        
        # Mock字体候选列表
        mock_candidates = [
            ("Mock Color Emoji", mock_font_path, True),
            ("Mock Mono Emoji", "/nonexistent/path.ttf", False),
        ]
        
        with patch.object(detector, '_get_emoji_font_candidates', return_value=mock_candidates):
            with patch.object(detector, 'verify_font', return_value=True):
                emoji_fonts = detector.detect_emoji_fonts()
                
                assert len(emoji_fonts) == 1
                font = emoji_fonts[0]
                assert font.name == "Mock Color Emoji"
                assert font.is_emoji == True
                assert font.is_color_emoji == True
                assert font.priority == 0
                print("✓ Mock fonts detection test passed")


def test_emoji_font_sorting():
    """测试emoji字体排序"""
    print("Testing emoji font sorting...")
    
    detector = FontDetector()
    
    # 创建测试字体列表
    from font_manager.core.models import FontInfo, FontStyle, FontWeight
    
    fonts = [
        FontInfo(
            name="Mono Emoji", path="/path/mono.ttf", family="Mono Emoji",
            is_emoji=True, is_color_emoji=False, priority=1
        ),
        FontInfo(
            name="Color Emoji", path="/path/color.ttf", family="Color Emoji",
            is_emoji=True, is_color_emoji=True, priority=0
        ),
        FontInfo(
            name="Another Mono", path="/path/mono2.ttf", family="Another Mono",
            is_emoji=True, is_color_emoji=False, priority=2
        ),
    ]
    
    # 测试优先彩色
    sorted_color = detector.sort_emoji_fonts_by_preference(fonts, prefer_color=True)
    assert sorted_color[0].name == "Color Emoji"
    assert sorted_color[1].name == "Mono Emoji"  # priority 1 < priority 2
    assert sorted_color[2].name == "Another Mono"
    print("✓ Color preference sorting test passed")
    
    # 测试优先黑白
    sorted_mono = detector.sort_emoji_fonts_by_preference(fonts, prefer_color=False)
    assert sorted_mono[0].name == "Mono Emoji"  # 黑白且priority最小
    assert sorted_mono[1].name == "Another Mono"
    assert sorted_mono[2].name == "Color Emoji"  # 彩色排最后
    print("✓ Mono preference sorting test passed")


def test_platform_specific_paths():
    """测试平台特定路径"""
    print("Testing platform-specific paths...")
    
    detector = FontDetector()
    
    # 测试macOS路径
    with patch.object(detector, 'platform', Platform.MACOS):
        candidates = detector._get_emoji_font_candidates()
        macos_paths = [c[1] for c in candidates if "Apple Color Emoji" in c[0]]
        assert any("/System/Library/Fonts/" in path for path in macos_paths)
        print("✓ macOS paths test passed")
    
    # 测试Linux路径
    with patch.object(detector, 'platform', Platform.LINUX):
        candidates = detector._get_emoji_font_candidates()
        linux_paths = [c[1] for c in candidates]
        assert any("/usr/share/fonts/" in path for path in linux_paths)
        print("✓ Linux paths test passed")
    
    # 测试Windows路径
    with patch.object(detector, 'platform', Platform.WINDOWS):
        candidates = detector._get_emoji_font_candidates()
        windows_paths = [c[1] for c in candidates]
        assert any("C:\\Windows\\Fonts\\" in path for path in windows_paths)
        print("✓ Windows paths test passed")


def test_emoji_font_priority_order():
    """测试emoji字体优先级顺序"""
    print("Testing emoji font priority order...")
    
    detector = FontDetector()
    
    # 测试macOS优先级：Apple Color Emoji应该是最高优先级
    with patch.object(detector, 'platform', Platform.MACOS):
        candidates = detector._get_emoji_font_candidates()
        # 第一个应该是Apple Color Emoji
        assert "Apple Color Emoji" in candidates[0][0]
        assert candidates[0][2] == True  # 应该是彩色的
        print("✓ macOS priority test passed")
    
    # 测试Linux优先级：Noto Color Emoji > Noto Emoji
    with patch.object(detector, 'platform', Platform.LINUX):
        candidates = detector._get_emoji_font_candidates()
        color_emoji_idx = next(i for i, c in enumerate(candidates) if "Noto Color Emoji" in c[0])
        mono_emoji_indices = [i for i, c in enumerate(candidates) if "Noto Emoji" in c[0] and "Color" not in c[0]]
        if mono_emoji_indices:
            assert color_emoji_idx < min(mono_emoji_indices)
        print("✓ Linux priority test passed")


if __name__ == "__main__":
    test_emoji_font_candidates()
    test_emoji_font_detection_no_fonts()
    test_emoji_font_detection_with_mock_fonts()
    test_emoji_font_sorting()
    test_platform_specific_paths()
    test_emoji_font_priority_order()
    print("\n🎉 All emoji detector tests passed!")