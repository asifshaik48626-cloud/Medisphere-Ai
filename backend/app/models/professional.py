import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class ProfessionalProfile(Base):
    __tablename__ = "professional_profiles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), unique=True, nullable=False)
    professional_type = Column(String(100), nullable=False)  # Doctor, Pharmacist, Physiotherapist, etc.
    speciality = Column(String(150), nullable=True)
    registration_number = Column(String(100), nullable=False)
    organization = Column(String(200), nullable=True)
    verification_status = Column(String(50), nullable=False, default="pending")  # pending, verified, rejected
    verified_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    verified_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="professional_profile")
    verifier = relationship("User", foreign_keys=[verified_by])
    appointments = relationship("Appointment", back_populates="professional")
