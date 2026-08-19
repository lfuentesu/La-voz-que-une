import streamlit as st
import pandas as pd
import os

# ---------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Periódico Digital El Bosque 1",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clave de acceso para el equipo editorial (Ajustable)
CLAVE_EDITORIAL = "bosque2026"
ARCHIVO_DATOS = "datos_periodico.xlsx"

# ---------------------------------------------------------
# CARGA Y GUARDADO DE DATOS
# ---------------------------------------------------------
def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        df = pd.read_excel(ARCHIVO_DATOS)
        # Normalizar nombres de columnas por seguridad
        df.columns = [str(c).strip().lower() for c in df.columns]
        return df
    else:
        # Estructura base en caso de que no exista el archivo
        return pd.DataFrame(columns=[
            "id", "fecha", "titulo", "categoria", "contenido", 
            "autor", "imagen", "estado"
        ])

def guardar_datos(df):
    df.to_excel(ARCHIVO_DATOS, index=False)

df_datos = cargar_datos()

# Asegurar que existan las columnas necesarias
columnas_requeridas = ["id", "fecha", "titulo", "categoria", "contenido", "autor", "imagen", "estado"]
for col in columnas_requeridas:
    if col not in df_datos.columns:
        df_datos[col] = ""

# ---------------------------------------------------------
# ESTILOS VISUALES Y CABECERA COLORIDA
# ---------------------------------------------------------
st.markdown("""
    <style>
    .main-title {
        color: #1E5631;
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .sub-title {
        color: #333333;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 20px;
    }
    .card-noticia {
        background-color: #F4F9F4;
        padding: 18px;
        border-radius: 10px;
        border-left: 5px solid #1E5631;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🌳 Periódico Digital El Bosque 1</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">La Voz que Une a Nuestra Comunidad • La Pincoya, Huechuraba</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# MENÚ DE NAVEGACIÓN
# ---------------------------------------------------------
opciones_menu = [
    "🏠 Inicio", 
    "📜 Memoria e Historia", 
    "📸 Galería", 
    "📢 Avisos Comunitarios", 
    "✍️ Participa", 
    "🔒 Administración"
]

pestaña = st.sidebar.radio("Navegación", opciones_menu)

# Filtrar solo publicaciones aprobadas para el público
df_aprobados = df_datos[df_datos['estado'].astype(str).str.lower() == 'aprobado'].copy()

# ---------------------------------------------------------
# 1. PESTAÑA: INICIO
# ---------------------------------------------------------
if pestaña == "🏠 Inicio":
    st.header("🏠 Noticias y Publicaciones Recientes")
    
    if df_aprobados.empty:
        st.info("Aún no hay publicaciones en la portada. ¡Sé el primero en enviar tu historia en la sección Participa!")
    else:
        for _, row in df_aprobados.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="card-noticia">
                    <span style="color:#888; font-size:0.85rem;">{row.get('fecha', '')} | Categoría: <b>{row.get('categoria', 'General')}</b></span>
                    <h3 style="margin-top:5px; color:#1E5631;">{row.get('titulo', '')}</h3>
                    <p>{row.get('contenido', '')}</p>
                    <small><b>Por:</b> {row.get('autor', 'Vecino de El Bosque 1')}</small>
                </div>
                """, unsafe_allow_html=True)
                
                if pd.notna(row.get('imagen')) and str(row.get('imagen')).strip() != "":
                    st.image(row['imagen'], use_column_width=True)
                st.divider()

# ---------------------------------------------------------
# 2. PESTAÑA: MEMORIA E HISTORIA
# ---------------------------------------------------------
elif pestaña == "📜 Memoria e Historia":
    st.header("📜 Memoria e Historia de Nuestro Barrio")
    st.write("Relatos, fotografías y recuerdos del camino recorrido por los pobladores de El Bosque 1 y La Pincoya.")
    
    # Filtro exacto para la categoría Memoria e Historia
    df_historia = df_aprobados[df_aprobados['categoria'].astype(str).str.strip().str.lower() == 'memoria e historia']
    
    if df_historia.empty:
        st.info("No hay relatos históricos publicados todavía. Puedes enviar tus memorias en la pestaña 'Participa'.")
    else:
        for _, row in df_historia.iterrows():
            st.markdown(f"### {row.get('titulo', '')}")
            st.caption(f"Publicado el {row.get('fecha', '')} | Relatado por: {row.get('autor', 'Anónimo')}")
            st.write(row.get('contenido', ''))
            if pd.notna(row.get('imagen')) and str(row.get('imagen')).strip() != "":
                st.image(row['imagen'], use_column_width=True)
            st.divider()

