import streamlit as st
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image

def read_barcodes(image):
    """Detecta y lee códigos de barras en una imagen."""
    img = np.array(image.convert('RGB'))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    barcodes = decode(gray)
    results = []
    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type
        (x, y, w, h) = barcode.rect
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        results.append((barcode_data, barcode_type))
    return img, results

# Interfaz en Streamlit
st.title("📷 Lector de Códigos de Barras")
st.write("Sube una imagen o usa la cámara para escanear un código de barras.")

# Opción para subir imagen
uploaded_file = st.file_uploader("Sube una imagen", type=["jpg", "png", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen subida", use_column_width=True)
    processed_img, results = read_barcodes(image)
    st.image(processed_img, caption="Imagen procesada", use_column_width=True)
    
    if results:
        st.success("Códigos detectados:")
        for data, btype in results:
            st.write(f"**Código:** {data} | **Tipo:** {btype}")
    else:
        st.warning("No se detectaron códigos de barras en la imagen.")

# Opción para usar la cámara
if st.button("📸 Abrir cámara para escanear"):
    st.warning("La captura con cámara requiere integraciones adicionales en Streamlit.")
    st.write("Puedes probar esta funcionalidad en local con OpenCV y el uso de la webcam.")

st.write("💡 Sube tu código a GitHub y ejecútalo en [Streamlit Community Cloud](https://share.streamlit.io/).")
