import streamlit as st
import os
import json
import pandas as pd
from datetime import datetime
from PIL import Image, ImageOps

# Configuración de la página
st.set_page_config(
    page_title="La Voz Que Une",
    page_icon="📰",
    layout="wide"
)

# -------------------------------------------------------------
# FUNCIÓN PARA ABRIR E IMÁGENES CON ROTACIÓN CORRECTA (EXIF)
# -------------------------------------------------------------
def abrir_imagen_corregida(path_imagen):
    try:
        image = Image.open(path_imagen)
        image = ImageOps.exif_transpose(image)
        return image
    except Exception:
        return path_imagen

# -------------------------------------------------------------
# ARCHIVOS DE ALMACENAMIENTO PERMANENTE
# -------------------------------------------------------------
ARCH_MARQUESINA = "marquesina.txt"
ARCH_QUIENES = "quienes_somos.txt"
ARCH_NOTICIAS = "noticias.json"
ARCH_MENSAJES = "mensajes.json"

def cargar_texto(archivo, texto_defecto):
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            return f.read()
    return texto_defecto

def guardar_texto(archivo, contenido):
    with open(archivo, "w", encoding="utf-8") as f:
        f.write(contenido)

def cargar_json(archivo):
    if os.path.exists(archivo):
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def guardar_json(archivo, datos):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

# Textos por defecto
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

# Carga inicial de datos
marquesina_actual = cargar_texto(ARCH_MARQUESINA, texto_marquesina_defecto)
quienes_actual = cargar_texto(ARCH_QUIENES, texto_quienes_defecto)
noticias_actuales = cargar_json(ARCH_NOTICIAS)
mensajes_recibidos = cargar_json(ARCH_MENSAJES)

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
    st.image(abrir_imagen_corregida(ruta_banner), use_container_width=True)

st.title("📰 La Voz Que Une")
st.caption("Periódico digital comunitario de la Población El Bosque 1 - Huechuraba")

# -------------------------------------------------------------
# MARQUESINA / LETRAS DESPLAZABLES
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
# SECCIÓN 1: INICIO (NOTICIAS PUBLICADAS)
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
        for idx, noti in enumerate(reversed(noticias_actuales)):
            st.markdown(f"### {noti['titulo']}")
            st.caption(f"📅 *Publicado el {noti['fecha']}* | 🏷️ **Categoría:** {noti.get('categoria', 'General')}")
            st.write(noti['contenido'])
            if "imagen" in noti and noti["imagen"] and os.path.exists(noti["imagen"]):
                st.image(abrir_imagen_corregida(noti["imagen"]), use_container_width=True)
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
                            st.image(abrir_imagen_corregida(path_foto), use_container_width=True)
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
                st.image(abrir_imagen_corregida(os.path.join(ruta_imagen_comunidad, fotos_varias[0])), caption="Comunidad El Bosque 1 - Huechuraba", use_container_width=True)

