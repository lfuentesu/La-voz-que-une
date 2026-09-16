import streamlit as st

# Configuración inicial de la página
st.set_page_config(
    page_title="La Voz Que Une",
    page_icon="📰",
    layout="wide"
)

# --- INICIALIZACIÓN DE VARIABLES EN MEMORIA (SESSION STATE) ---
if "mensaje_diario" not in st.session_state:
    st.session_state.mensaje_diario = "«La fuerza de nuestra comunidad radica en la unión, el respeto y la colaboración diaria entre vecinos.»"

if "avisos_pendientes" not in st.session_state:
    st.session_state.avisos_pendientes = [
        {"vecino": "María González", "tipo": "Ofrecimiento", "texto": "Servicio de costura y arreglos de ropa.", "imagen": None},
        {"vecino": "Juan Pérez", "tipo": "Aviso", "texto": "Se busca mascota extraviada (gato amarillo).", "imagen": None}
    ]

if "galeria_fotos" not in st.session_state:
    st.session_state.galeria_fotos = []

# --- 1. BANNER OFICIAL CON IMAGEN ---
try:
    st.image("banner.jpeg", use_container_width=True)
except Exception:
    st.title("📰 LA VOZ QUE UNE")
    st.caption("Portal Digital Comunitario e Informativo - Población El Bosque")

st.write("")

# --- 2. MENSAJE DIARIO DESPLAZABLE (MARQUESINA) ---
mensaje_html = f"""
<div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 10px; border-radius: 8px; margin-bottom: 15px;">
    <marquee behavior="scroll" direction="left" scrollamount="6" style="color: #166534; font-weight: bold; font-size: 1.05em;">
        📌 MENSAJE DEL DÍA: {st.session_state.mensaje_diario}
    </marquee>
</div>
"""
st.markdown(mensaje_html, unsafe_allow_html=True)

st.write("---")

# Definición de pestañas principales
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Noticias", 
    "Galería", 
    "Avisos Económicos", 
    "Participación Vecinal",
    "Humor", 
    "Historia de la Población", 
    "Administración"
])

# --- Pestaña 1: Noticias ---
with tab1:
    st.header("📌 Noticias Locales")
    st.write("Bienvenido al portal informativo comunal de la Población El Bosque.")

# --- Pestaña 2: Galería de Fotos ---
with tab2:
    st.header("📸 Galería Comunitaria")
    st.write("Espacio fotográfico de nuestros eventos e historia vecinal.")
    
    if len(st.session_state.galeria_fotos) == 0:
        st.info("Aún no hay fotografías publicadas en la galería.")
    else:
        cols = st.columns(3)
        for idx, foto in enumerate(st.session_state.galeria_fotos):
            with cols[idx % 3]:
                st.image(foto["archivo"], caption=foto["descripcion"], use_container_width=True)

# --- Pestaña 3: Avisos Económicos ---
with tab3:
    st.header("💼 Avisos Económicos")
    st.write("Clasificados, emprendimientos y servicios de los vecinos.")

# --- Pestaña 4: Participación Vecinal (Con envío de imágenes) ---
with tab4:
    st.header("🤝 Participación de los Vecinos")
    st.write("Envíe su aviso, propuesta, comentario o fotografía para ser publicado en el portal.")
    
    with st.form("form_participacion"):
        nombre = st.text_input("Su Nombre y Apellido:")
        tipo_aporte = st.selectbox("Tipo de publicación:", ["Aviso Económico", "Noticia / Aporte", "Fotografía para Galería", "Sugerencia"])
        mensaje = st.text_area("Escriba su mensaje o detalle de la publicación:")
        imagen_adjunta = st.file_uploader("Adjuntar una imagen o fotografía (opcional):", type=["jpg", "jpeg", "png"])
        enviado = st.form_submit_button("Enviar para revisión")
        
        if enviado:
            if nombre.strip() != "" and (mensaje.strip() != "" or imagen_adjunta is not None):
                st.session_state.avisos_pendientes.append({
                    "vecino": nombre,
                    "tipo": tipo_aporte,
                    "texto": mensaje,
                    "imagen": imagen_adjunta
                })
                st.success("¡Gracias! Su aporte ha sido enviado a la administración para revisión y aprobación.")
            else:
                st.warning("Por favor complete su nombre y un mensaje o imagen antes de enviar.")

