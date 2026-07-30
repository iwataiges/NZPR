# 20260728
# -*- coding: utf-8 -*-
import json
import openpyxl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import config 

INPUT_EXCEL1 = 'inputs/RE/20260728BNEF_LCOE_PV_japan_and_others.xlsx'
OUTPUT_PLOT1 = 'charts/20260728_01_plot_PV_LCOE.png'
OUTPUT_PLOT2 = 'charts/20260728_01_plot_PV+storage_LCOE.png'

rcParams['font.size'] = 18
rcParams['axes.labelsize'] = 20
rcParams['xtick.labelsize'] = 20
rcParams['ytick.labelsize'] = 20
#rcParams['lines.markersize'] = 10
rcParams['lines.linewidth'] = 3
rcParams['font.family'] = 'Hiragino Sans'
rcParams['xtick.labelsize'] = 'small'
rcParams['ytick.labelsize'] = 'small'

list_countries = [
    {
        'name': 'Australia',
        'color' : config.COL_BELIZE_HOLE_MED,
        'label' : 'Australia'
    },
    {
        'name': 'China (Mainland)',
        'color' : config.COL_AMETHYST_MED,
        'label' : 'China'
    },
    {
        'name': 'Germany',
        'color' : config.COL_WET_ASPHALT_MED,
        'label' : 'Germany'
    },
    {
        'name': 'India',
        'color' : config.COL_PUMPKIN_MED,
        'label' : 'India'
    },
    {
        'name': 'UK',
        'color' : config.COL_NEPHRITIS_MED,
        'label' : 'UK'
    },
    {
        'name': 'US',
        'color' : config.COL_SUNFLOWER_MED,
        'label' : 'USA'
    },
    {
        'name': 'South Korea',
        'color': config.COL_CONCRETE_MED,
        'label': 'South Korea'
    },
    {
        'name': 'Japan',
        'color' : config.COL_ALIZARIN_MED,
        'label' : 'Japan'
    },
]

ymin = 0.0
ymax = 450.0
lw1 = 5
lw2 = 3
ps = 7

def load_data():
    wb = openpyxl.load_workbook(INPUT_EXCEL1, data_only=True)
    sheet = wb['PV']
    data = sheet.values
    cols = next(data)
    data = list(data)
    df1 = pd.DataFrame(data, columns=cols)
    df1.dropna(subset=['Metric'], inplace=True)

    sheet = wb['PV+storage']
    data = sheet.values
    cols = next(data)
    data = list(data)
    df2 = pd.DataFrame(data, columns=cols)
    df2.dropna(subset=['Metric'], inplace=True)

    return df1, df2


def plot1(df1):
    fig, ax = plt.subplots(figsize=(10, 10))

    ax.set_ylim(ymin, ymax)
#    ax.set_yticks([0, 500, 1000, 1500, 2000])
    xmin = 2013.5
    xmax = 2025.5
    ax.set_xlim(xmin, xmax)


    for country in list_countries:
        tdata = df1[df1['Region'] == country['name']]

        vx = np.arange(2014, 2026)
        vy = np.array([
            tdata[2014],
            tdata[2015],
            tdata[2016],
            tdata[2017],
            tdata[2018],
            tdata[2019],
            tdata[2020],
            tdata[2021],
            tdata[2022],
            tdata[2023],
            tdata[2024],
            tdata[2025]
        ])

        if country['name'] == 'Japan':
            lw = lw1
        elif country['name'] == 'South Korea':
            vx = np.arange(2018,2026)
            vy = vy[4:]
        else:
            lw = lw2
        ax.plot(vx, vy, '-', color=country['color'], linewidth=lw, label=country['label'])

    ax.legend(loc='upper right')
    ax.set_ylabel('USD 2025 / MWh')
    plt.tight_layout()
    #plt.show()
    plt.savefig(OUTPUT_PLOT1)

def plot2(df2):
    fig, ax = plt.subplots(figsize=(10, 10))

    ax.set_ylim(ymin, ymax)
#    ax.set_yticks([0, 500, 1000, 1500, 2000])
    xmin = 2017.5
    xmax = 2025.5
    ax.set_xlim(xmin, xmax)

    vx = np.arange(2018, 2026)

    for country in list_countries:
        tdata = df2[df2['Region'] == country['name']]

        vy = np.array([
            tdata[2018],
            tdata[2019],
            tdata[2020],
            tdata[2021],
            tdata[2022],
            tdata[2023],
            tdata[2024],
            tdata[2025]
        ])

        if country['name'] == 'Japan':
            lw = lw1
            ax.plot(vx, vy, '-', color=country['color'], linewidth=lw, label=country['label'])
        elif country['name'] == 'South Korea':
            tx = 2025.0
            ty = tdata[2025]
            ax.plot(tx, ty, 'o', color=country['color'], ms=ps, label=country['label'])
        else:
            lw = lw2
            ax.plot(vx, vy, '-', color=country['color'], linewidth=lw, label=country['label'])

    ax.legend(loc='upper right')
    ax.set_ylabel('USD 2025 / MWh')
    plt.tight_layout()
    #plt.show()
    plt.savefig(OUTPUT_PLOT2)

if __name__ == '__main__':

    df1, df2 = load_data()
    plot1(df1)
    plot2(df2)

