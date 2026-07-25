from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

class IntakeSessionCreate(BaseModel):
    main_complaint: str
    input_mode: Optional[str] = "text"
    language_code: Optional[str] = "en"

class SymptomResponse(BaseModel):
    id: str
    symptom_name: str
    body_location: Optional[str] = None
    severity: Optional[int] = None
    duration_text: Optional[str] = None
    frequency: Optional[str] = None

    class Config:
        from_attributes = True

class IntakeSessionResponse(BaseModel):
    id: str
    patient_id: str
    status: str
    input_mode: str
    language_code: str
    main_complaint: str
    started_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class IntakeQuestionResponse(BaseModel):
    id: str
    question_code: str
    question_text: str
    language_code: str
    sequence_number: int
    required: bool

    class Config:
        from_attributes = True

class IntakeAnswerSubmit(BaseModel):
    answer_text: Optional[str] = None
    answer_json: Optional[Any] = None
    input_mode: Optional[str] = "text"
    confirmed_by_patient: Optional[bool] = True
