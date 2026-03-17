# 20260316
# -*- coding: utf-8 -*-
import json
import pandas as pd
import numpy as np
import config 

input_GHGI_json_file = 'outputs/20250506_GHGI/20250506_05_ghg_data.json'

dict_dtype = {
    'id': str,
    'label': str,
    'item_name_jp': str,
    'level': int,
    'n_sub': int,
    'unit': str,
}

#dict2_dtype = {
#    'id': str,
#    'item_name_jp': str,
#    'level': int,
#    'n_sub': int,
#    'unit': str,
#}

list_ids_to_select_GHGI = [
    '02_01_01', # エネルギー転換部門 (電気・熱配分後) (エネルギー起源)
]

list_ids_to_select_ES = [
    "#500000", # FEC total
    "#600100", # 産業
    "#650000", # 業務他
    "#700000", # 家庭
    "#800000", # 運輸
]

# output file names
output_co2_json_file   = 'outputs/20251201_21_energy_stat/20260316_32_energy_stat_co2_data_common_12_総合計_エネルギー利用分_RD.json'
output_co2_excel_file  = 'outputs/20251201_21_energy_stat/20260316_32_energy_stat_co2_data_common_12_総合計_エネルギー利用分_RD.xlsx'
output_intensity_json_file  = 'outputs/20251218_01_intensity/20260316_32_energy_stat_intensity_data_common_3_エネルギー利用_RD.json'
output_intensity_excel_file = 'outputs/20251218_01_intensity/20260316_32_energy_stat_intensity_data_common_3_エネルギー利用_RD.xlsx'

YEAR1_START = 2010
YEAR1_END   = 2024


def load_GHGI_data():
    df1 = pd.read_json(input_GHGI_json_file, orient='index', dtype=dict_dtype)
    df1_subset = df1[df1['id'].isin(list_ids_to_select_GHGI)]

    return df1_subset

def load_ES_data():
    input_ES_elec_json_file = 'outputs/20251201_21_energy_stat/20251201_21_energy_stat_data_common_0_電力.json'
    input_ES_heat_json_file = 'outputs/20251201_21_energy_stat/20251201_21_energy_stat_data_common_1_熱.json'
    input_ES_co2_all_energy_json_file = 'outputs/20251201_21_energy_stat/20251201_22_energy_stat_co2_data_common_12_総合計_エネルギー利用分.json'
    input_ES_energy_json_file = 'outputs/20251201_21_energy_stat/20251201_21_energy_stat_data_common_3_エネルギー利用.json'

    df2 = pd.read_json(input_ES_elec_json_file, orient='index', dtype=dict_dtype)
    df3 = pd.read_json(input_ES_heat_json_file, orient='index', dtype=dict_dtype)
    df4 = pd.read_json(input_ES_co2_all_energy_json_file, orient='index', dtype=dict_dtype)
    df5 = pd.read_json(input_ES_energy_json_file, orient='index', dtype=dict_dtype)

#    df2_subset = df2[df2['id'].isin(list_ids_to_select_ES)]
#    df3_subset = df3[df3['id'].isin(list_ids_to_select_ES)]
#    df4_subset = df4[df4['id'].isin(list_ids_to_select_ES)]
#    df5_subset = df5[df5['id'].isin(list_ids_to_select_ES)]
#
#    return df2_subset, df3_subset, df4_subset, df5_subset
    return df2, df3, df4, df5

# redistribute co2 emission from energy transformation sector, 
# based on energy fractions of electricity and heat
def redistribute_co2(df_GHGI_et, df_ES_elec, df_ES_heat, df_ES_co2):
    with open('inputs/20251201_06_data_structure_common.json', 'r', encoding='utf-8') as f:
        data_structure_common = json.load(f)

    df_ES_co2_rev = df_ES_co2.copy()

    # total energy for electricity and heat
    df_energy_es_elec_total = df_ES_elec[df_ES_elec['id']=='#500000']
    df_energy_es_heat_total = df_ES_heat[df_ES_heat['id']=='#500000']

    for item in data_structure_common:
        t_dict = data_structure_common[item]
        tid = t_dict['id']
#        df_ES_co2_subset = df_ES_co2[df_ES_co2['id']==tid]
        pos = df_ES_co2[df_ES_co2['id']==tid].index[0]

        for y in range(YEAR1_START, YEAR1_END):
            ystr = '%d' % (y)

            # co2 emission from energy transformation sector (after elec/heat allocation)
            co2_ghgi_et = df_GHGI_et[ystr].values[0]*1.0e-3

            energy_es_elec_sector = df_ES_elec[df_ES_elec['id']==tid][ystr].values[0]
            energy_es_heat_sector = df_ES_heat[df_ES_heat['id']==tid][ystr].values[0]

            energy_es_elec_total = df_energy_es_elec_total[ystr].values[0]
            energy_es_heat_total = df_energy_es_heat_total[ystr].values[0]

            frac_elec = (energy_es_elec_sector+energy_es_heat_sector) / (energy_es_elec_total+energy_es_heat_total)
            additional_co2 = co2_ghgi_et * frac_elec

            df_ES_co2_rev.loc[pos,ystr] = df_ES_co2.loc[pos,ystr]+additional_co2

    df_ES_co2_rev.to_json(output_co2_json_file, orient='index', force_ascii=False, indent=4)
    with pd.ExcelWriter(output_co2_excel_file) as writer:
        df_ES_co2_rev.to_excel(writer, sheet_name='総合計_エネルギー利用分_エネ転換再配分')

    return df_ES_co2_rev

def calc_intensity(df_ES_co2_rev, df_ES_energy):
    df_intensity_rev = df_ES_co2_rev.copy()
    df_intensity_rev['unit'] = 'MtCO2/TJ'

    list_years = []
    for j in range(YEAR1_START, YEAR1_END):
        list_years.append('%d' % (j))

    for year in list_years:
        df_e = df_ES_energy[year]
        df_c = df_ES_co2_rev[year]
        df_intensity_rev[year] = df_c / df_e
    
    df_intensity_rev.to_json(output_intensity_json_file, orient='index', force_ascii=False, indent=4)
    with pd.ExcelWriter(output_intensity_excel_file) as writer:
        df_intensity_rev.to_excel(writer, sheet_name='エネルギー利用_エネ転換再配分')

if __name__ == '__main__':
    df_GHGI_et = load_GHGI_data()
    df_ES_elec, df_ES_heat, df_ES_co2, df_ES_energy = load_ES_data()

    df_ES_co2_rev = redistribute_co2(df_GHGI_et, df_ES_elec, df_ES_heat, df_ES_co2)
    calc_intensity(df_ES_co2_rev, df_ES_energy)
