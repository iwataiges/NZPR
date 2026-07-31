# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import rcParams
import config

rcParams['font.size'] = 20
rcParams['axes.labelsize'] = 20
rcParams['xtick.labelsize'] = 20
rcParams['ytick.labelsize'] = 20
#rcParams['lines.markersize'] = 10
rcParams['lines.linewidth'] = 5
rcParams['font.family'] = 'Hiragino Sans'
#rcParams['xtick.labelsize'] = 'small'
#rcParams['ytick.labelsize'] = 'small'

def plot():
    data = [
        {
            'label': '2013 実績',
            'co2_power': 572.4,
            'co2_others': 663
        },
        {
            'label': '2023 実績',
            'co2_power': 401.9,
            'co2_others': 519.8
        },
        {
            'label': 'SEP6の\n電源構成',
            'co2_power': 205.9,
            'co2_others': 519.8
        },
        {
            'label': '1.5C RMの\n電源構成',
            'co2_power': 125.8,
            'co2_others': 519.8
        },
    ]

    OUTPUT_PLOT = 'charts/20260731_02_plot_bars_co2_power_mix.png'

    fig, ax = plt.subplots(figsize=(15,10))
#    ymax = 1200
    xmin_disp = -0.5
    xmax_disp = 3.5
#    ax.set(xlim=(xmin, xmax), ylim=(0, ymax))
    ax.set(xlim=(xmin_disp, xmax_disp))
    ax.set_ylabel('エネルギー起源CO2排出量 [MtCO2/年]')

    width1 = 0.5
    fs1 = 14
    fs2 = 18
    lw1 = 1

    for i in range(len(data)):
        v1 = data[i]['co2_power']
        v2 = data[i]['co2_others']

        if i > 0:
            v3 = data[i-1]['co2_power']
            v4 = data[i-1]['co2_others']
            tx = np.array([i-1+width1/2.0, i-width1/2.0])
            ty = np.array([v3, v1])
            ax.plot(tx, ty, '-', linewidth=lw1, color=config.COL_ASBESTOS_MED)
            ty = np.array([v3+v4, v1+v2])
            ax.plot(tx, ty, '-', linewidth=lw1, color=config.COL_ASBESTOS_MED)

        ax.bar(i, v1, width1, align='center', color=config.COL_ORANGE_MED)
        ax.bar(i, v2, width1, bottom=v1, align='center', color=config.COL_ASBESTOS_MED)

        str = '%d' % (v1+0.5)
        ax.text(i, v1*0.5, str, ha='center', va='center', fontsize=fs1, color=config.COL_CLOUDS_LIGHT, weight='bold')
        str = '%d' % (v2+0.5)
        ax.text(i, v1+v2*0.5, str, ha='center', va='center', fontsize=fs1, color=config.COL_CLOUDS_LIGHT, weight='bold')

        ax.text(i, -50, data[i]['label'], fontsize=fs2, ha='center', va='top', weight='bold')

    plt.gca().spines['bottom'].set_visible(True)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['left'].set_visible(True)
    plt.gca().spines['right'].set_visible(False)
    ax.set_xticks([])

    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT)

if __name__ == '__main__':
    plot()

