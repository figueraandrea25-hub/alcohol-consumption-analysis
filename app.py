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
def cargar_datos():
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
def asignar_region(iso3):
    iso3 = str(iso3).strip().upper()
    for region, codes in REGIONS.items():
        if iso3 in codes:
            return region
    return "Otras/Oceanía"

# Limpieza de datos, filtrando años, sexo, convirtiendo columnas numericas y calculando incertidumbre 
def limpiar_datos(df):
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
    df["REGION"] = df["ISO3"].apply(asignar_region)
    return df.dropna(subset=["ALCOHOL_LITERS_PER_CAPITA"])

# Grafica de data sucia vs limpia ( Simulando valores faltantes para comparar el efecto de la limpieza )
def crear_versiones_sucias(df):
    dirty = df.copy()
    dirty.loc[dirty.sample(frac=0.10, random_state=123).index, "ALCOHOL_LITERS_PER_CAPITA"] = pd.NA
    recovered = dirty.dropna(subset=["ALCOHOL_LITERS_PER_CAPITA"]).copy()
    return dirty, recovered

# Resumen de datos por región y año, calculando el promedio y la incertidumbre media
def resumen_regiones(df):
    summary = df.groupby("REGION", as_index=False).agg(
        Promedio=("ALCOHOL_LITERS_PER_CAPITA", "mean"),
        Mediana=("ALCOHOL_LITERS_PER_CAPITA", "median"),
        Desv_Est=("ALCOHOL_LITERS_PER_CAPITA", "std"),
        Incertidumbre=("CI_WIDTH", "mean"),
        Paises=("COUNTRY", "nunique"),
    )
    summary["REGION"] = pd.Categorical(summary["REGION"], categories=REGION_ORDER, ordered=True)
    return summary.sort_values("REGION")

# Formato basico para graficos, unificando colores y estilos
def style(fig, height=430):
    fig.update_layout(template="plotly_white", height=height, margin=dict(l=20, r=20, t=60, b=20), legend_title_text="")
    return fig

# Calculo de intervalos de confianza por macro-region
def macro_region_ci(df):
    ci = df.groupby("REGION", as_index=False).agg(
        media=("ALCOHOL_LITERS_PER_CAPITA", "mean"),
        sd=("ALCOHOL_LITERS_PER_CAPITA", "std"),
        n=("ALCOHOL_LITERS_PER_CAPITA", "count")
    )
    ci["se"] = ci["sd"] / (ci["n"] ** 0.5)
    ci["li"] = ci["media"] - 1.96 * ci["se"]
    ci["ls"] = ci["media"] + 1.96 * ci["se"]
    return ci.sort_values("media")

# Encabezado del dashboard 
st.title("Dashboard de Consumo de Alcohol (2015–2019)")
st.caption("Analisis de datos critico sobre la incertidumbre como una variable fundamental para ser presentada a la sociedad.")

# Carga final de la base para analizar

try:
    df = limpiar_datos(cargar_datos())
except Exception as e:
    st.error("No fue posible cargar la base de datos.")
    st.error(f"Detalle: {e}")
    st.stop()

# Versión sucia vs limpia para mostrar el impacto de la limpieza de datos
dirty, recovered = crear_versiones_sucias(df)

# Filtros generales para el dashboard
st.sidebar.header("Filtros")
year_range = st.sidebar.slider("Años", 2015, 2019, YEARS)
selected_regions = st.sidebar.multiselect("Regiones", REGION_ORDER, default=REGION_ORDER)

df = df[df["YEAR"].between(*year_range) & df["REGION"].isin(selected_regions)]
dirty = dirty[dirty["YEAR"].between(*year_range) & dirty["REGION"].isin(selected_regions)]
recovered = recovered[recovered["YEAR"].between(*year_range) & recovered["REGION"].isin(selected_regions)]

if df.empty:
    st.warning("No hay datos para los filtros seleccionados.")
    st.stop()

# Metricas de la muestra filtrada 
m1, m2, m3, m4 = st.columns(4)
m1.metric("Registros", f"{len(df):,}")
m2.metric("Países", df["COUNTRY"].nunique())
m3.metric("Promedio global", f"{df['ALCOHOL_LITERS_PER_CAPITA'].mean():.2f}")
m4.metric("Mediana global", f"{df['ALCOHOL_LITERS_PER_CAPITA'].median():.2f}")

# Organizacion pestañas Dashboard
tabs = st.tabs([
    "Resumen general", "Data sucia vs limpia", "Mediana", "Estadísticas regionales",
    "Dos países", "Intervalos por región", "Asimetría regional",
    "Macro-regiones IC 95%", "Top 10 países", "Consumo por año"
])

# Pestaña resumen general con tabla y grafico 
with tabs[0]:
    st.subheader("Panorama general")
    rs = resumen_regiones(df)
    fig = px.bar(rs, x="REGION", y="Promedio", color="REGION", color_discrete_map=REGION_COLORS, text_auto=".2f", title="Promedio de consumo por región")
    fig.update_layout(showlegend=False)
    st.plotly_chart(style(fig), use_container_width=True)
    st.dataframe(rs.style.format({"Promedio": "{:.2f}", "Mediana": "{:.2f}", "Desv_Est": "{:.2f}", "Incertidumbre": "{:.2f}"}), use_container_width=True)

