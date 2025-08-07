# 🧪 GitHub上传后完整测试指南

## 🎯 测试目标
确保Font Manager在GitHub上传后能够：
- ✅ 正常安装
- ✅ 无AttributeError错误
- ✅ 中文字体显示正常
- ✅ 一行代码解决方案有效

## 📋 测试步骤

### 第一步：基础安装测试

```bash
# 1. 从GitHub直接安装
pip install git+https://github.com/haha321-haha/font_manager.git

# 2. 验证安装成功
python -c "import font_manager; print('✅ 安装成功！')"
```

### 第二步：核心功能测试

```bash
# 3. 测试一行代码解决方案
python -c "from font_manager import setup_chinese_font; setup_chinese_font(); print('✅ 字体设置成功！')"

# 4. 测试FontManager类
python -c "from font_manager import FontManager; fm = FontManager(); result = fm.setup(); print(f'✅ 字体: {result.font_used.name}' if result.success else '❌ 失败')"
```

### 第三步：属性错误检测

```bash
# 5. 检测修复的FontInfo.quality_score属性
python -c "
from font_manager import FontManager
fm = FontManager()
result = fm.setup()
if result.success:
    print(f'✅ quality_score: {result.font_used.quality_score:.2f}')
    print('✅ FontInfo属性修复成功！')
else:
    print('❌ 设置失败')
"
```

### 第四步：演示脚本测试

```bash
# 6. 下载并运行演示脚本
curl -O https://raw.githubusercontent.com/haha321-haha/font_manager/main/font_manager_success_demo.py
python font_manager_success_demo.py

# 7. 运行全局配置脚本
curl -O https://raw.githubusercontent.com/haha321-haha/font_manager/main/setup_global_font_manager.py
python setup_global_font_manager.py
```

### 第五步：matplotlib中文显示测试

```bash
# 8. 创建并运行中文显示测试
cat > test_chinese_display.py << 'EOF'
import matplotlib.pyplot as plt
from font_manager import setup_chinese_font

# 一行代码解决中文字体问题
setup_chinese_font()

# 测试中文显示
plt.figure(figsize=(8, 6))
plt.plot([1, 2, 3, 4], [1, 4, 2, 3], 'o-')
plt.title('中文标题测试 - Font Manager')
plt.xlabel('横轴标签')
plt.ylabel('纵轴标签')
plt.text(2, 3, '中文文本显示测试', fontsize=12, ha='center')
plt.savefig('chinese_font_test.png', dpi=150, bbox_inches='tight')
print('✅ 中文字体显示测试完成！检查 chinese_font_test.png 文件')
plt.show()
EOF

python test_chinese_display.py
```

## 🔍 自动化测试脚本

### 创建一键测试脚本

