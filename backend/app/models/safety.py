import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from ..database import Base

class SafetyAssessment(Base):
    __tablename__ = "safety_assessments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    intake_session_id = Column(String(36), ForeignKey("intake_sessions.id"), nullable=False)
    urgency_level = Column(String(50), nullable=False)  # Emergency, Urgent, Same-day, Routine, Monitor, etc.
    decision_source = Column(String(100), nullable=False)  # e.g., "deterministic_rule_engine"
    rule_version = Column(String(50), nullable=False)
    recommendations_blocked = Column(Boolean, nullable=False, default=False)
    requires_professional_review = Column(Boolean, nullable=False, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    intake_session = relationship("IntakeSession", back_populates="safety_assessments")
    red_flags = relationship("RedFlagEvent", back_populates="safety_assessment")

class RedFlagEvent(Base):
    __tablename__ = "red_flag_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    safety_assessment_id = Column(String(36), ForeignKey("safety_assessments.id"), nullable=False)
    rule_code = Column(String(100), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String(50), nullable=False)  # Critical, High, Moderate
    evidence = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    safety_assessment = relationship("SafetyAssessment", back_populates="red_flags")
