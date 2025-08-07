#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Font Manager GitHub版本自动化测试脚本
一键检测GitHub上传后的Font Manager是否正常工作
"""

import sys
import traceback
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端

def print_header(title):
    """打印测试标题"""
    print(f"\n{'='*50}")
    print(f"🧪 {title}")
    print('='*50)

def test_import():
    """测试1: 导入测试"""
    print("📦 测试1: 导入Font Manager...")
    try:
        import font_manager
        print("✅ 导入成功")
        return True
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_setup_function():
    """测试2: setup_chinese_font函数测试"""
    print("\n🔧 测试2: setup_chinese_font函数...")
    try:
        from font_manager import setup_chinese_font
        setup_chinese_font()
        print("✅ setup_chinese_font函数正常")
        return True
    except Exception as e:
        print(f"❌ setup_chinese_font函数失败: {e}")
        return False

def test_font_manager_class():
    """测试3: FontManager类测试"""
    print("\n🏗️  测试3: FontManager类...")
    try:
        from font_manager import FontManager
        fm = FontManager()
        result = fm.setup()
        if result.success:
            print(f"✅ FontManager类正常 - 使用字体: {result.font_used.name}")
            return True
        else:
            print(f"❌ FontManager设置失败: {result.error_message}")
            return False
    except Exception as e:
        print(f"❌ FontManager类测试失败: {e}")
        return False

def test_fontinfo_attributes():
    """测试4: FontInfo属性测试（关键bug修复验证）"""
    print("\n🐛 测试4: FontInfo属性测试（bug修复验证）...")
    try:
        from font_manager import FontManager
        fm = FontManager()
        result = fm.setup()
        if result.success:
            # 测试修复的关键属性
            score = result.font_used.quality_score  # 这里之前是bug
            name = result.font_used.name
            path = result.font_used.path
            print(f"✅ FontInfo属性正常")
            print(f"   - 字体名称: {name}")
            print(f"   - 质量评分: {score:.2f}")
            print(f"   - 字体路径: {path}")
            return True
        else:
            print("❌ FontInfo属性测试失败 - 字体设置失败")
            return False
    except AttributeError as e:
        print(f"❌ FontInfo属性测试失败 - AttributeError: {e}")
        print("   这表明bug修复可能不完整！")
        return False
    except Exception as e:
        print(f"❌ FontInfo属性测试失败: {e}")
        return False

def test_chinese_display():
    """测试5: 中文显示测试"""
    print("\n🎨 测试5: 中文显示测试...")
    try:
        from font_manager import setup_chinese_font
        setup_chinese_font()
        
        # 创建测试图表
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # 测试数据
        categories = ['数据分析', '机器学习', '深度学习', '可视化']
        values = [85, 92, 78, 88]
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        
        # 创建柱状图
        bars = ax.bar(categories, values, color=colors, alpha=0.8)
        ax.set_title('🎉 Font Manager 中文字体测试', fontsize=16, fontweight='bold')
        ax.set_xlabel('技术领域', fontsize=12)
        ax.set_ylabel('掌握程度 (%)', fontsize=12)
        
        # 添加数值标签
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{value}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('font_manager_chinese_test.png', dpi=150, bbox_inches='tight')
        plt.close()
        
        print("✅ 中文显示测试完成")
        print("   - 已生成测试图片: font_manager_chinese_test.png")
        print("   - 请检查图片中的中文是否正常显示（无方框）")
        return True
    except Exception as e:
        print(f"❌ 中文显示测试失败: {e}")
        return False

def test_backup_config():
    """测试6: 配置备份测试（另一个修复的bug）"""
    print("\n💾 测试6: 配置备份测试...")
    try:
        from font_manager import FontManager
        fm = FontManager()
        result = fm.setup()
        if result.success:
            # 测试修复的backup_config方法
            backup_path = fm.backup_config("test_backup.json")
            print(f"✅ 配置备份功能正常")
            print(f"   - 备份路径: {backup_path}")
            return True
        else:
            print("❌ 配置备份测试失败 - 字体设置失败")
            return False
    except AttributeError as e:
        print(f"❌ 配置备份测试失败 - AttributeError: {e}")
        return False
    except Exception as e:
        print(f"❌ 配置备份测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print_header("Font Manager GitHub版本完整测试")
    print("🎯 测试目标: 验证GitHub上传后的Font Manager是否正常工作")
    print("🐛 重点验证: 修复的AttributeError问题")
    
    # 测试列表
    tests = [
        ("导入测试", test_import),
        ("setup_chinese_font函数", test_setup_function),
        ("FontManager类", test_font_manager_class),
        ("FontInfo属性（bug修复）", test_fontinfo_attributes),
        ("中文显示", test_chinese_display),
        ("配置备份（bug修复）", test_backup_config),
    ]
    
    passed = 0
    total = len(tests)
    failed_tests = []
    
    # 执行测试
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed_tests.append(test_name)
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
            failed_tests.append(test_name)
            traceback.print_exc()
    
    # 输出结果
    print_header("测试结果汇总")
    print(f"📊 总测试数: {total}")
    print(f"✅ 通过数: {passed}")
    print(f"❌ 失败数: {total - passed}")
    
    if failed_tests:
        print(f"\n❌ 失败的测试:")
        for test in failed_tests:
            print(f"   - {test}")
    
    print(f"\n🎯 成功率: {passed/total*100:.1f}%")
    
    if passed == total:
        print("\n🎉 恭喜！所有测试通过！")
        print("✅ Font Manager GitHub版本工作完美！")
        print("✅ 修复的bug已解决！")
        print("✅ 用户可以正常使用一行代码解决中文字体问题！")
        print("🚀 告别字体框框，拥抱完美中文显示！")
        return True
    else:
        print(f"\n⚠️  有 {total-passed} 个测试失败")
        print("🔧 请检查GitHub上传的文件是否完整")
        print("🐛 特别检查是否包含了修复后的文件")
        return False

if __name__ == "__main__":
    print("🚀 启动Font Manager GitHub版本自动化测试...")
    success = main()
    
    print(f"\n{'='*50}")
    if success:
        print("🎊 测试完成：Font Manager GitHub版本质量优秀！")
    else:
        print("🔧 测试完成：发现问题，需要修复")
    print('='*50)
    
    sys.exit(0 if success else 1)