import streamlit as st
import fitz  # PyMuPDF
import re

st.set_page_config(page_title="FHAB - Extractor Pro", layout="centered", page_icon="📄")

# Estilo para que se vea más limpio
st.markdown("<style>code { color: #1e88e5; font-size: 1.2em !important; }</style>", unsafe_allow_html=True)

st.title("📄 Extractor FHAB")
st.write("Extrae datos para el formulario de **Subir Comprobante de Proveedor**.")

uploaded_file = st.file_uploader("Subir Factura PDF", type="pdf")

if uploaded_file is not None:
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            texto = ""
            for page in doc:
                texto += page.get_text()
        
        # --- LÓGICA DE EXTRACCIÓN MEJORADA ---
        
        # 1. CUIT: Extrae solo los 11 dígitos
        cuit_raw = re.search(r'CUIT[:\s]*(\d{2}-?\d{8}-?\d{1})', texto)
        cuit_val = re.sub(r'\D', '', cuit_raw.group(1)) if cuit_raw else "No encontrado"

        # 2. Razón Social (Suele ser la primera línea del PDF)
        lineas = [l.strip() for l in texto.split('\n') if l.strip()]
        razon_social = lineas[0] if lineas else "Revisar en PDF"

        # 3. Tipo de Comprobante (Busca Factura A, B, C, Nota de Crédito, etc.)
        tipo_match = re.search(r'(FACTURA|NOTA DE CRÉDITO|NOTA DE DÉBITO)\s*([A-C])', texto, re.IGNORECASE)
        tipo_val = f"{tipo_match.group(1)} {tipo_match.group(2)}" if tipo_match else "No detectado"

        # 4. Fecha del Comprobante (DD/MM/AAAA)
        fecha_match = re.search(r'(\d{2}/\d{2}/\d{4})', texto)
        fecha_val = fecha_match.group(1) if fecha_match else ""

        # 5. Punto de Venta y Número
        # Busca formato 0000X - 0000000X
        comp_match = re.search(r'(\d{4,5})\s?-\s?(\d{8})', texto)
        ptovta = comp_match.group(1) if comp_match else ""
        nrocomp = comp_match.group(2) if comp_match else ""

        # 6. Importe Total
        total_match = re.search(r'(?:Total|Importe Total):\s*\$?\s*([\d\.,]+)', texto, re.IGNORECASE)
        total_val = total_match.group(1) if total_match else "0,00"

        st.success("✅ Extracción completada")

        # --- MOSTRAR DATOS SEGÚN EL FORMULARIO ---
        st.subheader("📋 Datos Extraídos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**CUIT del Proveedor**")
            st.code(cuit_val, language=None)
            
            st.write("**Fecha Comprobante**")
            st.code(fecha_val, language=None)
            
            st.write("**Punto de Venta**")
            st.code(ptovta, language=None)

        with col2:
            st.write("**Razón Social**")
            st.code(razon_social, language=None)
            
            st.write("**Tipo de Comprobante**")
            st.code(tipo_val, language=None)
            
            st.write("**Número de Comprobante**")
            st.code(nrocomp, language=None)

        st.write("**Importe Total ($)**")
        st.code(total_val, language=None)

        st.divider()
        
        # Botones de Acción
        c1, c2 = st.columns(2)
        with c1:
            st.link_button("🔍 Verificar en AFIP", "https://seti.afip.gob.ar/padron-puc-constancia-internet/ConsultaConstanciaAction.do")
        with c2:
            st.link_button("🚀 Registrar en Barceló", "https://validaciones.barcelo.edu.ar/subircomprobantes/index.php")

    except Exception as e:
        st.error(f"Hubo un error al leer el PDF: {e}")
