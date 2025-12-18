#!/usr/bin/env python3
"""
AI PPT 导演系统 - 图表生成工具
用于快速生成符合视觉规范的高端图表

使用示例：
python generate_chart.py --type bar --data "Q1:85,Q2:92,Q3:88,Q4:95" --color blue
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import json
import argparse
from pathlib import Path


# 配色方案定义（来自 03_视觉规范/配色方案.json）
COLOR_SCHEMES = {
    "blue": {
        "name": "科技蓝",
        "gradient": ["#4A90E2", "#5B7FCE", "#6D6FBB", "#7E5FA8"],
        "primary": "#4A90E2",
        "accent": "#FF6B6B",
        "text": "#2C3E50",
        "text_light": "#7F8C8D",
        "background": "#ECF0F1"
    },
    "orange": {
        "name": "商务橙",
        "gradient": ["#FF9500", "#FFA733", "#FFB966", "#FFCB99"],
        "primary": "#FF9500",
        "accent": "#4ECDC4",
        "text": "#34495E",
        "text_light": "#95A5A6",
        "background": "#F7F9FA"
    },
    "green": {
        "name": "专业绿",
        "gradient": ["#00D084", "#33D99A", "#66E2B0", "#99EBC6"],
        "primary": "#00D084",
        "accent": "#FDCB6E",
        "text": "#2D3436",
        "text_light": "#636E72",
        "background": "#DFE6E9"
    },
    "gold_blue": {
        "name": "高端金蓝",
        "gradient": ["#1E3A5F", "#2C5282", "#3A6FA5"],
        "primary": "#2C5282",
        "accent": "#D4AF37",
        "accent2": "#F4E4C1",
        "text": "#2D3436",
        "text_light": "#636E72",
        "background": "#F5F6FA"
    },
    "multilayer": {
        "name": "多层次专业",
        "gradient": ["#2C5282", "#3A6FA5", "#5A8FC4"],
        "primary": "#2C5282",
        "accent": "#FF9500",
        "accent2": "#D4AF37",
        "accent3": "#8B4513",
        "text": "#2D3436",
        "text_light": "#636E72",
        "background": "#F5F6FA"
    }
}


def setup_font():
    """设置中文字体"""
    # 尝试多个常用中文字体
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


def beautify_axes(ax, scheme):
    """美化坐标轴"""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#E0E0E0')
    ax.spines['bottom'].set_color('#E0E0E0')
    ax.tick_params(colors=scheme['text_light'], which='both')
    ax.grid(axis='y', color='#F0F0F0', linestyle='-', linewidth=0.5, alpha=0.7)


def parse_data(data_str):
    """
    解析数据字符串
    格式1: "Q1:85,Q2:92,Q3:88,Q4:95"  (类别:数值)
    格式2: "85,92,88,95"  (仅数值)
    """
    if ':' in data_str:
        # 格式1
        items = data_str.split(',')
        categories = []
        values = []
        for item in items:
            cat, val = item.split(':')
            categories.append(cat.strip())
            values.append(float(val.strip()))
        return categories, values
    else:
        # 格式2
        values = [float(x.strip()) for x in data_str.split(',')]
        categories = [f'项目{i+1}' for i in range(len(values))]
        return categories, values


def generate_bar_chart(categories, values, scheme, title="柱状图", output="chart_bar.png"):
    """生成柱状图"""
    fig, ax = plt.subplots(figsize=(10, 6))

    # 使用渐变色
    colors = scheme['gradient'][:len(categories)]
    bars = ax.bar(categories, values, color=colors, width=0.6)

    # 添加数据标签
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.0f}',
                ha='center', va='bottom',
                fontsize=20, fontweight='bold', color=scheme['text'])

    # 美化
    ax.set_ylim(0, max(values) * 1.15)
    beautify_axes(ax, scheme)
    ax.set_title(title, fontsize=24, fontweight='bold', color=scheme['text'], pad=20)

    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ 柱状图已保存: {output}")
    plt.close()


def generate_line_chart(categories, values, scheme, title="折线图", output="chart_line.png"):
    """生成折线图（带渐变填充）"""
    fig, ax = plt.subplots(figsize=(10, 6))

    # 绘制折线
    x = np.arange(len(categories))
    line = ax.plot(x, values, color=scheme['primary'], linewidth=3, marker='o',
                    markersize=10, markerfacecolor=scheme['primary'],
                    markeredgecolor='white', markeredgewidth=2)

    # 渐变填充
    ax.fill_between(x, values, alpha=0.3, color=scheme['primary'])

    # 添加数据标签
    for i, v in enumerate(values):
        ax.text(i, v + max(values)*0.03, f'{v:.0f}',
                ha='center', va='bottom',
                fontsize=18, fontweight='bold', color=scheme['text'])

    # 美化
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylim(0, max(values) * 1.15)
    beautify_axes(ax, scheme)
    ax.set_title(title, fontsize=24, fontweight='bold', color=scheme['text'], pad=20)

    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ 折线图已保存: {output}")
    plt.close()


def generate_pie_chart(categories, values, scheme, title="饼图", output="chart_pie.png"):
    """生成环形图"""
    fig, ax = plt.subplots(figsize=(10, 6))

    # 使用渐变色
    colors = scheme['gradient'][:len(categories)]

    # 突出显示最大值
    explode = [0.05 if v == max(values) else 0 for v in values]

    # 绘制饼图
    wedges, texts, autotexts = ax.pie(values, labels=categories, colors=colors,
                                        autopct='%1.1f%%', startangle=90,
                                        explode=explode, pctdistance=0.85,
                                        textprops={'fontsize': 16, 'color': scheme['text']})

    # 设置百分比文字样式
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(18)
        autotext.set_fontweight('bold')

    # 创建环形（中心空白）
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)

    ax.set_title(title, fontsize=24, fontweight='bold', color=scheme['text'], pad=20)

    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ 环形图已保存: {output}")
    plt.close()


def generate_donut_chart(categories, values, scheme, title="环形图", output="chart_donut.png"):
    """生成环形图（带中心数据）"""
    fig, ax = plt.subplots(figsize=(10, 8))

    # 使用渐变色
    colors = scheme['gradient'][:len(categories)]

    # 突出显示最大值
    explode = [0.05 if v == max(values) else 0 for v in values]

    # 绘制环形图
    wedges, texts, autotexts = ax.pie(values, labels=categories, colors=colors,
                                        autopct='%1.1f%%', startangle=90,
                                        explode=explode, pctdistance=0.85,
                                        textprops={'fontsize': 14, 'color': scheme['text']})

    # 设置百分比文字样式
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(16)
        autotext.set_fontweight('bold')

    # 创建环形（中心空白）
    centre_circle = plt.Circle((0, 0), 0.65, fc='white')
    fig.gca().add_artist(centre_circle)

    # 在中心添加总计
    total = sum(values)
    ax.text(0, 0, f'{total:.0f}', ha='center', va='center',
            fontsize=36, fontweight='bold', color=scheme['text'])
    ax.text(0, -0.15, '总计', ha='center', va='center',
            fontsize=16, color=scheme['text_light'])

    ax.set_title(title, fontsize=24, fontweight='bold', color=scheme['text'], pad=20)

    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ 环形图已保存: {output}")
    plt.close()


def generate_radar_chart(categories, values, scheme, title="雷达图", output="chart_radar.png"):
    """生成雷达图（能力评估）"""
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

    # 计算角度
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    values_plot = values + [values[0]]  # 闭合图形
    angles += angles[:1]

    # 绘制雷达图
    ax.plot(angles, values_plot, 'o-', linewidth=2, color=scheme['primary'], label='当前水平')
    ax.fill(angles, values_plot, alpha=0.25, color=scheme['primary'])

    # 设置刻度标签
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=14, color=scheme['text'])

    # 设置Y轴
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=10, color=scheme['text_light'])
    ax.grid(color='#E0E0E0', linestyle='-', linewidth=0.5)

    # 添加数据标签
    for angle, value, category in zip(angles[:-1], values, categories):
        ax.text(angle, value + 5, f'{value:.0f}',
                ha='center', va='center',
                fontsize=12, fontweight='bold', color=scheme['accent'])

    ax.set_title(title, fontsize=24, fontweight='bold', color=scheme['text'], pad=30)

    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ 雷达图已保存: {output}")
    plt.close()


def generate_waterfall_chart(categories, values, scheme, title="瀑布图", output="chart_waterfall.png"):
    """生成瀑布图（增长归因分析）"""
    fig, ax = plt.subplots(figsize=(12, 6))

    # 计算累计值
    cumulative = [0]
    for v in values[:-1]:
        cumulative.append(cumulative[-1] + v)

    # 绘制瀑布图
    colors = []
    for i, v in enumerate(values):
        if i == 0 or i == len(values) - 1:
            colors.append(scheme['primary'])  # 起点和终点用主色
        elif v >= 0:
            colors.append(scheme['accent'])  # 正增长用强调色
        else:
            colors.append('#FF6B6B')  # 负增长用红色

    # 绘制柱子
    x = np.arange(len(categories))
    for i, (cat, val, cum) in enumerate(zip(categories, values, cumulative)):
        if i == len(categories) - 1:
            # 最后一列是总计，从0开始
            ax.bar(i, val, bottom=0, color=colors[i], width=0.6)
        else:
            ax.bar(i, val, bottom=cum, color=colors[i], width=0.6)

    # 连接线
    for i in range(len(categories) - 2):
        ax.plot([i + 0.3, i + 0.7], [cumulative[i+1], cumulative[i+1]],
                'k--', linewidth=1, alpha=0.5)

    # 添加数据标签
    for i, (cat, val, cum) in enumerate(zip(categories, values, cumulative)):
        if i == len(categories) - 1:
            y_pos = val / 2
        else:
            y_pos = cum + val / 2

        ax.text(i, y_pos, f'{val:+.0f}' if i > 0 and i < len(categories) - 1 else f'{val:.0f}',
                ha='center', va='center',
                fontsize=16, fontweight='bold', color='white')

    # 美化
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=12)
    beautify_axes(ax, scheme)
    ax.set_title(title, fontsize=24, fontweight='bold', color=scheme['text'], pad=20)

    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ 瀑布图已保存: {output}")
    plt.close()


def generate_comparison_chart(categories, values1, values2, scheme,
                               title="对比图", label1="系列1", label2="系列2",
                               output="chart_comparison.png"):
    """生成分组柱状图"""
    fig, ax = plt.subplots(figsize=(12, 6))

    x = np.arange(len(categories))
    width = 0.35

    # 绘制两组柱子
    bars1 = ax.bar(x - width/2, values1, width, label=label1, color=scheme['primary'])
    bars2 = ax.bar(x + width/2, values2, width, label=label2, color=scheme['accent'])

    # 添加数据标签
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.0f}',
                    ha='center', va='bottom',
                    fontsize=16, fontweight='bold', color=scheme['text'])

    # 美化
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylim(0, max(max(values1), max(values2)) * 1.15)
    beautify_axes(ax, scheme)
    ax.set_title(title, fontsize=24, fontweight='bold', color=scheme['text'], pad=20)
    ax.legend(loc='upper left', fontsize=14, frameon=False)

    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ 对比图已保存: {output}")
    plt.close()


def main():
    parser = argparse.ArgumentParser(
        description="AI PPT导演系统 - 图表生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 基础图表
  python generate_chart.py --type bar --data "Q1:85,Q2:92,Q3:88,Q4:95" --color blue
  python generate_chart.py --type line --data "Q1:100,Q2:120,Q3:115,Q4:150" --title "季度增长趋势"
  python generate_chart.py --type pie --data "产品A:30,产品B:25,产品C:20,产品D:25" --color green

  # 高端图表（v2.0新增）
  python generate_chart.py --type donut --data "产品A:30,产品B:25,产品C:20,产品D:25" --color gold_blue --title "销售占比"
  python generate_chart.py --type radar --data "战略:85,执行:92,创新:78,协作:88,领导力:90" --color multilayer --title "能力评估"
  python generate_chart.py --type waterfall --data "Q1基准:100,产品增长:+35,市场拓展:+28,成本优化:-8,Q4总计:155" --title "增长归因分析"
        """
    )

    parser.add_argument('--type', '-t',
                        choices=['bar', 'line', 'pie', 'donut', 'radar', 'waterfall'],
                        required=True,
                        help='图表类型: bar(柱状图) | line(折线图) | pie(饼图) | donut(环形图) | radar(雷达图) | waterfall(瀑布图)')

    parser.add_argument('--data', '-d',
                        required=True,
                        help='数据，格式: "类别1:值1,类别2:值2,..." 或 "值1,值2,..."')

    parser.add_argument('--color', '-c',
                        choices=['blue', 'orange', 'green', 'gold_blue', 'multilayer'],
                        default='blue',
                        help='配色方案: blue(科技蓝) | orange(商务橙) | green(专业绿) | gold_blue(高端金蓝) | multilayer(多层次专业)')

    parser.add_argument('--title', '-T',
                        default='',
                        help='图表标题')

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
    categories, values = parse_data(args.data)
    print(f"✓ 数据解析完成: {len(categories)}个数据点")

    # 设置标题
    title = args.title if args.title else f"{scheme['name']} - {args.type.upper()}图表"

    # 设置输出文件名
    if args.output:
        output = args.output
    else:
        output = f"chart_{args.type}_{args.color}.png"

    # 生成图表
    if args.type == 'bar':
        generate_bar_chart(categories, values, scheme, title, output)
    elif args.type == 'line':
        generate_line_chart(categories, values, scheme, title, output)
    elif args.type == 'pie':
        generate_pie_chart(categories, values, scheme, title, output)
    elif args.type == 'donut':
        generate_donut_chart(categories, values, scheme, title, output)
    elif args.type == 'radar':
        generate_radar_chart(categories, values, scheme, title, output)
    elif args.type == 'waterfall':
        generate_waterfall_chart(categories, values, scheme, title, output)

    print(f"\n✓ 图表生成成功!")
    print(f"  文件位置: {Path(output).absolute()}")
    print(f"  配色方案: {scheme['name']}")
    print(f"  图表类型: {args.type}")


if __name__ == "__main__":
    main()
