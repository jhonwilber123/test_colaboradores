#routes.py
from fastapi import APIRouter, HTTPException
from app.core.config import settings

# --- CORRECCIÓN 1: Importamos el LLMClient (ya no el evaluation_service) ---
from app.services.llm_client import LLMClient

# Importamos el servicio de transcripción (Asegúrate de tener este archivo)
from app.services.transcription import transcription_service

# Importamos Modelos de Negocio
from app.models.file import AudioFile

# Importamos Schemas
from app.schemas.requests import AudioEvaluationRequest
from app.schemas.responses import AudioAnalysisResponse, EvaluationResponse, AIResponseSchema, PromptSchema

router = APIRouter(prefix="/v1")

# --- CORRECCIÓN 2: Instanciamos el cliente aquí ---
llm_client = LLMClient(api_key=settings.OPENAI_API_KEY)

@router.post(
    "/evaluate",
    response_model=AudioAnalysisResponse,
    summary="Evaluar un audio específico",
    description="Procesa un audio de la carpeta input y retorna su evaluación detallada."
)
async def evaluate_one(request: AudioEvaluationRequest):
    """
    Recibe un JSON {"filename": "..."} y procesa ese archivo.
    """
    filename = request.filename
    file_path = settings.INPUT_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"El archivo '{filename}' no existe en la carpeta {settings.INPUT_DIR}")

    try:
        # 1. Transcribir
        text = await transcription_service.transcribe(file_path)
        
        # 2. Crear objeto AudioFile
        audio_file = AudioFile(filename=filename, transcription=text)

        # 3. Evaluar (Usando LLMClient DIRECTAMENTE)
        # Nota: generate_text recibe el OBJETO file completo, no solo el texto
        eval_result = await llm_client.generate_text(file=audio_file)

        # 4. Mapear Modelo de Dominio -> Schema Pydantic (Response)
        ai_responses_schema = [
            AIResponseSchema(
                name=r.name, 
                result=r.result, 
                reasoning=r.reasoning
            ) for r in eval_result.AI_responses
        ]
        
        prompt_schema = None
        if eval_result.prompt:
            prompt_schema = PromptSchema(
                uid=eval_result.prompt.uid,
                name=eval_result.prompt.name,
                instructions=eval_result.prompt.instructions
            )

        eval_response = EvaluationResponse(
            prompt=prompt_schema,
            AI_responses=ai_responses_schema,
            created_at=str(eval_result.created_at)
        )

        return AudioAnalysisResponse(
            filename=audio_file.filename,
            transcription=audio_file.transcription,
            evaluation=eval_response
        )

    except Exception as e:
        print(f"❌ Error procesando {filename}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/evaluate_all")
async def evaluate_all():
    return {"message": "Endpoint en construcción"}