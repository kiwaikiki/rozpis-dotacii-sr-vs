#!/usr/bin/env python

get_ipython().run_line_magic("pip", "install pandas")
get_ipython().run_line_magic("pip", "install openpyxl")
get_ipython().run_line_magic("pip", "install scipy")
import pandas as pd
import numpy as np
data_source = "local"
prilohy_path = (
    {
        "A": "../data/prilohaA-napocet.xlsx",
        "B": "../data/prilohaB-crepc.xlsx",
        "C": "../data/prilohaC-monografie.xlsx",
        "D": "../data/prilohaD-granty.xlsx",
        "publ": "../data/publikacna_cinnost.xlsx",
    }
    if data_source == "local"
    else {
        "A": "https://www.minedu.sk/data/att/25844.xlsx",
        "B": "https://www.minedu.sk/data/att/25563.xlsx",
        "C": "https://www.minedu.sk/data/att/25537.xlsx",
        "D": "https://www.minedu.sk/data/att/25538.xlsx",
        "publ": "https://www.minedu.sk/data/att/24957.xlsx",
    }
)
prilohaA = pd.read_excel(prilohy_path["A"], sheet_name=None, header=None)
print(prilohaA.keys())
prilohaB = pd.read_excel(prilohy_path["B"], sheet_name=None)
print(prilohaB.keys())
prilohaC = pd.read_excel(prilohy_path["C"], sheet_name=None)
print(prilohaC.keys())
prilohaD = pd.read_excel(prilohy_path["D"], sheet_name=None)
print(prilohaD.keys())
prilohaPUBL = pd.read_excel(prilohy_path["publ"], sheet_name=None, header=None)
print(prilohaPUBL.keys())

oblasti_mapping_sheet = prilohaA["E3_oblasti"].copy()
dictionary1 = oblasti_mapping_sheet.set_index(0)[2].to_dict()
dictionary2 = oblasti_mapping_sheet.set_index(1)[2].to_dict()
dictionary3 = {
    key: value
    for key, value in zip(
        [
            "PRÍRODNÉ VEDY",
            "TECHNICKÉ VEDY",
            "LEKÁRSKE VEDY",
            "PÔDOHOSPODÁRSKE VEDY",
            "SPOLOČENSKÉ VEDY",
            "HUMANITNÉ VEDY",
        ],
        [f"M{i}" for i in range(1, 7)],
    )
}
oblasti_mapping = {**dictionary1, **dictionary2, **dictionary3}
oblasti_mapping

vs_skratky = pd.read_csv("../data/vs_skratky.csv", index_col=0)
vs_skratky2cely_nazov = (
    vs_skratky.reset_index()
    .drop(columns=["cislo"])
    .set_index("skratka_mesto")["VS_NAZOV"]
    .to_dict()
)
vs_skratky2cely_nazov

casovy_ramec = [2020, 2021]

epc_codes_ADx = ["ADC", "ADD", "ADM", "ADN"]
epc_codes_AAx = ["AAA", "AAB"]
epc_codes_Zxx = ["ZZZ", "ZZY", "ZYZ", "ZYY"]
epc_codes_M1_M4 = epc_codes_ADx
epc_codes_M5 = epc_codes_ADx + epc_codes_AAx
epc_codes_M6a = epc_codes_ADx + epc_codes_AAx
epc_codes_M6b = epc_codes_Zxx
publikacie_ADx = prilohaB["2021 - 3"].copy()
assert publikacie_ADx["EPC_KOD"].isin(epc_codes_ADx).all()
publikacie_AAx_2020 = prilohaC["vystupy 2020"].copy()
assert publikacie_AAx_2020["EPC_KOD"].isin(epc_codes_AAx).all()
publikacie_AAx_2021 = prilohaC["vystupy 2021"].copy()
assert publikacie_AAx_2021["EPC_KOD"].isin(epc_codes_AAx).all()
publikacie_AAx = pd.concat([publikacie_AAx_2020, publikacie_AAx_2021])
publikacie_vsetky = prilohaPUBL["data"].copy()
publikacie_vsetky.columns = publikacie_vsetky.iloc[2]
publikacie_vsetky = publikacie_vsetky.iloc[3:].reset_index()
publikacie_vsetky = publikacie_vsetky[publikacie_vsetky["ROK"].isin(casovy_ramec)]
publikacie_ADx_v2 = publikacie_vsetky[publikacie_vsetky["EPC_KOD"].isin(epc_codes_ADx)]
publikacie_AAx_v2 = publikacie_vsetky[publikacie_vsetky["EPC_KOD"].isin(epc_codes_AAx)]
vysledne_pocty_fakult_v_oblastiach = {
    "M1": 24,
    "M2": 40,
    "M3": 11,
    "M4": 10,
    "M5": 70,
    "M6": 47,
}

