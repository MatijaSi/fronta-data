import pandas as pd


def prepare_epwt(epwt: pd.DataFrame, oecd_ppp: pd.DataFrame) -> pd.DataFrame:
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
        .merge(
            oecd_ppp[["Countrycode", "Year", "Conversion"]], on=["Countrycode", "Year"]
        )
    )

    # Variable capital
    epwt["VariableCapital"] = epwt["LabShare"] * epwt["XGDPnatcur"] / epwt["Conversion"]

    epwt["AverageWage"] = epwt["wnatcur"] / epwt["Conversion"]

    # Constant capital
    epwt["ConstantCapital"] = epwt["Knatcur"] / epwt["Conversion"]

    # Surplus value
    epwt["SurplusValue"] = (
        (1 - epwt["LabShare"]) * epwt["XGDPnatcur"] / epwt["Conversion"]
    )

    # Rate of exploitation
    epwt["ROE"] = epwt["SurplusValue"] / epwt["VariableCapital"]

    # Technical composition of capital
    epwt["TCC"] = epwt["knatcur"] / epwt["Conversion"]

    # Organic composition of capital
    epwt["OCC"] = epwt["TCC"] / epwt["AverageWage"]  # v / c
    epwt["OCC2"] = 1 / epwt["rhonatcur"]  # v+pv / c

    # Rate of profit
    epwt["ROP"] = epwt["rnatcur"]

    return epwt
