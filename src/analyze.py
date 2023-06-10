#!/usr/bin/env python
# coding: utf-8


# get_ipython().run_line_magic('pip', 'install pandas')
# get_ipython().run_line_magic('pip', 'install openpyxl')
# get_ipython().run_line_magic('pip', 'install scipy')

import pandas as pd
import numpy as np

display = print

data_source = "online"  # "local" or "online

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
# ['E1_alokácia', 'E2_zamestnanci_2021', 'E3_oblasti', 'E4a_M1_prirodne', 'E4b_M2_technicke', 'E4c_M3_lekarske', 'E4d_M4_polno_les_vet', 'E4e_M5_spolocenske', 'E4f_M6_humanitne', 'E4g_M6_umenie']
prilohaB = pd.read_excel(prilohy_path["B"], sheet_name=None)
print(prilohaB.keys())
# ['2021 - 3']
prilohaC = pd.read_excel(prilohy_path["C"], sheet_name=None)
print(prilohaC.keys())
# ['crepc 2020', 'crepc 2021', 'crepc 2022', 'crepc 2022-2', 'CVTI_NORDIC', 'Nordic_CVTI 2020', 'Nordic_CVTI 2021', 'vystupy 2020', 'vystupy 2021', 'Hárok1']
prilohaD = pd.read_excel(prilohy_path["D"], sheet_name=None)
print(prilohaD.keys())
# ['T3 - výsk. zahr. grant. schémy', 'old', 'oblasti výskumu', 'VŠ', 'Odbory VaT']
prilohaPUBL = pd.read_excel(prilohy_path["publ"], sheet_name=None, header=None)
print(prilohaPUBL.keys())
# ['vs_podiel', 'jednotkove', 'kalkuljednotkove', 'distribucia', 'data', 'sucasti', 'zoznamvs', 'kategoriaskupiny', 'vahymnozin', 'mnoziny', 'Patenty', 'rozpis07712', 'rozpis07711']


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


