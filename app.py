import streamlit as st
import fitz
import re
import json
import base64

def obtener_nombre_mes(fecha_str):
    meses = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", 
              "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
    try:
        indice = int(fecha_str.split("-")[1]) - 1
        return meses[indice]
    except:
        return "MES"

st.set_page_config(page_title="FHAB - Extractor Pro", layout="centered")
st.title("🚀 Extractor y Organizador FHAB")

uploaded_file = st.file_uploader("Subir factura PDF", type="pdf")

if uploaded_file is not None:
    try:
        file_bytes = uploaded_file.read()
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            texto = "".join([page.get_text() for page in doc])

        # 1. CUIT
        c_match = re.search(r'CUIT[:\s]*([\d\-]+)', texto)
        cuit = "".join(re.findall(r'\d+', c_match.group(1)))[:11] if c_match else ""
        
        # 2. FECHA
        f_match = re.search(r'(\d{2})/(\d{2})/(\d{4})', texto)
        fecha_iso = f"{f_match.group(3)}-{f_match.group(2)}-{f_match.group(1)}" if f_match else ""
        nombre_mes = obtener_nombre_mes(fecha_iso)
        
        # 3. COMPROBANTE con relleno de ceros (zfill)
        comp = re.search(r'(\d{1,5})\s?-\s?(\d{1,8})', texto)
        ptovta = comp.group(1).zfill(4) if comp else "" # Siempre 4 dígitos
        nrocomp = comp.group(2).zfill(8) if comp else "" # Siempre 8 dígitos
        
        # 4. RAZÓN SOCIAL
        rs_match = re.search(r'^(.+)$', texto, re.MULTILINE)
        razon_social = re.sub(r'[^A-Z0-9 ]', '', rs_match.group(1).upper())[:25].strip() if rs_match else "PROVEEDOR"

        # 5. TOTAL
        total_match = re.findall(r'total[:\s]*\$?\s*([\d\.,]+)', texto, re.IGNORECASE)
        monto_final = total_match[-1].replace('.', '').replace(',', '.') if total_match else ""

        # Nombre del PDF: RAZON_PTO-NRO_MES.pdf
        nuevo_nombre = f"{razon_social}_{ptovta}-{nrocomp}_{nombre_mes}.pdf".replace(" ", "_")
        pdf_base64 = base64.b64encode(file_bytes).decode('utf-8')

        data = {
            "cuit": cuit, "fecha": fecha_iso, "ptovta": ptovta, 
            "nro": nrocomp, "total": monto_final, "pdf_name": nuevo_nombre, "pdf_data": pdf_base64
        }
        
        st.success(f"✅ Archivo listo: {nuevo_nombre}")
        st.code(json.dumps(data), language="json")
        st.info("Copia el código y usa tu marcador en la web de Barceló.")
        
    except Exception as e:
        st.error(f"Error: {e}")
