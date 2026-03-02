# 20251218 / 20260116
# -*- coding: utf-8 -*-
import json
import openpyxl
import pandas as pd
import numpy as np

INPUT_SEP_EXCEL_FILE = 'inputs/SEP/20260116_02_SEP_numbers.xlsx'

KL_TO_TJ = 0.03876 # 1/25.8

def load_data(wb, sheet_name):
    sheet = wb[sheet_name]
    data = sheet.values
    cols = next(data)
    data = list(data)
    df = pd.DataFrame(data, columns=cols)
    return df

if __name__ == '__main__':
    wb = openpyxl.load_workbook(INPUT_SEP_EXCEL_FILE, data_only=True)
    df_2030 = load_data(wb, '2030')
    df_2040_1 = load_data(wb, '2040_1')
    df_2040_2 = load_data(wb, '2040_2')
    df_2040_3 = load_data(wb, '2040_3')
    df_2040_4 = load_data(wb, '2040_4')
    df_2040_5 = load_data(wb, '2040_5')

    v = np.zeros((4,6,6))

    ## Final Energy Consumption (FEC)
    v[0,0,0] = (df_2030[(df_2030['部門'] == '合計')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    v[0,0,1] = (df_2040_1[(df_2040_1['部門'] == '合計')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    v[0,0,2] = (df_2040_2[(df_2040_2['部門'] == '合計')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    v[0,0,3] = (df_2040_3[(df_2040_3['部門'] == '合計')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    v[0,0,4] = (df_2040_4[(df_2040_4['部門'] == '合計')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    v[0,0,5] = (df_2040_5[(df_2040_5['部門'] == '合計')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
 
    df = pd.DataFrame(
        {
            "Year": [2030, 2040, 2040, 2040, 2040, 2040],
            "Scenario": [0, 1, 2, 3, 4, 5],
            "Sector": "Total",
            "id": '#500000',
            "Type": "FEC",
            "Value": [v[0,0,0], v[0,0,1], v[0,0,2], v[0,0,3], v[0,0,4], v[0,0,5]],
            "unit": "TJ",
        }
    )

    df_FEC_total = df.copy()

    v[0,1,0] = (df_2030[(df_2030['部門'] == '産業')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    v[0,1,1] = (df_2040_1[(df_2040_1['部門'] == '産業')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    v[0,1,2] = (df_2040_2[(df_2040_2['部門'] == '産業')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    v[0,1,3] = (df_2040_3[(df_2040_3['部門'] == '産業')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    v[0,1,4] = (df_2040_4[(df_2040_4['部門'] == '産業')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    v[0,1,5] = (df_2040_5[(df_2040_5['部門'] == '産業')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    df_FEC_industry = df.copy()
    df_FEC_industry['Sector'] = 'Industry'
    df_FEC_industry['id'] = '#600100'
    df_FEC_industry['Value'] = [v[0,1,0], v[0,1,1], v[0,1,2], v[0,1,3], v[0,1,4], v[0,1,5]]

    v[0,2,0] = (df_2030[(df_2030['部門'] == '業務')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    v[0,2,1] = (df_2040_1[(df_2040_1['部門'] == '業務')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    v[0,2,2] = (df_2040_2[(df_2040_2['部門'] == '業務')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    v[0,2,3] = (df_2040_3[(df_2040_3['部門'] == '業務')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    v[0,2,4] = (df_2040_4[(df_2040_4['部門'] == '業務')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    v[0,2,5] = (df_2040_5[(df_2040_5['部門'] == '業務')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    df_FEC_commercial = df.copy()
    df_FEC_commercial['Sector'] = 'Commercial'
    df_FEC_commercial['id'] = '#650000'
    df_FEC_commercial['Value'] = [v[0,2,0], v[0,2,1], v[0,2,2], v[0,2,3], v[0,2,4], v[0,2,5]]

    v[0,3,0] = (df_2030[(df_2030['部門'] == '家庭')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    v[0,3,1] = (df_2040_1[(df_2040_1['部門'] == '家庭')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    v[0,3,2] = (df_2040_2[(df_2040_2['部門'] == '家庭')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    v[0,3,3] = (df_2040_3[(df_2040_3['部門'] == '家庭')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    v[0,3,4] = (df_2040_4[(df_2040_4['部門'] == '家庭')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    v[0,3,5] = (df_2040_5[(df_2040_5['部門'] == '家庭')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    df_FEC_residential = df.copy()
    df_FEC_residential['Sector'] = 'Residential'
    df_FEC_residential['id'] = '#700000'
    df_FEC_residential['Value'] = [v[0,3,0], v[0,3,1], v[0,3,2], v[0,3,3], v[0,3,4], v[0,3,5]]

    v[0,4,0] = (df_2030[(df_2030['部門'] == '運輸')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    v[0,4,1] = (df_2040_1[(df_2040_1['部門'] == '運輸')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    v[0,4,2] = (df_2040_2[(df_2040_2['部門'] == '運輸')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    v[0,4,3] = (df_2040_3[(df_2040_3['部門'] == '運輸')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    v[0,4,4] = (df_2040_4[(df_2040_4['部門'] == '運輸')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    v[0,4,5] = (df_2040_5[(df_2040_5['部門'] == '運輸')]['最終エネルギー消費']*1.0e6*KL_TO_TJ).values[0]
    df_FEC_transport = df.copy()
    df_FEC_transport['Sector'] = 'Transport'
    df_FEC_transport['id'] = '#800000'
    df_FEC_transport['Value'] = [v[0,4,0], v[0,4,1], v[0,4,2], v[0,4,3], v[0,4,4], v[0,4,5]]

    ## Electricity Demand
    v[1,0,0] = (df_2030[(df_2030['部門'] == '合計')]['電力需要']*0.1).values[0]
    v[1,0,1] = (df_2040_1[(df_2040_1['部門'] == '合計')]['電力需要']*0.1).values[0]
    v[1,0,2] = (df_2040_2[(df_2040_2['部門'] == '合計')]['電力需要']*0.1).values[0]
    v[1,0,3] = (df_2040_3[(df_2040_3['部門'] == '合計')]['電力需要']*0.1).values[0]
    v[1,0,4] = (df_2040_4[(df_2040_4['部門'] == '合計')]['電力需要']*0.1).values[0]
    v[1,0,5] = (df_2040_5[(df_2040_5['部門'] == '合計')]['電力需要']*0.1).values[0]

    df = pd.DataFrame(
        {
            "Year": [2030, 2040, 2040, 2040, 2040, 2040],
            "Scenario": [0, 1, 2, 3, 4, 5],
            "Sector": "Total",
            "id": "#500000",
            "Type": "Electricity Demand",
            "Value": [v[1,0,0], v[1,0,1], v[1,0,2], v[1,0,3], v[1,0,4], v[1,0,5]],
            "unit": "TWh",
        }
    )

    df_elec_total = df.copy()

    v[1,1,0] = (df_2030[(df_2030['部門'] == '産業')]['電力需要']*0.1).values[0]
    v[1,1,1] = (df_2040_1[(df_2040_1['部門'] == '産業')]['電力需要']*0.1).values[0]
    v[1,1,2] = (df_2040_2[(df_2040_2['部門'] == '産業')]['電力需要']*0.1).values[0]
    v[1,1,3] = (df_2040_3[(df_2040_3['部門'] == '産業')]['電力需要']*0.1).values[0]
    v[1,1,4] = (df_2040_4[(df_2040_4['部門'] == '産業')]['電力需要']*0.1).values[0]
    v[1,1,5] = (df_2040_5[(df_2040_5['部門'] == '産業')]['電力需要']*0.1).values[0]
    df_elec_industry = df.copy()
    df_elec_industry['Sector'] = 'Industry'
    df_elec_industry['id'] = '#600100'
    df_elec_industry['Value'] = [v[1,1,0], v[1,1,1], v[1,1,2], v[1,1,3], v[1,1,4], v[1,1,5]]

    v[1,2,0] = (df_2030[(df_2030['部門'] == '業務')]['電力需要']*0.1).values[0]
    v[1,2,1] = (df_2040_1[(df_2040_1['部門'] == '業務')]['電力需要']*0.1).values[0]
    v[1,2,2] = (df_2040_2[(df_2040_2['部門'] == '業務')]['電力需要']*0.1).values[0]
    v[1,2,3] = (df_2040_3[(df_2040_3['部門'] == '業務')]['電力需要']*0.1).values[0]
    v[1,2,4] = (df_2040_4[(df_2040_4['部門'] == '業務')]['電力需要']*0.1).values[0]
    v[1,2,5] = (df_2040_5[(df_2040_5['部門'] == '業務')]['電力需要']*0.1).values[0]
    df_elec_commercial = df.copy()
    df_elec_commercial['Sector'] = 'Commercial'
    df_elec_commercial['id'] = '#650000'
    df_elec_commercial['Value'] = [v[1,2,0], v[1,2,1], v[1,2,2], v[1,2,3], v[1,2,4], v[1,2,5]]

    v[1,3,0] = (df_2030[(df_2030['部門'] == '家庭')]['電力需要']*0.1).values[0]
    v[1,3,1] = (df_2040_1[(df_2040_1['部門'] == '家庭')]['電力需要']*0.1).values[0]
    v[1,3,2] = (df_2040_2[(df_2040_2['部門'] == '家庭')]['電力需要']*0.1).values[0]
    v[1,3,3] = (df_2040_3[(df_2040_3['部門'] == '家庭')]['電力需要']*0.1).values[0]
    v[1,3,4] = (df_2040_4[(df_2040_4['部門'] == '家庭')]['電力需要']*0.1).values[0]
    v[1,3,5] = (df_2040_5[(df_2040_5['部門'] == '家庭')]['電力需要']*0.1).values[0]
    df_elec_residential = df.copy()
    df_elec_residential['Sector'] = 'Residential'
    df_elec_residential['id'] = '#700000'
    df_elec_residential['Value'] = [v[1,3,0], v[1,3,1], v[1,3,2], v[1,3,3], v[1,3,4], v[1,3,5]]

    v[1,4,0] = (df_2030[(df_2030['部門'] == '運輸')]['電力需要']*0.1).values[0]
    v[1,4,1] = (df_2040_1[(df_2040_1['部門'] == '運輸')]['電力需要']*0.1).values[0]
    v[1,4,2] = (df_2040_2[(df_2040_2['部門'] == '運輸')]['電力需要']*0.1).values[0]
    v[1,4,3] = (df_2040_3[(df_2040_3['部門'] == '運輸')]['電力需要']*0.1).values[0]
    v[1,4,4] = (df_2040_4[(df_2040_4['部門'] == '運輸')]['電力需要']*0.1).values[0]
    v[1,4,5] = (df_2040_5[(df_2040_5['部門'] == '運輸')]['電力需要']*0.1).values[0]
    df_elec_transport = df.copy()
    df_elec_transport['Sector'] = 'Transport'
    df_elec_transport['id'] = '#800000'
    df_elec_transport['Value'] = [v[1,4,0], v[1,4,1], v[1,4,2], v[1,4,3], v[1,4,4], v[1,4,5]]

    ## CO2 emissions
    v[2,0,0] = (df_2030[(df_2030['部門'] == '合計')]['CO2排出量']).values[0]
    v[2,0,1] = (df_2040_1[(df_2040_1['部門'] == '合計')]['CO2排出量']).values[0]
    v[2,0,2] = (df_2040_2[(df_2040_2['部門'] == '合計')]['CO2排出量']).values[0]
    v[2,0,3] = (df_2040_3[(df_2040_3['部門'] == '合計')]['CO2排出量']).values[0]
    v[2,0,4] = (df_2040_4[(df_2040_4['部門'] == '合計')]['CO2排出量']).values[0]
    v[2,0,5] = (df_2040_5[(df_2040_5['部門'] == '合計')]['CO2排出量']).values[0]

    df = pd.DataFrame(
        {
            "Year": [2030, 2040, 2040, 2040, 2040, 2040],
            "Scenario": [0, 1, 2, 3, 4, 5],
            "Sector": "Total",
            "id": "#500000",
            "Type": "CO2 Emissions",
            "Value": [v[2,0,0], v[2,0,1], v[2,0,2], v[2,0,3], v[2,0,4], v[2,0,5]],
            "unit": "MtCO2",
        }
    )

    df_co2_total = df.copy()

    v[2,1,0] = (df_2030[(df_2030['部門'] == '産業')]['CO2排出量']).values[0]
    v[2,1,1] = (df_2040_1[(df_2040_1['部門'] == '産業')]['CO2排出量']).values[0]
    v[2,1,2] = (df_2040_2[(df_2040_2['部門'] == '産業')]['CO2排出量']).values[0]
    v[2,1,3] = (df_2040_3[(df_2040_3['部門'] == '産業')]['CO2排出量']).values[0]
    v[2,1,4] = (df_2040_4[(df_2040_4['部門'] == '産業')]['CO2排出量']).values[0]
    v[2,1,5] = (df_2040_5[(df_2040_5['部門'] == '産業')]['CO2排出量']).values[0]
    df_co2_industry = df.copy()
    df_co2_industry['Sector'] = 'Industry'
    df_co2_industry['id'] = '#600100'
    df_co2_industry['Value'] = [v[2,1,0], v[2,1,1], v[2,1,2], v[2,1,3], v[2,1,4], v[2,1,5]]

    v[2,2,0] = (df_2030[(df_2030['部門'] == '業務')]['CO2排出量']).values[0]
    v[2,2,1] = (df_2040_1[(df_2040_1['部門'] == '業務')]['CO2排出量']).values[0]
    v[2,2,2] = (df_2040_2[(df_2040_2['部門'] == '業務')]['CO2排出量']).values[0]
    v[2,2,3] = (df_2040_3[(df_2040_3['部門'] == '業務')]['CO2排出量']).values[0]
    v[2,2,4] = (df_2040_4[(df_2040_4['部門'] == '業務')]['CO2排出量']).values[0]
    v[2,2,5] = (df_2040_5[(df_2040_5['部門'] == '業務')]['CO2排出量']).values[0]
    df_co2_commercial = df.copy() 
    df_co2_commercial['Sector'] = 'Commercial'
    df_co2_commercial['id'] = '#650000'
    df_co2_commercial['Value'] = [v[2,2,0], v[2,2,1], v[2,2,2], v[2,2,3], v[2,2,4], v[2,2,5]]

    v[2,3,0] = (df_2030[(df_2030['部門'] == '家庭')]['CO2排出量']).values[0]
    v[2,3,1] = (df_2040_1[(df_2040_1['部門'] == '家庭')]['CO2排出量']).values[0]
    v[2,3,2] = (df_2040_2[(df_2040_2['部門'] == '家庭')]['CO2排出量']).values[0]
    v[2,3,3] = (df_2040_3[(df_2040_3['部門'] == '家庭')]['CO2排出量']).values[0]
    v[2,3,4] = (df_2040_4[(df_2040_4['部門'] == '家庭')]['CO2排出量']).values[0]
    v[2,3,5] = (df_2040_5[(df_2040_5['部門'] == '家庭')]['CO2排出量']).values[0]
    df_co2_residential = df.copy()
    df_co2_residential['Sector'] = 'Residential'
    df_co2_residential['id'] = '#700000'
    df_co2_residential['Value'] = [v[2,3,0], v[2,3,1], v[2,3,2], v[2,3,3], v[2,3,4], v[2,3,5]]

    v[2,4,0] = (df_2030[(df_2030['部門'] == '運輸')]['CO2排出量']).values[0]
    v[2,4,1] = (df_2040_1[(df_2040_1['部門'] == '運輸')]['CO2排出量']).values[0]
    v[2,4,2] = (df_2040_2[(df_2040_2['部門'] == '運輸')]['CO2排出量']).values[0]
    v[2,4,3] = (df_2040_3[(df_2040_3['部門'] == '運輸')]['CO2排出量']).values[0]
    v[2,4,4] = (df_2040_4[(df_2040_4['部門'] == '運輸')]['CO2排出量']).values[0]
    v[2,4,5] = (df_2040_5[(df_2040_5['部門'] == '運輸')]['CO2排出量']).values[0]
    df_co2_transport = df.copy()
    df_co2_transport['Sector'] = 'Transport'
    df_co2_transport['id'] = '#800000'
    df_co2_transport['Value'] = [v[2,4,0], v[2,4,1], v[2,4,2], v[2,4,3], v[2,4,4], v[2,4,5]]

    v[2,5,0] = (df_2030[(df_2030['部門'] == 'エネルギー転換')]['CO2排出量']).values[0]
    v[2,5,1] = (df_2040_1[(df_2040_1['部門'] == 'エネルギー転換')]['CO2排出量']).values[0]
    v[2,5,2] = (df_2040_2[(df_2040_2['部門'] == 'エネルギー転換')]['CO2排出量']).values[0]
    v[2,5,3] = (df_2040_3[(df_2040_3['部門'] == 'エネルギー転換')]['CO2排出量']).values[0]
    v[2,5,4] = (df_2040_4[(df_2040_4['部門'] == 'エネルギー転換')]['CO2排出量']).values[0]
    v[2,5,5] = (df_2040_5[(df_2040_5['部門'] == 'エネルギー転換')]['CO2排出量']).values[0]
    df_co2_transformation = df.copy()
    df_co2_transformation['Sector'] = 'Transformation'
    df_co2_transformation['id'] = '#200000'
    df_co2_transformation['Value'] = [v[2,5,0], v[2,5,1], v[2,5,2], v[2,5,3], v[2,5,4], v[2,5,5]]

    ## CO2 Intensity
    v[3] = v[2] / v[0]
    df_intensity_total = df_co2_total.copy()
    df_intensity_total['Type'] = 'CO2 Intensity'
    df_intensity_total['Value'] = v[3,0,:]
    df_intensity_total['unit'] = 'MtCO2/TJ'

    df_intensity_industry = df_co2_industry.copy()
    df_intensity_industry['Type'] = 'CO2 Intensity'
    df_intensity_industry['Value'] = v[3,1,:]
    df_intensity_industry['unit'] = 'MtCO2/TJ'

    df_intensity_commercial = df_co2_commercial.copy()
    df_intensity_commercial['Type'] = 'CO2 Intensity'
    df_intensity_commercial['Value'] = v[3,2,:]
    df_intensity_commercial['unit'] = 'MtCO2/TJ'

    df_intensity_residential = df_co2_residential.copy()
    df_intensity_residential['Type'] = 'CO2 Intensity'
    df_intensity_residential['Value'] = v[3,3,:]
    df_intensity_residential['unit'] = 'MtCO2/TJ'

    df_intensity_transport = df_co2_transport.copy()
    df_intensity_transport['Type'] = 'CO2 Intensity'
    df_intensity_transport['Value'] = v[3,4,:]
    df_intensity_transport['unit'] = 'MtCO2/TJ'

    df_out = pd.concat([
        df_FEC_total, df_FEC_industry, df_FEC_commercial, df_FEC_residential, df_FEC_transport,
        df_elec_total, df_elec_industry, df_elec_commercial, df_elec_residential, df_elec_transport,
        df_co2_total, df_co2_industry, df_co2_commercial, df_co2_residential, df_co2_transport,df_co2_transformation,
        df_intensity_total, df_intensity_industry, df_intensity_commercial, df_intensity_residential, df_intensity_transport,
        ], ignore_index=True) 

    df_out.to_excel('outputs/20251218_02_SEP/20260116_15_SEP_numbers.xlsx', index=False)
    df_out.to_json('outputs/20251218_02_SEP/20260116_15_SEP_numbers.json', orient='index', force_ascii=False, indent=4)
