import streamlit as st

st.set_page_config(
page_title="La Voz Que Une",
page_icon="📰",
layout="wide"
)

st.markdown("""
<style>
.header-container {
    background: linear-gradient(135deg, #1E3A8A 0%, #0D9488 100%);
    padding: 25px;
    border-radius: 12px;
    text-align: center;
    color: white;
    margin-bottom: 15px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.header-title {
    font-family: 'Helvetica Neue', sans-serif;
    font-size: 2.8em;
    font-weight: 800;
    margin: 0;
    letter-spacing: 1px;
}
.header-sub {
    font-size: 1.2em;
    opacity: 0.9;
    margin-top: 5px;
}
.marquee-container {
    background-color: #F3F4F6;
    border-left: 5px solid #1E3A8A;
    padding: 8px 15px;
    margin-bottom: 25px;
    border-radius: 4px;
    overflow: hidden;
    white-space: nowrap;
}
.marquee-text {
    display: inline-block;
    font-weight: 600;
    color: #1F2937;
    animation: marquee 18s linear infinite;
}
@keyframes marquee {
    0% { transform: translateX(100%); }
    100% { transform: translateX(-100%); }
}
.stButton>button {
    width: 100%;
    background-color: #1E3A8A;
    color: white;
    font-weight: bold;
    border-radius: 6px;
}
</style>
""", unsafe_allow_html=True)

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

st.markdown("""
<div class="header-container">
    <div class="header-title">📰 LA VOZ QUE UNE</div>
    <div class="header-sub">Portal Digital Comunitario e Informativo</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="marquee-container">
    <span class="marquee-text">🔔 ÚLTIMA HORA: Bienvenidos a la nueva plataforma digital de La Voz Que Une &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp; 📌 Revise las últimas noticias comunitarias en nuestra edición digital</span>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab_admin = st.tabs([
"🗞️ Noticias", 
"📸 Galería", 
"📢 Avisos Económicos", 
"🎭 Humor", 
"📜 Historia de la Población",
"⚙️ Administración"
])

with tab1:
if not st.session_state.noticias:
    st.info("No hay noticias publicadas en este momento.")
else:
    for noticia in st.session_state.noticias:
        st.caption(f"Categoría: **{noticia['categoria']}**")
        st.title(noticia["titulo"])
        if noticia.get("bajada"):
            st.subheader(noticia["bajada"])
        
        img1 = noticia.get("imagen1", "").strip()
        img2 = noticia.get("imagen2", "").strip()
        
        if img1 and img2:
            col1, col2 = st.columns(2)
            with col1:
                st.image(img1, caption=noticia.get("pie1", ""), use_container_width=True)
            with col2:
                st.image(img2, caption=noticia.get("pie2", ""), use_container_width=True)
        elif img1:
            col_izq, col_centro, col_der = st.columns([1, 2, 1])
            with col_centro:
                st.image(img1, caption=noticia.get("pie1", ""), use_container_width=True)
        elif img2:
            col_izq, col_centro, col_der = st.columns([1, 2, 1])
            with col_centro:
                st.image(img2, caption=noticia.get("pie2", ""), use_container_width=True)

        st.markdown(noticia["contenido"])
        st.divider()

with tab2:
st.header("📸 Galería Fotográfica Comunitaria")
st.write("Imágenes de nuestros eventos, actividades y rincones de la comunidad.")
col_g1, col_g2, col_g3 = st.columns(3)
with col_g1:
    st.image("https://images.unsplash.com/photo-1511632765486-a01980e01a18?w=500", caption="Encuentro Vecinal", use_container_width=True)
with col_g2:
    st.image("https://images.unsplash.com/photo-1577495508048-b635879837f1?w=500", caption="Actividades al Aire Libre", use_container_width=True)
with col_g3:
    st.image("https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=500", caption="Talleres Comunitarios", use_container_width=True)

with tab3:
st.header("📢 Clasificados y Avisos Económicos")
st.write("Espacio destinado para pymes, emprendedores y servicios de nuestros vecinos.")
col_a1, col_a2 = st.columns(2)
with col_a1:
    st.info("🛠️ **Servicios de Carpintería y Reparaciones**\n\nConfección de muebles a medida, trabajos en madera e intarsia.\n\n📞 *Contacto: Vecino Central*")
with col_a2:
    st.success("🍞 **Panadería y Pastelería Artesanal**\n\nPan fresco y amasado todos los días a partir de las 17:00 hrs.\n\n📞 *Contacto: Local 3*")

with tab4:
st.header("🎭 El Rincón del Humor")
st.write("Un espacio para la alegría y el buen humor de nuestra población.")
st.markdown("""
> **Risa del día:**
> 
> — ¡Mamá, mamá! En la escuela me dicen que soy muy distraído.
> 
> — Niño, ¡tú vives en la casa de al lado! 😅
""")

with tab5:
st.header("📜 Historia de Nuestra Población")
st.markdown("""
Nuestra comunidad fue fundada gracias al esfuerzo, la organización y el trabajo mancomunado de familias que buscaban un futuro mejor.

A través de las décadas, el espíritu solidario ha mantenido viva la identidad de nuestro barrio, construyendo pasaje a pasaje la historia que hoy compartimos con orgullo.
""")

with tab_admin:
st.header("⚙️ Panel de Control del Editor")
password = st.text_input("Ingrese la clave de administrador para publicar:", type="password")

if password == "bosque2026":
    st.success("Acceso concedido.")
    st.subheader("📝 Publicar Nueva Noticia")
    
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
            st.session_state.noticias.insert(0, nueva_noticia)
            st.success("¡Noticia publicada con éxito! Vaya a la pestaña 'Noticias' para verla.")
            st.rerun()
elif password != "":
    st.error("Clave incorrecta. Por favor intente nuevamente.")

st.markdown("---")
st.markdown(
"<div style='text-align: center; color: #6B7280; font-size: 0.9em;'>"
"© La Voz Que Une - Portal Digital Comunitario | Desarrollado con Streamlit"
"</div>", 
unsafe_allow_html=True
)
