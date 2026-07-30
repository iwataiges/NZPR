# 20251218
# 20260226 / 0317
# -*- coding: utf-8 -*-
import json
#import openpyxl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import config 

#rcParams['font.size'] = 16
#rcParams['axes.labelsize'] = 16
#rcParams['xtick.labelsize'] = 16
#rcParams['ytick.labelsize'] = 16
rcParams['font.size'] = 12
rcParams['axes.labelsize'] = 12
rcParams['xtick.labelsize'] = 12
rcParams['ytick.labelsize'] = 12
#rcParams['lines.markersize'] = 10
rcParams['lines.linewidth'] = 3
rcParams['font.family'] = 'Hiragino Sans'
rcParams['xtick.labelsize'] = 'small'
rcParams['ytick.labelsize'] = 'small'


YEAR1_START = 2010
YEAR1_END   = 2024

FIT_YEAR_START = 2014
FIR_YEAR_END   = 2024

#jsonfile1_data = 'outputs/20251201_21_energy_stat/20251201_21_energy_stat_data_common_3_エネルギー利用.json'
#jsonfile2_data = 'outputs/20251201_01_1p5CRM_balance_energy/20251201_11_1p5CRM_balance_energy_data_common_10_エネルギー利用.json'
#jsonfile3_data = 'outputs/20251201_03_1p5CRM_steps_energy/20251201_13_1p5CRM_steps_energy_data_common_10_エネルギー利用.json'
jsonfile1_data = 'outputs/20251218_01_intensity/20260316_32_energy_stat_intensity_data_common_0_電力_RD.json'
jsonfile2_data = 'outputs/20251218_01_intensity/20251218_02_1p5CRM_balance_intensity_data_common_07_電力.json'
jsonfile3_data = 'outputs/20251218_01_intensity/20251218_03_1p5CRM_steps_intensity_data_common_07_電力.json'

list_subcategory = [
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
n_subcategory = len(list_subcategory)

list_subcatlabel = [
    'CO2(電力)',
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

year1_range = np.arange(YEAR1_START, YEAR1_END)

def load_data():
    year1_list = []
    for i in range(YEAR1_START, YEAR1_END):
        year1_list.append('%d' % (i))

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
    df1 = pd.read_json(jsonfile1_data, orient='index', dtype=dict1_dtype)

    dict2_dtype = {
        'id': str,
        'item_name_jp': str,
        'level': int,
        'n_sub': int,
        'unit': str,
        'baseyear': float,
        '2030': float,
        '2040': float,
        '2050': float,
    }
    df2 = pd.read_json(jsonfile2_data, orient='index', dtype=dict2_dtype)
    year2_list = ['baseyear', '2030', '2040', '2050']

    df3 = pd.read_json(jsonfile3_data, orient='index', dtype=dict2_dtype)

    return df1, df2, df3, year1_list, year2_list

def plot(df1, df2, df3, year1_list, year2_list):
    fig, axs = plt.subplots(4, 4, figsize=(13, 12))

    lw1 = 1.5
    lw2 = 1
    ms = 3

    Mt_to_t = 1.0e6

    ymin = 0.0
    ymax = 170.0
    ymin2 = ymin * 3600 * 1.0e-6 # tCO2/TJ to kgCO2/kWh
    ymax2 = ymax * 3600 * 1.0e-6

    for i in range(n_subcategory):
        df1_sub = df1[df1['id']==list_subcategory[i]]
        df2_sub = df2[df2['id']==list_subcategory[i]]
        df3_sub = df3[df3['id']==list_subcategory[i]]

        yp = i // 4
        xp = i % 4
        ax = axs[yp,xp]
        ax.set_ylim(ymin, ymax)

        ax2 = ax.twinx()
        ax2.set(ylim=(ymin2, ymax2))

        tx = year1_range # numpy ndarray
        ty = df1_sub[year1_list].iloc[0] * Mt_to_t # pandas series

        ax.plot(tx, ty, 'o-', color=config.COL_ASBESTOS_MED, linewidth=lw1, markersize=ms)


        list_years = []
        for j in range(FIT_YEAR_START, FIR_YEAR_END):
            list_years.append('%d' % (j))

        df1_subsubset = df1_sub[list_years]
        # exclude 2020
        df1_subsubset = df1_subsubset.drop(columns=['2020'])
        tx = np.array([2014, 2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023])
        tx = tx - 2013
        ty = df1_subsubset.iloc[0] * Mt_to_t

        # fitting
        fit2 = np.polyfit(tx, ty, 1)
        a = fit2[0]
        b = fit2[1]
        tx = np.array([FIT_YEAR_START, 2050])
        ty = a*(tx - 2013) + b
        ax.plot(tx, ty, '-.', color=config.COL_POMEGRANATE_MED, linewidth=lw2)
        ty_2030 = a * (2030 - 2013) + b
        ty_2035 = a * (2035 - 2013) + b
        ty_2040 = a * (2040 - 2013) + b
        print('id:%s a:%.3e b:%.3e 2030:%.3e 2035:%.3e 2040:%.3e' % (list_subcategory[i], a, b, ty_2030, ty_2035, ty_2040))

        # 1.5CRM
        tx = np.array([2017.5, 2030, 2040, 2050])
        ty = df2_sub[year2_list].iloc[0] * Mt_to_t
        ax.plot(tx, ty, 'o-', color=config.COL_TURQUOISE_MED, linewidth=lw1, markersize=ms)

        ty = df3_sub[year2_list].iloc[0] * Mt_to_t
        ax.plot(tx, ty, 'o-', color=config.COL_ORANGE_MED, linewidth=lw1, markersize=ms)

        ax.set_title(list_subcatlabel[i])
        if xp == 0:
            ax.set_ylabel('tCO2/TJ')
            ax2.set_ylabel('kgCO2/kWh')

        if i == 0:
            # 2030 エネルギー需給見通し
            tx = 2030
            ty = 0.253 / 3600 * Mt_to_t # tCO2/MWh -> tCO2/TJ
            ax.plot(tx, ty, 'o-', color=config.COL_ALIZARIN_MED, markersize=ms+1)

            # 2040 エネルギー需給見通し
            tx = np.array([2040, 2040])
            ty = np.array([0, 0.04/3600]) * Mt_to_t
            ax.plot(tx, ty, 'o-', color=config.COL_ALIZARIN_MED, markersize=ms+1)
            
            # 「技術進展シナリオ」
            tx = 2040
            ty = 0.13/3600 * Mt_to_t
            ax.plot(tx, ty, '^', color=config.COL_ALIZARIN_MED, markersize=ms+1)

        #ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        ax.set_yticks(np.arange(ymin, ymax, 50.0))
        minor_ticks = np.arange(ymin, ymax, 25.0)
        ax.set_yticks(minor_ticks, minor=True)

    # do not use the last subplot
    #axs[3,3].axis('off')

    #ax.legend(loc='lower left')
    plt.tight_layout()
    #plt.show()
    plt.savefig('charts/20260730_25_plot_intensity_subcat_elec.png')

if __name__ == '__main__':
    df1, df2, df3, year1_list, year2_list = load_data()
    plot(df1, df2, df3, year1_list, year2_list)
