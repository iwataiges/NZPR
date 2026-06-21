# work log for NZPR

(** previous repository (GHGpath) **)

## 20250506-1
### input from GHG intentory excel file to generate GHG data frame
```
python scripts/20250506_05_import_GHG_data.py
```
 => outputs/20250506_05_ghg_data.json, outputs/20250506_05_ghg_data.xlsx

## 20250721

add inputs/energy_stat/20250721_04_energy_statistics_data_structure.xlsx which contains position information for coal, oil, gas, nuclear, etc.

```
python scripts/20250721_04_import_energy_stat.py 
```
 => outputs/20250721_04_energy_stat_data.xlsx, 20250721_04_energy_stat_data_0_電力.json, ... 20250721_04_energy_stat_data_15_原子力発電.json

## 20251020 - 21-1

* inputs/energy_stat/20251020_05_energy_statistics_data_structure_co2.xlsx を更新し、エネルギー転換と統計誤差の行、総合計_電力･熱寄与間接排出配分後合計と総合計_エネルギー利用分の列を追加
```
python scripts/20251020_05_import_energy_stat_co2.py
```
=> outputs/20250721_04_energy_stat/20251020_05_energy_stat_co2_data.xlsx, ...json

* 総合エネルギー統計のエネルギー起源CO2とGHGIのそれとの比較
* エネルギー転換部門に大きな差異
* それ以外の各部門にも <400ktCO2の差異
* see: NZPR/20251020work/20251020_05_energy_stat_co2_data_work.xlsx (sheet: 総合計_エネルギー利用分)

* CO2/GHGについては、GHG inventoryの情報を使うべきか (大きな齟齬はない)

## 20251118
inputs/1p5CRM/20231114_1p5CRM_balance_energy_co2_rev1.xlsx,
inputs/1p5CRM/20231114_1p5CRM_steps_energy_co2_rev4.xlsx: baseyearのエネルギー消費量(N40)の修正

```
mkdir outputs/20251118_01_1p5CRM_balance_energy
python scripts/20251118_01_import_1p5CRM_balance_energy.py 
mkdir outputs/20251118_02_1p5CRM_balance_co2
python scripts/20251118_02_import_1p5CRM_balance_co2.py

mkdir outputs/20251118_03_1p5CRM_steps_energy
python scripts/20251118_03_import_1p5CRM_steps_energy.py
mkdir outputs/20251118_04_1p5CRM_steps_co2
python scripts/20251118_04_import_1p5CRM_steps_co2.py 
```

commonデータセット
'合計'は1.5CRMでは「合計」がエネルギー利用と同じになっているが、総合エネルギー統計を合わせるため、エネルギー利用と非エネルギー利用の和を計算
```
ls -1 outputs/20251118_01_1p5CRM_balance_energy/20251118_01_1p5CRM_balance_energy_data*.json > outputs/20251118_01_1p5CRM_balance_energy/list_20251118_01_1p5CRM_balance_energy_json.txt
#python scripts/20251119_11_refine_data_structure_1p5CRM_balance_energy.py 
```

data structure update: 20251120_06_1p5CRM_data_structure.xlsx

```
python scripts/20251118_02_import_1p5CRM_balance_co2.py

ls -1 outputs/20251118_02_1p5CRM_balance_co2/20251118_02_1p5CRM_balance_co2_data*.json > outputs/20251118_02_1p5CRM_balance_co2/list_20251118_02_1p5CRM_balance_co2_json.txt
#python scripts/20251119_12_refine_data_structure_1p5CRM_balance_co2.py
```

```
ls -1 outputs/20251118_03_1p5CRM_steps_energy/20251118_03_1p5CRM_steps_energy_data*.json > outputs/20251118_03_1p5CRM_steps_energy/list_20251118_03_1p5CRM_steps_energy_json.txt
#python scripts/20251119_13_refine_data_structure_1p5CRM_steps_energy.py 

python scripts/20251118_04_import_1p5CRM_steps_co2.py 
ls -1 outputs/20251118_04_1p5CRM_steps_co2/20251118_04_1p5CRM_steps_co2_data*.json > outputs/20251118_04_1p5CRM_steps_co2/list_20251118_04_1p5CRM_steps_co2_json.txt
#python scripts/20251119_14_refine_data_structure_1p5CRM_steps_co2.py
```

## 20251120

commonデータセット
総合エネルギー統計

```
#ls -1 outputs/20250721_04_energy_stat/20250721_04_energy_stat_data*.json > outputs/20251120_21_energy_stat/list_20250721_04_energy_stat_json.txt
#python scripts/20251120_21_refine_data_structure_energy_stat.py

ls -1 outputs/20250721_04_energy_stat/20251020_05_energy_stat_co2_data*.json > outputs/20251120_21_energy_stat/list_20251020_05_energy_stat_co2_json.txt
#python scripts/20251120_22_refine_data_structure_energy_stat_co2.py 
```

CO2排出量は「総合計_電力･熱寄与間接排出配分後合計」のデータが1.5CRMと比較できるものとなる（電気・熱配分後に相当）


### common dataset:
* data structure definition: inputs/20251118_05_data_structure_common.json
* 1.5CRM, balanced scenario: 
   * energy: outputs/20251118_01_1p5CRM_balance_energy/20251119_11_1p5CRM_balance_energy_data_common*.json
   * CO2: outputs/20251118_02_1p5CRM_balance_co2/20251119_12_1p5CRM_balance_co2_data_common*.json
* 1.5CRM, stated-policy scenario:
   * energy: outputs/20251118_03_1p5CRM_steps_energy/20251119_13_1p5CRM_steps_energy_data_common*.json
   * CO2: outputs/20251118_04_1p5CRM_steps_co2/20251119_14_1p5CRM_steps_co2_data_common*.json
* Energy Statistics:
   * energy: outputs/20251120_21_energy_stat/20251120_21_energy_stat_data_common*.json
   * CO2: outputs/20251120_21_energy_stat/20251120_22_energy_stat_co2_data_common*.json

