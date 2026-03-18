# -*- coding: utf-8 -*-
import json
#import openpyxl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.patches as patches
import config 

rcParams['font.size'] = 24
rcParams['axes.labelsize'] = 24
rcParams['xtick.labelsize'] = 20
rcParams['ytick.labelsize'] = 20
#rcParams['lines.markersize'] = 10
rcParams['lines.linewidth'] = 3
rcParams['font.family'] = 'Hiragino Sans'

energy_stat_json = 'outputs/20251201_21_energy_stat/20251201_21_energy_stat_data_common_3_エネルギー利用.json'
energy_1p5CRM_balance_json = 'outputs/20251201_01_1p5CRM_balance_energy/20251201_11_1p5CRM_balance_energy_data_common_10_エネルギー利用.json'
energy_1p5CRM_steps_json   = 'outputs/20251201_03_1p5CRM_steps_energy/20251201_13_1p5CRM_steps_energy_data_common_10_エネルギー利用.json'

energy_stat_fit_results = [
    {
        "sector": "total",
        "a": -1.949e-01,
        "b": 1.237e+01,
    },
    {
        "sector": "industry",
        "a": -7.859e-02,
        "b": 4.926e+00,
    },
    {
        "sector": "commercial",
        "a": -3.710e-02,
        "b": 2.221e+00,
    },
    {
        "sector": "residential",
        "a": -2.602e-02,
        "b": 1.991e+00,
    },
    {
        "sector": "transport",
        "a": -5.316e-02,
        "b": 3.232e+00,
    }
]

ids = [
    {
        "sector": "total",
        "sector_jp": "全体",
        "id": "#500000",
    },
    {
        "sector": "industry",
        "sector_jp": "産業",
        "id": "#600100",
    },
    {
        "sector": "commercial",
        "sector_jp": "業務他",
        "id": "#650000",
    },
    {
        "sector": "residential",
        "sector_jp": "家庭",
        "id": "#700000",
    },
    {
        "sector": "transport",
        "sector_jp": "運輸",
        "id": "#800000",
    }
]

f_steps_2030 = np.zeros(len(ids))
f_ext_2030   = np.zeros(len(ids))
diff_ext_steps_2030 = np.zeros(len(ids))
f_balance_2030 = np.zeros(len(ids))
diff_ext_balance_2030 = np.zeros(len(ids))

f_steps_2040 = np.zeros(len(ids))
f_ext_2040   = np.zeros(len(ids))
diff_ext_steps_2040 = np.zeros(len(ids))
f_balance_2040 = np.zeros(len(ids))
diff_ext_balance_2040 = np.zeros(len(ids))

def load_json():
    dict1_dtype = {
        'id': str,
        'item_name_jp': str,
        'level': int,
        'n_sub': int,
        'unit': str,
        '2010': float,
        '2011': float,
        '2012': float,
        '2013': float,
        '2014': float,
        '2015': float,
        '2016': float,
        '2017': float,
        '2018': float,
        '2019': float,
        '2020': float,
        '2021': float,
        '2022': float,
        '2023': float,
    }
    df0 = pd.read_json(energy_stat_json, orient='index', dtype=dict1_dtype)
    df_energy_stat = df0[['id', '2013', '2023']]

    dict2_dtype = {
        'id': str,
        'item_name_jp': str,
        'level': int,
        'n_sub': int,
        'unit': str,
        'baseyear': float,
        '2030': float,
        '2040': float,
        '2050': float,
    }
    df0 = pd.read_json(energy_1p5CRM_balance_json, orient='index', dtype=dict2_dtype)
    df_1p5CRM_balance = df0[['id', '2030', '2040']]
    df0 = pd.read_json(energy_1p5CRM_steps_json, orient='index', dtype=dict2_dtype)
    df_1p5CRM_steps = df0[['id', '2030', '2040']]

    return df_energy_stat, df_1p5CRM_balance, df_1p5CRM_steps

