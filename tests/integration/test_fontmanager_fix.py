#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FontManager 修复验证测试脚本

测试本次修复的功能：
1. setup_matplotlib_chinese 方法是否正常工作
2. setup_matplotlib_chinese_robust 健壮版本是否正常工作
3. 字体设置是否生效
4. 图片生成是否无堵塞问题
"""

import sys
import os
import time
import gc
from contextlib import contextmanager

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

def test_basic_import():
    """测试基本导入功能"""
    print("🧪 测试1: 基本导入功能")
    try:
        from font_manager import setup_matplotlib_chinese, setup_matplotlib_chinese_robust
        from font_manager import FontManager
        print("✅ 导入成功")
        return True
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_setup_matplotlib_chinese():
    """测试原版setup_matplotlib_chinese方法"""
    print("\n🧪 测试2: setup_matplotlib_chinese 方法")
    try:
        from font_manager import setup_matplotlib_chinese
        
        start_time = time.time()
        result = setup_matplotlib_chinese()
        end_time = time.time()
        
        print(f"⏱️ 执行时间: {end_time - start_time:.2f}秒")
        print(f"📊 设置结果: {result.success}")
        
        if result.success:
            print(f"✅ 使用字体: {result.font_used.name}")
            if result.fallback_fonts:
                print(f"📋 备用字体: {', '.join(result.fallback_fonts[:3])}")
        else:
            print(f"❌ 设置失败: {result.errors}")
            
        return result.success
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_setup_matplotlib_chinese_robust():
    """测试健壮版setup_matplotlib_chinese_robust方法"""
    print("\n🧪 测试3: setup_matplotlib_chinese_robust 健壮版")
    try:
        from font_manager import setup_matplotlib_chinese_robust
        
        start_time = time.time()
        result = setup_matplotlib_chinese_robust()
        end_time = time.time()
        
        print(f"⏱️ 执行时间: {end_time - start_time:.2f}秒")
        print(f"📊 设置结果: {result.success}")
        
        if result.success:
            print(f"✅ 使用字体: {result.font_used.name}")
            if result.fallback_fonts:
                print(f"📋 备用字体: {', '.join(result.fallback_fonts[:3])}")
        else:
            print(f"❌ 设置失败: {result.errors}")
            
        # 测试第二次调用（应该使用缓存）
        print("🔄 测试缓存机制...")
        start_time2 = time.time()
        result2 = setup_matplotlib_chinese_robust()
        end_time2 = time.time()
        
        print(f"⏱️ 第二次执行时间: {end_time2 - start_time2:.2f}秒")
        print(f"📊 缓存是否生效: {'是' if end_time2 - start_time2 < 0.1 else '否'}")
            
        return result.success
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

@contextmanager
def safe_matplotlib_test():
    """安全的matplotlib测试上下文"""
    fig = None
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        
        fig = plt.figure(figsize=(8, 6))
        yield fig
        
    except Exception as e:
        print(f"⚠️ matplotlib测试异常: {e}")
        raise
    finally:
        if fig:
            plt.close(fig)
            del fig
        gc.collect()

def test_chinese_display():
    """测试中文显示功能"""
    print("\n🧪 测试4: 中文显示功能")
    try:
        # 先设置字体
        from font_manager import setup_matplotlib_chinese_robust
        result = setup_matplotlib_chinese_robust()
        
        if not result.success:
            print("❌ 字体设置失败，跳过显示测试")
            return False
        
        # 测试中文显示
        with safe_matplotlib_test() as fig:
            ax = fig.add_subplot(111)
            
            # 绘制测试图表
            x = [1, 2, 3, 4, 5]
            y = [2, 5, 3, 8, 7]
            
            ax.plot(x, y, marker='o', linewidth=2, markersize=8)
            ax.set_title('FontManager修复测试图表', fontsize=16, fontweight='bold')
            ax.set_xlabel('时间轴', fontsize=12)
            ax.set_ylabel('数值', fontsize=12)
            ax.grid(True, alpha=0.3)
            
            # 添加中文标注
            ax.annotate('测试点', xy=(3, 3), xytext=(3.5, 4),
                       arrowprops=dict(arrowstyle='->', color='red'),
                       fontsize=10, color='red')
            
            # 保存测试图片
            output_path = "fontmanager_fix_test.png"
            fig.savefig(output_path, dpi=150, bbox_inches='tight')
            
            print(f"✅ 中文显示测试成功，图片已保存: {output_path}")
            return True
            
    except Exception as e:
        print(f"❌ 中文显示测试失败: {e}")
        return False

def test_memory_safety():
    """测试内存安全性"""
    print("\n🧪 测试5: 内存安全性（防堵塞）")
    try:
        import psutil
        import os
        
        # 获取当前进程
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        print(f"📊 初始内存使用: {initial_memory:.1f} MB")
        
        # 连续创建多个图形对象测试内存泄漏
        for i in range(5):
            with safe_matplotlib_test() as fig:
                ax = fig.add_subplot(111)
                ax.plot([1, 2, 3], [1, 4, 2])
                ax.set_title(f'测试图表 {i+1}')
                
                # 每次都强制垃圾回收
                gc.collect()
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        print(f"📊 最终内存使用: {final_memory:.1f} MB")
        print(f"📊 内存增长: {memory_increase:.1f} MB")
        
        # 如果内存增长小于10MB，认为是安全的
        if memory_increase < 10:
            print("✅ 内存安全性测试通过")
            return True
        else:
            print("⚠️ 内存增长较大，可能存在内存泄漏")
            return False
            
    except ImportError:
        print("⚠️ psutil未安装，跳过内存测试")
        return True
    except Exception as e:
        print(f"❌ 内存安全性测试失败: {e}")
        return False

def test_font_manager_class():
    """测试FontManager类的直接使用"""
    print("\n🧪 测试6: FontManager类直接使用")
    try:
        from font_manager import FontManager
        
        # 创建FontManager实例
        fm = FontManager()
        
        # 测试setup方法
        result = fm.setup()
        print(f"📊 FontManager.setup() 结果: {result.success}")
        
        if result.success:
            print(f"✅ 当前字体: {fm.current_font.name}")
            print(f"📊 是否已配置: {fm.is_configured}")
        
        # 测试健壮版方法
        result_robust = fm.setup_matplotlib_chinese_robust()
        print(f"📊 健壮版设置结果: {result_robust.success}")
        
        return result.success or result_robust.success
        
    except Exception as e:
        print(f"❌ FontManager类测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 FontManager 修复验证测试")
    print("=" * 50)
    
    tests = [
        ("基本导入", test_basic_import),
        ("原版方法", test_setup_matplotlib_chinese),
        ("健壮版方法", test_setup_matplotlib_chinese_robust),
        ("中文显示", test_chinese_display),
        ("内存安全", test_memory_safety),
        ("类直接使用", test_font_manager_class)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
            results.append((test_name, False))
    
    # 输出测试总结
    print("\n" + "=" * 50)
    print("📊 测试结果总结:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 总体结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！FontManager修复成功！")
        return True
    else:
        print("⚠️ 部分测试失败，需要进一步检查")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ 测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试程序异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)