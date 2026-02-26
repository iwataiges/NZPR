

## 20260224

* at github.com/repos/ create a new repository "NZPR"

```
cd ~/Documents/work/github
git clone git@github.com:iwataiges/NZPR.git
```

* working on doc/template/20260224_my-reference.docx
* to generate docx from markdown:
```
pandoc doc/report2026/20260224_01_NZPR_report.md --reference-doc=doc/template/20260224_my-reference.docx -o test/20260224_01_NZPR_report.docx 
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


----

(** previous repository (GHGpath) **)

## 20250506-1
### input from GHG intentory excel file to generate GHG data frame
```
python scripts/20250506_05_import_GHG_data.py
```
 => outputs/20250506_05_ghg_data.json, outputs/20250506_05_ghg_data.xlsx

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


## 20260116-1

* 7次エネ基の「技術進展」=「排出上振れ」シナリオの場合の2040年のGHG排出量推計
   * 需給見通しによると、エネルギー起源CO2排出量は、4シナリオで3.65-3.67億tCO2に対し、技術進展シナリオは5.39億tCO2 → +174MtCO2
   * 他のガスは変化ないとすると、GHGは2040年に 380 + 174 = 554 MtCO2。2013年1407MtCO2に対し60.6%削減

```
python scripts/scripts/20260116_02_plot_GHG_total_IPCC.py
python scripts/scripts/20260116_06_plot_GHG_total_1p5CRM.py
```
charts/20260116_02_plot_GHG_total_IPCC.png, 20260116_06_plot_GHG_total_1p5CRM.png

## 20260120-1

* 日本語版作成
```
python scripts/20251208_03_plot_GHGI_diff.py
python scripts/20251208_03_plot_GHGI_diff_EN.py
```
charts/charts/20251208_03_plot_GHG_total_diff.png, charts/20251208_03_plot_GHG_total_diff_EN.png

## 20260122
* GHG pathフィッティングを2014-2023 (2020除く)に
```
python scripts/20260122_06_plot_GHG_total.py
```
charts/20260122_06_plot_GHG_total.png, 20260122_06_plot_GHG_total_wo_failure2040.png (2040上振れの点なし)
