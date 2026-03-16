import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la Página de Streamlit
st.set_page_config(
    page_title="Dashboard de Consumo de Alcohol a nivel mundial",page_icon="🍷",layout="wide")
st.title("🍷 Dashboard de Consumo de Alcohol a nivel mundial"),
st.markdown("Dashboard interactivo para analizar el consumo de alcohol a nivel mundial, con filtros por idioma y visualizaciones dinámicas.")
# Definición de las Paletas de Colores
PALETTE_ALCOHOL_CONSUMPTION = ["#ce7437", "#7f61bc", "#fae208", "#b9baff", "#F0F0F0", "#000000"]
PALETTE_COLOURS = ["#6441a5", "#26C6DA", "#FF1493", "#00FF73", "#FF0000"]
PRIMARY_COLOR = PALETTE_COLOURS[0]


# Carga de Datos
@st.cache_data
def load_and_clean_data(url):
    df = pd.read_csv(url)

    # Normalizar nombres de columnas a mayúsculas y quitar espacios extra
    df.columns = df.columns.str.strip().str.upper().str.replace(' ', '_')

    # *** AJUSTE CLAVE: Normalizar el contenido de la columna LANGUAGE a mayúsculas ***
    if 'LANGUAGE' in df.columns:
        df['LANGUAGE'] = df['LANGUAGE'].str.upper()

    # Lógica de limpieza: buscar columna 'lower_ci' y reemplazar 0.0 por la moda de esa columna
    possible_cols = ['lower_ci', 'lower ci']
    target_col = None

    for col in possible_cols:
        normalized = col.upper().replace(' ', '_')
        if normalized in df.columns:
            target_col = normalized
            break

    if target_col:
        try:
            moda_lower_ci = df[target_col].mode()[0]






            df.loc[df[target_col] == 0.0, target_col] = moda_lower_ci
        except IndexError:
            df.loc[df[target_col] == 0.0, target_col] = 'No data'

    return df


# Función Principal de la Aplicación
def main():
    # Cargar los datos. Si falla, se muestra el error y la app se detiene.
    try:
        data_limpia = load_and_clean_data("https://raw.githubusercontent.com/figueraandrea25-hub/alcohol-consumption-analysis/refs/heads/andrea-dev/15.%20Alcohol%20consumption.csv")
        st.sidebar.success("✅ Datos cargados con éxito.")

    except FileNotFoundError:
        st.error("🔴 Error: Asegúrate de que el archivo 'https://raw.githubusercontent.com/figueraandrea25-hub/alcohol-consumption-analysis/refs/heads/andrea-dev/15.%20Alcohol%20consumption.csv' esté en la misma carpeta que 'app.py'.")
        return
    except Exception as e:
        st.error(f"🔴 Error inesperado durante la carga o limpieza de datos: {e}")
        return

    # --- 1. Generar Sidebar y Filtros ---
    st.sidebar.header("Filtros Globales")

    # Las opciones únicas ya estarán en mayúsculas gracias al cambio en load_and_clean_data
    language_options = data_limpia['LANGUAGE'].unique()

    # Usamos ENGLISH y SPANISH como default, que ahora coincidirán con las opciones.
    default_languages = [lang for lang in ["ENGLISH", "SPANISH"] if lang in language_options]

    selected_language = st.sidebar.multiselect(
        "Seleccionar Idioma(s) para el Análisis Detallado",
        options=language_options,
        default=default_languages
    )

    # Filtro general aplicado al DataFrame
    if selected_language:
        df_filtered_lang = data_limpia[data_limpia['LANGUAGE'].isin(selected_language)]
    else:
        df_filtered_lang = pd.DataFrame()

        # --- 2. Layout del Dashboard (Títulos Fijos) ---
    st.title("📊 Análisis Comparativo del Consumo de Alcohol a nivel mundial")
    st.markdown("---")

