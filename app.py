import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ==========================================
# CONFIGURACIÓN DE PÁGINA Y ESTILOS (CSS)
# ==========================================
st.set_page_config(
    page_title="La Voz que Une",
    page_icon="📰",
    layout="wide"
)

# Estilos personalizados (Verde institucional, franja tricolor, cinta deslizante)
st.markdown("""
    <style>
    /* Franja Tricolor Superior */
    .tricolor-bar {
        height: 6px;
        background: linear-gradient(to right, #D32F2F 33%, #FFFFFF 33%, #FFFFFF 66%, #1976D2 66%);
        margin-bottom: 15px;
        border-radius: 2px;
    }
    
    /* Encabezados y títulos institucionales */
    .main-title {
        color: #2E7D32;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
    }
    
    .sub-title {
        color: #4B4B4B;
        text-align: center;
        font-style: italic;
        margin-bottom: 25px;
    }

    /* Tarjetas de Noticias */
    .news-card {
        background-color: #F9F9F9;
        border-left: 5px solid #2E7D32;
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 4px;
    }

    /* Cinta de texto deslizante (Marquee) */
    .marquee-container {
        width: 100%;
        background-color: #2E7D32;
        color: white;
        padding: 8px 0;
        overflow: hidden;
        white-space: nowrap;
        box-sizing: border-box;
        margin-bottom: 25px;
        border-radius: 4px;
    }
    .marquee-text {
        display: inline-block;
        padding-left: 100%;
        animation: marquee 20s linear infinite;
        font-weight: 500;
    }
    @keyframes marquee {
        0%   { transform: translate(0, 0); }
        100% { transform: translate(-100%, 0); }
    }
    </style>
""", unsafe_allow_html=True)

# Clave de administración
CLAVE_ADMIN = "bosque2026"
ARCHIVO_DATOS = "datos_periodico.xlsx"

# ==========================================
# FUNCIONES PARA GESTIÓN DE DATOS
# ==========================================
def cargar_datos():
    columnas_estandar = ["Fecha", "Título", "Categoría", "Contenido", "Imagen_URL"]
    if os.path.exists(ARCHIVO_DATOS):
        try:
            df = pd.read_excel(ARCHIVO_DATOS)
            # Normalizar nombres de columnas si vienen en minúsculas
            mapeo = {}
            for col in df.columns:
                col_lower = str(col).strip().lower()
                if "tit" in col_lower:
                    mapeo[col] = "Título"
                elif "cat" in col_lower:
                    mapeo[col] = "Categoría"
                elif "cont" in col_lower:
                    mapeo[col] = "Contenido"
                elif "fec" in col_lower:
                    mapeo[col] = "Fecha"
                elif "img" in col_lower or "imagen" in col_lower:
                    mapeo[col] = "Imagen_URL"
            df = df.rename(columns=mapeo)
            
            # Asegurar que existan todas las columnas
            for c in columnas_estandar:
                if c not in df.columns:
                    df[c] = ""
            return df[columnas_estandar]
        except Exception:
            pass
    return pd.DataFrame(columns=columnas_estandar)

def guardar_datos(df):
    df.to_excel(ARCHIVO_DATOS, index=False)

# Inicializar datos en sesión
if 'noticias' not in st.session_state:
    st.session_state.noticias = cargar_datos()

# ==========================================
# ENCABEZADO PRINCIPAL
# ==========================================
st.markdown('<div class="tricolor-bar"></div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">LA VOZ QUE UNE</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Diario Comunitario e Informativo</p>', unsafe_allow_html=True)

# Cinta de aviso desplazable
aviso_texto = "Bienvenido a La Voz que Une — Periódico digital comunitario — Manténgase informado de las últimas noticias"
st.markdown(f'''
    <div class="marquee-container">
        <div class="marquee-text">{aviso_texto}</div>
    </div>
''', unsafe_allow_html=True)

# ==========================================
# NAVEGACIÓN Y PESTAÑAS
# ==========================================
tab_inicio, tab_admin = st.tabs(["📖 Portada / Noticias", "🔐 Administración"])

# ------------------------------------------
# PESTAÑA 1: PORTADA
# ------------------------------------------
with tab_inicio:
    df_noticias = st.session_state.noticias
    
    if df_noticias.empty:
        st.info("No hay publicaciones disponibles en este momento. Utilice el panel de administración para agregar la primera noticia.")
    else:
        for idx, row in df_noticias.iloc[::-1].iterrows():
            st.markdown('<div class="news-card">', unsafe_allow_html=True)
            
            titulo_val = row.get("Título", "Sin título")
            fecha_val = row.get("Fecha", "")
            cat_val = row.get("Categoría", "General")
            img_val = row.get("Imagen_URL", "")
            cont_val = row.get("Contenido", "")

            st.subheader(titulo_val)
            st.caption(f"📅 Publicado el: {fecha_val} | Categoría: {cat_val}")
            
            if pd.notna(img_val) and str(img_val).strip() != "":
                st.image(str(img_val), use_container_width=True)
            
            contenido_formateado = str(cont_val).replace("\n", "\n\n")
            st.markdown(contenido_formateado)
            st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# PESTAÑA 2: ADMINISTRACIÓN
# ------------------------------------------
with tab_admin:
    st.header("Panel de Control Editorial")
    
    password = st.text_input("Ingrese la contraseña de administración:", type="password")
    
    if password == CLAVE_ADMIN:
        st.success("Acceso concedido como Administrador.")
        
        st.subheader("Publicar Nueva Noticia")
        with st.form("form_nueva_noticia", clear_on_submit=True):
            titulo = st.text_input("Título del Artículo")
            categoria = st.selectbox("Categoría", ["Comunidad", "Educación", "Cultura", "Declaraciones", "General"])
            imagen_url = st.text_input("Ruta o enlace de la imagen (ej: nombre_imagen.jpg o URL)")
            contenido = st.text_area("Cuerpo de la noticia (Deje una línea en blanco entre párrafos):", height=200)
            
            submit = st.form_submit_button("Publicar Noticia")
            
            if submit:
                if titulo and contenido:
                    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")
                    nueva_fila = pd.DataFrame([{
                        "Fecha": fecha_actual,
                        "Título": titulo,
                        "Categoría": categoria,
                        "Contenido": contenido,
                        "Imagen_URL": imagen_url
                    }])
                    
                    st.session_state.noticias = pd.concat([st.session_state.noticias, nueva_fila], ignore_index=True)
                    guardar_datos(st.session_state.noticias)
                    st.success("¡Noticia publicada con éxito! Vaya a la pestaña 'Portada / Noticias' para visualizarla.")
                    st.rerun()
                else:
                    st.warning("Por favor complete al menos el título y el contenido.")
    elif password != "":
        st.error("Contraseña incorrecta.")
