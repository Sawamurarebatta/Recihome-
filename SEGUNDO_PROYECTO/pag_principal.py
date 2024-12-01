import pandas as pd
import streamlit as st

# Función para la página principal
def pagina_principal():
    # URL del GIF de fondo
    gif_url = "https://github.com/Sawamurarebatta/Recihome-/blob/main/SEGUNDO_PROYECTO/appl.gif?raw=true"
    # URL del logotipo
    logo_url = "https://github.com/Sawamurarebatta/Recihome-/blob/main/SEGUNDO_PROYECTO/logo.png?raw=true"

    # Título con logotipo
    st.markdown(f"""
        <style>
            .stApp {{
                background-image: url("{gif_url}");
                background-repeat: no-repeat;
                background-size: cover;
                background-position: center;
                height: 100vh;
                color: white; /* Cambia el color de texto para hacerlo visible sobre el GIF */
            }}
            .logo {{
                display: flex;
                justify-content: center;
                align-items: center;
                margin-bottom: 20px;
            }}
            .logo img {{
                width: 200px; /* Ajusta el tamaño del logo */
            }}
            p {{
                font-size: 20px;
                text-align: justify;
                font-family: 'Arial', sans-serif;
            }}
        </style>
        <div class="logo">
            <img src="{logo_url}" alt="Recihome Logo">
        </div>
        <p>
            Una app centrada en la visualización, recolección y reciclaje de residuos en el hogar, 
            permitiendo monitorear en tiempo real los residuos generados por los hogares en todo el Perú mediante gráficos y promedios de cada vivienda.
        </p>
        <p style="font-size: 18px; text-align: center;">
            Usa el menú de la izquierda para navegar entre páginas.
        </p>
    """, unsafe_allow_html=True)
    
    # Imagen en la esquina inferior derecha
    st.markdown("""
        <div style="position: fixed; bottom: 10px; right: 10px; z-index: 999;">
            <img src="https://raw.githubusercontent.com/Sawamurarebatta/Recihome-/main/SEGUNDO_PROYECTO/planeta.png" width="150">
        </div>
    """, unsafe_allow_html=True)
