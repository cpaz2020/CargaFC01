import streamlit as st
import fitz  # PyMuPDF
import re
import json
from streamlit_extras.add_vertical_space import add_vertical_space # Opcional

st.set_page_config(page_title="FHAB - AutoCarga Pro", layout="centered", page_icon="🚀")

st.title("🚀 Sistema de Extracción FHAB")

uploaded_file = st.file_uploader("Subir Factura PDF", type="pdf")

if uploaded_file is not None:
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            texto = "".join([page.get_text() for page in doc])

        # Extracción de datos
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

        st.success("✅ Factura procesada")

        # --- NUEVO BOTÓN DE COPIADO ---
        st.subheader("Paso 1: Copia los datos")
        
        # Este es el truco para el botón de copiado manual
        st.info("Haz clic en el botón de abajo para copiar los datos automáticamente.")
        
        # Botón que usa un componente de texto con valor pre-seleccionado
        st.text_input("Datos listos para copiar:", value=json_data, help="Haz clic derecho y copiar, o usa el botón de abajo")

        # Botón con JS para copiar al portapapeles
        copy_button_js = f"""
            <button style="width:100%; height:50px; background-color:#28a745; color:white; border:none; border-radius:5px; font-weight:bold; cursor:pointer;" 
            onclick="navigator.clipboard.writeText('{json_data}')">
                📋 CLICK AQUÍ PARA COPIAR DATOS
            </button>
        """
        st.components.v1.html(copy_button_js, height=70)

        st.subheader("Paso 2: Ve al formulario")
        st.link_button("Ir al Formulario de Barceló ↗️", "https://validaciones.barcelo.edu.ar/subircomprobantes/index.php")

    except Exception as e:
        st.error(f"Error: {e}")
