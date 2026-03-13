# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rcParams
import config

rcParams['font.size'] = 16
rcParams['axes.labelsize'] = 16
rcParams['xtick.labelsize'] = 18
rcParams['ytick.labelsize'] = 18
#rcParams['lines.markersize'] = 10
rcParams['lines.linewidth'] = 5
rcParams['font.family'] = 'Hiragino Sans'
#rcParams['xtick.labelsize'] = 'small'
#rcParams['ytick.labelsize'] = 'small'

list_input_csvs = [
    "inputs/EV/japan_carsales_annual.csv",
#    "inputs/EV/canada_carsales_annual.csv",
    "inputs/EV/usa_carsales_annual.csv",
#    "inputs/EV/turkey_carsales_annual.csv",
#    "inputs/EV/france_carsales_annual.csv",
    "inputs/EV/germany_carsales_annual.csv",
#    "inputs/EV/norway_carsales_annual.csv",
#    "inputs/EV/unitedkingdom_carsales_annual.csv",
#    "inputs/EV/china_carsales_annual.csv",
#    "inputs/EV/india_carsales_annual.csv",
#    "inputs/EV/indonesia_carsales_annual.csv",
#    "inputs/EV/malaysia_carsales_annual.csv",
#    "inputs/EV/nepal_carsales_annual.csv",
#    "inputs/EV/southkorea_carsales_annual.csv",
#    "inputs/EV/sweden_carsales_annual.csv"
]

list_texts = [
    "Japan",
#    "Canada",
    "USA",
#    "Turkey",
#    "France",
    "Germany",
#    "Norway",
#    "UK",
#    "China",
#    "India",
#    "Indonesia",
#    "Malaysia",
#    "Nepal",
#    "South Korea",
#    "Sweden"
]

list_colors = [
    {
        "type": "Internal Combustion",
        "color": config.COL_CONCRETE_MED,
    },
    {
        "type": "Non-plugin Hybrid",
        "color": config.COL_ORANGE_MED,
    },
    {
        "type": "Plugin Hybrid",
        "color": config.COL_NEPHRITIS_MED,
    },
    {
        "type": "Battery Electric",
        "color": config.COL_PETER_RIVER_MED,
    },
    {
        "type": "Hydrogen",
        "color": config.COL_SILVER_MED,
    },
    {
        "type": "Other",
        "color": config.COL_SILVER_MED,
    }
]

YEAR1 = 2018
YEAR2 = 2026

def load_csv(csv_file):
    df0 = pd.read_csv(csv_file)

    df = df0[(df0["YYYYMM"] >= 2018) & (df0["YYYYMM"] <= 2025)]

    df_columns_sub = df.columns.drop("YYYYMM")
    df["total"] = df[df_columns_sub].sum(axis=1)
    if "Plugin hybrid" not in df.columns:
        df["Plugin hybrid"] = 0
    if "Internal combustion" not in df.columns:
        df["Internal combustion"] = df["Diesel"] + df["Petrol"]

#    df["EV"] = df["Battery electric"] + df["Plugin hybrid"]

    return df

def setup_plot():
    fig, axes = plt.subplots(1, 3, figsize=(16,8), tight_layout=True)

    for i in range(3):
        ax = axes[i]
        x0 = YEAR1 - 0.2
        x1 = YEAR2 - 0.8
        ax.set_xlim(x0, x1)
        ax.set_ylim(0.0, 1.0)
        if i == 0:
            ytext = "Sales Share"
        else:
            ytext = ""
        ax.set_ylabel(ytext)

        px = np.array([x0, x1])
        py = np.zeros(2)
        ax.plot(px, py ,"-", color=config.COL_CONCRETE_LIGHT, linewidth=1)

        px = np.array([YEAR1, YEAR2])
        py = np.zeros(2)
        ax.plot(px, py ,"-", color=config.COL_CONCRETE_LIGHT, linewidth=1)
        py = np.array([100.0, 100.0])
        ax.plot(px, py ,"-", color=config.COL_CONCRETE_LIGHT, linewidth=1)

    return fig, axes

def plot_data(df, fig, ax, n):
    text = list_texts[n]
    width = 0.5

    ax.set_title(text)

    for i in range(YEAR1, YEAR2):
        df_sub = df[df["YYYYMM"] == i]
        r_ICE = df_sub["Internal combustion"].values[0] / df_sub["total"].values[0]
        r_HEV = df_sub["Non-plugin hybrid"].values[0] / df_sub["total"].values[0]
        r_PHEV = df_sub["Plugin hybrid"].values[0] / df_sub["total"].values[0]
        r_BEV = df_sub["Battery electric"].values[0] / df_sub["total"].values[0]

        x = i
        y0 = 0.0
        y1 = r_ICE
        wid = 0.6 / len(list_input_csvs)
        ax.bar(x, y1, width=width, bottom=y0, color=list_colors[0]["color"])
        y0 = y1
        y1 = r_HEV
        ax.bar(x, y1, width=width, bottom=y0, color=list_colors[1]["color"])
        y0 = y0+y1
        y1 = r_PHEV
        ax.bar(x, y1, width=width, bottom=y0, color=list_colors[2]["color"])
        y0 = y0+y1
        y1 = r_BEV
        ax.bar(x, y1, width=width, bottom=y0, color=list_colors[3]["color"])
        y0 = y0+y1
        y1 = 1.0 - y0
        ax.bar(x, y1, width=width, bottom=y0, color=list_colors[4]["color"])

def plot_legend(fig, ax):
    handles = []
    labels = []
    for i in range(4):
        item = list_colors[3-i]
        handles.append(plt.Rectangle((0,0),1,1, color=item["color"]))
        labels.append(item["type"])
    ax.legend(handles, labels, loc="lower right", fontsize=14)

if __name__ == '__main__':

    fig, axes = setup_plot()

    for i in range(len(list_input_csvs)):
        df = load_csv(list_input_csvs[i])
        plot_data(df, fig, axes[i], i)

    plot_legend(fig, axes[1])

    plt.tight_layout()
    plt.savefig("charts/20260313_02_plot_bars_vehicle_sales.png")
