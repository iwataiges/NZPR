# 20251208
# -*- coding: utf-8 -*-
import json
import pandas as pd
import numpy as np
import config 

GHGI_JSON_FILE  = 'outputs/20251201_31_GHGI/20251205_32_GHGI_ghg_toplevel.json'
YEAR_START = 1990
YEAR_END   = 2024

dict_dtype = {
    'id': str,
    'label': str,
    'item_name_jp': str,
    'level': int,
    'n_sub': int,
    'unit': str,
}

if __name__ == '__main__':
    df1 = pd.read_json(GHGI_JSON_FILE, orient='index', dtype=dict_dtype)

    df2 = df1[['id','label','item_name_jp','level','n_sub','unit']].copy()

    for i in range(YEAR_START+1, YEAR_END):
        year = '%d' % (i)
        df2[year] = df1[year] - df1['%d' % (i-1)]
    
    df2.to_json('outputs/20251201_31_GHGI/20251208_02_GHGI_ghg_toplevel_diff.json', orient='index', force_ascii=False, indent=4)
    df2.to_excel('outputs/20251201_31_GHGI/20251208_02_GHGI_ghg_toplevel_diff.xlsx')
