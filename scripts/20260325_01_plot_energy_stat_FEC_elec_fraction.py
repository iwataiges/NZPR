# 20260325
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import pandas as pd
import json
import config

rcParams['font.size'] = 24
rcParams['axes.labelsize'] = 24
rcParams['xtick.labelsize'] = 20
rcParams['ytick.labelsize'] = 20
#rcParams['lines.markersize'] = 10
rcParams['lines.linewidth'] = 3
rcParams['font.family'] = 'Hiragino Sans'

jsonfile1 = 'outputs/20251201_21_energy_stat/20251201_21_energy_stat_data_common_0_電力.json'
jsonfile2 = 'outputs/20251201_21_energy_stat/20251201_21_energy_stat_data_common_3_エネルギー利用.json'
OUTPUT_PLOT = 'charts/20260325_01_plot_energy_stat_FEC_elec_fraction.png'

list_ids = [
    '#500000', # FEC
    '#600100', # 産業
    '#611000', # 農林水産業
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
n_ids = len(list_ids)

list_subcatlabel = [
    'FEC (全体)',
    '産業',
    '農林水産',
    '建設',
    '製造',
    '(繊維)',
    '(パルプ･紙)',
    '(化学)',
    '(窯業･土石)',
    '(鉄鋼)',
    '(機械)',
    '業務他',
    '家庭',
    '運輸',
    '(旅客)', 
    '(貨物)',
]


list_ids_plot = [0, 1, 11, 12, 13]

def load_data():
    dict1_dtype = {
        'id': str,
        'item_name_jp': str,
        'level': int,
        'n_sub': int,
        'unit': str,
        '2010': float,
        '2011': float,
        '2012': float,
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
    df1 = pd.read_json(jsonfile1, orient='index', dtype=dict1_dtype)
    df2 = pd.read_json(jsonfile2, orient='index', dtype=dict1_dtype)

    return df1, df2

def plot(df1, df2):

    fig, ax = plt.subplots(figsize=(15,10))
    xstep = 0.8
    tx = 0.0
    width = 0.4
    
    fs1 = 20
    fs3 = 24

    for id in list_ids_plot:
        df1_sel = df1[df1['id']==list_ids[id]]
        e_elec = df1_sel['2023'].values[0]

        df2_sel = df2[df2['id']==list_ids[id]]
        e_FEC = df2_sel['2023'].values[0]
        frac_elec = e_elec / e_FEC

        ax.bar(tx, frac_elec, width, bottom=0.0, align='center', color=config.COL_CARROT_MED)
        ax.bar(tx, 1.0-frac_elec, width, bottom=frac_elec, align='center', color=config.COL_ASBESTOS_MED)

        text = '%2d%%' % (int(frac_elec*100.0+0.5))
        if frac_elec > 0.2:
            ax.text(tx, frac_elec/2.0, text, fontsize=fs1, color=config.COL_SILVER_LIGHT, ha='center', va='center', weight='bold')
        else:
            ax.text(tx, frac_elec+0.02, text, fontsize=fs1, color=config.COL_SILVER_LIGHT, ha='center', va='center', weight='bold')
        
        ax.text(tx, -0.02, list_subcatlabel[id], fontsize=fs1, ha='center', va='top')
        tx += xstep

    ax.text((len(list_ids_plot)-1)*xstep/2.0, 1.05, '2023年度', fontsize=fs3, ha='center', va='center', weight='bold')

    #ax.axis('off')
    plt.gca().spines['bottom'].set_visible(True)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT)


if __name__ == '__main__':
    df1, df2 = load_data()
    plot(df1, df2)
