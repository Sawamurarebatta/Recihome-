import pandas as pd
import streamlit as st
from colores import inyectar_estilos  

# Función para la página principal
def pagina_principal():
    # Inyectar los estilos CSS personalizados
    st.markdown(inyectar_estilos(), unsafe_allow_html=True)  # Asegúrate de ejecutar la función

    # Título de la aplicación
    st.title("Recihome")
    
    # Descripción de la aplicación
    st.write("Una app centrada en la visualización, recolección y reciclaje de residuos en el hogar, "
             "permitiendo monitorear en tiempo real los residuos generados por los hogares en todo el Perú mediante gráficos y promedios de cada vivienda.")
    
    st.write("Usa el menú de la izquierda para navegar entre páginas.")

    # Imagen en la esquina inferior derecha
    st.markdown("""
        <div style="position: fixed; bottom: 10px; right: 10px; z-index: 999;">
            <img src="https://raw.githubusercontent.com/Sawamurarebatta/Recihome-/main/SEGUNDO_PROYECTO/planeta.png" width="150">
        </div>
    """, unsafe_allow_html=True)
