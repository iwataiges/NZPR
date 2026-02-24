# 20251208
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
    sheet = wb['panel_a']
    data = sheet.values
    cols = next(data)
    data = list(data)
    df_ipcc = pd.DataFrame(data, columns=cols)
    df_C1 = df_ipcc[['Kyoto gases (GHG)_C1_q0.05_q0.95_range_x','Kyoto gases (GHG)_C1_q0.05_q0.95_range_low_y','Kyoto gases (GHG)_C1_q0.05_q0.95_range_high_y','Kyoto gases (GHG)_C1_q0.05_q0.95_median_y']]
    df_C1.dropna(inplace=True)

    df_C3 = df_ipcc[['Kyoto gases (GHG)_C3_q0.05_q0.95_range_x', 'Kyoto gases (GHG)_C3_q0.05_q0.95_range_low_y','Kyoto gases (GHG)_C3_q0.05_q0.95_range_high_y','Kyoto gases (GHG)_C3_q0.05_q0.95_median_y']]
    df_C3.dropna(inplace=True)

    df_IPCC2019 = df_ipcc[['GHG_observation_uncertainty_2019_whisker_value']]
    df_IPCC2019.dropna(inplace=True)

    return df_C1, df_C3, df_IPCC2019

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

# GHGI net emissions
def get_GHGI_subset_net(df_ghgi):
    list_year1n = []
    for i in range(YEAR1N_START, YEAR1N_END):
        list_year1n.append('%d' % (i))
    df_ghgi_subset = df_ghgi[list_year1n] # 2014-2023
    return df_ghgi_subset

def plot(df_ghgi_subset, df_C1, df_C3, ghg_ipcc2019):
    fig, ax = plt.subplots(figsize=(12, 8))

    lw1 = 3
    lw2 = 2
    lw3 = 1.5

    ymin = 0.0
    ymax = 1420.0
    ax.set_ylim(ymin, ymax)
    xmin = 2012.5
    xmax = 2051
    ax.set_xlim(xmin, xmax)

    # Linear extrapolation from 2013
    ghg_2013 = 1407.0
    tx = np.array([2013, 2050])
    ty = np.array([ghg_2013, 0.0])
    ax.plot(tx, ty, '-', color=config.COL_MIDNIGHT_BLUE_LIGHT, linewidth=lw3)

    ghgi2019 = df_ghgi_subset['2019'].sum()*1.0e-3

    # GHG net emissions
    tx = np.arange(YEAR1N_START, YEAR1N_END)
    ty = df_ghgi_subset.sum().values
    ty = ty*1.0e-3 # to MtCO2e
    ax.plot(tx, ty, 'o-', color=config.COL_MIDNIGHT_BLUE_MED, linewidth=lw1)

    # IPCC
    # IPCC C1 2019 (interpolation by 2015 and 2020)
    ghg_c1_2015 = df_C1['Kyoto gases (GHG)_C1_q0.05_q0.95_median_y'].values[0]
    ghg_c1_2020 = df_C1['Kyoto gases (GHG)_C1_q0.05_q0.95_median_y'].values[1]
    ghg_c1_2019 = 0.2*ghg_c1_2015 + 0.8*ghg_c1_2020

    tx = df_C3['Kyoto gases (GHG)_C3_q0.05_q0.95_range_x'].values
    ty_low = df_C3['Kyoto gases (GHG)_C3_q0.05_q0.95_range_low_y'].values / ghg_ipcc2019 * ghgi2019
    ty_med = df_C3['Kyoto gases (GHG)_C3_q0.05_q0.95_median_y'].values / ghg_ipcc2019 * ghgi2019
    ty_high = df_C3['Kyoto gases (GHG)_C3_q0.05_q0.95_range_high_y'].values / ghg_ipcc2019 * ghgi2019
    # cf. use ghg_c1_2019 for normalization
#    ty_med = df_C3['Kyoto gases (GHG)_C3_q0.05_q0.95_median_y'].values / ghg_c1_2019 * ghgi2019
#    ty_low = df_C3['Kyoto gases (GHG)_C3_q0.05_q0.95_range_low_y'].values / ghg_c1_2019 * ghgi2019
#    ty_high = df_C3['Kyoto gases (GHG)_C3_q0.05_q0.95_range_high_y'].values / ghg_c1_2019 * ghgi2019
    ax.fill_between(tx, ty_low, ty_high, color=config.COL_NEPHRITIS_LIGHT, alpha=0.5, label='IPCC AR6 C3 range')
    ax.plot(tx, ty_med, '-', color=config.COL_NEPHRITIS_MED, linewidth=lw2, label='IPCC AR6 C3 median')

    tx = df_C1['Kyoto gases (GHG)_C1_q0.05_q0.95_range_x'].values
    ty_med = df_C1['Kyoto gases (GHG)_C1_q0.05_q0.95_median_y'].values / ghg_ipcc2019 * ghgi2019
    ty_low = df_C1['Kyoto gases (GHG)_C1_q0.05_q0.95_range_low_y'].values / ghg_ipcc2019 * ghgi2019
    ty_high = df_C1['Kyoto gases (GHG)_C1_q0.05_q0.95_range_high_y'].values / ghg_ipcc2019 * ghgi2019
    # cf. use ghg_c1_2019 for normalization
#    ty_med = df_C1['Kyoto gases (GHG)_C1_q0.05_q0.95_median_y'].values / ghg_c1_2019 * ghgi2019
#    ty_low = df_C1['Kyoto gases (GHG)_C1_q0.05_q0.95_range_low_y'].values / ghg_c1_2019 * ghgi2019
#    ty_high = df_C1['Kyoto gases (GHG)_C1_q0.05_q0.95_range_high_y'].values / ghg_c1_2019 * ghgi2019
    ax.fill_between(tx, ty_low, ty_high, color=config.COL_PETER_RIVER_LIGHT, alpha=0.5, label='IPCC AR6 C1 range')
    ax.plot(tx, ty_med, '-', color=config.COL_PETER_RIVER_MED, linewidth=lw2, label='IPCC AR6 C1 median')

    print('IPCC 2019: %f' % (ghg_ipcc2019))
#    print(df_C1['Kyoto gases (GHG)_C1_q0.05_q0.95_median_y'].values / ghg_ipcc2019)
    print('IPCC C1 2019 (interpolated): %f' % (ghg_c1_2019))
    print('GHGI 2019: %f' % (ghgi2019))

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

    # Put Gas Type
    ax.text(xmax - (xmax-xmin)*0.1, ymax - (ymax-ymin)*0.07, 'GHG', color=config.COL_ASBESTOS_DARK, fontsize=24)

    ax.set_ylabel('MtCO2e')
    plt.tight_layout()
    #plt.show()
    plt.savefig('charts/20251208_01_plot_GHG_total_IPCC.png')

if __name__ == '__main__':
    df_C1, df_C3, df_IPCC2019 = load_IPCC_data()
    ghg_ipcc2019 = df_IPCC2019.loc[2][0]

    df_ghgi = load_GHGI_data()
    df_ghgi_subset = get_GHGI_subset_net(df_ghgi)

    plot(df_ghgi_subset, df_C1, df_C3, ghg_ipcc2019)

