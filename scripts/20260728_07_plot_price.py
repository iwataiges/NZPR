# 20250818 / 0829 / 0918 / 1021 gas and coal w/o CO2 cost
# 20260122
# 20260728
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import openpyxl
import matplotlib.pyplot as plt
from matplotlib import rcParams
#import time
#import matplotlib.ticker as ticker
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import config

rcParams['font.size'] = 16
rcParams['axes.labelsize'] = 16
rcParams['xtick.labelsize'] = 18
rcParams['ytick.labelsize'] = 18
#rcParams['lines.markersize'] = 10
rcParams['lines.linewidth'] = 5
rcParams['font.family'] = 'Hiragino Sans'
#rcParams['xtick.labelsize'] = 'small'
#rcParams['ytick.labelsize'] = 'small'

# 為替想定
#ExR = 125.0 # JPY/$

xlim1 = 2015.9
xlim2 = 2027.1
ylim1 = 8
ylim2 = 41

lw0 = 2.0
lw1 = 3.0
lw2 = 4.0
lw3 = 5.0


# 新電力ネット
excelfile1 = 'inputs/RE/20251219新電力ネット_電気料金推移.xlsx'
wb = openpyxl.load_workbook(excelfile1, data_only=True)
sheet = wb['Sheet1']
data = sheet.values
cols = next(data)
data = list(data)
df0 = pd.DataFrame(data, columns=cols)
df2_1 = df0[df0['種別']=='高圧'][['年', '月', '合計','Min','Max (沖縄を除く)','再エネ賦課金']]
df2_1['time'] = df2_1['年'] + (df2_1['月']-1)/12.0
#df2_1 = df0[['年', '月', '合計','Min','Max (沖縄を除く)']
#df2_2 = df0[['time', '東京-特別高圧','東京-高圧','東京-低圧（電灯）','東京-低圧（動力）']]
#df2_3 = df0[['time', 'ガス発電単価-CPなし', '石炭発電単価-CPなし','再エネ賦課金']]




fig, ax = plt.subplots(1,1,figsize=(12,8), layout='constrained')

ax.set_xlim(xlim1, xlim2)
ax.set_ylim(ylim1, ylim2)
#ax.set_xlabel('年')
ax.set_ylabel('価格 [円/kWh]')


# PPS-NET
tx = df2_1['time']
#ty = df2_3['ガス発電単価-政策コスト含む']+df2_3['再エネ賦課金']+delivery_cost+retail_cost
#ty = df2_3['ガス発電単価-CPなし']+delivery_cost+retail_cost
#ax.plot(tx, ty, '--', color=col_brown_light, linewidth=lw1, label='ガス発電単価')
#co2cost = 6.1 # コスト検証WG 2023年
#ax.plot(tx, ty-co2cost, '-', color=col_brown_med, linewidth=lw2, label='ガス発電単価')

#ty = df2_3['石炭発電単価-政策コスト含む']+df2_3['再エネ賦課金']+delivery_cost+retail_cost
#ty = df2_3['石炭発電単価-CPなし']+delivery_cost+retail_cost
#ax.plot(tx, ty, '--', color=col_grey_med, linewidth=lw1, label='石炭発電単価')
#co2cost = 14.0 # コスト検証WG 2023年
#ax.plot(tx, ty-co2cost, '-', color=col_grey_med, linewidth=lw2, label='石炭発電単価')

#ty = df2_1['全国-特別高圧']
#ax.plot(tx, ty, '-', color=col_teal_med, linewidth=lw1, label='全国平均単価-特別高圧')

ty = df2_1['合計']+df2_1['再エネ賦課金']
#ax.plot(tx, ty, '-', color=col_purple_med, linewidth=lw1, label='全国平均単価-高圧')

# 非FIT非化石証書(再エネ指定) 0.6 - 1.3円/kWh
#ty1 = ty + 0.6
#ty2 = ty + 1.3
#ax.fill_between(tx, ty1, ty2, color=config.COL_PURPLE_MED, alpha=0.5, label='全国平均単価-高圧+非化石証書')

# 非化石証書なし
ax.plot(tx, ty, '-', color=config.COL_PURPLE_DARK, linewidth=lw2, label='全国平均単価-高圧')

ty1 = df2_1['Min'] + df2_1['再エネ賦課金']
ty2 = df2_1['Max (沖縄を除く)'] + df2_1['再エネ賦課金'] 
ax.fill_between(tx, ty1, ty2, color=config.COL_PURPLE_LIGHT, alpha=0.5, label='全国最安値～最高値-高圧+非化石証書')

# 非化石証書
df2_2 = df2_1[df2_1['年']==2019]
tx = df2_2['time']
ty3 = df2_2['合計'] + df2_2['再エネ賦課金'] + 0.6
ty4 = df2_2['合計'] + df2_2['再エネ賦課金'] + 1.3
ax.plot(tx, ty3, '--', color=config.COL_PURPLE_MED, linewidth=lw0)
ax.plot(tx, ty4, '--', color=config.COL_PURPLE_MED, linewidth=lw0)
ax.fill_between(tx, ty3, ty4, color=config.COL_PURPLE_MED, alpha=0.25)

