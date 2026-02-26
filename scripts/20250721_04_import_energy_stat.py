# 20250509 / 0510 / 0512 / 0513 / 0721
# -*- coding: utf-8 -*-
import json
import openpyxl
import pandas as pd
import numpy as np

YEAR_START = 2010
YEAR_END   = 2024
year_range = np.arange(YEAR_START, YEAR_END)

# output file names
jsonfile_data  = 'outputs/20250721_04_energy_stat/20250721_04_energy_stat_data.json'
excelfile_data = 'outputs/20250721_04_energy_stat/20250721_04_energy_stat_data.xlsx'

data_structure_excel = 'inputs/energy_stat/20250721_04_energy_statistics_data_structure.xlsx'
wb = openpyxl.load_workbook(data_structure_excel)
sheet = wb['row']
data = sheet.values
cols = next(data)
data = list(data)
df_data_structure_row = pd.DataFrame(data, columns=cols)
n_rows = df_data_structure_row.index.shape[0]

sheet = wb['column']
data = sheet.values
cols = next(data)
data = list(data)
df_data_structure_col = pd.DataFrame(data, columns=cols)
n_cols = df_data_structure_col.index.shape[0]

list_energy_stat_excel = []
#list_years = []
f = open('inputs/energy_stat/list_energy_stat_excel.txt')
for line in f:
    s = line.split()
    list_energy_stat_excel.append(s[0])
#    list_years.append(int(s[1]))

df0 = pd.DataFrame(
    {
        "id": df_data_structure_row['id'],
        "item_name_jp": df_data_structure_row['item_name_jp'],
        "level": df_data_structure_row['level'],
        'n_sub': df_data_structure_row['n_sub'],
        "item_name_en": '',
        'unit': ''
    }
)
n_df0 = df0.index.shape[0]

df01 = pd.DataFrame(columns=year_range)
df02 = pd.DataFrame(columns=year_range)
df03 = pd.DataFrame(columns=year_range)
df04 = pd.DataFrame(columns=year_range)
df05 = pd.DataFrame(columns=year_range)
df06 = pd.DataFrame(columns=year_range)
df07 = pd.DataFrame(columns=year_range)
df08 = pd.DataFrame(columns=year_range)
df09 = pd.DataFrame(columns=year_range)
df10 = pd.DataFrame(columns=year_range)
df11 = pd.DataFrame(columns=year_range)
df12 = pd.DataFrame(columns=year_range)
df13 = pd.DataFrame(columns=year_range)
df14 = pd.DataFrame(columns=year_range)
df15 = pd.DataFrame(columns=year_range)
df16 = pd.DataFrame(columns=year_range)
list_df = [
    df01, df02, df03, df04, df05, df06, df07, df08, df09, df10, 
    df11, df12, df13, df14, df15, df16
]

# enter annual data
for i in range(len(list_energy_stat_excel)):
    year = YEAR_START+i
    wb = openpyxl.load_workbook(list_energy_stat_excel[i], data_only=True)
    sheet = wb['ｴﾈﾙｷﾞｰ単位表（本表）']
    rowname = 'row%d' % (year)
    columnname = 'column%d' % (year)

    for j in range(n_cols):
        dfx = list_df[j]

        for k in range(n_rows):
            if df_data_structure_row.loc[k,'n_sub'] == 0:
                # verify column and row
                column = df_data_structure_col.loc[j,columnname]
                cellname = '%s1' % (column)
                v = sheet[cellname].value
                if v != df_data_structure_col.loc[j,'id']:
                    print('id mismatch at %s column=%s id=%s %s' % (list_energy_stat_excel[i], df_data_structure_col.loc[j,columnname], df_data_structure_col.loc[j,'id'], v))
                    exit()
                row = df_data_structure_row.loc[k,rowname]
                cellname = 'A%d' % (row)
                v = sheet[cellname].value
                if v != df_data_structure_row.loc[k,'id']:
                    print('id mismatch at %s column=%s id=%s %s' % (list_energy_stat_excel[i], df_data_structure_row.loc[k,rowname], df_data_structure_row.loc[k,'id'], v))
                    exit()

                cellname = '%s%d' % (column,row)
                v = sheet[cellname].value
                dfx.loc[k,year] = v

