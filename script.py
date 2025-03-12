import streamlit as st
import pandas as pd
import cv2
from zbarlight import scan_codes
from PIL import Image
import numpy as np
import os

def decode_barcode(image):
    """ Decodifica códigos de barras o QR en una imagen. """
    codes = scan_codes('qrcode', Image.fromarray(image))
    return [code.decode('utf-8') for code in codes] if codes else []

def save_to_excel(data, file_path='codigos.xlsx'):
    """ Guarda los datos en un archivo Excel evitando la notación científica. """
    df = pd.DataFrame({'Código': data})
    df['Código'] = df['Código'].astype(str)  # Asegurar que se almacena como texto
    df.to_excel(file_path, index=False, engine='openpyxl')

def main():
    st.title("Escáner de Códigos de Barras y QR")
    st.write("Usa la cámara para escanear códigos y guardarlos en un archivo Excel.")
    
    scanned_codes = []
    
    uploaded_file = st.file_uploader("Sube una imagen para escanear", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        codes = decode_barcode(image)
        if codes:
            st.success(f"Códigos escaneados: {', '.join(codes)}")
            scanned_codes.extend(codes)
        else:
            st.warning("No se detectaron códigos en la imagen.")
    
    if 'codes' not in st.session_state:
        st.session_state.codes = []
    
    if scanned_codes:
        st.session_state.codes.extend(scanned_codes)
    
    if st.session_state.codes:
        st.write("Códigos escaneados:")
        st.table(pd.DataFrame({'Código': st.session_state.codes}))
    
    if st.button("Guardar en Excel"):
        save_to_excel(st.session_state.codes)
        st.success("Códigos guardados en codigos.xlsx")
        st.session_state.codes = []

if __name__ == "__main__":
    main()
