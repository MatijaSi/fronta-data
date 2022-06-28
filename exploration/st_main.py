import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from common import df_split_by_field, plot_multiline

from oecd_ppp import prepare_oecd_ppp
from epwt import prepare_epwt
from rop import calcRop

st.set_page_config(
    page_title="Fronta.org: Data", layout="wide", initial_sidebar_state="expanded"
)

st.title("Fronta.org: Data")

epwt = pd.read_excel("../data/EPWT 7.0 FV.xlsx", "EPWT7.0")
oecd_ppp = pd.read_excel("../data/OECD_PPP.xlsx", "OECD_PPP")

oecd_ppp = prepare_oecd_ppp(oecd_ppp)
epwt = prepare_epwt(epwt, oecd_ppp)

st.header("EPWT")

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

col1, col2 = st.columns([2, 1])

with col1:
    st.dataframe(filtered_epwt)


years = epwt["Year"].unique()
years.sort()
yearly = [{"Year": year, "ROP": calcRop(epwt, year)} for year in years]

arop = pd.DataFrame(yearly, columns=["Year", "ROP"])

rop_fig, rop_ax = plt.subplots()

rop_ax.set_title("Svetovna profitna mera")
rop_ax.plot(arop["Year"], arop["ROP"], label="Svet")

z = np.polyfit(arop["Year"], arop["ROP"], 1)
linearTrendLine = np.poly1d(z)

rop_ax.plot(
    arop["Year"],
    linearTrendLine(arop["Year"]),
    label="Linearni trend",
    linestyle="--",
    linewidth=1,
)

rop_ax.legend()

with col2:
    st.pyplot(rop_fig)


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

st.subheader("Legenda")
st.markdown(
    """
##### Vir podatkov: Extended Penn Tables 7.0

Naloženo z [Harvard Dataverse: EPWT 7.0 FV](https://dataverse.harvard.edu/file.xhtml?fileId=6022652&version=1.1).

**Tabelo se citira kot:**
Marquetti, A., Morrone, H., and Miebach, A. (2021). The Extended Penn World Tables 7.0. Texto para Discussão 2021/01, UFRGS.

Tabela je vir [večje zbirke podatkov](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/2OL4IW&version=1.1), s sledečimi pogoji:

**Licenca za uporabo:**
CC0 1.0 - Public domain

**Zbirka podatkov se citira kot:**
Basu, Deepankar, 2022, "World Profit Rates, 1960-2019", https://doi.org/10.7910/DVN/2OL4IW, Harvard Dataverse, V1

##### Vir podatkov: OECD_PPP.xlsx

Naloženo z [Harvard Dataverse: OECD PPP](https://dataverse.harvard.edu/file.xhtml?fileId=6022651&version=1.1).

Tabela je vir [večje zbirke podatkov](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/2OL4IW&version=1.1), s sledečimi pogoji:

**Licenca za uporabo:**
CC0 1.0 - Public domain

**Zbirka podatkov se citira kot:**
Basu, Deepankar, 2022, "World Profit Rates, 1960-2019", https://doi.org/10.7910/DVN/2OL4IW, Harvard Dataverse, V1

##### Metodologija:

Iz EPWT smo izčrpali sledeče stolpce:
*Country*, *Countrycode*, *Year*, *LabShare*, *rnatcur*, *XGDPnatcur*, *Knatcur*, *knatcur*, *wnatcur*, *delta*, *rhonatcur*.

Iz nje smo odstranili vse vrstice z vsaj enim praznim poljem.

Iz tabele OECD_PPP smo izčrpali:
*LOCATION*, *TIME*, *Value*.

Tabeli smo združili po stolpcih *CountryCode* = *LOCATION* in *Year* = *TIME*. Stolpec *Value* smo preimenovali v *Conversion*.

Nastali conversion smo uporabili za preračun izvirnih nacionalnih tekočih cen v PPP.

##### Podatkovna shema:

| Stolpec | Vir | Opis |
| -- | -- | -- |
| Country | Country | Država |
| Year | Year | Leto |
| VariableCapital | LabShare * XGDPnatcur / Conversion | Variabilni kapital |
| ConstantCapital | Knatcur / Conversion | Konstantni kapital |
| SurplusValue | (1 - LabShare) * XGDPnatcur / Conversion | Presežna vrednost |
| ROE | SurplusValue / VariableCapital | Mera eksploitacije |
| TCC | knatcur / Conversion | Tehnična kompozicija kapitala (konstantni kapital / št. delavcev) |
| OCC | TCC / wnatcur / Conversion | Organska kompozicija kapitala (konstantni kapital / variabilni kapital) |
| OCC2 | 1 / rhonatcur | Organska kompozicija kapitala 2 (konstantni kapital / (variabilni kapital + presežna vrednost)) |
| ROP | rnatcur | Profitna mera |

##### Literatura:
Basu, Deepankar; Huato, Julio; Jauregui, Jesus Lara; and Wasner, Evan, "World Profit Rates, 1960-2019" (2022). Economics Department Working Paper Series. 318.
[https://doi.org/10.7275/43yv-c721](https://doi.org/10.7275/43yv-c721)
"""
)
