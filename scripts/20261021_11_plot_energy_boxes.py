# -*- coding: utf-8 -*-
import json
#import openpyxl
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
import config

rcParams['font.size'] = 20
rcParams['axes.labelsize'] = 36
rcParams['xtick.labelsize'] = 20
rcParams['ytick.labelsize'] = 20
#rcParams['lines.markersize'] = 10
rcParams['lines.linewidth'] = 3
rcParams['font.family'] = 'Hiragino Sans'

list_subcategory = [
    '#500000', # FEC
    '#600100', # 産業
    '#611000', # 農林水産業
    '#612000', # 鉱業他
    '#615000', # 建設業
    '#620000', # 製造業
    '#622000', # 繊維工業
    '#624000', # パルプ･紙･紙加工品
    '#626000', # 化学工業 (含 石油石炭製品)
    '#628000', # 窯業･土石製品製造業
    '#629100', # 鉄鋼業
    '#629900', # 機械（含金属製品）
    '#650000', # 業務他 (第三次産業)
    '#700000', # 家庭
    '#800000', # 運輸
    '#810000', # 旅客
    '#850000', # 貨物
]
n_subcategory = len(list_subcategory)

list_subcatlabel = [
    'エネルギー起源',
    '産業',
    '農林水産',
    '鉱業他',
    '建設',
    '製造',
    '繊維',
    'パルプ･紙',
    '化学',
    '窯業･土石',
    '鉄鋼',
    '機械',
    '業務他',
    '家庭',
    '運輸',
    '旅客',
    '貨物',
]

list_subcat_to_plot = [
    2, # 農林水産業
    3, # 鉱業他
    4, # 建設業
    5, # 製造業
    12, # 業務他
    13, # 家庭
    14, # 運輸
]
n_subcat_to_plot = len(list_subcat_to_plot)

colors_lgt = [
    config.COL_SUNFLOWER_LIGHT,   # 農林水産業
    config.COL_AMETHYST_LIGHT,    # 鉱業他
    config.COL_TURQUOISE_LIGHT,   # 建設業
    config.COL_ALIZARIN_LIGHT,    # 製造業
    config.COL_BELIZE_HOLE_LIGHT, # 業務他
    config.COL_NEPHRITIS_LIGHT,   # 家庭
    config.COL_ORANGE_LIGHT       # 運輸
]

colors_med = [
    config.COL_SUNFLOWER_MED,   # 農林水産業
    config.COL_AMETHYST_MED,    # 鉱業他
    config.COL_TURQUOISE_MED,   # 建設業
    config.COL_ALIZARIN_MED,    # 製造業
    config.COL_BELIZE_HOLE_MED, # 業務他
    config.COL_NEPHRITIS_MED,   # 家庭
    config.COL_ORANGE_MED       # 運輸
]

colors = [
    config.COL_SUNFLOWER_DARK,   # 農林水産業
    config.COL_AMETHYST_DARK,    # 鉱業他
    config.COL_TURQUOISE_DARK,   # 建設業
    config.COL_ALIZARIN_DARK,    # 製造業
    config.COL_BELIZE_HOLE_DARK, # 業務他
    config.COL_NEPHRITIS_DARK,   # 家庭
    config.COL_ORANGE_DARK       # 運輸
]

# plot parameters
xmin = -0.1
xmax = 1.2
ymin = 0
ymax = 1.2
factor = 0.9
textoffset = 0.005


input_json_file1 = 'outputs/20251201_21_energy_stat/20251201_21_energy_stat_data_common_3_エネルギー利用.json'
input_json_file2 = 'outputs/20251218_01_intensity/20260311_01_energy_stat_intensity_data_common_3_エネルギー利用.json'

input_json_file1_1p5CRM_steps = 'outputs/20251201_03_1p5CRM_steps_energy/20251201_13_1p5CRM_steps_energy_data_common_10_エネルギー利用.json'
input_json_file2_1p5CRM_steps = 'outputs/20251218_01_intensity/20251218_03_1p5CRM_steps_intensity_data_common_10_エネルギー利用.json'
input_json_file1_1p5CRM_balnc = 'outputs/20251201_01_1p5CRM_balance_energy/20251201_11_1p5CRM_balance_energy_data_common_10_エネルギー利用.json'
input_json_file2_1p5CRM_balnc = 'outputs/20251218_01_intensity/20251218_02_1p5CRM_balance_intensity_data_common_10_エネルギー利用.json'

