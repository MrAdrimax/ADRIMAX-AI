import streamlit as st

# Título de la aplicación
st.title("ADRIMAX-AI")

# Texto de bienvenida
st.write("¡Bienvenid@s a Adrimax AI")

# Entrada de texto
nombre = st.text_input("Ingresa tu nombre:")

# Botón para mostrar el nombre
if st.button("Mostrar nombre"):
    st.write(f"Hola, {nombre}!")
