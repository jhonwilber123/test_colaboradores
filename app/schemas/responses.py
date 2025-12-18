#responses.py
from pydantic import BaseModel
from typing import List, Any, Optional

# Esquema para cada respuesta individual de la IA
class AIResponseSchema(BaseModel):
    name: str
    result: Any # Permite str, bool, etc.
    reasoning: str

# Esquema para el Prompt (opcional, útil para debug)
class PromptSchema(BaseModel):
    uid: str
    name: str
    instructions: str

# Esquema PRINCIPAL de la Evaluación
class EvaluationResponse(BaseModel):
    prompt: Optional[PromptSchema] = None
    AI_responses: List[AIResponseSchema]
    created_at: Optional[str] = None # O datetime si prefieres

# Esquema FINAL que agrupa todo (Archivo + Evaluación)
class AudioAnalysisResponse(BaseModel):
    filename: str
    transcription: str
    evaluation: EvaluationResponse