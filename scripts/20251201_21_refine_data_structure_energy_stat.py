# 20251104 / 1119 / 1121 / 1201
# -*- coding: utf-8 -*-
import json
#import openpyxl
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#from matplotlib import rcParams
import config 

#list_json_file = 'outputs/20251120_21_energy_stat/list_20250721_04_energy_stat_json.txt'
list_json_file = 'outputs/20250721_04_energy_stat/list_20250721_04_energy_stat_json.txt'

sheet_names = [
    '電力', '熱', '合計', 'エネルギー利用', '非エネルギー利用', '石炭', '石炭製品', '原油', 
    '石油製品', '天然ガス', '都市ガス', '再生可能エネルギー(水力を除く)', '水力発電（揚水除く）', 
    '揚水発電', '未活用エネルギー', '原子力発電'
]

# output file names
#jsonfile_data  = 'outputs/20251104_10_1p5CRM_balance_energy/20251104_10_1p5CRM_balance_energy_data.json'
excelfile_data = 'outputs/20251201_21_energy_stat/20251201_21_energy_stat_data_common.xlsx'

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
                new_row['unit'] = 'TJ'
                df2.loc[idx] = new_row
                df2x.loc[idx] = new_row
                idx += 1
                for tid in ids_to_combine:
                    tx = df2[df2['id'] == tid]
                    if tx.shape[0] == 0:
                        print(f"Error: id {tid} not found in {jsonfile}")
                        exit(1)
                    pos = df2[df2['id'] == tid].index[0]
                    df2.loc[pos,'level'] = t_dict['level'] + 1
            else:
                tid = t_dict['id']
                df_subset = df2[df2['id'] == tid]
                if df_subset.shape[0] > 1:
                    print(f"Error: Multiple entries found for id {tid} in {jsonfile}")
                    exit(1)
                if df_subset.shape[0] > 0:
                    pos = df2[df2['id'] == tid].index[0]
                    if df_subset.iloc[0]['level'] != t_dict['level']:
                        df2.loc[pos,'level'] = t_dict['level']
                    df2x.loc[pos] = df2.loc[pos]
                else:
                    print(f"Error: id {tid} not found in {jsonfile}")
                    exit(1)

        df2x.sort_values(by='id', inplace=True, ignore_index=True)

        outputfilename = jsonfile.replace('20250721_04_energy_stat/20250721_04', '20251201_21_energy_stat/20251201_21').replace('_stat_data','_stat_data_common')
        df2x.to_json(outputfilename, orient='index', force_ascii=False, indent=4)
        df2x.to_excel(writer, sheet_name=sheet_names[list_json.index(jsonfile)])

