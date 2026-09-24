import streamlit as st
import os

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
    st.session_state["texto_desplazable"] = "¡Bienvenidos a La Voz Que Une! Periódico digital comunitario de El Bosque. Infórmese sobre nuestras actividades, cultura y eventos vecinales."

if "texto_quienes_somos" not in st.session_state:
    st.session_state["texto_quienes_somos"] = """
### Nuestra Historia y Propósito

**La Voz Que Une** es una iniciativa comunitaria y ciudadana nacida en la comuna de El Bosque. Nuestro objetivo principal es rescatar la memoria local, difundir las actividades de nuestros vecinos y crear un espacio abierto para la cultura, las artes y el encuentro.

---

### El Equipo de Trabajo

Nuestro equipo está conformado por vecinos, educadores, gestores culturales y colaboradores comprometidos con la difusión comunitaria:

* **Dirección y Edición General:** Equipo Editorial *La Voz Que Une*.
* **Redacción y Colaboraciones:** Vecinos y organizaciones comunitarias de El Bosque.
* **Fotografía y Registro Histórico:** Archivo comunitario y aportes de los lectores.

---

*Agradecemos a todas las instituciones, talleres y personas que hacen posible mantener vivo este medio independiente.*
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
st.caption("Periódico digital comunitario de El Bosque")

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
        "y los encuentros de los vecinos de nuestra comunidad."
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
# SECCIÓN 3: QUIÉNES SOMOS (FORMATO EDITORIAL / TEXTO)
# -------------------------------------------------------------
elif opcion == "Quiénes somos":
    st.header("👥 Quiénes Somos")
    
    col_texto, col_imagen = st.columns([2, 1])

    with col_texto:
        st.markdown(st.session_state["texto_quienes_somos"])

    with col_imagen:
        # Si tiene una imagen institucional, afiche o foto del barrio, puede ponerla aquí
        ruta_imagen_comunidad = "galeria/VARIOS"
        if os.path.exists(ruta_imagen_comunidad):
            fotos_varias = [f for f in os.listdir(ruta_imagen_comunidad) if f.endswith(('.jpg', '.jpeg', '.png'))]
            if fotos_varias:
                st.image(os.path.join(ruta_imagen_comunidad, fotos_varias[0]), caption="Comunidad de El Bosque", use_container_width=True)

# -------------------------------------------------------------
# SECCIÓN 4: ADMINISTRACIÓN
# -------------------------------------------------------------
elif opcion == "Administración":
    st.header("⚙️ Panel de Administración")
    st.write("Espacio reservado para la gestión interna del portal comunitario.")
    
    st.divider()
    clave = st.text_input("Ingrese la clave de acceso:", type="password")
    
    if clave:
        # Reemplace 'lavoz123' por la clave que usted definió si es distinta
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
        else:
            st.error("Clave incorrecta. Intente nuevamente.")

# -------------------------------------------------------------
# SECCIÓN 5: CONTACTO
# -------------------------------------------------------------
elif opcion == "Contacto":
    st.header("✉️ Contacto")
    st.write("¿Tiene alguna noticia o sugerencia para compartir?")
    st.write("Escríbanos a nuestro correo electrónico.")