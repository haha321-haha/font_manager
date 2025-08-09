#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FontManager 健壮版本

解决问题：
1. 每次运行都需要修改的问题
2. 字体缓存冲突
3. 内存泄漏
4. 程序卡死

特点：
- 一次设置，永久生效
- 自动检测和恢复
- 内存安全
- 跨平台兼容
"""

import os
import sys
import gc
import time
import warnings
from contextlib import contextmanager

# 强制设置matplotlib后端，避免GUI问题
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 禁用字体相关警告
warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')

class RobustFontManager:
    """健壮的字体管理器"""
    
    def __init__(self):
        self.is_initialized = False
        self.current_font = None
        self.available_fonts = []
        
    def _detect_system_fonts(self):
        """检测系统可用的中文字体"""
        chinese_fonts = []
        
        # macOS字体
        macos_fonts = [
            'Arial Unicode MS',
            'PingFang SC',
            'Hiragino Sans GB',
            'STHeiti',
            'Heiti SC'
        ]
        
        # Windows字体
        windows_fonts = [
            'Microsoft YaHei',
            'SimHei',
            'SimSun',
            'KaiTi',
            'FangSong'
        ]
        
        # Linux字体
        linux_fonts = [
            'WenQuanYi Micro Hei',
            'WenQuanYi Zen Hei',
            'Noto Sans CJK SC',
            'Source Han Sans SC'
        ]
        
        # 备用字体
        fallback_fonts = [
            'DejaVu Sans',
            'Arial',
            'Liberation Sans'
        ]
        
        # 合并所有字体列表
        all_fonts = macos_fonts + windows_fonts + linux_fonts + fallback_fonts
        
        # 检测可用字体
        for font_name in all_fonts:
            if self._test_font(font_name):
                chinese_fonts.append(font_name)
        
        return chinese_fonts
    
    def _test_font(self, font_name):
        """测试字体是否可用"""
        try:
            # 临时设置字体
            old_fonts = plt.rcParams['font.sans-serif'].copy()
            plt.rcParams['font.sans-serif'] = [font_name]
            
            # 创建测试图形
            fig, ax = plt.subplots(figsize=(1, 1))
            ax.text(0.5, 0.5, '测试中文', fontsize=12)
            
            # 检查是否有字体警告
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                plt.tight_layout()
                
                # 如果没有警告，说明字体可用
                font_available = len(w) == 0
            
            plt.close(fig)
            del fig
            
            # 恢复原字体设置
            plt.rcParams['font.sans-serif'] = old_fonts
            
            return font_available
            
        except Exception:
            return False
        finally:
            gc.collect()
    
    def setup_chinese_font(self, force_refresh=False):
        """设置中文字体"""
        if self.is_initialized and not force_refresh:
            print(f"✅ 字体已初始化: {self.current_font}")
            return True
        
        print("🔍 正在检测系统字体...")
        
        # 清除matplotlib字体缓存
        if force_refresh:
            try:
                fm._rebuild()
                print("🔄 字体缓存已清除")
            except:
                pass
        
        # 检测可用字体
        self.available_fonts = self._detect_system_fonts()
        
        if not self.available_fonts:
            print("⚠️ 未找到合适的中文字体，使用默认字体")
            self.current_font = "default"
            self.is_initialized = True
            return False
        
        # 使用第一个可用字体
        best_font = self.available_fonts[0]
        
        try:
            # 设置matplotlib字体参数
            plt.rcParams.update({
                'font.sans-serif': [best_font] + self.available_fonts[1:],
                'axes.unicode_minus': False,
                'font.family': 'sans-serif',
                'figure.max_open_warning': 0
            })
            
            self.current_font = best_font
            self.is_initialized = True
            
            print(f"✅ 中文字体设置成功: {best_font}")
            print(f"📋 备用字体: {', '.join(self.available_fonts[1:3])}")
            
            return True
            
        except Exception as e:
            print(f"❌ 字体设置失败: {e}")
            return False
    
    def get_status(self):
        """获取字体管理器状态"""
        return {
            'initialized': self.is_initialized,
            'current_font': self.current_font,
            'available_fonts': self.available_fonts,
            'matplotlib_backend': matplotlib.get_backend()
        }
    
    def reset(self):
        """重置字体管理器"""
        self.is_initialized = False
        self.current_font = None
        self.available_fonts = []
        
        # 重置matplotlib参数
        plt.rcdefaults()
        matplotlib.use('Agg')
        
        print("🔄 字体管理器已重置")

# 全局字体管理器实例
_font_manager = RobustFontManager()

def setup_matplotlib_chinese(force_refresh=False):
    """
    设置matplotlib中文显示
    
    Args:
        force_refresh (bool): 是否强制刷新字体缓存
    
    Returns:
        bool: 设置是否成功
    """
    return _font_manager.setup_chinese_font(force_refresh)

def get_font_status():
    """获取字体状态"""
    return _font_manager.get_status()

def reset_font_manager():
    """重置字体管理器"""
    _font_manager.reset()

@contextmanager
def safe_matplotlib_figure(*args, **kwargs):
    """
    安全的matplotlib图形上下文管理器
    
    使用方式:
        with safe_matplotlib_figure(figsize=(12, 8)) as fig:
            ax = fig.add_subplot(111)
            ax.plot([1, 2, 3], [1, 4, 2])
            fig.savefig('output.png')
    """
    fig = None
    try:
        fig = plt.figure(*args, **kwargs)
        yield fig
    except Exception as e:
        print(f"❌ 图形创建失败: {e}")
        raise
    finally:
        if fig is not None:
            plt.close(fig)
            del fig
        gc.collect()

def create_test_chart(output_path="test_chinese_display.png"):
    """创建测试图表验证中文显示"""
    print("🧪 创建测试图表...")
    
    try:
        with safe_matplotlib_figure(figsize=(10, 6)) as fig:
            ax = fig.add_subplot(111)
            
            # 测试数据
            x = [1, 2, 3, 4, 5]
            y = [2, 5, 3, 8, 7]
            
            # 绘制图表
            ax.plot(x, y, marker='o', linewidth=2, markersize=8)
            ax.set_title('中文显示测试图表', fontsize=16, fontweight='bold')
            ax.set_xlabel('时间轴', fontsize=12)
            ax.set_ylabel('数值', fontsize=12)
            ax.grid(True, alpha=0.3)
            
            # 添加中文标注
            ax.annotate('最高点', xy=(4, 8), xytext=(4.5, 8.5),
                       arrowprops=dict(arrowstyle='->', color='red'),
                       fontsize=10, color='red')
            
            plt.tight_layout()
            fig.savefig(output_path, dpi=300, bbox_inches='tight')
            
        print(f"✅ 测试图表已保存: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ 测试图表创建失败: {e}")
        return False

def main():
    """主函数 - 演示使用方法"""
    print("🚀 FontManager 健壮版本演示")
    print("=" * 50)
    
    # 1. 设置中文字体
    print("1️⃣ 设置中文字体...")
    success = setup_matplotlib_chinese()
    
    # 2. 显示状态
    print("\n2️⃣ 字体状态:")
    status = get_font_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    # 3. 创建测试图表
    print("\n3️⃣ 创建测试图表...")
    create_test_chart()
    
    # 4. 演示多次使用不需要重新设置
    print("\n4️⃣ 再次调用（应该直接使用缓存）...")
    setup_matplotlib_chinese()  # 第二次调用应该很快
    
    print("\n🎉 演示完成！")
    print("\n💡 使用建议:")
    print("   - 程序启动时调用一次 setup_matplotlib_chinese()")
    print("   - 使用 safe_matplotlib_figure() 创建图形")
    print("   - 如果字体有问题，调用 setup_matplotlib_chinese(force_refresh=True)")

if __name__ == "__main__":
    main()