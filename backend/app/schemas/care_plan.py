from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CarePlanExerciseResponse(BaseModel):
    id: str
    exercise_id: str
    name: str
    description: str
    body_area: Optional[str] = None
    difficulty: Optional[str] = None
    duration_seconds: Optional[int] = None
    repetitions: Optional[int] = None
    video_url: Optional[str] = None
    reason: Optional[str] = None

    class Config:
        from_attributes = True

class CarePlanComplementaryResponse(BaseModel):
    id: str
    option_id: str
    name: str
    traditional_use: Optional[str] = None
    evidence_level: Optional[str] = None
    reason: Optional[str] = None

    class Config:
        from_attributes = True

class CarePlanMedicationResponse(BaseModel):
    id: str
    medication_id: str
    generic_name: str
    medicine_class: Optional[str] = None
    otc_or_prescription: str
    purpose: Optional[str] = None
    status: str
    reviewed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CarePlanResponse(BaseModel):
    id: str
    intake_session_id: str
    status: str
    professional_review_required: bool
    created_at: datetime
    updated_at: datetime
    exercises: List[CarePlanExerciseResponse] = []
    complementary_options: List[CarePlanComplementaryResponse] = []
    medications: List[CarePlanMedicationResponse] = []

    class Config:
        from_attributes = True
