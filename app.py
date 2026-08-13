# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA
# ---------------------------------------------------------
st.set_page_config(page_title="El Bosque 1", page_icon="🌳", layout="wide")

# ---------------------------------------------------------
# 2. DISEÑO COLORIDO Y ATRACTIVO (ESTILOS DIRECTOS)
# ---------------------------------------------------------
st.markdown('''
    <style>
    /* 1. Color de fondo de TODA la página */
    .stApp, [data-testid="stAppViewContainer"], .main {
        background-color: #DDEEE0 !important; /* Verde menta/suave colorido */
    }

    /* 2. Banner/Encabezado principal */
    .main-header { 
        background-color: #1E5631 !important; /* Verde bosque oscuro */
        padding: 25px; 
        border-radius: 15px; 
        color: #FFFFFF !important; 
        text-align: center; 
        margin-bottom: 25px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    }

    /* 3. Tarjetas con bordes coloridos para las noticias y avisos */
    .card-noticia { 
        background-color: #FFFFFF !important; 
        padding: 20px; 
        border-radius: 12px; 
        border-left: 8px solid #1E5631 !important; /* Borde verde */
        margin-bottom: 18px; 
        box-shadow: 0 3px 8px rgba(0,0,0,0.1);
        color: #1F2937 !important;
    }

    .card-aviso { 
        background-color: #FFFFFF !important; 
        padding: 20px; 
        border-radius: 12px; 
        border-left: 8px solid #D97706 !important; /* Borde Naranja/Dorado para clasificados */
        margin-bottom: 18px; 
        box-shadow: 0 3px 8px rgba(0,0,0,0.1);
        color: #1F2937 !important;
    }

    .card-humor { 
        background-color: #FFFFFF !important; 
        padding: 20px; 
        border-radius: 12px; 
        border-left: 8px solid #2563EB !important; /* Borde Azul para la Chispa del Barrio */
        margin-bottom: 18px; 
        box-shadow: 0 3px 8px rgba(0,0,0,0.1);
        color: #1F2937 !important;
    }

    /* 4. Botones muy visibles y coloridos */
    div[data-testid="stFormSubmitButton"] > button, .stButton > button {
        background-color: #2E7D32 !important; /* Verde vivo */
        color: #FFFFFF !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 14px 30px !important;
        font-weight: bold !important;
        font-size: 18px !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
        width: 100% !important;
    }

    div[data-testid="stFormSubmitButton"] > button:hover, .stButton > button:hover {
        background-color: #1B5E20 !important; /* Verde intenso al pasar el cursor */
        cursor: pointer !important;
    }

    /* 5. Menú de Pestañas (Tabs) */
    div[data-baseweb="tab-list"] {
        background-color: #C2E0C6 !important;
        padding: 8px;
        border-radius: 10px;
    }

    button[data-baseweb="tab"] {
        font-size: 16px !important;
        font-weight: bold !important;
        color: #1E5631 !important;
    }

    button[aria-selected="true"] {
        background-color: #FFFFFF !important;
        border-radius: 8px !important;
        color: #1E5631 !important;
    }
    </style>
''', unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. GESTIÓN DE BASE DE DATOS (EXCEL)
# ---------------------------------------------------------
EXCEL_FILE = "datos_periodico.xlsx"

def crear_excel_inicial():
    data_clasificados = pd.DataFrame([
        {"Oficio/Producto": "Gasfitería Don Roberto", "Detalle": "Reparación de cañerías y arreglos generales", "Contacto": "+56 9 8765 4321", "Estado": "Aprobado"},
        {"Oficio/Producto": "Amasandería La Esquina", "Detalle": "Pan amasado y empanadas el fin de semana", "Contacto": "+56 9 1234 5678", "Estado": "Aprobado"}
    ])
    data_humor = pd.DataFrame([
        {"Tipo": "Chiste del Día", "Contenido": "— Vecino, ¿sabe si en este pasaje hay buena señal?\n— ¡Súper buena! Cada vez que sale a barrer la vecina del frente, nos enteramos de todas las noticias.", "Estado": "Aprobado"}
    ])
    data_noticias = pd.DataFrame([
        {"Sección": "Inicio", "Título": "Jornada de Presentación del Portal Web", "Contenido": "Presentación oficial del periódico digital para los pobladores y junta de vecinos.", "Estado": "Aprobado"}
    ])
    data_pendientes = pd.DataFrame(columns=["Fecha", "Nombre", "Sección", "Mensaje", "Estado"])
    
    with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl") as writer:
        data_clasificados.to_excel(writer, sheet_name="Clasificados", index=False)
        data_humor.to_excel(writer, sheet_name="Humor", index=False)
        data_noticias.to_excel(writer, sheet_name="Noticias", index=False)
        data_pendientes.to_excel(writer, sheet_name="Pendientes", index=False)

def cargar_datos():
    if not os.path.exists(EXCEL_FILE):
        crear_excel_inicial()
    
    try:
        xls = pd.ExcelFile(EXCEL_FILE)
        if "Pendientes" not in xls.sheet_names:
            crear_excel_inicial()
            xls = pd.ExcelFile(EXCEL_FILE)

        clasificados = pd.read_excel(xls, sheet_name="Clasificados")
        humor = pd.read_excel(xls, sheet_name="Humor")
        noticias = pd.read_excel(xls, sheet_name="Noticias")
        pendientes = pd.read_excel(xls, sheet_name="Pendientes")
        return clasificados, humor, noticias, pendientes
    except PermissionError:
        st.error("⚠️ El archivo Excel está abierto. Por favor ciérrelo.")
        st.stop()

def guardar_pendiente(nombre, seccion, mensaje):
    try:
        clasificados, humor, noticias, pendientes = cargar_datos()
        
        nuevo_registro = pd.DataFrame([{
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Nombre": nombre,
            "Sección": seccion,
            "Mensaje": mensaje,
            "Estado": "Pendiente"
        }])
        
        pendientes_actualizado = pd.concat([pendientes, nuevo_registro], ignore_index=True)
        
        with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl") as writer:
            clasificados.to_excel(writer, sheet_name="Clasificados", index=False)
            humor.to_excel(writer, sheet_name="Humor", index=False)
            noticias.to_excel(writer, sheet_name="Noticias", index=False)
            pendientes_actualizado.to_excel(writer, sheet_name="Pendientes", index=False)
            
        return True
    except PermissionError:
        st.error("⚠️ Cierre el archivo Excel e intente de nuevo.")
        return False

# Cargar datos
df_clasificados, df_humor, df_noticias, _ = cargar_datos()

# ---------------------------------------------------------
# 4. INTERFAZ GRÁFICA Y CONTENIDOS
# ---------------------------------------------------------
st.markdown('''
    <div class="main-header">
        <h1>🌳 EL BOSQUE 1: Periódico Digital</h1>
        <p>Voz Comunitaria • 50+ Años de Historia • La Pincoya</p>
    </div>
''', unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Inicio", 
    "📜 Historia y Memoria", 
    "🛠️ Avisos y Clasificados", 
    "📢 La Voz del Barrio", 
    "🎭 La Chispa del Barrio",
    "✍️ Participa"
])

