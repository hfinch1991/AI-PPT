#!/usr/bin/env python3
"""
AI PPT 导演系统 - 大数字卡片生成工具
用于快速生成符合视觉规范的核心指标展示卡片

使用示例：
python generate_big_numbers.py --data "3000万:年度GMV:同比增长150%,10万+:活跃用户:月增长率35%,95%:客户满意度:行业领先水平" --color gold_blue
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np
import argparse
from pathlib import Path


# 配色方案定义
COLOR_SCHEMES = {
    "blue": {
        "name": "科技蓝",
        "primary": "#4A90E2",
        "accent": "#FF6B6B",
        "gradient": ["#4A90E2", "#5B7FCE", "#6D6FBB", "#7E5FA8"],
        "text": "#2C3E50",
        "text_light": "#7F8C8D",
        "background": "#ECF0F1"
    },
    "gold_blue": {
        "name": "高端金蓝",
        "primary": "#2C5282",
        "accent": "#D4AF37",
        "gradient": ["#2C5282", "#D4AF37", "#3A6FA5", "#F4E4C1"],
        "text": "#2D3436",
        "text_light": "#636E72",
        "background": "#F5F6FA"
    },
    "multilayer": {
        "name": "多层次专业",
        "primary": "#2C5282",
        "accent": "#FF9500",
        "gradient": ["#2C5282", "#FF9500", "#D4AF37", "#8B4513"],
        "text": "#2D3436",
        "text_light": "#636E72",
        "background": "#F5F6FA"
    },
    "orange": {
        "name": "商务橙",
        "primary": "#FF9500",
        "accent": "#4ECDC4",
        "gradient": ["#FF9500", "#FFA733", "#FFB966", "#FFCB99"],
        "text": "#34495E",
        "text_light": "#95A5A6",
        "background": "#F7F9FA"
    },
    "green": {
        "name": "专业绿",
        "primary": "#00D084",
        "accent": "#FDCB6E",
        "gradient": ["#00D084", "#33D99A", "#66E2B0", "#99EBC6"],
        "text": "#2D3436",
        "text_light": "#636E72",
        "background": "#DFE6E9"
    }
}


def setup_font():
    """设置中文字体"""
    font_candidates = ['PingFang HK', 'PingFang SC', 'Microsoft YaHei', 'SimHei', 'Arial Unicode MS']

    for font in font_candidates:
        try:
            plt.rcParams['font.sans-serif'] = [font]
            plt.rcParams['axes.unicode_minus'] = False
            print(f"✓ 使用字体: {font}")
            return
        except:
            continue

    print("⚠ 未找到中文字体，可能显示为方框")


def parse_metrics_data(data_str):
    """
    解析大数字数据
    格式: "数值1:标题1:描述1,数值2:标题2:描述2,..."
    """
    items = data_str.split(',')
    metrics = []
    for item in items:
        parts = item.split(':')
        if len(parts) >= 3:
            number = parts[0].strip()
            title = parts[1].strip()
            description = parts[2].strip()
            metrics.append({
                'number': number,
                'title': title,
                'description': description
            })
    return metrics


def generate_big_number_cards(metrics, scheme, title="核心指标", output="big_numbers.png"):
    """生成大数字卡片展示"""
    n = len(metrics)

    # 根据卡片数量调整布局
    if n <= 2:
        cols = n
        rows = 1
        figsize = (7 * cols, 6)
    elif n <= 4:
        cols = 2
        rows = 2
        figsize = (14, 12)
    else:
        cols = 3
        rows = (n + 2) // 3
        figsize = (18, 6 * rows)

    fig, axes = plt.subplots(rows, cols, figsize=figsize)

    # 标题
    fig.suptitle(title, fontsize=28, fontweight='bold', color=scheme['text'], y=0.98)

    # 扁平化axes数组
    if n == 1:
        axes = [axes]
    elif rows == 1 or cols == 1:
        axes = axes.flatten() if n > 1 else [axes]
    else:
        axes = axes.flatten()

    # 颜色交替（主色和强调色）
    colors = [scheme['primary'], scheme['accent']]

    for i, (ax, metric) in enumerate(zip(axes[:n], metrics)):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')

        # 选择颜色（交替使用）
        color = colors[i % 2]

        # 卡片背景（带圆角）
        card = FancyBboxPatch(
            (0.5, 0.5), 9, 9,
            boxstyle="round,pad=0.3",
            facecolor=color,
            edgecolor='none',
            alpha=0.95
        )
        ax.add_patch(card)

        # 大数字
        ax.text(5, 6.5, metric['number'],
                ha='center', va='center',
                fontsize=48, fontweight='bold', color='white')

        # 标题
        ax.text(5, 4.5, metric['title'],
                ha='center', va='center',
                fontsize=20, fontweight='bold', color='white')

        # 描述/增长率
        ax.text(5, 3.0, metric['description'],
                ha='center', va='center',
                fontsize=16, color='white', alpha=0.9)

        # 装饰性小元素（右上角）
        ax.text(8.5, 8.5, '●',
                ha='center', va='center',
                fontsize=30, color='white', alpha=0.3)

    # 隐藏多余的子图
    for ax in axes[n:]:
        ax.axis('off')

    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ 大数字卡片已保存: {output}")
    plt.close()


def main():
    parser = argparse.ArgumentParser(
        description="AI PPT导演系统 - 大数字卡片生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python generate_big_numbers.py --data "3000万:年度GMV:同比增长150%,10万+:活跃用户:月增长率35%,95%:客户满意度:行业领先水平" --color gold_blue
  python generate_big_numbers.py --data "156%:年度增长率:超额完成目标,42个:合作伙伴:覆盖全国" --color blue --title "年度成果概览"
        """
    )

    parser.add_argument('--data', '-d',
                        required=True,
                        help='大数字数据，格式: "数值1:标题1:描述1,数值2:标题2:描述2,..."')

    parser.add_argument('--color', '-c',
                        choices=['blue', 'orange', 'green', 'gold_blue', 'multilayer'],
                        default='gold_blue',
                        help='配色方案: blue(科技蓝) | orange(商务橙) | green(专业绿) | gold_blue(高端金蓝) | multilayer(多层次专业)')

    parser.add_argument('--title', '-T',
                        default='核心指标',
                        help='页面标题')

    parser.add_argument('--output', '-o',
                        default='',
                        help='输出文件名（默认自动生成）')

    args = parser.parse_args()

    # 设置字体
    setup_font()

    # 获取配色方案
    scheme = COLOR_SCHEMES[args.color]
    print(f"✓ 使用配色方案: {scheme['name']}")

    # 解析数据
    metrics = parse_metrics_data(args.data)
    print(f"✓ 数据解析完成: {len(metrics)}个指标")

    # 设置输出文件名
    if args.output:
        output = args.output
    else:
        output = f"big_numbers_{args.color}.png"

    # 生成大数字卡片
    generate_big_number_cards(metrics, scheme, args.title, output)

    print(f"\n✓ 大数字卡片生成成功!")
    print(f"  文件位置: {Path(output).absolute()}")
    print(f"  配色方案: {scheme['name']}")
    print(f"  指标数量: {len(metrics)}")


if __name__ == "__main__":
    main()
