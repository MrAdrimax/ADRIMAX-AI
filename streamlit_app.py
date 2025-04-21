import streamlit as st
import google.generativeai as genai
from google.generativeai import types
import requests
from io import BytesIO
from PIL import Image as PILImage

# Configuración de la API Key
api_key = st.text_input("AIzaSyDb82ILBtthgNiDkDGa2MiPsPCnDZ3wWeY", type="password")

# Selección de modelos
model_text = st.selectbox("🧠 Modelo de texto", ['gemini-2.0-flash', 'gemini-2.0-turbo'])
model_image = st.selectbox("🖼️ Modelo de imagen", ['gemini-2.0-flash-exp-image-generation'])

# Inicialización del cliente
def init_client():
    genai.configure(api_key=api_key)
    return genai.GenerativeModel

# Generación de texto
st.markdown("## ✍️ Generar Texto")
text_prompt = st.text_area("Escribe tu prompt de texto aquí")
if st.button("Generar Texto"):
    if not api_key:
        st.error("❌ Por favor, introduce tu API Key.")
    elif not text_prompt:
        st.warning("⚠️ El prompt de texto está vacío.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_text)
            response = model.generate_content(text_prompt)
            st.success("✅ Texto generado:")
            st.write(response.text)
        except Exception as e:
            st.error(f"❌ Error al generar texto: {e}")

# Generación de imagen
import streamlit as st
import google.generativeai as genai
from PIL import Image
import requests
from io import BytesIO

# Configura tu API key
genai.configure(api_key="AIzaSyDb82ILBtthgNiDkDGa2MiPsPCnDZ3wWeY")

# Inicializa el modelo Imagen 3
model = genai.GenerativeModel("imagen-3")

# Interfaz de Streamlit
st.title("Generador de Imágenes con Imagen 3")

prompt = st.text_input("Escribe tu prompt para generar una imagen:")

if st.button("Generar Imagen"):
    if prompt:
        try:
            response = model.generate_content(prompt)
            # Suponiendo que la respuesta contiene una URL de la imagen generada
            image_url = response.text  # Ajusta esto según la estructura real de la respuesta
            image_response = requests.get(image_url)
            image = Image.open(BytesIO(image_response.content))
            st.image(image, caption="Imagen Generada")
        except Exception as e:
            st.error(f"Error al generar la imagen: {e}")
    else:
        st.warning("Por favor, ingresa un prompt para generar una imagen.")


# Análisis de imagen
st.markdown("## 🔍 Analizar Imagen")
img_url = st.text_input("Introduce la URL de la imagen a analizar")
if st.button("Analizar Imagen"):
    if not api_key:
        st.error("❌ Por favor, introduce tu API Key.")
    elif not img_url:
        st.warning("⚠️ La URL de la imagen está vacía.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_text)
            img_data = requests.get(img_url).content
            response = model.generate_content(
                contents=[
                    "Describe qué ves en esta imagen:",
                    types.Part.from_bytes(data=img_data, mime_type="image/jpeg")
                ]
            )
            st.image(img_url, caption="🖼️ Imagen a analizar")
            st.success("✅ Descripción:")
            st.write(response.text)
        except Exception as e:
            st.error(f"❌ Error al analizar imagen: {e}")
