# -*- coding: utf-8 -*-
import json
import openpyxl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import config

rcParams['font.size'] = 16
rcParams['axes.labelsize'] = 16
rcParams['xtick.labelsize'] = 18
rcParams['ytick.labelsize'] = 18
#rcParams['lines.markersize'] = 10
rcParams['lines.linewidth'] = 5
rcParams['font.family'] = 'Hiragino Sans'

INPUT_EXCEL_FILE = 'inputs/ref/20260527製造業要因分解_FY2024.xlsx'

OUTPUT_PLOT1 = 'charts/20260527_02_plot_bars_manufacturing_gdp_FY2024.png'
OUTPUT_PLOT2 = 'charts/20260527_02_plot_bars_manufacturing_gdp_energy_FY2024.png'
OUTPUT_PLOT3 = 'charts/20260527_02_plot_bars_manufacturing_energy_FY2024.png'

sectors_to_plot = [
    'パルプ・紙',
    '化学', 
    '石油・石炭製品',
    '窯業・土石',
    '一次金属',
    '電子部品・デバイス',
    '電気機械',
    '情報・通信機器',
    '輸送用機械',
    'その他',
]
sectors_to_plot_text = [
    'パルプ・紙',
    '化学', 
    '石油・石炭\n製品',
    '窯業・土石',
    '一次金属',
    '電子部品・\nデバイス',
    '電気機械',
    '情報・通信\n機器',
    '輸送用機械',
    'その他',
]
sector_colors = [
    config.COL_CONCRETE_MED,
    config.COL_CONCRETE_MED,
    config.COL_CONCRETE_MED,
    config.COL_CONCRETE_MED,
    config.COL_CONCRETE_MED,
    config.COL_BELIZE_HOLE_MED,
    config.COL_BELIZE_HOLE_MED,
    config.COL_BELIZE_HOLE_MED,
    config.COL_BELIZE_HOLE_MED,
    config.COL_BELIZE_HOLE_MED,
]

def load_data():
    wb = openpyxl.load_workbook(INPUT_EXCEL_FILE, data_only=True)
    sheet = wb['for_plot']
    data = sheet.values
    cols = next(data)
    data = list(data)
    df = pd.DataFrame(data, columns=cols)
    return df

def plot1(df):
    fig, ax = plt.subplots(figsize=(15,10))

    width1 = 0.3
    fs1 = 16
    fs2 = 24
    lw1 = 3
    ms1 = 15
    xoff = 0.25

    xmin = -0.5
    xmax = len(sectors_to_plot)-0.5
    ymin = 0.0
    ymax = 2.6
    ax.set(xlim=(xmin,xmax), ylim=(ymin, ymax))
    ax.set_xticks([])

    df_sel = df[df['部門'].isin(sectors_to_plot)]

    xp = 0.0
    ct = 0
    for i in range(len(df_sel)):
        v = df_sel.iloc[i]['実質GDP 2024/2013']
        ax.bar(xp, v, width1, align='center', color=sector_colors[ct])
        ax.text(xp, -0.02, sectors_to_plot_text[ct], fontsize=fs1, ha='center', va='top')

        w = df_sel.iloc[i]['生産活動指数 (経団連) 2024/2013']
        if pd.isnull(w) == False:
            ax.plot(xp, w, 'o', markersize=ms1, color=config.COL_ALIZARIN_MED)

        ct += 1
        xp += 1.0

    v = df[df['部門']=='国内総生産']['実質GDP 2024/2013']
    tx = np.array([xmin+xoff, xmax-xoff])
    ty = np.array([v, v])
    ax.plot(tx, ty, '--', linewidth=lw1, color=config.COL_CARROT_MED)

    v = df[df['部門']=='製造業']['実質GDP 2024/2013']
    tx = np.array([xmin+xoff, xmax-xoff])
    ty = np.array([v, v])
    ax.plot(tx, ty, '-', linewidth=lw1, color=config.COL_PETER_RIVER_MED)

    ax.text(xmin+(xmax-xmin)*0.02, ymax-(ymax-ymin)*0.05, '生産高 2024/2013比', fontsize=fs2, ha='left', va='center')

    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT1)
    
def plot2(df):
    fig, ax = plt.subplots(figsize=(15,10))

    width1 = 0.3
    fs1 = 16
    fs2 = 24
    lw1 = 3
    xoff = 0.25

    xmin = -0.5
    xmax = len(sectors_to_plot)-0.5
    ymin = 0.0
    ymax = 2.6
    ax.set(xlim=(xmin,xmax), ylim=(ymin, ymax))
    ax.set_xticks([])

    df_sel = df[df['部門'].isin(sectors_to_plot)]

    xp = 0.0
    ct = 0
    for i in range(len(df_sel)):
        v = df_sel.iloc[i]['実質GDP/エネルギー 2024/2013']

        ax.bar(xp, v, width1, align='center', color=sector_colors[ct])
        ax.text(xp, -0.02, sectors_to_plot_text[ct], fontsize=fs1, ha='center', va='top')
        ct += 1
        xp += 1.0

    v = df[df['部門']=='国内総生産']['実質GDP/エネルギー 2024/2013']
    tx = np.array([xmin+xoff, xmax-xoff])
    ty = np.array([v, v])
    ax.plot(tx, ty, '--', linewidth=lw1, color=config.COL_CARROT_MED)

    v = df[df['部門']=='製造業']['実質GDP/エネルギー 2024/2013']
    tx = np.array([xmin+xoff, xmax-xoff])
    ty = np.array([v, v])
    ax.plot(tx, ty, '-', linewidth=lw1, color=config.COL_PETER_RIVER_MED)

    ax.text(xmin+(xmax-xmin)*0.02, ymax-(ymax-ymin)*0.05, 'エネルギーあたり生産高 2024/2013比', fontsize=fs2, ha='left', va='center')

    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT2)

def plot3(df):
    fig, ax = plt.subplots(figsize=(15,10))

    width1 = 0.3
    fs1 = 16
    fs2 = 24
    lw1 = 3
    xoff = 0.25

    xmin = -0.5
    xmax = len(sectors_to_plot)-0.5
    ymin = 0.0
    ymax = 1.2
    ax.set(xlim=(xmin,xmax), ylim=(ymin, ymax))
    ax.set_xticks([])
    ax.set_yticks(np.arange(0.0, 1.1, 0.2))

    df_sel = df[df['部門'].isin(sectors_to_plot)]

    xp = 0.0
    ct = 0
    for i in range(len(df_sel)):
        v = df_sel.iloc[i]['FEC 2024/2013']

        ax.bar(xp, v, width1, align='center', color=sector_colors[ct])
        ax.text(xp, -0.02, sectors_to_plot_text[ct], fontsize=fs1, ha='center', va='top')
        ct += 1
        xp += 1.0

    v = df[df['部門']=='国内総生産']['FEC 2024/2013']
    tx = np.array([xmin+xoff, xmax-xoff])
    ty = np.array([v, v])
    ax.plot(tx, ty, '--', linewidth=lw1, color=config.COL_CARROT_MED)

    v = df[df['部門']=='製造業']['FEC 2024/2013']
    tx = np.array([xmin+xoff, xmax-xoff])
    ty = np.array([v, v])
    ax.plot(tx, ty, '-', linewidth=lw1, color=config.COL_PETER_RIVER_MED)

    ax.text(xmin+(xmax-xmin)*0.02, ymax-(ymax-ymin)*0.05, 'エネルギー消費量 2024/2013比', fontsize=fs2, ha='left', va='center')

    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT3)

if __name__ == '__main__':
    df = load_data()
    plot1(df)
    plot2(df)
    plot3(df)
