# 20251203
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

# output file names
jsonfile_data   = 'outputs/20251201_31_GHGI/20251203_32_GHGI_ghg_toplevel.json'
excelfile_data  = 'outputs/20251201_31_GHGI/20251203_32_GHGI_ghg_toplevel.xlsx'

list_ids_to_select = [
    '01_01', # energy-related CO2
    '01_02', # non-energy-related CO2
    '03',    # CH4
    '04',    # N2O
    '05',    # F-gas
]
df1 = pd.read_json(input_json_file, orient='index', dtype=dict_dtype)
df1_subset = df1[df1['id'].isin(list_ids_to_select)]

df1_subset.to_json(jsonfile_data, orient='index', force_ascii=False, indent=4)
df1_subset.to_excel(excelfile_data, index=False)

