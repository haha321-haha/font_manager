#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FontManager风水分析中文显示演示

演示如何使用FontManager解决风水数据可视化中的中文显示问题
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from font_manager import setup_matplotlib_chinese
import os

# 1. 首先设置中文字体
print("🔧 使用FontManager修复中文显示...")
setup_matplotlib_chinese()

# 2. 创建模拟风水数据
data = {
    '主题': ['运势预测', '家居布局', '装饰摆件', '理论探讨', '风水用品'],
    '数量': [45, 30, 25, 20, 15],
    '互动量': [1200, 800, 650, 400, 300]
}

df = pd.DataFrame(data)

# 3. 创建中文风水分析图表
output_dir = os.path.join(os.path.dirname(__file__), 'demo_output')
os.makedirs(output_dir, exist_ok=True)

print("📊 正在生成中文风水分析图表...")

# 图表1: 主题分布
plt.figure(figsize=(12, 8))
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57']

bars = plt.bar(df['主题'], df['数量'], color=colors)
plt.title('风水主题分布分析', fontsize=16, fontweight='bold')
plt.xlabel('风水主题', fontsize=12)
plt.ylabel('推文数量', fontsize=12)

# 添加数值标签
for bar, value in zip(bars, df['数量']):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
             str(value), ha='center', va='bottom', fontsize=11)

plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '风水主题分布.png'), dpi=300, bbox_inches='tight')
plt.close()

# 图表2: 互动量分析
plt.figure(figsize=(12, 8))
plt.scatter(df['数量'], df['互动量'], s=100, c=colors, alpha=0.7)
plt.title('风水主题互动量分析', fontsize=16, fontweight='bold')
plt.xlabel('主题数量', fontsize=12)
plt.ylabel('总互动量', fontsize=12)

# 添加标签
for i, txt in enumerate(df['主题']):
    plt.annotate(txt, (df['数量'][i], df['互动量'][i]), 
                xytext=(5, 5), textcoords='offset points', fontsize=10)

plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '风水互动分析.png'), dpi=300, bbox_inches='tight')
plt.close()

# 图表3: 综合展示
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
fig.suptitle('风水数据综合可视化', fontsize=18, fontweight='bold')

# 子图1: 饼图
ax1.pie(df['数量'], labels=df['主题'], colors=colors, autopct='%1.1f%%', startangle=90)
ax1.set_title('主题比例分布', fontsize=14)

# 子图2: 柱状图
bars = ax2.bar(df['主题'], df['互动量'], color=colors)
ax2.set_title('各主题互动量', fontsize=14)
ax2.set_ylabel('互动量', fontsize=12)

# 旋转x轴标签
ax2.tick_params(axis='x', rotation=45)

# 添加数值标签
for bar, value in zip(bars, df['互动量']):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
             str(value), ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '风水综合分析.png'), dpi=300, bbox_inches='tight')
plt.close()

print("✅ 中文风水分析图表已生成完成！")
print(f"📁 图表保存在: {output_dir}")
print("\n生成的文件:")
for file in os.listdir(output_dir):
    if file.endswith('.png'):
        print(f"   📊 {file}")

print("\n🎊 FontManager已成功解决中文显示问题！")
print("💡 使用方法：在任何matplotlib代码前添加两行：")
print("   from font_manager import setup_matplotlib_chinese")
print("   setup_matplotlib_chinese()")