* note:
   * 1.5CRMのエネルギーは「合計」がエネルギー利用と同じになっているのに対し、総合エネルギー統計では、エネルギー利用と非エネルギー利用の和になっている。common datasetでは、総合エネルギー統計に合わせ、合計はエネルギー利用と非エネルギー利用の和としている。
   * 総合エネルギー統計及びGHGインベントリのエネルギー起源CO2排出量と一致した数値の出し方が不明

## 20251201
* common dataset definition: inputs/20251201_06_data_structure_common.json
```
mkdir outputs/20251201_01_1p5CRM_balance_energy
python scripts/20251201_11_refine_data_structure_1p5CRM_balance_energy.py 
mkdir outputs/20251201_02_1p5CRM_balance_co2
python scripts/20251201_12_refine_data_structure_1p5CRM_balance_co2.py
mkdir outputs/20251201_03_1p5CRM_steps_energy
python scripts/20251201_13_refine_data_structure_1p5CRM_steps_energy.py 
mkdir outputs/20251201_04_1p5CRM_steps_co2
python scripts/20251201_14_refine_data_structure_1p5CRM_steps_co2.py

mkdir outputs/20251201_21_energy_stat
python scripts/20251201_21_refine_data_structure_energy_stat.py
python scripts/20251201_22_refine_data_structure_energy_stat_co2.py 
```

common dataset of GHGI
```
mkdir outputs/20251201_31_GHGI
python scripts/20251201_31_refine_data_structure_GHGI_co2.py
```

## 20251203-2
* GHGインベントリ top-level emissions json/excel
```
python scripts/20251203_01_extract_GHGI_ghg_toplevel.py
```
outputs/20251201_31_GHGI/20251203_32_GHGI_ghg_toplevel.json, --.xlsx

* LULUCFを追加. id:06
   * 参考: 2024年4月のGHGインベントリでは2013年の総排出量は1407MtCO2で、これが2035/2040NDCの基準値になっている。2025年4月のインベントリでは2013年の総排出量は1395MtCO2。
```
python scripts/20251205_02_extract_GHGI_ghg_toplevel.py
```
outputs/20251201_31_GHGI/20251205_32_GHGI_ghg_toplevel.json, --.xlsx

## 20251205
```
mkdir inputs/IPCC/
```
copy data_syr_spm5_all_panels.xlsx

```
python scripts/20251208_01_plot_GHG_total_IPCC.py
```
charts/20251208_01_plot_GHG_total_IPCC.png
* IPCC C1, C3 (90%-ile) AR6 SYR Fig. SPM.5で表示された経路.
* IPCCの2019年GHG net emissionsは59.09 GtCO2e/yr. C1の2015,2020から内挿した2019年の値は54.93. C1は実際の経路よりも2019年時点で下を通っている。2019年59.09で規格化し、日本のGHGIネット排出量にスケールすると、C1の90%-ile範囲に、2030年、2035年NDCは入っていない。
* 2024 NDC paperでは、OWIDのGHG排出量とIPCC報告書のグラフデータとの2015年時点での差分を使って2019年時点の値を推計し57.04を2019年の値として使っていた。

## 20251208

* GHGIのデータにつき前年との差分を計算
```
python scripts/20251208_02_get_GHGI_diff.py
```
outputs/20251201_31_GHGI/20251208_02_GHGI_ghg_toplevel_diff.json, --.xlsx

* GHG reduction level (gap)
```
python scripts/20251208_03_plot_GHGI_diff.py
```
charts/20251208_03_plot_GHG_total_diff.png

* 1.5CRMの経路との比較
```
cp -p ~/ikuru.iwata@mx.iges.or.jp\ -\ Google\ Drive/My\ Drive/research/2024/20240104GHGpathway_policybrief/20240104calc/20240123GHGpath.xlsx inputs/1p5CRM
mkdir outputs/20251208_01_1p5CRM_GHG
python scripts/20251208_04_import_1p5CRM_balance_GHG.py
python scripts/20251208_04_import_1p5CRM_steps_GHG.py
python scripts/20251208_05_plot_GHG_total_1p5CRM.py 
```
outputs/20251208_01_1p5CRM_GHG/20251208_04_1p5CRM_balance_GHG_data.json, --.xlsx
outputs/20251208_01_1p5CRM_GHG/20251208_04_1p5CRM_steps_GHG_data.json, --.xlsx
charts/20251208_05_plot_GHG_total_1p5CRM.png

## 20251218-1

* エネルギー起源CO2と電力について、排出係数の計算。エネバラでは、CO2排出量について、「12_総合計_エネルギー利用分」を使う。12/2に検討した、エネルギー転換部門の自家消費や損失に伴うズレがある

```
mkdir outputs/20251218_01_intensity
python scripts/20251218_01_calc_intensity_energy_stat.py
python scripts/20251218_02_calc_intensity_1p5CRM_balance.py
python scripts/20251218_03_calc_intensity_1p5CRM_steps.py
```
outpus/20251218_01_intensity/
20251218_01_energy_stat_intensity_data_common.xlsx
20251218_01_energy_stat_intensity_data_common_0_電力.json
20251218_01_energy_stat_intensity_data_common_3_エネルギー利用.json
20251218_02_1p5CRM_balance_intensity_data_common.xlsx
20251218_02_1p5CRM_balance_intensity_data_common_07_電力.json
20251218_02_1p5CRM_balance_intensity_data_common_10_エネルギー利用.json
20251218_03_1p5CRM_steps_intensity_data_common.xlsx
20251218_03_1p5CRM_steps_intensity_data_common_07_電力.json
20251218_03_1p5CRM_steps_intensity_data_common_10_エネルギー利用.json

(20260311note: 20251218_01_energy_stat_intensityは20260311_01_energy_stat_intensityに更新)

## 20251218-3

* エネ基 エネルギー需給見通し 需要側情報: inputs/SEP/20251218_01_SEP_numbers.xlsx

```
mkdir outputs/20251218_02_SEP
python scripts/20251218_15_import_SEP_numbers.py       
```
outputs/20251218_02_SEP/20251218_15_SEP_numbers.json, --.xlsx
* 部門ごとの最終エネルギー消費量、電力需要、CO2排出量、排出係数
(20260311note: 20260311_02_SEP_numbersに更新)

