# -*- coding: utf-8 -*-
# 20251203 / 1205
# 20260116 with 2040 技術進展シナリオ
# 20260520 vashold 2023
import json
import csv
#import openpyxl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import config 

rcParams['font.size'] = 18
rcParams['axes.labelsize'] = 18
rcParams['xtick.labelsize'] = 18
rcParams['ytick.labelsize'] = 18
#rcParams['lines.markersize'] = 10
rcParams['lines.linewidth'] = 3
rcParams['font.family'] = 'Hiragino Sans'
rcParams['xtick.labelsize'] = 'small'
rcParams['ytick.labelsize'] = 'small'

YEAR1_START = 2010
YEAR1_END   = 2024
list_year1 = []
for i in range(YEAR1_START, YEAR1_END):
    list_year1.append('%d' % (i))

YEAR1N_START = 2014
YEAR1N_END   = 2024
list_year1n = []
for i in range(YEAR1N_START, YEAR1N_END):
    list_year1n.append('%d' % (i))

YEAR3_START = 2019
YEAR3_END   = 2050

def load_GHGI_data():
    input_json_file = 'outputs/20251201_31_GHGI/20251205_32_GHGI_ghg_toplevel.json'
    dict_dtype = {
        'id': str,
        'label': str,
        'item_name_jp': str,
        'level': int,
        'n_sub': int,
        'unit': str,
    }
    df1 = pd.read_json(input_json_file, orient='index', dtype=dict_dtype)
    return df1

def load_vashold_2023_data():
    input_csv_file = 'inputs/ref/vashold2023/japan_total_emissions_1980_2050.csv'
    dict_dtype = {
        'year': int,
        'total_emissions_MtCO2eq': float,
        'q5_MtCO2eq': float,
        'q16_MtCO2eq': float,
        'q84_MtCO2eq': float,
        'q95_MtCO2eq': float,
    }
    df2 = pd.read_csv(input_csv_file, dtype=dict_dtype)
    return df2

def plot(df1, df2):
    df1_net_subset = df1[list_year1n] # 2014-2023
    df1_emissions = df1[df1['id'] != '06'] # exclude LULUCF
    df1_emissions_subset = df1_emissions[list_year1]

    df2_subset = df2[(df2['year'] >= YEAR3_START) & (df2['year'] <= YEAR3_END)]
    
    fig, ax = plt.subplots(figsize=(12, 8))

    lw1 = 3
    lw2 = 2
    lw3 = 1.5

    ymin = 0.0
