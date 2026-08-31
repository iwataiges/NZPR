# 20251208
# -*- coding: utf-8 -*-
import json
import openpyxl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import config 

GHGI_JSON_FILE  = 'outputs/20251201_31_GHGI/20251205_32_GHGI_ghg_toplevel.json'
IGESRM_BALNC_GHG_JSON_FILE = 'outputs/20251208_01_1p5CRM_GHG/20251208_04_1p5CRM_balance_GHG_data.json'
IGESRM_STEPS_GHG_JSON_FILE = 'outputs/20251208_01_1p5CRM_GHG/20251208_04_1p5CRM_steps_GHG_data.json'

YEAR1_START = 2010
YEAR1_END   = 2024

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

def load_IGESRM_GHG_data():
    dict_dtype = {
        "Year": int,
        "GHG(森林吸収、DACCS含)": float,
        "CO2(森林吸収、DACCS含)": float,
        "その他GHG":float,
        "森林吸収源":float,
        "DACCS":float,
        "CCS回収分":float
    }
    df2 = pd.read_json(IGESRM_BALNC_GHG_JSON_FILE, orient='index', dtype=dict_dtype)
    df3 = pd.read_json(IGESRM_STEPS_GHG_JSON_FILE, orient='index', dtype=dict_dtype)
    
    return df2, df3

# GHGI net emissions
def get_GHGI_subset_net(df_ghgi):
    list_year1n = []
    for i in range(YEAR1N_START, YEAR1N_END):
        list_year1n.append('%d' % (i))
    df_ghgi_subset = df_ghgi[list_year1n] # 2014-2023
    return df_ghgi_subset

# GHGI gross emissions
def get_GHGI_subset_gross(df_ghgi):
    list_year1 = []
    for i in range(YEAR1_START, YEAR1_END):
        list_year1.append('%d' % (i))
    df_emissions = df_ghgi[df_ghgi['id'] != '06'] # exclude LULUCF
    df_ghgi_subset_gross = df_emissions[list_year1]
    return df_ghgi_subset_gross

def plot(df_ghgi_subset_gross, df_ghgi_subset, df_1p5CRM_balnc, df_1p5CRM_steps):
    fig, ax = plt.subplots(figsize=(12, 8))

    lw1 = 3
    lw2 = 2
    lw3 = 1.5

    ymin = 0.0
    ymax = 1420.0
    ax.set_ylim(ymin, ymax)
#    xmin = 2012.5
    xmin = 2009
    xmax = 2051
    ax.set_xlim(xmin, xmax)

    # Linear extrapolation from 2013
    ghg_2013 = 1407.0
    tx = np.array([2013, 2050])
    ty = np.array([ghg_2013, 0.0])
    ax.plot(tx, ty, '-', color=config.COL_MIDNIGHT_BLUE_LIGHT, linewidth=lw3)

    ghgi2019 = df_ghgi_subset['2019'].sum()*1.0e-3
    ghgi2021 = df_ghgi_subset['2021'].sum()*1.0e-3
    ghgi2022 = df_ghgi_subset['2022'].sum()*1.0e-3
    ghgi2023 = df_ghgi_subset['2023'].sum()*1.0e-3

    # GHG net emissions
    tx = np.arange(YEAR1N_START, YEAR1N_END)
    ty = df_ghgi_subset.sum().values
    ty = ty*1.0e-3 # to MtCO2e
    ax.plot(tx, ty, 'o-', color=config.COL_MIDNIGHT_BLUE_MED, linewidth=lw1)

    # GHG gross emissions
    tx = np.arange(YEAR1_START, YEAR1_END)
    ty = df_ghgi_subset_gross.sum().values
    ty = ty*1.0e-3 # to MtCO2e
    ax.plot(tx, ty, 'o-', color=config.COL_MIDNIGHT_BLUE_LIGHT, linewidth=lw1)

    # 1.5CRM
    tdf = df_1p5CRM_balnc[df_1p5CRM_balnc['Year']>=2023]
#    tdf = df_1p5CRM_balnc[df_1p5CRM_balnc['Year']>=2021]
    tx = tdf['Year'].values
    ty = tdf['GHG(森林吸収、DACCS含)'].to_numpy(copy=True)
    ax.plot(tx, ty, '-', color=config.COL_TURQUOISE_MED, linewidth=lw1, label='1.5CRM Balanced GHG (with forest absorption, DACCS)')

    tdf = df_1p5CRM_steps[df_1p5CRM_steps['Year']>=2023]
#    tdf = df_1p5CRM_steps[df_1p5CRM_steps['Year']>=2021]
    tx = tdf['Year'].values
    ty = tdf['GHG(森林吸収、DACCS含)'].to_numpy(copy=True)
#    ax.plot(tx, ty, '-', color=config.COL_ORANGE_MED, linewidth=lw1, label='1.5CRM Steps GHG (with forest absorption, DACCS)')


    # Linear fit (2014 - 2023)
    YEAR_BASE = 2013
    df_ghgi_net_ex2020 = df_ghgi_subset.drop(columns=['2020'])
    ty = df_ghgi_net_ex2020.sum().values
    ty = ty*1.0e-3 # to MtCO2e
    tx = np.array([2014, 2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023])
    tx = tx - YEAR_BASE

    fit1 = np.polyfit(tx, ty, 1)
    a = fit1[0]
    b = fit1[1]
    print('%d-%d %f %f' % (YEAR1N_START, YEAR1N_END, a, b))
    y_2030 = a * (2030.0 - YEAR_BASE) + b
    y_2040 = a * (2040.0 - YEAR_BASE) + b
    print(' 2030: %6.2f 2040: %6.2f' % (y_2030, y_2040))
        
    YEAR2_START = 2014
    YEAR2_END   = 2051
    tx = np.array([YEAR2_START, YEAR2_END])
    y1 = a*(YEAR2_START - YEAR_BASE) + b
    y2 = a*(YEAR2_END   - YEAR_BASE) + b
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
    ax.text(xmax - (xmax-xmin)*0.1, ymax - (ymax-ymin)*0.07, 'GHG', color=config.COL_ASBESTOS_DARK, fontsize=24)

    ax.set_ylabel('MtCO2e')
    plt.tight_layout()
    #plt.show()
    plt.savefig('charts/20260820_06_plot_GHG_total_1p5CRM.png')

if __name__ == '__main__':
    df_ghgi = load_GHGI_data()
    df_ghgi_subset = get_GHGI_subset_net(df_ghgi)
    df_ghgi_subset_gross = get_GHGI_subset_gross(df_ghgi)
    df_1p5CRM_balnc, df_1p5CRM_steps = load_IGESRM_GHG_data()

    plot(df_ghgi_subset_gross, df_ghgi_subset, df_1p5CRM_balnc, df_1p5CRM_steps)