## 20260116-1

* 7次エネ基の「技術進展」=「排出上振れ」シナリオの場合の2040年のGHG排出量推計
   * 需給見通しによると、エネルギー起源CO2排出量は、4シナリオで3.65-3.67億tCO2に対し、技術進展シナリオは5.39億tCO2 → +174MtCO2
   * 他のガスは変化ないとすると、GHGは2040年に 380 + 174 = 554 MtCO2。2013年1407MtCO2に対し60.6%削減

```
python scripts/scripts/20260116_02_plot_GHG_total_IPCC.py
python scripts/scripts/20260116_06_plot_GHG_total_1p5CRM.py
```
charts/20260116_02_plot_GHG_total_IPCC.png, 20260116_06_plot_GHG_total_1p5CRM.png

## 20260116-2

* エネ基 エネルギー需給見通し 需要側情報 (id追加): inputs/SEP/20260116_02_SEP_numbers.xlsx

```
python scripts/20260116_15_import_SEP_numbers.py
```
outputs/20251218_02_SEP/20260116_15_SEP_numbers.json, --.xlsx
部門ごとの最終エネルギー消費量、電力需要、CO2排出量、排出係数
(20260311note: 20260311_02_SEP_numbersに更新)


## 20260122
* GHG pathフィッティングを2014-2023 (2020除く)に
```
python scripts/20260122_06_plot_GHG_total.py
```
charts/20260122_06_plot_GHG_total.png, 20260122_06_plot_GHG_total_wo_failure2040.png (2040上振れの点なし)

## 20260205

* FEC for sectors, fitting 2014-2023 (excl. 2020)
```
python scripts/20260205_10_plot_energy_FEC_sectors.py
python scripts/20260205_10_plot_energy_FEC_sectors_EN.py
```
a:-7.859e-02 b:4.926e+00 2030:3.59 2035:3.20 産業
a:-8.033e-02 b:4.578e+00 2030:3.21 2035:2.81 製造
a:-4.180e-02 b:1.810e+00 2030:1.10 2035:0.89 鉄鋼
a:-3.710e-02 b:2.221e+00 2030:1.59 2035:1.41 業務他
a:-2.602e-02 b:1.991e+00 2030:1.55 2035:1.42 家庭
a:-5.316e-02 b:3.232e+00 2030:2.33 2035:2.06 運輸
charts/20260205_10_plot_energy_00_産業.png, etc.
chart/charts/20260205_10_plot_energy_00_Industry_EN.png, etc.

* CO2 for sectors, fitting 2014-2023 (excl. 2020)
```
python scripts/20260205_11_plot_co2_energy_sectors.py
python scripts/20260205_11_plot_co2_energy_sectors_EN.py
```
a:-1.118e+01 b:4.558e+02 2030:265.80 2035:209.91 産業
a:-1.119e+01 b:4.290e+02 2030:238.69 2035:182.71 製造
a:-5.141e+00 b:1.831e+02 2030:95.73 2035:70.03 鉄鋼
a:-6.199e+00 b:2.304e+02 2030:125.02 2035:94.02 業務他
a:-5.001e+00 b:1.969e+02 2030:111.87 2035:86.86 家庭
a:-3.883e+00 b:2.258e+02 2030:159.82 2035:140.41 運輸
charts/20260205_11_plot_co2_energy_00_産業.png, etc.
charts/20260205_11_plot_co2_energy_00_Industry_EN.png, etc.

* CO2 intensity for sectors, fitting 2014-2023 (excl. 2020)
```
python scripts/20260205_13_plot_intensity_energy_sectors.py
python scripts/20260205_13_plot_intensity_energy_sectors_EN.py
```
a:-9.583e-07 b:9.289e-05 2030:7.660e-05 2035:7.181e-05 産業
a:-9.868e-07 b:9.410e-05 2030:7.732e-05 2035:7.239e-05 製造
a:-6.620e-07 b:1.015e-04 2030:9.026e-05 2035:8.695e-05 鉄鋼
a:-1.285e-06 b:1.042e-04 2030:8.236e-05 2035:7.594e-05 業務他
a:-1.403e-06 b:9.921e-05 2030:7.537e-05 2035:6.836e-05 家庭
a:-6.285e-08 b:6.989e-05 2030:6.882e-05 2035:6.851e-05 運輸
charts/20260205_13_plot_intensity_energy_00_産業.png, etc.
charts/20260205_13_plot_intensity_energy_00_Industry_EN.png, etc.


--------
(working on NZPR repository)

## 20260224

* at github.com/repos/ create a new repository "NZPR"

```
cd ~/Documents/work/github
git clone git@github.com:iwataiges/NZPR.git
```

* working on doc/template/20260224_my-reference.docx
* to generate docx from markdown:
```
pandoc doc/report2026/20260224_01_NZPR_report.md --reference-doc=doc/template/20260224_my-reference.docx -o test/20260430_01_NZPR_report.docx 
```
    * (files under test directory will not be synced)

* python execution environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt 


## 20260225 
(update from 20251212)
* GHGI net CO2 emissions
* linear fitting
```
python scripts/20250225_01_GHGI_fitting_co2.py
```
- 2019 - 2023: y = a * (x-2013) + b, a = -22.71781753 b = 1170.85070326
- 2014 - 2023 (2020除く): a = -27.69784371 b = 1220.09373201