#    ymax = 1420.0
    ymax = 1620.0
    ax.set_ylim(ymin, ymax)

    # GHG gross emissions
    tx = np.arange(YEAR1_START, YEAR1_END)
    ty = df1_emissions_subset.sum().values
    ty = ty*1.0e-3 # to MtCO2e

    ax.plot(tx, ty, 'o-', color=config.COL_MIDNIGHT_BLUE_LIGHT, linewidth=lw1)

    # Linear to NZ2050 from 2013
    ghg_2013 = 1407.0
    tx = np.array([2013, 2050])
    ty = np.array([ghg_2013, 0.0])
    ax.plot(tx, ty, '-', color=config.COL_MIDNIGHT_BLUE_LIGHT, linewidth=lw3)

    # GHG net emissions
    tx = np.arange(YEAR1N_START, YEAR1N_END)
    ty = df1_net_subset.sum().values
    ty = ty*1.0e-3 # to MtCO2e

    ax.plot(tx, ty, 'o-', color=config.COL_MIDNIGHT_BLUE_MED, linewidth=lw1)


    # Linear fit (2014 - 2023)
    YEAR_BASE = 2013
    df1_net_ex2020 = df1_net_subset.drop(columns=['2020'])
    ty = df1_net_ex2020.sum().values
    ty = ty*1.0e-3 # to MtCO2e
    tx = np.array([2014, 2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023])
    tx = tx - YEAR_BASE

    fit1 = np.polyfit(tx, ty, 1)
    a = fit1[0]
    b = fit1[1]
    print('%d-%d %f %f' % (YEAR1N_START, YEAR1N_END, a, b))
    
    YEAR2_START = 2014
    YEAR2_END   = 2051
    tx = np.array([YEAR2_START, YEAR2_END])
    y1 = a*(YEAR2_START - YEAR_BASE) + b
    y2 = a*(YEAR2_END   - YEAR_BASE) + b
    ty = np.array([y1, y2])
    ax.plot(tx, ty, '-.', color=config.COL_POMEGRANATE_MED, linewidth=lw2)

    # Linear fit (2019 - 2023)
    FIT_YEAR_START = 2019
    FIT_YEAR_END   = 2024
    list_fit_year = []
    for i in range(FIT_YEAR_START, FIT_YEAR_END):
        list_fit_year.append('%d' % (i))

    tx = np.arange(FIT_YEAR_START, FIT_YEAR_END)
    tx = tx - YEAR_BASE
    df1_net_subset2 = df1_net_subset[list_fit_year]
    ty = df1_net_subset2.sum().values
    ty = ty*1.0e-3 # to MtCO2e
    fit2 = np.polyfit(tx, ty, 1)
    a = fit2[0]
    b = fit2[1]
    print('%d-%d %f %f' % (FIT_YEAR_START, FIT_YEAR_END, a, b))
        
    tx = np.array([FIT_YEAR_START, YEAR2_END])
    y1 = a*(FIT_YEAR_START - YEAR_BASE) + b
    y2 = a*(YEAR2_END   - YEAR_BASE) + b
    ty = np.array([y1, y2])
    ax.plot(tx, ty, '--', color=config.COL_POMEGRANATE_DARK, linewidth=lw2)


    # 2013 baseline
    tx = 2013
    ty = ghg_2013
    ax.plot(tx, ty, 's', color=config.COL_ALIZARIN_LIGHT, markersize=10)
    # 2030 NDC
    tx = np.array([2030, 2030])
    ty = np.array([760.0, 704.0])
    ax.plot(tx, ty, 'o-', color=config.COL_ALIZARIN_MED, markersize=10)
    # 2035 NDC
    px = 2035
    py = ghg_2013*0.4
    ax.plot(px, py, 'o', color=config.COL_ALIZARIN_MED, markersize=10)
    # 2040 NDC
    px = 2040
    py = ghg_2013*0.27
    ax.plot(px, py, 'o', color=config.COL_ALIZARIN_MED, markersize=10)

    # 2040 技術進展シナリオ
    px = 2040
    py = ghg_2013*0.394
    ax.plot(px, py, '^', color=config.COL_ALIZARIN_DARK, markersize=10)


    # Vashold 2023
    ## calculate offset in 2019
    vashold_2019 = df2[df2['year'] == 2019]['total_emissions_MtCO2eq'].values[0]
    df1_net_subset_2019 = df1_net_subset['2019'].sum()*1.0e-3 # to MtCO2e
    yoffset = df1_net_subset_2019 - vashold_2019

    tx = df2_subset['year'].values
    ty1_low = df2_subset['q5_MtCO2eq'].values + yoffset
    ty1_hgh = df2_subset['q95_MtCO2eq'].values + yoffset
    ax.fill_between(tx, ty1_low, ty1_hgh, color=config.COL_AMETHYST_LIGHT, alpha=0.5, label='Vashold 2023 90%% range')
    ty2_low = df2_subset['q16_MtCO2eq'].values + yoffset
    ty2_hgh = df2_subset['q84_MtCO2eq'].values + yoffset
    ax.fill_between(tx, ty2_low, ty2_hgh, color=config.COL_AMETHYST_MED, alpha=0.5, label='Vashold 2023 68%% range')
    ty3 = df2_subset['total_emissions_MtCO2eq'].values + yoffset
    ax.plot(tx, ty3, '-', color=config.COL_AMETHYST_DARK, linewidth=lw3, label='Vashold 2023')

    # Put Gas Type
    ax.text(YEAR1_START, ymax - (ymax-ymin)*0.07, 'GHG', color=config.COL_ASBESTOS_DARK, fontsize=24)

    #ax.set_title('CO2 (energy-related)')
    ax.set_ylabel('MtCO2e')
    #ax.legend(loc='lower left')
    plt.tight_layout()
    #plt.show()
    plt.savefig('charts/20260520_01_plot_GHG_total_w_vashold2023.png')

if __name__ == '__main__':
    df_ghgi = load_GHGI_data()
    df_vashold2023 = load_vashold_2023_data()
    plot(df_ghgi, df_vashold2023)
