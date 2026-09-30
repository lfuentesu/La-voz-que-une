import streamlit as st
import os
import json
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="La Voz Que Une",
    page_icon="📰",
    layout="wide"
)

# -------------------------------------------------------------
# FUNCIONES PARA LECTURA Y ESCRITURA EN ARCHIVOS DURA/PERMANENTE
# -------------------------------------------------------------
ARCH_MARQUESINA = "marquesina.txt"
ARCH_QUIENES = "quienes_somos.txt"
ARCH_NOTICIAS = "noticias.json"

def cargar_texto(archivo, texto_defecto):
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            return f.read()
    return texto_defecto

def guardar_texto(archivo, contenido):
    with open(archivo, "w", encoding="utf-8") as f:
        f.write(contenido)

def cargar_noticias():
    if os.path.exists(ARCH_NOTICIAS):
        try:
            with open(ARCH_NOTICIAS, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def guardar_noticias(lista_noticias):
    with open(ARCH_NOTICIAS, "w", encoding="utf-8") as f:
        json.dump(lista_noticias, f, ensure_ascii=False, indent=4)

# Textos por defecto si los archivos no existen aún
texto_marquesina_defecto = "¡Bienvenidos a La Voz Que Une! Periódico digital comunitario de la Población El Bosque 1, Huechuraba."
texto_quienes_defecto = """### Nuestra Historia y Propósito

**La Voz Que Une** es una iniciativa comunitaria y ciudadana nacida en la **Población El Bosque 1, comuna de Huechuraba**. Nuestro objetivo principal es rescatar la memoria local, difundir las actividades de nuestros vecinos y crear un espacio abierto para la cultura, las artes y el encuentro comunitario.

---

### El Equipo de Trabajo

Nuestro equipo está conformado por vecinos, educadores, gestores culturales y colaboradores comprometidos con la difusión de nuestro barrio:

* **Dirección y Edición General:** Equipo Editorial *La Voz Que Une*.
* **Redacción y Colaboraciones:** Vecinos y organizaciones comunitarias de la Población El Bosque 1.
* **Fotografía y Registro Histórico:** Archivo comunitario y aportes de los lectores de Huechuraba.
"""

# Cargar contenidos actuales desde los archivos
marquesina_actual = cargar_texto(ARCH_MARQUESINA, texto_marquesina_defecto)
quienes_actual = cargar_texto(ARCH_QUIENES, texto_quienes_defecto)
noticias_actuales = cargar_noticias()

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
# MARQUESINA / LETRAS DESPLAZABLES (LIMPIA DE SÍMBOLOS EXTRAÑOS)
# -------------------------------------------------------------
texto_marquesina_limpio = marquesina_actual.replace("<", "").replace(">", "").strip()

st.markdown(
    f"""
    <div style="background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 15px;">
        <marquee behavior="scroll" direction="left" scrollamount="6" style="color: #1f2937; font-weight: bold; font-size: 16px;">
            📢 {texto_marquesina_limpio}
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
# SECCIÓN 1: INICIO (DESPLIEGUE DE NOTICIAS Y PUBLICACIONES)
# -------------------------------------------------------------
if opcion == "Inicio":
    st.header("Bienvenido a nuestro portal comunitario")
    st.write(
        "Un espacio dedicado a difundir la cultura, la historia, los eventos "
        "y los encuentros de las vecinas y vecinos de la Población El Bosque 1 en Huechuraba."
    )
    
    st.divider()
    st.subheader("📰 Publicaciones y Noticias Comunitarias")

    if noticias_actuales:
        # Mostrar las noticias de más reciente a más antigua
        for idx, noti in enumerate(reversed(noticias_actuales)):
            st.markdown(f"### {noti['titulo']}")
            st.caption(f"📅 *Publicado el {noti['fecha']}* | 🏷️ **Categoría:** {noti['categoria']}")
            st.write(noti['contenido'])
            st.divider()
    else:
        st.info("Aún no hay publicaciones guardadas. Puede agregar la primera desde el Panel de Administración.")

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
        st.markdown(quienes_actual)

    with col_imagen:
        ruta_imagen_comunidad = "galeria/VARIOS"
        if os.path.exists(ruta_imagen_comunidad):
            fotos_varias = [f for f in os.listdir(ruta_imagen_comunidad) if f.endswith(('.jpg', '.jpeg', '.png'))]
            if fotos_varias:
                st.image(os.path.join(ruta_imagen_comunidad, fotos_varias[0]), caption="Comunidad El Bosque 1 - Huechuraba", use_container_width=True)

# -------------------------------------------------------------
# SECCIÓN 4: PANEL DE ADMINISTRACIÓN
# -------------------------------------------------------------
elif opcion == "Administración":
    st.header("⚙️ Panel de Administración")
    st.write("Gestión interna de contenidos, publicaciones y noticias.")
    
    st.divider()
    clave = st.text_input("Ingrese la clave de acceso:", type="password")
    
    if clave:
        # Recuerde verificar si mantiene "lavoz123" o la clave personalizada que usted definió
        if clave == "lavoz123":
            st.success("Acceso concedido al Panel de Administración.")

            sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs([
                "📝 Publicar Noticia", 
                "👤 Editar Quiénes Somos", 
                "📢 Modificar Marquesina",
                "🖼️ Subir Fotos a Galería"
            ])

            # PESTAÑA 1: PUBLICAR NUEVA NOTICIA
            with sub_tab1:
                st.subheader("Publicar un nuevo artículo o noticia en la portada")
                titulo_noticia = st.text_input("Título de la publicación:")
                cat_noticia = st.selectbox(
                    "Sección / Categoría de la publicación:",
                    ["Noticias Locales", "Cultura y Arte", "Deportes", "Anuncios Vecinales", "Memoria Histórica"]
                )
                cuerpo_noticia = st.text_area("Contenido del artículo:", height=200)

                if st.button("📌 Publicar en la Web"):
                    if titulo_noticia.strip() == "" or cuerpo_noticia.strip() == "":
                        st.error("Debe ingresar un título y contenido para publicar.")
                    else:
                        fecha_hoy = datetime.now().strftime("%d/%m/%Y")
                        nueva_pub = {
                            "titulo": titulo_noticia,
                            "categoria": cat_noticia,
                            "contenido": cuerpo_noticia,
                            "fecha": fecha_hoy
                        }
                        noticias_actuales.append(nueva_pub)
                        guardar_noticias(noticias_actuales)
                        st.success("¡Noticia publicada con éxito! Ya se encuentra visible en la sección Inicio.")
                        st.rerun()

            # PESTAÑA 2: EDITAR QUIÉNES SOMOS
            with sub_tab2:
                st.subheader("Editar la presentación de 'Quiénes somos'")
                nuevo_quienes = st.text_area(
                    "Modifique la historia o presentación del equipo:",
                    value=quienes_actual,
                    height=250
                )
                if st.button("💾 Guardar 'Quiénes Somos' Permanentemente"):
                    guardar_texto(ARCH_QUIENES, nuevo_quienes)
                    st.success("¡Texto guardado permanentemente en el servidor!")
                    st.rerun()

            # PESTAÑA 3: MODIFICAR MARQUESINA
            with sub_tab3:
                st.subheader("Modificar mensaje de las letras desplazables")
                nueva_marquesina = st.text_area(
                    "Escriba el nuevo aviso informativo (se guardará sin caracteres extraños):",
                    value=marquesina_actual,
                    height=100
                )
                if st.button("💾 Guardar Marquesina Permanentemente"):
                    # Limpiamos posibles símbolos extraños antes de guardar
                    texto_limpio_guardar = nueva_marquesina.replace("<", "").replace(">", "").strip()
                    guardar_texto(ARCH_MARQUESINA, texto_limpio_guardar)
                    st.success("¡Marquesina actualizada y guardada de forma limpia!")
                    st.rerun()

            # PESTAÑA 4: SUBIR FOTOS A LA GALERÍA
            with sub_tab4:
                st.subheader("Subir imágenes directamente a la Galería")
                if os.path.exists("galeria"):
                    cats_galeria = [c for c in os.listdir("galeria") if os.path.isdir(os.path.join("galeria", c))]
                    if cats_galeria:
                        cat_destino = st.selectbox("Seleccione la carpeta destino:", cats_galeria)
                        fotos_subir = st.file_uploader(
                            "Seleccione las imágenes a subir:",
                            type=["jpg", "jpeg", "png"],
                            accept_multiple_files=True
                        )
                        if st.button("📤 Guardar Fotos en Galería"):
                            if fotos_subir:
                                ruta_destino = os.path.join("galeria", cat_destino)
                                for f_img in fotos_subir:
                                    ruta_final = os.path.join(ruta_destino, f_img.name)
                                    with open(ruta_final, "wb") as file_out:
                                        file_out.write(f_img.getbuffer())
                                st.success(f"¡Se subieron {len(fotos_subir)} imágenes a la carpeta {cat_destino}!")
                            else:
                                st.warning("Por favor, seleccione al menos una imagen.")
                else:
                    st.error("La carpeta 'galeria' no se encuentra.")

        else:
            st.error("Clave incorrecta. Intente nuevamente.")

# -------------------------------------------------------------
# SECCIÓN 5: CONTACTO
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
            carpeta_envios = "mensajes_recibidos"
            os.makedirs(carpeta_envios, exist_ok=True)

            if archivos_adjuntos:
                for archivo in archivos_adjuntos:
                    nombre_limpio = nombre.replace(" ", "_").lower()
                    fecha_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                    nombre_archivo_guardado = f"{fecha_str}_{nombre_limpio}_{archivo.name}"
                    ruta_guardado = os.path.join(carpeta_envios, nombre_archivo_guardado)
                    
                    with open(ruta_guardado, "wb") as f:
                        f.write(archivo.getbuffer())

            st.success(f"¡Muchas gracias {nombre}! Su mensaje y archivos han sido recibidos con éxito por el equipo de La Voz Que Une.")