# -*- coding: utf-8 -*-
import openpyxl
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import config 

rcParams['font.size'] = 20
rcParams['axes.labelsize'] = 24
rcParams['xtick.labelsize'] = 20
rcParams['ytick.labelsize'] = 20
#rcParams['lines.markersize'] = 10
rcParams['lines.linewidth'] = 3
rcParams['font.family'] = 'Hiragino Sans'

INPUT_EXCEL_FILE = 'inputs/ref/20260528_01_製造業GDP_1994_2024.xlsx'
OUTPUT_PLOT = 'charts/20260528_01_plot_gdp_manufacturing.png'


def load_data():
    wb = openpyxl.load_workbook(INPUT_EXCEL_FILE, data_only=True)
    sheet = wb['Sheet1']
    data = sheet.values
    cols = next(data)
    data = list(data)
    df = pd.DataFrame(data, columns=cols)
    return df

def plot(df):

    years = df['year']
    gdp_manu = df['製造業']
    gdp_metal = df['一次金属']
    gdp_material = df['パルプ・紙']+df['化学']+df['石油・石炭製品']+df['窯業・土石']
    gdp_electron = df['電子部品・デバイス']
    gdp_vehicle = df['輸送用機械']
    gdp_total = df['国内総生産']

    lw1 = 3

    fig, ax = plt.subplots(figsize=(15,10))

    ymin = 0.0
    ymax = 40
    ax.set(ylim=(ymin, ymax))
    ax.set_yticks(np.array([0, 10, 20, 30]))
    ax.set_ylabel('割合 (%)')

    ty = gdp_material / gdp_manu * 100.0
    ax.plot(years, ty, '-', linewidth=lw1, color=config.COL_ALIZARIN_MED, label='素材系(一次金属除く)')

    fit = np.polyfit(years-1994.0, ty, 1)
    a = fit[0]
    b = fit[1]
    print('素材系(一次金属除く): %.4f %.4f ' % (a,b))

    ty = gdp_metal / gdp_manu * 100.0
    ax.plot(years, ty, '-', linewidth=lw1, color=config.COL_AMETHYST_MED, label='一次金属')

    fit = np.polyfit(years-1994.0, ty, 1)
    a = fit[0]
    b = fit[1]
    print('一次金属: %.4f %.4f ' % (a, b))

    ty = gdp_electron / gdp_manu * 100.0
    ax.plot(years, ty, '-', linewidth=lw1, color=config.COL_PETER_RIVER_MED, label='電子部品・デバイス')

    fit = np.polyfit(years-1994.0, ty, 1)
    a = fit[0]
    b = fit[1]
    print('電子部品: %.4f %.4f ' % (a, b))

    ty = gdp_vehicle / gdp_manu * 100.0
    ax.plot(years, ty, '-', linewidth=lw1, color=config.COL_GREEN_MED, label='輸送用機械')

    fit = np.polyfit(years-1994.0, ty, 1)
    a = fit[0]
    b = fit[1]
    print('輸送用機械: %.4f %.4f ' % (a, b))

    ty = gdp_manu / gdp_total * 100.0
    ax.plot(years, ty, '--', linewidth=lw1, color=config.COL_CONCRETE_MED, label='製造業/GDP')

    fit = np.polyfit(years-1994.0, ty, 1)
    a = fit[0]
    b = fit[1]
    print('製造業: %.4f %.4f ' % (a, b))

    ax.legend(loc='upper left')

    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT)



if __name__ == '__main__':
    df = load_data()
    plot(df)
    