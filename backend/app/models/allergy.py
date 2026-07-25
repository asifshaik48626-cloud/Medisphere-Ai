import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Allergy(Base):
    __tablename__ = "allergies"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patient_profiles.id"), nullable=False)
    substance_name = Column(String(200), nullable=False)
    normalized_code = Column(String(100), nullable=True)  # RxNorm, SNOMED, etc.
    reaction = Column(String(255), nullable=True)
    severity = Column(String(50), nullable=True)  # Mild, Moderate, Severe
    status = Column(String(50), nullable=False, default="active")  # active, inactive, resolved
    source = Column(String(100), nullable=False, default="patient_reported")  # patient_reported, medical_record, etc.

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = relationship("PatientProfile", back_populates="allergies")
