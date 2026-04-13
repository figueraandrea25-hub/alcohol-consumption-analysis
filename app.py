import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la Página de Streamlit

<<<<<<< HEAD
st.set_page_config(page_title="Dashboard de Consumo de Alcohol", layout="wide")
=======
st.set_page_config(
    page_title="Dashboard de Consumo de Alcohol por Regiones",

# Configuración de la Página de Streamlit

st.set_page_config(
    page_title="Dashboard de Consumo de Alcohol por Regiones",
st.set_page_config(
    page_title="Dashboard Consumo de Alcohol en el Mundo (2000-2022)",

    layout="wide",
    initial_sidebar_state="expanded"
)

PALETA_PRINCIPAL = ["#1a6b3c", "#2d9e6b", "#4cc38a", "#90dbb5", "#d4f0e3"]
COLOR_BASE = PALETA_PRINCIPAL[0]
>>>>>>> eeb434d9f71d56825d826ec80511f45180f73885

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

<<<<<<< HEAD
    df["REGION"] = df["ISO3"].apply(assign_region)
    return df.dropna(subset=["ALCOHOL_LITERS_PER_CAPITA"])
=======
    if "ISO3" in df.columns:
        df["ISO3"] = df["ISO3"].astype(str).str.strip().str.upper()

    df = df[df["YEAR"].between(ANIOS_ANALISIS[0], ANIOS_ANALISIS[1])].copy()
    df["REGION"] = df["ISO3"].apply(asignar_region)
    df = df[df["REGION"].isin(REGION_ORDER)].copy()

    for col in ["LOWER_CI", "UPPER_CI", "CI_WIDTH"]:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())

    return df


def tabla_formateada(df: pd.DataFrame, columnas_decimales=None):
    """Aplica formato simple para mostrar tablas de forma más limpia."""
    columnas_decimales = columnas_decimales or []
    formato = {col: "{:.2f}" for col in columnas_decimales if col in df.columns}
    return df.style.format(formato)


def construir_filtros(data: pd.DataFrame):
    """Centraliza los filtros globales y la navegación por secciones."""
    st.sidebar.header("Navegación y filtros")

    seccion_activa = st.sidebar.radio(
        "Sección del dashboard",
        options=SECCIONES,
        index=0
    )

    sex_options = sorted(data["SEX"].dropna().unique().tolist())
    default_sex = ["Both Sexes"] if "Both Sexes" in sex_options else sex_options[:1]
    selected_sex = st.sidebar.multiselect(
        "Sexo",
        options=sex_options,
        default=default_sex
    )
    selected_regions_global = st.sidebar.multiselect(
        "Regiones a incluir",
        options=REGION_ORDER,
        default=REGION_ORDER,
        help="Este filtro afecta todo el dashboard."
    )

    selected_years = st.sidebar.slider(
        "Rango de años",
        min_value=ANIOS_ANALISIS[0],
        max_value=ANIOS_ANALISIS[1],
        value=ANIOS_ANALISIS
    )

    top_n = st.sidebar.selectbox(
        "Top de países para rankings",
        options=[5, 10, 15, 20],
        index=1
    )

    return seccion_activa, selected_sex, selected_regions_global, selected_years, top_n
   
   # Analisis y grafico por regiones y paises  
def mostrar_encabezado():
    st.title("🌍 Dashboard de Consumo de Alcohol por Regiones")
    st.markdown(
        "Análisis interactivo del consumo de alcohol per cápita **solo entre 2015 y 2019**, "
        "organizado por regiones y países."
    )
    st.caption(
        "Ahora el panel funciona por secciones: eliges una vista y solo se muestra esa página para que la lectura sea más limpia."
    )
    st.markdown("---")


def mostrar_resumen_general(df_filtered: pd.DataFrame):
    st.header("📌 Resumen general")
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.metric("Regiones analizadas", df_filtered["REGION"].nunique())
    with k2:
        st.metric("Países analizados", df_filtered["COUNTRY"].nunique())
    with k3:
        st.metric("Promedio general (L/cápita)", f"{df_filtered['ALCOHOL_LITERS_PER_CAPITA'].mean():.2f}")
    with k4:
        st.metric("Valor máximo observado", f"{df_filtered['ALCOHOL_LITERS_PER_CAPITA'].max():.2f}")

    st.markdown("### Vista rápida de evolución anual")
    resumen_anual = (
        df_filtered.groupby("YEAR")["ALCOHOL_LITERS_PER_CAPITA"]
        .mean()
        .reset_index()
    )
    fig = px.line(
        resumen_anual,
        x="YEAR",
        y="ALCOHOL_LITERS_PER_CAPITA",
        markers=True,
        title="Promedio general por año",
        labels={"YEAR": "Año", "ALCOHOL_LITERS_PER_CAPITA": "Litros per cápita"}
    )
    st.plotly_chart(fig, use_container_width=True)


def mostrar_paises_por_region(df_filtered: pd.DataFrame):
    st.header("📋 Países organizados por región (2015–2019)")

    tabla_regiones = (
        df_filtered[["REGION", "COUNTRY", "ISO3"]]
        .drop_duplicates()
        .sort_values(["REGION", "COUNTRY"])
        .reset_index(drop=True)
    )

    resumen_region = (
        tabla_regiones.groupby("REGION")
        .agg(Paises=("COUNTRY", "nunique"))
        .reset_index()
    )

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown("### Resumen de países por región")
        st.dataframe(resumen_region, use_container_width=True)
    with c2:
        st.markdown("### Tabla ordenada por región y país")
        st.dataframe(tabla_regiones, use_container_width=True, height=420)

        # --- 2. Layout del Dashboard (Títulos Fijos) --
# Definición de las Paletas de Colores
PALETTE_WORLD = ["#1a6b3c", "#2d9e6b", "#4cc38a", "#90dbb5", "#d4f0e3", "#000000"]
PALETTE_COLOURS = ["#1a6b3c", "#e07b39", "#3a7ebf", "#c94040", "#8e44ad"]
PRIMARY_COLOR = PALETTE_COLOURS[0]

DATA_URL = (
    "https://raw.githubusercontent.com/figueraandrea25-hub/alcohol-consumption-analysis/refs/heads/andrea-dev/dataset/alcohol_data.csv"
)

>>>>>>> eeb434d9f71d56825d826ec80511f45180f73885
