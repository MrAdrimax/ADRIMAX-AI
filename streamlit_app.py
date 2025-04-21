# 1) Instala las librerías necesarias
pip install google-genai pillow requests ipywidgets

# 2) Interfaz completa con widgets
from google import genai
from google.genai import types
import requests
from io import BytesIO
from PIL import Image as PILImage
from IPython.display import display, clear_output, Image as IPyImage
import ipywidgets as widgets

# --- Inputs ---
api_key = widgets.Password(
    placeholder='Tu API Key de Google',
    description='API Key:',
    layout=widgets.Layout(width='70%')
)
model_text = widgets.Dropdown(
    options=['gemini-2.0-flash','gemini-2.0-turbo'],
    value='gemini-2.0-flash',
    description='Modelo texto:'
)
model_image = widgets.Dropdown(
    options=['gemini-2.0-flash-exp-image-generation'],
    value='gemini-2.0-flash-exp-image-generation',
    description='Modelo img:'
)

text_prompt = widgets.Textarea(
    placeholder='Escribe tu prompt de texto aquí',
    description='Prompt texto:',
    layout=widgets.Layout(width='100%', height='80px')
)
btn_text = widgets.Button(description='Generar Texto', button_style='info')

img_prompt = widgets.Text(
    placeholder='Prompt para generar imagen',
    description='Prompt img:',
    layout=widgets.Layout(width='100%')
)
btn_image = widgets.Button(description='Generar Imagen', button_style='success')

img_url = widgets.Text(
    placeholder='URL de imagen a analizar',
    description='URL imagen:',
    layout=widgets.Layout(width='100%')
)
btn_analyze = widgets.Button(description='Analizar Imagen', button_style='warning')

output = widgets.Output()

# --- Mostrar inputs ---
display(widgets.VBox([
    api_key, model_text, model_image,
    widgets.HTML("<hr><b>🔹 Texto</b>"),
    text_prompt, btn_text,
    widgets.HTML("<hr><b>🔹 Imagen</b>"),
    img_prompt, btn_image,
    widgets.HTML("<hr><b>🔹 Análisis</b>"),
    img_url, btn_analyze,
    widgets.HTML("<hr>"),
    output
]))

# --- Función para crear cliente ---
def init_client():
    return genai.Client(api_key=api_key.value)

# --- Callbacks ---
def on_text(_):
    with output:
        clear_output()
        if not api_key.value:
            print("❌ Pon tu API Key arriba.")
            return
        client = init_client()
        print("⏳ Generando texto…")
        resp = client.models.generate_content(
            model=model_text.value,
            contents=text_prompt.value
        )
        clear_output()
        print("✅ Texto generado:\n")
        print(resp.text)

def on_image(_):
    with output:
        clear_output()
        if not api_key.value:
            print("❌ Pon tu API Key arriba.")
            return
        client = init_client()
        print("⏳ Generando imagen…")
        # <-- Aquí está la corrección: pedimos TEXT + IMAGE
        resp = client.models.generate_content(
            model=model_image.value,
            contents=img_prompt.value,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT','IMAGE']
            )
        )
        clear_output()
        # Mostramos solo la parte de imagen
        for part in resp.candidates[0].content.parts:
            if part.inline_data:
                img = PILImage.open(BytesIO(part.inline_data.data))
                display(img)
                break

def on_analyze(_):
    with output:
        clear_output()
        if not api_key.value:
            print("❌ Pon tu API Key arriba.")
            return
        client = init_client()
        print("⏳ Analizando imagen…")
        img_data = requests.get(img_url.value).content
        resp = client.models.generate_content(
            model=model_text.value,
            contents=[
                "Describe qué ves en esta imagen:",
                types.Part.from_bytes(data=img_data, mime_type="image/jpeg")
            ]
        )
        clear_output()
        display(IPyImage(img_data))
        print("\n✅ Descripción:\n")
        print(resp.text)

# --- Asignar callbacks a los botones ---
btn_text.on_click(on_text)
btn_image.on_click(on_image)
btn_analyze.on_click(on_analyze)
