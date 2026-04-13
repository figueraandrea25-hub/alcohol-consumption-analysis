import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la Página de Streamlit

st.set_page_config(page_title="Dashboard de Consumo de Alcohol", layout="wide")

# Carga de Datos
DATA_URL = "https://raw.githubusercontent.com/figueraandrea25-hub/alcohol-consumption-analysis/refs/heads/main/alcohol_data.csv"
YEARS = (2015, 2019)

# Ordenamiento de la Data por regiones y asignación de colores 
REGIONS = {
    "América Latina y el Caribe": ["ATG","ARG","BHS","BRB","BLZ","BOL","BRA","CHL","COL","CRI","CUB","DMA","DOM","ECU","SLV","GRD","GTM","GUY","HTI","HND","JAM","MEX","NIC","PAN","PRY","PER","KNA","LCA","VCT","SUR","TTO","URY","VEN"],
    "América del Norte": ["CAN","USA"],
    "Asia": ["AFG","BHR","BGD","BTN","BRN","KHM","CHN","COK","CYP","PRK","EGY","FJI","IND","IDN","IRN","IRQ","ISR","JPN","JOR","KAZ","KGZ","KIR","KWT","LAO","LBN","MYS","MDV","MHL","FSM","MNG","MMR","NRU","NPL","NZL","NIU","OMN","PAK","PLW","PNG","PHL","QAT","KOR","WSM","SAU","SGP","SLB","LKA","SYR","TJK","THA","TLS","TON","TUR","TKM","TUV","ARE","UZB","VUT","VNM","YEM"],
    "Europa": ["ALB","AND","ARM","AUT","AZE","BLR","BEL","BIH","BGR","HRV","CZE","DNK","EST","FIN","FRA","GEO","DEU","GRC","HUN","ISL","IRL","ITA","LVA","LTU","LUX","MLT","MCO","MNE","NLD","MKD","NOR","POL","PRT","MDA","ROU","RUS","SMR","SRB","SVK","SVN","ESP","SWE","CHE","UKR","GBR"],
    "África": ["DZA","AGO","BEN","BWA","BFA","BDI","CMR","CPV","CAF","TCD","COM","COG","CIV","COD","DJI","GNQ","ERI","ETH","GAB","GMB","GHA","GIN","GNB","KEN","LSO","LBR","LBY","MDG","MWI","MLI","MRT","MUS","MAR","MOZ","NAM","NER","NGA","RWA","STP","SEN","SYC","SLE","SOM","ZAF","SSD","SDN","TGO","TUN","UGA","TZA","ZMB","ZWE"],
}
REGION_ORDER = list(REGIONS.keys()) + ["Otras/Oceanía"]
REGION_COLORS = {
    "América Latina y el Caribe": "#B04A45",
    "América del Norte": "#8D5A97",
    "Asia": "#2C7FB8",
    "Europa": "#A61C00",
    "África": "#516C92",
    "Otras/Oceanía": "#7A6C74",
}

# Carga y ordenamiento de los datos
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    df.columns = (
        df.columns.astype(str).str.strip().str.upper()
        .str.replace(" ", "_", regex=False)
        .str.replace(r"[^A-Z0-9_]", "", regex=True)
    )
    rename_map = {
        "COUNTRY_NAME": "COUNTRY",
        "TIME_PERIOD": "YEAR",
        "OBS_VALUE": "ALCOHOL_LITERS_PER_CAPITA",
        "ISO_3": "ISO3",
        "ISO_CODE": "ISO3",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
    return df

# Asignacion de regiones con el codigo ISO3
def assign_region(iso3):
    iso3 = str(iso3).strip().upper()
    for region, codes in REGIONS.items():
        if iso3 in codes:
            return region
    return "Otras/Oceanía"

# Limpieza de datos, filtrando años, sexo, convirtiendo columnas numericas y calculando incertidumbre 
def prepare_data(df):
    required = ["COUNTRY", "ISO3", "YEAR", "SEX", "ALCOHOL_LITERS_PER_CAPITA"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        st.error(f"Faltan columnas obligatorias: {missing}")
        st.write("Columnas encontradas:", df.columns.tolist())
        st.stop()

    df = df.copy()
    numeric_cols = ["YEAR", "ALCOHOL_LITERS_PER_CAPITA", "LOWER_CI", "UPPER_CI", "CI_WIDTH"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df["ISO3"] = df["ISO3"].astype(str).str.strip().str.upper()
    df["SEX"] = df["SEX"].astype(str).str.strip().str.lower()
    df = df[(df["YEAR"].between(*YEARS)) & (df["SEX"] == "both sexes")].copy()

    if "CI_WIDTH" not in df.columns:
        if "LOWER_CI" in df.columns and "UPPER_CI" in df.columns:
            df["CI_WIDTH"] = df["UPPER_CI"] - df["LOWER_CI"]
        else:
            df["CI_WIDTH"] = pd.NA
    df["REGION"] = df["ISO3"].apply(assign_region)
    return df.dropna(subset=["ALCOHOL_LITERS_PER_CAPITA"])

# Grafica de data sucia vs limpia ( Simulando valores faltantes para comparar el efecto de la limpieza )
def make_dirty_versions(df):
    dirty = df.copy()
    dirty.loc[dirty.sample(frac=0.10, random_state=123).index, "ALCOHOL_LITERS_PER_CAPITA"] = pd.NA
    recovered = dirty.dropna(subset=["ALCOHOL_LITERS_PER_CAPITA"]).copy()
    return dirty, recovered

# Resumen de datos por región y año, calculando el promedio y la incertidumbre media
def region_summary(df):
    summary = df.groupby("REGION", as_index=False).agg(
        Promedio=("ALCOHOL_LITERS_PER_CAPITA", "mean"),
        Mediana=("ALCOHOL_LITERS_PER_CAPITA", "median"),
        Desv_Est=("ALCOHOL_LITERS_PER_CAPITA", "std"),
        Incertidumbre=("CI_WIDTH", "mean"),
        Paises=("COUNTRY", "nunique"),
    )
    summary["REGION"] = pd.Categorical(summary["REGION"], categories=REGION_ORDER, ordered=True)
    return summary.sort_values("REGION")