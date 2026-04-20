import fitz  # PyMuPDF
import re

def extraer_datos_factura(pdf_path):
    doc = fitz.open(pdf_path)
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()

    # Buscamos el CUIT (Patrón: 11 dígitos)
    cuit = re.search(r'\b\d{11}\b', texto)
    
    # Buscamos el CAE (Patrón: "CAE N°: " seguido de 14 dígitos)
    cae = re.search(r'CAE\s*(?:N°)?:\s*(\d{14})', texto)

    # Buscamos el Total (Buscamos después de la palabra "Total")
    total = re.search(r'Total:\s*\$?\s*([\d\.,]+)', texto)

    return {
        "cuit": cuit.group(0) if cuit else "No encontrado",
        "cae": cae.group(1) if cae else "No encontrado",
        "total": total.group(1) if total else "0.00"
    }
