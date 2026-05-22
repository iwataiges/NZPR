# -*- coding: utf-8 -*-
# 20260520 GHG intensity per GDP, with Vashoold 2023
import json
import csv
import openpyxl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import config 

rcParams['font.size'] = 18
rcParams['axes.labelsize'] = 18
rcParams['xtick.labelsize'] = 18
rcParams['ytick.labelsize'] = 18
#rcParams['lines.markersize'] = 10
rcParams['lines.linewidth'] = 3
rcParams['font.family'] = 'Hiragino Sans'
rcParams['xtick.labelsize'] = 'small'
rcParams['ytick.labelsize'] = 'small'

YEAR1_START = 2010
YEAR1_END   = 2024
list_year1 = []
for i in range(YEAR1_START, YEAR1_END):
    list_year1.append('%d' % (i))

YEAR1N_START = 2014
YEAR1N_END   = 2024
list_year1n = []
for i in range(YEAR1N_START, YEAR1N_END):
    list_year1n.append('%d' % (i))

YEAR1A_START = 2010
YEAR1A_END   = 2019
list_year1a = []
for i in range(YEAR1A_START, YEAR1A_END):
    list_year1a.append('%d' % (i))

YEAR3_START = 2018
YEAR3_END   = 2050

IGESRM_BALNC_GHG_JSON_FILE = 'outputs/20251208_01_1p5CRM_GHG/20251208_04_1p5CRM_balance_GHG_data.json'
IGESRM_STEPS_GHG_JSON_FILE = 'outputs/20251208_01_1p5CRM_GHG/20251208_04_1p5CRM_steps_GHG_data.json'

def load_GHGI_data():
    input_json_file = 'outputs/20251201_31_GHGI/20251205_32_GHGI_ghg_toplevel.json'
    dict_dtype = {
        'id': str,
        'label': str,
        'item_name_jp': str,
        'level': int,
        'n_sub': int,
        'unit': str,
    }
    df1 = pd.read_json(input_json_file, orient='index', dtype=dict_dtype)
    return df1

def load_GDP_data():
    input_excel_file = 'inputs/ref/20260520_01_GDP_JP.xlsx'
    wb = openpyxl.load_workbook(input_excel_file)
    sheet = wb['Sheet1']
    data = sheet.values
    cols = next(data)
    data = list(data)
    df2 = pd.DataFrame(data, columns=cols)
    df2_sel = df2[['Year', 'WB GDP per capita, PPP (constant 2021 international $)', 'Population, total']]
    return df2_sel

def load_vashold_2023_data():
    input_csv_file = 'inputs/ref/vashold2023/japan_emissions_intensity.csv'
    dict_dtype = {
        'year': int,
        'total_emissions_MtCO2eq': float,
        'total_gdp_trillion_intl': float,
        'emissions_intensity_tCO2eq_per_10k_intl': float,
        'intensity_q16_68pct_lo': float,
        'intensity_q84_68pct_hi': float,
        'intensity_q5_90pct_lo': float,
        'intensity_q95_90pct_hi': float,
    }
    df3 = pd.read_csv(input_csv_file, dtype=dict_dtype)
    return df3

def load_IGESRM_GHG_data():
    dict_dtype = {
        "Year": int,
        "GHG排出量(DACCS含、森林吸収含まず)": float,
        "GHG(森林吸収、DACCS含)": float,
        "CO2(森林吸収、DACCS含)": float,
        "その他GHG":float,
        "森林吸収源":float,
        "DACCS":float,
        "CCS回収分":float
    }
    df4 = pd.read_json(IGESRM_BALNC_GHG_JSON_FILE, orient='index', dtype=dict_dtype)
    df5 = pd.read_json(IGESRM_STEPS_GHG_JSON_FILE, orient='index', dtype=dict_dtype)
    
    return df4, df5

