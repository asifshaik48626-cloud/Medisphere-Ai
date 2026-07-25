import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text, JSON, Numeric, BigInteger, Date
from sqlalchemy.orm import relationship
from ..database import Base

class SourceDocument(Base):
    __tablename__ = "source_documents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    publisher = Column(String(150), nullable=True)
    source_type = Column(String(100), nullable=True)  # Guideline, Journal, Manual
    url = Column(Text, nullable=True)
    publication_date = Column(Date, nullable=True)
    revision_date = Column(Date, nullable=True)
    status = Column(String(50), nullable=False, default="active")
    metadata_json = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    chunks = relationship("GuidelineChunk", back_populates="source_document")
    medications = relationship("MedicationCatalog", back_populates="source_document")
    complementary_options = relationship("ComplementaryOption", back_populates="source_document")

class GuidelineChunk(Base):
    __tablename__ = "guideline_chunks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_document_id = Column(String(36), ForeignKey("source_documents.id"), nullable=False)
    section_title = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    embedding = Column(JSON, nullable=True)  # Portable float list representation
    metadata_json = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    source_document = relationship("SourceDocument", back_populates="chunks")

class UploadedDocument(Base):
    __tablename__ = "uploaded_documents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patient_profiles.id"), nullable=False)
    document_type = Column(String(100), nullable=False)  # Prescription, LabReport, etc.
    original_filename = Column(String(255), nullable=False)
    storage_key = Column(Text, nullable=False)
    mime_type = Column(String(100), nullable=False)
    file_size = Column(BigInteger, nullable=False)
    processing_status = Column(String(50), nullable=False, default="uploaded")  # uploaded, processing, extracted, failed
    
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    patient = relationship("PatientProfile", back_populates="documents")
    ocr_results = relationship("OCRResult", back_populates="document")

class OCRResult(Base):
    __tablename__ = "ocr_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("uploaded_documents.id"), nullable=False)
    engine = Column(String(100), nullable=True)
    engine_version = Column(String(50), nullable=True)
    raw_text = Column(Text, nullable=False)
    structured_data = Column(JSON, nullable=True)
    confidence = Column(Numeric(5, 2), nullable=True)
    patient_confirmed = Column(Boolean, nullable=False, default=False)
    professional_confirmed = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    document = relationship("UploadedDocument", back_populates="ocr_results")
