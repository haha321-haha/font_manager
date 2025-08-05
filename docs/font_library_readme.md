# 📊 图表字体管理库

## 🎯 项目简介

这是一个专门用于解决 Python matplotlib 中文字体显示问题的管理库。每次制作图表前，在这里进行字体规范设置，避免出现中文字体显示问题。

## 🚀 快速开始

### 1. 基础测试
```bash
cd "/Users/duting/Downloads/图表字体管理库"
python test_font_manager.py
```

### 2. 查看演示效果
```bash
python demo_font_manager.py
```

### 3. 在项目中使用

#### 方法一：一键设置（推荐）
```python
import sys
sys.path.append('/Users/duting/Downloads/图表字体管理库')

from font_manager import setup_chinese_font

# 一行代码解决字体问题
result = setup_chinese_font()
if result.success:
    print(f"✅ 字体设置成功: {result.font_used.name}")
```

#### 方法二：完整API
```python
import sys
sys.path.append('/Users/duting/Downloads/图表字体管理库')

from font_manager import FontManager

# 创建字体管理器
fm = FontManager()

# 设置字体
result = fm.setup()

# 验证配置
report = fm.validate()
print(f"配置状态: {report.status}")
```

## 📁 目录结构

```
图表字体管理库/
├── README.md                   # 使用指南
├── quick_start.py             # 快速开始脚本
├── test_font_manager.py       # 基础测试
├── demo_font_manager.py       # 演示脚本
├── font_manager/              # 核心库
│   ├── __init__.py           # 主入口
│   ├── core/                 # 核心模块
│   ├── utils/                # 工具模块
│   ├── adapters/             # 平台适配器
│   ├── validators/           # 验证器
│   └── data/                 # 配置数据
├── specs/                     # 项目规范
│   ├── requirements.md       # 需求文档
│   ├── design.md            # 设计文档
│   └── tasks.md             # 实现计划
└── examples/                  # 使用示例
```

## 🎯 使用场景

### 场景1：新项目开始前
```python
# 在项目开始前运行一次
from font_manager import setup_chinese_font
setup_chinese_font()

# 然后正常使用matplotlib
import matplotlib.pyplot as plt
plt.title('中文标题')  # 中文正常显示
```

### 场景2：现有项目修复
```python
# 在现有项目的matplotlib导入后添加
import matplotlib.pyplot as plt

# 添加这两行
import sys
sys.path.append('/Users/duting/Downloads/图表字体管理库')
from font_manager import setup_chinese_font
setup_chinese_font()

# 原有代码无需修改
plt.title('中文标题')  # 中文正常显示
```

### 场景3：批量图表生成
```python
# 在批量生成图表的脚本开头
from font_manager import FontManager

fm = FontManager()
result = fm.setup()

if result.success:
    print(f"字体配置完成: {result.font_used.name}")
    # 继续生成图表...
```

## 🔧 高级功能

### 验证字体配置
```python
from font_manager import validate_font_config

report = validate_font_config()
print(f"配置状态: {report.status}")
print(f"综合评分: {report.overall_score}")
```

### 获取可用字体
```python
from font_manager import get_available_fonts

fonts = get_available_fonts()
for font in fonts:
    print(f"{font.name} - 中文支持: {'✅' if font.supports_chinese else '❌'}")
```

## 📞 问题排查

### 常见问题

1. **导入失败**
   - 确保路径正确：`/Users/duting/Downloads/图表字体管理库`
   - 检查目录是否存在

2. **字体设置失败**
   - 运行 `python test_font_manager.py` 检查基础功能
   - 查看日志输出获取详细信息

3. **中文仍显示异常**
   - 运行 `python demo_font_manager.py` 查看对比效果
   - 使用 `validate_font_config()` 检查配置状态

### 获取帮助
- 查看 `font_manager_project_summary.md` 了解详细信息
- 运行测试脚本验证功能
- 查看生成的演示图表对比效果

---

**🎉 让中文图表显示完美！**