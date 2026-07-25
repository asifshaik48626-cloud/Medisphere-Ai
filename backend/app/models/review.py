import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..database import Base

class ProfessionalReview(Base):
    __tablename__ = "professional_reviews"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    review_type = Column(String(100), nullable=False)  # CarePlan, Medication, Exercise, Remedy
    entity_type = Column(String(100), nullable=False)  # e.g., "CarePlan"
    entity_id = Column(String(36), nullable=False)  # target UUID
    assigned_to = Column(String(36), ForeignKey("users.id"), nullable=True)
    reviewer_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    status = Column(String(50), nullable=False, default="pending")  # pending, approved, rejected, changes_requested
    comments = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)

    # Relationships
    assigned_professional = relationship("User", foreign_keys=[assigned_to])
    reviewer = relationship("User", foreign_keys=[reviewer_id])
