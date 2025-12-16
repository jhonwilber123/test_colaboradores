from fastapi import APIRouter


router = APIRouter(prefix="/v1")

@router.post(
    path="/evaluate",
    summary="Evaluate one audio file",
    description="Evaluate a single audio file located in the specified directory.",
)
def evaluate_one():
    pass

@router.post(
    path="/evaluate_all",
    summary="Evaluate all audio files",
    description="Evaluate all audio files located in the specified directory.",
)
def evaluate_all():
    pass