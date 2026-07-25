from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any
from ..services.guideline_retrieval import GuidelineRetrieval
from .auth import get_current_user
from ..models.user import User

router = APIRouter(prefix="/guidelines", tags=["Guideline Retrieval"])

@router.get("/search")
def search_guidelines(
    query: str = Query(..., description="Symptom search query"),
    current_user: User = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    return GuidelineRetrieval.retrieve(query)
