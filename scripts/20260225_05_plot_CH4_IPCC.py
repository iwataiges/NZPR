# 20251212, 20260225
# -*- coding: utf-8 -*-
import json
import openpyxl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import config 

IPCC_EXCEL_FILE = 'inputs/IPCC/data_syr_spm5_all_panels.xlsx'
GHGI_JSON_FILE  = 'outputs/20251201_31_GHGI/20251205_32_GHGI_ghg_toplevel.json'

YEAR1N_START = 2014
YEAR1N_END   = 2024

rcParams['font.size'] = 18
rcParams['axes.labelsize'] = 18
rcParams['xtick.labelsize'] = 18
rcParams['ytick.labelsize'] = 18
#rcParams['lines.markersize'] = 10
rcParams['lines.linewidth'] = 3
rcParams['font.family'] = 'Hiragino Sans'
rcParams['xtick.labelsize'] = 'small'
rcParams['ytick.labelsize'] = 'small'


def load_IPCC_data():
    wb = openpyxl.load_workbook(IPCC_EXCEL_FILE, data_only=True)
    sheet = wb['panel_c']
    data = sheet.values
    cols = next(data)
    data = list(data)
    df_ipcc = pd.DataFrame(data, columns=cols)
    df_C1 = df_ipcc[['methane (CH4)_C1_q0.05_q0.95_range_x', 'methane (CH4)_C1_q0.05_q0.95_range_low_y', 'methane (CH4)_C1_q0.05_q0.95_range_high_y', 'methane (CH4)_C1_q0.05_q0.95_median_y']]
    df_C1.dropna(inplace=True)

    df_C3 = df_ipcc[['methane (CH4)_C3_q0.05_q0.95_range_x', 'methane (CH4)_C3_q0.05_q0.95_range_low_y', 'methane (CH4)_C3_q0.05_q0.95_range_high_y', 'methane (CH4)_C3_q0.05_q0.95_median_y']]
    df_C3.dropna(inplace=True)

    return df_C1, df_C3

def load_GHGI_data():
    dict_dtype = {
        'id': str,
        'label': str,
        'item_name_jp': str,
        'level': int,
        'n_sub': int,
        'unit': str,
    }
    df1 = pd.read_json(GHGI_JSON_FILE, orient='index', dtype=dict_dtype)
    return df1

# GHGI CH4 emissions
def get_GHGI_subset_CH4(df_ghgi):
    list_year1n = []
    df1 = df_ghgi[(df_ghgi['id']=='03')]
    for i in range(YEAR1N_START, YEAR1N_END):
        list_year1n.append('%d' % (i))
    df_ghgi_ch4 = df1[list_year1n] # 2014-2023
    return df_ghgi_ch4

