#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Font Detector 测试脚本

测试字体检测器的功能。
"""

import sys
from pathlib import Path

# 添加font_manager到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from font_manager import FontDetector, FontManager
from font_manager.utils.logger import setup_logging


def test_font_detector():
    """测试字体检测器"""
    print("🔍 测试字体检测器功能...")
    
    # 设置日志
    setup_logging(level="INFO", enable_color=True)
    
    try:
        # 创建字体检测器
        print("\n1️⃣ 创建字体检测器...")
        detector = FontDetector(cache_enabled=True)
        print(f"✅ 字体检测器创建成功，平台: {detector.platform.value}")
        
        # 检测系统字体
        print("\n2️⃣ 检测系统字体...")
        fonts = detector.detect_system_fonts()
        print(f"✅ 检测完成，找到 {len(fonts)} 个字体")
        
        # 显示前10个字体
        print("\n📝 字体列表 (前10个):")
        for i, font in enumerate(fonts[:10], 1):
            chinese_support = "✅" if font.supports_chinese else "❌"
            print(f"  {i:2d}. {font.name}")
            print(f"      路径: {font.path}")
            print(f"      中文支持: {chinese_support} | 评分: {font.quality_score:.2f} | 优先级: {font.platform_priority}")
        
        # 获取中文字体
        print("\n3️⃣ 获取中文字体...")
        chinese_fonts = detector.get_chinese_fonts(fonts)
        print(f"✅ 找到 {len(chinese_fonts)} 个中文字体")
        
        if chinese_fonts:
            print("\n🎯 最佳中文字体 (前5个):")
            for i, font in enumerate(chinese_fonts[:5], 1):
                print(f"  {i}. {font.name} (评分: {font.quality_score:.2f})")
        
        # 字体排序测试
        print("\n4️⃣ 测试字体排序...")
        sorted_fonts = detector.rank_fonts(fonts)
        print(f"✅ 字体排序完成")
        
        if sorted_fonts:
            best_font = sorted_fonts[0]
            print(f"🏆 最佳字体: {best_font.name}")
            print(f"   评分: {best_font.quality_score:.2f}")
            print(f"   中文支持: {'✅' if best_font.supports_chinese else '❌'}")
        
        # 字体验证测试
        print("\n5️⃣ 测试字体验证...")
        if fonts:
            test_font = fonts[0]
            is_valid = detector.verify_font(test_font.path)
            print(f"✅ 字体验证: {test_font.name} - {'有效' if is_valid else '无效'}")
        
        # 按名称查找字体
        print("\n6️⃣ 测试按名称查找字体...")
        if chinese_fonts:
            target_name = chinese_fonts[0].name
            found_font = detector.find_font_by_name(target_name, fonts)
            if found_font:
                print(f"✅ 找到字体: {found_font.name}")
            else:
                print(f"❌ 未找到字体: {target_name}")
        
        # 缓存信息
        print("\n7️⃣ 缓存信息:")
        print(f"   缓存大小: {detector.cache_size} 个字体")
        print(f"   缓存年龄: {detector.cache_age:.2f} 秒")
        
        print("\n🎉 字体检测器测试完成！")
        return True
        
    except Exception as e:
        print(f"\n❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_integration_with_manager():
    """测试与FontManager的集成"""
    print("\n🔗 测试与FontManager的集成...")
    
    try:
        # 创建FontManager
        fm = FontManager()
        
        # 测试字体设置
        print("测试字体设置...")
        result = fm.setup()
        
        print(f"设置结果: {'✅ 成功' if result.success else '❌ 失败'}")
        if result.font_used:
            print(f"使用字体: {result.font_used.name}")
            print(f"字体评分: {result.font_used.quality_score:.2f}")
            print(f"中文支持: {'✅' if result.font_used.supports_chinese else '❌'}")
        
        if result.fallback_fonts:
            print(f"备用字体: {', '.join(result.fallback_fonts[:3])}...")
        
        if result.warnings:
            print(f"警告: {', '.join(result.warnings)}")
        
        # 测试获取可用字体
        print("\n测试获取可用字体...")
        fonts = fm.get_available_fonts()
        print(f"可用字体: {len(fonts)} 个")
        
        # 显示统计信息
        chinese_count = sum(1 for f in fonts if f.supports_chinese)
        print(f"中文字体: {chinese_count} 个")
        
        print("✅ 集成测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def create_font_report():
    """创建字体报告"""
    print("\n📊 生成字体报告...")
    
    try:
        detector = FontDetector()
        fonts = detector.detect_system_fonts()
        
        # 统计信息
        total_fonts = len(fonts)
        chinese_fonts = [f for f in fonts if f.supports_chinese]
        chinese_count = len(chinese_fonts)
        
        # 按平台优先级分组
        priority_groups = {}
        for font in fonts:
            priority = font.platform_priority
            if priority not in priority_groups:
                priority_groups[priority] = []
            priority_groups[priority].append(font)
        
        # 排序中文字体
        sorted_chinese_fonts = detector.rank_fonts(chinese_fonts)
        
        # 生成报告
        report = f"""
# 字体检测报告

## 📊 统计信息
- **总字体数**: {total_fonts} 个
- **中文字体数**: {chinese_count} 个
- **中文字体比例**: {(chinese_count/total_fonts*100):.1f}%

## 🏆 最佳中文字体 (前10个)
"""
        
        for i, font in enumerate(sorted_chinese_fonts[:10], 1):
            report += f"{i:2d}. **{font.name}** (评分: {font.quality_score:.2f})\n"
            report += f"    - 路径: `{font.path}`\n"
            report += f"    - 优先级: {font.platform_priority}\n\n"
        
        report += f"""
## 📈 优先级分布
"""
        
        for priority in sorted(priority_groups.keys())[:5]:
            fonts_in_group = priority_groups[priority]
            report += f"- **优先级 {priority}**: {len(fonts_in_group)} 个字体\n"
        
        # 保存报告
        with open('font_detection_report.md', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("✅ 字体报告已保存: font_detection_report.md")
        return True
        
    except Exception as e:
        print(f"❌ 生成报告失败: {e}")
        return False


def main():
    """主测试函数"""
    print("🚀 Font Detector 功能测试")
    print("=" * 50)
    
    success_count = 0
    total_tests = 3
    
    # 运行测试
    if test_font_detector():
        success_count += 1
    
    if test_integration_with_manager():
        success_count += 1
    
    if create_font_report():
        success_count += 1
    
    # 输出结果
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {success_count}/{total_tests} 通过")
    
    if success_count == total_tests:
        print("🎉 所有测试通过！字体检测功能正常！")
        return True
    else:
        print("❌ 部分测试失败，需要修复问题")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)