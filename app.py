import streamlit as st
import fitz  # PyMuPDF
import re

# Configuración de la página
st.set_page_config(page_title="FHAB - Extractor de Facturas", layout="centered", page_icon="📄")

# Estilo para mejorar la estética
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📄 Sistema de Carga FHAB")
st.info("Sube una factura de ARCA y los datos se extraerán automáticamente para el formulario de Barceló.")

# Componente de subida de archivos
uploaded_file = st.file_uploader("Arrastra aquí tu factura PDF", type="pdf")

if uploaded_file is not None:
    try:
        # Procesamiento del PDF
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            texto = ""
            for page in doc:
                texto += page.get_text()
        
        # --- Extracción de Datos ---
        # CUIT (XX-XXXXXXXX-X)
        cuit_match = re.search(r'\d{2}-\d{8}-\d', texto)
        cuit_val = cuit_match.group(0) if cuit_match else "No encontrado"

        # Fecha (DD/MM/AAAA)
        fecha_match = re.search(r'(\d{2}/\d{2}/\d{4})', texto)
        fecha_val = fecha_match.group(0) if fecha_match else "No encontrada"

        # CAE (14 dígitos)
        cae_match = re.search(r'CAE\s*(?:N.)?[:\s]*(\d{14})', texto)
        cae_val = cae_match.group(1) if cae_match else "No encontrado"

        # Total (Maneja punto y coma de ARCA)
        total_match = re.search(r'(?:Total|Importe Total):\s*\$?\s*([\d\.,]+)', texto, re.IGNORECASE)
        total_val = total_match.group(1) if total_match else "0.00"

        st.success("✅ Factura procesada con éxito")
        
        st.subheader("📋 Datos para el formulario")
        st.write("Usa los botones de la derecha para copiar los valores rápidamente.")

        # Mostrar datos en filas con opción de copiar
        col_label, col_val = st.columns([1, 2])
        
        with col_label:
            st.write("**CUIT:**")
            st.write("**Fecha:**")
            st.write("**CAE:**")
            st.write("**Total:**")

        with col_val:
            st.code(cuit_val, language=None)
            st.code(fecha_val, language=None)
            st.code(cae_val, language=None)
            st.code(total_val, language=None)

        st.divider()
        
        # Botón de enlace al formulario externo
        st.link_button("🚀 Ir al Formulario de Barceló", "https://validaciones.barcelo.edu.ar/subircomprobantes/index.php")
        st.caption("Recuerda pegar los datos extraídos en los campos correspondientes.")

    except Exception as e:
        st.error(f"Error técnico: {e}")
else:
    st.warning("Esperando archivo PDF...")
