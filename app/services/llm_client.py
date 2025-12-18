#llm_client.py
import json
import uuid
import logging
from typing import Optional
from pydantic import BaseModel
from openai import AsyncOpenAI
from app.core.config import settings

# Importamos TUS modelos originales (INTACTOS)
from app.models.evaluation import Evaluation, AIResponse
from app.models.prompt import Prompt
from app.models.file import File

logger = logging.getLogger("app")

# --- Validadores Internos (Pydantic) ---
# Los definimos aquí para no crear más archivos y mantenerlo simple
class LLMAttributeData(BaseModel):
    status: str
    reasoning: str

class LLMEvaluationOutput(BaseModel):
    payment_commitment: LLMAttributeData
    debt_amount: LLMAttributeData
    payment_methods: LLMAttributeData
    payment_alternatives: LLMAttributeData
    non_payment_reason: Optional[str] = None

# --- La Clase Principal ---
class LLMClient:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.reasons_list = self._load_reasons()

    def _load_reasons(self) -> str:
        """Carga los motivos del JSON para inyectar contexto"""
        try:
            path = settings.BASE_DIR / "app" / "data" / "motivos.json"
            if not path.exists():
                return "Lista no disponible."
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return "\n".join([f"- {item['category']}: {item['situation']}" for item in data])
        except Exception:
            return "Lista no disponible."

    async def generate_text(self, file: File) -> Evaluation:
        """
        Implementación REAL del método. Recibe File -> Devuelve Evaluation.
        """
        logger.info(f"🤖 LLMClient: Evaluando {file.filename}...")

        # 1. Crear Prompt
        system_instructions = f"""
        Eres un QA de cobranzas. Analiza la transcripción.
        
        REGLAS:
        1. Compromiso: "Cumple" (fecha/plazo) vs "No Cumple".
        2. Monto: "Cumple" (monto exacto) vs "No Cumple".
        3. Medios: "Cumple" (lugares) vs "No Cumple".
        4. Alternativas: "Cumple" (opciones) vs "No Cumple".
        5. Motivo No Pago: Elige de: {self.reasons_list} o null.

        OUTPUT JSON:
        {{
            "payment_commitment": {{ "status": "Cumple/No Cumple", "reasoning": "..." }},
            "debt_amount": {{ "status": "Cumple/No Cumple", "reasoning": "..." }},
            "payment_methods": {{ "status": "Cumple/No Cumple", "reasoning": "..." }},
            "payment_alternatives": {{ "status": "Cumple/No Cumple", "reasoning": "..." }},
            "non_payment_reason": "Motivo o null"
        }}
        """

        try:
            # 2. Llamar a OpenAI
            response = await self.client.chat.completions.create(
                model=settings.MODEL_EVALUATION,
                messages=[
                    {"role": "system", "content": system_instructions},
                    {"role": "user", "content": file.transcription}
                ],
                temperature=0,
                response_format={"type": "json_object"}
            )
            
            # 3. Validar JSON
            content = response.choices[0].message.content
            validated = LLMEvaluationOutput(**json.loads(content))

            # 4. Convertir a AIResponse (Tu modelo original)
            responses_list = [
                AIResponse("Realiza compromiso de pago", validated.payment_commitment.status, validated.payment_commitment.reasoning),
                AIResponse("Expresa datos base (monto)", validated.debt_amount.status, validated.debt_amount.reasoning),
                AIResponse("Informa medios de pago", validated.payment_methods.status, validated.payment_methods.reasoning),
                AIResponse("Alternativas de pago", validated.payment_alternatives.status, validated.payment_alternatives.reasoning)
            ]

            if validated.non_payment_reason:
                responses_list.append(AIResponse("Motivo de No Pago", validated.non_payment_reason, "RAG Contextual"))

            # 5. Retornar Evaluation (Tu modelo original)
            return Evaluation(
                prompt=Prompt(
                    uid=str(uuid.uuid4()),
                    name="System Prompt v1",
                    instructions=system_instructions
                ),
                AI_responses=responses_list
            )

        except Exception as e:
            logger.error(f"❌ Error LLM: {e}")
            return Evaluation(
                prompt=Prompt(uid="err", name="Error", instructions="Fallo"), 
                AI_responses=[]
            )