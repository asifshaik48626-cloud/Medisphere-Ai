import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..database import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patient_profiles.id"), nullable=False)
    professional_id = Column(String(36), ForeignKey("professional_profiles.id"), nullable=False)
    appointment_type = Column(String(100), nullable=False, default="Consultation")  # Consultation, Routine, FollowUp
    scheduled_start = Column(DateTime, nullable=False)
    scheduled_end = Column(DateTime, nullable=False)
    status = Column(String(50), nullable=False, default="scheduled")  # scheduled, completed, cancelled, no_show
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = relationship("PatientProfile", back_populates="appointments")
    professional = relationship("ProfessionalProfile", back_populates="appointments")
