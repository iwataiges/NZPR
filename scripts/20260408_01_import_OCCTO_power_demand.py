# 20251231
# 20260408
# -*- coding: utf-8 -*-
import json
import openpyxl
import pandas as pd
import numpy as np

INPUT_EXCEL_FILE = 'inputs/RE/20260408OCCTO電力需要想定.xlsx'
OUTPUT_JSON_FILE = 'outputs/20251231_01_OCCTO/20260408_01_OCCTO_power_demand.json'

def load_data():
    wb = openpyxl.load_workbook(INPUT_EXCEL_FILE, data_only=True)
    sheet = wb['Sheet1']
    data = sheet.values
    cols = next(data)
    data = list(data)
    df = pd.DataFrame(data, columns=cols)
    return df

if __name__ == '__main__':

    df = load_data()
    df0 = df.dropna(subset='需要電力量_送電端')

    df1 = pd.DataFrame(
        {
            "Year": df0['年度'],
            "需要電力量_送電端": df0['需要電力量_送電端']*1.0e-3,
            "需要電力量_需要端": df0['需要電力量_需要端']*1.0e-3,
            "需要電力量_使用端": df0['需要電力量_使用端']*1.0e-3,
            "需要電力量_家庭用その他": df0['家庭用その他']*1.0e-3,
            "需要電力量_業務用": df0['業務用']*1.0e-3,
            "需要電力量_産業用その他": df0['産業用その他']*1.0e-3,
            "unit": "TWh/year"
        }
    )

    df2 = pd.DataFrame(
        [
            {
                "Year": 2040,
                "需要電力量_送電端_モデルケース1": df[df['年度']==2040]['モデルケース1'].values[0]*0.1,
                "需要電力量_送電端_モデルケース2": df[df['年度']==2040]['モデルケース2'].values[0]*0.1,
                "unit": "TWh/year"
            },
            {
                "Year": 2050,
                "需要電力量_送電端_モデルケース1": df[df['年度']==2050]['モデルケース1'].values[0]*0.1,
                "需要電力量_送電端_モデルケース2": df[df['年度']==2050]['モデルケース2'].values[0]*0.1,
                "需要電力量_送電端_モデルケース3": df[df['年度']==2050]['モデルケース3'].values[0]*0.1,
                "需要電力量_送電端_モデルケース4": df[df['年度']==2050]['モデルケース4'].values[0]*0.1,
                "unit": "TWh/year"
            }
        ]
    )

    dfx = pd.concat([df1, df2])
    dfx.reset_index(inplace=True, drop=True)
    dfx.to_json(OUTPUT_JSON_FILE, orient='index', force_ascii=False, indent=4)
