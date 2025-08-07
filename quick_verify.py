#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Font Manager GitHub版本快速验证脚本
30秒内验证Font Manager是否正常工作
"""

def quick_test():
    """快速测试Font Manager核心功能"""
    print("🚀 Font Manager GitHub版本快速验证...")
    print("-" * 40)
    
    try:
        # 测试1: 导入
        print("📦 测试导入...", end=" ")
        from font_manager import setup_chinese_font, FontManager
        print("✅")
        
        # 测试2: 一行代码解决方案
        print("🔧 测试一行代码解决方案...", end=" ")
        setup_chinese_font()
        print("✅")
        
        # 测试3: FontManager类和修复的bug
        print("🏗️  测试FontManager类...", end=" ")
        fm = FontManager()
        result = fm.setup()
        if result.success:
            # 关键：测试修复的属性
            score = result.font_used.quality_score  # 之前的bug
            print("✅")
            print(f"   字体: {result.font_used.name}")
            print(f"   评分: {score:.2f}")
        else:
            print("❌")
            return False
        
        # 测试4: 配置备份（修复的另一个bug）
        print("💾 测试配置备份...", end=" ")
        backup_path = fm.backup_config()
        print("✅")
        
        print("-" * 40)
        print("🎉 所有核心功能测试通过！")
        print("✅ Font Manager GitHub版本工作正常！")
        print("✅ 修复的bug已解决！")
        print("🚀 可以正常使用一行代码解决中文字体问题！")
        return True
        
    except AttributeError as e:
        print("❌")
        print(f"🐛 AttributeError: {e}")
        print("⚠️  这表明修复的bug可能还存在问题！")
        return False
    except Exception as e:
        print("❌")
        print(f"❌ 错误: {e}")
        return False

if __name__ == "__main__":
    success = quick_test()
    if not success:
        print("\n🔧 建议检查GitHub上传的文件是否包含修复后的版本")
    exit(0 if success else 1)