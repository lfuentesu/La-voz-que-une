import streamlit as st
import os
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="La Voz Que Une",
    page_icon="📰",
    layout="wide"
)

# -------------------------------------------------------------
# INICIALIZACIÓN DE VARIABLES EN SESSION_STATE
# -------------------------------------------------------------
if "texto_desplazable" not in st.session_state:
    st.session_state["texto_desplazable"] = "¡Bienvenidos a La Voz Que Une! Periódico digital comunitario de la Población El Bosque 1, Huechuraba. Infórmese sobre nuestras actividades, cultura y eventos vecinales."

if "texto_quienes_somos" not in st.session_state:
    st.session_state["texto_quienes_somos"] = """
### Nuestra Historia y Propósito

**La Voz Que Une** es una iniciativa comunitaria y ciudadana nacida en la **Población El Bosque 1, comuna de Huechuraba**. Nuestro objetivo principal es rescatar la memoria local, difundir las actividades de nuestros vecinos y crear un espacio abierto para la cultura, las artes y el encuentro comunitario.

---

### El Equipo de Trabajo

Nuestro equipo está conformado por vecinos, educadores, gestores culturales y colaboradores comprometidos con la difusión de nuestro barrio:

* **Dirección y Edición General:** Equipo Editorial *La Voz Que Une*.
* **Redacción y Colaboraciones:** Vecinos y organizaciones comunitarias de la Población El Bosque 1.
* **Fotografía y Registro Histórico:** Archivo comunitario y aportes de los lectores de Huechuraba.

---

*Agradecemos a todas las instituciones, talleres y vecinos que hacen posible mantener vivo este medio independiente.*
"""

# -------------------------------------------------------------
# BANNER PRINCIPAL
# -------------------------------------------------------------
ruta_banner = "banner.jpeg"

if not os.path.exists(ruta_banner):
    if os.path.exists("banner.jpg"):
        ruta_banner = "banner.jpg"
    elif os.path.exists("banner.png"):
        ruta_banner = "banner.png"

if os.path.exists(ruta_banner):
    st.image(ruta_banner, use_container_width=True)

st.title("📰 La Voz Que Une")
st.caption("Periódico digital comunitario de la Población El Bosque 1 - Huechuraba")

