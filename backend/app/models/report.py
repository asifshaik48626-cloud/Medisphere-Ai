import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from ..database import Base

class GeneratedReport(Base):
    __tablename__ = "generated_reports"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patient_profiles.id"), nullable=False)
    intake_session_id = Column(String(36), ForeignKey("intake_sessions.id"), nullable=True)
    report_type = Column(String(100), nullable=False)  # PatientSummary, DoctorNote, etc.
    status = Column(String(50), nullable=False, default="draft")  # draft, approved, archived
    storage_key = Column(Text, nullable=True)  # path in S3/MinIO
    generated_content = Column(JSON, nullable=True)
    model_version = Column(String(50), nullable=True)
    prompt_version = Column(String(50), nullable=True)
    approved_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = relationship("PatientProfile", back_populates="reports")
    intake_session = relationship("IntakeSession", back_populates="reports")
    approver = relationship("User", foreign_keys=[approved_by])