def plot(df1, df2, df3, df4, df5):
    df1_net_subset = df1[list_year1n] # 2014-2023
    df1_emissions = df1[df1['id'] != '06'] # exclude LULUCF
    df1_emissions_subset = df1_emissions[list_year1]

    df2_subset = df2[(df2['Year'] >= YEAR1_START) & (df2['Year'] < YEAR1_END)]

    emissions = df1_emissions_subset.sum().values
    emissions = emissions*1.0e-3 # to MtCO2e
    gdppc = df2_subset['WB GDP per capita, PPP (constant 2021 international $)'].values
    population = df2_subset['Population, total'].values
    gdp = gdppc * population
    intensity = emissions * 1.0e6 * 1.0e4 / gdp # tCO2eq per 10k intl$

    df3_subset = df3[(df3['year'] >= YEAR3_START) & (df3['year'] <= YEAR3_END)]

    year_1p5CRM = df4['Year'].values
    ghg_1p5CRM_balnc = df4['GHG排出量(DACCS含、森林吸収含まず)'].values # MtCO2e
    ghg_1p5CRM_steps = df5['GHG排出量(DACCS含、森林吸収含まず)'].values # MtCO2e

    JPY2015_to_intl2021 = 0.01005895
    gdp_1p5CRM_2020 = 539646 * 1.0e9 # 2020 GDP, 2015年暦年連鎖価格 円
    gdp_1p5CRM_balnc_2030 = 602 * 1.0e12 # 2030 GDP
    gdp_1p5CRM_balnc_2050 = 660 * 1.0e12 # 2050 GDP
    gdp_1p5CRM_steps_2030 = 660 * 1.0e12
    gdp_1p5CRM_steps_2050 = 715 * 1.0e12

    gdp_1p5CRM_balnc = np.zeros(len(year_1p5CRM))
    gdp_1p5CRM_steps = np.zeros(len(year_1p5CRM))
    for i in range(len(year_1p5CRM)):
        year = year_1p5CRM[i]
        if year < 2030:
            gdp_1p5CRM_balnc[i] = gdp_1p5CRM_2020 * (2030 - year) / 10.0 + gdp_1p5CRM_balnc_2030 * (year - 2020) / 10.0
            gdp_1p5CRM_steps[i] = gdp_1p5CRM_2020 * (2030 - year) / 10.0 + gdp_1p5CRM_steps_2030 * (year - 2020) / 10.0
        else:
            gdp_1p5CRM_balnc[i] = gdp_1p5CRM_balnc_2030 * (2050 - year) / 20.0 + gdp_1p5CRM_balnc_2050 * (year - 2030) / 20.0
            gdp_1p5CRM_steps[i] = gdp_1p5CRM_steps_2030 * (2050 - year) / 20.0 + gdp_1p5CRM_steps_2050 * (year - 2030) / 20.0
    gdp_1p5CRM_balnc = gdp_1p5CRM_balnc * JPY2015_to_intl2021 # to 2021 intl$
    gdp_1p5CRM_steps = gdp_1p5CRM_steps * JPY2015_to_intl2021 # to 2021 intl$ 
#    for i in range(len(year_1p5CRM)):
#        print('%d %10.3e %10.3e ' % (year_1p5CRM[i], gdp_1p5CRM_balnc[i], gdp_1p5CRM_steps[i]))

    intensity_1p5CRM_balnc = ghg_1p5CRM_balnc * 1.0e6 * 1.0e4 / gdp_1p5CRM_balnc # tCO2eq per 10k intl$
    intensity_1p5CRM_steps = ghg_1p5CRM_steps * 1.0e6 * 1.0e4 / gdp_1p5CRM_steps # tCO2eq per 10k intl$


    fig, ax = plt.subplots(figsize=(12, 8))

    lw1 = 3
    lw2 = 2
    lw3 = 1.5

    ymin = 0.0
    ymax = 3.0
    ax.set_ylim(ymin, ymax)

    # GHG gross emissions
    tx = np.arange(YEAR1_START, YEAR1_END)
    ax.plot(tx, intensity, 'o-', color=config.COL_MIDNIGHT_BLUE_LIGHT, linewidth=lw1)

    # GHG net emissions
