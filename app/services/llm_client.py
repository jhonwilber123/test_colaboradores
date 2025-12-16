
from app.models.evaluation import Evaluation
from app.models.file import File


class LLMClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate_text(self, file: File) -> Evaluation:
        """Generate text based on the provided file using the LLM API."""
        pass