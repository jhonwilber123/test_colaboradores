# 🎙️ Audio Evaluator API - Solución Prueba Técnica

Este proyecto implementa una API RESTful desarrollada en **FastAPI** para la evaluación automatizada de audios de cobranza, integrando la suite de modelos de **OpenAI** para transcripción y análisis lógico.

## 🧠 Arquitectura y Decisiones Técnicas

El proyecto sigue una arquitectura en capas (Clean Architecture simplificada) para garantizar la separación de responsabilidades, escalabilidad y facilidad de mantenimiento:

- **Modelos de IA:**
  - **Transcripción (ASR):** Se implementó el modelo `gpt-4o-audio-preview` (o compatible con transcripción/diarización) utilizando la estrategia `chunking_strategy="auto"`. Esto permite una diarización precisa (identificación de hablantes) y soporte robusto para audios de diversa duración.
  - **Evaluación (LLM):** Se utiliza `gpt-4o-mini` para procesar la transcripción, extraer entidades y generar un análisis estructurado en JSON según las reglas de negocio (compromiso de pago, montos, fechas).
- **Seguridad:** Gestión estricta de credenciales mediante variables de entorno (`.env`), evitando la exposición de API Keys en el código fuente.
- **Validación de Datos:** Uso de **Pydantic** para garantizar que tanto las entradas como las salidas de la API cumplan con los esquemas esperados.
- **Dockerización:** Configuración completa con `Dockerfile` y `docker-compose` para un despliegue agnóstico del entorno.
- **Procesamiento Batch:** Endpoint `/evaluate_all` capaz de iterar y procesar dinámicamente todos los archivos de audio presentes en un directorio.

## 🚀 Requisitos Previos

- **Python 3.10** o superior.
- Una **API Key de OpenAI** activa con permisos habilitados para modelos de Audio.
- **Git** instalado.
- (Opcional) **Docker Desktop** si se desea ejecutar en contenedor.

## 🛠️ Guía de Instalación (Local)

Sigue estos pasos para desplegar el proyecto manualmente en tu máquina:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/jhonwilber123/test_colaboradores.git
   cd test_colaboradores
   ```

2. **Crear y activar el entorno virtual:**
   ```bash
   python -m venv venv

   # En Windows:
   venv\Scripts\activate

   # En Mac/Linux:
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuración de Variables de Env:**
   Crea un archivo llamado `.env` en la raíz del proyecto y define tu clave de API:
   ```env
   OPENAI_API_KEY=sk-tu-clave-aqui...
   ```

## 🏃‍♂️ Ejecución

### Opción A: Ejecución Local con Python
1. **Preparar los Audios:**
   Crea una carpeta llamada `audios/` en la raíz del proyecto y coloca tus archivos de prueba (`.mp3`, `.wav`).
2. **Iniciar el Servidor:**
   ```bash
   uvicorn app.main:app --reload
   ```

### Opción B: Ejecución con Docker (Recomendado)
Si prefieres un entorno aislado:
1. Asegúrate de tener las credenciales en el archivo `.env` y los audios en la carpeta `audios/`.
2. Ejecuta:
   ```bash
   docker-compose up --build
   ```

## 🧪 Uso de la API

Una vez iniciado el servidor, abre tu navegador en la documentación interactiva:
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Endpoints Principales:
- **POST `/api/v1/evaluate_all`**: (Recomendado) Escanea la carpeta `audios/`, transcribe y evalúa cada archivo secuencialmente, devolviendo un reporte JSON completo.
- **POST `/api/v1/evaluate`**: Evalúa un archivo individual indicando su nombre exacto (ej: `audio1.mp3`) en el cuerpo de la petición.

---
**Autor:** Jhon Ajata  
**Estado:** Finalizado para revisión técnica.