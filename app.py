import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import re
import cv2

st.title("Extracción de km y hora del tablero de un auto")

def preprocess_image(image):
    # Convertir a escala de grises
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    # Aplicar umbral binario
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return thresh

def extract_km_and_time(text):
    # Patrones de expresiones regulares para kilómetros y hora
    km_pattern = re.compile(r'\b\d{5,7}\b')
    # Adaptamos la expresión regular para capturar "14:17" adecuadamente
    hora_pattern = re.compile(r'\b\d{1,2}[:;]\d{2}\b')
    
    km_match = km_pattern.findall(text)
    hora_match = hora_pattern.findall(text)
    
    km_text = km_match[0] if km_match else "No se encontraron kilómetros"
    
    # Adaptamos el resultado de la hora para formatear "14/7" como "14:17" si es necesario
    hora_text = "No se encontró hora"
    if hora_match:
        hora_text = hora_match[0].replace(';', ':')
    
    return km_text, hora_text

uploaded_file = st.file_uploader("Sube una imagen del tablero del auto", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Imagen subida', use_column_width=True)
    
    # Preprocesar la imagen
    processed_image = preprocess_image(image)
    
    # Inicializar el lector de easyocr
    reader = easyocr.Reader(['es'])  # Usa el idioma adecuado para tu caso
    
    # Realizar OCR
    text = reader.readtext(processed_image, detail=0)
    text_joined = " ".join(text)
    
    st.write("Texto extraído:")
    st.text(text_joined)
    
    # Extraer kilómetros y hora
    km_text, hora_text = extract_km_and_time(text_joined)
    
    if km_text != "No se encontraron kilómetros":
        st.write("Kilómetros:")
        st.text(km_text)
    else:
        st.write(km_text)
    
    if hora_text != "No se encontró hora":
        st.write("Hora:")
        st.text(hora_text)
    else:
        st.write(hora_text)
