import streamlit as st
import fitz
import re
import json

st.set_page_config(page_title="FHAB - Extractor", layout="centered")
st.title("🚀 Extractor de Facturas FHAB")

uploaded_file = st.file_uploader("Subir factura PDF", type="pdf")

if uploaded_file is not None:
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            texto = "".join([page.get_text() for page in doc])

        # Extracción segura
        c_match = re.search(r'CUIT[:\s]*([\d\-]+)', texto)
        cuit = "".join(re.findall(r'\d+', c_match.group(1)))[:11] if c_match else ""
        
        f_match = re.search(r'(\d{2})/(\d{2})/(\d{4})', texto)
        fecha = f"{f_match.group(3)}-{f_match.group(2)}-{f_match.group(1)}" if f_match else ""
        
        comp = re.search(r'(\d{4,5})\s?-\s?(\d{8})', texto)
        total_match = re.search(r'(?:Total|Importe Total):\s*\$?\s*([\d\.,]+)', texto, re.IGNORECASE)
        total = total_match.group(1).replace('.', '').replace(',', '.') if total_match else ""

        data = {
            "cuit": cuit, 
            "fecha": fecha, 
            "ptovta": comp.group(1) if comp else "", 
            "nro": comp.group(2) if comp else "", 
            "total": total
        }
        
        st.success("✅ Factura procesada")
        st.info("1. Haz clic en el icono de copiar del cuadro de abajo.")
        st.code(json.dumps(data), language="json")
        st.write("2. Ve a la web de Barceló y haz clic en el marcador '🚀 PEGAR FHAB' de tu navegador.")
        
    except Exception as e:
        st.error(f"Error: {e}")
