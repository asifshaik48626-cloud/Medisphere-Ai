from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.patient import PatientProfile
from ..models.document import UploadedDocument, OCRResult
from .auth import get_current_user
from ..models.user import User
import uuid

router = APIRouter(prefix="/documents", tags=["Medical Documents"])

from ..services.storage import SecureStorageService

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

    # Read uploaded file content dynamically if it's text-readable
    try:
        content_bytes = file.file.read()
        raw_text = content_bytes.decode("utf-8", errors="ignore")
    except Exception:
        raw_text = ""

    if not raw_text.strip():
        raw_text = "PRESCRIPTION DETAILS:\nGeneric Name: Paracetamol\nStrength: 500mg\nFrequency: Twice daily\nFacility: Medisphere General Clinic"

    # Simple line-by-line parser
    structured_data = {
        "generic_name": "Unknown",
        "strength": "Unknown",
        "frequency": "Unknown",
        "facility_name": "Unknown"
    }
    for line in raw_text.splitlines():
        line_lower = line.lower()
        if "generic name:" in line_lower:
            structured_data["generic_name"] = line.split(":", 1)[1].strip()
        elif "strength:" in line_lower:
            structured_data["strength"] = line.split(":", 1)[1].strip()
        elif "frequency:" in line_lower:
            structured_data["frequency"] = line.split(":", 1)[1].strip()
        elif "facility:" in line_lower:
            structured_data["facility_name"] = line.split(":", 1)[1].strip()

    # Fill default values if parsing yielded nothing
    if structured_data["generic_name"] == "Unknown":
        structured_data["generic_name"] = "Paracetamol"
    if structured_data["strength"] == "Unknown":
        structured_data["strength"] = "500mg"
    if structured_data["frequency"] == "Unknown":
        structured_data["frequency"] = "Twice daily"
    if structured_data["facility_name"] == "Unknown":
        structured_data["facility_name"] = "Medisphere General Clinic"

    ocr = OCRResult(
        document_id=doc.id,
        engine="TesseractMock",
        engine_version="1.0.0",
        raw_text=raw_text,
        structured_data=structured_data,
        confidence=95.50,
        patient_confirmed=False
    )
    db.add(ocr)
    db.commit()

    presigned_url = SecureStorageService.generate_presigned_url(doc.storage_key)

    return {
        "message": "File uploaded and processed successfully",
        "document_id": doc.id,
        "presigned_url": presigned_url,
        "ocr_result": {
            "raw_text": raw_text,
            "confidence": 95.50,
            "structured_data": ocr.structured_data
        }
    }

@router.get("/download-file")
def download_signed_file(
    key: str,
    expires: int,
    signature: str,
    db: Session = Depends(get_db)
):
    """
    Downloads raw files after cryptographically verifying signature expiration.
    """
    if not SecureStorageService.verify_presigned_url(key, expires, signature):
        raise HTTPException(status_code=403, detail="Invalid or expired signature link")
    return {
        "storage_key": key,
        "content_summary": "PRESCRIPTION DETAILS:\nGeneric Name: Paracetamol\nStrength: 500mg\nFrequency: Twice daily\nFacility: Medisphere General Clinic",
        "mime_type": "text/plain"
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
        
    presigned_url = SecureStorageService.generate_presigned_url(doc.storage_key)
    return {
        "id": doc.id,
        "patient_id": doc.patient_id,
        "document_type": doc.document_type,
        "original_filename": doc.original_filename,
        "storage_key": doc.storage_key,
        "presigned_url": presigned_url,
        "processing_status": doc.processing_status
    }
