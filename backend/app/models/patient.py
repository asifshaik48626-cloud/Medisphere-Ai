import uuid
from datetime import datetime
from sqlalchemy import Column, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class PatientProfile(Base):
    __tablename__ = "patient_profiles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    sex_at_birth = Column(String(50), nullable=True)
    gender_identity = Column(String(100), nullable=True)
    country_code = Column(String(5), nullable=False, default="IN")
    timezone = Column(String(50), nullable=False, default="Asia/Kolkata")
    emergency_contact_name = Column(String(150), nullable=True)
    emergency_contact_phone = Column(String(50), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="patient_profile")
    consents = relationship("Consent", back_populates="patient")
    allergies = relationship("Allergy", back_populates="patient")
    conditions = relationship("PatientCondition", back_populates="patient")
    medications = relationship("PatientMedication", back_populates="patient")
    intake_sessions = relationship("IntakeSession", back_populates="patient")
    documents = relationship("UploadedDocument", back_populates="patient")
    appointments = relationship("Appointment", back_populates="patient")
    reports = relationship("GeneratedReport", back_populates="patient")
