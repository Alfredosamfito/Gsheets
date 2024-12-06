import streamlit as st
import barcode
import pandas as pd
from barcode.codex import Code128
from barcode.writer import ImageWriter
from io import BytesIO

# Definimos los parámetros de configuración de la aplicación
st.set_page_config(
    page_title="Buscador de Códigos",  # Título de la página
    page_icon="🔍",  # Ícono
    layout="centered",  # Forma de layout ancho o compacto
    initial_sidebar_state="expanded"  # Definimos si el sidebar aparece expandido o colapsado
)
gsheetid = '16iIKA3O-7RyyMyN-uQuGy1vpA9eQ1KkReeq97ISy_Jw'
sheetid = '0'
url = f'https://docs.google.com/spreadsheets/d/{gsheetid}/export?format=csv&gid={sheetid}&format'

@st.cache_data
def load_data(url):
    return pd.read_csv(url)
# Cargar datos desde Google Sheets
dfDatos = load_data(url)

# Función para generar código de barras
def generar_codigo_barras(codigo):
    buffer = BytesIO()
    Code128(codigo, writer=ImageWriter()).write(buffer)
    buffer.seek(0)
    return buffer

dfDatos = pd.read_csv(url)
st.title("Buscador de :blue[Códigos]")

# Mostrar título de la tercera columna
if dfDatos.shape[1] >= 3:  # Verifica si hay al menos 3 columnas
    tercera_columna = dfDatos.columns[2]  # Obtiene el nombre de la tercera columna
    st.info(f"Maestro de Origen: _*:red[{tercera_columna}]*_")
else:
    st.warning("El DataFrame tiene menos de 3 columnas.")



# Campo de entrada para buscar en la columna "Descripción"
search_term = st.text_input("Ingrese Descripción de Artículo:")

if search_term:
    # Filtrar los resultados basados en la columna "Descripción"
    filtered_df = dfDatos[dfDatos["Descripción"].str.contains(search_term, case=False, na=False)]

    if not filtered_df.empty:
        # Mostrar los valores filtrados
        st.write("Códigos encontrados:")
        filtered_df["Codigo"] = filtered_df["Codigo"].apply(lambda x: int(float(x)) if isinstance(x, (float, str)) and x.isnumeric() else x)
        st.dataframe(filtered_df[["Codigo", "Descripción"]].reset_index(drop=True))

        # Generar y mostrar un código de barras para cada resultado
        for codigo in filtered_df["Codigo"]:
            st.write(f"Código de barras para: {codigo}")
            barcode_image = generar_codigo_barras(str(codigo))
            st.image(barcode_image, caption=f"Código: {codigo}")
    else:
        st.write("No se encontraron resultados.")
else:
    st.write("Introduce un término para buscar.")


st.divider()

search_term2= st.text_input("Increse Código del Artículo:")

if search_term2:
    # Filtrar los resultados basados en la columna "Descripción"
    filtered_df = dfDatos[dfDatos["Codigo"].str.contains(search_term2, case=False, na=False)]

    if not filtered_df.empty:
        # Mostrar los valores filtrados
        st.write("Códigos encontrados:")
        filtered_df["Codigo"] = filtered_df["Codigo"].apply(lambda x: int(float(x)) if isinstance(x, (float, str)) and x.isnumeric() else x)
        st.dataframe(filtered_df[["Codigo", "Descripción"]].reset_index(drop=True))

        # Generar y mostrar un código de barras para cada resultado
        for codigo in filtered_df["Codigo"]:
            st.write(f"Código de barras para: {codigo}")
            barcode_image = generar_codigo_barras(str(codigo))
            st.image(barcode_image, caption=f"Código: {codigo}")
    else:
        st.write("No se encontraron resultados.")
else:
    st.write("Introduce un término para buscar.")


st.divider()

footer_html = """<div style='text-align: center;'>
  <p>Creado por Alfredo Rubilar. 🧑🏻‍💻</p>
</div>"""
st.markdown(footer_html, unsafe_allow_html=True)