def melt_sheet(sheet, relevant_columns, melt_columns, output_column):
    return (
        sheet.loc[:, relevant_columns + melt_columns]
        .melt(id_vars=relevant_columns, value_name=output_column)
        .drop(columns=["variable"])
        .dropna(subset=[output_column])
    )
    
stlpce = ["VS_NAZOV", "FAKULTA_NAZOV", "PODIEL", "JCR_bonus", "ID v CREPC"]
melt_stlpce = [f"OBLAST_VYSKUMU_KOD{i}" for i in ["", 2, 3, 4, 5]]
publikacie_ADx_melted = melt_sheet(publikacie_ADx, stlpce, melt_stlpce, "oblast_kod")
publikacie_ADx_melted["oblast"] = publikacie_ADx_melted["oblast_kod"].map(
    oblasti_mapping
)
publikacie_ADx_melted["PODIEL"] = publikacie_ADx_melted["PODIEL"] / 100
publikacie_ADx_melted.rename(columns={"ID v CREPC": "ID_V_CREPC"}, inplace=True)
display(publikacie_ADx_melted.query("ID_V_CREPC == 133480"))
sum_podielov = publikacie_ADx_melted.groupby("ID_V_CREPC").sum()["PODIEL"].to_dict()
display(publikacie_ADx_melted.query("ID_V_CREPC == 133480"))
publikacie_ADx_melted

index_columns = ["VS_NAZOV", "FAKULTA_NAZOV"]

def sumup_groupby(sheet, groupby_columns, data_column, output_column):
    return (
        sheet.groupby(groupby_columns, dropna=False)[data_column]
        .sum()
        .rename(output_column)
    )
    
def krat2zaokruhli(sheet, column):
    zaokruhlene = column + "_zaokruhlene"
    sheet[zaokruhlene] = (sheet[column] * 2).apply(np.ceil)
    return sheet
    
publikacie_ADx_melted["vahaxJCR"] = (
    publikacie_ADx_melted["PODIEL"] * publikacie_ADx_melted["JCR_bonus"]
)
publikacie_ADx_melted = krat2zaokruhli(publikacie_ADx_melted, "vahaxJCR")
publikacie_ADx_sum = sumup_groupby(
    publikacie_ADx_melted, ["oblast"] + index_columns, "vahaxJCR_zaokruhlene", "sum_ADx"
)
publikacie_ADx_sum.sort_values(ascending=False)

stlpce = ["VS_NAZOV", "FAKULTA_NAZOV", "kategoria_metodika"]
melt_stlpce = [f"OBLAST_VYSKUMU_KOD{i}" for i in ["", 2]]
publikacie_AAx_melted = melt_sheet(publikacie_AAx, stlpce, melt_stlpce, "oblast_kod")
publikacie_AAx_melted["oblast"] = publikacie_AAx_melted["oblast_kod"].map(
    oblasti_mapping
)

publikacie_AAx_melted = krat2zaokruhli(publikacie_AAx_melted, "kategoria_metodika")
publikacie_AAx_sum = sumup_groupby(
    publikacie_AAx_melted,
    ["oblast"] + index_columns,
    "kategoria_metodika_zaokruhlene",
    "sum_AAx",
)
publikacie_AAx_sum.sort_values(ascending=False)

granty_orig = prilohaD["T3 - výsk. zahr. grant. schémy"].copy()

vyhra_key = """Výška finančných prostriedkov v kategórii BV prijatých vysokou školou na jej účet v období od 1.1. do 31.12.2021
(uviesť v eurách v celých jednotkách)"""
granty_orig.rename(
    columns={
        vyhra_key: "Výhra",
        "Vysoká škola": "VS_NAZOV",
        "Názov fakulty": "FAKULTA_NAZOV",
        "Identifikačné číslo projektu podľa zmluvy": "ID",
    },
    inplace=True,
)
relevant_columns = index_columns + [
    "SKUPINA ODBOROV VEDY A TECHNIKY",
    "Rok",
    "ID",
    "Výhra",
]
granty_orig = granty_orig.loc[:, relevant_columns].dropna(subset=["Výhra"])
granty_orig["FAKULTA_NAZOV"] = granty_orig["FAKULTA_NAZOV"].fillna("<neuvedené>")
granty_orig["oblast"] = granty_orig["SKUPINA ODBOROV VEDY A TECHNIKY"].map(
    oblasti_mapping
)
granty_orig

