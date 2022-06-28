from numpy import full
import streamlit as st
import pandas as pd

from oecd_ppp import prepare_oecd_ppp
from epwt import prepare_epwt

st.set_page_config(
    page_title="Fronta.org: Data", layout="wide", initial_sidebar_state="expanded"
)

st.title("Fronta.org: Data")

epwt = pd.read_excel("../data/EPWT 7.0 FV.xlsx", "EPWT7.0")
oecd_ppp = pd.read_excel("../data/OECD_PPP.xlsx", "OECD_PPP")

oecd_ppp = prepare_oecd_ppp(oecd_ppp)
epwt = prepare_epwt(epwt, oecd_ppp)

st.subheader("EPWT")

min_year = int(epwt["Year"].min())
max_year = int(epwt["Year"].max())

(start_year, end_year) = st.slider(
    "Leto", min_year, max_year, value=(min_year, max_year)
)

countries = epwt["Country"].unique()

selected_countries = st.multiselect(
    "Država",
    countries,
    countries,
)


st.dataframe(
    epwt[
        [
            "Country",
            "Year",
            "VariableCapital",
            "AverageWage",
            "ConstantCapital",
            "SurplusValue",
            "ROE",
            "TCC",
            "OCC",
            "OCC2",
            "ROP",
        ]
    ][epwt["Year"].between(start_year, end_year, inclusive="both")][
        epwt["Country"].isin(selected_countries)
    ]
)
