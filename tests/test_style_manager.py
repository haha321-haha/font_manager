#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Style Manager 测试脚本

测试样式管理器的功能。
"""

import sys
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# 添加font_manager到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from font_manager import StyleManager, FontStyleConfig, FontManager
from font_manager.utils.logger import setup_logging


def test_style_manager_basic():
    """测试样式管理器基础功能"""
    print("🎨 测试样式管理器基础功能...")
    
    try:
        print("\n1️⃣ 创建样式管理器...")
        style_manager = StyleManager()
        print("✅ 样式管理器创建成功")
        
        print("\n2️⃣ 测试主题管理...")
        themes = style_manager.get_available_themes()
        print(f"✅ 可用主题: {themes}")
        
        current_theme = style_manager.get_current_theme()
        print(f"✅ 当前主题: {current_theme.name if current_theme else 'None'}")
        
        print("\n3️⃣ 测试样式获取...")
        title_style = style_manager.get_style('title')
        if title_style:
            print(f"✅ 标题样式: 大小={title_style.font_size}, 粗细={title_style.font_weight}")
        
        legend_style = style_manager.get_style('legend')
        if legend_style:
            print(f"✅ 图例样式: 大小={legend_style.font_size}, 颜色={legend_style.color}")
        
        print("\n4️⃣ 测试样式设置...")
        custom_style = FontStyleConfig(
            font_size=18,
            font_weight=800,
            color='navy'
        )
        success = style_manager.set_style('title', custom_style)
        print(f"✅ 自定义样式设置: {'成功' if success else '失败'}")
        
        print("\n5️⃣ 测试样式更新...")
        success = style_manager.update_style('legend', font_size=12, color='darkgreen')
        print(f"✅ 样式更新: {'成功' if success else '失败'}")
        
        print("\n6️⃣ 测试主题切换...")
        success = style_manager.set_theme('academic')
        print(f"✅ 主题切换到学术论文: {'成功' if success else '失败'}")
        
        success = style_manager.set_theme('business')
        print(f"✅ 主题切换到商业报告: {'成功' if success else '失败'}")
        
        print("\n7️⃣ 测试样式摘要...")
        summary = style_manager.get_style_summary()
        print(f"✅ 样式摘要:")
        print(f"   当前主题: {summary['current_theme']}")
        print(f"   自定义样式数: {summary['custom_styles_count']}")
        print(f"   自定义样式: {summary['custom_styles']}")
        
        print("\n🎉 样式管理器基础功能测试完成！")
        return True
        
    except Exception as e:
        print(f"\n❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_theme_management():
    """测试主题管理功能"""
    print("\n🎭 测试主题管理功能...")
    
    try:
        style_manager = StyleManager()
        
        print("1️⃣ 测试主题创建...")
        new_theme = style_manager.create_theme('custom', 'default')
        print(f"✅ 新主题创建成功: {new_theme.name}")
        
        print("2️⃣ 测试主题导出...")
        theme_data = style_manager.export_theme('custom')
        if theme_data:
            print(f"✅ 主题导出成功，包含 {len(theme_data['styles'])} 个样式")
        
        print("3️⃣ 测试主题导入...")
        # 修改主题数据
        theme_data['name'] = 'imported_theme'
        theme_data['styles']['title']['font_size'] = 20
        
        success = style_manager.import_theme(theme_data)
        print(f"✅ 主题导入: {'成功' if success else '失败'}")
        
        print("4️⃣ 测试主题删除...")
        success = style_manager.delete_theme('custom')
        print(f"✅ 主题删除: {'成功' if success else '失败'}")
        
        # 尝试删除内置主题（应该失败）
        success = style_manager.delete_theme('default')
        print(f"✅ 内置主题删除保护: {'正常' if not success else '异常'}")
        
        print("✅ 主题管理功能测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 主题管理测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_matplotlib_integration():
    """测试matplotlib集成"""
    print("\n📊 测试matplotlib集成...")
    
    try:
        # 设置字体管理器
        fm = FontManager()
        result = fm.setup()
        
        if not result.success:
            print("⚠️ 字体设置失败，继续测试")
        
        print("1️⃣ 测试样式应用...")
        
        # 设置自定义样式
        fm.set_font_style('title', font_size=18, font_weight=800, color='navy')
        fm.set_font_style('legend', font_size=11, color='darkgreen')
        
        # 应用样式到matplotlib
        success1 = fm.apply_style_to_matplotlib('title')
        success2 = fm.apply_style_to_matplotlib('legend')
        
        print(f"✅ 标题样式应用: {'成功' if success1 else '失败'}")
        print(f"✅ 图例样式应用: {'成功' if success2 else '失败'}")
        
        print("2️⃣ 测试主题切换...")
        themes = fm.get_available_themes()
        print(f"✅ 可用主题: {themes}")
        
        for theme in ['academic', 'business', 'default']:
            success = fm.set_theme(theme)
            current = fm.get_current_theme()
            print(f"   {theme}: {'✅' if success and current == theme else '❌'}")
        
        print("3️⃣ 创建测试图表...")
        create_style_test_chart(fm)
        
        print("✅ matplotlib集成测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ matplotlib集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def create_style_test_chart(fm):
    """创建样式测试图表"""
    # 创建测试数据
    categories = ['默认主题', '学术论文', '商业报告', '自定义主题']
    values = [85, 92, 88, 95]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    
    # 创建图表
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 图表1: 柱状图
    bars = ax1.bar(categories, values, color=colors, alpha=0.8)
    ax1.set_title('样式主题效果对比', fontsize=16, fontweight='bold')
    ax1.set_ylabel('效果评分', fontsize=12)
    ax1.set_xlabel('主题类型', fontsize=12)
    
    # 添加数值标签
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{value}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax1.grid(True, alpha=0.3)
    ax1.legend(['评分'], loc='upper right')
    
    # 图表2: 饼图
    sizes = [30, 25, 25, 20]
    labels = ['标题样式', '轴标签', '图例', '注释']
    
    wedges, texts, autotexts = ax2.pie(sizes, labels=labels, autopct='%1.1f%%', 
                                       startangle=90, colors=colors)
    ax2.set_title('样式元素分布', fontsize=16, fontweight='bold')
    
    # 设置饼图文字样式
    for text in texts:
        text.set_fontsize(11)
    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')
        autotext.set_color('white')
    
    # 设置总标题
    current_theme = fm.get_current_theme()
    fig.suptitle(f'Font Manager 样式管理演示 - 当前主题: {current_theme}', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # 保存图表
    output_path = 'style_manager_test.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"✅ 样式测试图表已保存: {output_path}")


def test_font_style_config():
    """测试FontStyleConfig类"""
    print("\n⚙️ 测试FontStyleConfig类...")
    
    try:
        print("1️⃣ 测试基础创建...")
        style = FontStyleConfig(
            font_size=14,
            font_weight=600,
            color='blue'
        )
        print(f"✅ 样式创建成功: 大小={style.font_size}, 颜色={style.color}")
        
        print("2️⃣ 测试matplotlib属性转换...")
        props = style.to_matplotlib_props()
        print(f"✅ matplotlib属性: {props}")
        
        print("3️⃣ 测试字典转换...")
        style_dict = style.to_dict()
        print(f"✅ 字典格式: {len(style_dict)} 个属性")
        
        print("4️⃣ 测试从字典创建...")
        new_style = FontStyleConfig.from_dict(style_dict)
        print(f"✅ 从字典创建成功: {new_style.font_size}")
        
        print("5️⃣ 测试样式更新...")
        updated_style = style.update(font_size=16, color='red')
        print(f"✅ 样式更新: 大小={updated_style.font_size}, 颜色={updated_style.color}")
        
        print("6️⃣ 测试样式复制...")
        copied_style = style.copy()
        print(f"✅ 样式复制: {copied_style.font_size == style.font_size}")
        
        print("✅ FontStyleConfig类测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ FontStyleConfig测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("🚀 Style Manager 功能测试")
    print("=" * 50)
    
    # 设置日志
    setup_logging(level="INFO", enable_color=True)
    
    success_count = 0
    total_tests = 4
    
    # 运行测试
    if test_font_style_config():
        success_count += 1
    
    if test_style_manager_basic():
        success_count += 1
    
    if test_theme_management():
        success_count += 1
    
    if test_matplotlib_integration():
        success_count += 1
    
    # 输出结果
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {success_count}/{total_tests} 通过")
    
    if success_count == total_tests:
        print("🎉 所有测试通过！样式管理功能正常！")
        return True
    else:
        print("❌ 部分测试失败，需要修复问题")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)