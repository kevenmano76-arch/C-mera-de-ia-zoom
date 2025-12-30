import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuração segura da API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Configure a chave API nos Secrets!")

st.set_page_config(page_title="IA Zoom Camera", layout="wide")

# Estilo da Câmera
st.markdown("<style>.stApp {background-color: #000; color: white;}</style>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 4, 1])

with col1: st.button("🖼️")
with col3: st.button("🔄")

with col2:
    foto = st.camera_input(" ")
    zoom = st.select_slider("Zoom", options=[f"{i}x" for i in range(1, 51)], value="1x")
    
    if st.button("📸 PROCESSAR FOTO", use_container_width=True):
        if foto:
            try:
                img = Image.open(foto)
                # Modelo flash que é mais rápido e estável
                model = genai.GenerativeModel('models/gemini-1.5-flash')
                
                with st.spinner("IA lendo detalhes e melhorando a imagem..."):
                    # Comando simplificado para evitar o erro NotFound
                    response = model.generate_content([
                        f"Aumente a nitidez e leia os textos desta imagem como se fosse um zoom de {zoom}.", 
                        img
                    ])
                    st.image(img, caption="Original")
                    st.success("Resultado da IA:")
                    st.write(response.text)
            except Exception as e:
                st.error(f"Erro na IA: {e}")
        else:
            st.warning("Tire uma foto primeiro!")
            
