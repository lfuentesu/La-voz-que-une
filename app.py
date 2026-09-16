import streamlit as st

# Configuración inicial de la página
st.set_page_config(
    page_title="La Voz Que Une",
    page_icon="📰",
    layout="wide"
)

# --- 1. BANNER OFICIAL CON IMAGEN ---
# Muestra la imagen banner.jpeg guardada en la carpeta del proyecto
st.image("banner.jpeg", use_container_width=True)

st.write("")

# --- 2. MENSAJE DIARIO (DESPLEGABLE) ---
with st.expander("📌 Mensaje del Día - Haga clic para leer"):
    st.info("«La fuerza de nuestra comunidad radica en la unión, el respeto y la colaboración diaria entre vecinos.»")

st.write("---")

# Inicializar almacenamiento temporal de avisos si no existe
if "avisos_pendientes" not in st.session_state:
    st.session_state.avisos_pendientes = [
        {"vecino": "María González", "tipo": "Ofrecimiento", "texto": "Servicio de costura y arreglos de ropa."},
        {"vecino": "Juan Pérez", "tipo": "Aviso", "texto": "Se busca mascota extraviada (gato amarillo)."}
    ]

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

# --- Pestaña 2: Galería ---
with tab2:
    st.header("📸 Galería Comunitaria")
    st.write("Espacio fotográfico de nuestros eventos e historia vecinal.")

# --- Pestaña 3: Avisos Económicos ---
with tab3:
    st.header("💼 Avisos Económicos")
    st.write("Clasificados, emprendimientos y servicios de los vecinos.")

# --- 3. PESTAÑA DE PARTICIPACIÓN VECINAL ---
with tab4:
    st.header("🤝 Participación de los Vecinos")
    st.write("Envíe su aviso, propuesta o comentario para ser publicado en el portal.")
    
    with st.form("form_participacion"):
        nombre = st.text_input("Su Nombre y Apellido:")
        tipo_aporte = st.selectbox("Tipo de publicación:", ["Aviso Económico", "Noticia / Aporte", "Sugerencia"])
        mensaje = st.text_area("Escriba su mensaje o aviso:")
        enviado = st.form_submit_button("Enviar para revisión")
        
        if enviado:
            if nombre.strip() != "" and mensaje.strip() != "":
                st.session_state.avisos_pendientes.append({
                    "vecino": nombre,
                    "tipo": tipo_aporte,
                    "texto": mensaje
                })
                st.success("¡Gracias! Su mensaje ha sido enviado a la administración para aprobación.")
            else:
                st.warning("Por favor complete su nombre y el mensaje antes de enviar.")

# --- Pestaña 5: Humor ---
with tab5:
    st.header("😄 Espacio de Humor")
    st.write("Chistes, tiras cómicas y contenido de entretenimiento vecinal.")

# --- Pestaña 6: Historia ---
with tab6:
    st.header("📜 Historia de la Población")
    st.write("Relatos, fundadores y memoria histórica de nuestra comunidad.")

# --- 4. PESTAÑA DE ADMINISTRACIÓN PROTEGIDA ---
with tab7:
    st.header("⚙️ Administración del Portal")
    
    # Control de acceso por contraseña
    clave = st.text_input("Ingrese la clave de administrador:", type="password")
    
    # Clave de acceso por defecto: 1234
    if clave == "1234":
        st.success("Acceso concedido al Panel de Control.")
        st.subheader("📋 Solicitudes de Avisos Pendientes")
        
        if len(st.session_state.avisos_pendientes) == 0:
            st.info("No hay avisos pendientes de aprobación.")
        else:
            for i, aviso in enumerate(list(st.session_state.avisos_pendientes)):
                with st.expander(f"Solicitud de: {aviso['vecino']} ({aviso['tipo']})"):
                    st.write(f"**Mensaje:** {aviso['texto']}")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"Aprobar", key=f"aprob_{i}"):
                            st.session_state.avisos_pendientes.pop(i)
                            st.success("Aviso aprobado correctamente.")
                            st.rerun()
                    with col2:
                        if st.button(f"Descartar", key=f"desc_{i}"):
                            st.session_state.avisos_pendientes.pop(i)
                            st.error("Aviso descartado.")
                            st.rerun()
    elif clave != "":
        st.error("Clave incorrecta. Intente nuevamente.")
    else:
        st.info("Por favor, ingrese la contraseña para acceder a las opciones de administración.")