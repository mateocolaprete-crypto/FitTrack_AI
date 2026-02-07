import streamlit as st
from st_gsheets_connection import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Configuración de Perfil", page_icon="⚙️")

conn = st.connection("gsheets", type=GSheetsConnection)

st.title("⚙️ Configuración de Perfil Fitness")
st.write("Ajustá tus datos para que la IA calcule tus metas diarias.")

# 1. FORMULARIO DE DATOS FÍSICOS
with st.form("perfil_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        peso = st.number_input("Peso Actual (kg):", min_value=30.0, max_value=250.0, value=75.0)
        altura = st.number_input("Altura (cm):", min_value=100, max_value=250, value=175)
        edad = st.number_input("Edad:", min_value=12, max_value=100, value=25)
    
    with col2:
        genero = st.selectbox("Género:", ["Masculino", "Femenino"])
        actividad = st.selectbox("Nivel de Actividad:", [
            "Sedentario (Poco ejercicio)",
            "Ligero (1-3 días/semanal)",
            "Moderado (3-5 días/semanal)",
            "Intenso (6-7 días/semanal)"
        ])
        objetivo = st.selectbox("Objetivo:", ["Perder Grasa", "Mantener Peso", "Ganar Músculo"])

    if st.form_submit_button("💾 Calcular y Guardar Metas"):
        # 2. CÁLCULO PROFESIONAL (Fórmula Mifflin-St Jeor)
        if genero == "Masculino":
            bmr = (10 * peso) + (6.25 * altura) - (5 * edad) + 5
        else:
            bmr = (10 * peso) + (6.25 * altura) - (5 * edad) - 161
            
        # Multiplicador de actividad
        multiplicadores = {
            "Sedentario (Poco ejercicio)": 1.2,
            "Ligero (1-3 días/semanal)": 1.375,
            "Moderado (3-5 días/semanal)": 1.55,
            "Intenso (6-7 días/semanal)": 1.725
        }
        tdee = bmr * multiplicadores[actividad]
        
        # Ajuste según objetivo
        if objetivo == "Perder Grasa":
            cal_meta = tdee - 500
            prot_meta = peso * 2.0 # Más proteína para no perder músculo
        elif objetivo == "Ganar Músculo":
            cal_meta = tdee + 300
            prot_meta = peso * 2.2
        else:
            cal_meta = tdee
            prot_meta = peso * 1.8

        # 3. GUARDAR EN GOOGLE SHEETS
        nuevo_perfil = pd.DataFrame([{
            "Usuario": "Admin", # Podés hacerlo multiusuario después
            "Peso": peso,
            "Altura": altura,
            "Edad": edad,
            "Genero": genero,
            "Actividad": actividad,
            "Objetivo": objetivo,
            "Calorias_Meta": int(cal_meta),
            "Proteina_Meta": int(prot_meta)
        }])
        
        try:
            conn.update(worksheet="Perfil", data=nuevo_perfil)
            st.success(f"✅ ¡Perfil actualizado! Tu meta diaria es de {int(cal_meta)} kcal.")
            st.balloons()
        except Exception as e:
            st.error(f"Error al conectar con Google Sheets: {e}")

# 4. VISTA PREVIA
st.divider()
st.subheader("Tu Perfil Actual")
try:
    df_actual = conn.read(worksheet="Perfil", ttl=0)
    if not df_actual.empty:
        st.dataframe(df_actual)
    else:
        st.info("Aún no hay datos guardados.")
except:
    st.info("La hoja 'Perfil' está lista para recibir tus datos.")

