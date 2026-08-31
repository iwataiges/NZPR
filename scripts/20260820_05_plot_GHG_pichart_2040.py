# -*- coding: utf-8 -*-
# 20260507 / 0625
import json
import math

import config
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

# import openpyxl
import pandas as pd
from matplotlib import rcParams

rcParams["font.size"] = 18
rcParams["axes.labelsize"] = 18
rcParams["xtick.labelsize"] = 18
rcParams["ytick.labelsize"] = 18
# rcParams['lines.markersize'] = 10
rcParams["lines.linewidth"] = 3
rcParams["font.family"] = "Hiragino Sans"
rcParams["xtick.labelsize"] = "small"
rcParams["ytick.labelsize"] = "small"

input_json_file1 = "outputs/20251201_31_GHGI/20251205_32_GHGI_ghg_toplevel.json"
input_json_file2 = "inputs/20250218plan_GWC_GHG2030_2040.json"
output_png_file = "charts/20260820_05_plot_GHG_pi_2040.png"

colors = [
    config.COL_CONCRETE_MED,
    config.COL_CONCRETE_DARK,
    config.COL_WET_ASPHALT_MED,
    config.COL_WET_ASPHALT_DARK,
    config.COL_BELIZE_HOLE_DARK,
]


def load_GHGI_data():
    dict_dtype = {
        "id": str,
        "label": str,
        "item_name_jp": str,
        "level": int,
        "n_sub": int,
        "unit": str,
    }
    df1 = pd.read_json(input_json_file1, orient="index", dtype=dict_dtype)
    return df1


def load_NDC_data():
    dict_dtype = {
        "id": str,
        "label": str,
        "item_name": str,
        "2013": float,
        "2030": float,
        "2040_low": float,
        "2040_high": float,
        "unit": str,
    }
    df2 = pd.read_json(input_json_file2, orient="index", dtype=dict_dtype)
    return df2


def plot(df1, df2):
    fig, ax = plt.subplots(figsize=(12, 12))

    df1_2013 = df1["2013"]
    df1_2013_emissions_total = df1_2013[0:5].sum()

    ndc_2040_emissions_total_high = (
        df2.loc["net_GHG"]["2040_high"] * 1.0e3
    )  # MtCO2e to ktCO2e
    rate_2040_2013 = math.sqrt(ndc_2040_emissions_total_high / df1_2013_emissions_total)
    ndc_2040_emissions_high = np.zeros(5)
    ndc_2040_emissions_high[0] = df2.loc["energy-related"]["2040_high"] * 1.0e3
    ndc_2040_emissions_high[1] = df2.loc["non-energy-related"]["2040_high"] * 1.0e3
    ndc_2040_emissions_high[2] = df2.loc["CH4"]["2040_high"] * 1.0e3
    ndc_2040_emissions_high[3] = df2.loc["N2O"]["2040_high"] * 1.0e3
    ndc_2040_emissions_high[4] = df2.loc["F-gas"]["2040_high"] * 1.0e3

    labels = ["エネルギー起源CO2", "非エネルギー起源CO2", "CH4", "N2O", "F-gas"]

    wedges, texts, autotexts = ax.pie(
        ndc_2040_emissions_high, autopct="%1.1f%%", colors=colors, radius=rate_2040_2013
    )

    #    ax.legend(wedges, labels, loc='upper right', bbox_to_anchor=(0.5, 0, 0.5, 1))
    plt.setp(autotexts, color=config.COL_SILVER_LIGHT, weight="bold")

    #    ndc_2040_emissions_total_low = df2.loc['net_GHG']['2040_low'] * 1.0e3
    #    rate_2040_2013_low = math.sqrt(ndc_2040_emissions_total_low / df1_2013_emissions_total)
    #    c = patches.Circle(xy = (0,0), radius = rate_2040_2013_low, fill=False, ec=config.COL_CLOUDS_MED, ls='--', lw=1)
    #    ax.add_patch(c)

    # 1.5CRM
    GHG2040_1p5CRM = 152.062534487042  # MtCO2e
    rate_1p5CRM = math.sqrt(GHG2040_1p5CRM * 1.0e3 / df1_2013_emissions_total)
    c = patches.Circle(
        xy=(0, 0),
        radius=rate_1p5CRM,
        fill=False,
        ec=config.COL_TURQUOISE_MED,
        ls="-.",
        lw=3,
    )
    ax.add_patch(c)

    # extrapolation
    GHG2040_extra = 558.71 # MtCO2e, 20260122_06_plot_GHG_total.py
    rate_extra = math.sqrt(GHG2040_extra * 1.0e3 / df1_2013_emissions_total)
    c = patches.Circle(
        xy=(0, 0),
        radius=rate_extra,
        fill=False,
        ec=config.COL_POMEGRANATE_MED,
        ls="--",
        lw=4,
    )
    ax.add_patch(c)

    plt.tight_layout()
    # plt.show()
    plt.savefig(output_png_file)


if __name__ == "__main__":
    df_ghgi = load_GHGI_data()
    df_ndc = load_NDC_data()
    plot(df_ghgi, df_ndc)
