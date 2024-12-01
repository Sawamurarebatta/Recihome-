import streamlit as st
import plotly.express as px
import pandas as pd

def filtros_avanzados(archivo_cargado):
    if archivo_cargado.empty:
        st.error("El archivo cargado está vacío. Por favor, carga un archivo válido.")
        return

    required_columns = ['REG_NAT', 'DEPARTAMENTO', 'DISTRITO', 'PERIODO', 'QRESIDUOS_DOM']
    missing_columns = [col for col in required_columns if col not in archivo_cargado.columns]
    if missing_columns:
        st.error(f"Las siguientes columnas no se encuentran en el archivo cargado: {', '.join(missing_columns)}")
        st.write("Columnas disponibles:", list(archivo_cargado.columns))
        return

    try:
        columnas_residuos = archivo_cargado.loc[:, 'QRESIDUOS_DOM':archivo_cargado.columns[-2]].columns
    except KeyError as e:
        st.error(f"Error al seleccionar columnas: {e}")
        return

    st.header("Filtros para el análisis avanzado")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        region_seleccionada = st.selectbox("Selecciona la Región:", options=archivo_cargado['REG_NAT'].unique())

    with col2:
        departamentos_filtrados = archivo_cargado[archivo_cargado['REG_NAT'] == region_seleccionada]['DEPARTAMENTO'].unique()
        departamentos = ["Todos"] + list(departamentos_filtrados)
        departamento_seleccionado = st.selectbox("Selecciona el Departamento:", departamentos)

    with col3:
        if departamento_seleccionado == "Todos":
            distritos_filtrados = archivo_cargado[archivo_cargado['REG_NAT'] == region_seleccionada]['DISTRITO'].unique()
        else:
            distritos_filtrados = archivo_cargado[(archivo_cargado['REG_NAT'] == region_seleccionada) & (archivo_cargado['DEPARTAMENTO'] == departamento_seleccionado)]['DISTRITO'].unique()
        distritos = ["Todos"] + list(distritos_filtrados)
        distrito_seleccionado = st.selectbox("Selecciona el Distrito:", distritos)

    with col4:
        tipos_residuo = ["Todos"] + list(columnas_residuos)
        tipo_residuo = st.selectbox("Selecciona el Tipo de Residuo:", tipos_residuo)

    datos_filtrados = archivo_cargado[
        (archivo_cargado['REG_NAT'] == region_seleccionada) &
        ((archivo_cargado['DEPARTAMENTO'] == departamento_seleccionado) | (departamento_seleccionado == "Todos")) &
        ((archivo_cargado['DISTRITO'] == distrito_seleccionado) | (distrito_seleccionado == "Todos")) &
        (archivo_cargado['PERIODO'].isin([2019, 2020, 2021, 2022]))
    ]

    if tipo_residuo == "Todos":
        datos_filtrados['Cantidad de Basura'] = datos_filtrados[columnas_residuos].sum(axis=1)
        y_column = 'Cantidad de Basura'
        color_column = None
    else:
        datos_filtrados['Cantidad'] = datos_filtrados[tipo_residuo]
        y_column = 'Cantidad'
        color_column = None

    titulo_grafico = f"Cantidad de residuos en {region_seleccionada} (2019-2022)"

    fig_bar = px.bar(
        datos_filtrados,
        x='PERIODO',
        y=y_column,
        color=color_column,
        title=titulo_grafico,
        labels={y_column: "Cantidad (kg)", "PERIODO": "Año"},
        text_auto=False,
        color_discrete_sequence=px.colors.sequential.Reds
    )

    fig_bar.update_layout(
        title={
            'text': titulo_grafico,
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis=dict(
            tickmode='array',
            tickvals=[2019, 2020, 2021, 2022],
            ticktext=['2019', '2020', '2021', '2022']
        ),
        paper_bgcolor='#151515',
        plot_bgcolor='#151515',
        font=dict(color='white'),
        width=800,
        height=600,
        margin=dict(l=0, r=0, t=100, b=50)
    )

    st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Ejemplo de uso
if __name__ == "__main__":
    st.title("Análisis Avanzado de Residuos")

    archivo = st.file_uploader("Sube tu archivo CSV", type="csv")

    if archivo:
        datos = pd.read_csv(archivo)
        filtros_avanzados(datos)

