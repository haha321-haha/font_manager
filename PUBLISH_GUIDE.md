# 📦 PyPI发布指南

## 🎯 发布前检查清单

### ✅ 必需文件检查
- [x] `setup.py` - Python包配置
- [x] `pyproject.toml` - 现代包配置
- [x] `requirements.txt` - 依赖列表
- [x] `README.md` - 项目说明
- [x] `LICENSE` - MIT许可证
- [x] `MANIFEST.in` - 包含文件清单
- [x] `CHANGELOG.md` - 更新日志
- [x] `font_manager/` - 核心库代码

### ✅ GitHub配置检查
- [x] GitHub Secrets配置：`PYPI_API_TOKEN`
- [x] GitHub Actions工作流：`.github/workflows/publish.yml`
- [x] 仓库地址正确：`https://github.com/haha321-haha/font_manager`

## 🚀 发布方法

### 方法1：通过GitHub Release发布（推荐）

1. **推送代码到GitHub**：
```bash
cd "/Users/duting/Downloads/命理风水占卜🔮/font_manager/未命名文件夹"
git add .
git commit -m "🎉 Ready for PyPI release v1.0.0"
git push origin main
```

2. **创建GitHub Release**：
   - 访问：https://github.com/haha321-haha/font_manager/releases
   - 点击 "Create a new release"
   - Tag version: `v1.0.0`
   - Release title: `🎉 Font Manager v1.0.0 - 智能字体管理库首次发布`
   - 描述：复制CHANGELOG.md的内容
   - 点击 "Publish release"

3. **自动发布**：
   - GitHub Actions会自动触发
   - 自动构建包并发布到PyPI
   - 查看Actions页面确认发布状态

### 方法2：通过Git标签发布

```bash
# 创建并推送标签
git tag v1.0.0
git push origin v1.0.0
```

### 方法3：本地手动发布（备用）

```bash
# 安装构建工具
pip install build twine

# 构建包
python -m build

# 检查包
twine check dist/*

# 发布到PyPI
twine upload dist/* --username __token__ --password pypi-AgEIcHlwaS5vcmcCJGUwMWRmMTQzLTQ4NWMtNDU0ZC05NThmLTYxZDQ3ZDAzOThkZAACKlszLCJkYTNjNDQ1Mi03NTI4LTRmZDAtODdjYS1lMTRkZTljYjU0MmQiXQAABiCrpaNviLMewd01EnxkhoJn01atxaTaoTEyTHYYZDKV9Q
```

## 📊 发布后验证

### 1. 检查PyPI页面
访问：https://pypi.org/project/matplotlib-font-manager-yanlin/

### 2. 测试安装
```bash
# 在新环境中测试
pip install matplotlib-font-manager-yanlin

# 测试导入
python -c "from font_manager import setup_chinese_font; setup_chinese_font(); print('✅ 安装成功！')"
```

### 3. 更新README.md
发布成功后，更新README.md中的安装命令：
```bash
pip install matplotlib-font-manager-yanlin
```

## 🔧 常见问题解决

### 问题1：包名已存在
- 解决：修改setup.py中的name，添加后缀如`-yanlin`

### 问题2：CSRF令牌错误
- 检查PyPI API token是否正确
- 确认GitHub Secrets配置无误
- 重新生成PyPI token

### 问题3：构建失败
- 检查setup.py语法
- 确认所有依赖都在requirements.txt中
- 查看GitHub Actions日志

### 问题4：文件缺失
- 检查MANIFEST.in配置
- 确认font_manager目录结构正确
- 验证所有必需文件存在

## 🎉 发布成功后

1. **更新推文**：修改安装命令为实际的PyPI包名
2. **社区推广**：在Python社区分享项目
3. **持续维护**：响应用户反馈，修复bug
4. **版本更新**：后续版本发布流程

---

**🚀 准备发布吧！这个Font Manager项目一定会大受欢迎！**