def calculation(df_energy_stat, df_1p5CRM_balance, df_1p5CRM_steps):
    print('2030.')
    print('id,steps/2013,ext/2013,ext-steps,balance/2013,balance-steps')
    for i in range(len(ids)):
        id = ids[i]['id']

        # baseline (2013)
        e_2013 = df_energy_stat[df_energy_stat['id'] == id]['2013'].values[0]*1.0e-6

        # extrapolation
        a = energy_stat_fit_results[i]['a']
        b = energy_stat_fit_results[i]['b']
        e_ext_2030 = a * (2030 - 2013) + b
        # 1.5CRM
        e_1p5CRM_balance_2030 = df_1p5CRM_balance[df_1p5CRM_balance['id'] == id]['2030'].values[0]*1.0e-6
        e_1p5CRM_steps_2030 = df_1p5CRM_steps[df_1p5CRM_steps['id'] == id]['2030'].values[0]*1.0e-6

        f_steps_2030[i] = e_1p5CRM_steps_2030 / e_2013
        f_ext_2030[i]   = e_ext_2030 / e_2013
        diff_ext_steps_2030[i] = f_ext_2030[i] - f_steps_2030[i]

        f_balance_2030[i] = e_1p5CRM_balance_2030 / e_2013
        diff_ext_balance_2030[i] = f_ext_2030[i] - f_balance_2030[i]

        #print('%s %.2f %.2f %.2f %.2f ' % (id, e_2013, e_ext_2030, e_1p5CRM_balance_2030, e_1p5CRM_steps_2030))
        print('%s %.2f  %.2f %5.2f  %.2f %5.2f ' % (id, f_steps_2030[i], f_ext_2030[i], diff_ext_steps_2030[i], f_balance_2030[i], diff_ext_balance_2030[i]))

    print('2040.')
    print('id,steps/2013,ext/2013,ext-steps,balance/2013,ext-balance')
    for i in range(len(ids)):
        id = ids[i]['id']

        a = energy_stat_fit_results[i]['a']
        b = energy_stat_fit_results[i]['b']

        e_2013 = df_energy_stat[df_energy_stat['id'] == id]['2013'].values[0]*1.0e-6
        e_ext_2040 = a * (2040 - 2013) + b
        e_1p5CRM_balance_2040 = df_1p5CRM_balance[df_1p5CRM_balance['id'] == id]['2040'].values[0]*1.0e-6
        e_1p5CRM_steps_2040 = df_1p5CRM_steps[df_1p5CRM_steps['id'] == id]['2040'].values[0]*1.0e-6

        f_steps_2040[i] = e_1p5CRM_steps_2040 / e_2013
        f_ext_2040[i]   = e_ext_2040 / e_2013
        diff_ext_steps_2040[i] = f_ext_2040[i] - f_steps_2040[i]

        f_balance_2040[i] = e_1p5CRM_balance_2040 / e_2013
        diff_ext_balance_2040[i] = f_ext_2040[i] - f_balance_2040[i]

        print('%s %.2f  %.2f %5.2f  %.2f %5.2f ' % (id, f_steps_2040[i], f_ext_2040[i], diff_ext_steps_2040[i], f_balance_2040[i], diff_ext_balance_2040[i]))

