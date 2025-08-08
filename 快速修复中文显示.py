#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FontManager一键修复中文显示问题

使用方法：
    python 快速修复中文显示.py

这个脚本会自动检测并配置中文字体，解决matplotlib中文字体显示为方框的问题。
"""

import sys
import os

# 将当前目录添加到Python路径
sys.path.insert(0, os.path.dirname(__file__))

from font_manager import setup_matplotlib_chinese

def main():
    """主函数：一键修复中文显示"""
    print("🎯 FontManager 中文显示修复工具")
    print("=" * 50)
    
    try:
        # 一键设置中文字体
        print("🔍 正在检测并配置中文字体...")
        result = setup_matplotlib_chinese()
        
        if result.success:
            print("\n✅ 修复成功！")
            print(f"📱 已配置字体: {result.font_used.name}")
            print(f"📊 备用字体: {len(result.fallback_fonts)}个")
            print("\n🎊 现在matplotlib可以正常显示中文了！")
            print("\n💡 使用方法：")
            print("   在任何Python代码中，先运行：")
            print("   from font_manager import setup_matplotlib_chinese")
            print("   setup_matplotlib_chinese()")
        else:
            print("\n⚠️  字体设置遇到问题：")
            for error in result.errors:
                print(f"   ❌ {error}")
            print("\n💡 解决方案：")
            print("   1. 确保系统已安装中文字体")
            print("   2. 尝试重启Python环境")
            print("   3. 检查FontManager日志")
            
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        print("💡 请检查FontManager是否已正确安装")
        
    print("=" * 50)

if __name__ == "__main__":
    main()