import streamlit as st
import pandas as pd
import os


ARCHIVO_DATOS = "reportes.csv"
COLUMNAS = [
    "id", "fecha", "sala", "numero_equipo", 
    "tipo_problema", "descripcion", "responsable", 
    "estado", "observaciones"
]
st.title("🛠️ Servicio Técnico - Salas de Informática")


if not os.path.exists(ARCHIVO_DATOS):
    df_vacio = pd.DataFrame(columns=COLUMNAS)
    df_vacio.to_csv(ARCHIVO_DATOS, index=False)


st.set_page_config(page_title="Servicio Técnico", page_icon="🔧", layout="centered")


pestana_registro, pestana_consulta = st.tabs(["➕ Registrar servicio", "🔍 Consultar historial"])


with pestana_registro:
    with st.form("formulario_servicio", clear_on_submit=True):
        fecha = st.date_input("Fecha")
        sala = st.text_input("Sala (ej: Sala 18)")
        numero_equipo = st.text_input("N° o identificador del equipo (ej: PC-05)")
        tipo_problema = st.selectbox("Tipo de problema", ["Hardware", "Software", "Red / Conectividad", "Otro"])
        descripcion = st.text_area("Descripción del problema")
        responsable = st.text_input("Docente")
        estado = st.selectbox("Estado", ["Pendiente", "En proceso", "Resuelto"])
        observaciones = st.text_area("Observaciones (opcional)")

        enviado = st.form_submit_button("Guardar registro")

        if enviado:
            if not sala or not numero_equipo:
                st.error("Por favor complete los campos obligatorios (Sala y N° de equipo).")
            else:
                df_existente = pd.read_csv(ARCHIVO_DATOS)
                nuevo_id = len(df_existente) + 1
                
                nuevo_registro = pd.DataFrame([{
                    "id": nuevo_id,
                    "fecha": fecha.strftime("%Y/%m/%d"),
                    "sala": sala,
                    "numero_equipo": numero_equipo,
                    "tipo_problema": tipo_problema,
                    "descripcion": descripcion,
                    "responsable": responsable,
                    "estado": estado,
                    "observaciones": observaciones
                }])

                df_actualizado = pd.concat([df_existente, nuevo_registro], ignore_index=False)
                df_actualizado.to_csv(ARCHIVO_DATOS, index=False)
                st.success("¡Registro guardado con éxito!")


with pestana_consulta:
    st.header("Historial de servicio técnico")
    
    if os.path.exists(ARCHIVO_DATOS):
        df_datos = pd.read_csv(ARCHIVO_DATOS)
        
       
        col1, col2 = st.columns(2)
        
        with col1:
            salas_disponibles = ["Todas"] + sorted(list(df_datos["sala"].dropna().unique())) if not df_datos.empty else ["Todas"]
            filtro_sala = st.selectbox("Filtrar por sala", salas_disponibles)
            
        with col2:
            estados_disponibles = ["Todos", "Pendiente", "En proceso", "Resuelto"]
            filtro_estado = st.selectbox("Filtrar por estado", estados_disponibles)

        
        df_filtrado = df_datos.copy()
        
        if filtro_sala != "Todas":
            df_filtrado = df_filtrado[df_filtrado["sala"] == filtro_sala]
            
        if filtro_estado != "Todos":
            df_filtrado = df_filtrado[df_filtrado["estado"] == filtro_estado]

      
        st.write(f"Se encontraron **{len(df_filtrado)}** registros.")
        st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
