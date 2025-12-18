#!/usr/bin/env python3
"""
AI PPT 导演系统 - 时间轴生成工具
用于快速生成符合视觉规范的水平时间轴

使用示例：
python generate_timeline.py --data "Q1:启动阶段:完成市场调研,Q2:快速增长:用户破10万,Q3:稳步推进:优化产品体验,Q4:总结展望:全年目标达成" --color gold_blue
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import argparse
from pathlib import Path


# 配色方案定义
COLOR_SCHEMES = {
    "blue": {
        "name": "科技蓝",
        "colors": ["#4A90E2", "#5B7FCE", "#6D6FBB", "#7E5FA8"],
        "text": "#2C3E50",
        "text_light": "#7F8C8D"
    },
    "gold_blue": {
        "name": "高端金蓝",
        "colors": ["#2C5282", "#D4AF37", "#3A6FA5", "#8B4513"],
        "text": "#2D3436",
        "text_light": "#636E72"
    },
    "multilayer": {
        "name": "多层次专业",
        "colors": ["#2C5282", "#FF9500", "#D4AF37", "#5A8FC4"],
        "text": "#2D3436",
        "text_light": "#636E72"
    },
    "orange": {
        "name": "商务橙",
        "colors": ["#FF9500", "#FFA733", "#FFB966", "#FFCB99"],
        "text": "#34495E",
        "text_light": "#95A5A6"
    },
    "green": {
        "name": "专业绿",
        "colors": ["#00D084", "#33D99A", "#66E2B0", "#99EBC6"],
        "text": "#2D3436",
        "text_light": "#636E72"
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


def parse_timeline_data(data_str):
    """
    解析时间轴数据
    格式: "时间1:标题1:描述1,时间2:标题2:描述2,..."
    """
    items = data_str.split(',')
    timeline = []
    for item in items:
        parts = item.split(':')
        if len(parts) >= 3:
            time_label = parts[0].strip()
            title = parts[1].strip()
            description = parts[2].strip()
            timeline.append({
                'time': time_label,
                'title': title,
                'description': description
            })
    return timeline


def generate_horizontal_timeline(timeline, scheme, title="时间轴", output="timeline.png"):
    """生成水平时间轴（带底部数据卡片）"""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # 标题
    ax.text(5, 9.2, title, ha='center', va='top',
            fontsize=26, fontweight='bold', color=scheme['text'])

    # 时间轴主线
    line_y = 6.5
    ax.plot([1, 9], [line_y, line_y], color='#E0E0E0', linewidth=3, zorder=1)

    # 计算每个时间节点的位置
    n = len(timeline)
    x_positions = np.linspace(1.5, 8.5, n)

    # 绘制时间节点和连接线
    colors = scheme['colors'][:n]
    for i, (x, item, color) in enumerate(zip(x_positions, timeline, colors)):
        # 时间节点圆圈
        circle = plt.Circle((x, line_y), 0.2, color=color, zorder=3)
        ax.add_patch(circle)

        # 内圈白色
        inner_circle = plt.Circle((x, line_y), 0.12, color='white', zorder=4)
        ax.add_patch(inner_circle)

        # 时间标签（上方）
        ax.text(x, line_y + 0.5, item['time'],
                ha='center', va='bottom',
                fontsize=16, fontweight='bold', color=color)

        # 阶段标题（下方）
        ax.text(x, line_y - 0.5, item['title'],
                ha='center', va='top',
                fontsize=14, fontweight='bold', color=scheme['text'])

    # 底部数据卡片区域
    card_y_start = 4.0
    card_width = (8.5 - 1.5) / n - 0.2
    card_height = 2.5

    for i, (x, item, color) in enumerate(zip(x_positions, timeline, colors)):
        # 卡片背景
        card = FancyBboxPatch(
            (x - card_width/2, card_y_start - card_height),
            card_width, card_height,
            boxstyle="round,pad=0.1",
            facecolor=color,
            edgecolor='none',
            alpha=0.9,
            zorder=2
        )
        ax.add_patch(card)

        # 卡片内容（描述文字）
        ax.text(x, card_y_start - card_height/2, item['description'],
                ha='center', va='center',
                fontsize=11, color='white',
                fontweight='bold',
                wrap=True)

    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ 时间轴已保存: {output}")
    plt.close()


def main():
    parser = argparse.ArgumentParser(
        description="AI PPT导演系统 - 时间轴生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python generate_timeline.py --data "Q1:启动阶段:完成市场调研,Q2:快速增长:用户破10万,Q3:稳步推进:优化产品体验,Q4:总结展望:全年目标达成" --color gold_blue
  python generate_timeline.py --data "1月:需求分析:收集用户反馈,3月:设计开发:完成核心功能,6月:测试上线:Beta版发布,9月:正式运营:用户破万" --color blue --title "项目进度时间轴"
        """
    )

    parser.add_argument('--data', '-d',
                        required=True,
                        help='时间轴数据，格式: "时间1:标题1:描述1,时间2:标题2:描述2,..."')

    parser.add_argument('--color', '-c',
                        choices=['blue', 'orange', 'green', 'gold_blue', 'multilayer'],
                        default='gold_blue',
                        help='配色方案: blue(科技蓝) | orange(商务橙) | green(专业绿) | gold_blue(高端金蓝) | multilayer(多层次专业)')

    parser.add_argument('--title', '-T',
                        default='项目时间轴',
                        help='时间轴标题')

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
    timeline = parse_timeline_data(args.data)
    print(f"✓ 数据解析完成: {len(timeline)}个时间节点")

    # 设置输出文件名
    if args.output:
        output = args.output
    else:
        output = f"timeline_{args.color}.png"

    # 生成时间轴
    generate_horizontal_timeline(timeline, scheme, args.title, output)

    print(f"\n✓ 时间轴生成成功!")
    print(f"  文件位置: {Path(output).absolute()}")
    print(f"  配色方案: {scheme['name']}")
    print(f"  时间节点数: {len(timeline)}")


if __name__ == "__main__":
    main()
