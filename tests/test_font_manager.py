#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Font Manager 基础架构测试脚本

测试字体管理库的基础功能。
"""

import sys
from pathlib import Path

# 添加font_manager到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from font_manager import FontManager, setup_chinese_font, get_available_fonts, validate_font_config
from font_manager.utils.logger import setup_logging


def test_basic_functionality():
    """测试基础功能"""
    print("🧪 测试字体管理库基础功能...")
    
    # 设置日志
    setup_logging(level="INFO", enable_color=True)
    
    try:
        # 测试1: 创建FontManager实例
        print("\n1️⃣ 测试FontManager实例化...")
        fm = FontManager()
        print(f"✅ FontManager创建成功，平台: {fm.platform.value}")
        
        # 测试2: 一键设置字体
        print("\n2️⃣ 测试一键字体设置...")
        result = fm.setup()
        print(f"设置结果: {'✅ 成功' if result.success else '❌ 失败'}")
        if result.font_used:
            print(f"使用字体: {result.font_used.name}")
        if result.warnings:
            print(f"警告: {', '.join(result.warnings)}")
        if result.errors:
            print(f"错误: {', '.join(result.errors)}")
        print(f"设置耗时: {result.setup_time:.3f}秒")
        
        # 测试3: 获取可用字体
        print("\n3️⃣ 测试获取可用字体...")
        fonts = fm.get_available_fonts()
        print(f"找到 {len(fonts)} 个可用字体:")
        for font in fonts:
            print(f"  📝 {font.name} - 中文支持: {'✅' if font.supports_chinese else '❌'}")
        
        # 测试4: 验证字体配置
        print("\n4️⃣ 测试字体配置验证...")
        report = fm.validate()
        print(f"验证状态: {report.status}")
        print(f"字体可用: {'✅' if report.font_available else '❌'}")
        print(f"中文支持: {'✅' if report.chinese_support else '❌'}")
        print(f"综合评分: {report.overall_score:.2f}")
        if report.issues:
            print(f"问题: {', '.join(report.issues)}")
        if report.recommendations:
            print(f"建议: {', '.join(report.recommendations)}")
        
        # 测试5: 便捷函数
        print("\n5️⃣ 测试便捷函数...")
        
        print("测试 setup_chinese_font()...")
        quick_result = setup_chinese_font()
        print(f"快速设置: {'✅ 成功' if quick_result.success else '❌ 失败'}")
        
        print("测试 get_available_fonts()...")
        quick_fonts = get_available_fonts()
        print(f"快速获取字体: {len(quick_fonts)} 个")
        
        print("测试 validate_font_config()...")
        quick_report = validate_font_config()
        print(f"快速验证: {quick_report.status}")
        
        print("\n🎉 所有基础功能测试完成！")
        return True
        
    except Exception as e:
        print(f"\n❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_data_models():
    """测试数据模型"""
    print("\n📊 测试数据模型...")
    
    try:
        from font_manager.core.models import FontInfo, FontSetupResult, ValidationReport
        from font_manager.core.models import FontWeight, FontStyle, Platform
        
        # 测试FontInfo
        print("测试 FontInfo...")
        font_info = FontInfo(
            name="Test Font",
            path="/test/path",
            family="Test Family",
            supports_chinese=True,
            quality_score=0.8
        )
        print(f"✅ FontInfo创建成功: {font_info.name}")
        
        # 测试转换为字典
        font_dict = font_info.to_dict()
        print(f"✅ 字典转换成功，包含 {len(font_dict)} 个字段")
        
        # 测试从字典创建
        font_from_dict = FontInfo.from_dict(font_dict)
        print(f"✅ 从字典创建成功: {font_from_dict.name}")
        
        # 测试FontSetupResult
        print("测试 FontSetupResult...")
        setup_result = FontSetupResult(success=True, font_used=font_info)
        setup_result.add_warning("测试警告")
        setup_result.add_error("测试错误")
        print(f"✅ FontSetupResult创建成功，有警告: {setup_result.has_warnings}")
        
        # 测试ValidationReport
        print("测试 ValidationReport...")
        report = ValidationReport(font_available=True, chinese_support=True)
        report.add_issue("测试问题")
        report.add_recommendation("测试建议")
        report.set_test_result("test1", True)
        print(f"✅ ValidationReport创建成功，状态: {report.status}")
        
        print("✅ 所有数据模型测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 数据模型测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_utilities():
    """测试工具函数"""
    print("\n🔧 测试工具函数...")
    
    try:
        from font_manager.utils.helpers import (
            get_platform, is_font_file, normalize_font_name, 
            calculate_font_score, get_system_font_directories
        )
        
        # 测试平台检测
        platform = get_platform()
        print(f"✅ 平台检测: {platform.value}")
        
        # 测试字体文件检测
        is_font = is_font_file("test.ttf")
        print(f"✅ 字体文件检测: {is_font}")
        
        # 测试字体名称标准化
        normalized = normalize_font_name("  Microsoft   YaHei  ")
        print(f"✅ 字体名称标准化: '{normalized}'")
        
        # 测试字体评分
        score = calculate_font_score("Hiragino Sans GB", True, 5000000, platform)
        print(f"✅ 字体评分计算: {score:.2f}")
        
        # 测试系统字体目录
        font_dirs = get_system_font_directories()
        print(f"✅ 系统字体目录: {len(font_dirs)} 个")
        for font_dir in font_dirs[:3]:  # 只显示前3个
            print(f"  📁 {font_dir}")
        
        print("✅ 所有工具函数测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 工具函数测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("🚀 Font Manager 基础架构测试")
    print("=" * 50)
    
    success_count = 0
    total_tests = 3
    
    # 运行测试
    if test_data_models():
        success_count += 1
    
    if test_utilities():
        success_count += 1
    
    if test_basic_functionality():
        success_count += 1
    
    # 输出结果
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {success_count}/{total_tests} 通过")
    
    if success_count == total_tests:
        print("🎉 所有测试通过！基础架构搭建成功！")
        return True
    else:
        print("❌ 部分测试失败，需要修复问题")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)