# 20250924 / 1016 / 1105
# -*- coding: utf-8 -*-
import json
import openpyxl
import pandas as pd
import numpy as np

list_years = ['baseyear', '2030', '2040', '2050']
list_colnames = ['CO2_base', 'CO2_2030', 'CO2_2040', 'CO2_2050']
nyears = len(list_years)
# output file names
jsonfile_data  = 'outputs/20251118_04_1p5CRM_steps_co2/20251118_04_1p5CRM_steps_co2_data.json'
excelfile_data = 'outputs/20251118_04_1p5CRM_steps_co2/20251118_04_1p5CRM_steps_co2_data.xlsx'

data_structure_excel = 'inputs/1p5CRM/20251104_05_1p5CRM_data_structure.xlsx'
wb = openpyxl.load_workbook(data_structure_excel)
sheet = wb['row']
data = sheet.values
cols = next(data)
data = list(data)
df_data_structure_row = pd.DataFrame(data, columns=cols)
n_rows = df_data_structure_row.index.shape[0]

sheet = wb['column_co2']
data = sheet.values
cols = next(data)
data = list(data)
df_data_structure_col = pd.DataFrame(data, columns=cols)
df_data_structure_col.dropna(subset='unit',inplace=True,ignore_index=True)
n_cols = df_data_structure_col.index.shape[0]

#df0 = pd.DataFrame(
#    {
#        "id": df_data_structure_row['id'],
#        "label": df_data_structure_row['item_name_jp'],
#        "level": df_data_structure_row['level'],
#        'n_sub': df_data_structure_row['n_sub'],
#    }
#)
#n_df0 = df0.index.shape[0]
#
#df1 = pd.DataFrame(
#    {
#        "id": df_data_structure_col['id'],
#        "energy_base": df_data_structure_col['energy_basee'],
#        "energy_2030": df_data_structure_col['energy_2030'],
#        "energy_2040": df_data_structure_col['energy_2040'],
#        "energy_2050": df_data_structure_col['energy_2050'],
#    }
#)


# DataFrames for each of columns
df01 = pd.DataFrame(columns = list_years)
df02 = pd.DataFrame(columns = list_years)
df03 = pd.DataFrame(columns = list_years)
df04 = pd.DataFrame(columns = list_years)
df05 = pd.DataFrame(columns = list_years)
df06 = pd.DataFrame(columns = list_years)
df07 = pd.DataFrame(columns = list_years)
df08 = pd.DataFrame(columns = list_years)
df09 = pd.DataFrame(columns = list_years)
df10 = pd.DataFrame(columns = list_years)
df11 = pd.DataFrame(columns = list_years)
df12 = pd.DataFrame(columns = list_years)
df13 = pd.DataFrame(columns = list_years)
df14 = pd.DataFrame(columns = list_years)
df15 = pd.DataFrame(columns = list_years)
df16 = pd.DataFrame(columns = list_years)
list_df = [
    df01, df02, df03, df04, df05, df06, df07, df08, df09, df10, 
    df11, df12, df13, df14, df15, df16
]

#RM_balance_excel = 'inputs/1p5CRM/【バランス】全部門エネルギーCO2計算20231114.xlsx'
RM_balance_excel = 'inputs/1p5CRM/20231114_1p5CRM_steps_energy_co2_rev4.xlsx'
wb = openpyxl.load_workbook(RM_balance_excel, data_only=True)
sheet = wb['netozero計算フォーマット']

for i in range(nyears):
    colname = list_colnames[i]

    for j in range(n_cols):
        dfx = list_df[j]
        column = df_data_structure_col.loc[j,colname]

        for k in range(n_rows):
            if df_data_structure_row.loc[k,'n_sub'] == 0:
                row = df_data_structure_row.loc[k,'row']
                if pd.isnull(column) == False:
                    cellname = '%s%s' % (column,row)
                    v = sheet[cellname].value
                    if pd.isnull(v):
#                        print('%s %s %s' % (row, column, v))
                        v = 0.0
#                    else:
#                        print('%s %s %10.4e ' % (row, column, v))
                    dfx.loc[k,list_years[i]] = v



# calc sums
for j in range(n_cols):
    dfx = list_df[j]

    ## Level 1
    for k in range(n_rows):
        if df_data_structure_row.loc[k,'level']==1 and df_data_structure_row.loc[k,'n_sub']>0:
            n_sub = int(df_data_structure_row.loc[k,'n_sub'])
            sum = np.zeros(nyears)
            count = 0
            for l in range(k+1,n_rows):
                if df_data_structure_row.loc[l,'level']==2 and count < n_sub:
                    for m in range(nyears):
                        v = dfx.loc[l,list_years[m]]
                        sum[m] += v
                    count += 1
            for m in range(nyears):
                dfx.loc[k,list_years[m]] = sum[m]

    ## Level 0
    for k in range(n_rows):
        if df_data_structure_row.loc[k,'level']==0 and df_data_structure_row.loc[k,'n_sub']>0:
            n_sub = int(df_data_structure_row.loc[k,'n_sub'])
            sum = np.zeros(nyears)
            count = 0
            for l in range(k+1,n_rows):
                if df_data_structure_row.loc[l,'level']==1 and count < n_sub:
                    for m in range(nyears):
                        v = dfx.loc[l,list_years[m]]
                        sum[m] += v
                    count += 1
            for m in range(nyears):
                dfx.loc[k,list_years[m]] = sum[m]



with pd.ExcelWriter(excelfile_data) as writer:
    for j in range(n_cols):
        dfx = pd.concat([df_data_structure_row,list_df[j]], axis=1)
        for k in range(n_rows):
            dfx.loc[k,'unit'] = df_data_structure_col.loc[j,'unit']
        dfx.to_excel(writer, sheet_name=df_data_structure_col.loc[j,'item_name_jp'])

for j in range(n_cols):
    str = '_%02d_%s.json' % (j, df_data_structure_col.loc[j,'item_name_jp'])
    filename = jsonfile_data.replace('.json',str)
    dfx = dfx = pd.concat([df_data_structure_row,list_df[j]], axis=1)
    for k in range(n_rows):
        dfx.loc[k,'unit'] = df_data_structure_col.loc[j,'unit']
    dfx.to_json(filename, orient='index', force_ascii=False, indent=4)
