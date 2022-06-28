import streamlit as st
import pandas as pd
from common import df_split_by_field, plot_multiline

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

filtered_epwt = epwt[
    [
        "Country",
        "Year",
        "VariableCapital",
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

st.dataframe(filtered_epwt)

byCountry_epwt = df_split_by_field(filtered_epwt, "Country")

epwt_vc_plot = plot_multiline(
    byCountry_epwt,
    "Year",
    "VariableCapital",
    "Country",
    "Variabilni kapital (VariableCapital)",
)

epwt_cc_plot = plot_multiline(
    byCountry_epwt,
    "Year",
    "ConstantCapital",
    "Country",
    "Konstantni kapital (ConstantCapital)",
)

epwt_sv_plot = plot_multiline(
    byCountry_epwt,
    "Year",
    "SurplusValue",
    "Country",
    " Presežna vrednost (SurplusValue)",
)


epwt_roe_plot = plot_multiline(
    byCountry_epwt, "Year", "ROE", "Country", "Mera izkoriščanja (ROE)"
)

epwt_tcc_plot = plot_multiline(
    byCountry_epwt, "Year", "TCC", "Country", "Tehnična kompozicija kapitala (TCC)"
)

epwt_occ_plot = plot_multiline(
    byCountry_epwt, "Year", "OCC", "Country", "Organska kompozicija kapitala (OCC)"
)

epwt_occ2_plot = plot_multiline(
    byCountry_epwt, "Year", "OCC2", "Country", "Organska kompozicija kapitala 2 (OCC2)"
)

epwt_rop_plot = plot_multiline(
    byCountry_epwt, "Year", "ROP", "Country", "Profitna mera (ROP)"
)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.pyplot(epwt_vc_plot)
    st.pyplot(epwt_cc_plot)
    st.pyplot(epwt_sv_plot)

with col2:
    st.pyplot(epwt_roe_plot)

with col3:
    st.pyplot(epwt_tcc_plot)
    st.pyplot(epwt_occ_plot)
    st.pyplot(epwt_occ2_plot)

with col4:
    st.pyplot(epwt_rop_plot)
