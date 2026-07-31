# 20260730
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import openpyxl
import pandas as pd
from matplotlib import rcParams
import config

INPUT_EXCEL = 'inputs/GHGI/20260319GHGI_co2_fraction.xlsx'
OUTPUT_PLOT = 'charts/20260730_01_plot_bars_GHGI_co2_types.png'

rcParams['font.size'] = 16
rcParams['axes.labelsize'] = 16
rcParams['xtick.labelsize'] = 18
rcParams['ytick.labelsize'] = 18
#rcParams['lines.markersize'] = 10
rcParams['lines.linewidth'] = 5
rcParams['font.family'] = 'Hiragino Sans'
#rcParams['xtick.labelsize'] = 'small'
#rcParams['ytick.labelsize'] = 'small'


labels_to_disp = ['SEP5', 'SEP1', '1.5CRM']
texts_to_disp = ['SEP7:排出上振れ', 'SEP7:再エネ拡大', '1.5℃ RM']
#colors = [config.COL_NEPHRITIS_MED, config.COL_AMETHYST_MED, config.COL_SILVER_MED]
colors = [config.COL_PETER_RIVER_MED, config.COL_CARROT_MED, config.COL_GREEN_SEA_MED]
label_colors = [config.COL_WET_ASPHALT_DARK, config.COL_TURQUOISE_MED, config.COL_ORANGE_MED]

def load_data():
    wb = openpyxl.load_workbook(INPUT_EXCEL, data_only=True)
    sheet = wb['for_plot']
    data = sheet.values
    cols = next(data)
    data = list(data)
    df1 = pd.DataFrame(data, columns=cols)
    df1.dropna(subset=['Year'], inplace=True)
    return df1

def plot(df1):
    ndata1 = df1.index.shape[0]

    fig, ax = plt.subplots(figsize=(15,10))
    ymax = 1300.0
    ymin = -80
    xmin = 2013.5
    xmax = 2023.5
    ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
    ax.set(ylim=(ymin, ymax))
    ax.set_ylabel('MtCO2')

    width1 = 0.4
    fs1 = 14
    fs2 = 16

    tx = np.array([xmin, xmax])
    ty = np.array([0.0, 0.0])
    ax.plot(tx, ty, '-', lw=1, color=config.COL_CONCRETE_LIGHT)

    for i in range(ndata1):
        x = df1.iloc[i]['Year']
        co2_e = df1.iloc[i]['エネ起源']
        co2_ne = df1.iloc[i]['非エネ起源']
        co2_abs = df1.iloc[i]['吸収量']

        if x == 2014:
            co2_e_2014 = co2_e
            co2_ne_2014 = co2_ne
            co2_abs_2014 = co2_abs
        else:
            r_e = co2_e / co2_e_2014
            r_ne = co2_ne / co2_ne_2014
            r_abs = co2_abs / co2_abs_2014

        y1 = co2_e
        y2 = co2_ne
        if x > 2014:
            ax.bar(x, y2, width1, bottom=y1, align='center', color=colors[1])
            text = '%2d' % (r_ne*100.0)
            ax.text(x, y1+y2/2.0, text, color=config.COL_CLOUDS_LIGHT, fontsize=fs1, ha='center', va='center', weight='bold')
        else:
            ax.bar(x, y2, width1, bottom=y1, align='center', color=colors[1], label='非エネルギー起源')
            ax.text(x, y1+y2/2.0, '100', color=config.COL_CLOUDS_LIGHT, fontsize=fs1, ha='center', va='center', weight='bold')

        y1 = 0.0
        y2 = co2_e
        if x > 2014:
            ax.bar(x, y2, width1, bottom=y1, align='center', color=colors[0])
            text = '%2d' % (r_e*100.0)
            ax.text(x, y2/2.0, text, color=config.COL_CLOUDS_LIGHT, fontsize=fs1, ha='center', va='center', weight='bold')
        else:
            ax.bar(x, y2, width1, bottom=y1, align='center', color=colors[0], label='エネルギー起源')
            ax.text(x, y2/2.0, '100', color=config.COL_CLOUDS_LIGHT, fontsize=fs1, ha='center', va='center', weight='bold')

        y1 = 0
        y2 = co2_abs
        if x > 2014:
            ax.bar(x, y2, width1, bottom=y1, align='center', color=colors[2])
            text = '%2d' % (r_abs*100.0)
            ax.text(x, y1+y2/2.0, text, color=config.COL_CLOUDS_LIGHT, fontsize=fs1, ha='center', va='center', weight='bold')
        else:
            ax.bar(x, y2, width1, bottom=y1, align='center', color=colors[2], label='吸収')
            ax.text(x, y1+y2/2.0, '100', color=config.COL_CLOUDS_LIGHT, fontsize=fs1, ha='center', va='center', weight='bold')

#    ax.set_xticks([])
    y = np.arange(ymin, ymax, step=200)
    ax.set_yticks(np.arange(0, ymax, 200), minor = False)
    ax.set_yticks(np.arange(-50, ymax, 50), minor = True)

    ax.legend(loc='lower left', bbox_to_anchor=(0,0.05), borderaxespad=1)
#    categories = ['2024', '2030', '2040', '2050']
#    tx = np.arange(4)
#    ax.set_xticks(tx)
#    ax.set_xticklabels(categories)

    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT)


if __name__ == '__main__':
    df1 = load_data()
    plot(df1)

