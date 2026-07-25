import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text, JSON, Numeric
from sqlalchemy.orm import relationship
from ..database import Base

class IntakeSession(Base):
    __tablename__ = "intake_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patient_profiles.id"), nullable=False)
    status = Column(String(50), nullable=False, default="started")  # started, answering, completed, terminated
    input_mode = Column(String(50), nullable=False, default="text")  # text, voice
    language_code = Column(String(10), nullable=False, default="en")
    main_complaint = Column(Text, nullable=False)
    
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = relationship("PatientProfile", back_populates="intake_sessions")
    symptoms = relationship("Symptom", back_populates="intake_session")
    questions = relationship("IntakeQuestion", back_populates="intake_session")
    safety_assessments = relationship("SafetyAssessment", back_populates="intake_session")
    care_plans = relationship("CarePlan", back_populates="intake_session")
    reports = relationship("GeneratedReport", back_populates="intake_session")

class Symptom(Base):
    __tablename__ = "symptoms"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    intake_session_id = Column(String(36), ForeignKey("intake_sessions.id"), nullable=False)
    symptom_name = Column(String(150), nullable=False)
    normalized_code = Column(String(100), nullable=True)  # SNOMED
    body_location = Column(String(150), nullable=True)
    severity = Column(Integer, nullable=True)  # e.g., 1-10
    onset_at = Column(DateTime, nullable=True)
    duration_text = Column(String(100), nullable=True)  # e.g., "3 days"
    frequency = Column(String(100), nullable=True)  # e.g., "intermittent"
    metadata_json = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    intake_session = relationship("IntakeSession", back_populates="symptoms")

class IntakeQuestion(Base):
    __tablename__ = "intake_questions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    intake_session_id = Column(String(36), ForeignKey("intake_sessions.id"), nullable=False)
    question_code = Column(String(100), nullable=False)  # e.g., "temp_check"
    question_text = Column(Text, nullable=False)
    language_code = Column(String(10), nullable=False, default="en")
    sequence_number = Column(Integer, nullable=False)
    required = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    intake_session = relationship("IntakeSession", back_populates="questions")
    answers = relationship("IntakeAnswer", back_populates="question")

class IntakeAnswer(Base):
    __tablename__ = "intake_answers"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    question_id = Column(String(36), ForeignKey("intake_questions.id"), nullable=False)
    answer_text = Column(Text, nullable=True)
    answer_json = Column(JSON, nullable=True)
    input_mode = Column(String(50), nullable=False, default="text")  # text, voice
    confidence = Column(Numeric(5, 2), nullable=True)
    confirmed_by_patient = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    question = relationship("IntakeQuestion", back_populates="answers")
