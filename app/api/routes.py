#routes.py
from typing import List
from fastapi import APIRouter, HTTPException
from app.core.config import settings

# Servicios
from app.services.llm_client import LLMClient
from app.services.transcription import transcription_service

# Modelos
from app.models.file import AudioFile

# Schemas
from app.schemas.requests import AudioEvaluationRequest
from app.schemas.responses import AudioAnalysisResponse, EvaluationResponse, AIResponseSchema, PromptSchema

router = APIRouter(prefix="/v1")

# Instanciamos el cliente
llm_client = LLMClient(api_key=settings.OPENAI_API_KEY)

# --- FUNCIÓN AYUDA (Para no repetir código) ---
def map_evaluation_to_schema(audio_file, eval_result) -> AudioAnalysisResponse:
    """Convierte el resultado crudo en el JSON bonito de respuesta"""
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


@router.post(
    "/evaluate",
    response_model=AudioAnalysisResponse,
    summary="Evaluar UN solo audio",
    description="Procesa un archivo específico por su nombre."
)
async def evaluate_one(request: AudioEvaluationRequest):
    filename = request.filename
    file_path = settings.INPUT_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"El archivo '{filename}' no existe.")

    try:
        # 1. Transcribir
        text = await transcription_service.transcribe(file_path)
        audio_file = AudioFile(filename=filename, transcription=text)

        # 2. Evaluar
        eval_result = await llm_client.generate_text(file=audio_file)

        # 3. Mapear y Retornar
        return map_evaluation_to_schema(audio_file, eval_result)

    except Exception as e:
        print(f"❌ Error en {filename}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/evaluate_all",
    response_model=List[AudioAnalysisResponse],
    summary="Evaluar TODOS los audios",
    description="Busca todos los mp3/wav en la carpeta input y los evalúa en lote."
)
async def evaluate_all():
    results = []
    
    # Buscamos archivos de audio en la carpeta
    files = [
        f for f in settings.INPUT_DIR.glob("*") 
        if f.suffix.lower() in ['.mp3', '.wav', '.m4a']
    ]

    print(f"📂 Encontrados {len(files)} audios para procesar.")

    for file_path in files:
        try:
            print(f"🔄 Procesando: {file_path.name}...")
            
            # 1. Transcribir
            text = await transcription_service.transcribe(file_path)
            audio_file = AudioFile(filename=file_path.name, transcription=text)

            # 2. Evaluar
            eval_result = await llm_client.generate_text(file=audio_file)

            # 3. Agregar a la lista de resultados
            response_obj = map_evaluation_to_schema(audio_file, eval_result)
            results.append(response_obj)
            
        except Exception as e:
            print(f"⚠️ Error saltando archivo {file_path.name}: {e}")
            # No detenemos el loop, solo logueamos el error y seguimos con el siguiente
            continue

    return results