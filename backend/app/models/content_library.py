import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from ..database import Base

class ExerciseLibrary(Base):
    __tablename__ = "exercise_library"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    body_area = Column(String(100), nullable=True)
    difficulty = Column(String(50), nullable=True)  # Beginner, Intermediate, Advanced
    duration_seconds = Column(Integer, nullable=True)
    repetitions = Column(Integer, nullable=True)
    video_url = Column(Text, nullable=True)
    instructions = Column(JSON, nullable=True)
    contraindications = Column(JSON, nullable=True)
    stop_conditions = Column(JSON, nullable=True)
    evidence_level = Column(String(50), nullable=True)
    review_status = Column(String(50), nullable=False, default="pending")  # approved, rejected, pending
    reviewed_by = Column(String(36), ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    reviewer = relationship("User", foreign_keys=[reviewed_by])
    care_plan_exercises = relationship("CarePlanExercise", back_populates="exercise")

class ComplementaryOption(Base):
    __tablename__ = "complementary_options"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), unique=True, nullable=False)
    traditional_use = Column(Text, nullable=True)
    possible_benefits = Column(JSON, nullable=True)
    possible_risks = Column(JSON, nullable=True)
    contraindications = Column(JSON, nullable=True)
    drug_interactions = Column(JSON, nullable=True)
    evidence_level = Column(String(50), nullable=True)
    source_id = Column(String(36), ForeignKey("source_documents.id"), nullable=True)
    review_status = Column(String(50), nullable=False, default="pending")  # approved, rejected, pending
    reviewed_by = Column(String(36), ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    source_document = relationship("SourceDocument", back_populates="complementary_options")
    reviewer = relationship("User", foreign_keys=[reviewed_by])
    care_plan_options = relationship("CarePlanComplementaryOption", back_populates="option")