# a) excelentná publikačná činnosť podľa bodu 4, celková váha 60%.
#
# a) V oblastiach **M1**: prírodné vedy, **M2**: technické vedy, **M3**: lekárske vedy, **M4**: poľnohospodárske, lesnícke a veterinárske vedy sa zohľadňujú **váhou 100%** indexované publikácie (WoS, Scopus), teda kategórie **ADC, ADD, ADM, ADN**. Zoznam sa nachádza **v prílohe B**. Všetky výstupy sa **váhujú** podľa pracovísk tak, aby každý výstup bol zarátaný iba raz (súčet všetkých váh za daný **výstup je 1,00**).
#
# b) V oblasti **M5**: spoločenské vedy sa zohľadňujú **váhou 75%** indexované publikácie **(WoS, Scopus)**, teda kategórie **ADC, ADD, ADM, ADN**. Tieto výstupy sa bonifikujú v súlade s metodikou rozpisu **(prvý kvartil JCR je zohľadnený váhou 6, druhý kvartil váhou 4, tretí kvartil váhou 1 a štvrtý kvartil váhou 0,5)**. Zoznam sa nachádza **v prílohe B**. **Váhou 25%** sa zohľadňujú monografie (**AAA, AAB**). Tieto výstupy sa **bonifikujú** tak, že vydavateľstvá zaradené v databáze Nordic List (https://kanalregister.hkdir.no/publiseringskanaler/Forside.action?request_locale=en) v kategórii 2 (prestížne vedecké vydavateľstvo) sú bonifikované váhou 6, vydavateľstvá zaradené v databáze Nordic List v kategórii 1 (vedecké vydavateľstvo) váhou 4, vydavateľstvá zaradené v databáze CVTI (zoznam zahraničných vydavateľstiev: http://cms.crepc.sk/Data/Sites/1/pdf/zoznam-vydavatelstva/zoznam-vydavatelstva-01-2020.pdf) sú zohľadnené váhou 1 a všetky ostatné monografie sú zohľadnené váhou 0,5). Zoznam aj so zaradením sa nachádza v prílohe C. Všetky výstupy sa váhujú podľa pracovísk tak, aby každý výstup bol zarátaný iba raz (súčet všetkých váh za daný výstup je 1,00).
#
# c) V oblasti M6a: humanitné vedy sa zohľadňujú váhou 60% indexované publikácie (WoS, Scopus), teda kategórie ADC, ADD, ADM, ADN. Tieto výstupy sa bonifikujú v súlade s metodikou rozpisu (prvý kvartil JCR je zohľadnený váhou 6, druhý kvartil váhou 4, tretí kvartil váhou 1 a štvrtý kvartil váhou 0,5). Zoznam sa nachádza v prílohe B. Váhou 40% sa zohľadňujú monografie (AAA, AAB). Tieto výstupy sa bonifikujú tak, že vydavateľstvá zaradené v databáze Nordic List (https://kanalregister.hkdir.no/publiseringskanaler/Forside.action?request_locale=en) v kategórii 2 (prestížne vedecké vydavateľstvo) sú bonifikované váhou 6, vydavateľstvá zaradené v databáze Nordic List v kategórii 1 (vedecké vydavateľstvo) váhou 4, vydavateľstvá zaradené v databáze CVTI (zoznam zahraničných vydavateľstiev: http://cms.crepc.sk/Data/Sites/1/pdf/zoznam-vydavatelstva/zoznam-vydavatelstva-01-2020.pdf) sú zohľadnené váhou 1 a všetky ostatné monografie sú zohľadnené váhou 0,5). Zoznam aj so zaradením sa nachádza v prílohe C. Všetky výstupy sa váhujú podľa pracovísk tak, aby každý výstup bol zarátaný iba raz (súčet všetkých váh za daný výstup je 1,00).
#
# d) v oblasti M6b umenie sa zohľadňujú váhou 100% umelecké výstupy v kategóriách ZZZ, ZZY, ZYZ, ZYY podľa váh platných pre rozpis dotácie 2022. Údaje sa nachádzajú v rozpise dotácie na rok 2022, hárok E4g_M6_umenie. Osobitne sa zohľadňujú oblasti performatívne umenie a vizuálne umenie.


casovy_ramec = [2020, 2021]

# prilohy B, C
epc_codes_ADx = ["ADC", "ADD", "ADM", "ADN"]
epc_codes_AAx = ["AAA", "AAB"]
epc_codes_Zxx = ["ZZZ", "ZZY", "ZYZ", "ZYY"]

epc_codes_M1_M4 = epc_codes_ADx
epc_codes_M5 = epc_codes_ADx + epc_codes_AAx  # TODO bonifikacia
epc_codes_M6a = epc_codes_ADx + epc_codes_AAx  # TODO bonifikacia
epc_codes_M6b = epc_codes_Zxx  # E4g_M6_umenie

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
# publikacie_ADx_melted['PODIEL'] = publikacie_ADx_melted['PODIEL'] / publikacie_ADx_melted['ID_V_CREPC'].map(sum_podielov)
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


# {
#     oblast: publikacie_ADx_melted[publikacie_ADx_melted['oblast'] == oblast]
#         .loc[:, index_columns]
#         .drop_duplicates()
#         .set_index(index_columns)
#     for oblast in set(oblasti_mapping.values())
# }


# publikacie_ADx_sum = sumup_groupby(publikacie_ADx_melted, ['oblast'] + index_columns, 'PODIEL', 'sum_ADx')
publikacie_ADx_melted["vahaxJCR"] = (
    publikacie_ADx_melted["PODIEL"] * publikacie_ADx_melted["JCR_bonus"]
)
publikacie_ADx_sum = sumup_groupby(
    publikacie_ADx_melted, ["oblast"] + index_columns, "vahaxJCR", "sum_ADx"
)
# publikacie_ADx_melted = krat2zaokruhli(publikacie_ADx_melted, 'vahaxJCR')
# publikacie_ADx_sum = sumup_groupby(publikacie_ADx_melted, ['oblast'] + index_columns, 'vahaxJCR_zaokruhlene', 'sum_ADx')
publikacie_ADx_sum.sort_values(ascending=False)


