import pandas as pd


def calcRop(data: pd.DataFrame, year: int):
    df = data[data["Year"] == year]

    total_capital = (df["ConstantCapital"]).sum()

    weighted = df["ROP"] * df["ConstantCapital"] / total_capital

    return weighted.sum()