granty_orig.loc[
    granty_orig["ID"] == "H2020 739566", "FAKULTA_NAZOV"
] = "FunGlass - Centrum pre funkčné a povrchovo funkcionalizované sklá"

pocty_zamestnancov = prilohaA["E2_zamestnanci_2021"].copy()
pocty_zamestnancov.columns = pocty_zamestnancov.iloc[0].combine_first(
    pocty_zamestnancov.iloc[1]
)
pocty_zamestnancov = pocty_zamestnancov[2:]
pocty_zamestnancov = (
    pocty_zamestnancov[pocty_zamestnancov["kod skoly"].notna()]
    .drop(columns=["kod skoly"])
    .rename(columns={"FAKULTA_NAZOV / sucasti": "FAKULTA_NAZOV"})
    .set_index(index_columns)
    .fillna(0)
    .astype(int)
    .groupby(oblasti_mapping, axis=1)
    .sum()
)
pocty_zamestnancov

from collections import defaultdict
import string
translate_table = str.maketrans("", "", string.punctuation)
tokenize = lambda s: set(s.translate(translate_table).lower().split())
stare_nazvy = list(set(granty_orig.set_index(["VS_NAZOV", "FAKULTA_NAZOV"]).index))
fakulty = defaultdict(lambda: [[], []])
for vs, fakulta in stare_nazvy:
    vs_nazov = vs_skratky2cely_nazov[vs]
    fakulty[vs_nazov][0].append((vs, fakulta))
    nove_nazvy = list(set(pocty_zamestnancov.index))
for vs, fakulta in nove_nazvy:
    fakulty[vs][1].append(fakulta)
    granty2publikacie_naming_mapping = {}
for vs_nove in fakulty:
    stare, nove = fakulty[vs_nove]
    if not nove:
        print("UNKNOWN VS", vs_nove, stare)
        nove = ["unknown"]
    for vs_stara, fakulta_stara in stare:
        matching_to = fakulta_stara.translate(translate_table).split()
        if len(matching_to[-1]) <= 4 and matching_to[-1].isupper():
            matching_to.pop()
        matching_to = " ".join(matching_to)
                podobnosti = []
        for fakulta_nova in nove:
            podobnosti.append(
                len(tokenize(matching_to) & tokenize(fakulta_nova.lower()))
            )
        best_i = podobnosti.index(max(podobnosti))
        fakulta_nova = nove[best_i]
        dlzka1 = len(tokenize(matching_to))
        dlzka2 = len(tokenize(nove[best_i]))
        if podobnosti[best_i] != dlzka2 and podobnosti[best_i] < dlzka1 * 0.75:
            print(
                fakulta_stara, best_i, dlzka1, dlzka2, podobnosti[best_i], fakulta_nova
            )
            fakulta_nova = f"unknown[{fakulta_stara}]"
        granty2publikacie_naming_mapping[(vs_stara, fakulta_stara)] = (
            vs_nove,
            fakulta_nova,
        )
        granty2publikacie_naming_mapping
        
granty = granty_orig.copy().set_index(["VS_NAZOV", "FAKULTA_NAZOV"])
granty.index = granty.index.map(granty2publikacie_naming_mapping)
granty = granty.reset_index()
granty_unknown = (
    granty[granty["FAKULTA_NAZOV"].str.startswith("unknown")]
    .groupby(["VS_NAZOV", "FAKULTA_NAZOV"])
    .sum("Výhra")
)
total_granty, total_granty_unknown = (
    granty["Výhra"].sum(),
    granty_unknown["Výhra"].sum(),
)
print(
    f"Total: {total_granty:.0f}€, Unknown: {total_granty_unknown:.0f}€, {total_granty_unknown / total_granty:.1%}"
)
display(granty_unknown.sort_values("Výhra", ascending=False))
granty = granty.set_index(["oblast", "VS_NAZOV", "FAKULTA_NAZOV"])
granty.sort_values("Výhra", ascending=False)

granty_sum = sumup_groupby(granty, ["oblast"] + index_columns, "Výhra", "sum_granty")
granty_sum.loc["M1"].sort_values(ascending=False)
granty_sum = granty_sum.reset_index()
granty_sum = granty_sum.set_index(["oblast", "VS_NAZOV", "FAKULTA_NAZOV"])["sum_granty"]
granty_sum