# calc sums
for j in range(n_cols):
    dfx = list_df[j]

    ## Level 3
    for k in range(n_rows):
        if df0.loc[k,'level']==3 and df0.loc[k,'n_sub']>0:
            n_sub = int(df0.loc[k,'n_sub'])
            sum = np.zeros(YEAR_END-YEAR_START)
            count = 0
            for l in range(k+1,n_rows):
                if df0.loc[l,'level']==4 and count < n_sub:
                    for m in range(YEAR_START, YEAR_END):
                        v = dfx.loc[l,m]
                        sum[m-YEAR_START] += v
                    count += 1
            for m in range(YEAR_START, YEAR_END):
                dfx.loc[k,m] = sum[m-YEAR_START]

    ## Level 2
    for k in range(n_rows):
        if df0.loc[k,'level']==2 and df0.loc[k,'n_sub']>0:
            n_sub = int(df0.loc[k,'n_sub'])
            sum = np.zeros(YEAR_END-YEAR_START)
            count = 0
            for l in range(k+1,n_rows):
                if df0.loc[l,'level']==3 and count < n_sub:
                    for m in range(YEAR_START, YEAR_END):
                        v = dfx.loc[l,m]
                        sum[m-YEAR_START] += v
                    count += 1
            for m in range(YEAR_START, YEAR_END):
                dfx.loc[k,m] = sum[m-YEAR_START]

    ## Level 1
    for k in range(n_rows):
        if df0.loc[k,'level']==1 and df0.loc[k,'n_sub']>0:
            n_sub = int(df0.loc[k,'n_sub'])
            sum = np.zeros(YEAR_END-YEAR_START)
            count = 0
            for l in range(k+1,n_rows):
                if df0.loc[l,'level']==2 and count < n_sub:
                    for m in range(YEAR_START, YEAR_END):
                        v = dfx.loc[l,m]
                        sum[m-YEAR_START] += v
                    count += 1
            for m in range(YEAR_START, YEAR_END):
                dfx.loc[k,m] = sum[m-YEAR_START]

    ## Level 0
    for k in range(n_rows):
        if df0.loc[k,'level']==0 and df0.loc[k,'n_sub']>0:
            n_sub = int(df0.loc[k,'n_sub'])
            sum = np.zeros(YEAR_END-YEAR_START)
            count = 0
            for l in range(k+1,n_rows):
                if df0.loc[l,'level']==1 and count < n_sub:
                    for m in range(YEAR_START, YEAR_END):
                        v = dfx.loc[l,m]
                        sum[m-YEAR_START] += v
                    count += 1
            for m in range(YEAR_START, YEAR_END):
                dfx.loc[k,m] = sum[m-YEAR_START]


with pd.ExcelWriter(excelfile_data) as writer:
    for j in range(n_cols):
        dfx = pd.concat([df0,list_df[j]], axis=1)
        for k in range(n_rows):
            dfx.loc[k,'unit'] = df_data_structure_col.loc[j,'unit']
        dfx.to_excel(writer, sheet_name=df_data_structure_col.loc[j,'item_name_jp'])

for j in range(n_cols):
    str = '_%d_%s.json' % (j, df_data_structure_col.loc[j,'item_name_jp'])
    filename = jsonfile_data.replace('.json',str)
    dfx = dfx = pd.concat([df0,list_df[j]], axis=1)
    for k in range(n_rows):
        dfx.loc[k,'unit'] = df_data_structure_col.loc[j,'unit']
    dfx.to_json(filename, orient='index', force_ascii=False, indent=4)
