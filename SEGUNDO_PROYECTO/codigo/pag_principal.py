import pandas as pd
import streamlit as st

# Función para la página principal
def pagina_principal():
    # URL del GIF de fondo
    gif_url = "https://github.com/Sawamurarebatta/Recihome-/blob/main/SEGUNDO_PROYECTO/appl.gif?raw=true"  # URL del GIF

    # URL del logo
    logo_url = "https://github.com/Sawamurarebatta/Recihome-/blob/main/SEGUNDO_PROYECTO/logo.png?raw=true"  # URL del logo

    # Diseño de la página
    st.markdown(f"""
        <style>
            .stApp {{
                background-image: url("{gif_url}");
                background-repeat: no-repeat;
                background-size: cover;
                background-position: center;
                height: 100vh;
                color: white;  /* Cambia el color de texto para hacerlo visible sobre el GIF */
            }}
            .logo-container {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: 80vh;  /* Ajustar la altura para centrar verticalmente */
            }}
            p {{
                font-size: 20px;
                text-align: justify;
                font-family: 'Arial', sans-serif;
            }}
        </style>
        <div class="logo-container">
            <img src="{logo_url}" alt="Logo" style="max-width: 300px; height: auto;">
        </div>
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
