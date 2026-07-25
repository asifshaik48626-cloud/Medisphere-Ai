import uuid
from datetime import datetime
from sqlalchemy import Column, String, Date, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from ..database import Base

class MedicationCatalog(Base):
    __tablename__ = "medication_catalog"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    generic_name = Column(String(255), unique=True, nullable=False)
    brand_names = Column(JSON, nullable=True)  # List of brand names
    normalized_code = Column(String(100), nullable=True)  # RxNorm, RxCUI, etc.
    medicine_class = Column(String(150), nullable=True)
    otc_or_prescription = Column(String(50), nullable=False, default="prescription")  # otc, prescription
    warnings = Column(JSON, nullable=True)
    contraindications = Column(JSON, nullable=True)
    side_effects = Column(JSON, nullable=True)
    interaction_metadata = Column(JSON, nullable=True)
    source_id = Column(String(36), ForeignKey("source_documents.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    source_document = relationship("SourceDocument", back_populates="medications")
    care_plan_medications = relationship("CarePlanMedicationInformation", back_populates="medication")

class PatientMedication(Base):
    __tablename__ = "patient_medications"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patient_profiles.id"), nullable=False)
    brand_name = Column(String(200), nullable=True)
    generic_name = Column(String(255), nullable=False)
    normalized_code = Column(String(100), nullable=True)  # RxNorm
    strength = Column(String(100), nullable=True)  # e.g., 500mg
    dosage_form = Column(String(100), nullable=True)  # e.g., tablet, liquid
    frequency = Column(String(150), nullable=True)  # e.g., twice daily
    route = Column(String(100), nullable=True)  # e.g., oral
    status = Column(String(50), nullable=False, default="active")  # active, suspended, completed, discontinued
    prescribed_by = Column(String(200), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = relationship("PatientProfile", back_populates="medications")
