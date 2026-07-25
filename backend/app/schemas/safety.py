from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

class RedFlagResponse(BaseModel):
    id: str
    rule_code: str
    title: str
    description: str
    severity: str
    evidence: Optional[Any] = None

    class Config:
        from_attributes = True

class SafetyAssessmentResponse(BaseModel):
    id: str
    intake_session_id: str
    urgency_level: str
    decision_source: str
    rule_version: str
    recommendations_blocked: bool
    requires_professional_review: bool
    created_at: datetime
    red_flags: List[RedFlagResponse] = []

    class Config:
        from_attributes = True
