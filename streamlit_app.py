import streamlit as st
import google.generativeai as genai

# Configura tu clave de API de Google
genai.configure(api_key="AIzaSyDb82ILBtthgNiDkDGa2MiPsPCnDZ3wWeY")

# Inicializa el modelo
model = genai.GenerativeModel("gemini-pro")

# Título de la aplicación
st.title("Adrimax AI")

# Entrada de texto del usuario
prompt = st.text_input("Introduce tu pregunta:")

# Procesa la entrada cuando se proporciona un prompt
if prompt:
    respuesta = model.generate_content(prompt)
    st.write(respuesta.text)
