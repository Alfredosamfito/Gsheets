import streamlit as st
import pandas as pd

# Configuración inicial de Streamlit
st.set_page_config(
    page_title="Buscador de Códigos",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="expanded"
)

# URL del archivo de Google Sheets
gsheetid = '16iIKA3O-7RyyMyN-uQuGy1vpA9eQ1KkReeq97ISy_Jw'
sheetid = '0'
url = f'https://docs.google.com/spreadsheets/d/{gsheetid}/export?format=csv&gid={sheetid}'

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

# Cargar datos
dfDatos = load_data(url)

# Función para generar URL de código de barras
def generar_codigo_barras_url(codigo):
    return f"https://bwipjs-api.metafloor.com/?bcid=code128&text={codigo}&scale=3&includetext"

st.title("Buscador de :blue[Códigos]")

# Mostrar título de la tercera columna
if dfDatos.shape[1] >= 3:
    tercera_columna = dfDatos.columns[2]
    st.info(f"Maestro de Origen: _*:red[{tercera_columna}]*_")
else:
    st.warning("El DataFrame tiene menos de 3 columnas.")

# Campo de entrada para buscar por descripción
search_term = st.text_input("Ingrese Descripción de Artículo:")

if search_term:
    # Filtrar resultados
    filtered_df = dfDatos[dfDatos["Descripción"].str.contains(search_term, case=False, na=False)]

    if not filtered_df.empty:
        st.write("Códigos encontrados:")
        filtered_df["Codigo"] = filtered_df["Codigo"].apply(
            lambda x: int(float(x)) if isinstance(x, (float, str)) and x.isnumeric() else x
        )
        st.dataframe(filtered_df[["Codigo", "Descripción"]].reset_index(drop=True))

        # Mostrar código de barras para cada resultado
        for codigo in filtered_df["Codigo"]:
            st.write(f"Código de barras para: {codigo}")
            barcode_url = generar_codigo_barras_url(str(codigo))
            st.image(barcode_url, caption=f"Código: {codigo}")
    else:
        st.write("No se encontraron resultados.")
else:
    st.write("Introduce un término para buscar.")

st.divider()

# Campo de entrada para buscar por código
search_term2 = st.text_input("Ingrese Código del Artículo:")

if search_term2:
    filtered_df = dfDatos[dfDatos["Codigo"].astype(str).str.contains(search_term2, case=False, na=False)]

    if not filtered_df.empty:
        st.write("Códigos encontrados:")
        filtered_df["Codigo"] = filtered_df["Codigo"].apply(
            lambda x: int(float(x)) if isinstance(x, (float, str)) and x.isnumeric() else x
        )
        st.dataframe(filtered_df[["Codigo", "Descripción"]].reset_index(drop=True))

        for codigo in filtered_df["Codigo"]:
            st.write(f"Código de barras para: {codigo}")
            barcode_url = generar_codigo_barras_url(str(codigo))
            st.image(barcode_url, caption=f"Código: {codigo}")
    else:
        st.write("No se encontraron resultados.")
else:
    st.write("Introduce un término para buscar.")

st.divider()

# Footer
footer_html = """<div style='text-align: center;'>
  <p>Creado por Alfredo Rubilar. 🧑🏻‍💻</p>
</div>"""
st.markdown(footer_html, unsafe_allow_html=True)
