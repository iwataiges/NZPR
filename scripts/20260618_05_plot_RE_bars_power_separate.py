# 20250103
# 20250401_04_plot_RE_capacity_01PV.py
# 20250831
# 20251226
# 20260617
# original code from: https://how2matplotlib.com/create-a-stacked-bar-plot-in-matplotlib.html
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.colors import LinearSegmentedColormap
import openpyxl
import pandas as pd
import config

INPUT_EXCEL1 = 'inputs/RE/20260617_01_RE_japan.xlsx'
INPUT_EXCEL2 = 'inputs/RE/20260619_06_RE_power_for_plot.xlsx'
OUTPUT_PLOT = 'charts/20260618_05_plot_RE_bars_power_separate.png'

rcParams['font.size'] = 16
rcParams['axes.labelsize'] = 16
rcParams['xtick.labelsize'] = 18
rcParams['ytick.labelsize'] = 18
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
    wb = openpyxl.load_workbook(INPUT_EXCEL1, data_only=True)
    sheet = wb['power']
    data = sheet.values
    cols = next(data)
    data = list(data)
    df1 = pd.DataFrame(data, columns=cols)

    wb = openpyxl.load_workbook(INPUT_EXCEL2, data_only=True)
    sheet = wb['Sheet1']
    data = sheet.values
    cols = next(data)
    data = list(data)
    df2 = pd.DataFrame(data, columns=cols)

    return df1, df2

def plot_sub(ax, df1, df2, label1, label2, ymax, pos, title):
    xmin = -5
    xmax = 35
    width1 = 0.5
    fs = 14
    fs2 = 24
    year0 = 2010
    year1 = 2030
    x1 = 20

    factor = 5.0

    ax.set(xlim=(xmin, xmax), ylim=(0, ymax))
    ax.set_ylabel('発電量 [TWh]')

    ndata1 = df1.index.shape[0]
    textcolour = config.COL_WET_ASPHALT_DARK
    for i in range(ndata1):
        year = df1.iloc[i]['Year']
        x = year - year0
        value = df1.iloc[i][label1]
        ax.bar(x+width1/2.0, value, width1, bottom=0.0, align='center', color=color_matrix[pos][1])

        if year == 2010 or year == 2013 or year == 2023:
            yval1 = int(value+0.5)
            text = '%d' % (yval1)
            ax.text(x+width1/2.0, yval1 + ymax*0.01, text, ha='center', fontsize=fs, color=textcolour)

    ndata2 = df2.index.shape[0]
    for i in range(ndata2):
        year = df2.iloc[i]['Year']
        if year >= 2030:
#            x = df2.iloc[i]['x'] * factor
            x = year - year0
            offset = df2.iloc[i]['Offset'] * factor
            gradflg = False
            if df2.iloc[i]['Gradient'] == 'Y':
                gradflg = True
                # ugly width adjustment
                width2 = width1 + df2.iloc[i]['adjust'] * factor

            value = df2.iloc[i][label2]
            colpos = int(df2.iloc[i]['Tone'])

            if gradflg:
                value_high = df2.iloc[i][label2 + '_high']

            y1 = 0.0
            y2 = value
            ax.bar(x+width1/2.0+offset, y2, width1, bottom=y1, align='center', color=color_matrix[pos][colpos])
            if gradflg:
                y1 = y2
                y2 = y1 + value_high - value
                gradient_bar(ax, x, y2, offset=offset, colmap=color_matrix[pos][2], bottom=y1, width=width2)

            if pd.isnull(df2.iloc[i]['Label']):
                textcolour = config.COL_CONCRETE_DARK
            elif df2.iloc[i]['Label'] == 'Current':
                textcolour = config.COL_WET_ASPHALT_DARK
            elif df2.iloc[i]['Label'] == 'SEP':
                textcolour = config.COL_ALIZARIN_MED
            elif df2.iloc[i]['Label'] == '1.5CRM':
                textcolour = config.COL_NEPHRITIS_DARK

            ax.text(xmin + 1, ymax*0.9, title, fontsize=fs2, color=color_matrix[pos][1], ha='left')

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

    categories = ['2010', '2013', '2023', '2030', '2035', '2040']
    x = np.array([0, 3, 13, 20, 25, 30])
    ax.set_xticks(x+width1/2)
    ax.set_xticklabels(categories)

def plot_fit_line(ax, df1, df2, label1, array, pos):
    year0 = 2010
    x0 = 2019
    x1 = 2023
    x2 = 2040
    width1 = 0.5
    factor = 5.0

    offset = df2[(df2['Year']==x2) & (df2['Label']=='Current')]['Offset'].values[0]

    if len(array) > 1:
        a1 = array[1]
        b = df1[df1['Year']==x1][label1]
        tx = np.array([x1-year0, x2-year0+offset*factor])+width1/2.0
        ty = np.array([b,a1*(x2-x1)+b])
        ax.plot(tx, ty, '--', linewidth=1, color=color_matrix[pos][0])

    a0 = array[0]
    b = df1[df1['Year']==x0][label1]
    tx = np.array([x0-year0, x2-year0+offset*factor])+width1/2.0
    ty = np.array([b,a0*(x2-x0)+b])
    ax.plot(tx, ty, '--', linewidth=1, color=color_matrix[pos][0])

    return

def plot(df1, df2):

    fig, axs = plt.subplots(3,1, figsize=(15, 15))

    plot_sub(axs[0], df1, df2, 'PV_TWh_IRENA', 'PV', 410, 0, '太陽光')
    plot_sub(axs[1], df1, df2, 'OnSW_TWh_IRENA', 'OnSW', 300, 1, '陸上風力')
    plot_sub(axs[2], df1, df2, 'OffSW_TWh_IRENA', 'OffSW', 300, 2, '洋上風力')

    plot_fit_line(axs[0], df1, df2, 'PV_TWh_ES', [6.758, 3.856], 0)
    plot_fit_line(axs[1], df1, df2, 'OnSW_TWh_IRENA', [0.602], 1)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT)

if __name__ == '__main__':
    df1, df2 = load_data()
    plot(df1, df2)
