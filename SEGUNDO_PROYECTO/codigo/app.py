import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from pag_principal import pagina_principal
from distribucion_general import distribucion_general, grafico_lineal_por_periodo
from filtros_avanzados import filtros_avanzados
from mapa import dashboard_residuos
from colores import colores  # Importar el diccionario de colores
from description import descripcion_app  # Asegúrate de que description.py exista y sea accesible

# Configurar la página
st.set_page_config(layout="wide", page_title="ReciHome", page_icon="♻️")

# Aplicar el fondo principal y cambiar el color de las palabras a blanco
st.markdown(f"""
    <style>
        .stApp {{
            background-color: {colores['fondo_principal']};
            color: white;  /* Color blanco para el texto */
        }}
        .css-1d391kg, .css-1v3fvcr {{  /* Selector CSS para los textos */
            color: white !important;  /* Forzar el color blanco */
        }}
        .css-16huue1 a {{
            color: white !important;  /* Color blanco para enlaces */
        }}
    </style>
    """, unsafe_allow_html=True)

# Cargar datos
url = "https://raw.githubusercontent.com/Sawamurarebatta/Recihome-/main/SEGUNDO_PROYECTO/archivos/residuos.csv"
try:
    archivo_cargado = pd.read_csv(url, sep=';', encoding='latin1')
except Exception as e:
    archivo_cargado = None
    st.error(f"Error al cargar los datos: {e}")

# Crear el menú horizontal
selected = option_menu(
    menu_title="",
    options=["Página principal", "Descripción", "Distribución general", "Resumen", "Filtros Avanzados"],
    icons=["house", "clipboard", "bar-chart", "map", "filter"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "5px", "background-color": colores['fondo_principal']},
        "icon": {"color": colores['encabezado'], "font-size": "20px"},
        "nav-link": {
            "font-size": "14px",
            "margin": "5px",
            "text-align": "center",
            "color": "white",
            "--hover-color": colores['fondo_sidebar']
        },
        "nav-link-selected": {
            "background-color": "#1cc130 ",
            "font-weight": "bold",
            "color": "white",
        },
    }
)

# Mostrar contenido según la opción seleccionada
if selected == "Página principal":
    pagina_principal()

elif selected == "Distribución general":
    if archivo_cargado is not None:
        st.title("Distribución general")
        distribucion_general(archivo_cargado)
        grafico_lineal_por_periodo(archivo_cargado)
    else:
        st.error("No se pudieron cargar los datos para 'Distribución general'.")

elif selected == "Resumen":
    if archivo_cargado is not None:
        dashboard_residuos(archivo_cargado)
    else:
        st.error("No se pudieron cargar los datos para 'Resumen'.")

elif selected == "Descripción":
    descripcion_app()  # Llamar a la función desde description.py

elif selected == "Filtros Avanzados":
    if archivo_cargado is not None:
        filtros_avanzados(archivo_cargado)
    else:
        st.error("No se pudieron cargar los datos para 'Filtros Avanzados'.")


