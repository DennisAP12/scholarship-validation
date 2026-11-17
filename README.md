# Validador de Documentos para Becas

Aplicación web para organizar los documentos solicitados por distintos programas de becas y revisar si un archivo contiene palabras clave esperadas. Incluye una interfaz en React y una API en FastAPI que procesa PDF e imágenes con OCR en español.

> **Alcance:** la revisión detecta texto y palabras clave; no verifica la autenticidad del documento ni determina si una persona cumple los requisitos oficiales de una beca.

## Funcionalidades

- Consulta los documentos requeridos para Rita Cetina, Benito Juárez y Jóvenes Escribiendo el Futuro.
- Organiza los documentos por estudiante y tutor.
- Recibe archivos PDF e imágenes y extrae texto con PaddleOCR.
- Compara el texto extraído con palabras clave asociadas al tipo de documento.
- Muestra el resultado de la revisión y el progreso de los documentos seleccionados.
- Expone el servicio de análisis mediante una API REST con FastAPI.

## Tecnologías

- **Frontend:** React, Vite y Tailwind CSS.
- **Backend:** Python, FastAPI y Uvicorn.
- **OCR y procesamiento:** PaddleOCR, OpenCV, NumPy y PyMuPDF.

## Requisitos

- Node.js y npm.
- Python 3.10 o posterior.
- Las dependencias de OCR pueden requerir espacio adicional y descargar modelos al primer uso.

## Ejecución local

Clona el repositorio y abre una terminal en su carpeta raíz.

### 1. Instalar y ejecutar la API

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install fastapi uvicorn python-multipart
python api.py
```

La API queda disponible en `http://localhost:8000`. Puedes consultar su documentación interactiva en `http://localhost:8000/docs`.

### 2. Instalar y ejecutar el frontend

En otra terminal, desde la raíz del proyecto:

```powershell
cd front
npm install
npm run dev
```

Abre la dirección local que indique Vite en la terminal. El frontend envía las solicitudes de análisis a `http://localhost:8000`.

## Uso

1. Selecciona un programa de beca.
2. Elige el archivo PDF o imagen de uno de los documentos solicitados.
3. La API extrae el texto y busca las palabras clave configuradas para ese tipo de documento.
4. Revisa el resultado y el avance mostrado en pantalla.

## Estructura del proyecto

```text
.
├── api.py                      # API de carga y análisis de documentos
├── analizador_becas.py         # Extracción OCR y reglas por tipo de documento
├── requirements.txt            # Dependencias de Python y procesamiento OCR
└── front/
    ├── src/
    │   ├── components/         # Componentes de la interfaz
    │   ├── data/               # Programas y listas de documentos
    │   └── pages/              # Vistas de la aplicación
    └── package.json
```

## Privacidad y uso responsable

- No subas documentos personales reales al repositorio ni uses información sensible para demostraciones.
- La API guarda temporalmente el archivo durante el análisis y después intenta eliminarlo. El analizador también imprime en la terminal el texto extraído, que puede contener datos personales.
- Antes de desplegar esta aplicación o usarla con documentos reales, revisa el tratamiento de datos, elimina el registro de texto sensible y añade controles adecuados de seguridad y privacidad.

## Estado

Proyecto de portafolio en desarrollo. La interfaz se conecta a una API local; no incluye despliegue público ni integración con sistemas oficiales de becas.
