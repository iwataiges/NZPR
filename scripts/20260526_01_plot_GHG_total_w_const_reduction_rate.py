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

YEAR1_START = 1990
YEAR1_END   = 2024
list_year1 = []
for i in range(YEAR1_START, YEAR1_END):
    list_year1.append('%d' % (i))

YEAR1A_START = 2010
YEAR1A_END   = 2024

YEAR2_START = 2014
YEAR2_END   = 2024

YEAR3_START = 2023
YEAR3_END   = 2051

def load_ghg_toplevel():
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

def calc_ghg_reduction_rate(df1):
    df2 = pd.DataFrame(
        {
            'year': np.arange(YEAR1_START, YEAR1_END),
            '01_01': df1[df1['id'] == '01_01'][list_year1].values[0],
            '01_02': df1[df1['id'] == '01_02'][list_year1].values[0],
            '03': df1[df1['id'] == '03'][list_year1].values[0],
            '04': df1[df1['id'] == '04'][list_year1].values[0],
            '05': df1[df1['id'] == '05'][list_year1].values[0],
            '06': df1[df1['id'] == '06'][list_year1].values[0],
        }
    )

    ids_emissions = ['01_01', '01_02', '03', '04', '05']
    df2['emissions'] = df2[ids_emissions].sum(axis=1)
    df2['reduction_rate'] = np.zeros(len(df2))

    for i in range(YEAR1_START, YEAR1_END-1):
        v1 = df2[df2['year'] == i]['emissions'].values[0]
        v2 = df2[df2['year'] == i+1]['emissions'].values[0]
        df2.loc[df2['year'] == i+1, 'reduction_rate'] = (v2 - v1) / v1

    years_to_average = [2014, 2015, 2016, 2017, 2018, 2019, 2022, 2023]
    reduction_rate_avg = df2[df2['year'].isin(years_to_average)]['reduction_rate'].mean()
    print('reduction_rate_avg: %f' % (reduction_rate_avg))

    return df2, reduction_rate_avg

def set_future_emissions(df2, reduction_rate_avg):
    years = np.arange(YEAR3_START, YEAR3_END)

    df3 = pd.DataFrame(
        {
            'year': years,
            'emissions': np.zeros(len(years))
        }
    )

    v0 = df2[df2['year'] == YEAR3_START]['emissions'].values[0]
    df3.loc[df3['year'] == YEAR3_START, 'emissions'] = v0

    for i in range(YEAR3_START+1, YEAR3_END):
        df3.loc[df3['year'] == i, 'emissions'] = df3[df3['year'] == i-1]['emissions'].values[0] * (1.0 + reduction_rate_avg)

    return df3

def plot(df2, df3):

    df2_subset = df2[(df2['year'] >= YEAR2_START) & (df2['year'] < YEAR2_END)]
    df2_subset['net'] = df2_subset['emissions'] + df2_subset['06']

    fig, ax = plt.subplots(figsize=(14, 8))

    lw1 = 3
    lw2 = 2
    lw3 = 1.5

    ymin = 0.0
    ymax = 1420.0
    ax.set_ylim(ymin, ymax)
    ax.set_xticks(np.arange(YEAR1_START, YEAR3_END, 10))

    # GHG gross emissions
    df2a = df2[df2['year'] >= YEAR1A_START]
    tx = df2a['year']
    ty = df2a['emissions']*1.0e-3 # to MtCO2e

    ax.plot(tx, ty, 'o-', color=config.COL_MIDNIGHT_BLUE_LIGHT, linewidth=lw1)

    # Linear extrapolation from 2013
    ghg_2013 = 1407.0
    tx = np.array([2013, 2050])
    ty = np.array([ghg_2013, 0.0])
    ax.plot(tx, ty, '-', color=config.COL_MIDNIGHT_BLUE_LIGHT, linewidth=lw3)

    # GHG net emissions
    tx = df2_subset['year']
    ty = df2_subset['net']*1.0e-3 # to MtCO2e
    ax.plot(tx, ty, 'o-', color=config.COL_MIDNIGHT_BLUE_MED, linewidth=lw1)

    yoffset = df2[df2['year'] == 2023]['06'].values[0]*1.0e-3 # to MtCO2e
    tx = df3['year']
    ty = df3['emissions']*1.0e-3  + yoffset
    ax.plot(tx, ty, '-', color=config.COL_PETER_RIVER_MED, linewidth=lw1)

    ## fitted (2019 - 2023)
    a = -23.55143006
    b = 1262.4170493

    YEAR_BASE = 2013
    tx = np.array([2019, 2050])
    y1 = a*(2019 - YEAR_BASE) + b
    y2 = a*(2050 - YEAR_BASE) + b
    ty = np.array([y1, y2])

    ax.plot(tx, ty, '--', color=config.COL_POMEGRANATE_DARK, linewidth=lw2)

    ## fitted (2015 - 2023, excl. 2020)
    a = -27.66004534
    b = 1304.26403815

    tx = np.array([2015, 2050])
    y1 = a*(2015 - YEAR_BASE) + b
    y2 = a*(2050 - YEAR_BASE) + b
    ty = np.array([y1, y2])

    ax.plot(tx, ty, '-.', color=config.COL_POMEGRANATE_MED, linewidth=lw2)

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
    ax.text(2048, ymax - (ymax-ymin)*0.07, 'GHG', color=config.COL_ASBESTOS_DARK, fontsize=24)

    #ax.set_title('CO2 (energy-related)')
    ax.set_ylabel('MtCO2e')
    #ax.legend(loc='lower left')
    plt.tight_layout()
    #plt.show()
    plt.savefig('charts/20260526_01_GHG_total_w_const_reduction_rate.png')

    return

if __name__ == '__main__':
    df1 = load_ghg_toplevel()
    df2, reduction_rate_avg = calc_ghg_reduction_rate(df1)
    df3 = set_future_emissions(df2, reduction_rate_avg)
    plot(df2, df3)