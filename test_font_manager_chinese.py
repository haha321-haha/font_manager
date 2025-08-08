#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FontManager中文显示测试脚本

这个脚本演示如何使用FontManager解决matplotlib中文显示问题。
当遇到中文显示为方框时，只需运行此脚本即可完美解决。
"""

import matplotlib
matplotlib.use('Agg')  # 非交互式

import matplotlib.pyplot as plt
import numpy as np
from font_manager import setup_matplotlib_chinese
import os

def test_chinese_display():
    """测试中文显示功能"""
    print("🎯 开始测试FontManager中文显示功能...")
    
    # 1. 设置中文字体
    print("📦 正在设置中文字体...")
    result = setup_matplotlib_chinese()
    
    if result.success:
        print(f"✅ 字体设置成功！使用字体: {result.font_used.name}")
    else:
        print("⚠️  字体设置失败，将使用默认字体")
    
    # 2. 创建测试图表
    print("📊 正在创建中文测试图表...")
    
    # 创建示例数据
    months = ['一月', '二月', '三月', '四月', '五月', '六月']
    values = [12, 19, 3, 5, 2, 3]
    
    # 创建图表
    plt.figure(figsize=(12, 8))
    
    # 主标题
    plt.title('FontManager中文显示测试', fontsize=16, pad=20)
    
    # 创建柱状图
    bars = plt.bar(months, values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3'])
    
    # 添加数据标签
    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                str(value), ha='center', va='bottom', fontsize=12)
    
    # 设置坐标轴标签
    plt.xlabel('月份', fontsize=12)
    plt.ylabel('数值', fontsize=12)
    
    # 添加网格
    plt.grid(axis='y', alpha=0.3)
    
    # 添加副标题
    plt.text(0.5, 0.95, 'FontManager完美解决中文显示问题', 
             transform=plt.gca().transAxes, ha='center', 
             fontsize=10, style='italic', color='gray')
    
    # 调整布局
    plt.tight_layout()
    
    # 保存测试图表
    output_dir = os.path.join(os.path.dirname(__file__), 'test_results')
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'font_manager_chinese_test.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ 测试图表已保存: {output_path}")
    
    # 3. 创建综合测试图表
    print("📈 正在创建综合测试图表...")
    
    # 创建多个子图测试不同字体元素
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('FontManager综合中文测试', fontsize=18, fontweight='bold')
    
    # 子图1: 折线图
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    ax1.plot(x, y, 'b-', linewidth=2)
    ax1.set_title('正弦函数示例')
    ax1.set_xlabel('横轴标签')
    ax1.set_ylabel('纵轴标签')
    ax1.grid(True, alpha=0.3)
    
    # 子图2: 饼图
    labels = ['北京', '上海', '广州', '深圳', '其他']
    sizes = [30, 25, 20, 15, 10]
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
    ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax2.set_title('城市分布比例')
    
    # 子图3: 散点图
    x = np.random.randn(50)
    y = np.random.randn(50)
    ax3.scatter(x, y, c='red', alpha=0.6, s=50)
    ax3.set_title('随机数据散点图')
    ax3.set_xlabel('X轴数据')
    ax3.set_ylabel('Y轴数据')
    ax3.grid(True, alpha=0.3)
    
    # 子图4: 直方图
    data = np.random.randn(1000)
    ax4.hist(data, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    ax4.set_title('正态分布直方图')
    ax4.set_xlabel('数值范围')
    ax4.set_ylabel('频数')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # 保存综合测试图表
    comprehensive_path = os.path.join(output_dir, 'font_manager_comprehensive_test.png')
    plt.savefig(comprehensive_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ 综合测试图表已保存: {comprehensive_path}")
    
    # 4. 验证结果
    print("\n🎉 测试结果总结:")
    print(f"   ✅ 字体设置: {'成功' if result.success else '失败'}")
    print(f"   ✅ 使用字体: {result.font_used.name if result.font_used else '默认'}")
    print(f"   ✅ 备用字体: {len(result.fallback_fonts)}个")
    print(f"   ✅ 测试图表: 已生成并保存")
    
    return result.success

def quick_fix_script():
    """快速修复脚本 - 一键解决中文显示问题"""
    print("🚀 FontManager快速修复中文字体...")
    
    # 一键设置
    result = setup_matplotlib_chinese()
    
    if result.success:
        print("✅ 中文显示问题已解决！")
        print("📱 现在可以正常显示中文图表了")
    else:
        print("⚠️  修复可能未完全成功，请检查日志")
    
    return result

if __name__ == "__main__":
    # 运行完整测试
    success = test_chinese_display()
    
    if success:
        print("\n" + "="*50)
        print("🎊 恭喜！FontManager已成功解决中文显示问题")
        print("📊 现在matplotlib可以正常显示中文了")
        print("="*50)
    else:
        print("\n" + "="*50)
        print("⚠️  测试遇到问题，请检查FontManager配置")
        print("="*50)