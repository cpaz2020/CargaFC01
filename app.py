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

        # CUIT: Limpieza de guiones
        c_match = re.search(r'CUIT[:\s]*([\d\-]+)', texto)
        cuit = "".join(re.findall(r'\d+', c_match.group(1)))[:11] if c_match else ""
        
        # FECHA: Formato YYYY-MM-DD para input type="date"
        f_match = re.search(r'(\d{2})/(\d{2})/(\d{4})', texto)
        fecha_iso = f"{f_match.group(3)}-{f_match.group(2)}-{f_match.group(1)}" if f_match else ""
        
        # COMPROBANTE: Separación de Punto de Venta y Número
        comp = re.search(r'(\d{1,5})\s?-\s?(\d{8})', texto)
        ptovta = comp.group(1).zfill(1) if comp else ""
        nrocomp = comp.group(2) if comp else ""
        
        # TOTAL: Formato 0.00
        total_match = re.search(r'(?:Total|Importe Total):\s*\$?\s*([\d\.,]+)', texto, re.IGNORECASE)
        total = total_match.group(1).replace('.', '').replace(',', '.') if total_match else ""

        data = {
            "cuit": cuit, 
            "fecha": fecha_iso, 
            "ptovta": ptovta, 
            "nro": nrocomp, 
            "total": total
        }
        
        st.success("✅ Datos listos para Barceló")
        st.code(json.dumps(data), language="json")
        st.info("Copia el código de arriba y presiona tu marcador '🚀 PEGAR FHAB'")
        
    except Exception as e:
        st.error(f"Error en el proceso: {e}")
