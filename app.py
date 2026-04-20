import streamlit as st
import fitz
import re
import json

st.set_page_config(page_title="FHAB - Extractor", layout="centered")

st.title("🚀 Extractor FHAB")

uploaded_file = st.file_uploader("Subir Factura PDF", type="pdf")

if uploaded_file is not None:
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            texto = "".join([page.get_text() for page in doc])

        # Extracción limpia
        cuit = "".join(re.findall(r'\d+', re.search(r'CUIT[:\s]*[\d\-]+', texto).group(0)))[:11]
        f = re.search(r'(\d{2})/(\d{2})/(\d{4})', texto)
        fecha = f"{f.group(3)}-{f.group(2)}-{f.group(1)}" if f else ""
        comp = re.search(r'(\d{4,5})\s?-\s?(\d{8})', texto)
        total = re.search(r'(?:Total|Importe Total):\s*\$?\s*([\d\.,]+)', texto, re.IGNORECASE)
        monto = total.group(1).replace('.', '').replace(',', '.') if total else ""

        data = {"cuit": cuit, "fecha": fecha, "ptovta": comp.group(1) if comp else "", "nro": comp.group(2) if comp else "", "total": monto}
        
        st.success("✅ Factura procesada")
        st.subheader("Copia este código:")
        st.code(json.dumps(data), language="json")
        st.link_button("Ir al Formulario", "https://validaciones.barcelo.edu.ar/subircomprobantes/index.php")

    except Exception as e:
        st.error(f"Error: {e}")
