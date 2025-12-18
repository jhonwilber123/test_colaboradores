#requests.py
from pydantic import BaseModel

class AudioEvaluationRequest(BaseModel):
    filename: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "filename": "audio_cliente_01.mp3"
            }
        }