#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Font Manager 演示脚本

展示字体管理库的实际使用效果。
"""

import sys
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# 添加font_manager到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from font_manager import FontManager


def create_demo_chart_before():
    """创建使用默认字体的图表（修复前）"""
    print("📊 创建默认字体图表...")
    
    # 重置matplotlib配置
    plt.rcdefaults()
    
    # 创建测试数据
    languages = ['英语', '中文', '日语', '土耳其语', '西班牙语']
    counts = [258, 254, 209, 104, 9]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    
    # 创建图表
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(languages, counts, color=colors, alpha=0.8)
    
    # 设置标题和标签
    ax.set_title('推文语言分布 - 默认字体', fontsize=16, fontweight='bold')
    ax.set_xlabel('语言', fontsize=12)
    ax.set_ylabel('推文数量', fontsize=12)
    
    # 添加数值标签
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{count}', ha='center', va='bottom', fontsize=10)
    
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # 保存图表
    output_path = 'demo_before_font_fix.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"✅ 默认字体图表已保存: {output_path}")
    return output_path


def create_demo_chart_after():
    """创建使用字体管理库的图表（修复后）"""
    print("📊 创建字体管理库图表...")
    
    # 使用字体管理库设置字体
    fm = FontManager()
    result = fm.setup()
    
    if result.success:
        print(f"✅ 字体设置成功: {result.font_used.name}")
    else:
        print("⚠️ 字体设置失败，使用默认字体")
    
    # 创建测试数据
    languages = ['英语', '中文', '日语', '土耳其语', '西班牙语']
    counts = [258, 254, 209, 104, 9]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    
    # 创建图表
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(languages, counts, color=colors, alpha=0.8)
    
    # 设置标题和标签
    font_name = result.font_used.name if result.font_used else "默认字体"
    ax.set_title(f'推文语言分布 - {font_name}', fontsize=16, fontweight='bold')
    ax.set_xlabel('语言', fontsize=12)
    ax.set_ylabel('推文数量', fontsize=12)
    
    # 添加数值标签
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{count}', ha='center', va='bottom', fontsize=10)
    
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # 保存图表
    output_path = 'demo_after_font_fix.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"✅ 字体管理库图表已保存: {output_path}")
    return output_path


def create_comprehensive_demo():
    """创建综合演示图表"""
    print("📊 创建综合演示图表...")
    
    # 使用字体管理库
    fm = FontManager()
    result = fm.setup()
    
    # 创建综合图表
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    
    # 图表1: 语言分布柱状图
    languages = ['英语', '中文', '日语', '土耳其语', '西班牙语']
    counts = [258, 254, 209, 104, 9]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    
    bars = ax1.bar(languages, counts, color=colors, alpha=0.8)
    ax1.set_title('推文语言分布', fontsize=14, fontweight='bold')
    ax1.set_ylabel('推文数量', fontsize=12)
    
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{count}', ha='center', va='bottom', fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # 图表2: 时间趋势线图
    dates = np.arange(30)
    values = np.random.randint(10, 50, 30)
    
    ax2.plot(dates, values, marker='o', linewidth=2, markersize=4, color='#FF6B6B')
    ax2.set_title('推文发布时间趋势', fontsize=14, fontweight='bold')
    ax2.set_xlabel('天数', fontsize=12)
    ax2.set_ylabel('推文数量', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    # 图表3: 互动类型分布
    categories = ['点赞', '转发', '回复', '引用']
    values = [1250, 680, 420, 180]
    
    ax3.bar(categories, values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'], alpha=0.8)
    ax3.set_title('互动类型分布', fontsize=14, fontweight='bold')
    ax3.set_ylabel('总数量', fontsize=12)
    
    for i, v in enumerate(values):
        ax3.text(i, v + 20, str(v), ha='center', va='bottom', fontsize=10)
    ax3.grid(True, alpha=0.3)
    
    # 图表4: 内容分类饼图
    sizes = [30, 25, 20, 15, 10]
    labels = ['风水占卜', '命理分析', '运势预测', '塔罗牌', '其他']
    
    wedges, texts, autotexts = ax4.pie(sizes, labels=labels, autopct='%1.1f%%', 
                                       startangle=90, colors=colors)
    ax4.set_title('内容分类分布', fontsize=14, fontweight='bold')
    
    # 设置饼图文字样式
    for text in texts:
        text.set_fontsize(10)
    for autotext in autotexts:
        autotext.set_fontsize(9)
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    # 添加总标题
    font_name = result.font_used.name if result.font_used else "默认字体"
    fig.suptitle(f'Twitter数据分析综合报告 - 使用{font_name}', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # 保存图表
    output_path = 'demo_comprehensive.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"✅ 综合演示图表已保存: {output_path}")
    return output_path


def show_font_info():
    """显示字体信息"""
    print("\n🔍 字体管理库信息:")
    print("-" * 40)
    
    fm = FontManager()
    
    # 显示平台信息
    print(f"运行平台: {fm.platform.value}")
    
    # 设置字体
    result = fm.setup()
    print(f"字体设置: {'✅ 成功' if result.success else '❌ 失败'}")
    
    if result.font_used:
        font = result.font_used
        print(f"使用字体: {font.name}")
        print(f"字体路径: {font.path}")
        print(f"中文支持: {'✅' if font.supports_chinese else '❌'}")
        print(f"质量评分: {font.quality_score:.2f}")
    
    # 显示可用字体
    fonts = fm.get_available_fonts()
    print(f"\n可用字体 ({len(fonts)} 个):")
    for i, font in enumerate(fonts, 1):
        print(f"  {i}. {font.name} - 评分: {font.quality_score:.2f}")
    
    # 验证配置
    report = fm.validate()
    print(f"\n配置验证:")
    print(f"  状态: {report.status}")
    print(f"  综合评分: {report.overall_score:.2f}")
    print(f"  验证耗时: {report.validation_time:.3f}秒")


def main():
    """主演示函数"""
    print("🚀 Font Manager 演示")
    print("=" * 50)
    
    try:
        # 显示字体信息
        show_font_info()
        
        print("\n📊 生成演示图表...")
        print("-" * 40)
        
        # 创建对比图表
        before_chart = create_demo_chart_before()
        after_chart = create_demo_chart_after()
        
        # 创建综合演示
        comprehensive_chart = create_comprehensive_demo()
        
        print(f"\n🎉 演示完成！生成了以下文件:")
        print(f"  📈 {before_chart} - 修复前对比")
        print(f"  📈 {after_chart} - 修复后效果")
        print(f"  📈 {comprehensive_chart} - 综合演示")
        
        print(f"\n💡 使用说明:")
        print(f"  1. 查看生成的图表文件，对比中文字体显示效果")
        print(f"  2. 在你的项目中导入: from font_manager import FontManager")
        print(f"  3. 一行代码设置字体: FontManager().setup()")
        print(f"  4. 或使用便捷函数: setup_chinese_font()")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 演示过程中出错: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)