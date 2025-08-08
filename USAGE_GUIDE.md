# 📖 FontManager 详细使用指南

## 🎯 **核心概念**

FontManager 是一个**进程级别**的字体管理工具，不是系统级别的永久设置。

### ✅ **能解决什么问题**
- matplotlib/seaborn 中文显示为方框 (□□□)
- 跨平台字体兼容性问题
- 字体检测和自动选择
- 字体质量评估和优化

### ❌ **不能解决什么问题**
- 系统级别的字体安装
- 非matplotlib库的字体问题
- 永久性的全局字体设置

## 🔄 **生效范围详解**

### 进程内永久生效
```python
from font_manager import setup_matplotlib_chinese

# 调用一次后，当前Python进程内所有matplotlib图表都能正常显示中文
setup_matplotlib_chinese()

# 以下所有图表都能正常显示中文
import matplotlib.pyplot as plt
plt.figure()
plt.title('第一个图表')  # ✅ 中文正常
plt.show()

plt.figure()
plt.title('第二个图表')  # ✅ 中文正常
plt.show()
```

### 需要重新调用的情况

#### 1. 新的Python进程
```python
# 脚本1.py
from font_manager import setup_matplotlib_chinese
setup_matplotlib_chinese()  # 设置成功

# 脚本2.py (新进程)
# 需要重新调用
from font_manager import setup_matplotlib_chinese
setup_matplotlib_chinese()  # 必须重新设置
```

#### 2. Jupyter Notebook新内核
```python
# 重启内核后，需要重新运行
from font_manager import setup_matplotlib_chinese
setup_matplotlib_chinese()
```

#### 3. 其他代码覆盖了字体设置
```python
from font_manager import setup_matplotlib_chinese
import matplotlib.pyplot as plt

setup_matplotlib_chinese()  # 设置成功

# 其他代码可能会覆盖设置
plt.rcParams['font.family'] = 'DejaVu Sans'  # 覆盖了中文字体

# 需要重新调用
setup_matplotlib_chinese()  # 重新设置
```

## 📚 **不同库的支持情况**

### ✅ 完全支持的库

#### matplotlib
```python
from font_manager import setup_matplotlib_chinese
import matplotlib.pyplot as plt

setup_matplotlib_chinese()

plt.figure()
plt.title('中文标题')  # ✅ 正常显示
plt.xlabel('横轴标签')  # ✅ 正常显示
plt.ylabel('纵轴标签')  # ✅ 正常显示
plt.show()
```

#### seaborn
```python
from font_manager import setup_matplotlib_chinese
import seaborn as sns

setup_matplotlib_chinese()

sns.barplot(data=df, x='category', y='value')
plt.title('中文标题')  # ✅ 正常显示
plt.show()
```

#### pandas.plot()
```python
from font_manager import setup_matplotlib_chinese
import pandas as pd

setup_matplotlib_chinese()

df.plot(title='中文标题')  # ✅ 正常显示
plt.show()
```

### ⚠️ 需要特殊处理的库

#### WordCloud
```python
from font_manager import FontManager
from wordcloud import WordCloud

# 获取字体路径
fm = FontManager()
result = fm.setup_matplotlib_chinese()

if result.success:
    font_path = result.font_used.path
    
    # WordCloud需要显式指定字体路径
    wordcloud = WordCloud(
        font_path=font_path,  # 必须指定
        width=800,
        height=400,
        background_color='white'
    ).generate('中文词云测试')
    
    plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
```

### ❌ 不支持的库

#### Plotly
```python
# FontManager不影响Plotly
import plotly.graph_objects as go

# Plotly有自己的字体设置方法
fig = go.Figure()
fig.update_layout(
    font=dict(family="Arial Unicode MS, sans-serif")  # Plotly自己的设置
)
```

#### PIL/Pillow
```python
# FontManager不影响PIL
from PIL import Image, ImageDraw, ImageFont

# PIL需要自己指定字体文件
font = ImageFont.truetype('/System/Library/Fonts/Hiragino Sans GB.ttc', 20)
```