with tab1:
    st.header("Bienvenido al Periódico Digital de la Población El Bosque 1")
    st.success("📌 Próxima Reunión: Martes en la sede comunitaria.")
    for _, row in df_noticias[df_noticias["Estado"] == "Aprobado"].iterrows():
        st.markdown(f'''
            <div class="card-noticia">
                <h3>{row['Título']}</h3>
                <p>{row['Contenido']}</p>
            </div>
        ''', unsafe_allow_html=True)

with tab2:
    st.header("50+ Años de Memoria Viva")
    st.markdown('''
        <div class="card-noticia">
            <p>A comienzos de los años 70, las primeras familias llegaron a estos terrenos guiadas por el sueño de una vivienda digna y una comunidad unida.</p>
        </div>
    ''', unsafe_allow_html=True)

with tab3:
    st.header("Pizarra Comunitaria de Clasificados")
    aprobados = df_clasificados[df_clasificados["Estado"] == "Aprobado"]
    cols = st.columns(3)
    for idx, (_, row) in enumerate(aprobados.iterrows()):
        with cols[idx % 3]:
            st.markdown(f'''
                <div class="card-aviso">
                    <h4>🛠️ {row['Oficio/Producto']}</h4>
                    <p>{row['Detalle']}</p>
                    <p><b>Contacto:</b> {row['Contacto']}</p>
                </div>
            ''', unsafe_allow_html=True)

with tab4:
    st.header("Columnas de Opinión y Petitorios")
    st.warning("📣 Mejora de Luminarias: Catastro en pasajes interiores.")

with tab5:
    st.header("🎭 La Chispa del Barrio")
    st.write("Un espacio para la alegría, el buen humor y las sonrisas compartidas entre vecinos.")
    humor_aprobado = df_humor[df_humor["Estado"] == "Aprobado"]
    for _, row in humor_aprobado.iterrows():
        st.markdown(f'''
            <div class="card-humor">
                <h4>😄 {row['Tipo']}</h4>
                <p>{row['Contenido']}</p>
            </div>
        ''', unsafe_allow_html=True)

with tab6:
    st.header("Envía tu Noticia, Aviso o Historia")
    with st.form("form_publicacion", clear_on_submit=True):
        nombre = st.text_input("Tu Nombre o Seudónimo:")
        seccion = st.selectbox("Sección a la que envías:", ["Aviso Clasificado", "La Chispa del Barrio", "Historia / Noticia"])
        mensaje = st.text_area("Escribe tu contenido aquí:")
        enviado = st.form_submit_button("🚀 Enviar Publicación al Periódico")
        
        if enviado:
            if nombre.strip() != "" and mensaje.strip() != "":
                exito = guardar_pendiente(nombre, seccion, mensaje)
                if exito:
                    st.success("¡Muchas gracias! Tu mensaje ha sido registrado correctamente y se guardó en la bandeja del equipo editorial.")
            else:
                st.error("Por favor completa tu nombre y el mensaje antes de enviar.")