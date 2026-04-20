import streamlit as st
import fitz  # PyMuPDF
import re
import json

st.set_page_config(page_title="FHAB - AutoCarga Pro", layout="centered", page_icon="🚀")

st.title("🚀 Sistema de Extracción FHAB")
st.write("Extrae datos y autocompleta el formulario de Barceló.")

uploaded_file = st.file_uploader("Subir Factura PDF", type="pdf")

if uploaded_file is not None:
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            texto = "".join([page.get_text() for page in doc])

        # --- Extracción de datos ---
        cuit_match = re.search(r'CUIT[:\s]*([\d\-]+)', texto)
        cuit_val = "".join(re.findall(r'\d+', cuit_match.group(1)))[:11] if cuit_match else ""
        
        fecha_match = re.search(r'(\d{2})/(\d{2})/(\d{4})', texto)
        fecha_val_iso = f"{fecha_match.group(3)}-{fecha_match.group(2)}-{fecha_match.group(1)}" if fecha_match else ""
        
        comp_match = re.search(r'(\d{4,5})\s?-\s?(\d{8})', texto)
        ptovta = comp_match.group(1) if comp_match else ""
        nrocomp = comp_match.group(2) if comp_match else ""
        
        total_match = re.search(r'(?:Total|Importe Total):\s*\$?\s*([\d\.,]+)', texto, re.IGNORECASE)
        total_val = total_match.group(1).replace('.', '').replace(',', '.') if total_match else ""

        data_factura = {
            "cuit": cuit_val,
            "fecha_iso": fecha_val_iso,
            "ptovta": ptovta,
            "nro": nrocomp,
            "total": total_val
        }
        json_data = json.dumps(data_factura)

        st.success("✅ Factura procesada correctamente")

        # --- Interfaz de Copiado ---
        st.subheader("Paso 1: Copia los datos")
        st.info("Haz clic en el icono de copiar (arriba a la derecha del cuadro negro).")
        st.code(json_data, language="json")

        st.subheader("Paso 2: Ve al formulario")
        st.link_button("Ir al Formulario de Barceló ↗️", "https://validaciones.barcelo.edu.ar/subircomprobantes/index.php")

    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
