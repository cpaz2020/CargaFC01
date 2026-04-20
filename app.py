import streamlit as st
import fitz
import re
import json

st.title("🚀 FHAB - Sistema de Alta Velocidad")

uploaded_file = st.file_uploader("Subir Factura", type="pdf")

if uploaded_file is not None:
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        texto = "".join([page.get_text() for page in doc])
        
# ... (dentro de tu bloque 'if uploaded_file is not None')

# 1. Preparar el diccionario de datos
data_a_copiar = {
    "cuit": cuit_val,
    "fecha_iso": "-".join(fecha_val.split("/")[::-1]) if fecha_val else "", # Convierte DD/MM/AAAA a YYYY-MM-DD
    "ptovta": ptovta,
    "nro": nrocomp,
    "total": total_val.replace('.', '').replace(',', '.') # Formato decimal estándar
}

# 2. Mostrar el JSON para que el usuario lo copie manualmente (es lo más seguro)
st.subheader("Paso 1: Copia estos datos")
st.code(json.dumps(data_a_copiar), language="json")

st.subheader("Paso 2: Ve al formulario")
st.link_button("Ir a Barceló ↗️", "https://validaciones.barcelo.edu.ar/subircomprobantes/index.php")
    # Extracción
    cuit = "".join(re.findall(r'\d+', re.search(r'CUIT[:\s]*[\d\-]+', texto).group(0)))[:11]
    fecha = re.search(r'(\d{2})/(\d{2})/(\d{4})', texto)
    comp = re.search(r'(\d{4,5})\s?-\s?(\d{8})', texto)
    total = re.search(r'(?:Total|Importe Total):\s*\$?\s*([\d\.,]+)', texto, re.IGNORECASE)

    # Preparar JSON para el Portapapeles
    data_factura = {
        "cuit": cuit,
        "fecha_iso": f"{fecha.group(3)}-{fecha.group(2)}-{fecha.group(1)}" if fecha else "",
        "ptovta": comp.group(1) if comp else "",
        "nro": comp.group(2) if comp else "",
        "total": total.group(1).replace('.', '').replace(',', '.') if total else ""
    }

    st.success("✅ Factura procesada")
    
    # Botón mágico de copiado
    if st.button("📋 1. COPIAR DATOS PARA EL NAVEGADOR"):
        st.write(f'<script>navigator.clipboard.writeText({json.dumps(json.dumps(data_factura))})</script>', unsafe_allow_html=True)
        st.info("¡Datos copiados al portapapeles!")

    st.link_button("🚀 2. IR AL FORMULARIO Y PEGAR", "https://validaciones.barcelo.edu.ar/subircomprobantes/index.php", type="primary")
