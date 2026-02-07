import streamlit as st
from st_gsheets_connection import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Log de Entrenamiento", page_icon="💪")
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("💪 Registro de Entrenamiento")
st.markdown("Anotá tus cargas para asegurar la progresión sobrecargada.")

# 2. FORMULARIO DE CARGA
with st.container(border=True):
    with st.form("gym_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            fecha = st.date_input("Fecha:", datetime.now())
            ejercicio = st.text_input("Ejercicio:", placeholder="Ej: Press de Banca")
            peso = st.number_input("Peso (kg):", min_value=0.0, step=0.5)
            
        with col2:
            series = st.number_input("Series:", min_value=1, step=1)
            reps = st.number_input("Repeticiones:", min_value=1, step=1)
            rpe = st.slider("Esfuerzo (RPE 1-10):", 1, 10, 8)

        if st.form_submit_button("💾 Registrar Serie", use_container_width=True):
            try:
                # Leer datos existentes
                df_entrenos = conn.read(worksheet="Entrenamientos", ttl=0)
                
                # Crear nueva fila
                nueva_serie = pd.DataFrame([{
                    "Fecha": fecha.strftime("%Y-%m-%d"),
                    "Ejercicio": ejercicio.strip().title(),
                    "Series": int(series),
                    "Reps": int(reps),
                    "Peso_kg": peso,
                    "RPE": rpe,
                    "Volumen_Total": int(series * reps * peso)
                }])
                
                # Concatenar y actualizar
                df_updated = pd.concat([df_entrenos, nueva_serie], ignore_index=True)
                conn.update(worksheet="Entrenamientos", data=df_updated)
                
                st.success(f"✅ ¡{ejercicio} registrado!")
            except Exception as e:
                st.error(f"Error al guardar: {e}")

# 3. VISUALIZACIÓN DE PROGRESO
st.divider()
st.subheader("📋 Últimos Registros")

try:
    df_ver = conn.read(worksheet="Entrenamientos", ttl=0)
    if not df_ver.empty:
        # Mostrar los últimos 10 registros
        st.dataframe(df_ver.tail(10), use_container_width=True)
        
        # Pequeño gráfico de volumen por día
        st.subheader("📈 Volumen de Entrenamiento")
        vol_dia = df_ver.groupby('Fecha')['Volumen_Total'].sum()
        st.line_chart(vol_dia)
    else:
        st.info("Aún no hay entrenamientos registrados. ¡Dale a los hierros! 🏋️‍♂️")
except:
    st.info("La pestaña 'Entrenamientos' en el Excel está lista para recibir datos.")

