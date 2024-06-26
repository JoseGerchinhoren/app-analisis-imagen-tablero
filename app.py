import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import re

st.title("Extracción de km y hora del tablero de un auto")

uploaded_file = st.file_uploader("Sube una imagen del tablero del auto", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Imagen subida', use_column_width=True)

    # Inicializar el lector de easyocr
    reader = easyocr.Reader(['es'])  # Usa el idioma adecuado para tu caso

    # Realizar OCR
    text = reader.readtext(np.array(image), detail=0)

    st.write("Texto extraído:")
    st.text(" ".join(text))

    # Ejemplo de expresiones regulares para extraer km y hora
    km_pattern = re.compile(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)? km\b')
    hora_pattern = re.compile(r'\b\d{1,2}:\d{2}(:\d{2})?\b')

    text_joined = " ".join(text)
    km_match = km_pattern.search(text_joined)
    hora_match = hora_pattern.search(text_joined)

    if km_match:
        st.write("Kilómetros:")
        st.text(km_match.group())
    else:
        st.write("No se encontraron kilómetros en el texto extraído.")

    if hora_match:
        st.write("Hora:")
        st.text(hora_match.group())
    else:
        st.write("No se encontró hora en el texto extraído.")
