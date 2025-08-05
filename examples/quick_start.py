#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图表字体管理库 - 快速开始脚本

这个脚本演示如何在你的项目中快速使用字体管理库。
"""

import sys
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# 添加字体管理库路径
font_lib_path = "/Users/duting/Downloads/图表字体管理库"
if font_lib_path not in sys.path:
    sys.path.append(font_lib_path)

def quick_demo():
    """快速演示"""
    print("🚀 图表字体管理库 - 快速开始")
    print("=" * 50)
    
    try:
        # 导入字体管理库
        from font_manager import setup_chinese_font, FontManager
        
        print("📦 字体管理库导入成功")
        
        # 一键设置中文字体
        print("\n🔧 设置中文字体...")
        result = setup_chinese_font()
        
        if result.success:
            print(f"✅ 字体设置成功: {result.font_used.name}")
        else:
            print("⚠️ 字体设置失败，使用默认字体")
            if result.errors:
                print(f"错误: {', '.join(result.errors)}")
        
        # 创建测试图表
        print("\n📊 创建测试图表...")
        create_test_chart()
        
        # 显示字体信息
        print("\n🔍 字体信息:")
        fm = FontManager()
        fonts = fm.get_available_fonts()
        print(f"可用字体: {len(fonts)} 个")
        for font in fonts[:3]:  # 显示前3个
            print(f"  📝 {font.name} - 评分: {font.quality_score:.2f}")
        
        # 验证配置
        report = fm.validate()
        print(f"\n✅ 配置验证: {report.status} (评分: {report.overall_score:.2f})")
        
        print("\n🎉 快速开始演示完成！")
        print("💡 现在你可以在项目中正常使用matplotlib，中文字符将正确显示。")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请确保字体管理库路径正确")
        return False
    except Exception as e:
        print(f"❌ 演示过程出错: {e}")
        return False

def create_test_chart():
    """创建测试图表"""
    # 创建简单的测试数据
    categories = ['数据分析', '机器学习', '深度学习', '自然语言处理']
    values = [85, 92, 78, 88]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    
    # 创建图表
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(categories, values, color=colors, alpha=0.8)
    
    # 设置标题和标签
    ax.set_title('技术领域评分 - 中文字体测试', fontsize=16, fontweight='bold')
    ax.set_ylabel('评分', fontsize=12)
    ax.set_xlabel('技术领域', fontsize=12)
    
    # 添加数值标签
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{value}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # 设置样式
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_ylim(0, 100)
    
    plt.tight_layout()
    
    # 保存图表
    output_path = 'quick_start_test.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"✅ 测试图表已保存: {output_path}")

def usage_examples():
    """使用示例"""
    print("\n📚 使用示例:")
    print("-" * 30)
    
    print("1️⃣ 最简单的使用方法:")
    print("""
import sys
sys.path.append('/Users/duting/Downloads/图表字体管理库')
from font_manager import setup_chinese_font

setup_chinese_font()  # 一行代码解决问题
""")
    
    print("2️⃣ 完整的使用方法:")
    print("""
from font_manager import FontManager

fm = FontManager()
result = fm.setup()

if result.success:
    print(f"字体设置成功: {result.font_used.name}")
""")
    
    print("3️⃣ 验证字体配置:")
    print("""
from font_manager import validate_font_config

report = validate_font_config()
print(f"配置状态: {report.status}")
""")

def main():
    """主函数"""
    success = quick_demo()
    
    if success:
        usage_examples()
        print("\n🎯 下一步:")
        print("1. 在你的项目中添加字体管理库路径")
        print("2. 导入并调用 setup_chinese_font()")
        print("3. 正常使用matplotlib，中文字符将正确显示")
    else:
        print("\n🔧 问题排查:")
        print("1. 检查字体管理库是否在正确位置")
        print("2. 运行 test_font_manager.py 进行基础测试")
        print("3. 查看错误信息进行调试")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)