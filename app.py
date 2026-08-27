import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="La Voz que Une",
    page_icon="📰",
    layout="wide"
)

EXCEL_FILE = "datos_periodico.xlsx"
VISITAS_FILE = "visitas.txt"

# ---------------------------------------------------------
# FUNCIONES AUXILIARES: CONTADOR DE VISITAS
# ---------------------------------------------------------
def gestionar_visitas():
    if not os.path.exists(VISITAS_FILE):
        with open(VISITAS_FILE, "w") as f:
            f.write("1")
        return 1
    else:
        with open(VISITAS_FILE, "r") as f:
            try:
                conteo = int(f.read().strip())
            except ValueError:
                conteo = 0
        conteo += 1
        with open(VISITAS_FILE, "w") as f:
            f.write(str(conteo))
        return conteo

if "visita_registrada" not in st.session_state:
    st.session_state.total_visitas = gestionar_visitas()
    st.session_state.visita_registrada = True

# ---------------------------------------------------------
# FUNCIONES AUXILIARES: SISTEMA DE COMENTARIOS
# ---------------------------------------------------------
def guardar_comentario(seccion, nombre, contacto, comentario):
    nuevo_comentario = pd.DataFrame([{
        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Sección": seccion,
        "Nombre": nombre,
        "Contacto": contacto,
        "Comentario": comentario,
        "Estado": "Aprobado"
    }])
    
    try:
        if os.path.exists(EXCEL_FILE):
            excel_obj = pd.ExcelFile(EXCEL_FILE)
            if "Comentarios" in excel_obj.sheet_names:
                df_existente = pd.read_excel(EXCEL_FILE, sheet_name="Comentarios")
                df_updated = pd.concat([df_existente, nuevo_comentario], ignore_index=True)
            else:
                df_updated = nuevo_comentario
            
            with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                df_updated.to_excel(writer, sheet_name="Comentarios", index=False)
        else:
            nuevo_comentario.to_excel(EXCEL_FILE, sheet_name="Comentarios", index=False)
    except Exception as e:
        st.error(f"Error al guardar el comentario: {e}")

def mostrar_seccion_comentarios(seccion):
    st.markdown("---")
    st.subheader("💬 Comentarios de la Comunidad")
    
    # Cargar comentarios
    try:
        if os.path.exists(EXCEL_FILE):
            excel_obj = pd.ExcelFile(EXCEL_FILE)
            if "Comentarios" in excel_obj.sheet_names:
                df = pd.read_excel(EXCEL_FILE, sheet_name="Comentarios")
                if "Sección" in df.columns and "Estado" in df.columns:
                    df_seccion = df[(df["Sección"] == seccion) & (df["Estado"] == "Aprobado")]
                    
                    if not df_seccion.empty:
                        for _, row in df_seccion.iterrows():
                            with st.chat_message("user"):
                                st.write(f"**{row['Nombre']}** · *{row['Fecha']}*")
                                st.write(row["Comentario"])
                    else:
                        st.info("Aún no hay comentarios en esta sección. ¡Sé el primero en opinar!")
                else:
                    st.info("Aún no hay comentarios en esta sección.")
            else:
                st.info("Aún no hay comentarios en esta sección. ¡Sé el primero en opinar!")
        else:
            st.info("Aún no hay comentarios registrados.")
    except Exception:
        st.info("Aún no hay comentarios registrados.")

    # Formulario de ingreso de comentarios
    st.markdown("### Déjanos tu opinión o aporte")
    with st.form(key=f"form_comentario_{seccion}"):
        nombre = st.text_input("Nombre y Apellido *")
        contacto = st.text_input("Correo electrónico o Teléfono de contacto *")
        comentario = st.text_area("Escribe tu comentario aquí *")
        enviado = st.form_submit_button("Publicar Comentario")
        
        if enviado:
            if not nombre.strip() or not contacto.strip() or not comentario.strip():
                st.error("Por favor completa todos los campos marcados con (*).")
            else:
                guardar_comentario(seccion, nombre, contacto, comentario)
                st.success("¡Muchas gracias! Tu comentario ha sido publicado exitosamente.")
                st.rerun()

