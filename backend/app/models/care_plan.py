import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..database import Base

class CarePlan(Base):
    __tablename__ = "care_plans"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    intake_session_id = Column(String(36), ForeignKey("intake_sessions.id"), nullable=False)
    status = Column(String(50), nullable=False, default="draft")  # draft, awaiting_review, approved, rejected
    generated_by_model = Column(String(100), nullable=True)
    model_version = Column(String(50), nullable=True)
    prompt_version = Column(String(50), nullable=True)
    professional_review_required = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    intake_session = relationship("IntakeSession", back_populates="care_plans")
    exercises = relationship("CarePlanExercise", back_populates="care_plan")
    complementary_options = relationship("CarePlanComplementaryOption", back_populates="care_plan")
    medications = relationship("CarePlanMedicationInformation", back_populates="care_plan")

class CarePlanExercise(Base):
    __tablename__ = "care_plan_exercises"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    care_plan_id = Column(String(36), ForeignKey("care_plans.id"), nullable=False)
    exercise_id = Column(String(36), ForeignKey("exercise_library.id"), nullable=False)
    reason = Column(Text, nullable=True)
    display_order = Column(Integer, nullable=False, default=0)
    status = Column(String(50), nullable=False, default="active")

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    care_plan = relationship("CarePlan", back_populates="exercises")
    exercise = relationship("ExerciseLibrary", back_populates="care_plan_exercises")

class CarePlanComplementaryOption(Base):
    __tablename__ = "care_plan_complementary_options"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    care_plan_id = Column(String(36), ForeignKey("care_plans.id"), nullable=False)
    option_id = Column(String(36), ForeignKey("complementary_options.id"), nullable=False)
    reason = Column(Text, nullable=True)
    display_order = Column(Integer, nullable=False, default=0)
    status = Column(String(50), nullable=False, default="active")

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    care_plan = relationship("CarePlan", back_populates="complementary_options")
    option = relationship("ComplementaryOption", back_populates="care_plan_options")

class CarePlanMedicationInformation(Base):
    __tablename__ = "care_plan_medication_information"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    care_plan_id = Column(String(36), ForeignKey("care_plans.id"), nullable=False)
    medication_id = Column(String(36), ForeignKey("medication_catalog.id"), nullable=False)
    purpose = Column(Text, nullable=True)
    professional_review_required = Column(Boolean, nullable=False, default=True)
    status = Column(String(50), nullable=False, default="awaiting_review")  # approved, rejected, awaiting_review
    reviewed_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    care_plan = relationship("CarePlan", back_populates="medications")
    medication = relationship("MedicationCatalog", back_populates="care_plan_medications")
    reviewer = relationship("User", foreign_keys=[reviewed_by])
