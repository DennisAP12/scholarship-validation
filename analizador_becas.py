import os
import cv2
import numpy as np

try:
    from paddleocr import PaddleOCR
except ImportError:
    print("Error: PaddleOCR no está instalado.")
    print("Por favor, instala las dependencias ejecutando:")
    print("pip install paddlepaddle paddleocr")
    exit(1)

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF (fitz) no está instalado.")
    print("Por favor, instala la dependencia para leer PDFs ejecutando:")
    print("pip install PyMuPDF")
    exit(1)

# Inicializar PaddleOCR
print("Inicializando modelo OCR (esto puede tardar unos segundos la primera vez)...")
ocr = PaddleOCR(use_angle_cls=True, lang='es', show_log=False)

def extraer_texto(ruta_archivo):
    """
    Extrae el texto de un PDF o una imagen utilizando PaddleOCR.
    Si es un PDF, convierte cada página en imagen y extrae el texto.
    """
    if not os.path.exists(ruta_archivo):
        return None, f"Error: El archivo '{ruta_archivo}' no existe."
    
    extension = ruta_archivo.lower().split('.')[-1]
    texto_extraido = []
    
    print(f"Procesando archivo: {ruta_archivo}...")
    
    if extension == 'pdf':
        try:
            # Abrir el PDF usando PyMuPDF
            doc = fitz.open(ruta_archivo)
            for num_pagina in range(len(doc)):
                print(f"  Analizando página {num_pagina + 1} de {len(doc)}...")
                pagina = doc.load_page(num_pagina)
                
                # Renderizar página a imagen (pixmap) a buena resolución (zoom 2x para mejor OCR)
                mat = fitz.Matrix(2, 2)
                pix = pagina.get_pixmap(matrix=mat)
                
                # Convertir a arreglo numpy compatible con OpenCV/PaddleOCR
                img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
                
                # Ajustar canales de color para OpenCV (BGR)
                if pix.n == 4: # RGBA
                    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
                elif pix.n == 3: # RGB
                    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
                elif pix.n == 1: # Escala de grises
                    img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR)

                # Extraer texto de la imagen generada
                resultado = ocr.ocr(img_array, cls=True)
                
                if resultado and len(resultado) > 0 and resultado[0] is not None:
                    for linea in resultado[0]:
                        texto = linea[1][0]
                        texto_extraido.append(texto)
                        
        except Exception as e:
            return None, f"Error al leer el PDF: {e}"
            
    elif extension in ['jpg', 'jpeg', 'png', 'bmp', 'tiff']:
        # Es una imagen directa
        resultado = ocr.ocr(ruta_archivo, cls=True)
        if resultado and len(resultado) > 0 and resultado[0] is not None:
            for linea in resultado[0]:
                texto = linea[1][0]
                texto_extraido.append(texto)
    else:
        return None, f"Error: Formato de archivo '{extension}' no soportado. Usa PDF o imágenes (JPG/PNG)."
                
    return " ".join(texto_extraido), "Éxito"

def analizar_documento(texto, tipo_documento):
    """
    Analiza el texto extraído para verificar si contiene los campos clave esperados
    según el tipo de documento común para becas en México.
    """
    if not texto.strip():
        return "⚠️ ADVERTENCIA: No se pudo extraer ningún texto del documento. Verifica que no sea un documento en blanco o una imagen ilegible."
        
    texto_minusculas = texto.lower()
    campos_faltantes = []
    
    # Definir reglas y palabras clave que deberían estar presentes en los documentos
    if tipo_documento == 'identificacion':
        # INE o Pasaporte
        palabras_clave = ['idmex','seccion','vigencia','instituto', 'nacional', 'electoral', 'nombre', 'clave', 'elector', 'curp','registro','fecha','nacimiento','sexo']
    elif tipo_documento == 'comprobante_domicilio':
        # Recibo de luz, agua, teléfono
        palabras_clave = ['concepto', 'cfe', 'col', 'total','periodo','medidor','federal','electricidad']
    elif tipo_documento == 'constancia_estudios':
        # Constancia con calificaciones o inscripción
        palabras_clave = ['constancia', 'oficio', 'semestre', 'clave', 'atentamente','periodo','dependencia','materia','calificacion']
    elif tipo_documento == 'solicitud_beca':
        # Formato de solicitud (generalmente tienen firmas y fechas)
        palabras_clave = ['solicitud', 'firma', 'fecha', 'nombre']
    elif tipo_documento == 'curp':
        # Curp
        palabras_clave = ['clave','registro','curp','nombre','estados','unidos','mexicanos','segob']
    elif tipo_documento == 'acta':
        # Acta
        palabras_clave = ['acta','nacimiento','registro','unidos','mexicanos','estados','nombre','persona','datos','registrada']
    
    else:
        return "Tipo de documento no reconocido. Opciones: identificacion, comprobante_domicilio, constancia_estudios, solicitud_beca."

    # Verificar qué palabras clave faltan
    for palabra in palabras_clave:
        if palabra not in texto_minusculas:
            campos_faltantes.append(palabra)

    # Generar retroalimentación para el usuario
    if not campos_faltantes:
        return "✅ RESULTADO: El documento parece estar bien llenado y contiene la información principal requerida."
    else:
        feedback = "⚠️ ADVERTENCIA: Parece que el documento está incompleto o falta información clave. Revisa los siguientes puntos:\n"
        for campo in campos_faltantes:
            feedback += f"  - Falta o no se detecta claramente: '{campo.upper()}'\n"
        feedback += "\n💡 SUGERENCIA: Si es un PDF de varias páginas, asegúrate de que el documento esté completo, bien escaneado y que no se hayan recortado los bordes."
        return feedback

def evaluar_archivo_beca(ruta_archivo, tipo_documento):
    """
    Flujo principal: extrae texto y analiza el documento dando recomendaciones.
    """
    texto, mensaje = extraer_texto(ruta_archivo)
    
    if texto is None:
        return mensaje
        
    print("\n--- Texto Detectado ---")
    #texto_mostrar = texto[:500] + "..." if len(texto) > 500 else texto
    #print(texto_mostrar)
    print(texto)
    print("-----------------------\n")
    
    resultado_analisis = analizar_documento(texto, tipo_documento)
    return resultado_analisis

if __name__ == "__main__":
    print("=== Analizador de Documentos para Becas en México (Soporta PDF e Imágenes) ===\n")
    
    # --- CONFIGURACIÓN DE PRUEBA ---
    # Puedes usar un archivo .pdf o .jpg/.png
    archivo_prueba = "ACTA.pdf" 

    
    # Opciones válidas: identificacion, comprobante_domicilio, constancia_estudios, solicitud_beca
    tipo_documento_prueba = "acta" 
    
    if not os.path.exists(archivo_prueba):
        print(f"ℹ️  Para usar este script, coloca un PDF o imagen de tu documento con el nombre '{archivo_prueba}' en esta carpeta.")
        print(f"   También puedes modificar la variable 'archivo_prueba' en el código para apuntar a tu archivo real.")
    else:
        resultado = evaluar_archivo_beca(archivo_prueba, tipo_documento_prueba)
        print(resultado)
