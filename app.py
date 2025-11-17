import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================
# CONFIGURACIÓN GENERAL
# ============================================
st.set_page_config(
    page_title="Toyota Dashboard",
    page_icon="🚗",
    layout="wide"
)

st.markdown("""
    <style>
        .kpi-card {
            padding: 20px;
            border-radius: 15px;
            background-color: #f5f7fa;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
            text-align: center;
            border: 1px solid #e0e0e0;
        }
        .kpi-number {
            font-size: 40px;
            font-weight: 700;
            color: #1f77b4;
        }
        .section-title {
            font-size: 28px !important;
            font-weight: 800 !important;
            margin-top: 25px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🚗 **Dashboard Analítico – Toyota Colombia**")
st.write("Exploración interactiva y profesional del dataset `toyota.csv`")

# ============================================
# CARGA Y LIMPIEZA DEL DATASET
# ============================================
df = pd.read_csv("toyota.csv")

# Renombrar columnas a estándar español si existen
df = df.rename(columns={
    "model": "modelo",
    "year": "año",
    "price": "valor",
    "transmission": "transmisión",
    "mileage": "kilometraje",
    "fuelType": "combustible",
    "engineSize": "motor"
})

# --- LIMPIEZA DEL PRECIO ---
df["valor"] = (
    df["valor"]
    .astype(str)
    .str.replace(".", "", regex=False)
)
df["valor"] = pd.to_numeric(df["valor"], errors="coerce")

# Detectar tipos de columnas
num_cols = df.select_dtypes(include=["number"]).columns.tolist()
cat_cols = df.select_dtypes(exclude=["number"]).columns.tolist()

# ============================================
# SIDEBAR – FILTROS
# ============================================
st.sidebar.title("🔍 Filtros")

# Filtro por modelo
if "modelo" in df.columns:
    modelo_sel = st.sidebar.multiselect(
        "Modelo",
        df["modelo"].unique(),
        default=df["modelo"].unique()
    )
    df = df[df["modelo"].isin(modelo_sel)]

# Filtro por combustible
if "combustible" in df.columns:
    fuel_sel = st.sidebar.multiselect(
        "Tipo de Combustible",
        df["combustible"].unique(),
        default=df["combustible"].unique()
    )
    df = df[df["combustible"].isin(fuel_sel)]

# Filtro por rango de precios
if "valor" in df.columns:
    min_v, max_v = int(df["valor"].min()), int(df["valor"].max())
    val_range = st.sidebar.slider(
        "Rango de Precios",
        min_v, max_v,
        (min_v, max_v)
    )
    df = df[df["valor"].between(val_range[0], val_range[1])]

# ============================================
# KPI – MÉTRICAS CLAVE
# ============================================
st.markdown("<div class='section-title'>📌 Indicadores Generales</div>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
        <div class='kpi-card'>
            <h4>Total de Vehículos</h4>
            <div class='kpi-number'>{df.shape[0]}</div>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
        <div class='kpi-card'>
            <h4>Precio Promedio</h4>
            <div class='kpi-number'>${int(df['valor'].mean()):,}</div>
        </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
        <div class='kpi-card'>
            <h4>Precio Mínimo</h4>
            <div class='kpi-number'>${int(df['valor'].min()):,}</div>
        </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
        <div class='kpi-card'>
            <h4>Precio Máximo</h4>
            <div class='kpi-number'>${int(df['valor'].max()):,}</div>
        </div>
    """, unsafe_allow_html=True)

# ============================================
# ANÁLISIS GENERAL
# ============================================
st.markdown("<div class='section-title'>📝 Análisis General del Mercado Toyota</div>", unsafe_allow_html=True)

st.info("""
El mercado de vehículos Toyota presenta variaciones importantes según el modelo, 
el tipo de combustible y el rango de precios. Este dashboard permite identificar 
cómo se distribuyen los precios, cuáles son los modelos más comunes y qué tipo 
de combustible predomina en la oferta disponible.
""")

# ============================================
# GRÁFICAS
# ============================================
st.markdown("<div class='section-title'>📊 Visualizaciones</div>", unsafe_allow_html=True)

g1, g2 = st.columns(2)

# Pie chart por combustible
with g1:
    if "combustible" in df.columns:
        pie = px.pie(
            df,
            names="combustible",
            title="Distribución por Combustible",
            hole=0.4
        )
        st.plotly_chart(pie, use_container_width=True)

# Bar chart precio promedio por modelo
with g2:
    if "modelo" in df.columns:
        bar = px.bar(
            df.groupby("modelo")["valor"].mean().reset_index(),
            x="modelo",
            y="valor",
            title="Precio Promedio por Modelo",
            text_auto=True
        )
        st.plotly_chart(bar, use_container_width=True)

# ============================================
# HISTOGRAMA DE PRECIOS
# ============================================
st.markdown("<div class='section-title'>💰 Distribución de Precios</div>", unsafe_allow_html=True)

hist = px.histogram(
    df,
    x="valor",
    nbins=20,
    title="Histograma de Precios",
    labels={"valor": "Precio"}
)
st.plotly_chart(hist, use_container_width=True)

# ============================================
# LINE CHART – Variables numéricas
# ============================================
if len(num_cols) >= 2:
    st.markdown("<div class='section-title'>📈 Tendencias Numéricas</div>", unsafe_allow_html=True)
    st.line_chart(df[num_cols])

# ============================================
# TABLA DE DATOS
# ============================================
st.markdown("<div class='section-title'>📄 Datos Filtrados</div>", unsafe_allow_html=True)
st.dataframe(df, use_container_width=True)