# --- Pestaña 5: Humor ---
with tab5:
    st.header("😄 Espacio de Humor")
    st.write("Chistes, tiras cómicas y contenido de entretenimiento vecinal.")

# --- Pestaña 6: Historia ---
with tab6:
    st.header("📜 Historia de la Población")
    st.write("Relatos, fundadores y memoria histórica de nuestra comunidad.")

# --- Pestaña 7: Administración Protegida ---
with tab7:
    st.header("⚙️ Administración del Portal")
    
    clave = st.text_input("Ingrese la clave de administrador:", type="password")
    
    # Recuerde que puede personalizar la clave sustituyendo "1234"
    if clave == "1234":
        st.success("Acceso concedido al Panel de Control.")
        
        # --- A. CAMBIAR MENSAJE DIARIO ---
        st.subheader("📝 Editar Mensaje del Día (Desplazable)")
        nuevo_mensaje = st.text_input("Nuevo mensaje:", value=st.session_state.mensaje_diario)
        if st.button("Actualizar Mensaje"):
            st.session_state.mensaje_diario = nuevo_mensaje
            st.success("¡El mensaje del día ha sido actualizado con éxito!")
            st.rerun()
            
        st.write("---")
        
        # --- B. SUBIR FOTOS DIRECTAS A LA GALERÍA ---
        st.subheader("📸 Subir Imagen Directa a la Galería")
        imagen_subida = st.file_uploader("Seleccione una imagen (JPG, PNG):", type=["jpg", "jpeg", "png"], key="admin_uploader")
        descripcion_foto = st.text_input("Descripción o pie de foto:")
        
        if st.button("Publicar Imagen"):
            if imagen_subida is not None:
                st.session_state.galeria_fotos.append({
                    "archivo": imagen_subida,
                    "descripcion": descripcion_foto
                })
                st.success("¡Imagen publicada en la Galería Comunitaria!")
                st.rerun()
            else:
                st.warning("Por favor seleccione un archivo de imagen primero.")
                
        st.write("---")
        
        # --- C. GESTIÓN DE AVISOS Y FOTOS PENDIENTES ---
        st.subheader("📋 Solicitudes de Vecinos Pendientes")
        if len(st.session_state.avisos_pendientes) == 0:
            st.info("No hay publicaciones ni fotos pendientes de aprobación.")
        else:
            for i, aviso in enumerate(list(st.session_state.avisos_pendientes)):
                with st.expander(f"Solicitud de: {aviso['vecino']} ({aviso['tipo']})"):
                    if aviso['texto']:
                        st.write(f"**Mensaje:** {aviso['texto']}")
                    if aviso.get('imagen') is not None:
                        st.image(aviso['imagen'], caption="Imagen adjunta por el vecino", width=300)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"Aprobar", key=f"aprob_{i}"):
                            # Si es una foto para galería, se agrega a la galería
                            if aviso['tipo'] == "Fotografía para Galería" and aviso.get('imagen') is not None:
                                st.session_state.galeria_fotos.append({
                                    "archivo": aviso['imagen'],
                                    "descripcion": f"Enviada por {aviso['vecino']}: {aviso['texto']}"
                                })
                            st.session_state.avisos_pendientes.pop(i)
                            st.success("Aprobado correctamente.")
                            st.rerun()
                    with col2:
                        if st.button(f"Descartar", key=f"desc_{i}"):
                            st.session_state.avisos_pendientes.pop(i)
                            st.error("Descartado.")
                            st.rerun()

    elif clave != "":
        st.error("Clave incorrecta. Intente nuevamente.")
    else:
        st.info("Por favor, ingrese la contraseña para acceder a las opciones de administración.")