# 20260430
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import openpyxl
import pandas as pd
from matplotlib import rcParams
import config

INPUT_EXCEL = 'inputs/RE/20260430_01_PV_Wind_2040_power_for_plot.xlsx'
OUTPUT_PLOT = 'charts/20260430_01_plot_bars_power_PV_Wind_2040.png'

rcParams['font.size'] = 20
rcParams['axes.labelsize'] = 20
rcParams['xtick.labelsize'] = 20
rcParams['ytick.labelsize'] = 20
#rcParams['lines.markersize'] = 10
rcParams['lines.linewidth'] = 5
rcParams['font.family'] = 'Hiragino Sans'
#rcParams['xtick.labelsize'] = 'small'
#rcParams['ytick.labelsize'] = 'small'

# gradient
colors = [config.COL_ORANGE_MED, '#ffffff']
cmap_orange = LinearSegmentedColormap.from_list("mycmap", colors)
colors = [config.COL_GREEN_MED, '#ffffff']
cmap_green = LinearSegmentedColormap.from_list("mycmap", colors)
colors = [config.COL_BLUE_MED, '#ffffff']
cmap_blue = LinearSegmentedColormap.from_list("mycmap", colors)
colors = [config.COL_BROWN_MED, '#ffffff']
cmap_brown = LinearSegmentedColormap.from_list("mycmap", colors)
colors = [config.COL_CYAN_MED, '#ffffff']
cmap_cyan = LinearSegmentedColormap.from_list("mycmap", colors)
colors = [config.COL_BLUE_GREY_MED, '#ffffff']
cmap_blue_grey = LinearSegmentedColormap.from_list("mycmap", colors)

colors = [
    config.COL_ORANGE_MED,
    config.COL_GREEN_MED,
    config.COL_BLUE_MED,
    config.COL_ORANGE_LIGHT,
    config.COL_BLUE_LIGHT
]


def load_data():
    wb = openpyxl.load_workbook(INPUT_EXCEL, data_only=True)
    sheet = wb['Sheet1']
    data = sheet.values
    cols = next(data)
    data = list(data)
    df1 = pd.DataFrame(data, columns=cols)
    df1.dropna(subset=['x'], inplace=True)
    return df1

def plot(df1):
    ndata1 = df1.index.shape[0]

    fig, ax = plt.subplots(figsize=(15,10))
    ymax = 1000
    xmin = 0.25
    xmax = 2.75
    ax.set(xlim=(xmin, xmax), ylim=(0, ymax))
    ax.set_ylabel('発電電力量 [TWh/年]')

    width1 = 0.1
 #   fs = 14

    for i in range(ndata1):
        x = df1.iloc[i]['x']

        pv = df1.iloc[i]['PV']
        onsw = df1.iloc[i]['OnSW']
        offsw = df1.iloc[i]['OffSW']
        pv_h2 = df1.iloc[i]['PV_H2']
        offsw_h2 = df1.iloc[i]['OffSW_H2']

#        ty = pv+onsw+offsw+geot+hydro+bio+ymax*0.01
#        label = df1.iloc[i]['Label']

        y1 = 0.0
        y2 = pv
        ax.bar(x+width1/2.0, y2, width1, bottom=y1, align='center', color=colors[0])
        text = '%d' % (int(pv))
        ax.text(x+width1, y1+y2/2.0, text, color=colors[0], va='center')
 
        y1 = y2
        y2 = onsw
        ax.bar(x+width1/2.0, y2, width1, bottom=y1, align='center', color=colors[1])
        text = '%d' % (int(onsw))
        ax.text(x+width1, y1+y2/2.0, text, color=colors[1], va='center')

        y1 = y1 + y2
        y2 = offsw
        ax.bar(x+width1/2.0, y2, width1, bottom=y1, align='center', color=colors[2])
        text = '%d' % (int(offsw))
        ax.text(x+width1, y1+y2/2.0, text, color=colors[2], va='center')

        y1 = y1 + y2
        y2 = pv_h2
        ax.bar(x+width1/2.0, y2, width1, bottom=y1, align='center', color=colors[3])
        if pd.isnull(pv_h2) is False:
            text = '%d' % (int(pv_h2))
            ax.text(x+width1, y1+y2/2.0, text, color=colors[3], va='center')

        y1 = y1 + y2
        y2 = offsw_h2
        ax.bar(x+width1/2.0, y2, width1, bottom=y1, align='center', color=colors[4])
        if pd.isnull(offsw_h2) is False:
            text = '%d' % (int(offsw_h2))
            ax.text(x+width1, y1+y2/2.0, text, color=colors[4], va='center')

    categories = ['排出上振れ', '再エネ拡大', 'バランスサブ', 'バランス']
    tx = df1['x']
    ax.set_xticks(tx+width1/2)
    ax.set_xticklabels(categories)

    # legends
    x1 = xmin + (xmax - xmin) * 0.025
    x2 = xmin + (xmax - xmin) * 0.09
    x3 = xmin + (xmax - xmin) * 0.1
    labels = ['太陽光', '陸上風力', '洋上風力', '太陽光(水素製造)', '洋上風力(水素製造)']
    for i in range(5):
        y1 = (0.75 + i * 0.05) * ymax
        y2 = y1 + 0.01 * ymax
        xpos = np.array([x1, x2])
        ypos = np.array([y2, y2])
        ax.plot(xpos, ypos, '-', linewidth=5, color=colors[i])
        ax.text(x3, y1, labels[i], ha='left')
        #ax.text(x3, y1, labels[i], ha='left', backgroundcolor=color_matrix[i][0])

    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT)


if __name__ == '__main__':
    df1 = load_data()
    plot(df1)

