// ==UserScript==
// @name         Auto-Carga Facturas FHAB
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Pega automáticamente los datos de la factura en el formulario de Barceló
// @author       FHAB
// @match        https://validaciones.barcelo.edu.ar/subircomprobantes/index.php*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // Función para obtener datos del "Portapapeles Inteligente"
    window.addEventListener('load', function() {
        const btn = document.createElement('button');
        btn.innerHTML = '✨ Pegar Datos de FHAB';
        btn.style = "position:fixed;top:10px;right:10px;z-index:9999;padding:10px;background:#28a745;color:white;border:none;border-radius:5px;cursor:pointer;";
        document.body.appendChild(btn);

        btn.onclick = async function() {
            try {
                const text = await navigator.clipboard.readText();
                const data = JSON.parse(text);

                // Mapeo de campos basado en la imagen que enviaste
                // Nota: Los IDs ('cuit', 'fecha', etc) pueden variar según el HTML real
                document.querySelector('input[placeholder*="11 dígitos"]').value = data.cuit;
                document.querySelector('input[type="date"]').value = data.fecha_iso; // Formato YYYY-MM-DD
                document.querySelector('input[placeholder*="Ej: 5"]').value = data.ptovta;
                document.querySelector('input[placeholder*="Ej: 12345"]').value = data.nro;
                document.querySelector('input[placeholder*="12500.50"]').value = data.total;

                alert('¡Datos cargados! Por favor revisa y adjunta el PDF.');
            } catch (err) {
                alert('Primero copia los datos desde la App de FHAB');
            }
        };
    });
})();
