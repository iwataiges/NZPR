# 20260116
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import openpyxl
import pandas as pd
from matplotlib import rcParams
import config

INPUT_EXCEL = 'inputs/RE/20260707_01_primary_energy_supply.xlsx'
OUTPUT_PLOT = 'charts/20260707_01_plot_bars_energy_self_sufficiency.png'

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
colors = [config.COL_GREEN_SEA_MED, config.COL_AMETHYST_DARK, config.COL_SILVER_LIGHT]
label_colors = [config.COL_WET_ASPHALT_DARK, config.COL_TURQUOISE_MED, config.COL_ORANGE_MED]

def load_data():
    wb = openpyxl.load_workbook(INPUT_EXCEL, data_only=True)
    sheet = wb['for_plot']
    data = sheet.values
    cols = next(data)
    data = list(data)
    df1 = pd.DataFrame(data, columns=cols)
    df1.dropna(subset=['x'], inplace=True)
    return df1

def plot(df1):
    ndata1 = df1.index.shape[0]

    fig, ax = plt.subplots(figsize=(15,10))
    ymax = 110.0
    xmin = -0.5
    xmax = 3.5
    ax.set(xlim=(xmin, xmax), ylim=(0, ymax))
#    ax.set_ylabel('エネルギー電源構成 [%]')

    width1 = 0.2
    fs1 = 14
    fs2 = 16

    for i in range(ndata1):
        x = df1.iloc[i]['x']
        if x >= 0:
            offset = df1.iloc[i]['offset']
            label = df1.iloc[i]['Label']

            tes = df1.iloc[i]['TES']
            tes_re = df1.iloc[i]['RE']
            tes_nuc = df1.iloc[i]['Nuc']

            y1 = 0.0
            y2 = tes_re / tes * 100.0
            ax.bar(x+offset, y2, width1, bottom=y1, align='center', color=colors[0])

            y1 = y2
            y2 = tes_nuc / tes * 100.0
            ax.bar(x+offset, y2, width1, bottom=y1, align='center', color=colors[1])

            y1 = y1 + y2
            y2 = (tes - tes_re - tes_nuc) / tes * 100.0
            ax.bar(x+offset, y2, width1, bottom=y1, align='center', color=colors[2])

            ssr = (tes_re+tes_nuc)/tes * 100.0
#            str = '%4.1f%%' % (ssr)
            str = '%d%%' % (ssr+0.5)
            ax.text(x+offset, 102, str, fontsize=fs1, ha='center')

            j = df1.iloc[i]['label_color']
            ax.text(x+offset, 107, label, fontsize=fs2, ha='center', color=label_colors[j])

    ax.text(-0.4, 102, '自給率', fontsize=fs1, ha='left')

#    ax.set_xticks([])
    y = np.arange(0, 101, step=20)
    ax.set_yticks(y)

    categories = ['2024', '2030', '2040', '2050']
    tx = np.arange(4)
#    tx = (XMAX-XMIN) * (x - YEAR1) / (YEAR2 - YEAR1)
    ax.set_xticks(tx)
    ax.set_xticklabels(categories)

    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT)


if __name__ == '__main__':
    df1 = load_data()
    plot(df1)