# -------------------------------------------------------------
# MARQUESINA / LETRAS DESPLAZABLES
# -------------------------------------------------------------
st.markdown(
    f"""
    <div style="background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 15px;">
        <marquee behavior="scroll" direction="left" scrollamount="6" style="color: #1f2937; font-weight: bold; font-size: 16px;">
            📢 {st.session_state['texto_desplazable']}
        </marquee>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# -------------------------------------------------------------
# MENÚ DE NAVEGACIÓN LATERAL
# -------------------------------------------------------------
st.sidebar.title("Navegación")
opcion = st.sidebar.radio(
    "Ir a:",
    ["Inicio", "Galería", "Quiénes somos", "Administración", "Contacto"]
)

# -------------------------------------------------------------
# SECCIÓN 1: INICIO
# -------------------------------------------------------------
if opcion == "Inicio":
    st.header("Bienvenido a nuestro portal comunitario")
    st.write(
        "Un espacio dedicado a difundir la cultura, la historia, los eventos "
        "y los encuentros de las vecinas y vecinos de la Población El Bosque 1 en Huechuraba."
    )
    
    st.divider()
    st.subheader("Últimas Novedades")
    st.write("Seleccione en el menú de la izquierda (Navegación) para explorar las secciones.")

# -------------------------------------------------------------
# SECCIÓN 2: GALERÍA DE FOTOS
# -------------------------------------------------------------
elif opcion == "Galería":
    st.header("🖼️ Galería Comunitaria")
    st.write("Explore nuestro archivo fotográfico clasificado por eventos y actividades.")

    ruta_galeria = "galeria"

    if os.path.exists(ruta_galeria):
        categorias = [c for c in os.listdir(ruta_galeria) if os.path.isdir(os.path.join(ruta_galeria, c))]
        
        if categorias:
            opciones_categorias = ["-- Seleccione una categoría --"] + categorias
            categoria_seleccionada = st.selectbox("Seleccione un tema de la galería:", opciones_categorias)

            if categoria_seleccionada != "-- Seleccione una categoría --":
                ruta_categoria = os.path.join(ruta_galeria, categoria_seleccionada)
                
                extensiones_validas = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')
                fotos = [f for f in os.listdir(ruta_categoria) if f.endswith(extensiones_validas)]

                st.divider()
                st.subheader(f"Categoría: {categoria_seleccionada} ({len(fotos)} imágenes)")

                if fotos:
                    cols = st.columns(3)
                    for idx, foto in enumerate(fotos):
                        col = cols[idx % 3]
                        path_foto = os.path.join(ruta_categoria, foto)
                        with col:
                            st.image(path_foto, use_container_width=True)
                else:
                    st.warning("No hay imágenes en esta categoría aún.")
            else:
                st.info("💡 Seleccione una categoría en el desplegable superior o haga clic en **Inicio** en el menú lateral para volver a la portada.")
        else:
            st.warning("No se encontraron subcarpetas dentro de 'galeria'.")
    else:
        st.error("La carpeta 'galeria' no existe en el proyecto.")

# -------------------------------------------------------------
# SECCIÓN 3: QUIÉNES SOMOS
# -------------------------------------------------------------
elif opcion == "Quiénes somos":
    st.header("👥 Quiénes Somos")
    
    col_texto, col_imagen = st.columns([2, 1])

    with col_texto:
        st.markdown(st.session_state["texto_quienes_somos"])

    with col_imagen:
        ruta_imagen_comunidad = "galeria/VARIOS"
        if os.path.exists(ruta_imagen_comunidad):
            fotos_varias = [f for f in os.listdir(ruta_imagen_comunidad) if f.endswith(('.jpg', '.jpeg', '.png'))]
            if fotos_varias:
                st.image(os.path.join(ruta_imagen_comunidad, fotos_varias[0]), caption="Comunidad El Bosque 1 - Huechuraba", use_container_width=True)

# -------------------------------------------------------------
# SECCIÓN 4: ADMINISTRACIÓN
# -------------------------------------------------------------
elif opcion == "Administración":
    st.header("⚙️ Panel de Administración")
    st.write("Espacio reservado para la gestión interna del portal comunitario.")
    
    st.divider()
    clave = st.text_input("Ingrese la clave de acceso:", type="password")
    
    if clave:
        # Coloque aquí la clave personalizada que usted definió
        if clave == "Bosque2026":
            st.success("Acceso concedido al Panel de Administración.")
            
            st.subheader("📢 Modificar mensaje de la marquesina (letras desplazables)")
            nuevo_texto = st.text_area(
                "Escriba aquí el nuevo mensaje informativo para la portada:",
                value=st.session_state["texto_desplazable"],
                height=100
            )
            
            if st.button("Guardar marquesina"):
                st.session_state["texto_desplazable"] = nuevo_texto
                st.success("¡Marquesina actualizada!")

            st.divider()

            st.subheader("📝 Editar contenido de 'Quiénes somos'")
            nuevo_quienes_somos = st.text_area(
                "Modifique la presentación del equipo o la historia del proyecto:",
                value=st.session_state["texto_quienes_somos"],
                height=250
            )

            if st.button("Guardar texto de Quiénes somos"):
                st.session_state["texto_quienes_somos"] = nuevo_quienes_somos
                st.success("¡Sección Quiénes somos actualizada correctamente!")

            st.divider()

            st.subheader("📬 Fotografías e Imágenes Recibidas de los Vecinos")
            carpeta_envios = "mensajes_recibidos"
            if os.path.exists(carpeta_envios):
                archivos_recibidos = [f for f in os.listdir(carpeta_envios) if f.endswith(('.jpg', '.jpeg', '.png'))]
                if archivos_recibidos:
                    st.write(f"Se han recibido **{len(archivos_recibidos)}** archivos adjuntos:")
                    cols_recibidas = st.columns(3)
                    for idx, arch in enumerate(archivos_recibidos):
                        col = cols_recibidas[idx % 3]
                        with col:
                            st.image(os.path.join(carpeta_envios, arch), caption=arch, use_container_width=True)
                else:
                    st.info("Aún no se han subido imágenes a través del formulario de contacto.")
            else:
                st.info("La carpeta de mensajes recibidos se creará automáticamente cuando los vecinos envíen su primer archivo.")

        else:
            st.error("Clave incorrecta. Intente nuevamente.")

# -------------------------------------------------------------
# SECCIÓN 5: CONTACTO (FORMULARIO CON CARGA DE IMÁGENES)
# -------------------------------------------------------------
elif opcion == "Contacto":
    st.header("✉️ Contacto y Envío de Material")
    st.write(
        "¿Tiene alguna noticia, historia, sugerencia o fotografía que desee compartir con la comunidad de la Población El Bosque 1? "
        "Complete el siguiente formulario:"
    )

    st.divider()

    with st.form(key="formulario_contacto", clear_on_submit=True):
        nombre = st.text_input("Nombre y Apellido *")
        contacto_vecino = st.text_input("Correo electrónico o Teléfono de contacto *")
        asunto = st.selectbox(
            "Motivo del mensaje:",
            ["Consulta / Sugerencia", "Envío de noticia / Historia local", "Aporte de fotografía / Archivo", "Otro"]
        )
        mensaje = st.text_area("Escriba su mensaje o reseña aquí *", height=150)
        
        archivos_adjuntos = st.file_uploader(
            "Adjuntar fotografía o imagen (opcional):",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True
        )

        boton_enviar = st.form_submit_button("Enviar Mensaje")

    if boton_enviar:
        if nombre.strip() == "" or contacto_vecino.strip() == "" or mensaje.strip() == "":
            st.error("Por favor, complete los campos obligatorios (Nombre, Contacto y Mensaje).")
        else:
            # Crear carpeta de guardado de envíos si no existe
            carpeta_envios = "mensajes_recibidos"
            os.makedirs(carpeta_envios, exist_ok=True)

            # Si el vecino subió fotos, se guardan con fecha y nombre
            if archivos_adjuntos:
                for archivo in archivos_adjuntos:
                    nombre_limpio = nombre.replace(" ", "_").lower()
                    fecha_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                    nombre_archivo_guardado = f"{fecha_str}_{nombre_limpio}_{archivo.name}"
                    ruta_guardado = os.path.join(carpeta_envios, nombre_archivo_guardado)
                    
                    with open(ruta_guardado, "wb") as f:
                        f.write(archivo.getbuffer())

            st.success(f"¡Muchas gracias {nombre}! Su mensaje y archivos han sido recibidos con éxito por el equipo de La Voz Que Une.")