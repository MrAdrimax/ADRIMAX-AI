import streamlit as st
from google import genai
from google.genai import types
import requests
from io import BytesIO
from PIL import Image as PILImage

# Configuración de la API Key
api_key = st.text_input("🔑 Ingresa tu API Key de Google:", type="password")

# Selección de modelos
model_text = st.selectbox("📝 Modelo de texto:", ['gemini-2.0-flash', 'gemini-2.0-turbo'])
model_image = st.selectbox("🖼️ Modelo de imagen:", ['gemini-2.0-flash-exp'])

# Inicialización del cliente
def init_client():
    return genai.Client(api_key=api_key)

# Generación de texto
st.subheader("🔹 Generar Texto")
text_prompt = st.text_area("Escribe tu prompt de texto aquí:")
if st.button("Generar Texto"):
    if not api_key:
        st.error("❌ Por favor, ingresa tu API Key.")
    else:
        client = init_client()
        st.info("⏳ Generando texto…")
        try:
            resp = client.models.generate_content(
                model=model_text,
                contents=text_prompt
            )
            st.success("✅ Texto generado:")
            st.write(resp.text)
        except Exception as e:
            st.error(f"Error al generar texto: {e}")

# Generación de imagen
st.subheader("🔹 Generar Imagen")
img_prompt = st.text_input("Prompt para generar imagen:")
if st.button("Generar Imagen"):
    if not api_key:
        st.error("❌ Por favor, ingresa tu API Key.")
    else:
        client = init_client()
        st.info("⏳ Generando imagen…")
        try:
            resp = client.models.generate_content(
                model=model_image,
                contents=img_prompt,
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE']
                )
            )
            for part in resp.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    img = PILImage.open(BytesIO(part.inline_data.data))
                    st.image(img)
                    break
        except Exception as e:
            st.error(f"Error al generar la imagen: {e}")

# Análisis de imagen desde URL
st.subheader("🔹 Analizar Imagen desde URL")
img_url = st.text_input("URL de imagen a analizar:")
if st.button("Analizar Imagen"):
    if not api_key:
        st.error("❌ Por favor, ingresa tu API Key.")
    else:
        client = init_client()
        st.info("⏳ Analizando imagen…")
        try:
            img_data = requests.get(img_url).content
            resp = client.models.generate_content(
                model=model_text,
                contents=[
                    "Describe qué ves en esta imagen:",
                    types.Part.from_bytes(data=img_data, mime_type="image/jpeg")
                ]
            )
            st.image(img_data)
            st.success("✅ Descripción:")
            st.write(resp.text)
        except Exception as e:
            st.error(f"Error al analizar la imagen: {e}")
