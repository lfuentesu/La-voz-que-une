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

CLAVE_EDITORIAL = "bosque2026"
ARCHIVO_DATOS = "datos_periodico.xlsx"

# ---------------------------------------------------------
# CARGA Y LIMPIEZA DE DATOS
# ---------------------------------------------------------
def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        df = pd.read_excel(ARCHIVO_DATOS)
        df.columns = [str(c).strip().lower() for c in df.columns]
        return df
    else:
        return pd.DataFrame(columns=[
            "id", "fecha", "titulo", "categoria", "contenido", 
            "autor", "imagen", "estado"
        ])

def guardar_datos(df):
    df.to_excel(ARCHIVO_DATOS, index=False)

df_datos = cargar_datos()

# Asegurar columnas requeridas
columnas_requeridas = ["id", "fecha", "titulo", "categoria", "contenido", "autor", "imagen", "estado"]
for col in columnas_requeridas:
    if col not in df_datos.columns:
        df_datos[col] = ""

# Función auxiliar para limpiar textos y evitar "nan"
def obtener_texto(val, por_defecto=""):
    if pd.isna(val) or str(val).strip().lower() in ['nan', 'none', '']:
        return por_defecto
    return str(val).strip()

# ---------------------------------------------------------
# ESTILOS VISUALES
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

# Filtrar publicaciones aprobadas y válidas (no vacías)
def es_aprobado(val):
    v = str(val).strip().lower()
    return v in ['aprobado', 'aprobada', 'true']

df_aprobados = df_datos[df_datos['estado'].apply(es_aprobado)].copy()

# ---------------------------------------------------------
# 1. PESTAÑA: INICIO
# ---------------------------------------------------------
if pestaña == "🏠 Inicio":
    st.header("🏠 Noticias y Publicaciones Recientes")
    
    # Filtrar publicaciones que tengan al menos título o contenido real
    df_inicio_valido = df_aprobados[df_aprobados['titulo'].apply(lambda x: obtener_texto(x) != "") | 
                                   df_aprobados['contenido'].apply(lambda x: obtener_texto(x) != "")]
    
    if df_inicio_valido.empty:
        st.info("Aún no hay publicaciones en la portada.")
    else:
        for _, row in df_inicio_valido.iterrows():
            titulo = obtener_texto(row.get('titulo'), "Sin título")
            contenido = obtener_texto(row.get('contenido'), "")
            autor = obtener_texto(row.get('autor'), "Vecino de El Bosque 1")
            fecha = obtener_texto(row.get('fecha'), "")
            categoria = obtener_texto(row.get('categoria'), "General")
            imagen = obtener_texto(row.get('imagen'), "")

            st.markdown(f"""
            <div class="card-noticia">
                <span style="color:#888; font-size:0.85rem;">{fecha} | Categoría: <b>{categoria}</b></span>
                <h3 style="margin-top:5px; color:#1E5631;">{titulo}</h3>
                <p>{contenido}</p>
                <small><b>Por:</b> {autor}</small>
            </div>
            """, unsafe_allow_html=True)
            
            if imagen != "":
                st.image(imagen, use_column_width=True)
            st.divider()

# ---------------------------------------------------------
# 2. PESTAÑA: MEMORIA E HISTORIA
# ---------------------------------------------------------
elif pestaña == "📜 Memoria e Historia":
    st.header("📜 Memoria e Historia de Nuestro Barrio")
    st.write("Relatos, fotografías y recuerdos del camino recorrido por los pobladores de El Bosque 1 y La Pincoya.")
    
    df_historia = df_aprobados[df_aprobados['categoria'].astype(str).str.strip().str.lower() == 'memoria e historia']
    
    if df_historia.empty:
        st.info("No hay relatos históricos publicados todavía en esta pestaña.")
    else:
        for _, row in df_historia.iterrows():
            titulo = obtener_texto(row.get('titulo'), "Sin título")
            contenido = obtener_texto(row.get('contenido'), "")
            autor = obtener_texto(row.get('autor'), "Anónimo")
            fecha = obtener_texto(row.get('fecha'), "")
            imagen = obtener_texto(row.get('imagen'), "")

            st.markdown(f"### {titulo}")
            st.caption(f"Publicado el {fecha} | Relatado por: {autor}")
            st.write(contenido)
            if imagen != "":
                st.image(imagen, use_column_width=True)
            st.divider()