output_png_file_2013 = 'charts/20261021_11_plot_energy_boxes_2013.png'
output_png_file_2023 = 'charts/20261021_11_plot_energy_boxes_2023.png'
output_png_file_2030_steps = 'charts/20261021_11_plot_energy_boxes_2030_steps.png'
output_png_file_2030_balnc = 'charts/20261021_11_plot_energy_boxes_2030_balance.png'
output_png_file_2040_steps = 'charts/20261021_11_plot_energy_boxes_2040_steps.png'
output_png_file_2040_balnc = 'charts/20261021_11_plot_energy_boxes_2040_balance.png'

YEAR1_START = 2013
YEAR1_END   = 2024

def load_data_energy_stat():
    year1_list = []
    for i in range(YEAR1_START, YEAR1_END):
        year1_list.append('%d' % (i))

    dict1_dtype = {
        'id': str,
        'item_name_jp': str,
        'level': int,
        'n_sub': int,
        'unit': str,
        '2013': float,
        '2014': float,
        '2015': float,
        '2016': float,
        '2017': float,
        '2018': float,
        '2019': float,
        '2020': float,
        '2021': float,
        '2022': float,
        '2023': float,
    }
    df_e = pd.read_json(input_json_file1, orient='index', dtype=dict1_dtype)
    df_i = pd.read_json(input_json_file2, orient='index', dtype=dict1_dtype)

    return df_e, df_i

def load_data_1p5CRM():
    year1_list = []
    for i in range(YEAR1_START, YEAR1_END):
        year1_list.append('%d' % (i))

    dict1_dtype = {
        'id': str,
        'item_name_jp': str,
        'level': int,
        'n_sub': int,
        'unit': str,
        '2030': float,
        '2040': float,
        '2050': float,
    }
    df_steps_e = pd.read_json(input_json_file1_1p5CRM_steps, orient='index', dtype=dict1_dtype)
    df_steps_i = pd.read_json(input_json_file2_1p5CRM_steps, orient='index', dtype=dict1_dtype)
    df_balnc_e = pd.read_json(input_json_file1_1p5CRM_balnc, orient='index', dtype=dict1_dtype)
    df_balnc_i = pd.read_json(input_json_file2_1p5CRM_balnc, orient='index', dtype=dict1_dtype)

    return df_steps_e, df_steps_i, df_balnc_e, df_balnc_i

def plot_texts(ax, heights, widths):
    fs1 = 24
    fs2 = 36
    lw1 = 3

    texts = [
        {
            'text': '農林水産業',
            'posx': -0.1 * factor,
            'posy': 1.2 * factor
        },
        {
            'text': '鉱業',
            'posx': -0.05 * factor,
            'posy': 1.15 * factor
        },
        {
            'text': '建設業',
            'posx': 0.0 * factor,
            'posy': 1.1 * factor
        },
        {
            'text': '製造業'
        },
        {
            'text': '業務'
        },
        {
            'text': '家庭'
        },
        {
            'text': '運輸'
        }
    ]

    for i in range(3):
        ax.text(texts[i]['posx'], texts[i]['posy'], texts[i]['text'], color=colors[i], fontsize=fs1)
        lx = np.array([widths[i], texts[i]['posx']+0.01])
        ly = np.array([heights[i], texts[i]['posy']-0.01])
        ax.plot(lx, ly, '-', color=colors_lgt[i], linewidth=lw1)

    for i in range(3, n_subcat_to_plot):
        ax.text(widths[i], heights[i]*0.5, texts[i]['text'], color='#EEEEEE', fontsize=fs2, weight='bold', ha='center')

    return

