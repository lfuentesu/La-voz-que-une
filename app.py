import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuración inicial de la página
st.set_page_config(
    page_title="La Voz Que Une",
    page_icon="📰",
    layout="wide"
)

# ARCHIVO DE REGISTRO Y CARPETA PRINCIPAL DE GALERÍA
ARCHIVO_DATOS = "registros.csv"
CARPETA_GALERIA = "galeria"

# Crear carpeta principal de galería local si no existe
if not os.path.exists(CARPETA_GALERIA):
    os.makedirs(CARPETA_GALERIA)

# Función para cargar datos desde la planilla
def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        try:
            return pd.read_csv(ARCHIVO_DATOS)
        except Exception:
            pass
    return pd.DataFrame(columns=["Fecha", "Nombre", "Tipo", "Mensaje", "Estado"])

# Función para guardar datos en la planilla
def guardar_datos(df):
    df.to_csv(ARCHIVO_DATOS, index=False)

# --- INICIALIZACIÓN DE VARIABLES EN MEMORIA ---
if "mensaje_diario" not in st.session_state:
    st.session_state.mensaje_diario = "«La fuerza de nuestra comunidad radica en la unión, el respeto y la colaboración diaria entre vecinos.»"

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

# Cargar la base de datos de registros
df_registros = cargar_datos()

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
    
    noticias_aprobadas = df_registros[(df_registros["Tipo"].str.contains("Noticia", case=False, na=False)) & (df_registros["Estado"] == "Aprobado")]
    
    if noticias_aprobadas.empty:
        st.info("No hay noticias publicadas recientemente.")
    else:
        for _, row in noticias_aprobadas.iterrows():
            with st.container():
                st.subheader(f"📰 {row['Nombre']} ({row['Fecha']})")
                st.write(row['Mensaje'])
                st.write("---")

# --- Pestaña 2: Galería de Fotos Organizables por Tema ---
with tab2:
    st.header("📸 Galería Comunitaria")
    st.write("Espacio fotográfico de nuestros eventos e historia vecinal.")
    
    if os.path.exists(CARPETA_GALERIA):
        # Obtener lista de subcarpetas (temas) dentro de 'galeria'
        subcarpetas = [d for d in os.listdir(CARPETA_GALERIA) if os.path.isdir(os.path.join(CARPETA_GALERIA, d))]
        
        # Selector de tema para el vecino
        opciones_temas = ["Ver todas las fotos"] + subcarpetas
        tema_seleccionado = st.selectbox("📂 Seleccione una categoría o tema:", opciones_temas)
        
        # Obtener archivos de imágenes según el filtro
        archivos_galeria = []
        if tema_seleccionado == "Ver todas las fotos":
            for root, _, files in os.walk(CARPETA_GALERIA):
                for f in files:
                    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                        archivos_galeria.append(os.path.join(root, f))
        else:
            ruta_tema = os.path.join(CARPETA_GALERIA, tema_seleccionado)
            for f in os.listdir(ruta_tema):
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    archivos_galeria.append(os.path.join(ruta_tema, f))

        if len(archivos_galeria) == 0:
            st.info("No hay fotografías en esta categoría por el momento.")
        else:
            cols = st.columns(3)
            for idx, ruta_imagen in enumerate(archivos_galeria):
                archivo_nombre = os.path.basename(ruta_imagen)
                nombre_limpio = archivo_nombre.split('_', 2)[-1].replace('_', ' ').rsplit('.', 1)[0]
                with cols[idx % 3]:
                    st.image(ruta_imagen, caption=nombre_limpio if nombre_limpio else archivo_nombre, use_container_width=True)

# --- Pestaña 3: Avisos Económicos ---
with tab3:
    st.header("💼 Avisos Económicos")
    st.write("Clasificados, emprendimientos y servicios de los vecinos.")
    
    avisos_aprobados = df_registros[(df_registros["Tipo"].str.contains("Aviso", case=False, na=False)) & (df_registros["Estado"] == "Aprobado")]
    
    if avisos_aprobados.empty:
        st.info("No hay avisos económicos publicados por el momento.")
    else:
        for _, row in avisos_aprobados.iterrows():
            with st.container():
                st.success(f"💼 {row['Nombre']} - {row['Fecha']}")
                st.write(row['Mensaje'])
                st.write("---")