stlpce = ["VS_NAZOV", "FAKULTA_NAZOV", "kategoria_metodika"]
melt_stlpce = [f"OBLAST_VYSKUMU_KOD{i}" for i in ["", 2]]
publikacie_AAx_melted = melt_sheet(publikacie_AAx, stlpce, melt_stlpce, "oblast_kod")
publikacie_AAx_melted["oblast"] = publikacie_AAx_melted["oblast_kod"].map(
    oblasti_mapping
)


publikacie_AAx_sum = sumup_groupby(
    publikacie_AAx_melted, ["oblast"] + index_columns, "kategoria_metodika", "sum_AAx"
)
# publikacie_AAx_melted = krat2zaokruhli(publikacie_AAx_melted, 'kategoria_metodika')
# publikacie_AAx_sum = sumup_groupby(publikacie_AAx_melted, ['oblast'] + index_columns, 'kategoria_metodika_zaokruhlene', 'sum_AAx')
publikacie_AAx_sum.sort_values(ascending=False)


# 5. Excelentný výkon pri získavaní výskumných grantov sa určuje nasledovne: pre všetky oblasti okrem M6b (umenie) sa zohľadňuje objem grantových prostriedkov, získaných súťažným spôsobom v kategórii zahraničné výskumné granty. Zoznam sa nachádza v prílohe D. Zahraničné výskumné granty sa priraďujú iba tým pracoviskám, v ktorých vysoké školy uviedli príslušných zamestnancov v danej oblasti.
#
#


granty_orig = prilohaD["T3 - výsk. zahr. grant. schémy"].copy()
# granty_orig = granty_orig[granty_orig['Rok'].isin(casovy_ramec)]

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
    # print(m)
    relevant_high = pocty_zamestnancov[m][pocty_zamestnancov[m] >= 5]
    relevant_low = pocty_zamestnancov[m][pocty_zamestnancov[m] >= 1][
        pocty_zamestnancov[m] < 5
    ]
    relevant_zero = pocty_zamestnancov[m][pocty_zamestnancov[m] == 0]
    # print(pracoviska_excelentnost.loc[m])
    relevant_excelent = pracoviska_excelentnost.loc[m]
    relevant_excelent = relevant_excelent[
        relevant_excelent["sum_ADx"] + relevant_excelent["sum_AAx"] > 0
    ]
    # print(relevant)
    print(
        f"m={m}, 0==x={len(relevant_zero)} 0<x<5={len(relevant_low)}, 5<=x={len(relevant_high)}, pub|grant={len(relevant_excelent)}, excel={vysledne_pocty_fakult_v_oblastiach[m]}"
    )
    # print(relevant_high)
    # print(relevant_excelent)
    # print()

vysledne_pocty_fakult_v_oblastiach


import subprocess

# export grant data to csv
# run r script
# import resulting csv containing predicted values
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

    # csv = data.to_csv(index=False)
    # subprocess.run(['Rscript', 'predict.r'], stdin=csv)
    # predicted = pd.read_csv('predicted.csv')
    # pracoviska_excelentnost.loc[[oblast], 'publikacne_predicted'] = predicted


zamestnanci_publikacie


subprocess.run(["Rscript", "predict.r"])
# or run predict.r manually


for oblast in sorted(set(oblasti_mapping.values())):
    print(oblast)
    predicted = pd.read_csv(f"../data/predicted_{oblast}.csv")
    display(predicted)
    # pracoviska_excelentnost.loc[[oblast], 'publikacne_predicted'] = predicted


import scipy.stats as stats

