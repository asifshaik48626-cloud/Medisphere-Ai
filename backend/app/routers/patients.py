from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.patient import PatientProfile
from ..schemas.patient import PatientProfileCreate, PatientProfileResponse
from .auth import get_current_user
from ..models.user import User

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.get("/me", response_model=PatientProfileResponse)
def get_patient_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "patient":
        raise HTTPException(status_code=403, detail="Only patients can access patient profiles")
        
    profile = db.query(PatientProfile).filter(PatientProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Patient profile not found. Please create one.")
    return profile

@router.post("/me", response_model=PatientProfileResponse)
def create_patient_profile(
    profile_in: PatientProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "patient":
        raise HTTPException(status_code=403, detail="Only patients can create patient profiles")
        
    existing_profile = db.query(PatientProfile).filter(PatientProfile.user_id == current_user.id).first()
    if existing_profile:
        raise HTTPException(status_code=400, detail="Profile already exists. Use PATCH to update.")
        
    profile = PatientProfile(
        user_id=current_user.id,
        first_name=profile_in.first_name,
        last_name=profile_in.last_name,
        date_of_birth=profile_in.date_of_birth,
        sex_at_birth=profile_in.sex_at_birth,
        gender_identity=profile_in.gender_identity,
        country_code=profile_in.country_code,
        timezone=profile_in.timezone,
        emergency_contact_name=profile_in.emergency_contact_name,
        emergency_contact_phone=profile_in.emergency_contact_phone
    )
    
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile
