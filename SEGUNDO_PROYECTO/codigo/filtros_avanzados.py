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
        return
    
    columnas_residuos = archivo_cargado.columns[archivo_cargado.columns.get_loc('QRESIDUOS_DOM'): -1]

    st.header("Filtros para el análisis avanzado")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        region_seleccionada = st.selectbox("Selecciona la Región:", archivo_cargado['REG_NAT'].unique())
    with col2:
        departamentos_filtrados = archivo_cargado[archivo_cargado['REG_NAT'] == region_seleccionada]['DEPARTAMENTO'].unique()
        departamento_seleccionado = st.selectbox("Selecciona el Departamento:", ["Todos"] + list(departamentos_filtrados))
    with col3:
        distritos_filtrados = archivo_cargado[archivo_cargado['DEPARTAMENTO'] == departamento_seleccionado]['DISTRITO'].unique() if departamento_seleccionado != "Todos" else archivo_cargado['DISTRITO'].unique()
        distrito_seleccionado = st.selectbox("Selecciona el Distrito:", ["Todos"] + list(distritos_filtrados))
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
        datos_filtrados['Cantidad_Total'] = datos_filtrados[columnas_residuos].sum(axis=1)
        total_por_residuo = datos_filtrados[columnas_residuos].sum()
        top_5_residuos = total_por_residuo.nlargest(5).index
        datos_filtrados['TIPO_RESIDUO'] = datos_filtrados[columnas_residuos].idxmax(axis=1)
        datos_filtrados['TIPO_RESIDUO'] = datos_filtrados['TIPO_RESIDUO'].apply(lambda x: x if x in top_5_residuos else 'Otros')
        datos_agrupados = datos_filtrados.groupby(['PERIODO', 'TIPO_RESIDUO'])['Cantidad_Total'].sum().reset_index()
    else:
        datos_filtrados['Cantidad'] = datos_filtrados[tipo_residuo]
        datos_agrupados = datos_filtrados.groupby(['PERIODO'])[tipo_residuo].sum().reset_index()
    
    titulo = f"Distribución de {tipo_residuo if tipo_residuo != 'Todos' else 'residuos'} en {region_seleccionada}"
    
    fig_bar = px.bar(
        datos_agrupados,
        x='PERIODO',
        y='Cantidad_Total' if tipo_residuo == "Todos" else 'Cantidad',
        color='TIPO_RESIDUO' if tipo_residuo == "Todos" else None,
        title=titulo
    )
    
    st.plotly_chart(fig_bar)
    # Crear gráfico circular para departamentos o distritos
    if departamento_seleccionado == "Todos":
        datos_agrupados = datos_filtrados.groupby('DEPARTAMENTO')[y_column].sum().reset_index()
        fig_pie_departamentos = px.pie(
            datos_agrupados,
            names='DEPARTAMENTO',
            values=y_column,
            title=f'Distribución porcentual de residuos por departamento en {region_seleccionada}',
            color_discrete_sequence=px.colors.qualitative.T10  # Colores más variados
        )
    elif distrito_seleccionado == "Todos":
        datos_agrupados = datos_filtrados.groupby('DISTRITO')[y_column].sum().reset_index()
        fig_pie_departamentos = px.pie(
            datos_agrupados,
            names='DISTRITO',
            values=y_column,
            title=f'Distribución porcentual de residuos por distrito en {departamento_seleccionado}',
            color_discrete_sequence=px.colors.qualitative.T10  # Colores más variados
        )
    else:
        datos_agrupados = datos_filtrados.groupby(['DEPARTAMENTO', 'DISTRITO'])[y_column].sum().reset_index()
        fig_pie_departamentos = px.pie(
            datos_agrupados,
            names='DISTRITO',
            values=y_column,
            title=f'Distribución porcentual de residuos en el distrito {distrito_seleccionado}',
            color_discrete_sequence=px.colors.qualitative.T10  # Colores más variados
        )

    # Personalizar el gráfico circular para departamentos o distritos
    fig_pie_departamentos.update_layout(
        title={
            'text': 'Distribución porcentual de residuos por ubicación',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        paper_bgcolor='rgba(0, 51, 51, 1)',  # Fondo del gráfico
        plot_bgcolor='rgba(255, 255, 255, 1)',  # Fondo del área de trazado
        font=dict(color='white'),  # Texto blanco para contraste
        width=800,  # Ajustar la anchura del gráfico
        height=600,  # Ajustar la altura del gráfico
        margin=dict(l=0, r=0, t=100, b=50)  # Centrando el gráfico y aumentando el margen superior
    )

    # Mostrar gráficos
    st.plotly_chart(fig_bar)
    st.plotly_chart(fig_pie_residuos)
    st.plotly_chart(fig_pie_departamentos)
