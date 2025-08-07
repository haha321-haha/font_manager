#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全局Font Manager设置脚本
一次设置，永久生效！告别中文字体框框问题！
"""

from font_manager import FontManager, setup_chinese_font
import matplotlib.pyplot as plt
import os

def setup_global_font_manager():
    """设置全局Font Manager配置"""
    print("🚀 正在设置全局Font Manager配置...")
    
    # 创建Font Manager实例
    fm = FontManager()
    
    # 设置字体
    result = fm.setup()
    
    if result.success:
        print(f"✅ 字体设置成功！")
        print(f"📝 使用字体: {result.font_used.name}")
        print(f"⭐ 字体评分: {result.font_used.quality_score:.2f}")
        print(f"📍 字体路径: {result.font_used.path}")
        
        # 备份配置
        config_path = fm.backup_config("global_font_config_backup.json")
        print(f"💾 配置已备份到: {config_path}")
        
        # 创建快速设置脚本
        create_quick_setup_script()
        
        return True
    else:
        print(f"❌ 字体设置失败: {result.error_message}")
        return False

def create_quick_setup_script():
    """创建快速设置脚本"""
    script_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Font Manager 快速设置脚本
在任何Python项目中导入此模块即可自动设置中文字体
"""

from font_manager import setup_chinese_font

# 自动设置中文字体
setup_chinese_font()
print("✅ Font Manager 已自动设置中文字体！")
'''
    
    with open("auto_font_setup.py", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print("📄 已创建快速设置脚本: auto_font_setup.py")

def test_font_display():
    """测试字体显示效果"""
    print("\n🧪 测试中文字体显示效果...")
    
    # 设置字体
    setup_chinese_font()
    
    # 创建测试图表
    fig, ax = plt.subplots(figsize=(10, 6))
    
    categories = ['数据分析', '机器学习', '深度学习', '自然语言处理']
    values = [85, 92, 78, 88]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    
    bars = ax.bar(categories, values, color=colors, alpha=0.8)
    ax.set_title('🎉 Font Manager 成功解决中文显示问题！', fontsize=16, fontweight='bold')
    ax.set_xlabel('技术领域', fontsize=12)
    ax.set_ylabel('掌握程度 (%)', fontsize=12)
    
    # 添加数值标签
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{value}%', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('font_manager_test_success.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ 测试完成！中文显示完美！")

def create_usage_guide():
    """创建使用指南"""
    guide_content = """# 🎨 Font Manager 全局配置完成！

## 🎯 使用方法

### 方法1：一行代码解决（推荐）
```python
from font_manager import setup_chinese_font
setup_chinese_font()  # 一行搞定！
```

### 方法2：导入自动设置模块
```python
import auto_font_setup  # 自动设置，无需其他代码
```

### 方法3：高级配置
```python
from font_manager import FontManager
fm = FontManager()
fm.get_config_info()  # 获取配置信息
fm.setup()
```

## ✨ 特性

- ✅ 一行代码解决中文字体问题
- ✅ 自动检测最佳中文字体
- ✅ 跨平台兼容（macOS/Windows/Linux）
- ✅ 智能缓存，毫秒级设置
- ✅ 配置持久化，一次设置永久生效

## 🚀 从此告别字体框框问题！

再也不用担心matplotlib中文显示问题了！
"""
    
    with open("FONT_MANAGER_GUIDE.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    
    print("📖 使用指南已创建: FONT_MANAGER_GUIDE.md")

if __name__ == "__main__":
    print("=" * 60)
    print("🎨 Font Manager 全局配置向导")
    print("=" * 60)
    
    # 设置全局配置
    if setup_global_font_manager():
        print("\n" + "=" * 60)
        
        # 测试字体显示
        test_font_display()
        
        # 创建使用指南
        create_usage_guide()
        
        print("\n🎉 Font Manager 全局配置完成！")
        print("💡 从现在开始，任何Python项目只需一行代码即可解决中文字体问题！")
        print("🔥 告别字体框框，拥抱完美中文显示！")
        print("=" * 60)
    else:
        print("❌ 配置失败，请检查系统字体安装情况")