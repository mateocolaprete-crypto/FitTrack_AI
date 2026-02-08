import streamlit as st
import google.generativeai as genai
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import json
import re
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Analizador Nutricional IA", page_icon="🍎", layout="wide")

# Conexión a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. CONFIGURACIÓN DE GEMINI
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    # Sistema de doble intento para evitar el error 404
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception:
        model = genai.GenerativeModel('models/gemini-1.5-flash')
else:
    st.error("⚠️ No se encontró la GEMINI_API_KEY en los Secrets de Streamlit.")
    st.stop() # Detiene la ejecución si no hay API Key

st.title("🍎 Analizador de Comidas Inteligente")
st.markdown("Escribí lo que comiste y nuestra IA calculará los macros automáticamente.")

# 3. INTERFAZ DE ENTRADA
with st.container(border=True):
    col_a, col_b = st.columns([1, 2])
    with col_a:
        momento = st.selectbox("🕒 Momento", ["Desayuno", "Almuerzo", "Merienda", "Cena", "Snack"])
    with col_b:
        input_usuario = st.text_input("🥗 ¿Qué comiste?", placeholder="Ej: 2 tostadas con palta y 1 café con leche")

# 4. LÓGICA DE PROCESAMIENTO
if st.button("Analizar Comida ✨", use_container_width=True):
    if input_usuario:
        with st.status("Gemini analizando ingredientes...", expanded=True) as status:
            try:
                prompt = f"""
                Eres un nutricionista experto. Analiza: "{input_usuario}".
                Genera un JSON estrictamente con este formato:
                {{
                    "alimento": "nombre corto",
                    "calorias": 0,
                    "proteinas": 0,
                    "carbohidratos": 0,
                    "grasas": 0
                }}
                Usa valores numéricos enteros. Si no hay cantidades, estima una porción normal.
                JSON:
                """
                response = model.generate_content(prompt)
                
                # Limpieza del JSON
                match = re.search(r"\{.*\}", response.text, re.DOTALL)
                if match:
                    data = json.loads(match.group())
                    st.session_state.temp_data = data
                    status.update(label="¡Análisis completado!", state="complete", expanded=False)
                else:
                    st.error("La IA no devolvió un formato válido. Reintenta.")
            except Exception as e:
                st.error(f"Error técnico: {e}")
    else:
        st.warning("Por favor, ingresá una descripción.")

# 5. CONFIRMACIÓN Y GUARDADO
if "temp_data" in st.session_state:
    data = st.session_state.temp_data
    
    st.divider()
    st.subheader(f"📊 Resultado: {data['alimento'].capitalize()}")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🔥 Calorías", f"{data['calorias']} kcal")
    c2.metric("🍗 Proteínas", f"{data['proteinas']}g")
    c3.metric("🍞 Carbos", f"{data['carbohidratos']}g")
    c4.metric("🥑 Grasas", f"{data['grasas']}g")

    if st.button("💾 Confirmar y Registrar en mi Diario", type="primary"):
        try:
            # Leer datos actuales
            df_actual = conn.read(worksheet="Comidas", ttl=0)
            
            # Crear nueva fila
            nueva_comida = pd.DataFrame([{
                "Fecha": datetime.now().strftime("%Y-%m-%d"),
                "Momento": momento,
                "Alimento": data['alimento'],
                "Calorias": int(data['calorias']),
                "Proteinas": int(data['proteinas']),
                "Carbohidratos": int(data['carbohidratos']),
                "Grasas": int(data['grasas'])
            }])
            
            # Unir y subir
            df_updated = pd.concat([df_actual, nueva_comida], ignore_index=True)
            conn.update(worksheet="Comidas", data=df_updated)
            
            st.success("✅ ¡Comida registrada correctamente!")
            del st.session_state.temp_data 
            st.balloons() 
        except Exception as e:
            st.error(f"Error al guardar en Google Sheets: {e}")