def plot_2030():
    fig, ax = plt.subplots(figsize=(12, 8))

    lw1 = 2
    fs1 = 20
    fs2 = 16

    width = 0.75
    height = 0.75
    gap1 = 0.1
    gap2 = 0.125

    xoffset0 = 0.2
    xoffset1 = 0.7
    xoffset2 = xoffset1 + width/2 + gap1
    xoffset3 = xoffset2 + width/2 + gap1
    xoffset4 = xoffset3 + width + gap2
    xoffset5 = xoffset4 + width/2 + gap1

    scale1 = 0.5

    ax.set_axis_off()

    ax.set_xlim(0.25, 3.8)
    ax.set_ylim(-0.1, len(ids) + 0.5)

    ax.text(xoffset1+width/4, len(ids)+0.33, '現状延長\n2030年\nFEC削減割合\n(2013年比)', ha='center', va='center', fontsize=fs2)
    ax.text(xoffset2+width/4, len(ids)+0.33, '政府目標\n2030年\nFEC削減割合\n(2013年比)', ha='center', va='center', fontsize=fs2)
    ax.text(xoffset3+width/2, len(ids), '現状延長と政府目標の差', ha='center', va='center', fontsize=fs2)
    ax.text(xoffset4+width/4, len(ids)+0.33, '1.5℃RM\n2030年\nFEC削減割合\n(2013年比)', ha='center', va='center', fontsize=fs2)
    ax.text(xoffset5+width/2, len(ids), '現状延長と1.5℃RMの差', ha='center', va='center', fontsize=fs2)

    for i in range(len(ids)):
        by = len(ids) - i - 1

        bx = xoffset0
        ax.text(bx+width/2, by+height/2, ids[i]['sector_jp'], ha='right', va='center', color='black', fontsize=fs1, weight='bold')

        bx = xoffset1
        r = patches.Rectangle((bx, by), width/2, height, edgecolor=config.COL_ASBESTOS_LIGHT, fill=False, linewidth=lw1)
        ax.add_patch(r)
        text = '%d%%' % int((1.0-f_ext_2030[i])*100)
        ax.text(bx+width/4, by+height/2, text, ha='center', va='center', color='black', fontsize=fs1)

        bx = xoffset2
        r = patches.Rectangle((bx, by), width/2, height, edgecolor=config.COL_ASBESTOS_LIGHT, fill=False, linewidth=lw1)
        ax.add_patch(r)
        text = '%d%%' % int((1.0-f_steps_2030[i])*100)
        ax.text(bx+width/4, by+height/2, text, ha='center', va='center', color='black', fontsize=fs1)

        bx = xoffset3
        if diff_ext_steps_2030[i] > 0.0:
            diff = (1.0 - diff_ext_steps_2030[i]/scale1) * 255.0
            f = hex(int(diff))[2:].zfill(2)
            col = '#ff%s%s' % (f,f)
            text = '+%.1f%%' % (diff_ext_steps_2030[i]*100)
        else:
            diff = (1.0 + diff_ext_steps_2030[i]/scale1) * 255.0
            f = hex(int(diff))[2:].zfill(2)
            col = '#%sff%s' % (f,f)
            text = '%.1f%%' % (diff_ext_steps_2030[i]*100)
        r = patches.Rectangle((bx, by), width, height, edgecolor=config.COL_ASBESTOS_LIGHT, facecolor=col, fill=True, linewidth=lw1)
        ax.add_patch(r)
        ax.text(bx+width/2, by+height/2, text, ha='center', va='center', color='black', fontsize=fs1)

        bx = xoffset4
        r = patches.Rectangle((bx, by), width/2, height, edgecolor=config.COL_ASBESTOS_LIGHT, fill=False, linewidth=lw1)
        ax.add_patch(r)
        text = '%d%%' % int((1.0-f_balance_2030[i])*100)
        ax.text(bx+width/4, by+height/2, text, ha='center', va='center', color='black', fontsize=fs1)

        bx = xoffset5
        if diff_ext_balance_2030[i] > 0.0:
            diff = (1.0 - diff_ext_balance_2030[i]/scale1) * 255.0
            f = hex(int(diff))[2:].zfill(2)
            col = '#ff%s%s' % (f,f)
            text = '+%.1f%%' % (diff_ext_balance_2030[i]*100)
        else:
            diff = (1.0 + diff_ext_balance_2030[i]/scale1) * 255.0
            f = hex(int(diff))[2:].zfill(2)
            col = '#%sff%s' % (f,f)
            text = '%.1f%%' % (diff_ext_balance_2030[i]*100)
        r = patches.Rectangle((bx, by), width, height, edgecolor=config.COL_ASBESTOS_LIGHT, facecolor=col, fill=True, linewidth=lw1)
        ax.add_patch(r)
        ax.text(bx+width/2, by+height/2, text, ha='center', va='center', color='black', fontsize=fs1)

    plt.tight_layout()
    plt.savefig('charts/20260318_10_NZPR_sector_summary_calc_FEC_2030.png')


