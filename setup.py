#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme():
    if os.path.exists("README.md"):
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    return "Font Manager - 智能字体管理库"

# 读取requirements
def read_requirements():
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    return ["matplotlib>=3.5.0", "numpy>=1.20.0", "PyYAML>=6.0", "psutil>=5.8.0"]

setup(
    name="matplotlib-font-manager",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="一键解决matplotlib中文字体显示问题的智能字体管理库",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/matplotlib-font-manager",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    include_package_data=True,
    package_data={
        "font_manager": ["data/*.json"],
    },
    keywords="matplotlib, font, chinese, visualization, 中文字体, 数据可视化",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/matplotlib-font-manager/issues",
        "Source": "https://github.com/yourusername/matplotlib-font-manager",
        "Documentation": "https://github.com/yourusername/matplotlib-font-manager#readme",
    },
)