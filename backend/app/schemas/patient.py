from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class PatientProfileCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    sex_at_birth: Optional[str] = None
    gender_identity: Optional[str] = None
    country_code: Optional[str] = "IN"
    timezone: Optional[str] = "Asia/Kolkata"
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None

class PatientProfileResponse(PatientProfileCreate):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
