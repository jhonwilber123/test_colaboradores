#evaluation.py
import datetime

from app.models.prompt import Prompt


class AIResponse:

    def __init__(
        self,
        name: str,
        result: str | bool | list | dict | None,
        reasoning: str

    ) -> None:
        self.name = name
        self.result = result
        self.reasoning = reasoning
    
    def __dict__(self):
        return {
            "name": self.name,
            "result": self.result,
            "reasoning": self.reasoning,
        }

class Evaluation:

    def __init__(
        self,
        prompt: Prompt,
        AI_responses: list[AIResponse],
        
    ) -> None:
        self.prompt = prompt
        self.AI_responses = AI_responses
        self.created_at: str = str(datetime.now())