# ---------------------------------------------------------
# BARRA LATERAL (MENÚ Y CONTADOR)
# ---------------------------------------------------------
st.sidebar.title("La Voz que Une")
st.sidebar.markdown("Periódico Comunitario digital")

opcion = st.sidebar.radio(
    "Navegación:",
    ["Inicio", "Historia", "Galería", "Participa"]
)

st.sidebar.markdown("---")
if "total_visitas" in st.session_state:
    st.sidebar.metric(label="👀 Visitas Totales", value=st.session_state.total_visitas)

st.sidebar.caption("— Periódico La Voz que Une —")

# ---------------------------------------------------------
# CONTENIDO PRINCIPAL POR SECCIONES
# ---------------------------------------------------------

# 1. INICIO
if opcion == "Inicio":
    st.title("📰 La Voz que Une - Edición Digital")
    st.write("Bienvenidos al espacio informativo y comunitario. Aquí compartimos las últimas novedades y noticias de nuestra comunidad.")
    
    # Cargar y mostrar publicaciones desde Excel
    if os.path.exists(EXCEL_FILE):
        try:
            excel_obj = pd.ExcelFile(EXCEL_FILE)
            if "Noticias" in excel_obj.sheet_names:
                df_noticias = pd.read_excel(EXCEL_FILE, sheet_name="Noticias")
                
                if not df_noticias.empty:
                    df_noticias.columns = [str(col).strip().capitalize() for col in df_noticias.columns]
                    
                    if "Estado" in df_noticias.columns:
                        df_visibles = df_noticias[df_noticias["Estado"].astype(str).str.contains("Aprobad", case=False, na=False)]
                    else:
                        df_visibles = df_noticias

                    if not df_visibles.empty:
                        st.markdown("### Últimas Publicaciones")
                        for _, row in df_visibles.iterrows():
                            titulo = row.get("Título", row.get("Titulo", "Aviso Comunitario"))
                            contenido = row.get("Contenido", row.get("Detalle", row.get("Texto", "")))
                            fecha = row.get("Fecha", "")

                            st.subheader(titulo)
                            if pd.notna(fecha) and str(fecha).strip() != "":
                                st.caption(f"📅 Publicado el {fecha}")
                            st.write(contenido)
                            st.markdown("---")
        except Exception as e:
            st.error(f"Error al leer las noticias: {e}")

    # FORMULARIO DE COMENTARIOS EN INICIO
    mostrar_seccion_comentarios("Inicio")

# 2. HISTORIA
elif opcion == "Historia":
    st.title("📜 Nuestra Historia")
    st.write("Un recorrido por la memoria histórica, el patrimonio y los hitos que han marcado el desarrollo de nuestro entorno y su gente.")
    
    st.markdown("""
    > *"Un pueblo que conoce su historia es un pueblo que proyecta su futuro con identidad y dignidad."*
    """)
    
    # FORMULARIO DE COMENTARIOS EN HISTORIA
    mostrar_seccion_comentarios("Historia")

# 3. GALERÍA
elif opcion == "Galería":
    st.title("🖼️ Galería Comunitaria")
    st.write("Registros visuales, fotografías patrimoniales y actividades destacadas de la comunidad.")
    
    # FORMULARIO DE COMENTARIOS EN GALERÍA
    mostrar_seccion_comentarios("Galería")

# 4. PARTICIPA
elif opcion == "Participa":
    st.title("🤝 Participa y Envía tu Nota")
    st.write("Este periódico lo hacemos entre todos. Déjanos tu propuesta de noticia, opinión o fotografía.")
    
    with st.form(key="form_participa"):
        nombre_p = st.text_input("Tu Nombre")
        correo_p = st.text_input("Correo o Teléfono de Contacto")
        mensaje_p = st.text_area("Propuesta o Noticia")
        archivo_p = st.file_uploader("Adjuntar imagen (opcional)", type=["png", "jpg", "jpeg"])
        
        btn_participa = st.form_submit_button("Enviar Colaboración")
        if btn_participa:
            if not nombre_p.strip() or not mensaje_p.strip():
                st.error("Por favor completa tu nombre y el mensaje.")
            else:
                st.success("¡Gracias por tu colaboración! El equipo editorial revisará tu aporte.")
