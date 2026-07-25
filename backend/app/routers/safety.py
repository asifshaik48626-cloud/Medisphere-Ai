from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.intake import IntakeSession, Symptom
from ..models.patient import PatientProfile
from ..models.safety import SafetyAssessment, RedFlagEvent
from ..schemas.safety import SafetyAssessmentResponse
from ..services.safety_engine import SafetyEngine
from .auth import get_current_user
from ..models.user import User
from datetime import datetime, date

router = APIRouter(prefix="/safety", tags=["Safety Engine"])

@router.post("/evaluate/{intake_id}", response_model=SafetyAssessmentResponse)
def evaluate_intake_safety(
    intake_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Fetch intake session
    session = db.query(IntakeSession).filter(IntakeSession.id == intake_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Intake session not found")
        
    # Get patient profile details
    patient = db.query(PatientProfile).filter(PatientProfile.id == session.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")

    # Calculate age
    today = date.today()
    birth_date = patient.date_of_birth
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    # Fetch patient symptoms for this session
    db_symptoms = db.query(Symptom).filter(Symptom.intake_session_id == intake_id).all()
    symptoms_list = []
    for s in db_symptoms:
        symptoms_list.append({
            "symptom_name": s.symptom_name,
            "severity": s.severity or 5,
            "duration_days": 1,  # fallback/parsed duration
            "associated_symptoms": []
        })

    # Prepare safety evaluation input
    patient_info = {
        "age": age,
        "pregnancy_status": False,  # Mocked / can be fetched from patient conditions
        "allergies": [],
        "existing_conditions": []
    }

    # Run Safety Engine
    evaluation = SafetyEngine.evaluate(patient_info, symptoms_list)

    # Save to database
    # Deleting old safety assessments for this session if any
    old_assessments = db.query(SafetyAssessment).filter(SafetyAssessment.intake_session_id == intake_id).all()
    for oa in old_assessments:
        db.query(RedFlagEvent).filter(RedFlagEvent.safety_assessment_id == oa.id).delete()
        db.delete(oa)
    db.commit()

    assessment = SafetyAssessment(
        intake_session_id=intake_id,
        urgency_level=evaluation["urgency_level"],
        decision_source=evaluation["decision_source"],
        rule_version=evaluation["rule_version"],
        recommendations_blocked=evaluation["recommendations_blocked"],
        requires_professional_review=evaluation["requires_professional_review"]
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    # Save red flags
    for rf in evaluation["red_flags"]:
        red_flag_event = RedFlagEvent(
            safety_assessment_id=assessment.id,
            rule_code=rf["rule_code"],
            title=rf["title"],
            description=rf["description"],
            severity=rf["severity"],
            evidence=rf["evidence"]
        )
        db.add(red_flag_event)
    db.commit()
    db.refresh(assessment)

    return assessment
