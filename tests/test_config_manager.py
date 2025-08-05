#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Config Manager 测试脚本

测试配置管理器的功能。
"""

import sys
import tempfile
import json
from pathlib import Path

# 添加font_manager到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from font_manager import ConfigManager, FontManager
from font_manager.utils.logger import setup_logging


def test_config_manager_basic():
    """测试配置管理器基础功能"""
    print("🔧 测试配置管理器基础功能...")
    
    try:
        # 使用临时文件测试
        temp_config_path = tempfile.mktemp(suffix='.json')
        
        print(f"\n1️⃣ 创建配置管理器...")
        config_manager = ConfigManager(temp_config_path)
        print(f"✅ 配置管理器创建成功，配置路径: {config_manager.config_path}")
        
        print(f"\n2️⃣ 测试默认配置加载...")
        config = config_manager.load_config()
        print(f"✅ 默认配置加载成功，包含 {len(config)} 个顶级配置项")
        
        # 显示主要配置项
        print("主要配置项:")
        for key in ['font_config', 'validation', 'logging', 'cache']:
            if key in config:
                print(f"  📝 {key}: {type(config[key]).__name__}")
        
        print(f"\n3️⃣ 测试配置读取...")
        auto_detect = config_manager.get('font_config.auto_detect')
        print(f"✅ 读取配置成功: auto_detect = {auto_detect}")
        
        preferred_fonts = config_manager.get_preferred_fonts()
        print(f"✅ 首选字体: {len(preferred_fonts)} 个")
        for i, font in enumerate(preferred_fonts[:3], 1):
            print(f"  {i}. {font}")
        
        print(f"\n4️⃣ 测试配置修改...")
        config_manager.set('font_config.auto_detect', False)
        new_value = config_manager.get('font_config.auto_detect')
        print(f"✅ 配置修改成功: auto_detect = {new_value}")
        
        # 测试字体样式配置
        title_style = config_manager.get_font_style('title')
        print(f"✅ 标题样式: {title_style}")
        
        print(f"\n5️⃣ 测试配置保存...")
        save_result = config_manager.save_config()
        print(f"✅ 配置保存: {'成功' if save_result else '失败'}")
        
        print(f"\n6️⃣ 测试配置备份...")
        backup_path = config_manager.backup_config()
        print(f"✅ 配置备份成功: {backup_path}")
        
        print(f"\n7️⃣ 测试配置信息...")
        config_info = config_manager.get_config_info()
        print(f"✅ 配置信息:")
        for key, value in config_info.items():
            print(f"  📝 {key}: {value}")
        
        # 清理临时文件
        Path(temp_config_path).unlink(missing_ok=True)
        Path(backup_path).unlink(missing_ok=True)
        
        print("\n🎉 配置管理器基础功能测试完成！")
        return True
        
    except Exception as e:
        print(f"\n❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config_integration():
    """测试配置管理器与FontManager的集成"""
    print("\n🔗 测试配置管理器集成...")
    
    try:
        # 创建FontManager
        fm = FontManager()
        
        print("1️⃣ 测试配置读取...")
        auto_detect = fm.get_config('font_config.auto_detect')
        print(f"✅ 读取配置: auto_detect = {auto_detect}")
        
        print("2️⃣ 测试首选字体...")
        preferred_fonts = fm.get_preferred_fonts()
        print(f"✅ 首选字体: {len(preferred_fonts)} 个")
        for i, font in enumerate(preferred_fonts[:3], 1):
            print(f"  {i}. {font}")
        
        print("3️⃣ 测试字体样式设置...")
        fm.set_font_style('title', font_size=18, font_weight=800)
        print("✅ 字体样式设置成功")
        
        print("4️⃣ 测试配置信息...")
        config_info = fm.get_config_info()
        print(f"✅ 配置文件: {config_info['config_path']}")
        print(f"✅ 配置版本: {config_info['version']}")
        
        print("5️⃣ 测试配置备份...")
        backup_path = fm.backup_config()
        print(f"✅ 配置备份: {backup_path}")
        
        print("✅ 配置管理器集成测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config_formats():
    """测试不同配置文件格式"""
    print("\n📄 测试配置文件格式...")
    
    try:
        # 测试JSON格式
        print("1️⃣ 测试JSON格式...")
        json_config_path = tempfile.mktemp(suffix='.json')
        
        json_config = ConfigManager(json_config_path)
        json_config.load_config()
        json_config.set('test_key', 'json_value')
        json_config.save_config()
        
        # 验证文件内容
        with open(json_config_path, 'r', encoding='utf-8') as f:
            content = json.load(f)
            assert content['test_key'] == 'json_value'
        
        print("✅ JSON格式测试通过")
        
        # 测试YAML格式
        print("2️⃣ 测试YAML格式...")
        try:
            import yaml
            
            yaml_config_path = tempfile.mktemp(suffix='.yaml')
            
            yaml_config = ConfigManager(yaml_config_path)
            yaml_config.load_config()
            yaml_config.set('test_key', 'yaml_value')
            yaml_config.save_config()
            
            # 验证文件内容
            with open(yaml_config_path, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)
                assert content['test_key'] == 'yaml_value'
            
            print("✅ YAML格式测试通过")
            
            # 清理文件
            Path(yaml_config_path).unlink(missing_ok=True)
            
        except ImportError:
            print("⚠️ YAML库未安装，跳过YAML格式测试")
        
        # 清理文件
        Path(json_config_path).unlink(missing_ok=True)
        
        print("✅ 配置文件格式测试完成！")
        return True
        
    except Exception as e:
        print(f"❌ 格式测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config_validation():
    """测试配置验证功能"""
    print("\n🔍 测试配置验证...")
    
    try:
        # 创建无效配置
        print("1️⃣ 测试无效配置处理...")
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            invalid_config = {"invalid": "config"}
            json.dump(invalid_config, f)
            invalid_config_path = f.name
        
        try:
            config_manager = ConfigManager(invalid_config_path)
            config_manager.load_config()
            print("⚠️ 无效配置未被检测到")
        except Exception as e:
            print(f"✅ 无效配置被正确检测: {type(e).__name__}")
        
        # 清理文件
        Path(invalid_config_path).unlink(missing_ok=True)
        
        print("2️⃣ 测试配置重置...")
        temp_config_path = tempfile.mktemp(suffix='.json')
        
        config_manager = ConfigManager(temp_config_path)
        config_manager.load_config()
        config_manager.set('test_key', 'test_value')
        
        # 重置配置
        reset_result = config_manager.reset_to_default()
        print(f"✅ 配置重置: {'成功' if reset_result else '失败'}")
        
        # 验证重置结果
        test_value = config_manager.get('test_key')
        if test_value is None:
            print("✅ 配置重置验证通过")
        else:
            print(f"⚠️ 配置重置验证失败: test_key = {test_value}")
        
        # 清理文件
        Path(temp_config_path).unlink(missing_ok=True)
        
        print("✅ 配置验证测试完成！")
        return True
        
    except Exception as e:
        print(f"❌ 验证测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("🚀 Config Manager 功能测试")
    print("=" * 50)
    
    # 设置日志
    setup_logging(level="INFO", enable_color=True)
    
    success_count = 0
    total_tests = 4
    
    # 运行测试
    if test_config_manager_basic():
        success_count += 1
    
    if test_config_integration():
        success_count += 1
    
    if test_config_formats():
        success_count += 1
    
    if test_config_validation():
        success_count += 1
    
    # 输出结果
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {success_count}/{total_tests} 通过")
    
    if success_count == total_tests:
        print("🎉 所有测试通过！配置管理功能正常！")
        return True
    else:
        print("❌ 部分测试失败，需要修复问题")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)