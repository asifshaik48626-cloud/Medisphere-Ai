import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    auth_provider_id = Column(String(255), unique=True, nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=True)
    phone = Column(String(50), unique=True, index=True, nullable=True)
    role = Column(String(50), nullable=False, index=True)  # Patient, Doctor, Pharmacist, etc.
    status = Column(String(50), nullable=False, default="active", index=True)  # Active, Pending, Suspended, etc.
    preferred_language = Column(String(10), default="en")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    patient_profile = relationship("PatientProfile", back_populates="user", uselist=False)
    professional_profile = relationship("ProfessionalProfile", foreign_keys="ProfessionalProfile.user_id", back_populates="user", uselist=False)
    audit_logs = relationship("AuditLog", back_populates="actor_user")
