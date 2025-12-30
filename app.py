import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Puxa a chave de forma segura dos Secrets do Streamlit
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("ERRO: Configure a chave API nos Secrets do Streamlit!")

st.set_page_config(layout="wide", page_title="AI Zoom Camera")

# Interface Estilizada
st.markdown("""
    <style>
    .stApp { background-color: #000; color: white; }
    div[data-testid="stCameraInput"] { border: 2px solid #333; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# Layout: Galeria (Esq), Câmera (Meio), Inverter (Dir)
col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    st.button("🖼️", help="Ver Galeria")

with col3:
    st.button("🔄", help="Alternar Câmera")

with col2:
    foto = st.camera_input(" ")
    zoom = st.select_slider("Ajuste de Zoom", options=[f"{i}x" for i in range(1, 51)], value="1x")
    
    if st.button("🔴 TIRAR FOTO E MELHORAR", use_container_width=True):
        if foto:
            with st.spinner("Processando Super-Zoom 4K..."):
                img = Image.open(foto)
                model = genai.GenerativeModel('gemini-1.5-flash')
                # Comando para a IA agir como lente
                response = model.generate_content([
                    f"Atue como uma lente telescópica. Aplique zoom de {zoom}. "
                    "Melhore a nitidez de todos os textos e detalhes pequenos para que fiquem legíveis.", 
                    img
                ])
                st.image(img, caption="Foto Original")
                st.subheader("Resultado Melhorado pela IA:")
                st.write(response.text)
        else:
            st.warning("Ative a câmera primeiro!")
  
