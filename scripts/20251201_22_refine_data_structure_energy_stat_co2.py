# 20251104 / 1119 / 1121 / 1201
# -*- coding: utf-8 -*-
import json
#import openpyxl
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#from matplotlib import rcParams
import config 

tC_to_tCO2 = 3.664 # (12.011 + 15.999 x 2) / 12.011

#list_json_file = 'outputs/20251120_21_energy_stat/list_20251020_05_energy_stat_co2_json.txt'
list_json_file = 'outputs/20250721_04_energy_stat/list_20251020_05_energy_stat_co2_json.txt'

sheet_names = [
    '電力', '熱', '合計', 'エネルギー利用', '非エネルギー利用', '石炭', '石炭製品', '原油', 
    '石油製品', '天然ガス', '都市ガス', '総合計_電力･熱寄与間接排出配分後合計', '総合計_エネルギー利用分'
]

# output file names
#jsonfile_data  = 'outputs/20251104_10_1p5CRM_balance_energy/20251104_10_1p5CRM_balance_energy_data.json'
excelfile_data = 'outputs/20251201_21_energy_stat/20251201_22_energy_stat_co2_data_common.xlsx'

with open('inputs/20251201_06_data_structure_common.json', 'r', encoding='utf-8') as f:
    data_structure_common = json.load(f)

dict2_dtype = {
    'id': str,
    'item_name_jp': str,
    'level': int,
    'n_sub': int,
    'unit': str,
}

list_json = []
with open(list_json_file, 'r', encoding='utf-8') as f:
    for line in f:
        list_json.append(line.strip())

with pd.ExcelWriter(excelfile_data) as writer:
    for jsonfile in list_json:
        df2 = pd.read_json(jsonfile, orient='index', dtype=dict2_dtype)
        idx = df2.index.shape[0]

        df2x = pd.DataFrame(columns=df2.columns)

        for item in data_structure_common:
            t_dict = data_structure_common[item]
            if 'ids_to_combine_energy_stat' in t_dict:
                ids_to_combine = t_dict['ids_to_combine_energy_stat']
                #n_sub = t_dict['n_sub_1p5CRM']
                df_subset = df2[df2['id'].isin(ids_to_combine)]
                numeric_sum = df_subset.sum(numeric_only=True)
                # build a row aligned to df2 columns to avoid concatenation of empty/all-NA entries
                new_row = pd.Series(index=df2.columns, dtype=object)
                # fill numeric results
                for k, v in numeric_sum.items():
                    if k in new_row.index:
                        new_row[k] = v
                # fill metadata
                new_row['id'] = t_dict['id']
                new_row['item_name_jp'] = t_dict['item_name_jp']
                new_row['level'] = t_dict['level']
                new_row['n_sub'] = t_dict['n_sub_energy_stat']
                new_row['row'] = ''
                new_row['unit'] = 'MtCO2'
                df2.loc[idx] = new_row
                df2x.loc[idx] = new_row
                idx += 1
                for tid in ids_to_combine:
                    pos = df2[df2['id'] == tid].index[0]
                    df2.loc[pos,'level'] = t_dict['level'] + 1
            else:
                tid = t_dict['id']
                df_subset = df2[df2['id'] == tid]
                if df_subset.shape[0] > 1:
                    print(f"Error: Multiple entries found for id {tid} in {jsonfile}")
                    exit(1)
                elif df_subset.shape[0] == 1:
                    pos = df2[df2['id'] == tid].index[0]
                    if df_subset.iloc[0]['level'] != t_dict['level']:
                        df2.loc[pos,'level'] = t_dict['level']
                    df2x.loc[pos] = df2.loc[pos]
                    df2x.loc[pos,'unit'] = 'MtCO2'
                else:
                    print(f"Error: id {tid} not found in {jsonfile}")
                    exit(1)

        # 1e3 tC to MtCO2
        for col in df2x.columns:
            if col not in ['id', 'item_name_jp', 'item_name_en', 'level', 'n_sub', 'unit', 'row']:
                df2x[col] = df2x[col] * 1.0e-3 * tC_to_tCO2

        df2x.sort_values(by='id', inplace=True, ignore_index=True)

        outputfilename = jsonfile.replace('20250721_04_energy_stat/20251020_05', '20251201_21_energy_stat/20251201_22').replace('_stat_co2_data','_stat_co2_data_common')
        df2x.to_json(outputfilename, orient='index', force_ascii=False, indent=4)
        df2x.to_excel(writer, sheet_name=sheet_names[list_json.index(jsonfile)])

