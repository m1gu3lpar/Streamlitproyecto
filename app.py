import streamlit as st
import pandas as pd

# ==========================
# CONFIGURACIÓN INICIAL
# ==========================
st.set_page_config(
    page_title="Analizador de Carros Toyota",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Analizador de carros **Toyota**")
st.write("Dashboard interactivo basado en tu archivo *toyota.csv*")

# ==========================
# CARGA DEL DATASET
# ==========================
df = pd.read_csv("toyota.csv")

st.sidebar.header("🔎 Filtros")

# Detectar columnas numéricas y categóricas automáticamente
num_cols = df.select_dtypes(include="number").columns.tolist()
cat_cols = df.select_dtypes(exclude="number").columns.tolist()

# Filtro dinámico por columna categórica (si existe)
if len(cat_cols) > 0:
    cat_col = st.sidebar.selectbox("Categoría para filtrar:", cat_cols)
    cat_value = st.sidebar.selectbox("Valor:", df[cat_col].unique())
    df_filtrado = df[df[cat_col] == cat_value]
else:
    df_filtrado = df

# ==========================
# MOSTRAR DATAFRAME
# ==========================
st.subheader("📄 Datos filtrados")
st.dataframe(df_filtrado, use_container_width=True)

# ==========================
# GRÁFICOS
# ==========================

st.subheader("📊 Gráficos")

col1, col2 = st.columns(2)

# Gráfico de barras
with col1:
    st.write("### 📌 Distribución numérica")
    if len(num_cols) > 0:
        st.bar_chart(df_filtrado[num_cols])
    else:
        st.write("No hay columnas numéricas para graficar.")

# Gráfico de líneas
with col2:
    st.write("### 📈 Tendencia general")
    if len(num_cols) > 0:
        st.line_chart(df_filtrado[num_cols])
    else:
        st.write("No se puede generar la gráfica de líneas.")