```bash
# 9. 创建自动化测试脚本
cat > github_font_manager_test.py << 'EOF'
#!/usr/bin/env python3
"""
Font Manager GitHub版本自动化测试脚本
"""
import sys
import traceback
import matplotlib.pyplot as plt

def test_import():
    """测试导入"""
    try:
        import font_manager
        print("✅ 1. 导入测试通过")
        return True
    except Exception as e:
        print(f"❌ 1. 导入测试失败: {e}")
        return False

def test_setup_function():
    """测试setup_chinese_font函数"""
    try:
        from font_manager import setup_chinese_font
        setup_chinese_font()
        print("✅ 2. setup_chinese_font函数测试通过")
        return True
    except Exception as e:
        print(f"❌ 2. setup_chinese_font函数测试失败: {e}")
        return False

def test_font_manager_class():
    """测试FontManager类"""
    try:
        from font_manager import FontManager
        fm = FontManager()
        result = fm.setup()
        if result.success:
            print(f"✅ 3. FontManager类测试通过 - 字体: {result.font_used.name}")
            return True
        else:
            print(f"❌ 3. FontManager类测试失败: {result.error_message}")
            return False
    except Exception as e:
        print(f"❌ 3. FontManager类测试失败: {e}")
        return False

def test_fontinfo_attributes():
    """测试FontInfo属性（修复的bug）"""
    try:
        from font_manager import FontManager
        fm = FontManager()
        result = fm.setup()
        if result.success:
            # 测试修复的属性
            score = result.font_used.quality_score
            name = result.font_used.name
            path = result.font_used.path
            print(f"✅ 4. FontInfo属性测试通过 - 评分: {score:.2f}")
            return True
        else:
            print("❌ 4. FontInfo属性测试失败 - 字体设置失败")
            return False
    except AttributeError as e:
        print(f"❌ 4. FontInfo属性测试失败 - AttributeError: {e}")
        return False
    except Exception as e:
        print(f"❌ 4. FontInfo属性测试失败: {e}")
        return False

def test_chinese_display():
    """测试中文显示"""
    try:
        from font_manager import setup_chinese_font
        setup_chinese_font()
        
        plt.figure(figsize=(6, 4))
        plt.plot([1, 2, 3], [1, 4, 2])
        plt.title('中文测试')
        plt.xlabel('测试')
        plt.ylabel('数值')
        plt.savefig('test_output.png', bbox_inches='tight')
        plt.close()
        
        print("✅ 5. 中文显示测试通过 - 已生成test_output.png")
        return True
    except Exception as e:
        print(f"❌ 5. 中文显示测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 Font Manager GitHub版本测试开始...")
    print("=" * 50)
    
    tests = [
        test_import,
        test_setup_function,
        test_font_manager_class,
        test_fontinfo_attributes,
        test_chinese_display
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            traceback.print_exc()
    
    print("=" * 50)
    print(f"🎯 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！Font Manager GitHub版本工作正常！")
        return True
    else:
        print("⚠️  部分测试失败，请检查问题")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
EOF

python github_font_manager_test.py
```

## 📊 测试结果判断

### ✅ 成功标准
- 所有5个测试都通过
- 无AttributeError错误
- 生成的图片中中文显示正常
- 控制台输出显示字体设置成功

### ❌ 失败情况处理
如果测试失败，检查：
1. **导入失败** - 检查安装是否成功
2. **AttributeError** - 检查是否上传了修复后的文件
3. **字体设置失败** - 检查系统字体支持
4. **中文显示异常** - 检查matplotlib配置

## 🔧 问题排查命令

```bash
# 检查安装的版本信息
python -c "import font_manager; print(font_manager.__version__ if hasattr(font_manager, '__version__') else 'Version info not available')"

# 检查可用字体
python -c "from font_manager import FontManager; fm = FontManager(); fonts = fm.get_available_fonts(); print(f'找到 {len(fonts)} 个字体')"

# 详细错误信息
python -c "
import traceback
try:
    from font_manager import FontManager
    fm = FontManager()
    result = fm.setup()
    print('成功!' if result.success else f'失败: {result.error_message}')
except Exception as e:
    print('详细错误信息:')
    traceback.print_exc()
"
```

## 📱 快速验证命令（一行搞定）

```bash
# 超级快速测试（推荐）
python -c "
try:
    from font_manager import setup_chinese_font, FontManager
    setup_chinese_font()
    fm = FontManager()
    result = fm.setup()
    score = result.font_used.quality_score if result.success else 0
    print(f'🎉 Font Manager GitHub版本测试通过！字体: {result.font_used.name if result.success else \"未知\"}, 评分: {score:.2f}')
except Exception as e:
    print(f'❌ 测试失败: {e}')
"
```

---

## 🎯 测试完成后的确认

如果所有测试都通过，说明：
- ✅ Font Manager在GitHub上完美工作
- ✅ 修复的bug已解决
- ✅ 用户可以正常使用一行代码解决方案
- ✅ 告别字体框框问题！

**🚀 Font Manager GitHub版本质量保证！**