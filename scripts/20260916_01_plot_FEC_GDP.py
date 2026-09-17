# 20260916
# -*- coding: utf-8 -*-
import json
import openpyxl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.ticker import MultipleLocator
#from matplotlib.ticker import AutoMinorLocator, MultipleLocator
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

YEAR_BASE = 2013

jsonfile_FEC = 'outputs/20251201_21_energy_stat/20251201_21_energy_stat_data_common_2_合計.json'
excelfile_GDP = 'inputs/ref/20260520_01_GDP_JP.xlsx'

output_png = 'charts/20260916_01_plot_energy_gdp.png'

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
    'FEC (エネルギー起源)',
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
    df1 = pd.read_json(jsonfile_FEC, orient='index', dtype=dict1_dtype)

    wb = openpyxl.load_workbook(excelfile_GDP, data_only=True)
    sheet = wb['Sheet1']
    data = sheet.values
    cols = next(data)
    data = list(data)
    df2_0 = pd.DataFrame(data, columns=cols)
    df2 = df2_0[(df2_0['Year']>=YEAR1_START) & (df2_0['Year']<YEAR1_END)]

    return df1, df2, year1_list


def plot(df1, df2, year1_list):
    fig, ax = plt.subplots(figsize=(12, 8))

    lw1 = 3
    lw2 = 2
    ms = 4
    ms2 = 8

    ymin = 0.55
    ymax = 1.45
    xmin = 2009
    xmax = 2031
    ax.set(xlim=(xmin,xmax), ylim=(ymin, ymax))

    tx = np.array([xmin, xmax])
    ty = np.array([1.0, 1.0])
    ax.plot(tx, ty, '-', color=config.COL_GREY_MED, linewidth=1)

    ## FEC
    df1_sub = df1[df1['id']==list_subcategory[0]]

    FEC = df1_sub[year1_list].iloc[0]/1.0e6 # pandas series
    FEC_2013 = df1_sub['2013'].iloc[0]/1.0e6
    tx = year1_range # numpy ndarray
    ty = FEC / FEC_2013

    ax.plot(tx, ty, 'o-', color=config.COL_ASBESTOS_MED, linewidth=lw1, markersize=ms)

    list_years = []
    for j in range(FIT_YEAR_START, FIR_YEAR_END):
        list_years.append('%d' % (j))

    df1_subsubset = df1_sub[list_years]
    # exclude 2020
    df1_subsubset = df1_subsubset.drop(columns=['2020'])
    fx = np.array([2014, 2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023])
    fx = fx - YEAR_BASE
    fy = df1_subsubset.iloc[0]/1.0e6

    # fitting
    fit2 = np.polyfit(fx, fy, 1)
    a = fit2[0]
    b = fit2[1]
    lx = np.array([FIT_YEAR_START, 2040])
    ly = (a*(lx - YEAR_BASE) + b) / FEC_2013
    ax.plot(lx, ly, '--', color=config.COL_ASBESTOS_MED, linewidth=lw2)
    ty_2030 = a * (2030 - YEAR_BASE) + b
    print('FEC: a:%.3e b:%.3e 2030:%.2f ' % (a, b, ty_2030))

    ## GDP
    GDP = df2['年度_内閣府GDP (10億円 2020暦年連鎖価格)'].values
    GDP_2013 = df2['年度_内閣府GDP (10億円 2020暦年連鎖価格)'].iloc[3]
    ty = GDP / GDP_2013

    ax.plot(tx, ty, 'o-', color=config.COL_ALIZARIN_MED, linewidth=lw1, markersize=ms)

    # fitting
    fy = np.concatenate([ty[4:10], ty[11:]])
    fit2 = np.polyfit(fx, fy, 1)
    a = fit2[0]
    b = fit2[1]
    lx = np.array([FIT_YEAR_START, 2040])
    ly = a*(lx - YEAR_BASE) + b
    ax.plot(lx, ly, '--', color=config.COL_ALIZARIN_MED, linewidth=lw2)
    ty_2030 = a * (2030 - YEAR_BASE) + b
    print('GDP: a:%.3e b:%.3e 2030:%.2f ' % (a, b, ty_2030))

    ## FEC / GDP
    FEC_GDP = FEC / GDP
    FEC_GDP_2013 = FEC_2013 / GDP_2013
    ty = FEC_GDP / FEC_GDP_2013

    ax.plot(tx, ty, 'o-', color=config.COL_NEPHRITIS_MED, linewidth=lw1, markersize=ms)

    # fitting
    fy = np.concatenate([ty[4:10], ty[11:]])
    fit2 = np.polyfit(fx, fy, 1)
    a = fit2[0]
    b = fit2[1]
    lx = np.array([FIT_YEAR_START, 2040])
    ly = a*(lx - YEAR_BASE) + b
    ax.plot(lx, ly, '--', color=config.COL_NEPHRITIS_MED, linewidth=lw2)
    ty_2030 = a * (2030 - YEAR_BASE) + b
    print('FEC/GDP: a:%.3e b:%.3e 2030:%.2f ' % (a, b, ty_2030))


    # SEP 2030
    FEC_SEP2030 = 10.852800 # EJ
    GDP_SEP2030 = 660000 # billion JPY

    tx = 2030
    ty = FEC_SEP2030 / FEC_2013
    ax.plot(tx, ty, 'o', color=config.COL_ASBESTOS_MED, markersize=ms2)

    ty = GDP_SEP2030 / GDP_2013
    ax.plot(tx, ty, 'o', color=config.COL_ALIZARIN_MED, markersize=ms2)

    ty = (FEC_SEP2030 / GDP_SEP2030) / (FEC_2013 / GDP_2013)
    ax.plot(tx, ty, 'o', color=config.COL_NEPHRITIS_MED, markersize=ms2)

    #ax.set_xticks(np.arange(YEAR1_START, xmax, 5))
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(0.2))
    ax.yaxis.set_minor_locator(MultipleLocator(0.1))
    #ax.legend(loc='lower left')
    plt.tight_layout()
    #plt.show()
    plt.savefig(output_png)


    return 


if __name__ == '__main__':
    df_FEC, df_GDP, year1_list = load_data()

    plot(df_FEC, df_GDP, year1_list)
