import matplotlib.pyplot as plt
import pandas as pd

# WIOD Data
sea_wiod = pd.read_excel("../data/SEA-WIOD.xlsx", "DATA")

sea_rop_raw = []

years_covered = range(2000, 2015)

for i, row in sea_wiod[["country", "description", "code"]].drop_duplicates().iterrows():
    country = sea_wiod[sea_wiod["country"] == row["country"]]
    sector = country[country["code"] == row["code"]]

    value_added = sector[sector["variable"] == "VA"]
    capital_stock = sector[sector["variable"] == "K"]
    labour_share = sector[sector["variable"] == "LAB"]

    for year in years_covered:
        newValue = value_added[year].iloc[0]
        constantCapital = capital_stock[year].iloc[0]
        variableCapital = labour_share[year].iloc[0]
        surplusValue = newValue - variableCapital

        if (
            newValue == 0
            or constantCapital == 0
            or variableCapital == 0
            or surplusValue == 0
        ):
            continue

        sea_rop_raw += [
            {
                "country": row["country"],
                "description": row["description"],
                "code": row["code"],
                "year": year,
                "VA": newValue,
                "ConstantCapital": constantCapital,
                "VariableCapital": variableCapital,
                "SurplusValue": surplusValue,
                "ROE": surplusValue / variableCapital,
                "ROP": surplusValue / (constantCapital + variableCapital),
                "OCC": constantCapital / variableCapital,
                "OCC2": constantCapital / newValue,
            }
        ]


sea_rop = pd.DataFrame(sea_rop_raw)

slo = sea_rop[sea_rop["country"] == "SVN"]

construction = slo[slo["code"] == "F"]

plt.plot(construction["year"], construction["ROP"])
plt.savefig("figures/slo_sektorF_ROP.png")

print(construction.to_string())