# ---------------------------------------------------------
# 3. PESTAÑA: GALERÍA DE FOTOS
# ---------------------------------------------------------
elif pestaña == "📸 Galería":
    st.header("📸 Galería Fotográfica")
    st.write("Retratos de nuestros eventos, reuniones, vecinos e historia visual comunitaria.")
    
    df_galeria = df_aprobados[df_aprobados['imagen'].apply(lambda x: obtener_texto(x) != "")]
    
    if df_galeria.empty:
        st.info("Aún no hay imágenes publicadas en la galería.")
    else:
        cols = st.columns(3)
        for idx, (_, row) in enumerate(df_galeria.iterrows()):
            with cols[idx % 3]:
                st.image(row['imagen'], use_column_width=True)
                st.caption(f"**{obtener_texto(row.get('titulo'), '')}**\n_{obtener_texto(row.get('fecha'), '')}_")

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
            st.warning(f"**{obtener_texto(row.get('titulo'), '')}**\n\n{obtener_texto(row.get('contenido'), '')}\n\n_Contacto / Autor: {obtener_texto(row.get('autor'), 'Vecino')}_")

# ---------------------------------------------------------
# 5. PESTAÑA: PARTICIPA
# ---------------------------------------------------------
elif pestaña == "✍️ Participa":
    st.header("✍️ Envía tu Noticia, Relato o Aviso")
    st.write("Escribe tu aporte para que el equipo editorial lo revise.")
    
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
        
        enviado = st.form_submit_button("📤 Enviar para Revisión")
        
        if enviado:
            if titulo.strip() == "" or contenido.strip() == "":
                st.error("Por favor completa el título y el contenido.")
            else:
                nueva_fila = {
                    "id": len(df_datos) + 1,
                    "fecha": pd.Timestamp.now().strftime("%Y-%m-%d"),
                    "titulo": titulo,
                    "categoria": categoria,
                    "contenido": contenido,
                    "autor": nombre if nombre.strip() != "" else "Vecino",
                    "imagen": "",
                    "estado": "Pendiente"
                }
                df_datos = pd.concat([df_datos, pd.DataFrame([nueva_fila])], ignore_index=True)
                guardar_datos(df_datos)
                st.success("¡Muchas gracias! Tu publicación ha sido enviada al equipo editorial.")

# ---------------------------------------------------------
# 6. PESTAÑA: ADMINISTRACIÓN
# ---------------------------------------------------------
elif pestaña == "🔒 Administración":
    st.header("🔒 Panel de Administración Editorial")
    
    clave_ingresada = st.text_input("Ingresa la clave secreta:", type="password")
    
    if clave_ingresada == CLAVE_EDITORIAL:
        st.success("Acceso concedido al Equipo Editorial.")
        
        st.subheader("📋 Registros en la Base de Datos")
        st.dataframe(df_datos[['id', 'fecha', 'titulo', 'categoria', 'autor', 'estado']])
        
        st.subheader("📌 Publicaciones Pendientes")
        df_pendientes = df_datos[df_datos['estado'].astype(str).str.strip().str.lower() == 'pendiente']
        
        if df_pendientes.empty:
            st.info("No hay publicaciones pendientes por revisar.")
        else:
            for idx, row in df_pendientes.iterrows():
                with st.expander(f"Revisar: {obtener_texto(row.get('titulo'), 'Sin título')}"):
                    st.write(f"**Autor:** {obtener_texto(row.get('autor'), 'Anónimo')}")
                    st.write(f"**Categoría:** {obtener_texto(row.get('categoria'), 'General')}")
                    st.write(f"**Contenido:** {obtener_texto(row.get('contenido'), '')}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"✅ Aprobar #{row['id']}", key=f"ap_{row['id']}"):
                            df_datos.loc[df_datos['id'] == row['id'], 'estado'] = 'Aprobado'
                            guardar_datos(df_datos)
                            st.rerun()
                    with col2:
                        if st.button(f"🗑️ Descartar #{row['id']}", key=f"desc_{row['id']}"):
                            df_datos = df_datos[df_datos['id'] != row['id']]
                            guardar_datos(df_datos)
                            st.rerun()
    elif clave_ingresada != "":
        st.error("Clave incorrecta.")
