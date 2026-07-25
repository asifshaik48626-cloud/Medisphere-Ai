import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from ..database import Base

class Consent(Base):
    __tablename__ = "consents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patient_profiles.id"), nullable=False)
    consent_type = Column(String(100), nullable=False)  # Privacy, AI, Voice, etc.
    version = Column(String(50), nullable=False)
    accepted = Column(Boolean, nullable=False, default=True)
    accepted_at = Column(DateTime, default=datetime.utcnow)
    revoked_at = Column(DateTime, nullable=True)
    ip_address = Column(String(45), nullable=True)  # IPv4/IPv6 length
    metadata_json = Column(JSON, nullable=True)  # Stored as metadata_json to avoid Python conflict

    # Relationships
    patient = relationship("PatientProfile", back_populates="consents")
