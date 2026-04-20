import streamlit as st
import fitz  # PyMuPDF
import re

st.set_page_config(page_title="FHAB - Extractor Pro", layout="centered", page_icon="📄")

st.title("📄 Extractor FHAB + Validación")

uploaded_file = st.file_uploader("Subir Factura PDF", type="pdf")

if uploaded_file is not None:
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            texto = ""
            for page in doc:
                texto += page.get_text()
        
        # --- EXTRACCIÓN MEJORADA ---
        
        # 1. CUIT: Extrae cualquier grupo de números y limpia para dejar solo 11 dígitos
        cuit_raw = re.findall(r'\d+', re.search(r'CUIT[:\s]*[\d\-]+', texto).group(0)) if re.search(r'CUIT[:\s]*[\d\-]+', texto) else []
        cuit_val = "".join(cuit_raw)
        if len(cuit_val) > 11: cuit_val = cuit_val[:11] # Ajuste por si toma números de más

        # 2. Razón Social (Intenta buscar el primer bloque de texto grande o nombre del emisor)
        # Nota: En facturas ARCA suele estar al principio. 
        lineas = texto.split('\n')
        razon_social = lineas[0].strip() if len(lineas) > 0 else "No detectada"

        # 3. Punto de Venta y Número
        comp_match = re.search(r'(\d{4,5})\s?-\s?(\d{8})', texto)
        ptovta = comp_match.group(1) if comp_match else ""
        nrocomp = comp_match.group(2) if comp_match else ""

        # 4. Importe Total
        total_match = re.search(r'(?:Total|Importe Total):\s*\$?\s*([\d\.,]+)', texto, re.IGNORECASE)
        total_val = total_match.group(1) if total_match else "0,00"

        st.success("✅ Datos procesados")

        # --- MOSTRAR DATOS ---
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**CUIT del Proveedor**")
            st.code(cuit_val, language=None)
            
            st.write("**Razón Social (en Factura)**")
            st.code(razon_social, language=None)

        with col2:
            st.write("**Punto de Venta**")
            st.code(ptovta, language=None)
            
            st.write("**Número Comprobante**")
            st.code(nrocomp, language=None)

        st.write("**Importe Total**")
        st.code(total_val, language=None)

        st.divider()
        
        # --- VALIDACIÓN AFIP ---
        st.subheader("🔍 Validación Externa")
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            # Link a la constancia de CUIT de AFIP
            url_afip = f"https://seti.afip.gob.ar/padron-puc-constancia-internet/ConsultaConstanciaAction.do"
            st.link_button("Verificar CUIT en AFIP", url_afip)
            st.caption("Deberás ingresar el CUIT manualmente por seguridad de AFIP.")

        with col_btn2:
            st.link_button("🚀 Ir al Formulario Barceló", "https://validaciones.barcelo.edu.ar/subircomprobantes/index.php")

    except Exception as e:
        st.error(f"Error: {e}")
