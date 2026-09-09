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
FRASE_FILE = "frase_dia.txt"
CLAVE_ADMIN = "bosque2026"  # Reemplace aquí con su clave personal

# Estilos CSS institucionales y animación de texto en movimiento
st.markdown("""
<style>
    /* Colores institucionales */
    :root {
        --verde-principal: #2E7D32;
        --amarillo-marca: #F9C00D;
        --rojo-marca: #E53935;
        --texto-oscuro: #333333;
    }
    
    /* Encabezados y títulos principales */
    h1, h2, h3 {
        color: #2E7D32 !important;
        font-family: 'Montserrat', 'Arial', sans-serif;
    }
    
    /* Franja decorativa superior */
    .franja-marca {
        height: 6px;
        background: linear-gradient(90deg, #2E7D32 50%, #F9C00D 75%, #E53935 100%);
        margin-bottom: 15px;
        border-radius: 3px;
    }

    /* Eslogan destacado */
    .eslogan-comunidad {
        color: #2E7D32;
        font-size: 1.25rem;
        font-weight: 700;
        margin-top: -10px;
        margin-bottom: 20px;
    }

    /* Estilo y Animación de la Cinta de Texto Desplazable */
    .cinta-contenedor {
        width: 100%;
        background-color: #2E7D32;
        color: #FFFFFF;
        overflow: hidden;
        white-space: nowrap;
        box-sizing: border-box;
        padding: 10px 0;
        border-radius: 6px;
        margin-bottom: 25px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .cinta-texto {
        display: inline-block;
        padding-left: 100%;
        animation: moverTexto 20s linear infinite;
        font-weight: 600;
        font-size: 1.1rem;
    }

    @keyframes moverTexto {
        0%   { transform: translate(0, 0); }
        100% { transform: translate(-100%, 0); }
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# FUNCIONES AUXILIARES: BANNER Y FRASE DEL DÍA
# ---------------------------------------------------------
def mostrar_banner():
    st.markdown('<div class="franja-marca"></div>', unsafe_allow_html=True)
    posibles_nombres = ["banner.jpeg", "banner.jpg", "banner.png", "encabezado.png", "encabezado.jpg"]
    encontrado = False
    for nombre in posibles_nombres:
        if os.path.exists(nombre):
            st.image(nombre, use_container_width=True)
            encontrado = True
            break
    if not encontrado:
        st.markdown("<h1 style='text-align: center;'>LA VOZ QUE UNE</h1>", unsafe_allow_html=True)
        st.markdown("<p class='eslogan-comunidad' style='text-align: center;'>Construyendo comunidad organizada, comprometida y solidaria</p>", unsafe_allow_html=True)

def mostrar_frase_desplazable():
    if os.path.exists(FRASE_FILE):
        with open(FRASE_FILE, "r", encoding="utf-8") as f:
            frase = f.read().strip()
        if frase:
            st.markdown(f'''
            <div class="cinta-contenedor">
                <div class="cinta-texto">📢 {frase}</div>
            </div>
            ''', unsafe_allow_html=True)

def guardar_frase_dia(nueva_frase):
    with open(FRASE_FILE, "w", encoding="utf-8") as f:
        f.write(nueva_frase.strip())

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
st.sidebar.markdown("**Construyendo comunidad organizada, comprometida y solidaria**")

opcion = st.sidebar.radio(
    "Navegación:",
    ["Inicio", "Historia", "Galería", "Participa", "Administración"]
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
    mostrar_banner()
    mostrar_frase_desplazable()  # <--- Cinta con texto en movimiento debajo del banner
    
    st.title("📰 La Voz que Une - Edición Digital")
    st.markdown("<p class='eslogan-comunidad'>Construyendo comunidad organizada, comprometida y solidaria</p>", unsafe_allow_html=True)
    st.write("Bienvenidos al espacio informativo y comunitario. Aquí compartimos las últimas novedades y noticias de nuestra comunidad.")
    
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
                            imagen_path = row.get("Imagen", "")

                            st.subheader(titulo)
                            if pd.notna(fecha) and str(fecha).strip() != "":
                                st.caption(f"📅 Publicado el {fecha}")
                            
                            if pd.notna(imagen_path) and str(imagen_path).strip() != "" and os.path.exists(str(imagen_path)):
                                st.image(str(imagen_path), use_container_width=True)
                                
                            st.write(contenido)
                            st.markdown("---")
        except Exception as e:
            st.error(f"Error al leer las noticias: {e}")

    mostrar_seccion_comentarios("Inicio")

# 2. HISTORIA
elif opcion == "Historia":
    mostrar_banner()
    mostrar_frase_desplazable()
    st.title("📜 Nuestra Historia")
    st.write("Un recorrido por la memoria histórica, el patrimonio y los hitos que han marcado el desarrollo de nuestro entorno y su gente.")
    
    st.markdown("""
    > *"Un pueblo que conoce su historia es un pueblo que proyecta su futuro con identidad y dignidad."*
    """)
    
    mostrar_seccion_comentarios("Historia")

# 3. GALERÍA
elif opcion == "Galería":
    mostrar_banner()
    mostrar_frase_desplazable()
    st.title("🖼️ Galería Comunitaria")
    st.write("Registros visuales, fotografías patrimoniales y actividades destacadas de la comunidad.")
    
    mostrar_seccion_comentarios("Galería")

# 4. PARTICIPA
elif opcion == "Participa":
    mostrar_banner()
    mostrar_frase_desplazable()
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
                imagen_nombre = ""
                if archivo_p is not None:
                    imagen_nombre = f"img_{int(datetime.now().timestamp())}.jpg"
                    with open(imagen_nombre, "wb") as f:
                        f.write(archivo_p.getbuffer())

                nueva_noticia = pd.DataFrame([{
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Título": f"Aporte de {nombre_p}",
                    "Contenido": mensaje_p,
                    "Contacto": correo_p,
                    "Estado": "Pendiente",
                    "Imagen": imagen_nombre
                }])
                
                try:
                    if os.path.exists(EXCEL_FILE):
                        excel_obj = pd.ExcelFile(EXCEL_FILE)
                        if "Noticias" in excel_obj.sheet_names:
                            df_ex = pd.read_excel(EXCEL_FILE, sheet_name="Noticias")
                            df_up = pd.concat([df_ex, nueva_noticia], ignore_index=True)
                        else:
                            df_up = nueva_noticia
                        with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                            df_up.to_excel(writer, sheet_name="Noticias", index=False)
                    else:
                        nueva_noticia.to_excel(EXCEL_FILE, sheet_name="Noticias", index=False)
                    st.success("¡Gracias por tu colaboración! El equipo editorial revisará tu aporte.")
                except Exception as e:
                    st.error(f"Error al enviar la colaboración: {e}")

# 5. ADMINISTRACIÓN
elif opcion == "Administración":
    st.title("⚙️ Panel de Administración")
    
    password = st.text_input("Ingrese la clave de administrador:", type="password")
    
    if password == CLAVE_ADMIN:
        st.success("Acceso concedido.")
        
        # --- NUEVA SECCIÓN: CAMBIAR LA FRASE O AVISO DEL DÍA ---
        st.subheader("💬 Frase o Aviso Desplazable del Día")
        frase_actual = ""
        if os.path.exists(FRASE_FILE):
            with open(FRASE_FILE, "r", encoding="utf-8") as f:
                frase_actual = f.read().strip()

        with st.form("form_frase_dia"):
            nueva_frase_input = st.text_input("Escriba el aviso o frase que se desplazará en la portada:", value=frase_actual)
            guardar_frase_btn = st.form_submit_button("Actualizar Frase del Día")
            if guardar_frase_btn:
                guardar_frase_dia(nueva_frase_input)
                st.success("¡Frase del día actualizada correctamente!")
                st.rerun()

        st.markdown("---")
        st.subheader("📌 Gestión de Noticias y Avisos")
        
        st.markdown("#### Publicar Nueva Noticia o Aviso Directo")
        with st.form("form_admin_noticia"):
            titulo_admin = st.text_input("Título de la noticia/aviso")
            contenido_admin = st.text_area("Contenido de la publicación (copiar de Word)")
            imagen_admin = st.file_uploader("Adjuntar imagen para la noticia (opcional)", type=["png", "jpg", "jpeg"])
            publicar_btn = st.form_submit_button("Publicar Ahora")
            
            if publicar_btn:
                if titulo_admin.strip() and contenido_admin.strip():
                    ruta_imagen = ""
                    if imagen_admin is not None:
                        ruta_imagen = f"noticia_{int(datetime.now().timestamp())}.jpg"
                        with open(ruta_imagen, "wb") as f:
                            f.write(imagen_admin.getbuffer())

                    nueva_pub = pd.DataFrame([{
                        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Título": titulo_admin,
                        "Contenido": contenido_admin,
                        "Contacto": "Administración",
                        "Estado": "Aprobado",
                        "Imagen": ruta_imagen
                    }])
                    try:
                        if os.path.exists(EXCEL_FILE):
                            excel_obj = pd.ExcelFile(EXCEL_FILE)
                            if "Noticias" in excel_obj.sheet_names:
                                df_ex = pd.read_excel(EXCEL_FILE, sheet_name="Noticias")
                                df_up = pd.concat([df_ex, nueva_pub], ignore_index=True)
                            else:
                                df_up = nueva_pub
                            with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                                df_up.to_excel(writer, sheet_name="Noticias", index=False)
                        else:
                            nueva_pub.to_excel(EXCEL_FILE, sheet_name="Noticias", index=False)
                        st.success("¡Publicación guardada exitosamente!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al guardar: {e}")
                else:
                    st.error("Por favor complete título y contenido.")
                    
        st.markdown("---")
        st.markdown("#### Revisar y Gestionar Publicaciones Pendientes y Existentes")
        
        if os.path.exists(EXCEL_FILE):
            try:
                excel_obj = pd.ExcelFile(EXCEL_FILE)
                if "Noticias" in excel_obj.sheet_names:
                    df_noticias = pd.read_excel(EXCEL_FILE, sheet_name="Noticias")
                    
                    if not df_noticias.empty:
                        df_noticias.columns = [str(col).strip().capitalize() for col in df_noticias.columns]
                        
                        for idx, row in df_noticias.iterrows():
                            col_info, col_btn1, col_btn2 = st.columns([3, 1, 1])
                            
                            titulo = row.get("Título", row.get("Titulo", "Sin título"))
                            estado = row.get("Estado", "Pendiente")
                            contacto = row.get("Contacto", "N/A")
                            
                            with col_info:
                                st.write(f"**{titulo}** | *Contacto:* {contacto} | *Estado actual:* **{estado}**")
                                st.caption(str(row.get("Contenido", ""))[:100] + "...")
                            
                            with col_btn1:
                                if st.button("✅ Aprobar", key=f"aprobar_{idx}"):
                                    df_noticias.at[idx, "Estado"] = "Aprobado"
                                    with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                                        df_noticias.to_excel(writer, sheet_name="Noticias", index=False)
                                    st.success(f"Aprobado: {titulo}")
                                    st.rerun()
                                    
                            with col_btn2:
                                if st.button("❌ Descartar", key=f"descartar_{idx}"):
                                    df_noticias.at[idx, "Estado"] = "Rechazado"
                                    with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                                        df_noticias.to_excel(writer, sheet_name="Noticias", index=False)
                                    st.warning(f"Descartado: {titulo}")
                                    st.rerun()
                                    
                            st.markdown("---")
                    else:
                        st.info("No hay publicaciones en la base de datos.")
            except Exception as e:
                st.error(f"Error al cargar la lista: {e}")
    elif password != "":
        st.error("Clave incorrecta. Intente nuevamente.")
        
