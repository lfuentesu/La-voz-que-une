import streamlit as st

st.set_page_config(page_title="La Voz Que Une", page_icon="📰", layout="wide")

st.title("📰 LA VOZ QUE UNE")
st.subheader("Portal Digital Comunitario e Informativo - Poblacion El Bosque")
st.write("---")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Noticias", 
    "Galeria", 
    "Avisos Economicos", 
    "Humor", 
    "Historia de la Poblacion", 
    "Administracion"
])

with tab1:
    st.header("📌 Noticias Locales")
    st.write("Bienvenido al portal informativo comunal de la Poblacion El Bosque.")

with tab2:
    st.header("📸 Galeria Comunitaria")
    st.write("Espacio fotografico de nuestros eventos e historia vecinal.")

with tab3:
    st.header("💼 Avisos Economicos")
    st.write("Clasificados, emprendimientos y servicios de los vecinos.")

with tab4:
    st.header("😄 Espacio de Humor")
    st.write("Chistes, tiras comicas y contenido de entretenimiento vecinal.")

with tab5:
    st.header("📜 Historia de la Poblacion")
    st.write("Relatos, fundadores y memoria historica de nuestra comunidad.")

with tab6:
    st.header("⚙️ Administracion del Portal")
    st.write("Modulo reservado para la gestion de contenidos del sitio.")

