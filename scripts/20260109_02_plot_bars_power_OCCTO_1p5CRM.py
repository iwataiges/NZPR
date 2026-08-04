# 20251226 / 1229
# 20260109
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import openpyxl
import pandas as pd
from matplotlib import rcParams
import config

INPUT_EXCEL = 'inputs/RE/20260109_power_20402050_OCCTO_1p5CRM.xlsx'
OUTPUT_PLOT = 'charts/20260109_02_plot_bars_power_OCCTO_1p5CRM.png'

rcParams['font.size'] = 16
rcParams['axes.labelsize'] = 16
rcParams['xtick.labelsize'] = 18
rcParams['ytick.labelsize'] = 18
#rcParams['lines.markersize'] = 10
rcParams['lines.linewidth'] = 5
rcParams['font.family'] = 'Hiragino Sans'
#rcParams['xtick.labelsize'] = 'small'
#rcParams['ytick.labelsize'] = 'small'

colors_med = [
    config.COL_ORANGE_MED,     # PV
    config.COL_GREEN_MED,      # Wind
    config.COL_BROWN_MED,      # Geothermal
    config.COL_CYAN_MED,       # Hydro
    config.COL_AMBER_MED,      # Biomass
    config.COL_CONCRETE_MED,   # Thermal
    config.COL_PURPLE_MED      # Nuclear
]

colors_dark = [
    config.COL_ORANGE_DARK,     # PV
    config.COL_GREEN_DARK,      # Wind
    config.COL_BROWN_DARK,      # Geothermal
    config.COL_CYAN_DARK,       # Hydro
    config.COL_AMBER_DARK,      # Biomass
    config.COL_CONCRETE_DARK,   # Thermal
    config.COL_PURPLE_DARK      # Nuclear
]


def load_data():
    wb = openpyxl.load_workbook(INPUT_EXCEL, data_only=True)
    sheet = wb['Sheet1']
    data = sheet.values
    cols = next(data)
    data = list(data)
    df = pd.DataFrame(data, columns=cols)
    df.dropna(subset=['Year'], inplace=True)
    df1 = df[df['Nuclear_scale'] != '原子力大']
    return df1

def plot(df1):
    ndata1 = df1.index.shape[0]

    fig, ax = plt.subplots(figsize=(15,10))
    ymax = 1500
    xmin = -0.25
    xmax = 3.1
    ax.set(xlim=(xmin, xmax), ylim=(0, ymax))
    ax.set_ylabel('発電電力量 [TWh/年]')

    xpos = np.array([0, 0.7, 1.5, 2.5])
    years = [2013, 2023, 2040, 2050]
    sources = ['PV', 'Wind', 'GeoT', 'Hydro', 'Biomass', 'Thermal', 'Nuclear']

    width1 = 0.1
    fs = 14

    for i in range(ndata1):
        year = df1.iloc[i]['Year']
        for j in range(len(years)):
            if year == years[j]:
                tx = xpos[j]
        source = df1.iloc[i]['Source']
        if source == 'OCCTO':
            if year == 2040:
                offset = df1.iloc[i]['Total']*0.00075 - 0.8
            elif year == 2050:
                offset = df1.iloc[i]['Total']*0.0012 - 1.5
            else:
                print('Error: year=%d, source=%s' % (year, source))
                exit(1)
        elif source == '1.5CRM 系統電力':
            offset = 0.2
        else:
            offset = 0.0

        y1 = 0.0
        for j in range(len(sources)):
            v = df1.iloc[i][sources[j]]
            if year < 2030:
                col = colors_dark[j]
            else:
                col = colors_med[j]
            ax.bar(tx+width1/2.0+offset, v, width1, bottom=y1, align='center', color=col)
            y1 = y1 + v



    ax.set_xticks(xpos+width1/2)
    ax.set_xticklabels(years)

    # legends
    x1 = xmin + (xmax - xmin) * 0.025
    x2 = xmin + (xmax - xmin) * 0.09
    x3 = xmin + (xmax - xmin) * 0.1
    labels = ['太陽光', '風力', '地熱', '水力', 'バイオマス', '火力', '原子力']
    for i in range(len(labels)):
        y1 = (0.75 + i * 0.035) * ymax
        y2 = y1 + 0.01 * ymax
        xpos = np.array([x1, x2])
        ypos = np.array([y2, y2])
        ax.plot(xpos, ypos, '-', linewidth=5, color=colors_med[i])
        ax.text(x3, y1, labels[i], ha='left')
        #ax.text(x3, y1, labels[i], ha='left', backgroundcolor=color_matrix[i][0])


    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT)


if __name__ == '__main__':
    df1 = load_data()
    plot(df1)

