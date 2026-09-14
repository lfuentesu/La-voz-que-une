import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="La Voz Que Une",
    page_icon="📰",
    layout="wide"
)

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #1E3A8A;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: bold;
        padding-bottom: 5px;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        color: #4B5563;
        font-size: 1.1em;
        margin-bottom: 25px;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E3A8A;
        color: white;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZACIÓN DEL ESTADO DE SESIÓN ---
if "noticias" not in st.session_state:
    st.session_state.noticias = [
        {
            "titulo": "Bienvenidos a La Voz Que Une",
            "categoria": "Comunidad",
            "bajada": "El nuevo portal digital comunitario al servicio de nuestros vecinos.",
            "contenido": """Estamos muy felices de presentar **La Voz Que Une**, un espacio diseñado para informar, conectar y destacar las iniciativas de nuestra comunidad. 
            
A través de este portal, compartiremos noticias locales, eventos, historias de vecinos y toda la información relevante para nuestro entorno.""",
            "imagen1": "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=600",
            "pie1": "Periodismo comunitario y participativo.",
            "imagen2": "",
            "pie2": ""
        }
    ]

# --- CABECERA PRINCIPAL ---
st.markdown("<h1 class='main-title'>📰 LA VOZ QUE UNE</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Diario Digital Comunitario</p>", unsafe_allow_html=True)
st.divider()

# --- NAVEGACIÓN PRINCIPAL ---
pestaña1, pestaña2 = st.tabs(["🗞️ Edición Impresa / Noticias", "⚙️ Panel de Administración"])

# ==========================================
# PESTAÑA 1: PORTADA Y NOTICIAS
# ==========================================
with pestaña1:
    if not st.session_state.noticias:
        st.info("No hay noticias publicadas en este momento.")
    else:
        for i, noticia in enumerate(st.session_state.noticias):
            st.caption(f"Categoría: **{noticia['categoria']}**")
            st.title(noticia["titulo"])
            if noticia.get("bajada"):
                st.subheader(noticia["bajada"])
            
            # --- MANEJO OPTIMIZADO DE IMÁGENES ---
            img1 = noticia.get("imagen1", "").strip()
            img2 = noticia.get("imagen2", "").strip()
            
            # CASO A: Dos imágenes (Se muestran lado a lado en 2 columnas)
            if img1 and img2:
                col1, col2 = st.columns(2)
                with col1:
                    st.image(img1, caption=noticia.get("pie1", ""), use_container_width=True)
                with col2:
                    st.image(img2, caption=noticia.get("pie2", ""), use_container_width=True)
            
            # CASO B: Una sola imagen (Se muestra centrada y a tamaño moderado)
            elif img1:
                col_izq, col_centro, col_der = st.columns([1, 2, 1])
                with col_centro:
                    st.image(img1, caption=noticia.get("pie1", ""), use_container_width=True)
            elif img2:
                col_izq, col_centro, col_der = st.columns([1, 2, 1])
                with col_centro:
                    st.image(img2, caption=noticia.get("pie2", ""), use_container_width=True)

            # Contenido del texto de la noticia
            st.markdown(noticia["contenido"])
            st.divider()

# ==========================================
# PESTAÑA 2: PANEL DE ADMINISTRACIÓN
# ==========================================
with pestaña2:
    st.header("📝 Publicar Nueva Noticia")
    st.write("Complete el siguiente formulario para ingresar una nueva publicación al portal:")
    
    with st.form("form_noticia", clear_on_submit=True):
        titulo = st.text_input("Título de la Noticia *")
        categoria = st.selectbox("Categoría *", ["Comunidad", "Cultura", "Educación", "Deportes", "Avisos"])
        bajada = st.text_input("Subtítulo / Bajada resumen")
        contenido = st.text_area("Cuerpo del Artículo (admite formato Markdown) *", height=200)
        
        st.markdown("---")
        st.markdown("##### 🖼️ Imágenes del Artículo (Opcional)")
        
        col_img1, col_img2 = st.columns(2)
        with col_img1:
            imagen1 = st.text_input("URL Imagen 1 (Enlace directo)")
            pie1 = st.text_input("Pie de Foto 1")
            
        with col_img2:
            imagen2 = st.text_input("URL Imagen 2 (Enlace directo)")
            pie2 = st.text_input("Pie de Foto 2")

        boton_publicar = st.form_submit_button("🚀 Publicar Noticia")

    if boton_publicar:
        if not titulo or not contenido:
            st.error("Por favor complete los campos obligatorios (Título y Contenido).")
        else:
            nueva_noticia = {
                "titulo": titulo,
                "categoria": categoria,
                "bajada": bajada,
                "contenido": contenido,
                "imagen1": imagen1,
                "pie1": pie1,
                "imagen2": imagen2,
                "pie2": pie2
            }
            # Se inserta al inicio de la lista para que aparezca primero
            st.session_state.noticias.insert(0, nueva_noticia)
            st.success("¡Noticia publicada con éxito! Vaya a la pestaña 'Edición Impresa / Noticias' para verla.")
            st.rerun()

# --- PIE DE PÁGINA ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #6B7280; font-size: 0.9em;'>"
    "© La Voz Que Une - Portal Digital Comunitario | Desarrollado con Streamlit"
    "</div>", 
    unsafe_allow_html=True
)