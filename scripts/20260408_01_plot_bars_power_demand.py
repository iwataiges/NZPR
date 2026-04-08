# 20251231
# 20260408
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import openpyxl
import pandas as pd
from matplotlib import rcParams
import config

INPUT_JSON_FILE1 = 'outputs/20251201_01_1p5CRM_balance_energy/20251201_11_1p5CRM_balance_energy_data_common_07_電力.json'
INPUT_JSON_FILE2 = 'outputs/20251201_03_1p5CRM_steps_energy/20251201_13_1p5CRM_steps_energy_data_common_07_電力.json'
INPUT_JSON_OCCTO_FILE = 'outputs/20251231_01_OCCTO/20260408_01_OCCTO_power_demand.json'

OUTPUT_PLOT = 'charts/20260408_01_plot_bars_power_demand.png'

YEAR1 = 2013
YEAR2 = 2050
XMIN = 0.0
XMAX = 5.0

rcParams['font.size'] = 16
rcParams['axes.labelsize'] = 16
rcParams['xtick.labelsize'] = 18
rcParams['ytick.labelsize'] = 18
#rcParams['lines.markersize'] = 10
rcParams['lines.linewidth'] = 5
rcParams['font.family'] = 'Hiragino Sans'
#rcParams['xtick.labelsize'] = 'small'
#rcParams['ytick.labelsize'] = 'small'

ids_to_plot = [
    '#611000', # 農林水産業
    '#612000', # 鉱業他
    '#615000', # 建設業
    '#620000', # 製造業
    '#650000', # 業務他
    '#700000', # 家庭
    '#800000', # 運輸
]

colors = [
    config.COL_BROWN_MED,     # 農林水産業
    config.COL_GREY_MED,      # 鉱業他
    config.COL_BLUE_GREY_MED, # 建設業
    config.COL_RED_MED,       # 製造業
    config.COL_BLUE_MED,      # 業務他
    config.COL_GREEN_MED,     # 家庭
    config.COL_ORANGE_MED     # 運輸
]
labels = ['農林水産', '鉱業他', '建設業', '製造業', '業務他', '家庭', '運輸']

color_matrix = [
    [config.COL_ORANGE_MED, config.COL_ORANGE_DARK],
    [config.COL_GREEN_MED, config.COL_GREEN_DARK],
    [config.COL_BLUE_MED, config.COL_BLUE_DARK],
    [config.COL_BROWN_MED, config.COL_BROWN_DARK],
    [config.COL_CYAN_MED, config.COL_CYAN_DARK],
    [config.COL_AMBER_MED, config.COL_AMBER_DARK],
    [config.COL_CONCRETE_MED, config.COL_CONCRETE_DARK],
    [config.COL_ASBESTOS_MED, config.COL_ASBESTOS_DARK],
    [config.COL_WET_ASPHALT_MED, config.COL_WET_ASPHALT_DARK],
    [config.COL_PURPLE_MED, config.COL_PURPLE_DARK],
    [config.COL_LIGHT_BLUE_MED, config.COL_LIGHT_BLUE_DARK],
    [config.COL_DEEP_ORANGE_MED, config.COL_DEEP_ORANGE_DARK]
]

TJ_to_TWh = 1.0/3600.0


def load_data():
    dict1_dtype = {
        'id': str,
        'row': int,
        'level': int,
        'n_sub': int,
        'item_name_jp': str,
        'unit': str
    }

    df1 = pd.read_json(INPUT_JSON_FILE1, orient='index', dtype=dict1_dtype)
    df2 = pd.read_json(INPUT_JSON_FILE2, orient='index', dtype=dict1_dtype)

    df1_1 = df1[df1['id'].isin(ids_to_plot)]
    df2_1 = df2[df2['id'].isin(ids_to_plot)]

    dict2_dtype = {
        'Year': int,
        "需要電力量_送電端":float,
        "需要電力量_送電端_モデルケース1":float,
        "需要電力量_送電端_モデルケース2":float,
        "需要電力量_送電端_モデルケース3":float,
        "需要電力量_送電端_モデルケース4":float,
        "unit":str
    }
    df_occto = pd.read_json(INPUT_JSON_OCCTO_FILE, orient='index', dtype=dict2_dtype)

    return df1_1, df2_1, df_occto

