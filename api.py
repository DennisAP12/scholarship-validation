from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import shutil
import uuid

# Importamos la lógica de tu script de PaddleOCR
from analizador_becas import evaluar_archivo_beca

# Crear la aplicación FastAPI
app = FastAPI(
    title="API de Analizador de Documentos para Becas",
    description="Permite verificar escaneos (PDFs o imágenes) para comprobar si contienen todos los campos necesarios.",
    version="1.0.0"
)

# Configurar CORS (Súper importante para que un frontend en HTML/JS pueda comunicarse con la API sin bloqueos de seguridad)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permitir a cualquier frontend conectarse
    allow_credentials=True,
    allow_methods=["*"], # Permitir POST, GET, OPTIONS, etc.
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"mensaje": "La API del analizador de becas está activa y funcionando."}

@app.post("/analizar")
async def analizar_documento_api(
    tipo_documento: str = Form(description="El tipo de documento a analizar (ej. identificacion, curp, comprobante_domicilio)"),
    file: UploadFile = File(description="El archivo PDF o de imagen a subir")
):
    """
    Recibe un documento y devuelve el resultado del OCR y la validación.
    """
    # Crear un nombre único para evitar cruces si varios usuarios suben archivos al mismo tiempo
    extension = file.filename.split('.')[-1] if '.' in file.filename else 'pdf'
    temp_filename = f"temp_upload_{uuid.uuid4().hex}.{extension}"
    
    try:
        # Guardar el archivo en el disco temporalmente
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Ejecutar el analizador que construiste
        print(f"Analizando vía API: {file.filename} como {tipo_documento}")
        resultado = evaluar_archivo_beca(temp_filename, tipo_documento)
        
        # Determinar si el resultado fue exitoso basándonos en tu formato de texto
        es_valido = "✅" in resultado or "RESULTADO:" in resultado
        
        return JSONResponse(content={
            "success": True,
            "es_valido": es_valido,
            "mensaje": resultado,
            "tipo_documento": tipo_documento,
            "nombre_archivo": file.filename
        })
        
    except Exception as e:
        # En caso de que el código falle, regresar un error estructurado
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"Error interno en el servidor: {str(e)}"
            }
        )
        
    finally:
        # Eliminar el archivo del disco para no llenar tu memoria de basura
        if os.path.exists(temp_filename):
            try:
                os.remove(temp_filename)
            except:
                pass

if __name__ == "__main__":
    print("Iniciando el servidor de la API...")
    # Se utiliza uvicorn para levantar la aplicación en el puerto 8000
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
