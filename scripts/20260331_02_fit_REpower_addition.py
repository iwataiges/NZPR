# 20250908 / 20260331
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import openpyxl

excelfile1 = 'inputs/RE/20250820IRENA_REstatistics_global_japan_GWh.xlsx'
wb = openpyxl.load_workbook(excelfile1, data_only=True)
sheet = wb['Japan']
data = sheet.values
cols = next(data)
data = list(data)
df0 = pd.DataFrame(data, columns=cols)
ndata0 = df0.index.shape[0]

year0 = 2000
year1 = 2014
year2 = 2023

df0_1 = df0[['Year','Solar photovoltaic','Onshore wind energy','PV_additions','OnSW_additions']]
df1 = df0_1[(df0_1['Year']>=year1) & (df0_1['Year']<=year2)]

pv_year1 = df1.at[year1-year0,'Solar photovoltaic']
pv_year2 = df1.at[year2-year0,'Solar photovoltaic']
onsw_year1 = df1.at[year1-year0,'Onshore wind energy']
onsw_year2 = df1.at[year2-year0,'Onshore wind energy']

x1 = df1['Year'].to_numpy() - year1
y1 = df1['Solar photovoltaic'].to_numpy() - pv_year1

a1, b1 = np.polyfit(x1, y1, 1)
print('  PV: a x + b a = %7.4e b=%7.4e ' % (a1, b1))

y2 = df1['Onshore wind energy'].to_numpy() - onsw_year1
a2, b2 = np.polyfit(x1, y2, 1)
print('OnSW: a x + b a = %7.4e b=%7.4e ' % (a2, b2))


year1 = 2019
year2 = 2023
df2 = df0_1[(df0_1['Year']>=year1) & (df0_1['Year']<=year2)]

y3 = df2['PV_additions'].to_numpy()
y4 = df2['OnSW_additions'].to_numpy()

a3 = np.mean(y3)
a4 = np.mean(y4)

print('%4d-%4d average: PV: %8.2f OnSW: %8.2f' % (year1,year2,a3,a4))


year3 = 2041

print('# Year,PV(extrapolation),PV(average),OnSW(extrapolation),OnSW(average)')
for i in range(year2, year3):
    tx = i
    ty1 = a1 * (tx-year1) + b1 + pv_year1
    ty2 = a2 * (tx-year1) + b2 + onsw_year1

    ty3 = pv_year2 + a3 * (i - year2)
    ty4 = onsw_year2 + a4 * (i - year2)

    print('%4d %9.2f %9.2f  %9.2f %9.2f ' % (tx, ty1, ty3, ty2, ty4))