* [地球温暖化対策計画(2025/2/18)](https://www.env.go.jp/earth/ondanka/keikaku/250218.html)の概要に記された、エネルギー起源、非エネルギー起源CO2、CH4, N2O, F-gasの2030年、2040年の目安・目標: inputs/20250218plan_GWC_GHG2030_2040.xlsx
   * 2030年: net CO2 = 677 + 70.0 - 47.7 = 699.3
   * 2040年: net CO2 = 360 / 370 + 59 - 84 = 335 / 345

* IPCC C1/C3との比較、1.5CRMとの比較
```
python scripts/20260225_02_plot_CO2_net_IPCC.py 
python scripts/20260225_03_plot_CO2_net_1p5CRM.py
```
charts/20260225_02_plot_CO2_net_IPCC.png
charts/20260225_03_plot_CO2_net_1p5CRM.png

* GHGI CH4
```
python scripts/20260225_04_GHGI_fitting_ch4.py
```
- 2019-2023: a = -0.31787239 b=32.6578949
- 2014-2023 (excl. 2020): a = -0.28798915 b=32.43185503
```
python scripts/20260225_05_plot_CH4_IPCC.py
```
charts/20260225_05_plot_CH4_IPCC.png

## 20260226-1

* update GHG diff plots (upside down)
```
python scripts/20260226_03_plot_GHGI_diff.py
python scripts/20260226_03_plot_GHGI_diff_EN.py
```
charts/charts/20260226_03_plot_GHG_total_diff.png, charts/20260226_03_plot_GHG_total_diff_EN.png

## 20260226-2 (update from 20260105-1, 20251218-1, 20251222)
* total FEC, power, CO2 intensity (incl. english version). fitting from 2014 to 2023
```
python scripts/20260226_04_plot_energy_total.py
```
a:-1.949e-01 b:1.237e+01 2030:9.06 2035:8.08 2040:7.11

```
20260226_04_plot_energy_total_EN.py
20260226_05_plot_energy_elec_total.py
20260226_05_plot_energy_elec_total_EJ.py
20260226_11_plot_intensity_energy_total.py
20260226_11_plot_intensity_energy_total_EN.py
20260226_13_plot_intensity_elec_total.py
20260226_13_plot_intensity_elec_total_EN.py

```
charts/20260226_04_plot_energy_total.png etc.

* 部門別エネルギー消費量 (一覧)
python scripts/20260226_20_plot_energy_subcat.py
python scripts/20260226_20_plot_energy_subcat_EN.py
* 部門別電力量 (一覧)
python scripts/20260226_21_plot_energy_elec_subcat.py
python scripts/20260226_21_plot_energy_elec_subcat_TWh.py # TWhで表示
* 部門別CO2排出量 (一覧)
python scripts/20260226_22_plot_co2_subcat_energy.py # エネルギー起源CO2
id:#500000 a:-2.626e+01 b:1.109e+03 2030:662.51 2035:531.20 2040:399.89
id:#600100 a:-1.118e+01 b:4.558e+02 2030:265.80 2035:209.91 2040:154.02
id:#611000 a:9.057e-02 b:1.777e+01 2030:19.31 2035:19.76 2040:20.21
id:#615000 a:-3.431e-02 b:7.506e+00 2030:6.92 2035:6.75 2040:6.58
id:#620000 a:-1.119e+01 b:4.290e+02 2030:238.69 2035:182.71 2040:126.74
id:#622000 a:-2.711e-01 b:9.808e+00 2030:5.20 2035:3.84 2040:2.49
id:#624000 a:-7.758e-01 b:2.535e+01 2030:12.16 2035:8.28 2040:4.40
id:#626000 a:-1.317e+00 b:6.632e+01 2030:43.92 2035:37.33 2040:30.75
id:#628000 a:-9.403e-01 b:3.443e+01 2030:18.45 2035:13.75 2040:9.05
id:#629100 a:-5.141e+00 b:1.831e+02 2030:95.73 2035:70.03 2040:44.32
id:#629900 a:-1.413e+00 b:5.711e+01 2030:33.09 2035:26.02 2040:18.96
id:#650000 a:-6.199e+00 b:2.304e+02 2030:125.02 2035:94.02 2040:63.03
id:#700000 a:-5.001e+00 b:1.969e+02 2030:111.87 2035:86.86 2040:61.86
id:#800000 a:-3.883e+00 b:2.258e+02 2030:159.82 2035:140.41 2040:120.99
id:#810000 a:-2.842e+00 b:1.353e+02 2030:86.98 2035:72.77 2040:58.56
id:#850000 a:-1.042e+00 b:9.055e+01 2030:72.84 2035:67.63 2040:62.43

python scripts/20260226_23_plot_co2_subcat_elec.py.  # 電力 CO2
id:#500000 a:-1.386e+01 b:4.970e+02 2030:261.33 2035:192.02 2040:122.70
id:#600100 a:-5.503e+00 b:1.833e+02 2030:89.73 2035:62.21 2040:34.70
id:#611000 a:1.968e-02 b:1.582e+00 2030:1.92 2035:2.02 2040:2.11
id:#615000 a:-7.863e-02 b:3.268e+00 2030:1.93 2035:1.54 2040:1.15
id:#620000 a:-5.419e+00 b:1.778e+02 2030:85.70 2035:58.61 2040:31.52
id:#622000 a:-1.514e-01 b:5.070e+00 2030:2.50 2035:1.74 2040:0.98
id:#624000 a:-4.220e-01 b:1.420e+01 2030:7.03 2035:4.92 2040:2.80
id:#626000 a:-6.366e-01 b:2.542e+01 2030:14.59 2035:11.41 2040:8.23
id:#628000 a:-3.770e-01 b:1.066e+01 2030:4.25 2035:2.37 2040:0.48
id:#629100 a:-1.434e+00 b:3.890e+01 2030:14.52 2035:7.35 2040:0.18
id:#629900 a:-1.311e+00 b:4.791e+01 2030:25.62 2035:19.07 2040:12.51
id:#650000 a:-4.233e+00 b:1.672e+02 2030:95.28 2035:74.12 2040:52.95
id:#700000 a:-3.865e+00 b:1.373e+02 2030:71.59 2035:52.27 2040:32.94
id:#800000 a:-2.622e-01 b:9.188e+00 2030:4.73 2035:3.42 2040:2.11
id:#810000 a:-2.449e-01 b:8.760e+00 2030:4.60 2035:3.37 2040:2.15
id:#850000 a:-1.736e-02 b:4.283e-01 2030:0.13 2035:0.05 2040:-0.04
(.venv) (base) ~/Documents/work/github/NZPR[1056]

* 部門別排出係数　(一覧)
python scripts/20260226_24_plot_intensity_subcat_energy.py
python scripts/20260226_25_plot_intensity_subcat_elec.py

## 20260311
* update energy_stat_intensity
```
python scripts/20260311_01_calc_intensity_energy_stat.py
```
outputs/20251218_01_intensity/20260311_01_energy_stat_intensity_data_common_0_電力.json
outputs/20251218_01_intensity/20260311_01_energy_stat_intensity_data_common_2_合計.json
outputs/20251218_01_intensity/20260311_01_energy_stat_intensity_data_common_3_エネルギー利用.json
outputs/20251218_01_intensity/20260311_01_energy_stat_intensity_data_common_4_非エネルギー利用.json
outputs/20251218_01_intensity/20260311_01_energy_stat_intensity_data_common.xlsx

* update SEP numbers
```
python scripts/20260311_02_import_SEP_numbers.py
```
outputs/20251218_02_SEP/20260311_02_SEP_numbers.json, 20260311_02_SEP_numbers.xlsx

* update plots
```
python scripts/20260226_04_plot_energy_total.py
python scripts/20260226_04_plot_energy_total_EN.py
python scripts/20260226_11_plot_intensity_energy_total.py
python scripts/20260226_11_plot_intensity_energy_total_EN.py
python scripts/20260226_20_plot_energy_subcat.py
python scripts/20260226_24_plot_intensity_subcat_energy.py
python scripts/20260205_10_plot_energy_FEC_sectors.py
python scripts/20260205_10_plot_energy_FEC_sectors_EN.py
python scripts/20260205_11_plot_co2_energy_sectors.py
python scripts/20260205_11_plot_co2_energy_sectors_EN.py
python scripts/20260205_13_plot_intensity_energy_sectors.py
python scripts/20260205_13_plot_intensity_energy_sectors_EN.py
```

## 20260313 EV
```
python scripts/20260313_01_plot_ev_sales_share.py
python scripts/20260313_02_plot_bars_vehicles_sales.py
```
charts/20260313_01_plot_ev_sales_share.png
charts/20260313_02_plot_bars_vehicle_sales.png

## 20260316-17 エネルギー起源CO2のエネルギー転換部門からの排出を他部門に割り当てる
```
python scripts/20260316_01_redistribute_co2.py
```
outputs/20251201_21_energy_stat/20260316_32_energy_stat_co2_data_common_12_総合計_エネルギー利用分_RD.json, ​​20260316_32_energy_stat_co2_data_common_12_総合計_エネルギー利用分_RD.xlsx
outputs/20251218_01_intensity/20260316_32_energy_stat_intensity_data_common_3_エネルギー利用_RD.json, 20260316_32_energy_stat_intensity_data_common_3_エネルギー利用_RD.xlsx

エネルギー転換部門 事業用発電からの排出の再配分
```
python scripts/20260316_02_redistribute_co2_elec.py
```
outputs/20251201_21_energy_stat/20260316_32_energy_stat_co2_data_common_0_電力_RD.json, 20260316_32_energy_stat_co2_data_common_0_電力_RD.xlsx
utputs/20251218_01_intensity/20260316_32_energy_stat_intensity_data_common_0_電力_RD.json, 20260316_32_energy_stat_intensity_data_common_0_電力_RD.xlsx

```
20260226_11_plot_intensity_energy_total.py
20260226_11_plot_intensity_energy_total_EN.py
20260226_13_plot_intensity_energy_total.py
20260226_13_plot_intensity_energy_total_EN.py
```
charts/
20260226_11_plot_intensity_total_energy.png
20260226_11_plot_intensity_total_energy_EN.png
20260226_13_plot_intensity_elec_total.png
20260226_13_plot_intensity_elec_total_EN.png

```
scripts/20260226_22_plot_co2_subcat_energy.py 
```
charts/20260226_22_plot_co2_subcat_energy.png
id:#500000 a:-2.841e+01 b:1.210e+03 2030:726.64 2035:584.61 2040:442.58
id:#600100 a:-1.237e+01 b:5.057e+02 2030:295.39 2035:233.53 2040:171.67
id:#611000 a:9.658e-02 b:1.802e+01 2030:19.66 2035:20.14 2040:20.62
id:#615000 a:-4.323e-02 b:8.021e+00 2030:7.29 2035:7.07 2040:6.85
id:#620000 a:-1.238e+01 b:4.780e+02 2030:267.52 2035:205.62 2040:143.72
id:#622000 a:-3.300e-01 b:1.168e+01 2030:6.07 2035:4.42 2040:2.77
id:#624000 a:-9.957e-01 b:3.281e+01 2030:15.88 2035:10.90 2040:5.92
id:#626000 a:-1.617e+00 b:7.836e+01 2030:50.87 2035:42.78 2040:34.70
id:#628000 a:-9.988e-01 b:3.644e+01 2030:19.46 2035:14.47 2040:9.47
id:#629100 a:-5.367e+00 b:1.914e+02 2030:100.19 2035:73.36 2040:46.53
id:#629900 a:-1.571e+00 b:6.561e+01 2030:38.90 2035:31.04 2040:23.18
id:#650000 a:-6.683e+00 b:2.577e+02 2030:144.12 2035:110.71 2040:77.29
id:#700000 a:-5.439e+00 b:2.188e+02 2030:126.37 2035:99.18 2040:71.99
id:#800000 a:-3.913e+00 b:2.273e+02 2030:160.76 2035:141.20 2040:121.64
id:#810000 a:-2.869e+00 b:1.367e+02 2030:87.89 2035:73.55 2040:59.20
id:#850000 a:-1.044e+00 b:9.062e+01 2030:72.87 2035:67.65 2040:62.43

```
scripts/20260226_23_plot_co2_subcat_elec.py 
```
charts/20260226_23_plot_co2_subcat_elec.png
id:#500000 a:-1.457e+01 b:5.418e+02 2030:294.16 2035:221.32 2040:148.48
id:#600100 a:-5.811e+00 b:1.999e+02 2030:101.09 2035:72.03 2040:42.98
id:#611000 a:2.417e-02 b:1.722e+00 2030:2.13 2035:2.25 2040:2.37
id:#615000 a:-8.203e-02 b:3.557e+00 2030:2.16 2035:1.75 2040:1.34
id:#620000 a:-5.726e+00 b:1.939e+02 2030:96.59 2035:67.96 2040:39.33
id:#622000 a:-1.633e-01 b:5.495e+00 2030:2.72 2035:1.90 2040:1.09
id:#624000 a:-4.626e-01 b:1.571e+01 2030:7.84 2035:5.53 2040:3.22
id:#626000 a:-6.794e-01 b:2.787e+01 2030:16.32 2035:12.92 2040:9.52
id:#628000 a:-3.985e-01 b:1.152e+01 2030:4.74 2035:2.75 2040:0.76
id:#629100 a:-1.508e+00 b:4.227e+01 2030:16.63 2035:9.09 2040:1.56
id:#629900 a:-1.372e+00 b:5.219e+01 2030:28.87 2035:22.01 2040:15.15
id:#650000 a:-4.429e+00 b:1.822e+02 2030:106.90 2035:84.75 2040:62.61
id:#700000 a:-4.052e+00 b:1.497e+02 2030:80.84 2035:60.58 2040:40.32
id:#800000 a:-2.752e-01 b:1.001e+01 2030:5.33 2035:3.95 2040:2.58
id:#810000 a:-2.567e-01 b:9.541e+00 2030:5.18 2035:3.89 2040:2.61
id:#850000 a:-1.849e-02 b:4.665e-01 2030:0.15 2035:0.06 2040:-0.03

```
scripts/20260226_24_plot_intensity_subcat_energy.py
```
id:#500000 a:-9.060e-07 b:9.809e-05 2030:8.268e-05 2035:7.815e-05 2040:7.362e-05
id:#600100 a:-1.056e-06 b:1.031e-04 2030:8.510e-05 2035:7.982e-05 2040:7.454e-05
id:#611000 a:-8.730e-08 b:7.439e-05 2030:7.290e-05 2035:7.247e-05 2040:7.203e-05
id:#615000 a:-1.024e-06 b:9.400e-05 2030:7.659e-05 2035:7.147e-05 2040:6.634e-05
id:#620000 a:-1.075e-06 b:1.048e-04 2030:8.656e-05 2035:8.118e-05 2040:7.581e-05
id:#622000 a:-1.018e-06 b:1.206e-04 2030:1.033e-04 2035:9.819e-05 2040:9.310e-05
id:#624000 a:-1.299e-06 b:9.214e-05 2030:7.005e-05 2035:6.355e-05 2040:5.706e-05
id:#626000 a:-4.665e-07 b:8.638e-05 2030:7.845e-05 2035:7.612e-05 2040:7.379e-05
id:#628000 a:-1.112e-06 b:9.459e-05 2030:7.569e-05 2035:7.013e-05 2040:6.457e-05
id:#629100 a:-6.861e-07 b:1.061e-04 2030:9.445e-05 2035:9.102e-05 2040:8.759e-05
id:#629900 a:-2.503e-06 b:1.355e-04 2030:9.291e-05 2035:8.040e-05 2040:6.788e-05
id:#650000 a:-1.296e-06 b:1.165e-04 2030:9.447e-05 2035:8.799e-05 2040:8.151e-05
id:#700000 a:-1.487e-06 b:1.102e-04 2030:8.496e-05 2035:7.752e-05 2040:7.008e-05
id:#800000 a:-6.499e-08 b:7.034e-05 2030:6.924e-05 2035:6.891e-05 2040:6.859e-05
id:#810000 a:-9.225e-08 b:7.116e-05 2030:6.960e-05 2035:6.913e-05 2040:6.867e-05
id:#850000 a:-1.686e-08 b:6.914e-05 2030:6.885e-05 2035:6.877e-05 2040:6.868e-05

```
scripts/20260226_25_plot_intensity_subcat_elec.py
```
id:#600100 a:-2.989e-06 b:1.534e-04 2030:1.025e-04 2035:8.759e-05 2040:7.265e-05
id:#611000 a:-3.002e-06 b:1.542e-04 2030:1.031e-04 2035:8.812e-05 2040:7.311e-05
id:#615000 a:-2.925e-06 b:1.560e-04 2030:1.062e-04 2035:9.160e-05 2040:7.698e-05
id:#620000 a:-2.990e-06 b:1.533e-04 2030:1.025e-04 2035:8.750e-05 2040:7.255e-05
id:#622000 a:-1.570e-06 b:1.637e-04 2030:1.370e-04 2035:1.292e-04 2040:1.213e-04
id:#624000 a:-1.437e-06 b:1.326e-04 2030:1.082e-04 2035:1.010e-04 2040:9.380e-05
id:#626000 a:-2.202e-06 b:1.444e-04 2030:1.070e-04 2035:9.598e-05 2040:8.496e-05
id:#628000 a:-3.407e-06 b:1.715e-04 2030:1.136e-04 2035:9.656e-05 2040:7.952e-05
id:#629100 a:-3.804e-06 b:1.601e-04 2030:9.544e-05 2035:7.642e-05 2040:5.740e-05
id:#629900 a:-3.193e-06 b:1.552e-04 2030:1.009e-04 2035:8.493e-05 2040:6.896e-05
id:#650000 a:-3.026e-06 b:1.550e-04 2030:1.035e-04 2035:8.839e-05 2040:7.326e-05
id:#700000 a:-3.099e-06 b:1.529e-04 2030:1.002e-04 2035:8.469e-05 2040:6.919e-05
id:#800000 a:-3.155e-06 b:1.553e-04 2030:1.017e-04 2035:8.591e-05 2040:7.013e-05
id:#810000 a:-3.155e-06 b:1.553e-04 2030:1.017e-04 2035:8.591e-05 2040:7.013e-05
id:#850000 a:-3.155e-06 b:1.553e-04 2030:1.017e-04 2035:8.591e-05 2040:7.013e-05

charts/20260226_24_plot_intensity_subcat_energy.png
charts/20260226_25_plot_intensity_subcat_elec.png

```
scripts/20260205_11_plot_co2_energy_sectors.py
scripts/20260205_11_plot_co2_energy_sectors_EN.py
```
charts/20260205_11_plot_co2_energy_00_産業.png, etc.
a:-1.237e+01 b:5.057e+02 2030:295.39 2035:233.53 2040:171.67 産業
a:-1.238e+01 b:4.780e+02 2030:267.52 2035:205.62 2040:143.72 製造
a:-5.367e+00 b:1.914e+02 2030:100.19 2035:73.36 2040:46.53 鉄鋼
a:-6.683e+00 b:2.577e+02 2030:144.12 2035:110.71 2040:77.29 業務他
a:-5.439e+00 b:2.188e+02 2030:126.37 2035:99.18 2040:71.99 家庭
a:-3.913e+00 b:2.273e+02 2030:160.76 2035:141.20 2040:121.64 運輸

```
scripts/20260205_13_plot_intensity_energy_sectors.py
scripts/20260205_13_plot_intensity_energy_sectors_EN.py
```
a:-1.056e-06 b:1.031e-04 2030:8.510e-05 2035:7.982e-05 2040:7.454e-05 産業
a:-1.075e-06 b:1.048e-04 2030:8.656e-05 2035:8.118e-05 2040:7.581e-05 製造
a:-6.861e-07 b:1.061e-04 2030:9.445e-05 2035:9.102e-05 2040:8.759e-05 鉄鋼
a:-1.296e-06 b:1.165e-04 2030:9.447e-05 2035:8.799e-05 2040:8.151e-05 業務他
a:-1.487e-06 b:1.102e-04 2030:8.496e-05 2035:7.752e-05 2040:7.008e-05 家庭
a:-6.499e-08 b:7.034e-05 2030:6.924e-05 2035:6.891e-05 2040:6.859e-05 運輸

## 20260318 部門ごとの進捗まとめ

実績の外挿の2013年からの減少幅を計算し、stepsの減少幅やbalanceの減少幅との差を2030, 2040断面で見る

```
scripts/20260318_10_NZPR_sector_summary_calc_FEC.py
scripts/20260318_11_NZPR_sector_summary_calc_co2.py
scripts/20260318_12_NZPR_sector_summary_calc_intensity.py
```
charts/
20260318_10_NZPR_sector_summary_calc_FEC_2030.png, 20260318_10_NZPR_sector_summary_calc_FEC_2040.png
20260318_11_NZPR_sector_summary_calc_co2_2030.png, 20260318_11_NZPR_sector_summary_calc_co2_2040.png
20260318_12_NZPR_sector_summary_calc_intensity_2030.png, 20260318_12_NZPR_sector_summary_calc_intensity_2040.png

## 20260325

* 電力がエネルギー利用FECに占める割合
* 総合エネルギー統計
```
python scripts/20260325_01_plot_energy_stat_FEC_elec_fraction.py
```
* 1.5CRM 2040年
```
python scripts/20260325_02_plot_1p5CRM_FEC_elec_fraction.py
```
charts/20260325_01_plot_energy_stat_FEC_elec_fraction.png
charts/20260325_02_plot_1p5CRM_FEC_elec_fraction2040.png


## 20260331 電力脱炭素化関係プロット

* PV導入容量, 2014-2023/2024実績の直線フィットを延長
```
python scripts/20260331_01_fit_PVaddition.py
```
エネルギー白書:
a=-0.5723732700302341 b=1161.2734400681265
IRENA:
a=-0.6617114090909526 b=1342.9046076819059

年, エネルギー白書, IRENA
2030 85.266  97.679 
2035 85.266  97.679 
2040 85.266  97.679 
(増加量が0なので増えない)

2019-2023の導入量の平均: エネルギー白書: 4.73 GW/yr, IRENA: 5.28 GW/yr
この増加量を維持した場合
年, エネルギー白書, IRENA
2030 110.1823697 121.2925326
2035 133.85553 147.7018656
2040 157.5286904 174.1111986
(see 20250820_02_再エネ導入量_work.xlsx)
IRENAの数字を利用

* 風力はIRENA(エネルギー白書では陸上/洋上の区別なし)
=> inputs/RE/20260331_05_RE_cap_for_plot.xlsx
```
python scripts/20260331_01_plot_RE_bars_capacity.py 
```
charts/20260331_01_plot_RE_bars_capacity.png


* 電力量, IRENAのデータを利用。2014-2023の実績の直線フィットの延長と、2019-2023の平均の継続
```
python scripts/20260331_02_fit_REpower_addition.py 
```
# Year,PV(extrapolation),PV(average),OnSW(extrapolation),OnSW(average)
2023  60405.91  96459.48    7276.01  10386.99 
2024  68566.79 103217.84    7864.13  10989.14 
2025  76727.68 109976.20    8452.26  11591.29 
2026  84888.57 116734.56    9040.39  12193.45 
2027  93049.46 123492.93    9628.51  12795.60 
2028 101210.34 130251.29   10216.64  13397.75 
2029 109371.23 137009.65   10804.77  13999.90 
2030 117532.12 143768.01   11392.90  14602.05 
2031 125693.01 150526.37   11981.02  15204.21 
2032 133853.89 157284.73   12569.15  15806.36 
2033 142014.78 164043.10   13157.28  16408.51 
2034 150175.67 170801.46   13745.40  17010.66 
2035 158336.56 177559.82   14333.53  17612.82 
2036 166497.45 184318.18   14921.66  18214.97 
2037 174658.33 191076.54   15509.78  18817.12 
2038 182819.22 197834.90   16097.91  19419.27 
2039 190980.11 204593.26   16686.04  20021.42 
2040 199141.00 211351.63   17274.17  20623.58 
=> inputs/RE/20260331_05_RE_power_for_plot.xlsx

```
python scripts/20260331_02_plot_RE_bars_power.py 
```
charts/20260331_02_plot_RE_bars_power.png

* 太陽光、陸上風力、洋上風力 設備容量
```
python scripts/20260331_03_plot_RE_bars_capacity_separate.py 
```
charts/20260331_03_plot_RE_bars_capacity_separate.png

## 20260401

* RE power, 1.5CRM (steps, balance, balance-sub) and energy stat
```
python scripts/20260401_01_plot_RE_power.py
```
charts/20260401_01_plot_IGESRM_RE_power.png

## 20260408
* OCCTO電力需要見通し
```
python scripts/20260408_01_import_OCCTO_power_demand.py 
```
outputs/20251231_01_OCCTO/20260408_01_OCCTO_power_demand.json

* power demand, simplified
```
python scripts/20260408_01_plot_bars_power_demand.py
```
charts/20260408_01_plot_bars_power_demand.png

## 20260430

* 2040年の太陽光・風力発電量(エネ基、1.5CRMバランス・バランスサブ)
```
python scripts/20260430_01_plot_bars_power_PV_Wind_2040.py
```
charts/20260430_01_plot_bars_power_PV_Wind_2040.png

## 20260507
```
pandoc doc/report2026/20260224_01_NZPR_report.md --reference-doc=doc/template/20260224_my-reference.docx -o test/20260507_03_NZPR_report.docx
```

## 20260508
* update SEP numbers (CO2emissions are energy-related)
```
python scripts/20260508_03_import_SEP_numbers.py
```
outputs/20251218_02_SEP/20260508_03_SEP_numbers.json, 20260508_03_SEP_numbers.xlsx

## 20260520
* Vashold 2023のGHG emissions projectionとの比較
python scripts/20260520_01_plot_GHG_total_w_vashold2023.py 
* 同じく、intensity (GHG emissions per GDP)のprojectionとの比較
python scripts/20260520_02_plot_GHG_intensity_w_vashold2023.py 
charts/20260520_01_plot_GHG_total_w_vashold2023.png
charts/20260520_02_plot_GHG_intensity_w_vashold2023.png


## 20260522
```
pandoc doc/report2026/20260224_01_NZPR_report.md --reference-doc=doc/template/20260224_my-reference.docx -o test/20260521_04_NZPR_report.docx
```

## 20260608

https://zenn.dev/sky_y/articles/pandoc-advent-2020-bib2
https://www.zotero.org/styles?q=id%3Asist02
mv ~/Downloads/sist02.csl doc/csl/
mv ~/Downloads/experimental-astronomy.csl doc/csl/

pandoc doc/report2026/20260224_01_NZPR_report.md --reference-doc=doc/template/20260608_my-reference.docx --citeproc --bibliography=doc/report2026/NZPR.bib --csl=doc/csl/experimental-astronomy.csl -o test/20260608_09_NZPR_report.docx

## 20260610
python scripts/20260610_03_plot_FEC_elec_fraction.py 
charts/20260610_03_plot_FEC_elec_fraction.png

## 20260615
pandoc doc/report2026/20260224_01_NZPR_report.md --reference-doc=doc/template/20260608_my-reference.docx --citeproc --bibliography=doc/report2026/NZPR.bib --csl=doc/csl/experimental-astronomy.csl -o test/20260615_10_NZPR_report.docx

## 20260617
* capacity and power for RE, updated. see also 1p5CRM/NZPR/20260617work_REstat/ and google doc: 20251120NZPR
python scripts/20260617_04_plot_RE_bars_capacity_separate.py

## 20260618

* 「現状の延長」での再エネ設備容量、再考 (see 20260331 as well)
2019-2023, 2020-2024の5年の平均を計算
scripts/20260618_01_average_RE_cap_additions.py

2019-2023 average: 6.181 0.350 0.024 
2020-2024 average: 5.282 0.338 0.044 

IRENAの統計は、発電量は2023年までしかない。
設備容量と発電量で平均の期間が異なることになるが、
2020-2024で計算する。

year, pv, onsw, offsw
2030: 121.29   7.60   0.55
2035: 147.70   9.29   0.77
2040: 174.11  10.97   0.99

太陽光の設備容量増加は顕著に減少しているため、2024年の増加分実績が継続した場合も入れる。
2024 additions: 2.533
2030: 104.80 
2035: 117.47 
2040: 130.13 

python scripts/20260617_04_plot_RE_bars_capacity_separate.py 
charts/20260617_04_plot_RE_bars_capacity_separate.png

* 発電量の増加量、平均値
python scripts/20260619_01_average_RE_power_additions.py

2019-2023 average: 6.758 0.602 0.000 

2030: 143.77  14.60   0.10
2035: 177.56  17.61   0.10
2040: 211.35  20.62   0.10

PVは2023年の増加量でも計算
2023 additions: 3.856
2030: 123.45 
2035: 142.73 
2040: 162.01 

=> 20260619_06_RE_power_for_plot.xlsx
python scripts/20260618_05_plot_RE_bars_power_separate.py
charts/20260618_05_plot_RE_bars_power_separate.png


* 設備容量差分 (PV, OnSW)
python scripts/20260619_01_plot_RE_bars_capacity_additions_separate.py
charts/20260619_01_plot_RE_bars_capacity_additions_separate.png

* 発電量差分 (PV, OnSW)
python scripts/20260619_02_plot_RE_bars_power_additions_separate.py
charts/20260619_02_plot_RE_bars_power_additions_separate.png

## 20260619
* RE cumlative barsの更新
scripts/20260619_04_plot_RE_bars_capacity.py 
charts/20260619_04_plot_RE_bars_capacity.png

scripts/20260619_05_plot_RE_bars_power.py 
charts/20260619_05_plot_RE_bars_power.png

pandoc doc/report2026/20260224_01_NZPR_report.md --reference-doc=doc/template/20260608_my-reference.docx --citeproc --bibliography=doc/report2026/NZPR.bib --csl=doc/csl/experimental-astronomy.csl -o test/20260619_11_NZPR_report.docx

pandoc doc/report2026/20260224_01_NZPR_report.md --reference-doc=doc/template/20260608_my-reference.docx --citeproc --bibliography=doc/report2026/NZPR.bib --csl=doc/csl/sist02.csl -o test/20260619_12_NZPR_report.docx
