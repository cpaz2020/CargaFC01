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

import streamlit as st
import fitz  # PyMuPDF
import re

st.set_page_config(page_title="FHAB - Extractor", layout="wide")

st.title("📄 Sistema de Carga - FHAB")
st.write("Extrae datos de facturas ARCA para el formulario de Barceló.")

uploaded_file = st.file_uploader("Subir factura PDF", type="pdf")

if uploaded_file is not None:
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            texto = ""
            for page in doc:
                texto += page.get_text()
        
        # --- Lógica de Extracción Avanzada ---
        
        # 1. CUIT (Busca el formato XX-XXXXXXXX-X)
        cuit_regex = re.search(r'\d{2}-\d{8}-\d', texto)
        cuit_val = cuit_regex.group(0) if cuit_regex else ""

        # 2. Número de Comprobante (Busca Punto de Venta - Número)
        nro_regex = re.search(r'(\d{5}-\d{8})', texto)
        nro_val = nro_regex.group(0) if nro_regex else ""

        # 3. Fecha (Busca DD/MM/AAAA)
        fecha_regex = re.search(r'(\d{2}/\d{2}/\d{4})', texto)
        fecha_val = fecha_regex.group(0) if fecha_regex else ""

        # 4. CAE
        cae_regex = re.search(r'CAE\s*(?:N.)?[:\s]*(\d{14})', texto)
        cae_val = cae_regex.group(1) if cae_regex else ""

        # 5. Importe Total (Busca el valor numérico después de 'Total: $')
        # Esta regex es más fuerte para el formato de ARCA
        total_regex = re.search(r'Importe Total:\s*\$?\s*([\d\.,]+)', texto, re.IGNORECASE)
        total_val = total_regex.group(1) if total_regex else ""

        # --- Interfaz de Confirmación ---
        st.success("✅ Datos extraídos con éxito")
        
        st.subheader("Verifique los datos antes de cargar:")
        col1, col2 = st.columns(2)
        
        with col1:
            f_cuit = st.text_input("CUIT Emisor", value=cuit_val)
            f_nro = st.text_input("Nro. Factura", value=nro_val)
            f_fecha = st.text_input("Fecha Emisión", value=fecha_val)
        
        with col2:
            f_total = st.text_input("Monto Total ($)", value=total_val)
            f_cae = st.text_input("Número de CAE", value=cae_val)
            
        st.divider()
        
        # --- El Paso al Formulario ---
        st.info("Al hacer clic, se abrirá el formulario. Copia y pega los datos de arriba.")
        st.link_button("🚀 Abrir Formulario de la Universidad", "https://validaciones.barcelo.edu.ar/subircomprobantes/index.php")

    except Exception as e:
        st.error(f"Error al procesar: {e}")
