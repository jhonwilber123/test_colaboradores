#transcription.py
import logging
from pathlib import Path
from openai import AsyncOpenAI
from app.core.config import settings

logger = logging.getLogger("app")

class TranscriptionService:
    def __init__(self):
        # Usamos la misma Key que configuramos en settings
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def transcribe(self, file_path: Path) -> str:
        """
        Envía el audio a Whisper-1 y devuelve el texto.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"El archivo no existe: {file_path}")

        logger.info(f"🎙️ Transcribiendo audio: {file_path.name} ...")
        
        try:
            with open(file_path, "rb") as audio_file:
                # Llamada a la API de Whisper
                transcript = await self.client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file,
                    response_format="text" # Pedimos texto plano directo
                )
            
            logger.info("✅ Transcripción completada.")
            return transcript
            
        except Exception as e:
            logger.error(f"❌ Error en Whisper: {e}")
            raise e

# Instanciamos el servicio para importarlo en routes.py
transcription_service = TranscriptionService()