# -------------------------------------------------------------
# SECCIÓN 4: PANEL DE ADMINISTRACIÓN
# -------------------------------------------------------------
elif opcion == "Administración":
    st.header("⚙️ Panel de Administración")
    st.write("Gestión interna de contenidos, publicaciones y moderación de aportes.")
    
    st.divider()
    clave = st.text_input("Ingrese la clave de acceso:", type="password")
    
    if clave:
        if clave == "Bosque2026":
            st.success("Acceso concedido al Panel de Administración.")

            sub_tab1, sub_tab2, sub_tab3, sub_tab4, sub_tab5, sub_tab6 = st.tabs([
                "📬 Mensajes y Moderación",
                "📝 Publicar Noticia", 
                "👤 Editar Quiénes Somos", 
                "📢 Modificar Marquesina",
                "🖼️ Subir Fotos",
                "🗑️ Gestionar / Eliminar Galería"
            ])

            # PESTAÑA 1: MODERACIÓN DE MENSAJES RECIBIDOS
            with sub_tab1:
                st.subheader("📬 Envíos y Aportes Recibidos de los Vecinos")
                st.write("Revise los mensajes enviados desde la sección Contacto y decida si aprobarlos para la portada o descartarlos.")

                if mensajes_recibidos:
                    df_mensajes = pd.DataFrame(mensajes_recibidos)
                    columnas_renombradas = {
                        "fecha": "Fecha y Hora",
                        "nombre": "Nombre del Vecino",
                        "contacto": "Contacto (Teléfono/Correo)",
                        "asunto": "Motivo / Asunto",
                        "mensaje": "Mensaje Completo"
                    }
                    cols_existentes = [c for c in columnas_renombradas.keys() if c in df_mensajes.columns]
                    df_exportar = df_mensajes[cols_existentes].rename(columns=columnas_renombradas)
                    
                    csv_data = df_exportar.to_csv(index=False, encoding="utf-8-sig")

                    st.download_button(
                        label="📥 Descargar historial de mensajes (Formato CSV / Excel)",
                        data=csv_data,
                        file_name=f"mensajes_recibidos_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        help="Haga clic para descargar todos los mensajes en una planilla compatible con Excel o Google Sheets."
                    )
                    st.divider()

                    for i, msg in enumerate(mensajes_recibidos):
                        with st.expander(f"📩 {msg.get('asunto', 'Sin asunto')} — Enviado por: {msg.get('nombre', 'Anónimo')} ({msg.get('fecha', '')})"):
                            st.write(f"**Contacto:** {msg.get('contacto', 'No indicado')}")
                            st.write(f"**Mensaje:** {msg.get('mensaje', '')}")
                            
                            ruta_img = msg.get("imagen")
                            if ruta_img and os.path.exists(ruta_img):
                                st.image(abrir_imagen_corregida(ruta_img), width=300, caption="Imagen adjunta por el vecino")

                            col_btn1, col_btn2 = st.columns([1, 1])

                            with col_btn1:
                                if st.button(f"✅ Aprobar y Publicar Noticia #{i+1}", key=f"aprob_{i}"):
                                    nueva_noticia = {
                                        "titulo": f"{msg.get('asunto')} - {msg.get('nombre')}",
                                        "categoria": "Aportes Vecinales",
                                        "contenido": msg.get('mensaje'),
                                        "fecha": msg.get('fecha'),
                                        "imagen": msg.get('imagen')
                                    }
                                    noticias_actuales.append(nueva_noticia)
                                    guardar_json(ARCH_NOTICIAS, noticias_actuales)
                                    
                                    mensajes_recibidos.pop(i)
                                    guardar_json(ARCH_MENSAJES, mensajes_recibidos)
                                    st.success("¡Publicación aprobada y agregada a la sección Inicio!")
                                    st.rerun()

                            with col_btn2:
                                if st.button(f"🗑️ Descartar Mensaje #{i+1}", key=f"desc_{i}"):
                                    mensajes_recibidos.pop(i)
                                    guardar_json(ARCH_MENSAJES, mensajes_recibidos)
                                    st.warning("Mensaje descartado.")
                                    st.rerun()
                else:
                    st.info("No hay mensajes pendientes de revisión en este momento.")

            # PESTAÑA 2: PUBLICAR NUEVA NOTICIA
            with sub_tab2:
                st.subheader("Publicar un nuevo artículo o noticia directamente")
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
                        guardar_json(ARCH_NOTICIAS, noticias_actuales)
                        st.success("¡Noticia publicada con éxito! Ya se encuentra visible en la sección Inicio.")
                        st.rerun()

            # PESTAÑA 3: EDITAR QUIÉNES SOMOS
            with sub_tab3:
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

            # PESTAÑA 4: MODIFICAR MARQUESINA
            with sub_tab4:
                st.subheader("Modificar mensaje de las letras desplazables")
                nueva_marquesina = st.text_area(
                    "Escriba el nuevo aviso informativo:",
                    value=marquesina_actual,
                    height=100
                )
                if st.button("💾 Guardar Marquesina Permanentemente"):
                    texto_limpio_guardar = nueva_marquesina.replace("<", "").replace(">", "").strip()
                    guardar_texto(ARCH_MARQUESINA, texto_limpio_guardar)
                    st.success("¡Marquesina actualizada correctamente!")
                    st.rerun()

            # PESTAÑA 5: SUBIR FOTOS A LA GALERÍA
            with sub_tab5:
                st.subheader("Subir imágenes directamente a la Galería")
                if os.path.exists("galeria"):
                    cats_galeria = [c for c in os.listdir("galeria") if os.path.isdir(os.path.join("galeria", c))]
                    
                    # Opción para crear nueva subcarpeta
                    nueva_carpeta = st.text_input("➕ Crear nueva categoría/carpeta en la Galería (opcional):")
                    if st.button("Crear Carpeta"):
                        if nueva_carpeta.strip():
                            nombre_carp_limpio = nueva_carpeta.strip().upper()
                            os.makedirs(os.path.join("galeria", nombre_carp_limpio), exist_ok=True)
                            st.success(f"¡Carpeta '{nombre_carp_limpio}' creada correctamente!")
                            st.rerun()

                    st.divider()

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
                                st.rerun()
                            else:
                                st.warning("Por favor, seleccione al menos una imagen.")
                else:
                    st.error("La carpeta 'galeria' no se encuentra.")

            # PESTAÑA 6: GESTIONAR Y ELIMINAR FOTOS Y CARPETAS
            with sub_tab6:
                st.subheader("🗑️ Eliminar Fotos o Carpetas de la Galería")
                if os.path.exists("galeria"):
                    cats_galeria = [c for c in os.listdir("galeria") if os.path.isdir(os.path.join("galeria", c))]
                    if cats_galeria:
                        cat_gestionar = st.selectbox("Seleccione la categoría que desea administrar:", cats_galeria, key="gest_cat")
                        ruta_cat_gest = os.path.join("galeria", cat_gestionar)
                        
                        fotos_en_cat = [f for f in os.listdir(ruta_cat_gest) if f.endswith(('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'))]

                        st.write(f"Imágenes en **{cat_gestionar}**: ({len(fotos_en_cat)} imágenes)")

                        if fotos_en_cat:
                            cols_del = st.columns(3)
                            for idx, f_del in enumerate(fotos_en_cat):
                                col = cols_del[idx % 3]
                                path_del = os.path.join(ruta_cat_gest, f_del)
                                with col:
                                    st.image(abrir_imagen_corregida(path_del), use_container_width=True)
                                    if st.button(f"🗑️ Borrar {f_del[:15]}...", key=f"del_img_{idx}"):
                                        os.remove(path_del)
                                        st.success(f"Imagen '{f_del}' eliminada.")
                                        st.rerun()
                        else:
                            st.info("Esta carpeta está vacía.")

                        st.divider()
                        st.warning("⚠️ Zona de Eliminación de Carpetas Completas")
                        if st.button(f"❌ Borrar carpeta completa '{cat_gestionar}'", help="Borrará la carpeta y todas las imágenes dentro de ella."):
                            import shutil
                            shutil.rmtree(ruta_cat_gest)
                            st.success(f"Carpeta '{cat_gestionar}' eliminada por completo.")
                            st.rerun()

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
            ruta_imagen_guardada = None
            if archivos_adjuntos:
                carpeta_envios = "mensajes_recibidos"
                os.makedirs(carpeta_envios, exist_ok=True)
                for archivo in archivos_adjuntos:
                    nombre_limpio = nombre.replace(" ", "_").lower()
                    fecha_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                    nombre_archivo_guardado = f"{fecha_str}_{nombre_limpio}_{archivo.name}"
                    ruta_guardado = os.path.join(carpeta_envios, nombre_archivo_guardado)
                    
                    with open(ruta_guardado, "wb") as f:
                        f.write(archivo.getbuffer())
                    ruta_imagen_guardada = ruta_guardado

            nuevo_mensaje = {
                "nombre": nombre,
                "contacto": contacto_vecino,
                "asunto": asunto,
                "mensaje": mensaje,
                "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "imagen": ruta_imagen_guardada
            }
            
            mensajes_recibidos.append(nuevo_mensaje)
            guardar_json(ARCH_MENSAJES, mensajes_recibidos)

            st.success(f"¡Muchas gracias {nombre}! Su mensaje ha sido recibido por el equipo editorial de La Voz Que Une.")