#    tx = np.arange(YEAR1N_START, YEAR1N_END)
#    ty = df1_net_subset.sum().values
#    ty = ty*1.0e-3 # to MtCO2e
#
#    ax.plot(tx, ty, 'o-', color=config.COL_MIDNIGHT_BLUE_MED, linewidth=lw1)


    # Linear fit (2014 - 2023)
    YEAR_BASE = 2013
    df1_emissions_2014_2023 = df1_emissions_subset[list_year1n].drop(columns=['2020'])
    df2_subset_2014_2023 = df2[(df2['Year'].isin([2014, 2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023]))]
    gdppc_2014_2023 = df2_subset_2014_2023['WB GDP per capita, PPP (constant 2021 international $)'].values
    population_2014_2023 = df2_subset_2014_2023['Population, total'].values
    gdp_2014_2023 = gdppc_2014_2023 * population_2014_2023

    emissions = df1_emissions_2014_2023.sum().values * 1.0e-3
    intensity = emissions * 1.0e6 * 1.0e4 / gdp_2014_2023 # tCO2eq per 10k intl$
    ty = intensity

    tx = np.array([2014, 2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023])
    tx = tx - YEAR_BASE

    fit1 = np.polyfit(tx, ty, 1)
    a = fit1[0]
    b = fit1[1]
    print('%d-%d %f %f' % (YEAR1N_START, YEAR1N_END, a, b))
    
    YEAR2_START = 2014
    YEAR2_END   = 2051
    tx = np.array([YEAR2_START, YEAR2_END])
    y1 = a*(YEAR2_START - YEAR_BASE) + b
    y2 = a*(YEAR2_END   - YEAR_BASE) + b
    ty = np.array([y1, y2])
    ax.plot(tx, ty, '-.', color=config.COL_POMEGRANATE_MED, linewidth=lw2)

    # Linear fit (2019 - 2023)
