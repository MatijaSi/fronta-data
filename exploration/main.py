from functools import reduce
from typing import List
import pandas as pd
import matplotlib.pyplot as plt

epwt = pd.read_excel("../data/EPWT 7.0 FV.xlsx", "EPWT7.0")
oecd_ppp = pd.read_excel("../data/OECD_PPP.xlsx", "OECD_PPP")

oecd_ppp["Countrycode"] = oecd_ppp["LOCATION"]
oecd_ppp["Year"] = oecd_ppp["TIME"]
oecd_ppp["Conversion"] = oecd_ppp["Value"]

epwt = (
    epwt[
        [
            "Country",
            "Countrycode",
            "Year",
            "LabShare",
            "rnatcur",
            "XGDPnatcur",
            "Knatcur",
            "knatcur",
            "wnatcur",
            "delta",
            "rhonatcur",
        ]
    ]
    .dropna()
    .merge(oecd_ppp[["Countrycode", "Year", "Conversion"]], on=["Countrycode", "Year"])
)


# Variable capital
epwt["VariableCapital"] = epwt["LabShare"] * epwt["XGDPnatcur"] / epwt["Conversion"]

epwt["AverageWage"] = epwt["wnatcur"] / epwt["Conversion"]

# Constant capital
epwt["ConstantCapital"] = epwt["Knatcur"] / epwt["Conversion"]

# Surplus value
epwt["SurplusValue"] = (1 - epwt["LabShare"]) * epwt["XGDPnatcur"] / epwt["Conversion"]

# Rate of exploitation
epwt["ROE"] = epwt["SurplusValue"] / epwt["VariableCapital"]

# Technical composition of capital
epwt["TCC"] = epwt["knatcur"] / epwt["Conversion"]

# Organic composition of capital
epwt["OCC"] = epwt["TCC"] / epwt["AverageWage"]  # v / c
epwt["OCC2"] = 1 / epwt["rhonatcur"]  # v+pv / c

# Rate of profit
epwt["ROP"] = epwt["rnatcur"]


def df_split_by_field(df: pd.DataFrame, field: str) -> List[pd.DataFrame]:
    distinct = df[field].unique()

    dfs = [df[df[field] == country] for country in distinct]

    return dfs


def plot_multiline(
    dfs: List[pd.DataFrame], x: str, y: str, label: str, filename: str, title: str
):
    plt.figure(1)
    plt.title(title)

    for df in dfs:
        plt.plot(
            df[x],
            df[y],
            label=df[label].min(),
        )

    plt.legend()

    plt.savefig(filename)
    plt.close(1)


plot = False
if plot == True:
    data = epwt[["Country", "Year", "ROP", "OCC", "ROE", "TCC"]][
        epwt["Country"].isin(["Poland", "Germany", "Slovenia"])
    ]

    byCountry = df_split_by_field(data, "Country")

    minYear = max([df["Year"].min() for df in byCountry])

    byCountry = [df[df["Year"] >= minYear] for df in byCountry]

    plot_multiline(
        byCountry, "Year", "ROE", "Country", "figures/ROE.png", "Mera izkoriščanja"
    )

    plot_multiline(
        byCountry,
        "Year",
        "OCC",
        "Country",
        "figures/OCC.png",
        "Organska kompozicija kapitala",
    )

    plot_multiline(
        byCountry, "Year", "ROP", "Country", "figures/ROP.png", "Profitna mera"
    )

    plot_multiline(
        byCountry,
        "Year",
        "TCC",
        "Country",
        "figures/TCC.png",
        "Tehnična kompozicija kapitala",
    )

if False:
    print(
        epwt[epwt["Year"] == 2019][
            [
                "Country",
                "OCC",
                "OCC2",
                "ROE",
                "ROP",
            ]
        ]
        .sort_values("OCC2", ascending=False)
        .to_string()
    )

years = epwt["Year"].unique()
years.sort()


def calcRop(data: pd.DataFrame, year: int):
    df = data[data["Year"] == year]

    total_capital = (df["ConstantCapital"]).sum()

    weighted = df["ROP"] * df["ConstantCapital"] / total_capital

    return weighted.sum()


yearly = [{"Year": year, "ROP": calcRop(epwt, year)} for year in years]

arop = pd.DataFrame(yearly, columns=["Year", "ROP"])

print(arop.to_string())

plt.title("Svetovna profitna mera (v %)")
plt.plot(arop["Year"], arop["ROP"] * 100)
plt.savefig("figures/AROP.png")
