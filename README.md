# 🎙️ Audio Evaluator API - Solución Prueba Técnica

Este proyecto implementa una API RESTful desarrollada en **FastAPI** para la evaluación automatizada de audios de cobranza, integrando la suite de modelos de **OpenAI** para transcripción y análisis lógico.

## 🧠 Arquitectura y Decisiones Técnicas

El proyecto sigue una arquitectura en capas (Clean Architecture simplificada) para garantizar la separación de responsabilidades, escalabilidad y facilidad de mantenimiento:

- **Modelos de IA:**
  - **Transcripción (ASR):** Se implementó el modelo utilizando la estrategia `gpt-4o-audio-preview` o equivalente (según la suite de OpenAI para transcripción y diarización), permitiendo una identificación de hablantes precisa y soporte robusto para audios de diversa duración.
  - **Evaluación (LLM):** Se utiliza `gpt-4o-mini` para procesar la transcripción, extraer entidades y generar un análisis estructurado en JSON según las reglas de negocio (compromiso de pago, montos, fechas).
- **Seguridad:** Gestión estricta de credenciales mediante variables de entorno (`.env`), evitando la exposición de API Keys en el código fuente.
- **Validación de Datos:** Uso de **Pydantic** para garantizar que tanto las entradas como las salidas de la API cumplan con los esquemas esperados.
- **Procesamiento Batch:** Se desarrolló el endpoint `/evaluate_all` capaz de iterar y procesar dinámicamente todos los archivos de audio presentes en un directorio, facilitando pruebas masivas.

## 🚀 Requisitos Previos

- **Python 3.10** o superior.
- Una **API Key de OpenAI** activa con permisos habilitados para modelos de Audio (Model Capabilities).
- Git instalado.

## 🛠️ Guía de Instalación

Sigue estos pasos para desplegar el proyecto localmente:

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

4. **Configuración de Variables de Entorno:**
   Crea un archivo llamado `.env` en la raíz del proyecto y define tu clave de API:
   ```ini
   OPENAI_API_KEY=sk-tu-clave-aqui...
   ```

## 🏃‍♂️ Ejecución y Pruebas

1. **Preparar los Audios:**
   Crea una carpeta llamada `audios` en la raíz del proyecto (al mismo nivel que `app/` y `main.py`). Coloca dentro tus archivos de prueba (`.mp3`, `.wav`, `.m4a`). 
   *Nota: La carpeta de audios no se incluye en el repositorio por buenas prácticas.*

2. **Iniciar el Servidor:**
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Consumir la API:**
   Abre tu navegador y ve a la documentación interactiva (Swagger UI): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Endpoints Disponibles:

- **POST `/api/v1/evaluate_all`**: (Recomendado) Procesa automáticamente todos los audios de la carpeta `audios/` y devuelve un JSON con los resultados.
- **POST `/api/v1/evaluate`**: Permite evaluar un archivo específico indicando su nombre en el cuerpo de la petición.

---
**Autor:** Jhon Ajata  
**Estado:** Finalizado para revisión técnica.