#    FIT_YEAR_START = 2019
#    FIT_YEAR_END   = 2024
#    list_fit_year = []
#    for i in range(FIT_YEAR_START, FIT_YEAR_END):
#        list_fit_year.append('%d' % (i))
#
#    tx = np.arange(FIT_YEAR_START, FIT_YEAR_END)
#    tx = tx - YEAR_BASE
#    df1_net_subset2 = df1_net_subset[list_fit_year]
#    ty = df1_net_subset2.sum().values
#    ty = ty*1.0e-3 # to MtCO2e
#    fit2 = np.polyfit(tx, ty, 1)
#    a = fit2[0]
#    b = fit2[1]
#    print('%d-%d %f %f' % (FIT_YEAR_START, FIT_YEAR_END, a, b))
#        
#    tx = np.array([FIT_YEAR_START, YEAR2_END])
#    y1 = a*(FIT_YEAR_START - YEAR_BASE) + b
#    y2 = a*(YEAR2_END   - YEAR_BASE) + b
#    ty = np.array([y1, y2])
#    ax.plot(tx, ty, '--', color=config.COL_POMEGRANATE_DARK, linewidth=lw2)

    # 1p5CRM
    tx = year_1p5CRM[3:] # from 2025
    ty1 = intensity_1p5CRM_balnc[3:]
    ax.plot(tx, ty1, '-', color=config.COL_TURQUOISE_MED, linewidth=lw1, label='1.5CRM Balanced')
    ty2 = intensity_1p5CRM_steps[3:]
    ax.plot(tx, ty2, '-', color=config.COL_ORANGE_MED, linewidth=lw1, label='1.5CRM Steps')


    # 2030 NDC
    tx = 2030
    GDP_2030 = 660 * 1.0e12 / 99.4139 # 2030 GDP in 2021 intl$
    GHG_2030_1 = 8.14 * 1.0e8
    GHG_2030_2 = (8.14 + 7.04 - 7.60) * 1.0e8
    tx = np.array([2030, 2030])
    ty = np.array([GHG_2030_1, GHG_2030_2]) / GDP_2030 * 1.0e4 # tCO2eq per 10k intl$
    ax.plot(tx, ty, 'o-', color=config.COL_ALIZARIN_MED, markersize=10)

    # 2040 NDC
    tx = 2040
    GDP_2040 = 5.574e12 * 1.38 # 2040 GDP in 2021 intl$
    GHG_2040 = 469 * 1.0e6
    ty = GHG_2040 / GDP_2040 * 1.0e4 # tCO2eq per 10k intl$
    ax.plot(tx, ty, 'o', color=config.COL_ALIZARIN_MED, markersize=10)

    # 2040 技術進展シナリオ
    GHG_2040 = (469 + 174) * 1.0e6
    ty = GHG_2040 / GDP_2040 * 1.0e4 # tCO2eq per 10k intl$
    ax.plot(tx, ty, '^', color=config.COL_ALIZARIN_DARK, markersize=10)


    # Vashold 2023
    ## calculate GHG difference between GHGI and Vashold 2023 for 2010-2018, and use the mean factor as the offset for Vashold 2023
    ghg_vashold_2010_2018 = df3[(df3['year'] >= 2010) & (df3['year'] <= 2018)]['total_emissions_MtCO2eq'].values
    df1_emissions_subset2 = df1_emissions[list_year1a]
    ghg_GHGI_2010_2018 = df1_emissions_subset2.sum().values * 1.0e-3
    ghg_factors = ghg_GHGI_2010_2018 / ghg_vashold_2010_2018
    ghg_factor_mean = np.mean(ghg_factors)
    print('GHG factor (2010-2018) mean: %f' % (ghg_factor_mean))

    GDP_adjust_2021_2011 = 1.1312 # 2021 vs 2011 international dollars
    tx = df3_subset['year'].values

    ty1_low = df3_subset['intensity_q5_90pct_lo'].values
    ty1_low = ty1_low * ghg_factor_mean / GDP_adjust_2021_2011
    ty1_hgh = df3_subset['intensity_q95_90pct_hi'].values
    ty1_hgh = ty1_hgh * ghg_factor_mean / GDP_adjust_2021_2011
    ax.fill_between(tx, ty1_low, ty1_hgh, color=config.COL_AMETHYST_LIGHT, alpha=0.5, label='Vashold 2023 90%% range')

    ty2_low = df3_subset['intensity_q16_68pct_lo'].values
    ty2_low = ty2_low * ghg_factor_mean / GDP_adjust_2021_2011
    ty2_hgh = df3_subset['intensity_q84_68pct_hi'].values
    ty2_hgh = ty2_hgh * ghg_factor_mean / GDP_adjust_2021_2011
    ax.fill_between(tx, ty2_low, ty2_hgh, color=config.COL_AMETHYST_MED, alpha=0.5, label='Vashold 2023 68%% range')

    ty3 = df3_subset['emissions_intensity_tCO2eq_per_10k_intl'].values
    ty3 = ty3 * ghg_factor_mean / GDP_adjust_2021_2011
    ax.plot(tx, ty3, '-', color=config.COL_AMETHYST_DARK, linewidth=lw3, label='Vashold 2023')


    # Put Gas Type
    ax.text(YEAR1_START, ymax - (ymax-ymin)*0.07, 'GHG Intensity', color=config.COL_ASBESTOS_DARK, fontsize=24)

    #ax.set_title('CO2 (energy-related)')
    ax.set_ylabel('tCO2e per 10k intl$')
    #ax.legend(loc='lower left')
    plt.tight_layout()
    #plt.show()
    plt.savefig('charts/20260520_02_plot_GHG_intensity_w_vashold2023.png')

if __name__ == '__main__':
    df_ghgi = load_GHGI_data()
    df_gdp = load_GDP_data()
    df_vahold2023 = load_vashold_2023_data()
    df_1p5CRM_balnc, df_1p5CRM_steps = load_IGESRM_GHG_data()

    plot(df_ghgi, df_gdp, df_vahold2023, df_1p5CRM_balnc, df_1p5CRM_steps)