# Pestaña Data sucia vs limpia (Tabla y grafico)
with tabs[1]:
    st.subheader("Comparación de data sucia vs limpia")
    comparison = pd.DataFrame({
        "Estado": ["Limpia", "Sucia", "Recuperada"],
        "Registros": [len(df), len(dirty), len(recovered)],
        "Media": [df["ALCOHOL_LITERS_PER_CAPITA"].mean(), dirty["ALCOHOL_LITERS_PER_CAPITA"].mean(skipna=True), recovered["ALCOHOL_LITERS_PER_CAPITA"].mean()],
        "Mediana": [df["ALCOHOL_LITERS_PER_CAPITA"].median(), dirty["ALCOHOL_LITERS_PER_CAPITA"].median(skipna=True), recovered["ALCOHOL_LITERS_PER_CAPITA"].median()]
    })
    st.dataframe(comparison.style.format({"Media": "{:.2f}", "Mediana": "{:.2f}"}), use_container_width=True)
    fig = px.bar(comparison.melt(id_vars="Estado", value_vars=["Media", "Mediana"], var_name="Indicador", value_name="Valor"),
                 x="Estado", y="Valor", color="Indicador", barmode="group", title="Comparación de media y mediana")
    st.plotly_chart(style(fig), use_container_width=True)

# Analisis de media y mediana con el fin de evaluar la robustez del estimador centra por region 
with tabs[2]:
    st.subheader("Contraste entre media y mediana")
    med = resumen_regiones(df)[["REGION", "Promedio", "Mediana"]].copy()
    med["Sesgo_%"] = ((med["Promedio"] - med["Mediana"]) / med["Mediana"]) * 100
    fig = px.bar(med.melt(id_vars="REGION", value_vars=["Promedio", "Mediana"], var_name="Medida", value_name="Valor"),
                 x="REGION", y="Valor", color="Medida", barmode="group", title="Promedio vs mediana por región")
    st.plotly_chart(style(fig), use_container_width=True)
    st.dataframe(med.style.format({"Promedio": "{:.2f}", "Mediana": "{:.2f}", "Sesgo_%": "{:.2f}"}), use_container_width=True)

