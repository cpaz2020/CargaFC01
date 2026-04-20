import streamlit as st
import fitz  # PyMuPDF
import re
import json

st.set_page_config(page_title="FHAB - AutoCarga Pro", layout="centered", page_icon="🚀")

st.title("🚀 Sistema de Extracción FHAB")
st.write("Sube tu factura para copiar los datos y autocompletar el formulario.")

uploaded_file = st.file_uploader("Subir Factura PDF", type="pdf")

if uploaded_file is not None:
    try:
        # 1. Leer el PDF
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            texto = ""
            for page in doc:
                texto += page.get_text()

        # 2. Extraer datos con Regex (Lógica mejorada)
        cuit_match = re.search(r'CUIT[:\s]*([\d\-]+)', texto)
        cuit_val = "".join(re.findall(r'\d+', cuit_match.group(1)))[:11] if cuit_match else ""

        fecha_match = re.search(r'(\d{2})/(\d{2})/(\d{4})', texto)
        fecha_val_iso = f"{fecha_match.group(3)}-{fecha_match.group(2)}-{fecha_match.group(1)}" if fecha_match else ""

        comp_match = re.search(r'(\d{4,5})\s?-\s?(\d{8})', texto)
        ptovta = comp_match.group(1) if comp_match else ""
        nrocomp = comp_match.group(2) if comp_match else ""

        total_match = re.search(r'(?:Total|Importe Total):\s*\$?\s*([\d\.,]+)', texto, re.IGNORECASE)
        total_val = total_match.group(1).replace('.', '').replace(',', '.') if total_match else ""

        # 3. Preparar el JSON para Tampermonkey
        data_factura = {
            "cuit": cuit_val,
            "fecha_iso": fecha_val_iso,
            "ptovta": ptovta,
            "nro": nrocomp,
            "total": total_val
        }

        st.success("✅ Factura procesada correctamente")

        # --- INTERFAZ DE PASOS ---
        st.subheader("Paso 1: Copia los datos al portapapeles")
        # Mostramos el JSON en un bloque de código para que el usuario use el botón "Copy" de Streamlit
        st.code(json.dumps(data_factura), language="json")
        
        st.info("Haz clic en el icono de copiar (arriba a la derecha del cuadro negro) antes de continuar.")

        st.subheader("Paso 2: Ve al formulario y presiona el botón naranja")
        st.link_button("Ir al Formulario de Barceló ↗️", "https://validaciones.barcelo.edu.ar/subircomprobantes/index.php")

    except Exception as e:
        st.error(f"Error al procesar: {e}")
else:
    st.info("Esperando que subas un archivo PDF...")
