# 20251230
# 20260401
# 20260721 2020-202
# -*- coding: utf-8 -*-
import json
import openpyxl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import config 

INPUT_EXCEL1 = 'inputs/RE/20251230_01_IGESRM_RE_power_for_plot.xlsx'
INPUT_EXCEL2 = 'inputs/energy_stat/20260414_power_energy_stat.xlsx'
OUTPUT_PLOT = 'charts/20260721_02_plot_IGESRM_RE_power.png'

YEAR1N_START = 2020
YEAR1N_END   = 2025

rcParams['font.size'] = 18
rcParams['axes.labelsize'] = 18
rcParams['xtick.labelsize'] = 18
rcParams['ytick.labelsize'] = 18
#rcParams['lines.markersize'] = 10
rcParams['lines.linewidth'] = 3
rcParams['font.family'] = 'Hiragino Sans'
rcParams['xtick.labelsize'] = 'small'
rcParams['ytick.labelsize'] = 'small'


def load_data():
    wb = openpyxl.load_workbook(INPUT_EXCEL1, data_only=True)
    sheet = wb['Sheet1']
    data = sheet.values
    cols = next(data)
    data = list(data)
    df1 = pd.DataFrame(data, columns=cols)
    df1.dropna(subset=['Year'], inplace=True)

    wb = openpyxl.load_workbook(INPUT_EXCEL2, data_only=True)
    sheet = wb['Sheet1']
    data = sheet.values
    cols = next(data)
    data = list(data)
    df2 = pd.DataFrame(data, columns=cols)
    df2.dropna(subset=['Year'], inplace=True)

    return df1, df2


def plot(df1, df2):
    fig, ax = plt.subplots(figsize=(12, 8))

    lw1 = 3
    lw2 = 2
    lw3 = 1.5

    ymin = 0.0
    ymax = 2200.0
    #ymax = 800.0
    ax.set_ylim(ymin, ymax)
    ax.set_yticks([0, 500, 1000, 1500, 2000])
    xmin = 2009
    xmax = 2051
    ax.set_xlim(xmin, xmax)

    tdf1 = df1[df1['Label'] == 'SPS']
    tx = tdf1['Year']
    ty = tdf1['RE']
    ax.plot(tx, ty, 'o-', color=config.COL_ORANGE_MED, linewidth=lw1)

    tdf1 = df1[df1['Label'] == 'balanced-sub']
    tx = tdf1['Year']
    ty = tdf1['RE']
    ax.plot(tx, ty, 'o--', color=config.COL_TURQUOISE_MED, linewidth=lw1)

    tdf1 = df1[df1['Label'] == '1.5CRM']
    tx = tdf1['Year']
    ty = tdf1['RE']
    ax.plot(tx, ty, 'o-', color=config.COL_TURQUOISE_MED, linewidth=lw1)

    # energy stat, fitting
    df2_subset = df2[(df2['Year']>=YEAR1N_START) & (df2['Year']<YEAR1N_END)]
    tx = df2_subset['Year']-2013
    ty = df2_subset['RE']
    fit1 = np.polyfit(tx, ty, 1)
    a = fit1[0]
    b = fit1[1]
    tx = np.array([YEAR1N_START, 2050])
    ty = a*(tx - 2013) + b
    ax.plot(tx, ty, '-.', color=config.COL_POMEGRANATE_MED, linewidth=lw3)
    ty_2030 = a * (2030 - 2013) + b
    ty_2035 = a * (2035 - 2013) + b
    ty_2040 = a * (2040 - 2013) + b
    print('a:%.3e b:%.3e ' % (a, b))
    print('2030:%.1f 2035:%.1f 2040:%.1f' % (ty_2030, ty_2035, ty_2040))

    # energy stat
    tx = df2['Year']
    ty = df2['RE']
    ax.plot(tx, ty, 'o-', color=config.COL_ASBESTOS_MED, linewidth=lw2)


    ax.set_ylabel('TWh/Year')
    plt.tight_layout()
    #plt.show()
    plt.savefig(OUTPUT_PLOT)

if __name__ == '__main__':

    df1, df2 = load_data()
    plot(df1, df2)

