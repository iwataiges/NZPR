# 20251218
# -*- coding: utf-8 -*-
import json
import openpyxl
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#from matplotlib import rcParams
import config 

INPUT_ENERGY_ELEC_JSON_FILE = 'outputs/20251201_01_1p5CRM_balance_energy/20251201_11_1p5CRM_balance_energy_data_common_07_電力.json'
INPUT_CO2_ELEC_JSON_FILE    = 'outputs/20251201_02_1p5CRM_balance_co2/20251119_12_1p5CRM_balance_co2_data_common_07_電力.json'

INPUT_ENERGY_ENERGY_JSON_FILE   = 'outputs/20251201_01_1p5CRM_balance_energy/20251201_11_1p5CRM_balance_energy_data_common_10_エネルギー利用.json'
INPUT_CO2_ENERGY_ELEC_JSON_FILE = 'outputs/20251201_02_1p5CRM_balance_co2/20251119_12_1p5CRM_balance_co2_data_common_10_エネルギー利用.json'

OUTPUT_EXCEL_FILE = 'outputs/20251218_01_intensity/20251218_02_1p5CRM_balance_intensity_data_common.xlsx'
OUTPUT_ELEC_JSON_FILE   = 'outputs/20251218_01_intensity/20251218_02_1p5CRM_balance_intensity_data_common_07_電力.json'
OUTPUT_ENERGY_JSON_FILE = 'outputs/20251218_01_intensity/20251218_02_1p5CRM_balance_intensity_data_common_10_エネルギー利用.json'


def load_data():
    dict_dtype = {
        'id': str,
        'item_name_jp': str,
        'level': int,
        'n_sub': int,
        'unit': str,
    }
    df1 = pd.read_json(INPUT_ENERGY_ELEC_JSON_FILE, orient='index', dtype=dict_dtype)
    df2 = pd.read_json(INPUT_CO2_ELEC_JSON_FILE, orient='index', dtype=dict_dtype)

    df3 = pd.read_json(INPUT_ENERGY_ENERGY_JSON_FILE, orient='index', dtype=dict_dtype)
    df4 = pd.read_json(INPUT_CO2_ENERGY_ELEC_JSON_FILE, orient='index', dtype=dict_dtype)

    return df1, df2, df3, df4

def calc_intensity(df_energy_elec, df_co2_elec, df_energy_energy, df_co2_energy):
    df_intensity_elec = df_co2_elec.copy()
    df_intensity_energy = df_co2_energy.copy()

    list_years = ['baseyear', '2030', '2040', '2050']

    for year in list_years:
        df_e_elec = df_energy_elec[year]
        df_c_elec = df_co2_elec[year]
        df_intensity_elec[year] = df_c_elec / df_e_elec

        df_e_energy = df_energy_energy[year]
        df_c_energy = df_co2_energy[year]
        df_intensity_energy[year] = df_c_energy / df_e_energy

    df_intensity_elec['unit'] = 'MtCO2/TJ'
    df_intensity_energy['unit'] = 'MtCO2/TJ'

    return df_intensity_elec, df_intensity_energy

if __name__ == '__main__':
    df_energy_elec, df_co2_elec, df_energy_energy, df_co2_energy = load_data()

    df_intensity_elec, df_intensity_energy = calc_intensity(df_energy_elec, df_co2_elec, df_energy_energy, df_co2_energy)

    df_intensity_elec.to_json(OUTPUT_ELEC_JSON_FILE, orient='index', force_ascii=False)
    df_intensity_energy.to_json(OUTPUT_ENERGY_JSON_FILE, orient='index', force_ascii=False)

    with pd.ExcelWriter(OUTPUT_EXCEL_FILE) as writer:
        df_intensity_elec.to_excel(writer, sheet_name='電力')
        df_intensity_energy.to_excel(writer, sheet_name='エネルギー利用')

