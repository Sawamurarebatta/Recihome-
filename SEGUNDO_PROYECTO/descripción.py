import streamlit as st

def descripcion_app():
    # Crear un diseño de dos columnas
    col1, col2 = st.columns([1, 3])

    # Columna izquierda: Imagen
    with col1:
        st.image(r"C:\Users\Yosselin\Downloads\Recihome--main (1)\ULTIMO_STREAMLIT\images\residuo.png", use_container_width=True)



    # Columna derecha: Descripción
    with col2:
        # Título principal
        st.title("Bienvenidos a ReciHome")
        
        # Descripción principal
        st.write(
            """
            Este **dashboard interactivo** describe la producción de todo tipo de residuos a nivel nacional en el Perú, 
            considerando cada departamento y distrito entre los años **2019** al **2022**. 
            Aquí podrás explorar los datos de manera detallada, utilizando herramientas como gráficos interactivos y mapas de distribución 
            para visualizar y analizar la información.
            """
        )

        # Subtítulo: Objetivos
        st.subheader("Objetivos")
        st.write(
            """
            - **Concientizar al público** sobre la importancia de reducir y gestionar adecuadamente los residuos que generamos.
            - Proporcionar información accesible y visual para entender la distribución de residuos a nivel nacional.
            - Fomentar prácticas sostenibles en los hogares, comunidades y empresas para proteger nuestro medio ambiente.
            - Facilitar el acceso a herramientas interactivas para analizar la generación de residuos de forma dinámica y efectiva.
            """
        )

        # Mención de navegación interactiva
        st.write(
            """
            En esta plataforma, podrás **desplazarte por la página** y emplear:
            - **Filtros interactivos** para personalizar los datos según tus intereses.
            - **Mapas de distribución** para localizar las áreas con mayor acumulación de residuos.
            - **Gráficos dinámicos** que muestran las tendencias de generación de residuos en diferentes regiones.
            """
        )

        # Subtítulo: Integrantes
        st.subheader("Integrantes del equipo")
        # Lista de integrantes
        st.write(
            """
            - Patricia Rebatta Jeri  
            - Yosselin Cosme Perez  
            - Justin Hernandez  
            - Andrea Villamjizar Maravi
            """
        )
import streamlit as st

def descripcion_app():
    # Crear un diseño de dos columnas
    col1, col2 = st.columns([1, 3])

    # Columna izquierda: Imagen
    with col1:
        st.image("residuo.png", use_column_width=True)

    # Columna derecha: Descripción
    with col2:
        # Título principal
        st.title("Bienvenidos a ReciHome")
        
        # Descripción principal
        st.write(
            """
            Este **dashboard interactivo** describe la producción de todo tipo de residuos a nivel nacional en el Perú, 
            considerando cada departamento y distrito entre los años **2019** al **2022**. 
            Aquí podrás explorar los datos de manera detallada, utilizando herramientas como gráficos interactivos y mapas de distribución 
            para visualizar y analizar la información.
            """
        )

        # Subtítulo: Objetivos
        st.subheader("Objetivos")
        st.write(
            """
            - **Concientizar al público** sobre la importancia de reducir y gestionar adecuadamente los residuos que generamos.
            - Proporcionar información accesible y visual para entender la distribución de residuos a nivel nacional.
            - Fomentar prácticas sostenibles en los hogares, comunidades y empresas para proteger nuestro medio ambiente.
            - Facilitar el acceso a herramientas interactivas para analizar la generación de residuos de forma dinámica y efectiva.
            """
        )

        # Mención de navegación interactiva
        st.write(
            """
            En esta plataforma, podrás **desplazarte por la página** y emplear:
            - **Filtros interactivos** para personalizar los datos según tus intereses.
            - **Mapas de distribución** para localizar las áreas con mayor acumulación de residuos.
            - **Gráficos dinámicos** que muestran las tendencias de generación de residuos en diferentes regiones.
            """
        )

        # Subtítulo: Integrantes
        st.subheader("Integrantes del equipo")
        # Lista de integrantes
        st.write(
            """
            - Patricia Rebatta Jeri  
            - Yosselin Cosme Perez  
            - Justin Hernandez  
            - Andrea Villamjizar Maravi
            """
        )