uni_adx = set(map(lambda x: x[1:], publikacie_ADx_sum.index))
uni_aax = set(map(lambda x: x[1:], publikacie_AAx_sum.index))
uni_granty = set(map(lambda x: x[1:], granty_sum.index))
print(list(map(len, [uni_adx, uni_aax, uni_granty])))
print(len(uni_adx & uni_aax))
print(len(uni_adx & uni_granty))
print(len(uni_aax & uni_granty))
print(len((uni_aax | uni_adx) & uni_granty))
display(uni_adx | uni_aax)
display(uni_granty - uni_adx - uni_aax)

pracoviska_excelentnost = pd.concat(
    [
        publikacie_ADx_sum,
        publikacie_AAx_sum,
        granty_sum,
    ],
    axis=1,
    join="outer",
)
pracoviska_excelentnost.loc[
    ["M1", "M2", "M3", "M4"], "publikacna_excelentnost"
] = pracoviska_excelentnost.loc[["M1", "M2", "M3", "M4"]]["sum_ADx"]
pracoviska_excelentnost.loc[
    ["M5"], "publikacna_excelentnost"
] = pracoviska_excelentnost.loc[["M5"]].apply(
    lambda x: x["sum_ADx"] * 0.75 + x["sum_AAx"] * 0.25, axis=1
)
pracoviska_excelentnost.loc[
    ["M6"], "publikacna_excelentnost"
] = pracoviska_excelentnost.loc[["M6"]].apply(
    lambda x: x["sum_ADx"] * 0.60 + x["sum_AAx"] * 0.40, axis=1
)
pracoviska_excelentnost.sort_values(by="publikacna_excelentnost", ascending=False)

for m in pocty_zamestnancov.columns:
    relevant_high = pocty_zamestnancov[m][pocty_zamestnancov[m] >= 5]
    relevant_low = pocty_zamestnancov[m][pocty_zamestnancov[m] >= 1][
        pocty_zamestnancov[m] < 5
    ]
    relevant_zero = pocty_zamestnancov[m][pocty_zamestnancov[m] == 0]
        relevant_excelent = pracoviska_excelentnost.loc[m]
    relevant_excelent = relevant_excelent[
        relevant_excelent["sum_ADx"] + relevant_excelent["sum_AAx"] > 0
    ]
        print(
        f"m={m}, 0==x={len(relevant_zero)} 0<x<5={len(relevant_low)}, 5<=x={len(relevant_high)}, pub|grant={len(relevant_excelent)}, excel={vysledne_pocty_fakult_v_oblastiach[m]}"
    )
    
vysledne_pocty_fakult_v_oblastiach

import subprocess

zamestnanci_publikacie = (
    pocty_zamestnancov.melt(
        ignore_index=False, var_name="oblast", value_name="pocty_zamestnancov"
    )
    .reset_index()
    .set_index(["oblast", "VS_NAZOV", "FAKULTA_NAZOV"])
    .query("pocty_zamestnancov >= 5")
    .join(pracoviska_excelentnost[["publikacna_excelentnost", "sum_granty"]])
    .fillna(0)
)
for oblast in sorted(set(oblasti_mapping.values())):
    print(oblast)
    display(zamestnanci_publikacie.loc[oblast])
    data = zamestnanci_publikacie.loc[oblast].reset_index()
        data.to_csv(f"../data/data_{oblast}.csv", index=False)
    
subprocess.run(["Rscript", "predict.r"])

for oblast in sorted(set(oblasti_mapping.values())):
    print(oblast)
    predicted = pd.read_csv(f"../data/predicted_{oblast}.csv")
    display(predicted)
    
import scipy.stats as stats
rezid_data = []
for oblast in sorted(set(oblasti_mapping.values())):
    print(oblast)
    data = pd.read_csv(f"../data/data_to_model_{oblast}_rezid.csv")
        data["oblast"] = oblast
        data = data.set_index(["oblast", "VS_NAZOV", "FAKULTA_NAZOV"])
        if rezid_data is None:
        rezid_data = data
    else:
        rezid_data.append(data)
        rezid_data = pd.concat(rezid_data)
rezid_data["publ_z_score"] = stats.zscore(rezid_data["rezidua_publ"])
rezid_data["grant_z_score"] = stats.zscore(rezid_data["rezidua_granty"])
rezid_data
