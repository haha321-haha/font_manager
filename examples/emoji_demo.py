#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

from font_manager import setup_matplotlib_chinese


def _font_name(item) -> str:
    try:
        return getattr(item, "name", str(item))
    except Exception:
        return str(item)


def main() -> None:
    output_dir = os.path.join(os.path.dirname(__file__), "_out")
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "emoji_demo.png")

    # 一行初始化：中文 + emoji 后备（可根据需要关闭/切换偏好）
    result = setup_matplotlib_chinese(emoji_fallback=True, emoji_prefer_color=True)
    print("setup success:", getattr(result, "success", None))
    print("chinese font:", getattr(getattr(result, "font_used", None), "name", None))
    emoji_fonts = list(getattr(result, "emoji_fonts", []) or [])
    if emoji_fonts:
        print("emoji fallback fonts:", ", ".join([_font_name(f) for f in emoji_fonts]))

    plt.figure(figsize=(8, 5))
    plt.title("中文 + Emoji 演示 🌟", fontsize=18, pad=12)
    plt.text(0.5, 0.65, "中文标题不应为方框", ha="center", va="center", fontsize=16)
    plt.text(0.5, 0.45, "Emoji 示例：🎉🎊🔥✨🚀", ha="center", va="center", fontsize=16)
    first_emoji_font = _font_name(emoji_fonts[0]) if emoji_fonts else "未检测到"
    plt.text(0.5, 0.25, f"Emoji字体：{first_emoji_font}", ha="center", va="center", fontsize=12)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    print("Saved:", out_path)


if __name__ == "__main__":
    main()
