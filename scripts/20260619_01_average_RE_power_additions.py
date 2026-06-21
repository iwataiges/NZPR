# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import openpyxl

if __name__ == '__main__':
    excelfile1 = 'inputs/RE/20260617_01_RE_japan.xlsx'
    wb = openpyxl.load_workbook(excelfile1, data_only=True)
    sheet = wb['power']
    data = sheet.values
    cols = next(data)
    data = list(data)
    df0 = pd.DataFrame(data, columns=cols)
    ndata0 = df0.index.shape[0]

    df0['PV_diff'] = pd.Series()
    df0['OnSW_diff'] = pd.Series()
    df0['OffSW_diff'] = pd.Series()

    for i in range(ndata0-1):
        pv0 = df0.iloc[i]['PV_TWh_IRENA']
        pv1 = df0.iloc[i+1]['PV_TWh_IRENA']
        df0.at[i+1, 'PV_diff'] = pv1 - pv0

        onsw0 = df0.iloc[i]['OnSW_TWh_IRENA']
        onsw1 = df0.iloc[i+1]['OnSW_TWh_IRENA']
        df0.at[i+1, 'OnSW_diff'] = onsw1 - onsw0

        offsw0 = df0.iloc[i]['OffSW_TWh_IRENA']
        offsw1 = df0.iloc[i+1]['OffSW_TWh_IRENA']
        df0.at[i+1, 'OffSW_diff'] = offsw1 - offsw0

        year1 = df0.iloc[i+1]['Year']
        print('%d: %5.3f %5.3f %5.3f ' % (year1, pv1-pv0, onsw1-onsw0, offsw1-offsw0))

        if year1 == 2023:
            pv_add2023 = pv1-pv0

    df1 = df0[(df0['Year']>=2019) & (df0['Year']<=2023)]
    pv_add_ave = np.average(df1['PV_diff'])
    onsw_add_ave = np.average(df1['OnSW_diff'])
    offsw_add_ave = np.average(df1['OffSW_diff'])

    print('2019-2023 average: %5.3f %5.3f %5.3f '% (pv_add_ave, onsw_add_ave, offsw_add_ave))

    # no data for 2024
#    df1 = df0[(df0['Year']>=2020) & (df0['Year']<=2024)]
#    pv_add_ave = np.average(df1['PV_diff'])
#    onsw_add_ave = np.average(df1['OnSW_diff'])
#    offsw_add_ave = np.average(df1['OffSW_diff'])
#
#    print('2020-2024 average: %5.3f %5.3f %5.3f '% (pv_add_ave, onsw_add_ave, offsw_add_ave))

    pv2023 = df0[df0['Year']==2023]['PV_TWh_IRENA'].values[0]
    pv2030 = pv2023 + pv_add_ave * (2030-2023)
    pv2035 = pv2023 + pv_add_ave * (2035-2023)
    pv2040 = pv2023 + pv_add_ave * (2040-2023)

    onsw2023 = df0[df0['Year']==2023]['OnSW_TWh_IRENA'].values[0]
    onsw2030 = onsw2023 + onsw_add_ave * (2030-2023)
    onsw2035 = onsw2023 + onsw_add_ave * (2035-2023)
    onsw2040 = onsw2023 + onsw_add_ave * (2040-2023)

    offsw2023 = df0[df0['Year']==2023]['OffSW_TWh_IRENA'].values[0]
    offsw2030 = offsw2023 + offsw_add_ave * (2030-2023)
    offsw2035 = offsw2023 + offsw_add_ave * (2035-2023)
    offsw2040 = offsw2023 + offsw_add_ave * (2040-2024)

    print('2030: %6.2f %6.2f %6.2f' % (pv2030, onsw2030, offsw2030))
    print('2035: %6.2f %6.2f %6.2f' % (pv2035, onsw2035, offsw2035))
    print('2040: %6.2f %6.2f %6.2f' % (pv2040, onsw2040, offsw2040))

    pv2030_2 = pv2023 + pv_add2023 * (2030-2023)
    pv2035_2 = pv2023 + pv_add2023 * (2035-2023)
    pv2040_2 = pv2023 + pv_add2023 * (2040-2023)
    print('2023 additions: %5.3f' % (pv_add2023))
    print('2030: %6.2f ' % (pv2030_2))
    print('2035: %6.2f ' % (pv2035_2))
    print('2040: %6.2f ' % (pv2040_2))
