import streamlit as st
import os

# Configuración de la página
st.set_page_config(
    page_title="La Voz Que Une",
    page_icon="📰",
    layout="wide"
)

# Menú de navegación lateral
st.sidebar.title("Navegación")
opcion = st.sidebar.radio(
    "Ir a:",
    ["Inicio", "Galería", "Quiénes somos", "Contacto"]
)

# -------------------------------------------------------------
# SECCIÓN 1: INICIO
# -------------------------------------------------------------
if opcion == "Inicio":
    st.title("📰 La Voz Que Une")
    st.subheader("Periódico digital comunitario de El Bosque")
    st.write("Bienvenido a nuestro portal de noticias, cultura y encuentros vecinales.")
    
    st.divider()
    st.write("Aquí irá el contenido principal y las noticias del día...")

# -------------------------------------------------------------
# SECCIÓN 2: GALERÍA DE FOTOS
# -------------------------------------------------------------
elif opcion == "Galería":
    st.title("🖼️ Galería Comunitaria")
    st.write("Explore nuestro archivo fotográfico clasificado por eventos y actividades.")

    # Ruta de la carpeta galeria
    ruta_galeria = "galeria"

    if os.path.exists(ruta_galeria):
        # Obtener las subcarpetas dentro de galeria
        categorias = [c for c in os.listdir(ruta_galeria) if os.path.isdir(os.path.join(ruta_galeria, c))]
        
        if categorias:
            # Opción por defecto para no mostrar ninguna categoría al inicio
            opciones_categorias = ["-- Seleccione una categoría --"] + categorias
            categoria_seleccionada = st.selectbox("Seleccione una categoría de la lista:", opciones_categorias)

            if categoria_seleccionada != "-- Seleccione una categoría --":
                ruta_categoria = os.path.join(ruta_galeria, categoria_seleccionada)
                
                # Obtener archivos de imagen (.jpg, .png, .jpeg)
                extensiones_validas = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')
                fotos = [f for f in os.listdir(ruta_categoria) if f.endswith(extensiones_validas)]

                st.divider()
                st.write(f"### Mostrando fotos de: **{categoria_seleccionada}** ({len(fotos)} imágenes)")

                if fotos:
                    # Desplegar fotos en una cuadrícula de 3 columnas
                    cols = st.columns(3)
                    for idx, foto in enumerate(fotos):
                        col = cols[idx % 3]
                        path_foto = os.path.join(ruta_categoria, foto)
                        with col:
                            st.image(path_foto, use_container_width=True)
                else:
                    st.warning("No hay imágenes en esta categoría aún.")
            else:
                st.info("👆 Seleccione un tema arriba o use el menú lateral de la izquierda para volver al **Inicio**.")
        else:
            st.warning("No se encontraron subcarpetas dentro de 'galeria'.")
    else:
        st.error("La carpeta 'galeria' no existe en el proyecto.")

# -------------------------------------------------------------
# SECCIÓN 3: QUIÉNES SOMOS
# -------------------------------------------------------------
elif opcion == "Quiénes somos":
    st.title("👥 Quiénes Somos")
    st.markdown("### El equipo detrás de *La Voz Que Une*")
    st.write("Somos un grupo de vecinos y colaboradores comprometidos con la difusión comunitaria, la cultura y la historia de nuestra comuna.")

    st.divider()

    # Mostramos a los integrantes en columnas
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Nombre del Integrante 1")
        st.markdown("**Cargo / Rol:** Editor / Redactor")
        st.write(
            "Escriba aquí una breve reseña de la persona. Por ejemplo: Vecino de la comuna con amplia trayectoria en iniciativas comunitarias..."
        )

    with col2:
        st.subheader("Nombre del Integrante 2")
        st.markdown("**Cargo / Rol:** Colaborador / Fotografía")
        st.write(
            "Escriba aquí una breve reseña de la segunda persona. Por ejemplo: Encargado del registro fotográfico y apoyo en las actividades vecinales..."
        )

# -------------------------------------------------------------
# SECCIÓN 4: CONTACTO
# -------------------------------------------------------------
elif opcion == "Contacto":
    st.title("✉️ Contacto")
    st.write("¿Tiene alguna noticia, sugerencia o fotografía para compartir con la comunidad?")
    st.write("Escríbanos a nuestro correo electrónico o contáctenos por nuestras redes.")