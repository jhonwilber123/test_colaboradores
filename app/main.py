#main.py
from fastapi import FastAPI
from app.core.logging import configure_logging
from app.api.routes import router

configure_logging()

app = FastAPI(title="Audio Evaluator", version="0.1.0")

app.include_router(router, prefix="/api") # Prefijo API para orden

@app.get("/health")
def health():
    return {"status": "ok"}