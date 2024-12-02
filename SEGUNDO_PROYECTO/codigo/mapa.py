import pandas as pd
import streamlit as st
import plotly.express as px
import requests

def dashboard_residuos(archivo_cargado):
    # Cambiar el color del texto de Streamlit a blanco, incluyendo st.metric
    st.markdown(
        """
        <style>
            .stApp {
                color: white;  /* Cambiar color general del texto a blanco */
            }
            div[data-testid="stMetricValue"] {
                color: white; /* Cambiar color del valor en st.metric */
                font-size: 24px; /* Tamaño opcional para el valor */
                font-weight: bold; /* Opcional: negrita para el valor */
            }
            div[data-testid="stMetricLabel"] {
                color: white; /* Cambiar color de la etiqueta en st.metric */
                font-size: 18px; /* Tamaño opcional para la etiqueta */
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Resumen General: Residuos por Región y Tipo")

    # Preprocesamiento
    columnas_residuos = archivo_cargado.loc[:, 'QRESIDUOS_DOM':archivo_cargado.columns[-2]].columns

    # Sumar residuos por departamento
    residuos_por_region = archivo_cargado.groupby('DEPARTAMENTO')[columnas_residuos].sum()
    residuos_por_region["Total Residuos"] = residuos_por_region.sum(axis=1)
    residuos_totales = residuos_por_region["Total Residuos"].sum()

    # Crear una fila de dos columnas para las métricas clave
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Residuos Totales Generados", value=f"{residuos_totales/1_000_000:.2f} M")
    with col2:
        region_max = residuos_por_region["Total Residuos"].idxmax()
        max_residuos = residuos_por_region["Total Residuos"].max()
        st.metric(label=f"Mayor Generación: {region_max}", value=f"{max_residuos/1_000_000:.2f} M")
    # Descargar GeoJSON desde GitHub
    geojson_url = "https://raw.githubusercontent.com/Sawamurarebatta/Recihome-/main/SEGUNDO_PROYECTO/peru_regions.geojson"
    geojson_response = requests.get(geojson_url)

    if geojson_response.status_code == 200:
        peru_geojson = geojson_response.json()
    else:
        st.error("No se pudo cargar el archivo GeoJSON desde GitHub.")
        return

    # Validar la estructura del GeoJSON
    if "features" not in peru_geojson or not isinstance(peru_geojson["features"], list):
        st.error("El archivo GeoJSON tiene un formato incorrecto.")
        return

    # Verificar que los nombres coincidan entre los datos y el GeoJSON
    try:
        nombres_departamentos_geojson = {
            feature["properties"].get("NOMBDEP", "").upper() for feature in peru_geojson["features"]
        }
    except KeyError:
        st.error("La estructura del archivo GeoJSON no es la esperada.")
        return

    nombres_departamentos_datos = set(residuos_por_region.index.str.upper())
    coincidencias = nombres_departamentos_datos.intersection(nombres_departamentos_geojson)
    no_coincidencias = nombres_departamentos_datos.difference(nombres_departamentos_geojson)

    if no_coincidencias:
        st.warning(f"Los siguientes departamentos en tus datos no coinciden con el GeoJSON: {', '.join(no_coincidencias)}")

    # Crear una fila para el mapa y el gráfico de barras
    row1_col1, row1_col2 = st.columns([2, 1])  # Columna ancha para el mapa y una columna más estrecha para el gráfico

    with row1_col1:
        st.subheader("Mapa de Generación de Residuos por Departamento")
        mapa_peru = px.choropleth(
            residuos_por_region.reset_index(),
            geojson=peru_geojson,
            locations="DEPARTAMENTO",
            featureidkey="properties.NOMBDEP",  # Aquí se ajusta la clave para los nombres
            color="Total Residuos",
            color_continuous_scale=["#A2DFF7", "#0072B2"],  # Escala de celeste a azul
            labels={"Total Residuos": "Cantidad de Residuos (kg)"},
            title="Distribución de Residuos por Departamento"
        )
        mapa_peru.update_geos(fitbounds="locations", visible=False)
        mapa_peru.update_layout(
            geo=dict(bgcolor="black"),  # Fondo negro
            paper_bgcolor="black",  # Fondo del gráfico negro
            plot_bgcolor="black",  # Fondo del gráfico negro
            font=dict(color="white")  # Texto blanco
        )
        st.plotly_chart(mapa_peru, use_container_width=True)

    with row1_col2:
        st.subheader("Top Departamentos por Generación de Residuos")
        top_departamentos = residuos_por_region.nlargest(5, "Total Residuos").reset_index()
        top_chart = px.bar(
            top_departamentos,
            x="Total Residuos",
            y="DEPARTAMENTO",
            orientation="h",
            text="Total Residuos",
            color="DEPARTAMENTO",
            color_discrete_sequence=["#640D5F", "#D91656", "#EB5B00", "#FFB200"],  # Colores personalizados
            labels={"Total Residuos": "Cantidad de Residuos (kg)", "DEPARTAMENTO": "Departamento"},
            title="Top 5 Departamentos Generadores de Residuos"
        )
        top_chart.update_layout(
            paper_bgcolor="black",  # Fondo negro
            plot_bgcolor="black",  # Fondo negro
            font=dict(color="white")  # Texto blanco
        )
        top_chart.update_traces(textfont=dict(color="white"))  # Texto interno blanco
        st.plotly_chart(top_chart, use_container_width=True)
