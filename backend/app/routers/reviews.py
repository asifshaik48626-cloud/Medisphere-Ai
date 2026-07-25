from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.review import ProfessionalReview
from ..models.care_plan import CarePlan, CarePlanMedicationInformation
from .auth import get_current_user
from ..models.user import User
from datetime import datetime

router = APIRouter(prefix="/reviews", tags=["Professional Review"])

@router.get("/queue")
def get_review_queue(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["doctor", "pharmacist", "physiotherapist", "practitioner"]:
        raise HTTPException(status_code=403, detail="Only verified professionals can view the review queue")

    # Map roles to target review types
    review_type_map = {
        "doctor": "CarePlan",
        "pharmacist": "Medication",
        "physiotherapist": "Exercise",
        "practitioner": "Remedy"
    }
    
    target_type = review_type_map.get(current_user.role)
    reviews = db.query(ProfessionalReview).filter(
        ProfessionalReview.review_type == target_type,
        ProfessionalReview.status == "pending"
    ).all()
    
    return reviews

@router.post("/{id}/approve")
def approve_review(
    id: str,
    comments: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["doctor", "pharmacist", "physiotherapist", "practitioner"]:
        raise HTTPException(status_code=403, detail="Unauthorized")

    review = db.query(ProfessionalReview).filter(ProfessionalReview.id == id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review item not found")

    review.status = "approved"
    review.reviewer_id = current_user.id
    review.reviewed_at = datetime.utcnow()
    if comments:
        review.comments = comments

    # Perform cascading updates on target entities
    if review.entity_type == "CarePlan":
        plan = db.query(CarePlan).filter(CarePlan.id == review.entity_id).first()
        if plan:
            plan.status = "approved"
            
    elif review.entity_type == "Medication":
        med = db.query(CarePlanMedicationInformation).filter(CarePlanMedicationInformation.id == review.entity_id).first()
        if med:
            med.status = "approved"
            med.reviewed_by = current_user.id
            med.reviewed_at = datetime.utcnow()

    db.commit()
    return {"status": "approved", "review_id": id}

@router.post("/{id}/reject")
def reject_review(
    id: str,
    comments: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["doctor", "pharmacist", "physiotherapist", "practitioner"]:
        raise HTTPException(status_code=403, detail="Unauthorized")

    review = db.query(ProfessionalReview).filter(ProfessionalReview.id == id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review item not found")

    review.status = "rejected"
    review.reviewer_id = current_user.id
    review.reviewed_at = datetime.utcnow()
    review.comments = comments

    # Update target entities
    if review.entity_type == "CarePlan":
        plan = db.query(CarePlan).filter(CarePlan.id == review.entity_id).first()
        if plan:
            plan.status = "rejected"
            
    elif review.entity_type == "Medication":
        med = db.query(CarePlanMedicationInformation).filter(CarePlanMedicationInformation.id == review.entity_id).first()
        if med:
            med.status = "rejected"

    db.commit()
    return {"status": "rejected", "review_id": id}