def plot_2013(df_e, df_i):

    tid_FEC = '#500000'
    e_FEC_2013 = df_e[df_e['id']==tid_FEC]['2013'].values[0]
    i_FEC_2013 = df_i[df_i['id']==tid_FEC]['2013'].values[0]

    heights = np.zeros(n_subcat_to_plot)
    widths = np.zeros(n_subcat_to_plot)

    fig, ax = plt.subplots(figsize=(15,15))

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel('エネルギー消費量')
    ax.set_ylabel('排出原単位')
#    ax.set_xticks(np.array([0.0, 1.0]))
#    ax.set_yticks(np.array([0.0, 1.0]))
    ax.set_xticks(np.array([]))
    ax.set_yticks(np.array([]))
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)

    px = 0.0
    for i in range(n_subcat_to_plot):
        tid = list_subcategory[list_subcat_to_plot[i]]
        e_2013 = df_e[df_e['id']==tid]['2013'].values[0]
        i_2013 = df_i[df_i['id']==tid]['2013'].values[0]

        wid1 = e_2013 / e_FEC_2013 * factor
        hgt1 = i_2013 / i_FEC_2013 * factor

        r = Rectangle((px,0), wid1, hgt1, facecolor=colors[i], edgecolor=colors[i], lw=2, ls='-')
        ax.add_patch(r)

        heights[i] = hgt1
        widths[i] = px
        if i >= 3:
            widths[i] += wid1*0.5
        px = px + wid1

    lx = [xmin, xmax]
    ly = [ymin, ymin]
    ax.plot(lx, ly, lw=3, color=config.COL_ASBESTOS_DARK)
    lx = [xmin, xmin]
    ly = [ymin, ymax]
    ax.plot(lx, ly, lw=3, color=config.COL_ASBESTOS_DARK)

    ax.text(xmax-(xmax-xmin)*0.3, ymax-(ymax-ymin)*0.1, '2013', fontsize=36, color=config.COL_ASBESTOS_DARK)

    plot_texts(ax, heights, widths)

    plt.tight_layout()
    #plt.show()
    plt.savefig(output_png_file_2013)

def plot_2023(df_e, df_i):

    tid_FEC = '#500000'
    e_FEC_2013 = df_e[df_e['id']==tid_FEC]['2013'].values[0]
    i_FEC_2013 = df_i[df_i['id']==tid_FEC]['2013'].values[0]

    heights = np.zeros(n_subcat_to_plot)
    widths = np.zeros(n_subcat_to_plot)

    # 2023
    fig, ax = plt.subplots(figsize=(15,15))

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel('エネルギー消費量')
    ax.set_ylabel('排出原単位')
#    ax.set_xticks(np.array([0.0, 1.0]))
#    ax.set_yticks(np.array([0.0, 1.0]))
    ax.set_xticks(np.array([]))
    ax.set_yticks(np.array([]))
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)

    px = 0.0
    for i in range(n_subcat_to_plot):
        tid = list_subcategory[list_subcat_to_plot[i]]
        e_2013 = df_e[df_e['id']==tid]['2013'].values[0]
        i_2013 = df_i[df_i['id']==tid]['2013'].values[0]
        e_2023 = df_e[df_e['id']==tid]['2023'].values[0]
        i_2023 = df_i[df_i['id']==tid]['2023'].values[0]

        wid1 = e_2013 / e_FEC_2013 * factor
        hgt1 = i_2013 / i_FEC_2013 * factor
        wid2 = e_2023 / e_FEC_2013 * factor
        hgt2 = i_2023 / i_FEC_2013 * factor

        r = Rectangle((px,0), wid1, hgt1, facecolor='w', edgecolor=colors[i], lw=2, ls='--')
        ax.add_patch(r)
        r = Rectangle((px,0), wid2, hgt2, facecolor=colors[i], edgecolor=colors[i], lw=2, ls='-')
        ax.add_patch(r)

        if i == 3:
            ax.text(px+wid1-textoffset, hgt1+textoffset, '2013', color=colors[i], ha='right')
            ax.text(px+wid2-textoffset, hgt2+textoffset, '2023', color=colors[i], ha='right')

        heights[i] = hgt2
        widths[i] = px
        if i >= 3:
            widths[i] += wid2*0.5

        px = px + np.max(np.array([wid1, wid2]))

    lx = [xmin, xmax]
    ly = [ymin, ymin]
    ax.plot(lx, ly, lw=3, color=config.COL_ASBESTOS_DARK)
    lx = [xmin, xmin]
    ly = [ymin, ymax]
    ax.plot(lx, ly, lw=3, color=config.COL_ASBESTOS_DARK)

    ax.text(xmax-(xmax-xmin)*0.3, ymax-(ymax-ymin)*0.1, '2023', fontsize=36, color=config.COL_ASBESTOS_DARK)

    plot_texts(ax, heights, widths)

    plt.tight_layout()
    #plt.show()
    plt.savefig(output_png_file_2023)

