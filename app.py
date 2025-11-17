import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================
# CONFIGURACIÓN
# ==========================
st.set_page_config(
    page_title="Toyota Dashboard",
    page_icon="🚗",
    layout="wide"
)

st.markdown("""
    <style>
        .big-metric {
            font-size: 38px;
            font-weight: 700;
            color: #1f77b4;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🚗 **Dashboard de Carros Toyota**")
st.write("Análisis interactivo basado en tu dataset *toyota.csv*")

# ==========================
# CARGA DEL DATASET
# ==========================
df = pd.read_csv("toyota.csv")

# Detección automática
num_cols = df.select_dtypes(include="number").columns.tolist()
cat_cols = df.select_dtypes(exclude="number").columns.tolist()

# ==========================
# SIDEBAR (FILTROS)
# ==========================
st.sidebar.header("🔎 Filtros del Dashboard")

# FILTRO POR MODELO
if "modelo" in df.columns:
    modelo_sel = st.sidebar.multiselect(
        "Modelo:",
        options=df["modelo"].unique(),
        default=df["modelo"].unique()
    )
    df = df[df["modelo"].isin(modelo_sel)]

# FILTRO POR COMBUSTIBLE (gasolina, diesel, híbrido...)
for col in cat_cols:
    if any(x in col.lower() for x in ["combustible", "fuel", "tipo"]):
        combustible_col = col
        combustible_sel = st.sidebar.multiselect(
            "Tipo de combustible:", 
            df[col].unique(), 
            df[col].unique()
        )
        df = df[df[col].isin(combustible_sel)]

# FILTRO POR RANGO DE VALOR (si existe)
if "valor" in df.columns:
    min_v, max_v = int(df["valor"].min()), int(df["valor"].max())
    valor_range = st.sidebar.slider("Rango de precio:", min_v, max_v, (min_v, max_v))
    df = df[(df["valor"] >= valor_range[0]) & (df["valor"] <= valor_range[1])]

# ==========================
# MÉTRICAS (KPI CARDS)
# ==========================

st.subheader("📌 **Resumen general**")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Total de Carros**")
    st.markdown(f"<div class='big-metric'>{df.shape[0]}</div>", unsafe_allow_html=True)

with col2:
    if "valor" in df.columns:
        precio_prom = int(df["valor"].mean())
        st.markdown("**Precio promedio**")
        st.markdown(f"<div class='big-metric'>${precio_prom:,}</div>", unsafe_allow_html=True)

with col3:
    if "valor" in df.columns:
        maximo = int(df["valor"].max())
        st.markdown("**Precio máximo**")
        st.markdown(f"<div class='big-metric'>${maximo:,}</div>", unsafe_allow_html=True)

# ==========================
# TABLA DINÁMICA
# ==========================

st.subheader("📄 **Datos filtrados**")
st.dataframe(df, use_container_width=True)

# ==========================
# GRÁFICAS
# ==========================

st.subheader("📊 **Visualizaciones**")
graf1, graf2 = st.columns(2)

# PIE CHART – Distribución por combustible
with graf1:
    if "combustible" in df.columns:
        pie = px.pie(
            df,
            names="combustible",
            title="Distribución por tipo de combustible",
            hole=0.45
        )
        st.plotly_chart(pie, use_container_width=True)

# BAR CHART – Promedio de precios por modelo
with graf2:
    if "modelo" in df.columns and "valor" in df.columns:
        bar = px.bar(
            df.groupby("modelo")["valor"].mean().reset_index(),
            x="modelo",
            y="valor",
            title="Precio promedio por modelo",
            text_auto=True
        )
        st.plotly_chart(bar, use_container_width=True)

# LINE CHART – Tendencia numérica (si aplica)
if len(num_cols) > 1:
    st.subheader("📈 **Tendencias de variables numéricas**")
    st.line_chart(df[num_cols])