def plot_2040():
    fig, ax = plt.subplots(figsize=(12, 8))

    lw1 = 2
    fs1 = 20
    fs2 = 16

    width = 0.75
    height = 0.75
    gap1 = 0.1
    gap2 = 0.125

    xoffset0 = 0.2
    xoffset1 = 0.7
    xoffset2 = xoffset1 + width/2 + gap1
    xoffset3 = xoffset2 + width/2 + gap1
    xoffset4 = xoffset3 + width + gap2
    xoffset5 = xoffset4 + width/2 + gap1

    scale1 = 0.5

    ax.set_axis_off()

    ax.set_xlim(0.25, 3.8)
    ax.set_ylim(-0.1, len(ids) + 0.5)

    ax.text(xoffset1+width/4, len(ids)+0.33, '現状延長\n2040年\nFEC削減割合\n(2013年比)', ha='center', va='center', fontsize=fs2)
    ax.text(xoffset2+width/4, len(ids)+0.33, '政府目標\n2040年\nFEC削減割合\n(2013年比)', ha='center', va='center', fontsize=fs2)
    ax.text(xoffset3+width/2, len(ids), '現状延長と政府目標の差', ha='center', va='center', fontsize=fs2)
    ax.text(xoffset4+width/4, len(ids)+0.33, '1.5℃RM\n2040年\nFEC削減割合\n(2013年比)', ha='center', va='center', fontsize=fs2)
    ax.text(xoffset5+width/2, len(ids), '現状延長と1.5℃RMの差', ha='center', va='center', fontsize=fs2)

    for i in range(len(ids)):
        by = len(ids) - i - 1

        bx = xoffset0
        ax.text(bx+width/2, by+height/2, ids[i]['sector_jp'], ha='right', va='center', color='black', fontsize=fs1, weight='bold')

        bx = xoffset1
        r = patches.Rectangle((bx, by), width/2, height, edgecolor=config.COL_ASBESTOS_LIGHT, fill=False, linewidth=lw1)
        ax.add_patch(r)
        text = '%d%%' % int((1.0-f_ext_2040[i])*100)
        ax.text(bx+width/4, by+height/2, text, ha='center', va='center', color='black', fontsize=fs1)

        bx = xoffset2
        r = patches.Rectangle((bx, by), width/2, height, edgecolor=config.COL_ASBESTOS_LIGHT, fill=False, linewidth=lw1)
        ax.add_patch(r)
        text = '%d%%' % int((1.0-f_steps_2040[i])*100)
        ax.text(bx+width/4, by+height/2, text, ha='center', va='center', color='black', fontsize=fs1)

        bx = xoffset3
        if diff_ext_steps_2040[i] > 0.0:
            diff = (1.0 - diff_ext_steps_2040[i]/scale1) * 255.0
            f = hex(int(diff))[2:].zfill(2)
            col = '#ff%s%s' % (f,f)
            text = '+%.1f%%' % (diff_ext_steps_2040[i]*100)
        else:
            diff = (1.0 + diff_ext_steps_2040[i]/scale1) * 255.0
            f = hex(int(diff))[2:].zfill(2)
            col = '#%sff%s' % (f,f)
            text = '%.1f%%' % (diff_ext_steps_2040[i]*100)
        r = patches.Rectangle((bx, by), width, height, edgecolor=config.COL_ASBESTOS_LIGHT, facecolor=col, fill=True, linewidth=lw1)
        ax.add_patch(r)
        ax.text(bx+width/2, by+height/2, text, ha='center', va='center', color='black', fontsize=fs1)

        bx = xoffset4
        r = patches.Rectangle((bx, by), width/2, height, edgecolor=config.COL_ASBESTOS_LIGHT, fill=False, linewidth=lw1)
        ax.add_patch(r)
        text = '%d%%' % int((1.0-f_balance_2040[i])*100)
        ax.text(bx+width/4, by+height/2, text, ha='center', va='center', color='black', fontsize=fs1)

        bx = xoffset5
        if diff_ext_balance_2040[i] > 0.0:
            diff = (1.0 - diff_ext_balance_2040[i]/scale1) * 255.0
            f = hex(int(diff))[2:].zfill(2)
            col = '#ff%s%s' % (f,f)
            text = '+%.1f%%' % (diff_ext_balance_2040[i]*100)
        else:
            diff = (1.0 + diff_ext_balance_2040[i]/scale1) * 255.0
            f = hex(int(diff))[2:].zfill(2)
            col = '#%sff%s' % (f,f)
            text = '%.1f%%' % (diff_ext_balance_2040[i]*100)
        r = patches.Rectangle((bx, by), width, height, edgecolor=config.COL_ASBESTOS_LIGHT, facecolor=col, fill=True, linewidth=lw1)
        ax.add_patch(r)
        ax.text(bx+width/2, by+height/2, text, ha='center', va='center', color='black', fontsize=fs1)

    plt.tight_layout()
    plt.savefig('charts/20260318_10_NZPR_sector_summary_calc_FEC_2040.png')


if __name__ == '__main__':
    df_energy_stat, df_1p5CRM_balance, df_1p5CRM_steps = load_json()
    calculation(df_energy_stat, df_1p5CRM_balance, df_1p5CRM_steps)
    plot_2030()
    plot_2040()