## BNEF (2024)
delivery_cost = 4.0
retail_cost = 3.0
# PV on-site PPA, BNEF
bx = np.array([2023, 2025])
by1 = np.array([11.0+retail_cost, 11.0+retail_cost])
by2 = np.array([18.0+retail_cost, 18.0+retail_cost])
ax.fill_between(bx, by1, by2, color=config.COL_ALIZARIN_MED, alpha=0.25)
# median
by = np.array([14.0+retail_cost, 14.0+retail_cost])
ax.plot(bx, by, '-', color=config.COL_ALIZARIN_MED, linewidth=lw0)
        
# PV offsite physical PPA, BNEF
# 再エネ賦課金: 2023年度: 1.4円/kWh, 2024年度: 3.49円/kWh
bx = np.array([2023, 2025])
by1 = np.array([13.0+1.4+delivery_cost+retail_cost, 13.0+3.49+delivery_cost+retail_cost])
by2 = np.array([20.0+1.4+delivery_cost+retail_cost, 20.0+3.49+delivery_cost+retail_cost])
ax.fill_between(bx, by1, by2, color=config.COL_ORANGE_MED, alpha=0.25)
# median
by = np.array([14.0+1.4+delivery_cost+retail_cost, 14.0+3.49+delivery_cost+retail_cost])
ax.plot(bx, by, '-', color=config.COL_ORANGE_MED, linewidth=lw0)

# onshore wind PPA, BNEF
bx = np.array([2023, 2025])
by1 = np.array([17.0+1.4+delivery_cost+retail_cost, 17.0+3.49+delivery_cost+retail_cost])
by2 = np.array([27.0+1.4+delivery_cost+retail_cost, 27.0+3.49+delivery_cost+retail_cost])
ax.fill_between(bx, by1, by2, color=config.COL_GREEN_MED, alpha=0.25)
# median
by = np.array([24.0+1.4+delivery_cost+retail_cost, 24.0+3.49+delivery_cost+retail_cost])
ax.plot(bx, by, '-', color=config.COL_GREEN_MED, linewidth=lw0)

## BNEF (2026)
delivery_cost = 4.0
retail_cost = 3.0
# PV on-site PPA, BNEF
bx = np.array([2025, 2026])
by1 = np.array([15.0+retail_cost, 15.0+retail_cost])
by2 = np.array([20.0+retail_cost, 20.0+retail_cost])
ax.fill_between(bx, by1, by2, color=config.COL_ALIZARIN_MED, alpha=0.25)
# median
by = np.array([18.0+retail_cost, 18.0+retail_cost])
ax.plot(bx, by, '-', color=config.COL_ALIZARIN_MED, linewidth=lw0)
        
# PV offsite physical PPA, BNEF
# 再エネ賦課金: 2025年度: 3.98円/kWh
bx = np.array([2025, 2026])
by1 = np.array([12.0+3.98+delivery_cost+retail_cost, 12.0+3.98+delivery_cost+retail_cost])
by2 = np.array([17.0+3.98+delivery_cost+retail_cost, 17.0+3.98+delivery_cost+retail_cost])
ax.fill_between(bx, by1, by2, color=config.COL_ORANGE_MED, alpha=0.25)
# median
by = np.array([15.0+3.98+delivery_cost+retail_cost, 15.0+3.98+delivery_cost+retail_cost])
ax.plot(bx, by, '-', color=config.COL_ORANGE_MED, linewidth=lw0)

# onshore wind PPA, BNEF
bx = np.array([2025, 2026])
by1 = np.array([16.0+3.98+delivery_cost+retail_cost, 16.0+3.98+delivery_cost+retail_cost])
by2 = np.array([21.0+3.98+delivery_cost+retail_cost, 21.0+3.98+delivery_cost+retail_cost])
ax.fill_between(bx, by1, by2, color=config.COL_GREEN_MED, alpha=0.25)
# median
by = np.array([19.0+3.98+delivery_cost+retail_cost, 19.0+3.98+delivery_cost+retail_cost])
ax.plot(bx, by, '-', color=config.COL_GREEN_MED, linewidth=lw0)



## JPEA
jx = np.array([2021, 2022])
jy = np.array([21.6+3.36, 21.6+3.36])
ax.plot(jx, jy, '-', color=config.COL_CARROT_MED, linewidth=lw2, label='JPEA Offsite PPA')
jx = np.array([2022, 2023])
jy = np.array([24.1+3.45, 24.1+3.45])
ax.plot(jx, jy, '-', color=config.COL_CARROT_MED, linewidth=lw2)
jx = np.array([2023, 2024])
jy = np.array([24.9+1.4, 24.9+1.4])
ax.plot(jx, jy, '-', color=config.COL_CARROT_MED, linewidth=lw2)


#ax.legend(loc='upper left')
ax.yaxis.set_major_locator(MultipleLocator(10))

#plt.show()
plt.savefig('charts/20260728_07_plot_spot_prices.png')

