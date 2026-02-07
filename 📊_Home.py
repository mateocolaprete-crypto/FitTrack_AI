import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA (Debe ser lo primero)
st.set_page_config(
    page_title="FitTrack AI - Professional",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS personalizado para mejorar la estética
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# 2. CONEXIÓN Y CARGA DE DATOS
def load_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    try:
        df_perfil = conn.read(worksheet="Perfil", ttl=0)
        df_comidas = conn.read(worksheet="Comidas", ttl=0)
        return df_perfil, df_comidas
    except Exception:
        return pd.DataFrame(), pd.DataFrame()

df_perfil, df_comidas = load_data()

# 3. CABECERA
st.title("📊 FitTrack AI: Tu Centro de Mando")
fecha_hoy = datetime.now().strftime("%d / %m / %Y")
st.info(f"📅 Hoy es {fecha_hoy}")

# 4. LÓGICA DE NEGOCIO (Procesamiento de Macros)
if not df_perfil.empty:
    user = df_perfil.iloc[0]  # Tomamos el primer perfil configurado
    
    # Filtrar comidas de hoy
    hoy_str = datetime.now().strftime("%Y-%m-%d")
    if not df_comidas.empty:
        # Convertimos columna Fecha a string por seguridad en la comparación
        df_comidas['Fecha'] = df_comidas['Fecha'].astype(str)
        comidas_hoy = df_comidas[df_comidas['Fecha'] == hoy_str]
    else:
        comidas_hoy = pd.DataFrame()

    # Sumatorias
    cal_hoy = comidas_hoy['Calorias'].sum() if not comidas_hoy.empty else 0
    prot_hoy = comidas_hoy['Proteinas'].sum() if not comidas_hoy.empty else 0
    carbs_hoy = comidas_hoy['Carbohidratos'].sum() if not comidas_hoy.empty else 0
    grasas_hoy = comidas_hoy['Grasas'].sum() if not comidas_hoy.empty else 0

    # 5. DASHBOARD VISUAL
    st.subheader("🎯 Resumen del Día")
    
    m1, m2, m3, m4 = st.columns(4)
    
    # Calorías con lógica de color
    restante_cal = user['Calorias_Meta'] - cal_hoy
    m1.metric("🔥 Calorías Restantes", f"{restante_cal} kcal", delta=f"{cal_hoy} consumidas", delta_color="inverse")
    
    # Proteínas (El macro más importante)
    m2.metric("🍗 Proteína", f"{prot_hoy}g / {user['Proteina_Meta']}g")
    
    # Otros macros
    m3.metric("🍞 Carbohidratos", f"{carbs_hoy}g")
    m4.metric("🥑 Grasas", f"{grasas_hoy}g")

    st.divider()

    # Barra de Progreso Visual
    col_prog, col_txt = st.columns([0.8, 0.2])
    porcentaje = min(cal_hoy / user['Calorias_Meta'], 1.0) if user['Calorias_Meta'] > 0 else 0
    
    with col_prog:
        st.write(f"**Progreso Calórico: {porcentaje*100:.1f}%**")
        st.progress(porcentaje)
    
    with col_txt:
        if porcentaje >= 1:
            st.warning("¡Meta alcanzada! 🏆")
        elif porcentaje > 0.8:
            st.info("Casi llegas...")
        else:
            st.success("¡Vas por buen camino!")

else:
    st.warning("👋 ¡Bienvenido! Parece que aún no has configurado tu perfil.")
    st.write("Andá a la sección ⚙️ **Configuración** en el menú lateral para establecer tus metas.")

# 6. HISTORIAL RÁPIDO
if not df_comidas.empty:
    with st.expander("👁️ Ver últimas comidas registradas"):
        st.table(df_comidas.tail(5))