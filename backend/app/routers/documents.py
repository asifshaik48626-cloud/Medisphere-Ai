from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.patient import PatientProfile
from ..models.document import UploadedDocument, OCRResult
from .auth import get_current_user
from ..models.user import User
import uuid

router = APIRouter(prefix="/documents", tags=["Medical Documents"])

@router.post("/upload")
def upload_medical_document(
    document_type: str = Form(...),  # Prescription, LabReport, etc.
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "patient":
        raise HTTPException(status_code=403, detail="Only patients can upload reports")
        
    profile = db.query(PatientProfile).filter(PatientProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=400, detail="Patient profile required before uploading documents")

    # Generate static storage path for mock uploads
    storage_key = f"uploads/{profile.id}/{uuid.uuid4()}-{file.filename}"

    # Create document record
    doc = UploadedDocument(
        patient_id=profile.id,
        document_type=document_type,
        original_filename=file.filename,
        storage_key=storage_key,
        mime_type=file.content_type or "application/octet-stream",
        file_size=1000,  # mock size
        processing_status="extracted"
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    # Automatically generate structured mock OCR results for MVP demonstration
    raw_text = "PRESCRIPTION DETAILS:\nGeneric Name: Paracetamol\nStrength: 500mg\nFrequency: Twice daily\nFacility: Medisphere General Clinic"
    
    ocr = OCRResult(
        document_id=doc.id,
        engine="TesseractMock",
        engine_version="1.0.0",
        raw_text=raw_text,
        structured_data={
            "generic_name": "Paracetamol",
            "strength": "500mg",
            "frequency": "Twice daily",
            "facility_name": "Medisphere General Clinic"
        },
        confidence=95.50,
        patient_confirmed=False
    )
    db.add(ocr)
    db.commit()

    return {
        "message": "File uploaded and processed successfully",
        "document_id": doc.id,
        "ocr_result": {
            "raw_text": raw_text,
            "confidence": 95.50,
            "structured_data": ocr.structured_data
        }
    }

@router.get("/{id}")
def get_uploaded_document(
    id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc = db.query(UploadedDocument).filter(UploadedDocument.id == id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc
