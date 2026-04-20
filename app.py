import streamlit as st
import fitz  # PyMuPDF
import re

# Configuración básica
st.set_page_config(page_title="FHAB - Extractor", layout="centered")

st.title("📄 Extractor de Facturas FHAB")

# Este es el componente que crea el botón de subida
uploaded_file = st.file_uploader("Arrastra aquí tu factura PDF", type="pdf")

if uploaded_file is not None:
    try:
        # Leer el contenido del PDF
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            texto = ""
            for page in doc:
                texto += page.get_text()
        
        st.success("✅ Archivo leído correctamente")
        
        # --- Búsqueda de datos ---
        # CUIT
        cuit = re.search(r'\d{2}-\d{8}-\d', texto)
        # CAE
        cae = re.search(r'CAE[:\s]*(\d{14})', texto)
        
        # Mostrar resultados en pantalla
        st.subheader("Datos extraídos:")
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("CUIT detectado", value=cuit.group(0) if cuit else "No encontrado")
        
        with col2:
            st.text_input("CAE detectado", value=cae.group(1) if cae else "No encontrado")

    except Exception as e:
        st.error(f"Hubo un problema al procesar el PDF: {e}")

else:
    st.info("Esperando que subas un archivo...")
