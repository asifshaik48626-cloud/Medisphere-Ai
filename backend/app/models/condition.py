import uuid
from datetime import datetime
from sqlalchemy import Column, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class PatientCondition(Base):
    __tablename__ = "patient_conditions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patient_profiles.id"), nullable=False)
    condition_name = Column(String(200), nullable=False)
    normalized_code = Column(String(100), nullable=True)  # ICD-10, SNOMED, etc.
    status = Column(String(50), nullable=False, default="active")  # active, inactive, resolved, history
    onset_date = Column(Date, nullable=True)
    recorded_by = Column(String(36), ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = relationship("PatientProfile", back_populates="conditions")
    recorder = relationship("User", foreign_keys=[recorded_by])