def plot_2030_steps(df_e, df_i, df_steps_e, df_steps_i):

    tid_FEC = '#500000'
    e_FEC_2013 = df_e[df_e['id']==tid_FEC]['2013'].values[0]
    i_FEC_2013 = df_i[df_i['id']==tid_FEC]['2013'].values[0]

    heights = np.zeros(n_subcat_to_plot)
    widths = np.zeros(n_subcat_to_plot)

    # 2030
    fig, ax = plt.subplots(figsize=(15,15))

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel('エネルギー消費量')
    ax.set_ylabel('排出原単位')
#    ax.set_xticks(np.array([0.0, 1.0]))
#    ax.set_yticks(np.array([0.0, 1.0]))
    ax.set_xticks(np.array([]))
    ax.set_yticks(np.array([]))
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)

    px = 0.0
    for i in range(n_subcat_to_plot):
        tid = list_subcategory[list_subcat_to_plot[i]]
        e_2013 = df_e[df_e['id']==tid]['2013'].values[0]
        i_2013 = df_i[df_i['id']==tid]['2013'].values[0]
        e_2030 = df_steps_e[df_steps_e['id']==tid]['2030'].values[0]
        i_2030 = df_steps_i[df_steps_i['id']==tid]['2030'].values[0]

        wid1 = e_2013 / e_FEC_2013 * factor
        hgt1 = i_2013 / i_FEC_2013 * factor
        wid2 = e_2030 / e_FEC_2013 * factor
        hgt2 = i_2030 / i_FEC_2013 * factor

        r = Rectangle((px,0), wid1, hgt1, facecolor='w', edgecolor=colors[i], lw=2, ls='--')
        ax.add_patch(r)
        r = Rectangle((px,0), wid2, hgt2, facecolor=colors[i], edgecolor=colors[i], lw=2, ls='-')
        ax.add_patch(r)

        if i == 3:
            ax.text(px+wid1-textoffset, hgt1+textoffset, '2013', color=colors[i], ha='right')
            ax.text(px+wid2-textoffset, hgt2+textoffset, '2030', color=colors[i], ha='right')

        heights[i] = hgt2
        widths[i] = px
        if i >= 3:
            widths[i] += wid2*0.5

        px = px + np.max(np.array([wid1, wid2]))

    lx = [xmin, xmax]
    ly = [ymin, ymin]
    ax.plot(lx, ly, lw=3, color=config.COL_ASBESTOS_DARK)
    lx = [xmin, xmin]
    ly = [ymin, ymax]
    ax.plot(lx, ly, lw=3, color=config.COL_ASBESTOS_DARK)

    plot_texts(ax, heights, widths)

    plt.tight_layout()
    #plt.show()
    plt.savefig(output_png_file_2030_steps)

def plot_2030_balnc(df_e, df_i, df_balnc_e, df_balnc_i):

    tid_FEC = '#500000'
    e_FEC_2013 = df_e[df_e['id']==tid_FEC]['2013'].values[0]
    i_FEC_2013 = df_i[df_i['id']==tid_FEC]['2013'].values[0]

    heights = np.zeros(n_subcat_to_plot)
    widths = np.zeros(n_subcat_to_plot)

    # 2030
    fig, ax = plt.subplots(figsize=(15,15))

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel('エネルギー消費量')
    ax.set_ylabel('排出原単位')