def plot(df_ghgi_ch4, df_C1, df_C3):
    fig, ax = plt.subplots(figsize=(12, 8))

    lw1 = 3
    lw2 = 2
    lw3 = 1.5

    ymin = 0.0
    ymax = 37.0
    ax.set_ylim(ymin, ymax)
    xmin = 2012.5
    xmax = 2051
    ax.set_xlim(xmin, xmax)

    ch4_ghgi2019 = df_ghgi_ch4['2019'].values[0]*1.0e-3

    # CH4 GHGI
    tx = np.arange(YEAR1N_START, YEAR1N_END)
    ty = df_ghgi_ch4.sum().values
    ty = ty*1.0e-3 # to MtCO2e
    ax.plot(tx, ty, 'o-', color=config.COL_MIDNIGHT_BLUE_MED, linewidth=lw1)

    ## fitted (2019 - 2023)
    a = -0.31787239
    b = 32.6578949

    YEAR1_START = 2019
    YEAR1_END   = 2050
    YEAR_BASE = 2013
    tx = np.array([YEAR1_START, YEAR1_END])
    y1 = a*(YEAR1_START - YEAR_BASE) + b
    y2 = a*(YEAR1_END   - YEAR_BASE) + b
    ty = np.array([y1, y2])
    ax.plot(tx, ty, '--', color=config.COL_POMEGRANATE_DARK, linewidth=lw2)

    ## fitted (2014 - 2023, excl. 2020)
    a = -0.28798915 
    b = 32.43185503

    YEAR2_START = 2014
    YEAR2_END   = 2050
    tx = np.array([YEAR2_START, YEAR2_END])
    y1 = a*(YEAR2_START - YEAR_BASE) + b
    y2 = a*(YEAR2_END   - YEAR_BASE) + b
    ty = np.array([y1, y2])
    ax.plot(tx, ty, '-.', color=config.COL_POMEGRANATE_MED, linewidth=lw2)

    # IPCC
    # IPCC C1 2019 (interpolation by 2015 and 2020)
    ch4_c1_2015 = df_C1['methane (CH4)_C1_q0.05_q0.95_median_y'].values[0]
    ch4_c1_2020 = df_C1['methane (CH4)_C1_q0.05_q0.95_median_y'].values[1]
    ch4_c1_2019 = 0.2*ch4_c1_2015 + 0.8*ch4_c1_2020

    tx = df_C3['methane (CH4)_C3_q0.05_q0.95_range_x'].values
    ty_low = df_C3['methane (CH4)_C3_q0.05_q0.95_range_low_y'].values / ch4_c1_2019 * ch4_ghgi2019
    ty_med = df_C3['methane (CH4)_C3_q0.05_q0.95_median_y'].values / ch4_c1_2019 * ch4_ghgi2019
    ty_high = df_C3['methane (CH4)_C3_q0.05_q0.95_range_high_y'].values / ch4_c1_2019 * ch4_ghgi2019
    ax.fill_between(tx, ty_low, ty_high, color=config.COL_NEPHRITIS_LIGHT, alpha=0.5, label='IPCC AR6 C3 range')
    ax.plot(tx, ty_med, '-', color=config.COL_NEPHRITIS_MED, linewidth=lw2, label='IPCC AR6 C3 median')

    tx = df_C1['methane (CH4)_C1_q0.05_q0.95_range_x'].values
    ty_low = df_C1['methane (CH4)_C1_q0.05_q0.95_range_low_y'].values / ch4_c1_2019 * ch4_ghgi2019
    ty_med = df_C1['methane (CH4)_C1_q0.05_q0.95_median_y'].values / ch4_c1_2019 * ch4_ghgi2019
    ty_high = df_C1['methane (CH4)_C1_q0.05_q0.95_range_high_y'].values / ch4_c1_2019 * ch4_ghgi2019
    ax.fill_between(tx, ty_low, ty_high, color=config.COL_PETER_RIVER_LIGHT, alpha=0.5, label='IPCC AR6 C1 range')
    ax.plot(tx, ty_med, '-', color=config.COL_PETER_RIVER_MED, linewidth=lw2, label='IPCC AR6 C1 median')

    print('IPCC C1 2019 (interpolated): %f' % (ch4_c1_2019))
    print('GHGI 2019: %f' % (ch4_ghgi2019))

    # 2030 Plan for Global Warming Countermeasures
    px = 2030
    py = 29.1
    ax.plot(px, py, 'o', color=config.COL_ALIZARIN_MED, markersize=10)

    # 2040 Plan for Global Warming Countermeasures
    px = 2040
    py = 25.0
    ax.plot(px, py, 'o', color=config.COL_ALIZARIN_MED, markersize=10)

    # Put Gas Type
    ax.text(xmax - (xmax-xmin)*0.1, ymax - (ymax-ymin)*0.07, 'CH4', color=config.COL_ASBESTOS_DARK, fontsize=24)

    ax.set_ylabel('MtCO2e')
    plt.tight_layout()
    #plt.show()
    plt.savefig('charts/20260225_05_plot_CH4_IPCC.png')

if __name__ == '__main__':
    df_C1, df_C3 = load_IPCC_data()

    df_ghgi = load_GHGI_data()
    df_ghgi_ch4 = get_GHGI_subset_CH4(df_ghgi)

    plot(df_ghgi_ch4, df_C1, df_C3)