rezid_data = []
for oblast in sorted(set(oblasti_mapping.values())):
    print(oblast)
    data = pd.read_csv(
        f"../data/zbehnute/data_to_model_{oblast}_rezid.csv"
    )  # tu chce byt tabulka s rezid

    ### TODO
    data["sum_granty"] = data["sum_granty"] / 2
    data["rezidua_granty"] = data["rezidua_granty"] / 2
    data["fit_granty"] = data["sum_granty"] - data["rezidua_granty"]
    ####

    # display(data)
    data["oblast"] = oblast
    # display(data)
    data = data.set_index(["oblast", "VS_NAZOV", "FAKULTA_NAZOV"])
    # display(data)
    data["publ_z_score"] = stats.zscore(data["rezidua_publ"])
    data["grant_z_score"] = stats.zscore(data["rezidua_granty"])
    data["final_score"] = data["publ_z_score"] * 0.6 + data["grant_z_score"] * 0.4
    if rezid_data is None:
        rezid_data = data
    else:
        rezid_data.append(data)
rezid_data[0]


rozdelenie_penazi = (
    zamestnanci_publikacie.groupby("oblast")
    .sum()["publikacna_excelentnost"]
    .astype(int)
    .reset_index()
    .rename(columns={"publikacna_excelentnost": "publikacie_23"})
)
# rozdelenie_penazi['granty_23'] = zamestnanci_publikacie.groupby('oblast').sum()['sum_granty'].reset_index()['sum_granty']
# rozdelenie_penazi['publikacie_23'] = zamestnanci_publikacie.groupby('oblast').sum()['publikacna_excelentnost'].reset_index()
display(rozdelenie_penazi)
rozdelenie_penazi["publikacie_podiel"] = (
    rozdelenie_penazi["publikacie_23"] / rozdelenie_penazi["publikacie_23"].sum()
)
rozdelenie_penazi["granty23"] = (
    zamestnanci_publikacie.groupby("oblast")
    .sum()["sum_granty"]
    .reset_index()["sum_granty"]
)
rozdelenie_penazi["granty_podiel"] = (
    rozdelenie_penazi["granty23"] / rozdelenie_penazi["granty23"].sum()
)
rozdelenie_penazi["final_podiel"] = (
    rozdelenie_penazi["publikacie_podiel"] * 0.6
    + rozdelenie_penazi["granty_podiel"] * 0.4
)

peniaze_na_rozdelenie = 17538657.52
rozdelenie_penazi["peniaze"] = rozdelenie_penazi["final_podiel"] * peniaze_na_rozdelenie

rozdelenie_penazi


kam_peniaze = []
for i, oblast in enumerate(sorted(set(oblasti_mapping.values()))):
    data = rezid_data[i]
    suma = rozdelenie_penazi.loc[rozdelenie_penazi["oblast"] == oblast][
        "peniaze"
    ].values[0]
    kam_peniaze = data.sort_values(by="final_score", ascending=False)[
        : round(len(data) / 4)
    ]
    vykon_spolu = kam_peniaze["final_score"].sum()
    kam_peniaze["podiel_vykon"] = kam_peniaze["final_score"] / vykon_spolu
    kam_peniaze["vaha_zam23"] = (
        kam_peniaze["pocty_zamestnancov"] * kam_peniaze["podiel_vykon"]
    )
    suma_na_zamestnanca = suma / kam_peniaze["vaha_zam23"].sum()
    kam_peniaze["pridelene_peniaze"] = kam_peniaze["vaha_zam23"] * suma_na_zamestnanca

    data = pd.concat(
        [data, kam_peniaze[["podiel_vykon", "vaha_zam23", "pridelene_peniaze"]]], axis=1
    )
    rezid_data[i] = data


# get_ipython().run_line_magic("pip", "install xlsxwriter")

writer = pd.ExcelWriter("output.xlsx", engine="xlsxwriter")
workbook = writer.book
rozdelenie_penazi.to_excel(writer, sheet_name="Alokacia")
worksheet = writer.sheets[f"Alokacia"]
for j, col in enumerate(rozdelenie_penazi):
    column_len = rozdelenie_penazi[col].astype(str).str.len().max()
    column_len = max(column_len, len(col))
    worksheet.set_column(j, j, column_len)
