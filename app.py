import streamlit as st
import fitz  # PyMuPDF
import re

st.set_page_config(page_title="FHAB - Extractor", layout="centered", page_icon="📄")

st.title("📄 Extractor para Formulario Barceló")
st.info("Extrae los datos exactos para el sistema de Comprobantes de Proveedor.")

uploaded_file = st.file_uploader("Subir Factura PDF", type="pdf")

if uploaded_file is not None:
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            texto = ""
            for page in doc:
                texto += page.get_text()
        
        # --- EXTRACCIÓN PERSONALIZADA PARA EL FORMULARIO ---
        
        # 1. CUIT (Extrae solo los números, sin guiones para el formulario)
        cuit_match = re.search(r'(\d{2})[-]?(\d{8})[-]?(\d{1})', texto)
        cuit_val = "".join(cuit_match.groups()) if cuit_match else "No detectado"

        # 2. Punto de Venta y Número (Formatos como 00005-00001234)
        comp_match = re.search(r'(\d{4,5})\s?-\s?(\d{8})', texto)
        ptovta = comp_match.group(1).lstrip('0') if comp_match else "" # Sin ceros a la izquierda si quieres
        nrocomp = comp_match.group(2).lstrip('0') if comp_match else ""

        # 3. Fecha (DD/MM/AAAA)
        fecha_match = re.search(r'(\d{2}/\d{2}/\d{4})', texto)
        fecha_val = fecha_match.group(1) if fecha_match else ""

        # 4. Importe Total (Busca el valor después de "Importe Total")
        total_match = re.search(r'(?:Total|Importe Total):\s*\$?\s*([\d\.,]+)', texto, re.IGNORECASE)
        total_val = total_match.group(1).replace('.', '') if total_match else "0,00" # Ajuste de formato

        st.success("✅ Datos listos para copiar")

        # --- MOSTRAR SEGÚN EL FORMULARIO ---
        st.subheader("Datos del Comprobante")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**CUIT del Proveedor** (11 dígitos)")
            st.code(cuit_val, language=None)
            
            st.write("**Fecha Comprobante**")
            st.code(fecha_val, language=None)
            
            st.write("**Punto de Venta**")
            st.code(ptovta, language=None)

        with col2:
            st.write("**Razón Social**")
            st.code("Ver en PDF", language=None) # La razón social suele ser variable, mejor verla
            
            st.write("**Importe Total ($)**")
            st.code(total_val, language=None)
            
            st.write("**Número de Comprobante**")
            st.code(nrocomp, language=None)

        st.divider()
        st.link_button("🔗 Ir al Formulario Barceló", "https://validaciones.barcelo.edu.ar/subircomprobantes/index.php")
        st.caption("Pasa el mouse sobre cada código para copiarlo al portapapeles.")

    except Exception as e:
        st.error(f"Error al procesar: {e}")
