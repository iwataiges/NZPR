# 20251203, 20260225
# -*- coding: utf-8 -*-
import json
import pandas as pd
import numpy as np
import config 

input_json_file = 'outputs/20251201_31_GHGI/20251205_32_GHGI_ghg_toplevel.json'
dict_dtype = {
    'id': str,
    'label': str,
    'item_name_jp': str,
    'level': int,
    'n_sub': int,
    'unit': str,
}

YEAR_START1 = 2019
YEAR_END1   = 2024

YEAR_START2 = 2014
YEAR_END2   = 2024


def load_GHGI_data():
    df0 = pd.read_json(input_json_file, orient='index', dtype=dict_dtype)
    df1 = df0[(df0['id']=='03')]

    return df1

def fitting1(df, year_start, year_end):
    list_years = []
    for i in range(year_start, year_end):
        list_years.append('%d' % (i))

    df_subset = df[list_years]

    tx = np.arange(year_start, year_end) - 2013
    ty = df_subset.sum().values
    ty = ty*1.0e-3 # to MtCO2e

    fit1 = np.polyfit(tx, ty, 1)
    return fit1

def fitting2(df, year_start, year_end):#print(tx, ty)
    list_years = []
    for i in range(year_start, year_end):
        list_years.append('%d' % (i))

    df_subset = df[list_years]
    df_subset = df_subset.drop(columns=['2020'])

    tx = np.array([2014, 2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023]) - 2013
    ty = df_subset.sum().values
    ty = ty*1.0e-3 # to MtCO2e

    fit2 = np.polyfit(tx, ty, 1)
    return fit2


if __name__ == '__main__':
    df = load_GHGI_data()
    fit1 = fitting1(df, YEAR_START1, YEAR_END1)
    fit2 = fitting2(df, YEAR_START2, YEAR_END2)
    print(fit1)
    print(fit2)