# Graficos de promedio, mediana, desviacion estandar e incertidumbre ( Estadisticas regionales)
with tabs[3]:
    st.subheader("Estadísticas por región")
    rs = resumen_regiones(df)
    c1, c2 = st.columns(2)
    c3, c4 = st.columns(2)
    with c1:
        fig = px.bar(rs, x="REGION", y="Promedio", color="REGION", color_discrete_map=REGION_COLORS, title="Promedio")
        fig.update_layout(showlegend=False)
        st.plotly_chart(style(fig, 350), use_container_width=True)
    with c2:
        fig = px.bar(rs, x="REGION", y="Mediana", color="REGION", color_discrete_map=REGION_COLORS, title="Mediana")
        fig.update_layout(showlegend=False)
        st.plotly_chart(style(fig, 350), use_container_width=True)
    with c3:
        fig = px.bar(rs, x="REGION", y="Desv_Est", color="REGION", color_discrete_map=REGION_COLORS, title="Desviación estándar")
        fig.update_layout(showlegend=False)
        st.plotly_chart(style(fig, 350), use_container_width=True)
    with c4:
        fig = px.bar(rs, x="REGION", y="Incertidumbre", color="REGION", color_discrete_map=REGION_COLORS, title="Incertidumbre")
        fig.update_layout(showlegend=False)
        st.plotly_chart(style(fig, 350), use_container_width=True)

    # Tablas y graficos de comparacion entre paises
    with tabs[4]:
        st.subheader("Comparación entre dos países de la misma región")
        region = st.selectbox("Región", selected_regions, key="two_region")
        countries = sorted(df.loc[df["REGION"] == region, "COUNTRY"].unique())
        if len(countries) >= 2:
            c1, c2 = st.columns(2)
            with c1:
                country_a = st.selectbox("País A", countries, key="a")
            with c2:
                country_b = st.selectbox("País B", countries, index=1, key="b")
            comp = df[df["COUNTRY"].isin([country_a, country_b])].copy()
            yearly = comp.groupby(["COUNTRY", "YEAR"], as_index=False)["ALCOHOL_LITERS_PER_CAPITA"].mean()
            fig = px.line(yearly, x="YEAR", y="ALCOHOL_LITERS_PER_CAPITA", color="COUNTRY", markers=True, title=f"Evolución temporal: {country_a} vs {country_b}")
            st.plotly_chart(style(fig), use_container_width=True)
            intervals = comp.groupby("COUNTRY", as_index=False).agg(Media=("ALCOHOL_LITERS_PER_CAPITA", "mean"), LI=("LOWER_CI", "mean"), LS=("UPPER_CI", "mean"))
            st.dataframe(intervals.style.format({"Media": "{:.2f}", "LI": "{:.2f}", "LS": "{:.2f}"}), use_container_width=True)
        else:
            st.warning("No hay suficientes países en esa región.")
    
    # Tabla/ Grafico de intervalos de confianza por pais
    with tabs[5]:
        st.subheader("Intervalos de confianza por país dentro de una región")
        region = st.selectbox("Selecciona región", selected_regions, key="int_region")
        country_int = df[df["REGION"] == region].groupby("COUNTRY", as_index=False).agg(
            Media=("ALCOHOL_LITERS_PER_CAPITA", "mean"),
            LI=("LOWER_CI", "mean"),
            LS=("UPPER_CI", "mean"),
            Incertidumbre=("CI_WIDTH", "mean")
        ).sort_values("Media", ascending=False)
        fig = px.scatter(country_int, x="Media", y="COUNTRY", error_x="Incertidumbre", color="Media", color_continuous_scale="RdBu_r",
                         title=f"Consumo e incertidumbre por país - {region}")
        st.plotly_chart(style(fig, max(420, len(country_int) * 28 + 140)), use_container_width=True)
        st.dataframe(country_int.style.format({"Media": "{:.2f}", "LI": "{:.2f}", "LS": "{:.2f}", "Incertidumbre": "{:.2f}"}), use_container_width=True)
    
    # Analisis de asimetría regional ( Histrograma con media y mediana para estudiar la distribucion)
    with tabs[6]:
        st.subheader("Análisis de asimetría regional")
        chosen = [r for r in selected_regions if r in df["REGION"].unique()]
        if chosen:
            region_plot = st.selectbox("Región para ver distribución", chosen, key="skew_region")
            vals = df[df["REGION"] == region_plot].copy()
            fig = px.histogram(vals, x="ALCOHOL_LITERS_PER_CAPITA", nbins=20, title=f"Distribución del consumo - {region_plot}",
                               color_discrete_sequence=["#B04A45"])
            fig.add_vline(x=vals["ALCOHOL_LITERS_PER_CAPITA"].mean(), line_dash="dash", line_color="blue")
            fig.add_vline(x=vals["ALCOHOL_LITERS_PER_CAPITA"].median(), line_color="red")
            st.plotly_chart(style(fig), use_container_width=True)
            st.caption("Línea azul punteada = media. Línea roja = mediana.")
        else:
            st.warning("No hay regiones disponibles.")
    
    # Tabla y grafico sobre intervalos de confianza por macro-región
    with tabs[7]:
        st.subheader("Consumo por macro-región con IC 95%")
        ci = macro_region_ci(df)
        ci["Error_95"] = ci["ls"] - ci["media"]
        fig = px.scatter(ci, x="media", y="REGION", error_x="Error_95", color="media", color_continuous_scale="RdBu_r",
                         text=ci["media"].round(2), title="Media regional e intervalo de confianza 95%")
        st.plotly_chart(style(fig, 540), use_container_width=True)
        st.dataframe(ci.style.format({"media": "{:.2f}", "sd": "{:.2f}", "se": "{:.2f}", "li": "{:.2f}", "ls": "{:.2f}"}), use_container_width=True)
    
    # Creacion ranking de paises con mayor consumo (top 10)
    with tabs[8]:
        st.subheader("Top 10 países con mayor consumo")
        top10 = df.groupby("COUNTRY", as_index=False)["ALCOHOL_LITERS_PER_CAPITA"].mean().sort_values("ALCOHOL_LITERS_PER_CAPITA", ascending=False).head(10)
        fig = px.bar(top10, x="ALCOHOL_LITERS_PER_CAPITA", y="COUNTRY", orientation="h", color="ALCOHOL_LITERS_PER_CAPITA",
                     color_continuous_scale="Reds", text_auto=".2f", title="Top 10 países con mayor consumo")
        st.plotly_chart(style(fig), use_container_width=True)
        st.dataframe(top10.style.format({"ALCOHOL_LITERS_PER_CAPITA": "{:.2f}"}), use_container_width=True)
    
    # Linea evolucion temporal del consumo por año a nivel global   
    with tabs[9]:
        st.subheader("Consumo promedio por año")
        years_df = df.groupby("YEAR", as_index=False)["ALCOHOL_LITERS_PER_CAPITA"].mean()
        fig = px.line(years_df, x="YEAR", y="ALCOHOL_LITERS_PER_CAPITA", markers=True, title="Promedio global por año")
        fig.update_xaxes(dtick=1, tickformat="d")
        st.plotly_chart(style(fig), use_container_width=True)
        region_year = df.groupby(["REGION", "YEAR"], as_index=False)["ALCOHOL_LITERS_PER_CAPITA"].mean()
        fig2 = px.line(region_year, x="YEAR", y="ALCOHOL_LITERS_PER_CAPITA", color="REGION", color_discrete_map=REGION_COLORS,
                       markers=True, title="Comparación regional por año")
        fig2.update_xaxes(dtick=1, tickformat="d"
        st.plotly_chart(style(fig2, 450), use_container_width=True)