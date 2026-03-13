# -*- coding: utf-8 -*-
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import config

rcParams['font.size'] = 16
rcParams['axes.labelsize'] = 16
rcParams['xtick.labelsize'] = 14
rcParams['ytick.labelsize'] = 14
#rcParams['lines.markersize'] = 10
rcParams['lines.linewidth'] = 5
rcParams['font.family'] = 'Hiragino Sans'

list_input_csvs = [
    "inputs/EV/japan_carsales_annual.csv",
    "inputs/EV/canada_carsales_annual.csv",
    "inputs/EV/usa_carsales_annual.csv",
    "inputs/EV/turkey_carsales_annual.csv",
    "inputs/EV/france_carsales_annual.csv",
    "inputs/EV/germany_carsales_annual.csv",
    "inputs/EV/norway_carsales_annual.csv",
    "inputs/EV/unitedkingdom_carsales_annual.csv",
    "inputs/EV/china_carsales_annual.csv",
#    "inputs/EV/india_carsales_annual.csv",
    "inputs/EV/indonesia_carsales_annual.csv",
    "inputs/EV/malaysia_carsales_annual.csv",
    "inputs/EV/nepal_carsales_annual.csv",
    "inputs/EV/southkorea_carsales_annual.csv",
    "inputs/EV/sweden_carsales_annual.csv"
]

list_texts = [
    "Japan",
    "Canada",
    "USA",
    "Turkey",
    "France",
    "Germany",
    "Norway",
    "UK",
    "China",
#    "India",
    "Indonesia",
    "Malaysia",
    "Nepal",
    "South Korea",
    "Sweden"
]

list_colors = [
    config.COL_ALIZARIN_MED,
    config.COL_PETER_RIVER_MED,
    config.COL_PETER_RIVER_MED,
    config.COL_GREEN_MED,
    config.COL_GREEN_MED,
    config.COL_GREEN_MED,
    config.COL_GREEN_MED,
    config.COL_GREEN_MED,
    config.COL_ORANGE_MED,
    config.COL_ORANGE_MED,
    config.COL_ORANGE_MED,
    config.COL_ORANGE_MED,
    config.COL_ORANGE_MED,
    config.COL_GREEN_MED,
]

offsets = np.zeros(len(list_input_csvs))
offsets[1] = 0.015
offsets[2] = -0.015
offsets[9] = 0.02
offsets[10] = 0.005

def load_csv(csv_file):
    df0 = pd.read_csv(csv_file)

    df = df0[(df0["YYYYMM"] >= 2018) & (df0["YYYYMM"] <= 2025)]

    df_columns_sub = df.columns.drop("YYYYMM")
    df["total"] = df[df_columns_sub].sum(axis=1)
    if "Plugin hybrid" not in df.columns:
        df["Plugin hybrid"] = 0
    df["EV"] = df["Battery electric"] + df["Plugin hybrid"]

    df2021 = df[df["YYYYMM"] == 2021]

    df["EV_rel2021"] = df["EV"] / df2021["EV"].values[0]

    return df

def setup_plot():
    fig, ax = plt.subplots(figsize=(12,8))

    YEAR1 = 2018
    YEAR2 = 2026
    ax.set_xlim(YEAR1, YEAR2)
    ax.set_ylabel("EV Sales Share (%)")
#    ax.set_yscale("log")
#    ax.set_ylim(-0.02, 1.02)
    ax.set_ylim(-2, 102)

    px = np.array([YEAR1, YEAR2])
    py = np.zeros(2)
    ax.plot(px, py ,"-", color=config.COL_CONCRETE_LIGHT, linewidth=1)
    py = np.array([100.0, 100.0])
    ax.plot(px, py ,"-", color=config.COL_CONCRETE_LIGHT, linewidth=1)

    return fig, ax

def plot_data(df, fig, ax, n):
    col = list_colors[n]
    offset = offsets[n]
    text = list_texts[n]

    if text == "Japan":
        lw = 3
        ps = 5
    else:
        lw = 2
        ps = 3
    fs = 12
    x = df["YYYYMM"]
    y = df["EV"]/df["total"]*100.0

    ax.plot(x, y, "o-", markersize=ps, color=col, linewidth=lw)

    tx = 2025.1
    ty = y.values[-1] + offset*100.0
    ax.text(tx, ty, text, fontsize=fs, color=col, va="center", ha="left")

if __name__ == '__main__':

    fig, ax = setup_plot()

    for i in range(len(list_input_csvs)-1, -1, -1):
        df = load_csv(list_input_csvs[i])
        plot_data(df, fig, ax, i)

    plt.tight_layout()
    plt.savefig("charts/20260313_01_plot_ev_sales_share.png")
