# 20250103
# 20250401_04_plot_RE_capacity_01PV.py
# 20250831
# 20251226 / 20260331
# original code from: https://how2matplotlib.com/create-a-stacked-bar-plot-in-matplotlib.html
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.colors import LinearSegmentedColormap
import openpyxl
import pandas as pd
import config

INPUT_EXCEL = 'inputs/RE/20260331_05_RE_cap_for_plot.xlsx'
OUTPUT_PLOT = 'charts/20260331_03_plot_RE_bars_capacity_separate.png'

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

color_matrix = [
    [config.COL_ORANGE_MED, config.COL_ORANGE_DARK, cmap_orange],
    [config.COL_GREEN_MED, config.COL_GREEN_DARK, cmap_green],
    [config.COL_BLUE_MED, config.COL_BLUE_DARK, cmap_blue],
    [config.COL_BROWN_MED, config.COL_BROWN_DARK, cmap_brown],
    [config.COL_CYAN_MED, config.COL_CYAN_DARK, cmap_cyan],
    [config.COL_BLUE_GREY_MED, config.COL_BLUE_GREY_DARK, cmap_blue_grey]
]

# bar with gradient: https://matplotlib.org/stable/gallery/lines_bars_and_markers/gradient_bar.html
def gradient_vertical(ax, cmap_range=(0,1), **kwargs):
    v = np.array([1, 0])
    X = np.array([[v @ [1, 0], v @ [1, 1]],
                  [v @ [0, 0], v @ [0, 1]]])
    a, b = cmap_range
    X = a + (b-a) / X.max() * X
    im = ax.imshow(X, interpolation='bicubic', clim=(0,1), aspect='auto', **kwargs)

def gradient_bar(ax, x, y, offset, colmap, width=0.5, bottom=0):
    left = x
    top = y
    right = left + width
    gradient_vertical(ax, extent=(left+offset, right+offset, bottom, top),
                      cmap=colmap, cmap_range=(0.0, 1.0))

def load_data():
    wb = openpyxl.load_workbook(INPUT_EXCEL, data_only=True)
    sheet = wb['Sheet1']
    data = sheet.values
    cols = next(data)
    data = list(data)
    df1 = pd.DataFrame(data, columns=cols)
    return df1

def plot_sub(ax, df1, label, ymax, pos, title):
    ndata1 = df1.index.shape[0]
    xmin = -0.5
    xmax = 4.5
    width1 = 0.1
    fs = 14

    ax.set(xlim=(xmin, xmax), ylim=(0, ymax))
    ax.set_ylabel('設備容量 [GW]')

    for i in range(ndata1):
        x = df1.iloc[i]['x']
        offset = df1.iloc[i]['Offset']
        gradflg = False
        if df1.iloc[i]['Gradient'] == 'Y':
            gradflg = True
            # ugly width adjustment
            width2 = width1 + df1.iloc[i]['adjust']*0.5

        value = df1.iloc[i][label]
        colpos = df1.iloc[i]['Tone']

        if gradflg:
            value_high = df1.iloc[i][label + '_high']

        y1 = 0.0
        y2 = value
        ax.bar(x+width1/2.0+offset, y2, width1, bottom=y1, align='center', color=color_matrix[pos][colpos])
        if gradflg:
            y1 = y2
            y2 = y1 + value_high - value
            gradient_bar(ax, x, y2, offset=offset, colmap=color_matrix[pos][2], bottom=y1, width=width2)

        if pd.isnull(df1.iloc[i]['Label']):
            textcolour = config.COL_CONCRETE_DARK
        elif df1.iloc[i]['Label'] == 'Current':
            textcolour = config.COL_WET_ASPHALT_DARK
        elif df1.iloc[i]['Label'] == 'SEP':
            textcolour = config.COL_ALIZARIN_MED
        elif df1.iloc[i]['Label'] == '1.5CRM':
            textcolour = config.COL_NEPHRITIS_DARK

        ax.text(xmin + 0.1, ymax*0.9, title, fontsize=36, color=color_matrix[pos][1], ha='left')

        # number texts
        yval1 = int(value+0.5)
        if gradflg:
            yval2 = int(value_high+0.5)
            if yval2 == yval1:
                text = '%d' % (yval1)
            elif yval2 > 99:
                text = '%d\n|\n%d' % (yval2, yval1)
            else:
                text = '%d-%d' % (yval1, yval2)
            ax.text(x+width1/2.0+offset, yval2 + ymax*0.01, text, ha='center', fontsize=fs, color=textcolour)
        else:
            text = '%d' % (yval1)
            ax.text(x+width1/2.0+offset, yval1 + ymax*0.01, text, ha='center', fontsize=fs, color=textcolour)

    categories = ['2013', '2022', '2024', '2030', '2035', '2040']
    x = np.array([0, 0.6, 1, 2, 3, 4])
    ax.set_xticks(x+width1/2)
    ax.set_xticklabels(categories)

def plot(df1):

    fig, axs = plt.subplots(3,1, figsize=(18, 18))

    plot_sub(axs[0], df1, 'PV', 300, 0, '太陽光')
    plot_sub(axs[1], df1, 'OnSW', 150, 1, '陸上風力')
    plot_sub(axs[2], df1, 'OffSW', 150, 2, '洋上風力')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT)

if __name__ == '__main__':
    df1 = load_data()
    plot(df1)
