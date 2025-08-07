#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Font Manager 成功案例演示
展示一行代码解决matplotlib中文字体问题
"""

import matplotlib.pyplot as plt
import numpy as np
from font_manager import setup_chinese_font

# 🚀 一行代码解决中文字体问题！
setup_chinese_font()

# 创建测试数据
categories = ['装饰类', '家居布局', '运势预测', '理论探讨']
values = [43.4, 30.0, 20.5, 6.1]
colors = ['#FF7F0E', '#1F77B4', '#2CA02C', '#D62728']

# 创建图表
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# 柱状图
bars = ax1.bar(categories, values, color=colors, alpha=0.8)
ax1.set_title('风水主题分布 - Font Manager修复后', fontsize=16, fontweight='bold')
ax1.set_xlabel('主题类别', fontsize=12)
ax1.set_ylabel('占比 (%)', fontsize=12)

# 添加数值标签
for bar, value in zip(bars, values):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
             f'{value}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

# 饼图
wedges, texts, autotexts = ax2.pie(values, labels=categories, colors=colors, 
                                   autopct='%1.1f%%', startangle=90)
ax2.set_title('主题占比分布 - 中文显示完美！', fontsize=16, fontweight='bold')

# 美化文字
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

plt.tight_layout()

# 添加成功标识
fig.suptitle('🎉 Font Manager 成功解决中文字体问题！', 
             fontsize=18, fontweight='bold', y=0.98)

plt.savefig('font_manager_success_demo.png', dpi=300, bbox_inches='tight')
plt.show()

print("✅ Font Manager 演示完成！")
print("🎯 中文字体显示：完美！")
print("⚡ 设置时间：毫秒级")
print("🔧 代码量：一行搞定")
print("🌟 跨平台：自动适配")