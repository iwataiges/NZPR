# 20251226 / 20260331
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import openpyxl
import pandas as pd
from matplotlib import rcParams
import config

INPUT_EXCEL = 'inputs/RE/20260331_05_RE_power_for_plot.xlsx'
OUTPUT_PLOT = 'charts/20260331_02_plot_RE_bars_power.png'

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
    ymax = 900
    xmin = -0.5
    xmax = 4.5
    ax.set(xlim=(xmin, xmax), ylim=(0, ymax))
    ax.set_ylabel('発電電力量 [TWh/年]')

    width1 = 0.1
    fs = 14

    for i in range(ndata1):
        x = df1.iloc[i]['x']
        offset = df1.iloc[i]['Offset']
        gradflg = False
        if df1.iloc[i]['Gradient'] == 'Y':
            gradflg = True
            # ugly width adjustment
            width2 = width1 + df1.iloc[i]['adjust']

        pv = df1.iloc[i]['PV']
        onsw = df1.iloc[i]['OnSW']
        offsw = df1.iloc[i]['OffSW']
        geot = df1.iloc[i]['GeoT']
        hydro = df1.iloc[i]['Hydro']
        bio = df1.iloc[i]['Biomass']
        colpos = int(df1.at[i,'Tone'])

        ty = pv+onsw+offsw+geot+hydro+bio+ymax*0.01

        if gradflg:
            pv_high = df1.iloc[i]['PV_high']
            onsw_high = df1.iloc[i]['OnSW_high']
            offsw_high = df1.iloc[i]['OffSW_high']
            geot_high = df1.iloc[i]['GeoT_high']
            hydro_high = df1.iloc[i]['Hydro_high']
            bio_high = df1.iloc[i]['Biomass_high']
            ty = pv_high+onsw_high+offsw_high+geot_high+hydro_high+bio_high+ymax*0.01

        label = df1.iloc[i]['Label']

        # highlight background
#        if pd.isnull(label) == False:
#            if label == 'Current':
#                col_bg = col_grey_light
#            elif label == 'SEP':
#                col_bg = col_yellow_light
#            elif label == '1.5CRM':
#                col_bg = col_green_light
#            ax.bar(x+width1/2.0+offset, ty, width1+width3, align='center', color=col_bg, alpha=0.5)
#            ax.bar(x+width1/2.0+offset, ty, width1, align='center', color='#ffffff')

        y1 = 0.0
        y2 = pv
        ax.bar(x+width1/2.0+offset, y2, width1, bottom=y1, align='center', color=color_matrix[0][colpos])
        if gradflg:
            y1 = y2
            y2 = y1 + pv_high - pv
            gradient_bar(ax, x, y2, offset=offset, colmap=color_matrix[0][2], bottom=y1, width=width2)

        y1 = y2
        y2 = onsw
        ax.bar(x+width1/2.0+offset, y2, width1, bottom=y1, align='center', color=color_matrix[1][colpos])
        if gradflg:
            y3 = y2+y1
            y4 = y3 + onsw_high - onsw
            gradient_bar(ax, x, y4, offset=offset, colmap=color_matrix[1][2], bottom=y3, width=width2)
            y2 = y2 + onsw_high - onsw

        y1 = y1 + y2
        y2 = offsw
        ax.bar(x+width1/2.0+offset, y2, width1, bottom=y1, align='center', color=color_matrix[2][colpos])
        if gradflg:
            y3 = y2+y1
            y4 = y3 + offsw_high - offsw
            gradient_bar(ax, x, y4, offset=offset, colmap=color_matrix[2][2], bottom=y3, width=width2)
            y2 = y2 + offsw_high - offsw

        y1 = y1 + y2
        y2 = geot
        ax.bar(x+width1/2.0+offset, y2, width1, bottom=y1, align='center', color=color_matrix[3][colpos])
        if gradflg:
            y3 = y2+y1
            y4 = y3 + geot_high - geot
            gradient_bar(ax, x, y4, offset=offset, colmap=color_matrix[3][2], bottom=y3, width=width2)
            y2 = y2 + geot_high - geot

        y1 = y1 + y2
        y2 = hydro
        ax.bar(x+width1/2.0+offset, y2, width1, bottom=y1, align='center', color=color_matrix[4][colpos])
        if gradflg:
            y3 = y2+y1
            y4 = y3 + hydro_high - hydro
            gradient_bar(ax, x, y4, offset=offset, colmap=color_matrix[4][2], bottom=y3, width=width2)
            y2 = y2 + hydro_high - hydro

        y1 = y1 + y2
        y2 = bio
        ax.bar(x+width1/2.0+offset, y2, width1, bottom=y1, align='center', color=color_matrix[5][colpos])
        if gradflg:
            y3 = y2+y1
            y4 = y3 + bio_high - bio
            gradient_bar(ax, x, y4, offset=offset, colmap=color_matrix[5][2], bottom=y3, width=width2)
            y2 = y2 + bio_high - bio

        if pd.isnull(df1.iloc[i]['Label']):
            textcolour = config.COL_CONCRETE_DARK
        elif df1.iloc[i]['Label'] == 'Current':
            textcolour = config.COL_WET_ASPHALT_DARK
        elif df1.iloc[i]['Label'] == 'SEP':
            textcolour = config.COL_ALIZARIN_MED
        elif df1.iloc[i]['Label'] == '1.5CRM':
            textcolour = config.COL_NEPHRITIS_DARK

        yval1 = pv + onsw + offsw + geot + hydro + bio
        if gradflg:
            yval2 = pv_high + onsw_high + offsw_high + geot_high + hydro_high + bio_high
            text = '%d\n|\n%d' % (int(yval2), int(yval1))
            ax.text(x+width1/2.0+offset, yval2 + ymax*0.01, text, ha='center', fontsize=fs, color=textcolour)
        else:
            text = '%d' % (int(yval1))
            ax.text(x+width1/2.0+offset, yval1 + ymax*0.01, text, ha='center', fontsize=fs, color=textcolour)


    categories = ['2013', '2023', '2030', '2035', '2040']
    x = np.array([0, 1, 2, 3, 4])
    ax.set_xticks(x+width1/2)
    ax.set_xticklabels(categories)

    # legends
    x1 = xmin + (xmax - xmin) * 0.025
    x2 = xmin + (xmax - xmin) * 0.09
    x3 = xmin + (xmax - xmin) * 0.1
    labels = ['太陽光', '陸上風力', '洋上風力', '地熱', '水力', 'バイオマス']
    for i in range(6):
        y1 = (0.75 + i * 0.04) * ymax
        y2 = y1 + 0.01 * ymax
        xpos = np.array([x1, x2])
        ypos = np.array([y2, y2])
        ax.plot(xpos, ypos, '-', linewidth=5, color=color_matrix[i][0])
        ax.text(x3, y1, labels[i], ha='left')
        #ax.text(x3, y1, labels[i], ha='left', backgroundcolor=color_matrix[i][0])

    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT)


if __name__ == '__main__':
    df1 = load_data()
    plot(df1)