#    ax.set_xticks(np.array([0.0, 1.0]))
#    ax.set_yticks(np.array([0.0, 1.0]))
    ax.set_xticks(np.array([]))
    ax.set_yticks(np.array([]))
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)

    px = 0.0
    for i in range(n_subcat_to_plot):
        tid = list_subcategory[list_subcat_to_plot[i]]
        e_2013 = df_e[df_e['id']==tid]['2013'].values[0]
        i_2013 = df_i[df_i['id']==tid]['2013'].values[0]
        e_2030 = df_balnc_e[df_balnc_e['id']==tid]['2030'].values[0]
        i_2030 = df_balnc_i[df_balnc_i['id']==tid]['2030'].values[0]

        wid1 = e_2013 / e_FEC_2013 * factor
        hgt1 = i_2013 / i_FEC_2013 * factor
        wid2 = e_2030 / e_FEC_2013 * factor
        hgt2 = i_2030 / i_FEC_2013 * factor

        r = Rectangle((px,0), wid1, hgt1, facecolor='w', edgecolor=colors[i], lw=2, ls='--')
        ax.add_patch(r)
        r = Rectangle((px,0), wid2, hgt2, facecolor=colors[i], edgecolor=colors[i], lw=2, ls='-')
        ax.add_patch(r)

        if i == 3:
            ax.text(px+wid1-textoffset, hgt1+textoffset, '2013', color=colors[i], ha='right')
            ax.text(px+wid2-textoffset, hgt2+textoffset, '2030', color=colors[i], ha='right')

        heights[i] = hgt2
        widths[i] = px
        if i >= 3:
            widths[i] += wid2*0.5

        px = px + np.max(np.array([wid1, wid2]))

    lx = [xmin, xmax]
    ly = [ymin, ymin]
    ax.plot(lx, ly, lw=3, color=config.COL_ASBESTOS_DARK)
    lx = [xmin, xmin]
    ly = [ymin, ymax]
    ax.plot(lx, ly, lw=3, color=config.COL_ASBESTOS_DARK)

    plot_texts(ax, heights, widths)

    plt.tight_layout()
    #plt.show()
    plt.savefig(output_png_file_2030_balnc)

def plot_2040_steps(df_e, df_i, df_steps_e, df_steps_i):

    tid_FEC = '#500000'
    e_FEC_2013 = df_e[df_e['id']==tid_FEC]['2013'].values[0]
    i_FEC_2013 = df_i[df_i['id']==tid_FEC]['2013'].values[0]

    heights = np.zeros(n_subcat_to_plot)
    widths = np.zeros(n_subcat_to_plot)

    # 2040
    fig, ax = plt.subplots(figsize=(15,15))

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel('エネルギー消費量')
    ax.set_ylabel('排出原単位')
#    ax.set_xticks(np.array([0.0, 1.0]))
#    ax.set_yticks(np.array([0.0, 1.0]))
    ax.set_xticks(np.array([]))
    ax.set_yticks(np.array([]))
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)

    px = 0.0
    for i in range(n_subcat_to_plot):
        tid = list_subcategory[list_subcat_to_plot[i]]
        e_2013 = df_e[df_e['id']==tid]['2013'].values[0]
        i_2013 = df_i[df_i['id']==tid]['2013'].values[0]
        e_2040 = df_steps_e[df_steps_e['id']==tid]['2040'].values[0]
        i_2040 = df_steps_i[df_steps_i['id']==tid]['2040'].values[0]

        wid1 = e_2013 / e_FEC_2013 * factor
        hgt1 = i_2013 / i_FEC_2013 * factor
        wid2 = e_2040 / e_FEC_2013 * factor
        hgt2 = i_2040 / i_FEC_2013 * factor

        r = Rectangle((px,0), wid1, hgt1, facecolor='w', edgecolor=colors[i], lw=2, ls='--')
        ax.add_patch(r)
        r = Rectangle((px,0), wid2, hgt2, facecolor=colors[i], edgecolor=colors[i], lw=2, ls='-')
        ax.add_patch(r)

        if i == 3:
            ax.text(px+wid1-textoffset, hgt1+textoffset, '2013', color=colors[i], ha='right')
            ax.text(px+wid2-textoffset, hgt2+textoffset, '2040', color=colors[i], ha='right')

        heights[i] = hgt2
        widths[i] = px
        if i >= 3:
            widths[i] += wid2*0.5

        px = px + np.max(np.array([wid1, wid2]))

    lx = [xmin, xmax]
    ly = [ymin, ymin]
    ax.plot(lx, ly, lw=3, color=config.COL_ASBESTOS_DARK)
    lx = [xmin, xmin]
    ly = [ymin, ymax]
    ax.plot(lx, ly, lw=3, color=config.COL_ASBESTOS_DARK)

    plot_texts(ax, heights, widths)

    plt.tight_layout()
    #plt.show()
    plt.savefig(output_png_file_2040_steps)

