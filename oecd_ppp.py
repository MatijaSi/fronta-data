import pandas as pd


def prepare_oecd_ppp(oecd_ppp: pd.DataFrame) -> pd.DataFrame:
    oecd_ppp["Countrycode"] = oecd_ppp["LOCATION"]
    oecd_ppp["Year"] = oecd_ppp["TIME"]
    oecd_ppp["Conversion"] = oecd_ppp["Value"]

    return oecd_ppp