for i, sheet in enumerate(rezid_data):
    sheet = sheet.reset_index()
    sheet.to_excel(writer, sheet_name=f"oblast_M{i + 1}", index=False)
    worksheet = writer.sheets[f"oblast_M{i + 1}"]
    for j, col in enumerate(sheet):
        column_len = sheet[col].astype(str).str.len().max()
        column_len = max(column_len, len(col))
        worksheet.set_column(j, j, column_len)
    format4 = workbook.add_format({"bg_color": "#ffff00"})
    worksheet.conditional_format(
        f"O2:O{len(sheet)}",
        {"type": "cell", "criteria": "!=", "value": 0, "format": format4},
    )
writer.close()


display(rezid_data[0])


# %pip install matplotlib
import matplotlib.pyplot as plt

ref_granty = []
ref_publikacie = []
pd.options.display.max_rows = 200

for i in sorted(prilohaA.keys())[3:-1]:
    data = prilohaA[i].copy()
    data.columns = data.iloc[1]
    data = (
        data.iloc[2:]
        .rename(columns={"FAKULTA_NAZOV / sucasti": "FAKULTA_NAZOV"})
        .set_index(index_columns)
    )

    # display(data)
    if i in ["E4f_M6_humanitne", "E4e_M5_spolocenske"]:
        ref_granty.append(data.loc[:, "grant23"])
    else:
        ref_granty.append(data.loc[:, "granty23"])
    ref_publikacie.append(data.loc[:, "index23fin"])


def graph_porovnanie(data, poradie, stlpec_u_nas, stlpec_ref, nazov):
    fig = plt.figure()
    fig.suptitle(nazov)
    porovnanie = pd.DataFrame(data)
    porovnanie["nase"] = (
        rezid_data[poradie]
        .loc[:, stlpec_u_nas]
        .reset_index()
        .drop(columns=["oblast"])
        .set_index(index_columns)
    )
    porovnanie = porovnanie[list(porovnanie.reset_index()["VS_NAZOV"].isna() == False)]
    porovnanie.loc[porovnanie[stlpec_ref] == 0, stlpec_ref] = (
        porovnanie.loc[porovnanie[stlpec_ref] == 0, "nase"] / 2
    ).apply(np.abs)
    porovnanie = porovnanie.loc[porovnanie[stlpec_ref] != 0]
    porovnanie["rozdiel"] = porovnanie["nase"] / porovnanie[stlpec_ref] - 1
    porovnanie = porovnanie.reset_index()
    porovnanie["nazov_cely"] = (
        porovnanie["VS_NAZOV"].map(lambda s: " ".join(s.split()[:2]))
        + " - "
        + porovnanie["FAKULTA_NAZOV"]
    )
    porovnanie.set_index("nazov_cely")["rozdiel"].plot.bar()
    plt.plot(porovnanie.reset_index().set_index("nazov_cely")["rozdiel"], "o")
    fig.savefig(nazov + ".png", bbox_inches="tight")


# graph_porovnanie(ref_granty[0], 0, 'sum_granty', 'granty23','m1_granty_porovnanie')

for i in range(4):
    graph_porovnanie(
        ref_granty[i], i, "sum_granty", "granty23", f"m{i+1}_granty_porovnanie"
    )
    graph_porovnanie(
        ref_publikacie[i],
        i,
        "publikacna_excelentnost",
        "index23fin",
        f"m{i+1}_publikacie_porovnanie",
    )

for i in range(4, 6):
    graph_porovnanie(
        ref_granty[i], i, "sum_granty", "grant23", f"m{i+1}_granty_porovnanie"
    )
    graph_porovnanie(
        ref_publikacie[i],
        i,
        "publikacna_excelentnost",
        "index23fin",
        f"m{i+1}_publikacie_porovnanie",
    )
