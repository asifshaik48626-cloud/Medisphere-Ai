from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.care_plan import CarePlan, CarePlanExercise, CarePlanComplementaryOption, CarePlanMedicationInformation
from ..models.safety import SafetyAssessment
from ..models.content_library import ExerciseLibrary, ComplementaryOption
from ..models.medication import MedicationCatalog
from ..schemas.care_plan import CarePlanResponse, CarePlanExerciseResponse, CarePlanMedicationResponse, CarePlanComplementaryResponse
from .auth import get_current_user
from ..models.user import User

router = APIRouter(prefix="/care-plans", tags=["Care Plans"])

@router.post("/generate/{intake_id}", response_model=CarePlanResponse)
def generate_care_plan(
    intake_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Fetch safety evaluation
    safety = db.query(SafetyAssessment).filter(SafetyAssessment.intake_session_id == intake_id).first()
    if not safety:
        raise HTTPException(status_code=400, detail="Run safety assessment before generating care plan")

    # Check if a care plan already exists
    existing_plan = db.query(CarePlan).filter(CarePlan.intake_session_id == intake_id).first()
    if existing_plan:
        return existing_plan

    # Create care plan
    care_plan = CarePlan(
        intake_session_id=intake_id,
        status="awaiting_review" if not safety.recommendations_blocked else "approved",
        professional_review_required=not safety.recommendations_blocked
    )
    db.add(care_plan)
    db.commit()
    db.refresh(care_plan)

    # If recommendations are blocked (Emergency), do NOT attach exercises, remedies, or meds
    if safety.recommendations_blocked:
        return care_plan

    # Otherwise, link some mock static content library recommendations for the MVP
    # Let's fetch some exercises
    exercises = db.query(ExerciseLibrary).filter(ExerciseLibrary.review_status == "approved").limit(2).all()
    for i, ex in enumerate(exercises):
        cpe = CarePlanExercise(
            care_plan_id=care_plan.id,
            exercise_id=ex.id,
            reason=f"Supportive movement for symptoms.",
            display_order=i
        )
        db.add(cpe)

    # Let's fetch maximum 3 complementary options
    remedies = db.query(ComplementaryOption).filter(ComplementaryOption.review_status == "approved").limit(3).all()
    for i, rem in enumerate(remedies):
        cpr = CarePlanComplementaryOption(
            care_plan_id=care_plan.id,
            option_id=rem.id,
            reason="Traditional supportive wellness.",
            display_order=i
        )
        db.add(cpr)

    # Let's fetch a medication
    meds = db.query(MedicationCatalog).limit(1).all()
    for m in meds:
        cpm = CarePlanMedicationInformation(
            care_plan_id=care_plan.id,
            medication_id=m.id,
            purpose="Symptomatic relief.",
            status="awaiting_review"
        )
        db.add(cpm)

    db.commit()
    db.refresh(care_plan)
    return care_plan

@router.get("/{id}", response_model=CarePlanResponse)
def get_care_plan(
    id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    plan = db.query(CarePlan).filter(CarePlan.id == id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Care plan not found")
        
    return plan
