# 20251208
# 20260120 日本語
# 20260226 upside down
# -*- coding: utf-8 -*-
import json
import openpyxl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import config 
from matplotlib.ticker import MaxNLocator, MultipleLocator

GHGI_DIFF_JSON_FILE  = 'outputs/20251201_31_GHGI/20251208_02_GHGI_ghg_toplevel_diff.json'

YEAR1_START = 2015
YEAR1_END   = 2024

NDC2030_1 = 760.0
NDC2030_2 = 704.0
GHGI2023  = 1017.245
NDC2013 = 1407
GHG_RM2030 = 606.022
GHG_RM2035 = 340.323

rcParams['font.size'] = 18
rcParams['axes.labelsize'] = 18
rcParams['xtick.labelsize'] = 18
rcParams['ytick.labelsize'] = 18
#rcParams['lines.markersize'] = 10
rcParams['lines.linewidth'] = 3
rcParams['font.family'] = 'Hiragino Sans'
rcParams['xtick.labelsize'] = 'small'
rcParams['ytick.labelsize'] = 'small'


def load_GHGI_diff_data():
    dict_dtype = {
        'id': str,
        'label': str,
        'item_name_jp': str,
        'level': int,
        'n_sub': int,
        'unit': str,
    }

    df_orig = pd.read_json(GHGI_DIFF_JSON_FILE, orient='index', dtype=dict_dtype)

    list_year1 = []
    for i in range(YEAR1_START, YEAR1_END):
        list_year1.append('%d' % (i))
    df = df_orig[list_year1]
    
    return df, list_year1

def get_GHG_diff(df, list_year):
    df_ghg = df[list_year].sum(axis=0)*1.0e-3  # to MtCO2eq
    return df_ghg

def get_average_diff(df_ghg):
    df_subset = df_ghg[['2015','2016','2017','2018','2019','2022','2023']]
    average_diff = df_subset.mean()
    return average_diff

def plot(df_ghg, average):
    fig, ax = plt.subplots(figsize=(12, 8))

    lw1 = 3
    lw2 = 2
    lw3 = 1.5
    fs1 = 16

#    ymin = 0.0
#    ymax = 1420.0
#    ax.set_ylim(ymin, ymax)
    xmin = 2014
    xmax = 2035.5
    ax.set_xlim(xmin, xmax)
    # force integer x-axis
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    # set major and minor ticks
    ax.set_xticks(np.arange(2015, 2036, 5))
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    

    # zero line
    tx = np.array([xmin, xmax])
    ty = np.array([0.0, 0.0])
    ax.plot(tx, ty, '-', color=config.COL_CONCRETE_DARK, linewidth=lw3)

    # GHGI diff bars
    tx = np.array([2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023])
    ty = df_ghg.values
    ax.bar(tx, ty, color=config.COL_PETER_RIVER_MED, width=0.5)

    # 2020 and 2021
    tx = np.array([2020, 2021])
    ty = ty[5:7]
    ax.bar(tx, ty, color=config.COL_PETER_RIVER_LIGHT, width=0.5)

    # average (excl. 2020,2021)
    tx = np.array([xmin, 2023.5])
    ty = np.array([average, average])
    ax.plot(tx, ty, '--', color=config.COL_PETER_RIVER_DARK, linewidth=lw3)
    tx = np.array([2029, xmax])
    ty = np.array([average, average])
    ax.plot(tx, ty, '--', color=config.COL_PETER_RIVER_DARK, linewidth=lw3)
    ax.text(2023.75, average, '平均 %3.1f MtCO2e/年' % (average), color=config.COL_PETER_RIVER_DARK, fontsize=fs1, va='center', ha='left')
    ax.text(2023.75, average-2.5, '(除 2020-2019, 2021-2020)', color=config.COL_PETER_RIVER_DARK, fontsize=fs1-4, va='center', ha='left')

    # average GHG reduction required for NDC 2030
    avg1 = (NDC2030_1 - GHGI2023) / (2030 - 2023)
    avg2 = (NDC2030_2 - GHGI2023) / (2030 - 2023)
    tx = np.array([2024, 2030])
    ty1 = np.array([avg1, avg1])
    ty2 = np.array([avg2, avg2])
    ax.fill_between(tx, ty1, ty2, color=config.COL_ALIZARIN_LIGHT, alpha=0.5)
    ax.text(2027, avg2+0.1, '2030年NDCに必要: \n%3.1f – %3.1f MtCO2e/年' % (avg2, avg1), color=config.COL_ALIZARIN_MED, fontsize=fs1, va='bottom', ha='center')

    # average GHG reduction required for NDC 2035
    ndc2035 = NDC2013 * 0.4
    avg1 = (ndc2035 - GHGI2023) / (2035 - 2023)
    tx = np.array([2024, 2035])
    ty = np.array([avg1, avg1])
    ax.plot(tx, ty, ':', color=config.COL_POMEGRANATE_MED, linewidth=lw2)
    ax.text(2033, avg1+0.1, '2035年NDCに必要: \n%3.1f MtCO2e/年' % (avg1), color=config.COL_ALIZARIN_DARK, fontsize=fs1, va='bottom', ha='center')

    # average GHG reduction required for NDC 2040
#    ndc2040 = NDC2013 * 0.27
#    avg1 = (GHGI2023 - ndc2040) / (2040 - 2023)
#    tx = np.array([2024, 2040])
#    ty = np.array([avg1, avg1])
#    ax.plot(tx, ty, ':', color=config.COL_POMEGRANATE_DARK, linewidth=lw2)

    # average GHG reduction required for 1.5CRM 2030
#    avg1 = (GHGI2023 - GHG_RM2030) / (2030 - 2023)
#    tx = np.array([2024, 2030])
#    ty1 = np.array([avg1, avg1])
#    ax.plot(tx, ty, '--', color=config.COL_NEPHRITIS_MED, linewidth=lw2)
    avg2 = (GHG_RM2035 - GHGI2023) / (2035 - 2023)
    tx = np.array([2024, 2035])
    ty = np.array([avg2, avg2])
    ax.plot(tx, ty, ':', color=config.COL_NEPHRITIS_DARK, linewidth=lw2)
    ax.text(2033, avg2+0.4, '1.5CRM 2035に必要: \n%3.1f MtCO2e/年' % (avg2), color=config.COL_NEPHRITIS_DARK, fontsize=fs1, va='bottom', ha='center')

    ax.set_ylabel('GHG排出削減量 [MtCO2e/年]')
    plt.tight_layout()
    #plt.show()
    plt.savefig('charts/20260226_03_plot_GHG_total_diff.png')


if __name__ == '__main__':
    df, list_year = load_GHGI_diff_data()

    df_ghg = get_GHG_diff(df, list_year)

    average = get_average_diff(df_ghg)
    
    plot(df_ghg, average)