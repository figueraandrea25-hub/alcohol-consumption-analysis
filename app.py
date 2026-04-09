import streamlit as st
import pandas as pd
import plotly.express as px
<<<<<<< HEAD

# Configuración de la Página de Streamlit

st.set_page_config(
    page_title="Dashboard de Consumo de Alcohol por Regiones",
=======
st.set_page_config(
    page_title="Dashboard Consumo de Alcohol en el Mundo (2000-2022)",
>>>>>>> main
    layout="wide",
    initial_sidebar_state="expanded"
)

<<<<<<< HEAD
PALETA_PRINCIPAL = ["#1a6b3c", "#2d9e6b", "#4cc38a", "#90dbb5", "#d4f0e3"]
COLOR_BASE = PALETA_PRINCIPAL[0]

# Carga de Datos
DATA_URL = "https://raw.githubusercontent.com/figueraandrea25-hub/alcohol-consumption-analysis/refs/heads/main/alcohol_data.csv"
ANIOS_ANALISIS = (2015, 2019)

# Ordenamiento de la Data por regiones 
REGION_MAP = {
    "América Latina y el Caribe": [
        "ATG", "ARG", "BHS", "BRB", "BLZ", "BOL", "BRA", "CHL", "COL", "CRI", "CUB", "DMA",
        "DOM", "ECU", "SLV", "GRD", "GTM", "GUY", "HTI", "HND", "JAM", "MEX", "NIC", "PAN",
        "PRY", "PER", "KNA", "LCA", "VCT", "SUR", "TTO", "URY", "VEN"
    ],
    "América del Norte": ["CAN", "USA"],
    "Asia": [
        "AFG", "BHR", "BGD", "BTN", "BRN", "KHM", "CHN", "COK", "CYP", "PRK", "EGY", "FJI",
        "IND", "IDN", "IRN", "IRQ", "ISR", "JPN", "JOR", "KAZ", "KGZ", "KIR", "KWT", "LAO",
        "LBN", "MYS", "MDV", "MHL", "FSM", "MNG", "MMR", "NRU", "NPL", "NZL", "NIU", "OMN",
        "PAK", "PLW", "PNG", "PHL", "QAT", "KOR", "WSM", "SAU", "SGP", "SLB", "LKA", "SYR",
        "TJK", "THA", "TLS", "TON", "TUR", "TKM", "TUV", "ARE", "UZB", "VUT", "VNM", "YEM"
    ],
    "Europa": [
        "ALB", "AND", "ARM", "AUT", "AZE", "BLR", "BEL", "BIH", "BGR", "HRV", "CZE", "DNK",
        "EST", "FIN", "FRA", "GEO", "DEU", "GRC", "HUN", "ISL", "IRL", "ISR", "ITA", "KAZ",
        "KGZ", "LVA", "LTU", "LUX", "MLT", "MCO", "MNE", "NLD", "MKD", "NOR", "POL", "PRT",
        "MDA", "ROU", "RUS", "SMR", "SRB", "SVK", "SVN", "ESP", "SWE", "CHE", "TJK", "TUR",
        "TKM", "UKR", "GBR", "UZB"
    ],
    "África": [
        "DZA", "AGO", "BEN", "BWA", "BFA", "BDI", "CMR", "CPV", "CAF", "TCD", "COM", "COG",
        "CIV", "COD", "DJI", "EGY", "GNQ", "ERI", "ETH", "GAB", "GMB", "GHA", "GIN", "GNB",
        "KEN", "LSO", "LBR", "LBY", "MDG", "MWI", "MLI", "MRT", "MUS", "MAR", "MOZ", "NAM",
        "NER", "NGA", "RWA", "STP", "SEN", "SYC", "SLE", "SOM", "ZAF", "SSD", "SDN", "SYR",
        "TGO", "TUN", "UGA", "TZA", "ZMB", "ZWE"
    ]
}

REGION_ORDER = [
    "América Latina y el Caribe",
    "América del Norte",
    "Asia",
    "Europa",
    "África"
]

SECCIONES = [
    "Resumen general",
    "Países por región",
    "Comparación entre regiones",
    "Comparación dentro de una región",
    "Ranking de países",
    "Mapa mundial",
    "Explorador de datos"
]

# Funciones para cargar y procesar los datos
 
def asignar_region(iso3: str) -> str:
    """Asigna una región según el orden definido por el usuario."""
    if pd.isna(iso3):
        return "Otras / Sin clasificar"

    for region in REGION_ORDER:
        if iso3 in REGION_MAP[region]:
            return region
    return "Otras / Sin clasificar"

# Carga y ordenamiento de los datos
@st.cache_data
def cargar_y_preparar_datos(url: str) -> pd.DataFrame:
    """Carga la base, normaliza columnas y deja lista la data para el dashboard."""
    df = pd.read_csv(url)

    df.columns = (
        df.columns
        .str.strip()
        .str.upper()
        .str.replace(" ", "_", regex=False)
    )

    columnas_numericas = [
        "YEAR", "ALCOHOL_LITERS_PER_CAPITA", "LOWER_CI", "UPPER_CI", "CI_WIDTH"
    ]
    for col in columnas_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "COUNTRY" in df.columns:
        df["COUNTRY"] = df["COUNTRY"].astype(str).str.strip()

    if "SEX" in df.columns:
        df["SEX"] = df["SEX"].astype(str).str.strip().str.title()

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

        # --- 2. Layout del Dashboard (Títulos Fijos) --
=======
# Definición de las Paletas de Colores
PALETTE_WORLD = ["#1a6b3c", "#2d9e6b", "#4cc38a", "#90dbb5", "#d4f0e3", "#000000"]
PALETTE_COLOURS = ["#1a6b3c", "#e07b39", "#3a7ebf", "#c94040", "#8e44ad"]
PRIMARY_COLOR = PALETTE_COLOURS[0]

DATA_URL = (
    "https://raw.githubusercontent.com/figueraandrea25-hub/alcohol-consumption-analysis/refs/heads/andrea-dev/dataset/alcohol_data.csv"
)
>>>>>>> main
