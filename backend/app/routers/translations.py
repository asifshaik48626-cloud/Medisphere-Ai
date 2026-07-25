from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from ..services.translator import MedicalTranslator
from .auth import get_current_user
from ..models.user import User

router = APIRouter(prefix="/translations", tags=["Multilingual Translation"])

class TranslationRequest(BaseModel):
    text: str
    target_lang: str

class DetectionRequest(BaseModel):
    text: str

@router.post("/translate")
def translate_text(
    req: TranslationRequest,
    current_user: User = Depends(get_current_user)
):
    translated = MedicalTranslator.translate(req.text, req.target_lang)
    return {
        "original_text": req.text,
        "translated_text": translated,
        "language": req.target_lang
    }

@router.post("/detect")
def detect_language(
    req: DetectionRequest,
    current_user: User = Depends(get_current_user)
):
    lang = MedicalTranslator.identify_language(req.text)
    return {
        "text": req.text,
        "detected_language": lang
    }
