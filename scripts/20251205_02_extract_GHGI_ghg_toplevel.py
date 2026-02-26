# 20251203 / 1205
# -*- coding: utf-8 -*-
import json
import pandas as pd
import numpy as np
import config 

input_json_file = 'outputs/20250506_GHGI/20250506_05_ghg_data.json'
dict_dtype = {
    'id': str,
    'label': str,
    'item_name_jp': str,
    'level': int,
    'n_sub': int,
    'unit': str,
}

dict_lulucf = {
    "300": {
        "id":"06",
        "label":"NDC-LULUCF",
        "level":0,
        "n_sub":0,
        "unit":"ktCO2e",
        "item_name_jp":"NDC-LULUCF",
        "2014": -69014.47964,
        "2015": -65737.64206,
        "2016": -64238.03992,
        "2017": -63687.60298,
        "2018": -62204.4405,
        "2019": -58216.61997,
        "2020": -55954.3649,
        "2021": -56597.2489,
        "2022": -53776.98327,
        "2023": -53694.26613
    }
}

df2 = pd.DataFrame.from_dict(dict_lulucf, orient='index')

# output file names
jsonfile_data   = 'outputs/20251201_31_GHGI/20251205_32_GHGI_ghg_toplevel.json'
excelfile_data  = 'outputs/20251201_31_GHGI/20251205_32_GHGI_ghg_toplevel.xlsx'

list_ids_to_select = [
    '01_01', # energy-related CO2
    '01_02', # non-energy-related CO2
    '03',    # CH4
    '04',    # N2O
    '05',    # F-gas
]
df1 = pd.read_json(input_json_file, orient='index', dtype=dict_dtype)
df1_subset = df1[df1['id'].isin(list_ids_to_select)]

df3 = pd.concat([df1_subset, df2], ignore_index=True)

df3.to_json(jsonfile_data, orient='index', force_ascii=False, indent=4)
df3.to_excel(excelfile_data, index=False)

