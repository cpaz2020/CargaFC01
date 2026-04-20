import streamlit as st
import fitz  # PyMuPDF
import re
import urllib.parse

st.set_page_config(page_title="FHAB - AutoCarga", layout="centered", page_icon="🚀")

st.title("🚀 Extractor y Auto-Carga FHAB")
st.write("Sube la factura y presiona el botón para intentar el auto-completado.")

uploaded_file = st.file_uploader("Subir Factura PDF", type="pdf")

if uploaded_file is not None:
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            texto = ""
            for page in doc:
                texto += page.get_text()
        
        # --- EXTRACCIÓN DE DATOS ---
        cuit_raw = re.search(r'CUIT[:\s]*(\d{2}-?\d{8}-?\d{1})', texto)
        cuit_val = re.sub(r'\D', '', cuit_raw.group(1)) if cuit_raw else ""

        fecha_match = re.search(r'(\d{2}/\d{2}/\d{4})', texto)
        fecha_val = fecha_match.group(1) if fecha_match else ""

        comp_match = re.search(r'(\d{4,5})\s?-\s?(\d{8})', texto)
        ptovta = comp_match.group(1) if comp_match else ""
        nrocomp = comp_match.group(2) if comp_match else ""

        total_match = re.search(r'(?:Total|Importe Total):\s*\$?\s*([\d\.,]+)', texto, re.IGNORECASE)
        total_val = total_match.group(1) if total_match else ""

        # --- CONSTRUCCIÓN DE URL PARA AUTOCOMPLETE ---
        # Mapeamos los campos extraídos a posibles nombres de variables del formulario
        params = {
            "cuit": cuit_val,
            "fecha": fecha_val,
            "ptovta": ptovta,
            "nro": nrocomp,
            "importe": total_val
        }
        url_base = "https://validaciones.barcelo.edu.ar/subircomprobantes/index.php"
        url_auto = f"{url_base}?{urllib.parse.urlencode(params)}"

        st.success("✅ Datos listos")

        # --- VISTA PREVIA ---
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("CUIT", value=cuit_val)
            st.text_input("Fecha", value=fecha_val)
        with col2:
            st.text_input("Punto Venta", value=ptovta)
            st.text_input("Número", value=nrocomp)
        
        st.text_input("Total", value=total_val)

        st.divider()

        # --- BOTÓN DE AUTO-COMPLETADO ---
        st.warning("⚠️ El auto-completado depende de los permisos del sitio de destino.")
        st.link_button("🔥 AUTO-COMPLETAR Y REGISTRAR", url_auto, type="primary")
        
        st.caption("Si los campos no se llenan solos, usa la función de copiar en cada recuadro.")

    except Exception as e:
        st.error(f"Error: {e}")
