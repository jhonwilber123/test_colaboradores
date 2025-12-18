#transcription.py
import logging
from pathlib import Path
from openai import AsyncOpenAI
from app.core.config import settings

logger = logging.getLogger("app")

class TranscriptionService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def transcribe(self, file_path: Path) -> str:
        """
        Transcribe usando el modelo solicitado con la estrategia automática.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"El archivo no existe: {file_path}")

        logger.info(f"🎙️ Transcribiendo audio: {file_path.name} ...")
        
        try:
            with open(file_path, "rb") as audio_file:
                transcript = await self.client.audio.transcriptions.create(
                    model="gpt-4o-transcribe-diarize",
                    file=audio_file,
                    response_format="text",
                    # CAMBIO AQUÍ: El error nos dijo que usemos "auto"
                    chunking_strategy="auto" 
                )
            
            logger.info("✅ Transcripción completada.")
            return transcript
            
        except Exception as e:
            logger.error(f"❌ Error en Transcripción: {e}")
            raise e

transcription_service = TranscriptionService()