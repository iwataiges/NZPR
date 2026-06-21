# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import openpyxl

if __name__ == '__main__':
    excelfile1 = 'inputs/RE/20260617_01_RE_japan.xlsx'
    wb = openpyxl.load_workbook(excelfile1, data_only=True)
    sheet = wb['capacity']
    data = sheet.values
    cols = next(data)
    data = list(data)
    df0 = pd.DataFrame(data, columns=cols)
    ndata0 = df0.index.shape[0]

    df0['PV_diff'] = pd.Series()
    df0['OnSW_diff'] = pd.Series()
    df0['OffSW_diff'] = pd.Series()

    for i in range(ndata0-1):
        pv0 = df0.iloc[i]['PV_GW_IRENA']
        pv1 = df0.iloc[i+1]['PV_GW_IRENA']
        df0.at[i+1, 'PV_diff'] = pv1 - pv0

        onsw0 = df0.iloc[i]['OnSW_GW_IRENA']
        onsw1 = df0.iloc[i+1]['OnSW_GW_IRENA']
        df0.at[i+1, 'OnSW_diff'] = onsw1 - onsw0

        offsw0 = df0.iloc[i]['OffSW_GW_IRENA']
        offsw1 = df0.iloc[i+1]['OffSW_GW_IRENA']
        df0.at[i+1, 'OffSW_diff'] = offsw1 - offsw0

        year1 = df0.iloc[i+1]['Year']
        print('%d: %5.3f %5.3f %5.3f ' % (year1, pv1-pv0, onsw1-onsw0, offsw1-offsw0))

        if year1 == 2024:
            pv_add2024 = pv1-pv0

    df1 = df0[(df0['Year']>=2019) & (df0['Year']<=2023)]
    pv_add_ave = np.average(df1['PV_diff'])
    onsw_add_ave = np.average(df1['OnSW_diff'])
    offsw_add_ave = np.average(df1['OffSW_diff'])

    print('2019-2023 average: %5.3f %5.3f %5.3f '% (pv_add_ave, onsw_add_ave, offsw_add_ave))

    df1 = df0[(df0['Year']>=2020) & (df0['Year']<=2024)]
    pv_add_ave = np.average(df1['PV_diff'])
    onsw_add_ave = np.average(df1['OnSW_diff'])
    offsw_add_ave = np.average(df1['OffSW_diff'])

    print('2020-2024 average: %5.3f %5.3f %5.3f '% (pv_add_ave, onsw_add_ave, offsw_add_ave))

    pv2024 = df0[df0['Year']==2024]['PV_GW_IRENA'].values[0]
    pv2030 = pv2024 + pv_add_ave * (2030-2024)
    pv2035 = pv2024 + pv_add_ave * (2035-2024)
    pv2040 = pv2024 + pv_add_ave * (2040-2024)

    onsw2024 = df0[df0['Year']==2024]['OnSW_GW_IRENA'].values[0]
    onsw2030 = onsw2024 + onsw_add_ave * (2030-2024)
    onsw2035 = onsw2024 + onsw_add_ave * (2035-2024)
    onsw2040 = onsw2024 + onsw_add_ave * (2040-2024)

    offsw2024 = df0[df0['Year']==2024]['OffSW_GW_IRENA'].values[0]
    offsw2030 = offsw2024 + offsw_add_ave * (2030-2024)
    offsw2035 = offsw2024 + offsw_add_ave * (2035-2024)
    offsw2040 = offsw2024 + offsw_add_ave * (2040-2024)

    print('2030: %6.2f %6.2f %6.2f' % (pv2030, onsw2030, offsw2030))
    print('2035: %6.2f %6.2f %6.2f' % (pv2035, onsw2035, offsw2035))
    print('2040: %6.2f %6.2f %6.2f' % (pv2040, onsw2040, offsw2040))

    pv2030_2 = pv2024 + pv_add2024 * (2030-2024)
    pv2035_2 = pv2024 + pv_add2024 * (2035-2024)
    pv2040_2 = pv2024 + pv_add2024 * (2040-2024)
    print('2024 additions: %5.3f' % (pv_add2024))
    print('2030: %6.2f ' % (pv2030_2))
    print('2035: %6.2f ' % (pv2035_2))
    print('2040: %6.2f ' % (pv2040_2))
