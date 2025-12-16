from fastapi import FastAPI
from app.core.logging import configure_logging

configure_logging()

app = FastAPI(title="Audio Evaluator", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok"}