#config.py
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    
    # Modelos
    MODEL_EVALUATION: str = "gpt-4o-mini"
    
    # Rutas
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    
    # --- CAMBIO AQUÍ: Apuntamos a tu carpeta "audios" ---
    INPUT_DIR: Path = BASE_DIR / "audios" 

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()