def plot(df1, df2, df_occto):

    fig, ax = plt.subplots(figsize=(15,10))
    ymax = 1200
    xmin_disp = -0.5
    xmax_disp = 5.5
#    ax.set(xlim=(xmin, xmax), ylim=(0, ymax))
    ax.set(xlim=(xmin_disp, xmax_disp))
    ax.set_ylabel('需要電力量 [TWh/年]')

    width1 = 0.1
    fs = 12

    offset1 = 0.0
    offset2 = 0.12
    textoffset = 0.03
    # 2030
    x = (XMAX - XMIN) * (2030 - YEAR1) / (YEAR2 - YEAR1)
    y1 = 0
    for i in range(len(ids_to_plot)):
        v = df1[df1['id']==ids_to_plot[i]]["2030"].values[0] * TJ_to_TWh
    #    y2 = v
    #    ax.bar(x+width1/2.0+offset1, y2, width1, bottom=y1, align='center', color=colors[i])
        y1 = y1 + v
    text = '%d' % (int(y1))
    ax.bar(x+width1/2.0+offset1, y1, width1, align='center', color=config.COL_TURQUOISE_MED)
    ax.text(x+width1/2.0+offset1, y1 + ymax*0.01, text, ha='center', fontsize=fs, color=config.COL_TURQUOISE_MED)
    y1 = 0
    for i in range(len(ids_to_plot)):
        v = df2[df2['id']==ids_to_plot[i]]["2030"].values[0] * TJ_to_TWh
    #    y2 = v
    #    ax.bar(x+width1/2.0+offset2, y2, width1, bottom=y1, align='center', color=colors[i])
        y1 = y1 + v
    text = '%d' % (int(y1))
    ax.bar(x+width1/2.0+offset2, y1, width1, align='center', color=config.COL_ORANGE_MED)
    ax.text(x+width1/2.0+offset2+textoffset, y1 + ymax*0.01, text, ha='center', fontsize=fs, color=config.COL_ORANGE_MED)

    # 2035
    x = (XMAX - XMIN) * (2035 - YEAR1) / (YEAR2 - YEAR1)
    y1 = 0
    for i in range(len(ids_to_plot)):
        v1 = df1[df1['id']==ids_to_plot[i]]["2030"].values[0] * TJ_to_TWh
        v2 = df1[df1['id']==ids_to_plot[i]]["2040"].values[0] * TJ_to_TWh
        y2 = (v1+v2)/2.0
        #ax.bar(x+width1/2.0+offset1, y2, width1, bottom=y1, align='center', color=colors[i])
        y1 = y1 + y2
    text = '%d' % (int(y1))
    ax.bar(x+width1/2.0+offset1, y1, width1, align='center', color=config.COL_TURQUOISE_MED)
    ax.text(x+width1/2.0+offset1, y1 + ymax*0.01, text, ha='center', fontsize=fs, color=config.COL_TURQUOISE_MED)
    y1 = 0
    for i in range(len(ids_to_plot)):
        v1 = df2[df2['id']==ids_to_plot[i]]["2030"].values[0] * TJ_to_TWh
        v2 = df2[df2['id']==ids_to_plot[i]]["2040"].values[0] * TJ_to_TWh
        y2 = (v1+v2)/2.0
        #ax.bar(x+width1/2.0+offset2, y2, width1, bottom=y1, align='center', color=colors[i])
        y1 = y1 + y2
    text = '%d' % (int(y1))
    ax.bar(x+width1/2.0+offset2, y1, width1, align='center', color=config.COL_ORANGE_MED)
    ax.text(x+width1/2.0+offset2+textoffset, y1 + ymax*0.01, text, ha='center', fontsize=fs, color=config.COL_ORANGE_MED)

    # 2040
    x = (XMAX - XMIN) * (2040 - YEAR1) / (YEAR2 - YEAR1)
    y1 = 0
    for i in range(len(ids_to_plot)):
        v = df1[df1['id']==ids_to_plot[i]]["2040"].values[0] * TJ_to_TWh
        #y2 = v
        #ax.bar(x+width1/2.0+offset1, y2, width1, bottom=y1, align='center', color=colors[i])
        y1 = y1 + v
    text = '%d' % (int(y1))
    ax.bar(x+width1/2.0+offset1, y1, width1, align='center', color=config.COL_TURQUOISE_MED)
    ax.text(x+width1/2.0+offset1, y1 + ymax*0.01, text, ha='center', fontsize=fs, color=config.COL_TURQUOISE_MED)
    y1 = 0
    for i in range(len(ids_to_plot)):
        v = df2[df2['id']==ids_to_plot[i]]["2040"].values[0] * TJ_to_TWh
        #y2 = v
        #ax.bar(x+width1/2.0+offset2, y2, width1, bottom=y1, align='center', color=colors[i])
        y1 = y1 + v
    text = '%d' % (int(y1))
    ax.bar(x+width1/2.0+offset2, y1, width1, align='center', color=config.COL_ORANGE_MED)
    ax.text(x+width1/2.0+offset2+textoffset, y1 + ymax*0.01, text, ha='center', fontsize=fs, color=config.COL_ORANGE_MED)

    # 2050
    x = (XMAX - XMIN) * (2050 - YEAR1) / (YEAR2 - YEAR1)
    y1 = 0
    for i in range(len(ids_to_plot)):
        v = df1[df1['id']==ids_to_plot[i]]["2050"].values[0] * TJ_to_TWh
        #y2 = v
        #ax.bar(x+width1/2.0+offset1, y2, width1, bottom=y1, align='center', color=colors[i])
        y1 = y1 + v
    text = '%d' % (int(y1))
    ax.bar(x+width1/2.0+offset1, y1, width1, align='center', color=config.COL_TURQUOISE_MED)
    ax.text(x+width1/2.0+offset1, y1 + ymax*0.01, text, ha='center', fontsize=fs, color=config.COL_TURQUOISE_MED)
    y1 = 0
    for i in range(len(ids_to_plot)):
        v = df2[df2['id']==ids_to_plot[i]]["2050"].values[0] * TJ_to_TWh
        #y2 = v
        #ax.bar(x+width1/2.0+offset2, y2, width1, bottom=y1, align='center', color=colors[i])
        y1 = y1 + v
    text = '%d' % (int(y1))
    ax.bar(x+width1/2.0+offset2, y1, width1, align='center', color=config.COL_ORANGE_MED)
    ax.text(x+width1/2.0+offset2+textoffset, y1 + ymax*0.01, text, ha='center', fontsize=fs, color=config.COL_ORANGE_MED)


    # OCCTO
    ## 2013
    x = (XMAX - XMIN) * (2013 - YEAR1) / (YEAR2 - YEAR1)
    y2 = df_occto[df_occto['Year']==2013]['需要電力量_送電端'].values[0]
    ax.bar(x+width1/2.0, y2, width1, align='center', color=config.COL_SILVER_DARK)
    text = '%d' % (int(y2))
    ax.text(x+width1/2.0, y2 + ymax*0.01, text, ha='center', fontsize=fs, color=config.COL_SILVER_DARK)

    ## 2023
    x = (XMAX - XMIN) * (2023 - YEAR1) / (YEAR2 - YEAR1)
    y2 = df_occto[df_occto['Year']==2023]['需要電力量_送電端'].values[0]
    ax.bar(x+width1/2.0, y2, width1, align='center', color=config.COL_SILVER_DARK)
    text = '%d' % (int(y2))
    ax.text(x+width1/2.0, y2 + ymax*0.01, text, ha='center', fontsize=fs, color=config.COL_SILVER_DARK)

    offset = -0.12
    textoffset = -0.03
    ## 2030
    x = (XMAX - XMIN) * (2030 - YEAR1) / (YEAR2 - YEAR1)
    y2 = df_occto[df_occto['Year']==2030]['需要電力量_送電端'].values[0]
    ax.bar(x+width1/2.0+offset, y2, width1, align='center', color=config.COL_SILVER_MED)
    text = '%d' % (int(y2))
    ax.text(x+width1/2.0+offset+textoffset, y2 + ymax*0.01, text, ha='center', fontsize=fs, color=config.COL_SILVER_MED)

    ## 2035
    x = (XMAX - XMIN) * (2035 - YEAR1) / (YEAR2 - YEAR1)
    y2 = df_occto[df_occto['Year']==2035]['需要電力量_送電端'].values[0]
    ax.bar(x+width1/2.0+offset, y2, width1, align='center', color=config.COL_SILVER_MED)
    text = '%d' % (int(y2))
    ax.text(x+width1/2.0+offset+textoffset, y2 + ymax*0.01, text, ha='center', fontsize=fs, color=config.COL_SILVER_MED)

    ## 2040
    x = (XMAX - XMIN) * (2040 - YEAR1) / (YEAR2 - YEAR1)
    y2 = df_occto[df_occto['Year']==2040]['需要電力量_送電端_モデルケース1'].values[0]
    ax.bar(x+width1/2.0+offset*2, y2, width1, align='center', color=config.COL_SILVER_MED)
    text = '%d' % (int(y2))
    ax.text(x+width1/2.0+offset*2+textoffset, y2 + ymax*0.01, text, ha='center', fontsize=fs, color=config.COL_SILVER_MED)
    y2 = df_occto[df_occto['Year']==2040]['需要電力量_送電端_モデルケース2'].values[0]
    ax.bar(x+width1/2.0+offset, y2, width1, align='center', color=config.COL_SILVER_MED)
    text = '%d' % (int(y2))
    ax.text(x+width1/2.0+offset, y2 + ymax*0.01, text, ha='center', fontsize=fs, color=config.COL_SILVER_MED)

    ## 2050
    x = (XMAX - XMIN) * (2050 - YEAR1) / (YEAR2 - YEAR1)
    y2 = df_occto[df_occto['Year']==2050]['需要電力量_送電端_モデルケース1'].values[0]
    ax.bar(x+width1/2.0+offset*4, y2, width1, align='center', color=config.COL_SILVER_MED)
    text = '%d' % (int(y2))
    ax.text(x+width1/2.0+offset*4, y2 + ymax*0.01, text, ha='center', fontsize=fs, color=config.COL_SILVER_MED)
    y2 = df_occto[df_occto['Year']==2050]['需要電力量_送電端_モデルケース2'].values[0]
    ax.bar(x+width1/2.0+offset*3, y2, width1, align='center', color=config.COL_SILVER_MED)
    text = '%d' % (int(y2))
    ax.text(x+width1/2.0+offset*3+textoffset, y2 + ymax*0.01, text, ha='center', fontsize=fs, color=config.COL_SILVER_MED)
    y2 = df_occto[df_occto['Year']==2050]['需要電力量_送電端_モデルケース3'].values[0]
    ax.bar(x+width1/2.0+offset*2, y2, width1, align='center', color=config.COL_SILVER_MED)
    text = '%d' % (int(y2))
    ax.text(x+width1/2.0+offset*2+textoffset, y2 + ymax*0.01, text, ha='center', fontsize=fs, color=config.COL_SILVER_MED)
    y2 = df_occto[df_occto['Year']==2050]['需要電力量_送電端_モデルケース4'].values[0]
    ax.bar(x+width1/2.0+offset, y2, width1, align='center', color=config.COL_SILVER_MED)
    text = '%d' % (int(y2))
    ax.text(x+width1/2.0+offset+textoffset, y2 + ymax*0.01, text, ha='center', fontsize=fs, color=config.COL_SILVER_MED)

    categories = ['2013', '2023', '2030', '2035', '2040', '2050']
    x = np.array([2013, 2023, 2030, 2035, 2040, 2050])
    tx = (XMAX-XMIN) * (x - YEAR1) / (YEAR2 - YEAR1)
    ax.set_xticks(tx+width1/2)
    ax.set_xticklabels(categories)

    # legends
    #x1 = xmin_disp + (xmax_disp - xmin_disp) * 0.025
    #x2 = xmin_disp + (xmax_disp - xmin_disp) * 0.09
    #x3 = xmin_disp + (xmax_disp - xmin_disp) * 0.1
    #for i in range(len(ids_to_plot)):
    #    y1 = (0.85 + i * 0.035) * ymax
    #    y2 = y1 + 0.01 * ymax
    #    xpos = np.array([x1, x2])
    #    ypos = np.array([y2, y2])
    #    ax.plot(xpos, ypos, '-', linewidth=5, color=colors[i])
    #    ax.text(x3, y1, labels[i], ha='left')

    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT)


if __name__ == '__main__':
    df1, df2, df_occto = load_data()
    plot(df1, df2, df_occto)