# --- Pestaña 4: Participación Vecinal ---
with tab4:
    st.header("🤝 Participación de los Vecinos")
    st.write("Envíe su aviso, noticia, propuesta o fotografía para ser publicado en el portal.")
    
    with st.form("form_participacion"):
        nombre = st.text_input("Su Nombre y Apellido:")
        tipo_aporte = st.selectbox("Tipo de publicación:", ["Noticia", "Aviso Económico", "Fotografía para Galería", "Sugerencia"])
        mensaje = st.text_area("Escriba su mensaje o detalle de la publicación:")
        imagen_adjunta = st.file_uploader("Adjuntar una imagen o fotografía (opcional):", type=["jpg", "jpeg", "png"])
        enviado = st.form_submit_button("Enviar para revisión")
        
        if enviado:
            if nombre.strip() != "" and (mensaje.strip() != "" or imagen_adjunta is not None):
                if imagen_adjunta is not None:
                    nombre_archivo = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{imagen_adjunta.name.replace(' ', '_')}"
                    ruta_guardado = os.path.join(CARPETA_GALERIA, nombre_archivo)
                    with open(ruta_guardado, "wb") as f:
                        f.write(imagen_adjunta.getbuffer())

                nuevo_registro = {
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Nombre": nombre,
                    "Tipo": tipo_aporte,
                    "Mensaje": mensaje,
                    "Estado": "Pendiente"
                }
                df_registros = pd.concat([df_registros, pd.DataFrame([nuevo_registro])], ignore_index=True)
                guardar_datos(df_registros)
                
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
    st.header("⚙️ Administración del Portal Editorial")
    st.caption("Panel exclusivo para el equipo editorial de La Voz Que Une")
    
    clave = st.text_input("Ingrese la clave de administrador:", type="password")
    
    if clave == "Bosque2026":  # Reemplace aquí por su clave si la cambió
        st.success("Acceso concedido al Panel Editorial.")
        
        # --- A. EDITAR MENSAJE DIARIO ---
        st.subheader("📝 Editar Mensaje del Día (Desplazable)")
        nuevo_mensaje = st.text_input("Nuevo mensaje:", value=st.session_state.mensaje_diario)
        if st.button("Actualizar Mensaje"):
            st.session_state.mensaje_diario = nuevo_mensaje
            st.success("¡El mensaje del día ha sido actualizado con éxito!")
            st.rerun()
            
        st.write("---")

        # --- B. GESTIÓN DE CATEGORÍAS/CARPETAS DE GALERÍA ---
        st.subheader("📁 Crear Nueva Categoría o Tema para la Galería")
        nombre_nueva_carpeta = st.text_input("Nombre de la nueva categoría (ej: Fiestas Patrias, Talleres, Historia):")
        if st.button("Crear Categoría"):
            if nombre_nueva_carpeta.strip() != "":
                nombre_carpeta_limpio = nombre_nueva_carpeta.strip().replace(" ", "_")
                ruta_nueva = os.path.join(CARPETA_GALERIA, nombre_carpeta_limpio)
                if not os.path.exists(ruta_nueva):
                    os.makedirs(ruta_nueva)
                    st.success(f"¡Categoría '{nombre_nueva_carpeta}' creada con éxito!")
                    st.rerun()
                else:
                    st.info("Esa categoría ya existe.")
            else:
                st.warning("Escriba un nombre para la categoría.")

        st.write("---")
        
        # --- C. SUBIDA DIRECTA DE FOTOS POR CATEGORÍA ---
        st.subheader("📸 Cargar Imagen Directa a la Galería")
        
        # Obtener lista actualizada de subcarpetas existentes
        subcarpetas = [d for d in os.listdir(CARPETA_GALERIA) if os.path.isdir(os.path.join(CARPETA_GALERIA, d))]
        opciones_destino = ["General (Sin tema específico)"] + subcarpetas
        
        carpeta_destino = st.selectbox("Seleccione la categoría donde guardar la foto:", opciones_destino)
        foto_admin = st.file_uploader("Seleccione una imagen (JPG, PNG):", type=["jpg", "jpeg", "png"], key="upload_editorial")
        pie_de_foto = st.text_input("Pie de foto o descripción corta (opcional):")
        
        if st.button("Publicar Foto en Galería"):
            if foto_admin is not None:
                texto_desc = pie_de_foto.replace(' ', '_') if pie_de_foto.strip() != "" else foto_admin.name.replace(' ', '_')
                nombre_archivo = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{texto_desc}.jpg"
                
                if carpeta_destino == "General (Sin tema específico)":
                    ruta_guardado = os.path.join(CARPETA_GALERIA, nombre_archivo)
                else:
                    ruta_guardado = os.path.join(CARPETA_GALERIA, carpeta_destino, nombre_archivo)

                with open(ruta_guardado, "wb") as f:
                    f.write(foto_admin.getbuffer())
                st.success("¡Fotografía publicada con éxito en la Galería Comunitaria!")
                st.rerun()
            else:
                st.warning("Seleccione un archivo de imagen antes de publicar.")

        st.write("---")

        # --- D. PLANILLA DE REGISTRO TIPO EXCEL ---
        st.subheader("📊 Registros y Solicitudes de Vecinos (Planilla)")
        
        if df_registros.empty:
            st.info("Aún no hay registros de solicitudes en la base de datos.")
        else:
            st.dataframe(df_registros, use_container_width=True)
            
            csv_data = df_registros.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar planilla de registros (CSV)",
                data=csv_data,
                file_name="registros_la_voz_que_une.csv",
                mime="text/csv"
            )
            
            st.write("---")
            st.subheader("📋 Gestión de Estados (Aprobar / Descartar)")
            
            pendientes = df_registros[df_registros["Estado"] == "Pendiente"]
            
            if pendientes.empty:
                st.info("No hay solicitudes pendientes por revisar.")
            else:
                for idx, row in pendientes.iterrows():
                    with st.expander(f"Solicitud #{idx+1}: {row['Nombre']} ({row['Tipo']}) - {row['Fecha']}"):
                        st.write(f"**Mensaje:** {row['Mensaje']}")
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"Aprobar solicitud", key=f"aprob_df_{idx}"):
                                df_registros.at[idx, "Estado"] = "Aprobado"
                                guardar_datos(df_registros)
                                st.success("Solicitud aprobada y publicada automáticamente.")
                                st.rerun()
                        with col2:
                            if st.button(f"Descartar solicitud", key=f"desc_df_{idx}"):
                                df_registros.at[idx, "Estado"] = "Descartado"
                                guardar_datos(df_registros)
                                st.error("Solicitud descartada.")
                                st.rerun()

    elif clave != "":
        st.error("Clave incorrecta. Intente nuevamente.")
    else:
        st.info("Por favor, ingrese la contraseña de administración para acceder.")