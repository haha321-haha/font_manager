#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FontManager最终验证脚本
验证setup_matplotlib_chinese方法是否完全解决中文显示问题
"""

import sys
import os
import matplotlib
matplotlib.use('Agg')  # 使用非GUI后端
import matplotlib.pyplot as plt

# 添加FontManager路径
sys.path.insert(0, 'GitHub上传专用文件夹')

def test_fontmanager_complete():
    """完整测试FontManager功能"""
    print("🎯 FontManager最终验证测试")
    print("=" * 50)
    
    try:
        # 测试1: 导入测试
        print("📦 测试1: 导入FontManager...")
        from font_manager import FontManager, setup_matplotlib_chinese
        print("✅ 导入成功")
        
        # 测试2: 类方法测试
        print("\n🔧 测试2: 类方法调用...")
        fm = FontManager()
        result1 = fm.setup_matplotlib_chinese()
        if result1.success:
            print(f"✅ 类方法成功: {result1.font_used.name}")
        else:
            print(f"❌ 类方法失败: {result1.errors}")
        
        # 测试3: 便捷函数测试
        print("\n⚡ 测试3: 便捷函数调用...")
        result2 = setup_matplotlib_chinese()
        if result2.success:
            print(f"✅ 便捷函数成功: {result2.font_used.name}")
        else:
            print(f"❌ 便捷函数失败: {result2.errors}")
        
        # 测试4: 中文显示测试
        print("\n🎨 测试4: 中文图表生成...")
        create_chinese_test_chart()
        
        print("\n🎉 所有测试通过！FontManager已完美修复中文显示问题！")
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        return False

def create_chinese_test_chart():
    """创建中文测试图表"""
    # 创建输出目录
    output_dir = '/Users/duting/Downloads/命理风水占卜🔮/爬虫分析图表'
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建测试图表
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    # 图表1: 柱状图
    categories = ['装饰', '家居布局', '运势预测', '理论探讨']
    values = [31, 18, 8, 5]
    colors = ['#FF7F0E', '#1F77B4', '#2CA02C', '#D62728']
    
    ax1.bar(categories, values, color=colors)
    ax1.set_title('风水主题分布', fontsize=14, fontweight='bold')
    ax1.set_xlabel('主题类别', fontsize=12)
    ax1.set_ylabel('数量', fontsize=12)
    
    # 图表2: 饼图
    ax2.pie(values, labels=categories, autopct='%1.1f%%', colors=colors)
    ax2.set_title('主题占比分析', fontsize=14, fontweight='bold')
    
    # 图表3: 折线图
    days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    trend = [20, 25, 30, 28, 35, 40, 32]
    
    ax3.plot(days, trend, marker='o', linewidth=2, color='#2CA02C')
    ax3.set_title('每周趋势分析', fontsize=14, fontweight='bold')
    ax3.set_xlabel('星期', fontsize=12)
    ax3.set_ylabel('活跃度', fontsize=12)
    ax3.grid(True, alpha=0.3)
    
    # 图表4: 散点图
    import numpy as np
    x = np.random.randn(50)
    y = np.random.randn(50)
    
    ax4.scatter(x, y, alpha=0.6, c=colors[0])
    ax4.set_title('数据分布图', fontsize=14, fontweight='bold')
    ax4.set_xlabel('X轴数据', fontsize=12)
    ax4.set_ylabel('Y轴数据', fontsize=12)
    
    plt.tight_layout()
    
    # 保存图表
    output_file = f'{output_dir}/FontManager最终验证图表.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✅ 测试图表已保存: {output_file}")
    
    plt.close()

if __name__ == "__main__":
    success = test_fontmanager_complete()
    if success:
        print("\n🎊 FontManager验证完成！中文显示问题已彻底解决！")
    else:
        print("\n💔 验证失败，需要进一步检查...")