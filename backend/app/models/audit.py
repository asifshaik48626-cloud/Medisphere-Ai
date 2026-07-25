import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from ..database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    actor_user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    action = Column(String(150), nullable=False, index=True)  # e.g., "view_patient_record"
    entity_type = Column(String(100), nullable=True)  # e.g., "PatientProfile"
    entity_id = Column(String(36), nullable=True)
    before_data = Column(JSON, nullable=True)
    after_data = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)  # Support IPv6
    user_agent = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    actor_user = relationship("User", back_populates="audit_logs")
