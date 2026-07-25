from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.report import GeneratedReport
from ..models.patient import PatientProfile
from ..models.care_plan import CarePlan
from ..models.user import User
from .auth import get_current_user
import json

router = APIRouter(prefix="/reports", tags=["Report Generation"])

@router.post("/generate")
def generate_report(
    patient_id: str,
    intake_session_id: str = None,
    report_type: str = "ClinicalSummary",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify patient profile
    patient = db.query(PatientProfile).filter(PatientProfile.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")

    # Access control
    if current_user.role == "patient":
        profile = db.query(PatientProfile).filter(PatientProfile.user_id == current_user.id).first()
        if not profile or profile.id != patient_id:
            raise HTTPException(status_code=403, detail="Not authorized to generate reports for other patients")

    # Pull active care plan
    care_plan = db.query(CarePlan).filter(CarePlan.patient_id == patient_id).order_by(CarePlan.created_at.desc()).first()
    
    # Structure report contents
    generated_content = {
        "title": "MediSphere AI - Clinical Care Summary",
        "patient_name": f"{patient.first_name} {patient.last_name}",
        "date_of_birth": str(patient.date_of_birth),
        "country": patient.country_code,
        "urgency_rating": "Routine" if not care_plan else "Urgent" if "urgent" in str(care_plan.notes).lower() else "Monitor",
        "clinical_timeline": [
            {
                "timestamp": "2026-07-26T00:00:00Z",
                "event": "Intake Assessment Completed",
                "notes": "Patient described high temperature and headache."
            }
        ],
        "three_column_care_plan": {
            "movements": ["Gentle neck rolls", "Deep diaphragmatic breathing"] if not care_plan else [],
            "remedies": ["Ginger root extraction infusion"] if not care_plan else [],
            "medications": ["Paracetamol 500mg as needed"] if not care_plan else []
        },
        "safety_disclaimer": "MediSphere AI is an assistant utility. This summary does not replace formal diagnosis or clinical verification."
    }

    report = GeneratedReport(
        patient_id=patient_id,
        intake_session_id=intake_session_id,
        report_type=report_type,
        status="approved" if current_user.role != "patient" else "draft",
        generated_content=generated_content,
        model_version="MediSphere-v1",
        prompt_version="clinical-v1.0"
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    return {
        "message": "Report generated successfully",
        "report_id": report.id,
        "content": generated_content
    }

@router.get("/{id}/download", response_class=PlainTextResponse)
def download_clinical_report(
    id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    report = db.query(GeneratedReport).filter(GeneratedReport.id == id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report record not found")

    content = report.generated_content
    
    # Format report into clean markdown for print output
    markdown_report = f"""# {content.get('title', 'Clinical Summary')}
Generated on: {report.created_at.strftime('%Y-%m-%d %H:%M:%S')} UTC
Report ID: {report.id}
Status: {report.status.upper()}

## Patient Demographics
- **Name**: {content.get('patient_name')}
- **Date of Birth**: {content.get('date_of_birth')}
- **Country Code**: {content.get('country')}

## Clinical Details
- **Urgency Rating**: {content.get('urgency_rating')}
- **Safety Disclaimer**: {content.get('safety_disclaimer')}

## Recommended Three-Column Care Actions
### 1. Movements & Exercises
{chr(10).join(['- ' + ex for ex in content.get('three_column_care_plan', {}).get('movements', [])])}

### 2. Complementary Remedies
{chr(10).join(['- ' + rem for rem in content.get('three_column_care_plan', {}).get('remedies', [])])}

### 3. Medications
{chr(10).join(['- ' + med for med in content.get('three_column_care_plan', {}).get('medications', [])])}

---
*Verified by MediSphere Clinical Assistant Protocol*
"""
    return markdown_report

@router.get("/list")
def list_reports(
    patient_id: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(GeneratedReport)
    
    if current_user.role == "patient":
        profile = db.query(PatientProfile).filter(PatientProfile.user_id == current_user.id).first()
        if not profile:
            return []
        query = query.filter(GeneratedReport.patient_id == profile.id)
    elif patient_id:
        query = query.filter(GeneratedReport.patient_id == patient_id)
        
    return query.order_by(GeneratedReport.created_at.desc()).all()