## 🌍 **跨平台使用**

### macOS
```python
from font_manager import setup_matplotlib_chinese

setup_matplotlib_chinese()
# 自动选择: Hiragino Sans GB (冬青黑体)
```

### Windows
```python
from font_manager import setup_matplotlib_chinese

setup_matplotlib_chinese()
# 自动选择: Microsoft YaHei 或 SimHei
```

### Linux
```bash
# 1. 先安装中文字体
sudo apt-get install fonts-noto-cjk  # Ubuntu/Debian
# 或
sudo yum install google-noto-cjk-fonts  # CentOS/RHEL

# 2. 然后使用
python -c "from font_manager import setup_matplotlib_chinese; setup_matplotlib_chinese()"
```

## 💡 **最佳实践**

### 1. 项目入口设置
```python
# main.py 或 __init__.py
from font_manager import setup_matplotlib_chinese

# 在项目启动时调用一次
setup_matplotlib_chinese()

# 后续所有模块都能正常显示中文
```

### 2. Jupyter Notebook
```python
# 第一个cell
from font_manager import setup_matplotlib_chinese
setup_matplotlib_chinese()

print("✅ 中文字体设置完成，后续所有图表都能正常显示中文")
```

### 3. 长期运行的服务
```python
# server.py
import logging
from font_manager import setup_matplotlib_chinese

def initialize_app():
    # 服务启动时设置一次
    result = setup_matplotlib_chinese()
    if result.success:
        logging.info(f"字体设置成功: {result.font_used.name}")
    else:
        logging.warning("字体设置失败，图表可能无法正常显示中文")

if __name__ == "__main__":
    initialize_app()
    # 启动服务...
```

### 4. 测试和CI环境
```python
# test_setup.py
import pytest
from font_manager import setup_matplotlib_chinese

@pytest.fixture(scope="session", autouse=True)
def setup_chinese_font():
    """测试会话开始时自动设置中文字体"""
    setup_matplotlib_chinese()
```

## 🔧 **故障排除**

### 问题1: 设置后仍然显示方框
```python
from font_manager import setup_matplotlib_chinese
import matplotlib.pyplot as plt

# 检查设置结果
result = setup_matplotlib_chinese()
print(f"设置状态: {result.success}")
print(f"使用字体: {result.font_used.name if result.success else '失败'}")

# 检查当前matplotlib设置
print(f"当前字体设置: {plt.rcParams['font.sans-serif']}")
```

### 问题2: 在某些环境下无法找到中文字体
```python
from font_manager import FontManager

fm = FontManager()
fonts = fm.get_available_fonts()

# 查看所有可用字体
chinese_fonts = [f for f in fonts if f.supports_chinese]
print(f"找到 {len(chinese_fonts)} 个中文字体:")
for font in chinese_fonts[:5]:  # 显示前5个
    print(f"  - {font.name}: {font.path}")
```

### 问题3: 性能问题
```python
from font_manager import setup_matplotlib_chinese

# 第一次调用会检测字体，可能较慢
result = setup_matplotlib_chinese()
print(f"设置耗时: {result.setup_time:.3f}秒")

# 后续调用会使用缓存，很快
result2 = setup_matplotlib_chinese()
print(f"缓存调用耗时: {result2.setup_time:.3f}秒")
```

## 📊 **性能优化建议**

1. **避免重复调用**: 在同一进程中只需调用一次
2. **使用缓存**: FontManager会自动缓存字体检测结果
3. **预热字体**: 在应用启动时调用一次，避免首次使用时的延迟

## 🎯 **总结**

FontManager 提供了一个简单而强大的解决方案来处理 Python 数据可视化中的中文字体问题。记住以下要点：

- ✅ **一次设置，进程内永久生效**
- ⚠️ **新进程需要重新调用**
- 🎯 **主要支持 matplotlib 生态系统**
- 💡 **在项目入口处调用一次是最佳实践**

通过正确使用 FontManager，你可以彻底告别中文显示为方框的问题！🎉