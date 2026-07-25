from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ..services.rag_chat import GuidelinesRagChat
from .auth import get_current_user
from ..models.user import User

router = APIRouter(prefix="/guidelines", tags=["Clinical RAG Chat"])

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
def chat_guidelines(
    req: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Answers clinical queries grounded in standard guidelines.
    """
    return GuidelinesRagChat.answer_question(req.message)