def plot_2040_balnc(df_e, df_i, df_balnc_e, df_balnc_i):

    tid_FEC = '#500000'
    e_FEC_2013 = df_e[df_e['id']==tid_FEC]['2013'].values[0]
    i_FEC_2013 = df_i[df_i['id']==tid_FEC]['2013'].values[0]

    heights = np.zeros(n_subcat_to_plot)
    widths = np.zeros(n_subcat_to_plot)

    # 2040
    fig, ax = plt.subplots(figsize=(15,15))

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel('エネルギー消費量')
    ax.set_ylabel('排出原単位')
#    ax.set_xticks(np.array([0.0, 1.0]))
#    ax.set_yticks(np.array([0.0, 1.0]))
    ax.set_xticks(np.array([]))
    ax.set_yticks(np.array([]))
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)

    px = 0.0
    for i in range(n_subcat_to_plot):
        tid = list_subcategory[list_subcat_to_plot[i]]
        e_2013 = df_e[df_e['id']==tid]['2013'].values[0]
        i_2013 = df_i[df_i['id']==tid]['2013'].values[0]
        e_2040 = df_balnc_e[df_balnc_e['id']==tid]['2040'].values[0]
        i_2040 = df_balnc_i[df_balnc_i['id']==tid]['2040'].values[0]

        wid1 = e_2013 / e_FEC_2013 * factor
        hgt1 = i_2013 / i_FEC_2013 * factor
        wid2 = e_2040 / e_FEC_2013 * factor
        hgt2 = i_2040 / i_FEC_2013 * factor

        r = Rectangle((px,0), wid1, hgt1, facecolor='w', edgecolor=colors[i], lw=2, ls='--')
        ax.add_patch(r)
        r = Rectangle((px,0), wid2, hgt2, facecolor=colors[i], edgecolor=colors[i], lw=2, ls='-')
        ax.add_patch(r)

        if i == 3:
            ax.text(px+wid1-textoffset, hgt1+textoffset, '2013', color=colors[i], ha='right')
            ax.text(px+wid2-textoffset, hgt2+textoffset, '2040', color=colors[i], ha='right')

        heights[i] = hgt2
        widths[i] = px
        if i >= 3:
            widths[i] += wid2*0.5

        px = px + np.max(np.array([wid1, wid2]))

    lx = [xmin, xmax]
    ly = [ymin, ymin]
    ax.plot(lx, ly, lw=3, color=config.COL_ASBESTOS_DARK)
    lx = [xmin, xmin]
    ly = [ymin, ymax]
    ax.plot(lx, ly, lw=3, color=config.COL_ASBESTOS_DARK)

    plot_texts(ax, heights, widths)

    plt.tight_layout()
    #plt.show()
    plt.savefig(output_png_file_2040_balnc)


if __name__ == '__main__':
    df_e, df_i = load_data_energy_stat()
    df_steps_e, df_steps_i, df_balnc_e, df_balnc_i = load_data_1p5CRM()

    plot_2013(df_e, df_i)
    plot_2023(df_e, df_i)
    plot_2030_steps(df_e, df_i, df_steps_e, df_steps_i)
    plot_2030_balnc(df_e, df_i, df_balnc_e, df_balnc_i)
    plot_2040_steps(df_e, df_i, df_steps_e, df_steps_i)
    plot_2040_balnc(df_e, df_i, df_balnc_e, df_balnc_i)
