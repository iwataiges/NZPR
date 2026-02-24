# 20251203 / 1205
# 20260116 with 2040 技術進展シナリオ
# -*- coding: utf-8 -*-
import json
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

def plot(df1):
    df1_net_subset = df1[list_year1n] # 2014-2023
    df1_emissions = df1[df1['id'] != '06'] # exclude LULUCF
    df1_emissions_subset = df1_emissions[list_year1]

    fig, ax = plt.subplots(figsize=(12, 8))

    lw1 = 3
    lw2 = 2
    lw3 = 1.5

    ymin = 0.0
    ymax = 1420.0
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

#    ## fitted (2019 - 2023)
#    a = -23.55143006
#    b = 1262.4170493
#
#    YEAR2_START = 2019
#    YEAR2_END   = 2051
#    tx = np.array([YEAR2_START, YEAR2_END])
#    y1 = a*(YEAR2_START - YEAR_BASE) + b
#    y2 = a*(YEAR2_END   - YEAR_BASE) + b
#    ty = np.array([y1, y2])
#
#    ax.plot(tx, ty, '--', color=config.COL_POMEGRANATE_DARK, linewidth=lw2)

#    ## fitted (2015 - 2023, excl. 2020)
#    a = -27.66004534
#    b = 1304.26403815
#
#    YEAR2_START = 2015
#    YEAR2_END   = 2051
#    YEAR_BASE = 2013
#    tx = np.array([YEAR2_START, YEAR2_END])
#    y1 = a*(YEAR2_START - YEAR_BASE) + b
#    y2 = a*(YEAR2_END   - YEAR_BASE) + b
#    ty = np.array([y1, y2])
#
#    ax.plot(tx, ty, '-.', color=config.COL_POMEGRANATE_MED, linewidth=lw2)

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

    # Put Gas Type
    ax.text(2048.5, ymax - (ymax-ymin)*0.07, 'GHG', color=config.COL_ASBESTOS_DARK, fontsize=24)

    #ax.set_title('CO2 (energy-related)')
    ax.set_ylabel('MtCO2e')
    #ax.legend(loc='lower left')
    plt.tight_layout()
    #plt.show()
    plt.savefig('charts/20260122_06_plot_GHG_total.png')

if __name__ == '__main__':
    df_ghgi = load_GHGI_data()
    plot(df_ghgi)
