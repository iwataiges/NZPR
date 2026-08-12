# 20260116
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import openpyxl
import pandas as pd
from matplotlib import rcParams
import config

INPUT_EXCEL = 'inputs/WF/20260120業務2035_for_WF.xlsx'
OUTPUT_PLOT1 = 'charts/20260120_01_WF_業務2035_energy.png'
OUTPUT_PLOT2 = 'charts/20260120_01_WF_業務2035_co2.png'

rcParams['font.size'] = 16
rcParams['axes.labelsize'] = 16
rcParams['xtick.labelsize'] = 14
rcParams['ytick.labelsize'] = 14
#rcParams['lines.markersize'] = 10
rcParams['lines.linewidth'] = 5
rcParams['font.family'] = 'Hiragino Sans'

colors = [
    config.COL_SILVER_MED,
    config.COL_POMEGRANATE_MED,
    config.COL_PETER_RIVER_MED
]

def load_data():
    wb = openpyxl.load_workbook(INPUT_EXCEL, data_only=True)
    sheet = wb['energy']
    data = sheet.values
    cols = next(data)
    data = list(data)
    df1 = pd.DataFrame(data, columns=cols)

    sheet = wb['co2']
    data = sheet.values
    cols = next(data)
    data = list(data)
    df2 = pd.DataFrame(data, columns=cols)

    return df1, df2

def plot(df, outputfilename):
    fig, ax = plt.subplots(figsize=(15,10))

    fs1 = 12
    fs2 = 16
    lw1 = 1
    width1 = 0.5

    labels = []
    ymax = df['total'].max()
    ymin = 0.0
    offy = -0.03

    ndata = df.index.shape[0]
    for i in range(ndata):
        x = df.loc[i]['x']
        v = df.loc[i]['v']
        base = df.loc[i]['base']
        diff = df.loc[i]['diff']

        ax.bar(x, v, bottom=base, width=width1, color=colors[df.loc[i]['color']], label=df.loc[i]['label'])
        if i > 0:
            tx2 = x - width1/2.0
            if pd.isnull(diff):
                ty2 = v
            elif diff > 0:
                ty2 = base
            else:
                ty2 = base + v
            ax.plot(np.array([tx1, tx2]), np.array([ty1, ty2]), '-', color=config.COL_ASBESTOS_LIGHT, linewidth=lw1)
        else:
            v0 = v

        if pd.isnull(diff):
            val = v*100.0/v0
            val_text = '%d%%' % (int(val+0.5))
            ax.text(x, v/2.0, val_text, fontsize=fs1, ha='center', va='center', color=config.COL_WET_ASPHALT_DARK)
        elif diff > 0:
            val = diff*100.0/v0
            val_text = '+%d' % (int(val+0.5))
            if val > 5:
                ax.text(x, base + v/2.0, val_text, fontsize=fs1, ha='center', va='center', color=config.COL_SILVER_LIGHT, weight='bold')
            else:
                ax.text(x, base + offy*(ymax - ymin), val_text, fontsize=fs1, ha='center', va='center', color=colors[df.loc[i]['color']], weight='bold')
        else:
            val = diff*100.0/v0
            val_text = '%d' % (int(val-0.5))
            if val < -5:
                ax.text(x, base + v/2.0, val_text, fontsize=fs1, ha='center', va='center', color=config.COL_SILVER_LIGHT, weight='bold')
            else:
                ax.text(x, base + offy*(ymax - ymin), val_text, fontsize=fs1, ha='center', va='center', color=colors[df.loc[i]['color']], weight='bold')

        texts = df.loc[i]['label'].split('_')
        for j in range(len(texts)):
            ax.text(x, offy*(j+1)*(ymax-ymin), texts[j], fontsize=fs2, ha='center', va='top')

        tx1 = x + width1/2.0
        if pd.isnull(diff):
            ty1 = v
        elif diff > 0:
            ty1 = base + diff
        else:
            ty1 = base

    ax.set_xticks([])
    ax.set_yticks([])

    plt.tight_layout()
    plt.savefig(outputfilename)



if __name__ == '__main__':
    df1, df2 = load_data()
    plot(df1, OUTPUT_PLOT1)
    plot(df2, OUTPUT_PLOT2)
 