import streamlit as st
import plotly.express as px
import pandas as pd

def filtros_avanzados(archivo_cargado):
    # Validar que el DataFrame no esté vacío
    if archivo_cargado.empty:
        st.error("El archivo cargado está vacío. Por favor, carga un archivo válido.")
        return
    
    # Verificar que las columnas necesarias existan
    required_columns = ['REG_NAT', 'DEPARTAMENTO', 'DISTRITO', 'PERIODO', 'QRESIDUOS_DOM']
    missing_columns = [col for col in required_columns if col not in archivo_cargado.columns]
    if missing_columns:
        st.error(f"Las siguientes columnas no se encuentran en el archivo cargado: {', '.join(missing_columns)}")
        st.write("Columnas disponibles:", list(archivo_cargado.columns))
        return
    
    # Seleccionar rango de columnas de residuos
    try:
        columnas_residuos = archivo_cargado.loc[:, 'QRESIDUOS_DOM':archivo_cargado.columns[-2]].columns
    except KeyError as e:
        st.error(f"Error al seleccionar columnas: {e}")
        return
    
    st.header("Filtros para el análisis avanzado")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        region_seleccionada = st.selectbox(
            "Selecciona la Región:",
            options=archivo_cargado['REG_NAT'].unique()
        )
    
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
    
    # Filtrar datos según las selecciones y los años 2019 a 2022
    datos_filtrados = archivo_cargado[
        (archivo_cargado['REG_NAT'] == region_seleccionada) &
        ((archivo_cargado['DEPARTAMENTO'] == departamento_seleccionado) | (departamento_seleccionado == "Todos")) &
        ((archivo_cargado['DISTRITO'] == distrito_seleccionado) | (distrito_seleccionado == "Todos")) &
        (archivo_cargado['PERIODO'].isin([2019, 2020, 2021, 2022]))
    ]
    
    # Calcular la cantidad total de basura si se selecciona "Todos"
    if tipo_residuo == "Todos":
        datos_filtrados['Cantidad de Basura'] = datos_filtrados[columnas_residuos].sum(axis=1)
        datos_filtrados = datos_filtrados.melt(id_vars=['REG_NAT', 'DEPARTAMENTO', 'DISTRITO', 'PERIODO', 'Cantidad de Basura'], 
                                               value_vars=columnas_residuos, 
                                               var_name='TIPO_RESIDUO', 
                                               value_name='Cantidad')
        y_column = 'Cantidad de Basura'
        color_column = 'TIPO_RESIDUO'
        
        # Agrupar datos para mostrar solo el top 5 y agrupar los demás como "Otros"
        top_5 = datos_filtrados.groupby('TIPO_RESIDUO')['Cantidad'].sum().nlargest(5).index
        datos_filtrados['TIPO_RESIDUO'] = datos_filtrados['TIPO_RESIDUO'].apply(lambda x: x if x in top_5 else 'Otros')
        datos_filtrados_agrupados = datos_filtrados.groupby(['REG_NAT', 'DEPARTAMENTO', 'DISTRITO', 'PERIODO', 'TIPO_RESIDUO']).sum().reset_index()
        otros = datos_filtrados_agrupados[datos_filtrados_agrupados['TIPO_RESIDUO'] == 'Otros']['Cantidad'].sum()
        datos_filtrados_agrupados = datos_filtrados_agrupados[datos_filtrados_agrupados['TIPO_RESIDUO'] != 'Otros']
        otros_df = pd.DataFrame({'TIPO_RESIDUO': ['Otros'], 'Cantidad': [otros]})
        datos_filtrados_agrupados = pd.concat([datos_filtrados_agrupados, otros_df], ignore_index=True)
        datos_filtrados = datos_filtrados_agrupados

        # Cambiar visualmente el texto de los datos
        datos_filtrados['TIPO_RESIDUO'] = datos_filtrados['TIPO_RESIDUO'].str.replace('_', ' ').str.title()
    else:
        datos_filtrados['Cantidad'] = datos_filtrados[tipo_residuo]
        y_column = tipo_residuo
        color_column = None

    # Construir el título dinámicamente
    if tipo_residuo == "Todos":
        tipo_residuo_titulo = "todos los tipos de Residuos"
    else:
        tipo_residuo_titulo = tipo_residuo.replace('_', ' ').title()

    if distrito_seleccionado == "Todos" and departamento_seleccionado == "Todos":
        distrito_titulo = f"todos los departamentos de la región {region_seleccionada}"
    elif distrito_seleccionado == "Todos":
        distrito_titulo = f"todos los distritos de {departamento_seleccionado}"
    else:
        distrito_titulo = f"el distrito de {distrito_seleccionado}"

    if departamento_seleccionado == "Todos":
        departamento_titulo = f"todos los departamentos de la región {region_seleccionada}"
    else:
        departamento_titulo = f"el departamento de {departamento_seleccionado}"

    if tipo_residuo == "Todos":
        titulo_grafico = f"Residuos de basura en {distrito_titulo} durante los años 2019 a 2022"
    else:
        titulo_grafico = f"Cantidad de {tipo_residuo_titulo} en {distrito_titulo} durante los años 2019 a 2022"

    # Crear gráfico de barras
    fig_bar = px.bar(
        datos_filtrados,
        x='PERIODO',
        y=y_column,
        color=color_column,
        title=titulo_grafico,
        labels={y_column: "Cantidad (kg)", "PERIODO": "Año"},
        text_auto=False,  # Desactivar el texto automático
        color_discrete_sequence=px.colors.qualitative.T10  # Colores más variados
    )
    
    # Calcular el total acumulado por columna
    total_acumulado = datos_filtrados.groupby('PERIODO')[y_column].sum().reset_index()
    total_acumulado['Cantidad'] = total_acumulado[y_column].apply(lambda x: f"{x/1_000_000:.1f}M" if x >= 1_000_000 else f"{x/1_000:.1f}K" if x >= 1_000 else f"{x:.0f}")

    # Agregar texto por encima de las columnas
    fig_bar.update_traces(texttemplate=total_acumulado['Cantidad'], textposition='outside')

    # Personalizar el fondo del gráfico y centrar el título
    fig_bar.update_layout(
        title={
            'text': titulo_grafico,
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis=dict(
            tickmode='array',
            tickvals=[2019, 2020, 2021, 2022],
            ticktext=['2019', '2020', '2021', '2022']
        ),
        paper_bgcolor='rgba(0, 51, 51, 1)',  # Fondo del gráfico
        plot_bgcolor='rgba(255, 255, 255, 1)',  # Fondo del área de trazado
        font=dict(color='white'),  # Texto blanco para contraste
        width=800,  # Aumentar la anchura del gráfico
        height=600,  # Ajustar la altura del gráfico
        margin=dict(l=0, r=0, t=100, b=50)  # Centrando el gráfico y aumentar el margen superior
    )

    # Crear gráfico circular para tipos de residuos
    if tipo_residuo == "Todos":
        fig_pie_residuos = px.pie(
            datos_filtrados,
            names='TIPO_RESIDUO',
            values='Cantidad',
            title='Distribución porcentual de tipos de residuos',
            color_discrete_sequence=px.colors.qualitative.T10  # Colores más variados
        )
        fig_pie_residuos.update_traces(textposition='inside', textinfo='percent+label')
    else:
        # Crear un DataFrame específico para el gráfico circular
        datos_circular = pd.DataFrame({'Tipo Residuo': [tipo_residuo_titulo], 'Cantidad': [datos_filtrados['Cantidad'].sum()]})
        fig_pie_residuos = px.pie(
            datos_circular,
            names='Tipo Residuo',
            values='Cantidad',
            title=f'Distribución porcentual de {tipo_residuo_titulo}',
            color_discrete_sequence=px.colors.qualitative.T10  # Colores más variados
        )
        fig_pie_residuos.update_traces(textposition='inside', textinfo='percent+label')

    # Personalizar el gráfico circular de tipos de residuos
    fig_pie_residuos.update_layout(
        title={
            'text': 'Distribución porcentual de tipos de residuos',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        paper_bgcolor='rgba(0, 51, 51, 1)',  # Fondo del gráfico
        plot_bgcolor='rgba(255, 255, 255, 1)',  # Fondo del área de trazado
        font=dict(color='white'),  # Texto blanco para contraste
        width=800,  # Ajustar la anchura del gráfico
        height=600,  # Ajustar la altura del gráfico
        margin=dict(l=0, r=0, t=100, b=50)  # Centrando el gráfico y aumentar el margen superior
    )

    # Crear gráfico circular para departamentos o distritos
    if departamento_seleccionado == "Todos":
        datos_agrupados = datos_filtrados.groupby('DEPARTAMENTO')['Cantidad'].sum().nlargest(15).reset_index()
        fig_pie_ubicacion = px.pie(
            datos_agrupados,
            names='DEPARTAMENTO',
            values='Cantidad',
            title='Distribución porcentual por departamentos',
            color_discrete_sequence=px.colors.qualitative.T10  # Colores más variados
        )
    else:
        datos_agrupados = datos_filtrados.groupby('DISTRITO')['Cantidad'].sum().nlargest(15).reset_index()
        fig_pie_ubicacion = px.pie(
            datos_agrupados,
            names='DISTRITO',
            values='Cantidad',
            title='Distribución porcentual por distritos',
            color_discrete_sequence=px.colors.qualitative.T10  # Colores más variados
        )
    fig_pie_ubicacion.update_traces(textposition='inside', textinfo='percent+label')

    # Personalizar el gráfico circular de ubicaciones
    fig_pie_ubicacion.update_layout(
        title={
            'text': 'Distribución porcentual por ubicaciones',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        paper_bgcolor='rgba(0, 51, 51, 1)',  # Fondo del gráfico
        plot_bgcolor='rgba(255, 255, 255, 1)',  # Fondo del área de trazado
        font=dict(color='white'),  # Texto blanco para contraste
        width=800,  # Ajustar la anchura del gráfico
        height=600,  # Ajustar la altura del gráfico
        margin=dict(l=0, r=0, t=100, b=50)  # Centrando el gráfico y aumentar el margen superior
    )

    # Mostrar gráfico de barras centrado
    st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Mostrar gráficos circulares en columnas
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_pie_residuos)
    with col2:
        st.plotly_chart(fig_pie_ubicacion)

# Ejemplo de uso
if __name__ == "__main__":
    st.title("Análisis Avanzado de Residuos")
    
    # Subida de archivo
    archivo = st.file_uploader("Sube tu archivo CSV", type="csv")
    
    if archivo:
        # Cargar datos
        datos = pd.read_csv(archivo)
        filtros_avanzados(datos)


