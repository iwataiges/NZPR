# 20251208
# -*- coding: utf-8 -*-
import json
import openpyxl
import pandas as pd
import numpy as np

IGESRM_GHG_EXCEL_FILE = 'inputs/1p5CRM/20240123GHGpath_rev1.xlsx'

def load_data():
    wb = openpyxl.load_workbook(IGESRM_GHG_EXCEL_FILE, data_only=True)
    sheet = wb['IGESRM20231114_steps']
    data = sheet.values
    cols = next(data)
    data = list(data)
    df_orig = pd.DataFrame(data, columns=cols)
    df = df_orig[[
        'Year',
        'GHG排出量(DACCS含、森林吸収含まず)',
        'CO2(DACCS含、森林吸収含まず)',
        'GHG(森林吸収、DACCS含)',
        '2013年比削減割合(GHG)',
        '2019年比削減割合(GHG)',
        'CO2(森林吸収、DACCS含)',
        '2013年比削減割合(CO2)',
        '2019年比削減割合(CO2)',
        '農林水産業',
        '電力',
        '製造業',
        '運輸',
        '建物',
        'その他GHG',
        '森林吸収源',
        'DACCS',
        'CCS回収分'
    ]]
    df.dropna(subset='Year', inplace=True)
    return df

if __name__ == '__main__':
    df = load_data()
    df.to_json('outputs/20251208_01_1p5CRM_GHG/20251208_04_1p5CRM_steps_GHG_data.json', orient='index', force_ascii=False, indent=4)
    df.to_excel('outputs/20251208_01_1p5CRM_GHG/20251208_04_1p5CRM_steps_GHG_data.xlsx')
