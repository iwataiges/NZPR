# 20251218 / 1222
# 20260105 / 0226 / 0311 / 0317
# -*- coding: utf-8 -*-
import json
#import openpyxl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import config 

rcParams['font.size'] = 24
rcParams['axes.labelsize'] = 24
rcParams['xtick.labelsize'] = 20
rcParams['ytick.labelsize'] = 20
#rcParams['lines.markersize'] = 10
rcParams['lines.linewidth'] = 3
rcParams['font.family'] = 'Hiragino Sans'


YEAR1_START = 2010
YEAR1_END   = 2024

FIT_YEAR_START = 2014
FIR_YEAR_END   = 2024

jsonfile1_data = 'outputs/20251218_01_intensity/20260316_32_energy_stat_intensity_data_common_3_エネルギー利用_RD.json'
jsonfile2_data = 'outputs/20251218_01_intensity/20251218_02_1p5CRM_balance_intensity_data_common_10_エネルギー利用.json'
jsonfile3_data = 'outputs/20251218_01_intensity/20251218_03_1p5CRM_steps_intensity_data_common_10_エネルギー利用.json'

jsonfile_sep_data = 'outputs/20251218_02_SEP/20260311_02_SEP_numbers.json'

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
    'エネルギー起源CO2',
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

sector_str = [
    'Total', 'Industry', # 0-1
    '', '', '', '', '', '', '', '', '', #  2-10
    'Commercial', # 11
    'Residential', # 12
    'Transport', # 13
    '', '' # 14-15
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

def load_sep_data():
    dict_dtype = {
        'Year': int,
        'Scenario': int,
        'Sector': str,
        'Type': str,
        'Value': float,
        'unit': str
    }
    df = pd.read_json(jsonfile_sep_data, orient='index', dtype=dict_dtype)
    return df

def plot(df1, df2, df3, year1_list, year2_list, df_sep):
    fig, ax = plt.subplots(figsize=(10, 10))

    lw1 = 3
    lw2 = 2
    ms = 8

    Mt_to_t = 1.0e6

#    ymin = 0.0
#    ymax = 1.7e-4
    ymin = 0.0
    ymax = 170.0
    ax.set_ylim(ymin, ymax)

    df1_sub = df1[df1['id']==list_subcategory[0]]
    df2_sub = df2[df2['id']==list_subcategory[0]]
    df3_sub = df3[df3['id']==list_subcategory[0]]

    tx = year1_range # numpy ndarray
    ty = df1_sub[year1_list].iloc[0]*Mt_to_t # pandas series
    ax.plot(tx, ty, 'o-', color=config.COL_ASBESTOS_MED, linewidth=lw1, markersize=ms)

    list_years = []
    for j in range(FIT_YEAR_START, FIR_YEAR_END):
        list_years.append('%d' % (j))
    df1_subsubset = df1_sub[list_years]
    # exclude 2020
    df1_subsubset = df1_subsubset.drop(columns=['2020'])
    tx = np.array([2014, 2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023])
    tx = tx - 2013
    ty = df1_subsubset.iloc[0]*Mt_to_t

    # fitting
    fit2 = np.polyfit(tx, ty, 1)
    a = fit2[0]
    b = fit2[1]
    tx = np.array([FIT_YEAR_START, 2050])
    ty = a*(tx - 2013) + b
    ax.plot(tx, ty, '-.', color=config.COL_POMEGRANATE_MED, linewidth=lw2)

    # 1.5CRM
    tx = np.array([2017.5, 2030, 2040, 2050])
    ty = df2_sub[year2_list].iloc[0]*Mt_to_t
    ax.plot(tx, ty, 'o-', color=config.COL_TURQUOISE_MED, linewidth=lw1, markersize=ms)

    ty = df3_sub[year2_list].iloc[0]*Mt_to_t
    ax.plot(tx, ty, 'o-', color=config.COL_ORANGE_MED, linewidth=lw1, markersize=ms)

    for j in range(6):
        tdx = df_sep[(df_sep['Scenario']==j) & (df_sep['Sector']==sector_str[0]) & (df_sep['Type']=='CO2 Intensity(energy-related)')]
        tx = tdx['Year']
        ty = tdx['Value']*Mt_to_t
        if j < 5:
            marker = 'o'
            col = config.COL_ALIZARIN_MED
        else:
            marker = '^'
            col = config.COL_ALIZARIN_DARK
        ax.plot(tx, ty, marker, color=col, markersize=ms+1)

    xmin = YEAR1_START
    xmax = 2050
    ax.text(xmax - (xmax-xmin)*0.32, ymax - (ymax-ymin)*0.07, 'CO2排出原単位', color=config.COL_ASBESTOS_DARK, fontsize=24)
    ax.text(xmax - (xmax-xmin)*0.3, ymax - (ymax-ymin)*0.11, '(エネルギー起源)', color=config.COL_ASBESTOS_DARK, fontsize=20)
    ax.set_xticks(np.arange(xmin, xmax+1, step=10))

    ax.set_ylabel('tCO2/TJ')
    #ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    #ax.set_yticks(np.arange(ymin, ymax, 5e-5))
    #minor_ticks = np.arange(ymin, ymax, 2.5e-5)
    ax.set_yticks(np.arange(ymin, ymax, 50.0))
    minor_ticks = np.arange(ymin, ymax, 25.0)
    ax.set_yticks(minor_ticks, minor=True)

    #ax.legend(loc='lower left')
    plt.tight_layout()
    #plt.show()
    plt.savefig('charts/20260730_11_plot_intensity_total_energy.png')

if __name__ == '__main__':
    df1, df2, df3, year1_list, year2_list = load_data()
    df_sep = load_sep_data()
    plot(df1, df2, df3, year1_list, year2_list, df_sep)
