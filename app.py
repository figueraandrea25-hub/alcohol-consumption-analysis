import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(
    page_title="Dashboard Consumo de Alcohol en el Mundo (2000-2022)",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Definición de las Paletas de Colores
PALETTE_WORLD = ["#1a6b3c", "#2d9e6b", "#4cc38a", "#90dbb5", "#d4f0e3", "#000000"]
PALETTE_COLOURS = ["#1a6b3c", "#e07b39", "#3a7ebf", "#c94040", "#8e44ad"]
PRIMARY_COLOR = PALETTE_COLOURS[0]

DATA_URL = (
    "https://raw.githubusercontent.com/figueraandrea25-hub/alcohol-consumption-analysis/refs/heads/andrea-dev/dataset/alcohol_data.csv"
)