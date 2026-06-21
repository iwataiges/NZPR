# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.colors import LinearSegmentedColormap
import openpyxl
import pandas as pd
import config

INPUT_EXCEL1 = 'inputs/RE/20260617_01_RE_japan.xlsx'
OUTPUT_PLOT = 'charts/20260619_02_plot_RE_bars_power_additions_separate.png'

rcParams['font.size'] = 16
rcParams['axes.labelsize'] = 16
rcParams['xtick.labelsize'] = 18
rcParams['ytick.labelsize'] = 18
#rcParams['lines.markersize'] = 10
rcParams['lines.linewidth'] = 5
rcParams['font.family'] = 'Hiragino Sans'
#rcParams['xtick.labelsize'] = 'small'
#rcParams['ytick.labelsize'] = 'small'

colors = [
    config.COL_ORANGE_DARK,
    config.COL_GREEN_DARK,
    config.COL_BLUE_DARK,
    config.COL_BROWN_DARK,
    config.COL_CYAN_DARK,
    config.COL_BLUE_GREY_DARK,
]

def load_data():
    wb = openpyxl.load_workbook(INPUT_EXCEL1, data_only=True)
    sheet = wb['power']
    data = sheet.values
    cols = next(data)
    data = list(data)
    df1 = pd.DataFrame(data, columns=cols)

    return df1

def plot_sub(ax, df1, label, ymax, pos, title):
    xmin = -1
    xmax = 15
    width1 = 0.5
    fs = 14
    fs2 = 24
    year0 = 2011

    ax.set(xlim=(xmin, xmax), ylim=(0, ymax))
    ax.set_ylabel('発電量変化 [TWh/年]')

    ndata1 = df1.index.shape[0]
    textcolour = config.COL_WET_ASPHALT_DARK
    for i in range(ndata1-1):
        year1 = df1.iloc[i]['Year']
        year2 = df1.iloc[i+1]['Year']
        x = year2 - year0
        value1 = df1.iloc[i][label+'_TWh_IRENA']
        value2 = df1.iloc[i+1][label+'_TWh_IRENA']
        diff = value2 - value1
        ax.bar(x+width1/2.0, diff, width1, bottom=0.0, align='center', color=colors[pos])

        text = '%3.1f' % (diff)
        ax.text(x+width1/2.0, diff + ymax*0.01, text, ha='center', fontsize=fs, color=textcolour)

    ax.text(xmin + 0.5, ymax*0.9, title, fontsize=fs2, color=colors[pos], ha='left')

    categories = ['2011', '2013', '2015', '2020', '2023']
    x = np.array([0, 2, 4, 9, 12])
    ax.set_xticks(x+width1/2)
    ax.set_xticklabels(categories)

    if ymax > 5:
        y = np.arange(0, ymax+1, 2)
    else:
        y = np.arange(0, ymax+0.5, 0.5)
    ax.set_yticks(y)

    return

def plot(df1):

    fig, axs = plt.subplots(2,1, figsize=(15, 10))

    plot_sub(axs[0], df1, 'PV', 15, 0, '太陽光')
    plot_sub(axs[1], df1, 'OnSW', 2, 1, '陸上風力')

    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT)

if __name__ == '__main__':
    df1 = load_data()
    plot(df1)
