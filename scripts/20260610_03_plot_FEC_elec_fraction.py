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

jsonfile3 = 'outputs/20251201_03_1p5CRM_steps_energy/20251201_13_1p5CRM_steps_energy_data_common_07_電力.json'
jsonfile4 = 'outputs/20251201_03_1p5CRM_steps_energy/20251201_13_1p5CRM_steps_energy_data_common_10_エネルギー利用.json'
jsonfile5 = 'outputs/20251201_01_1p5CRM_balance_energy/20251201_11_1p5CRM_balance_energy_data_common_07_電力.json'
jsonfile6 = 'outputs/20251201_01_1p5CRM_balance_energy/20251201_11_1p5CRM_balance_energy_data_common_10_エネルギー利用.json'

OUTPUT_PLOT = 'charts/20260610_03_plot_FEC_elec_fraction.png'

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

def load_data_es():
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

def load_data_1p5CRM():
    dict2_dtype = {
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
    df3 = pd.read_json(jsonfile3, orient='index', dtype=dict2_dtype)
    df4 = pd.read_json(jsonfile4, orient='index', dtype=dict2_dtype)
    df5 = pd.read_json(jsonfile5, orient='index', dtype=dict2_dtype)
    df6 = pd.read_json(jsonfile6, orient='index', dtype=dict2_dtype)

    return df3, df4, df5, df6


def plot(df1, df2, df3, df4, df5, df6):

    fig, ax = plt.subplots(figsize=(20,10))
    xstep = 0.5
    xstep1 = 1.2
    xstep2 = 0.35
    tx = 0.0
    width = 0.3
    
    fs1 = 16
    fs2 = 14
    fs3 = 14
    fs4 = 24
    lw = 1

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
        
        ax.text(tx, 1.1, '2023', fontsize=fs3, ha='center', va='center', weight='bold')

        tx += xstep

        df3_sel = df3[df3['id']==list_ids[id]]
        e_elec_steps2040 = df3_sel['2040'].values[0]

        df4_sel = df4[df4['id']==list_ids[id]]
        e_FEC_steps2040 = df4_sel['2040'].values[0]
        frac_elec_steps2040 = e_elec_steps2040 / e_FEC_steps2040

        df5_sel = df5[df5['id']==list_ids[id]]
        e_elec_balance2040 = df5_sel['2040'].values[0]

        df6_sel = df6[df6['id']==list_ids[id]]
        e_FEC_balance2040 = df6_sel['2040'].values[0]
        frac_elec_balance2040 = e_elec_balance2040 / e_FEC_balance2040

        ax.bar(tx, frac_elec_steps2040, width, bottom=0.0, align='center', color=config.COL_CARROT_MED)
        ax.bar(tx, 1.0-frac_elec_steps2040, width, bottom=frac_elec_steps2040, align='center', color=config.COL_ASBESTOS_MED)

        text = '%2d%%' % (int(frac_elec_steps2040*100.0+0.5))
        if frac_elec_steps2040 > 0.1:
            ax.text(tx, frac_elec_steps2040/2.0, text, fontsize=fs1, color=config.COL_SILVER_LIGHT, ha='center', va='center', weight='bold')
        else:
            ax.text(tx, frac_elec_steps2040+0.02, text, fontsize=fs1, color=config.COL_SILVER_LIGHT, ha='center', va='center', weight='bold')

        ax.bar(tx+xstep2, frac_elec_balance2040, width, bottom=0.0, align='center', color=config.COL_CARROT_MED)
        ax.bar(tx+xstep2, 1.0-frac_elec_balance2040, width, bottom=frac_elec_balance2040, align='center', color=config.COL_ASBESTOS_MED)

        text = '%2d%%' % (int(frac_elec_balance2040*100.0+0.5))
        if frac_elec_balance2040 > 0.1:
            ax.text(tx+xstep2, frac_elec_balance2040/2.0, text, fontsize=fs1, color=config.COL_SILVER_LIGHT, ha='center', va='center', weight='bold')
        else:
            ax.text(tx+xstep2, frac_elec_balance2040+0.02, text, fontsize=fs1, color=config.COL_SILVER_LIGHT, ha='center', va='center', weight='bold')

        ax.text(tx, 1.02, '政府\n目標', fontsize=fs2, ha='center', va='bottom', color=config.COL_ORANGE_MED)
        ax.text(tx+xstep2, 1.02, '1.5C\nRM', fontsize=fs2, ha='center', va='bottom', color=config.COL_TURQUOISE_MED)
        ax.text(tx+xstep2/2, 1.1, '2040', fontsize=fs3, ha='center', va='center', weight='bold')
        px = np.array([tx-width/2,tx+xstep2+width/2])
        py = np.array([1.085, 1.085])
        ax.plot(px, py, '-', linewidth=lw, color='#333')

        ax.text(tx, -0.02, list_subcatlabel[id], fontsize=fs4, ha='center', va='top')
#        ax.text(tx+width/2, -0.05, list_subcatlabel[id], fontsize=fs1, ha='center', va='top')
        tx += xstep1

    #ax.text((len(list_ids_plot)-0.5)*xstep1/2.0, 1.1, '2040年', fontsize=fs3, ha='center', va='center', weight='bold')

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
    df1, df2 = load_data_es()
    df3, df4, df5, df6 = load_data_1p5CRM()
    plot(df1, df2, df3, df4, df5, df6)