# ---------------------------------------------------------
# 3. PESTAÑA: GALERÍA DE FOTOS (NUEVA)
# ---------------------------------------------------------
elif pestaña == "📸 Galería":
    st.header("📸 Galería Fotográfica")
    st.write("Retratos de nuestros eventos, reuniones, vecinos e historia visual comunitaria.")
    
    # Buscar registros que tengan imagen y estén aprobados
    df_galeria = df_aprobados[df_aprobados['imagen'].notna() & (df_aprobados['imagen'].astype(str).str.strip() != "")]
    
    if df_galeria.empty:
        st.info("Aún no se han publicado imágenes en la galería. ¡Envía tus fotografías desde la pestaña 'Participa'!")
    else:
        cols = st.columns(3)  # Organizar en 3 columnas
        for idx, (_, row) in enumerate(df_galeria.iterrows()):
            with cols[idx % 3]:
                st.image(row['imagen'], use_column_width=True)
                st.caption(f"**{row.get('titulo', '')}**\n_{row.get('fecha', '')}_")

# ---------------------------------------------------------
# 4. PESTAÑA: AVISOS COMUNITARIOS
# ---------------------------------------------------------
elif pestaña == "📢 Avisos Comunitarios":
    st.header("📢 Avisos y Datos del Barrio")
    
    df_avisos = df_aprobados[df_aprobados['categoria'].astype(str).str.strip().str.lower() == 'avisos comunitarios']
    
    if df_avisos.empty:
        st.info("No hay avisos vigentes en este momento.")
    else:
        for _, row in df_avisos.iterrows():
            st.warning(f"**{row.get('titulo', '')}**\n\n{row.get('contenido', '')}\n\n_Contacto / Autor: {row.get('autor', '')}_")

# ---------------------------------------------------------
# 5. PESTAÑA: PARTICIPA (FORMULARIO PÚBLICO)
# ---------------------------------------------------------
elif pestaña == "✍️ Participa":
    st.header("✍️ Envía tu Noticia, Relato o Aviso")
    st.write("Escribe tu aporte. El equipo editorial lo revisará antes de ser publicado en la portada.")
    
    with st.form("form_participa", clear_on_submit=True):
        nombre = st.text_input("Tu Nombre o Apodo:")
        categoria = st.selectbox("Selecciona la Sección:", [
            "Inicio", 
            "Memoria e Historia", 
            "Galería", 
            "Avisos Comunitarios"
        ])
        titulo = st.text_input("Título de la Publicación:")
        contenido = st.text_area("Escribe tu texto aquí:")
        enlace_imagen = st.text_input("Enlace de imagen (Opcional - URL pública):")
        
        enviado = st.form_submit_button("📤 Enviar para Revisión")
        
        if enviado:
            if titulo.strip() == "" or contenido.strip() == "":
                st.error("Por favor completa al menos el título y el contenido.")
            else:
                nueva_fila = {
                    "id": len(df_datos) + 1,
                    "fecha": pd.Timestamp.now().strftime("%Y-%m-%d"),
                    "titulo": titulo,
                    "categoria": categoria,
                    "contenido": contenido,
                    "autor": nombre if nombre.strip() != "" else "Vecino",
                    "imagen": enlace_imagen,
                    "estado": "Pendiente"
                }
                df_datos = pd.concat([df_datos, pd.DataFrame([nueva_fila])], ignore_index=True)
                guardar_datos(df_datos)
                st.success("¡Muchas gracias! Tu publicación ha sido enviada al equipo editorial para su aprobación.")

# ---------------------------------------------------------
# 6. PESTAÑA: ADMINISTRACIÓN (PANEL EDITORIAL)
# ---------------------------------------------------------
elif pestaña == "🔒 Administración":
    st.header("🔒 Panel de Administración Editorial")
    
    clave_ingresada = st.text_input("Ingresa la clave secreta:", type="password")
    
    if clave_ingresada == CLAVE_EDITORIAL:
        st.success("Acceso concedido al Equipo Editorial.")
        
        df_pendientes = df_datos[df_datos['estado'].astype(str).str.lower() == 'pendiente']
        
        st.subheader("📌 Publicaciones Pendientes de Revisión")
        if df_pendientes.empty:
            st.info("No hay publicaciones pendientes por revisar.")
        else:
            for idx, row in df_pendientes.iterrows():
                with st.expander(f"Revisar: {row.get('titulo', 'Sin título')} (Por: {row.get('autor', 'Anónimo')})"):
                    st.write(f"**Categoría:** {row.get('categoria', '')}")
                    st.write(f"**Contenido:** {row.get('contenido', '')}")
                    if pd.notna(row.get('imagen')) and str(row.get('imagen')).strip() != "":
                        st.image(row['imagen'], width=300)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"✅ Aprobar y Publicar #{row['id']}", key=f"ap_{row['id']}"):
                            df_datos.loc[df_datos['id'] == row['id'], 'estado'] = 'Aprobado'
                            guardar_datos(df_datos)
                            st.rerun()
                    with col2:
                        if st.button(f"🗑️ Descartar #{row['id']}", key=f"desc_{row['id']}"):
                            df_datos = df_datos[df_datos['id'] != row['id']]
                            guardar_datos(df_datos)
                            st.rerun()
    elif clave_ingresada != "":
        st.error("Clave incorrecta. Consulta con el equipo editorial.")
