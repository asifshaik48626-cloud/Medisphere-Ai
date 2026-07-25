from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.patient import PatientProfile
from ..models.intake import IntakeSession, IntakeQuestion, IntakeAnswer, Symptom
from ..schemas.intake import IntakeSessionCreate, IntakeSessionResponse, IntakeQuestionResponse, IntakeAnswerSubmit
from .auth import get_current_user
from ..models.user import User

router = APIRouter(prefix="/intakes", tags=["Symptom Intake"])

@router.post("", response_model=IntakeSessionResponse)
def create_intake_session(
    session_in: IntakeSessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "patient":
        raise HTTPException(status_code=403, detail="Only patients can start intakes")
        
    profile = db.query(PatientProfile).filter(PatientProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=400, detail="Patient profile required before starting symptom intake")

    # Create session
    session = IntakeSession(
        patient_id=profile.id,
        main_complaint=session_in.main_complaint,
        input_mode=session_in.input_mode,
        language_code=session_in.language_code,
        status="answering"
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    # Automatically seed questions based on main complaint keywords (Fever or Headache)
    complaint_lower = session_in.main_complaint.lower()
    questions = []
    
    if "fever" in complaint_lower:
        questions = [
            IntakeQuestion(
                intake_session_id=session.id,
                question_code="fever_temp",
                question_text="What is your current body temperature in degrees (Fahrenheit or Celsius) if measured?",
                sequence_number=1,
                required=True
            ),
            IntakeQuestion(
                intake_session_id=session.id,
                question_code="fever_red_flags",
                question_text="Do you have a stiff neck, severe headache, confusion, or difficulty breathing?",
                sequence_number=2,
                required=True
            ),
            IntakeQuestion(
                intake_session_id=session.id,
                question_code="fever_duration",
                question_text="How many days has the fever lasted?",
                sequence_number=3,
                required=True
            )
        ]
    elif "headache" in complaint_lower:
        questions = [
            IntakeQuestion(
                intake_session_id=session.id,
                question_code="headache_thunderclap",
                question_text="Did this headache start suddenly and reach maximum severe intensity within one minute?",
                sequence_number=1,
                required=True
            ),
            IntakeQuestion(
                intake_session_id=session.id,
                question_code="headache_red_flags",
                question_text="Do you have neck stiffness, fever, confusion, numbness, or slurred speech?",
                sequence_number=2,
                required=True
            ),
            IntakeQuestion(
                intake_session_id=session.id,
                question_code="headache_location",
                question_text="Where is the pain located, and how would you describe it?",
                sequence_number=3,
                required=True
            )
        ]
    else:
        # Default fallback general questions
        questions = [
            IntakeQuestion(
                intake_session_id=session.id,
                question_code="general_severity",
                question_text="How severe is the pain/discomfort on a scale of 1 to 10?",
                sequence_number=1,
                required=True
            ),
            IntakeQuestion(
                intake_session_id=session.id,
                question_code="general_duration",
                question_text="How long have you been experiencing these symptoms?",
                sequence_number=2,
                required=True
            )
        ]

    for q in questions:
        db.add(q)
    db.commit()
    
    return session

@router.get("/{id}/questions", response_model=List[IntakeQuestionResponse])
def get_intake_questions(
    id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = db.query(IntakeSession).filter(IntakeSession.id == id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Intake session not found")
        
    return db.query(IntakeQuestion).filter(IntakeQuestion.intake_session_id == id).order_by(IntakeQuestion.sequence_number).all()

@router.post("/questions/{q_id}/answers")
def submit_answer(
    q_id: str,
    answer_in: IntakeAnswerSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    question = db.query(IntakeQuestion).filter(IntakeQuestion.id == q_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
        
    session = db.query(IntakeSession).filter(IntakeSession.id == question.intake_session_id).first()
    
    # Save the answer
    existing_answer = db.query(IntakeAnswer).filter(IntakeAnswer.question_id == q_id).first()
    if existing_answer:
        existing_answer.answer_text = answer_in.answer_text
        existing_answer.answer_json = answer_in.answer_json
        existing_answer.input_mode = answer_in.input_mode
        existing_answer.confirmed_by_patient = answer_in.confirmed_by_patient
        db.commit()
        db.refresh(existing_answer)
        answer = existing_answer
    else:
        answer = IntakeAnswer(
            question_id=q_id,
            answer_text=answer_in.answer_text,
            answer_json=answer_in.answer_json,
            input_mode=answer_in.input_mode,
            confirmed_by_patient=answer_in.confirmed_by_patient
        )
        db.add(answer)
        db.commit()
        db.refresh(answer)

    # Process and extract symptoms from answers
    cls_extract_symptoms(session, question, answer, db)
    
    return {"message": "Answer saved successfully", "answer_id": answer.id}

def cls_extract_symptoms(session: IntakeSession, question: IntakeQuestion, answer: IntakeAnswer, db: Session):
    """
    Parses user answers to populate structured Symptom records.
    For this MVP, we parse standard questionnaires deterministically.
    """
    text = (answer.answer_text or "").lower()
    
    # Let's search or update a symptom for this session
    # Fever temperature question
    if question.question_code == "fever_temp":
        # Check if they entered a high temp
        severity_val = 5
        if "10" in text or "39" in text or "40" in text:
            severity_val = 8
        
        existing_sym = db.query(Symptom).filter(Symptom.intake_session_id == session.id, Symptom.symptom_name == "Fever").first()
        if not existing_sym:
            symptom = Symptom(
                intake_session_id=session.id,
                symptom_name="Fever",
                severity=severity_val,
                body_location="Systemic",
                duration_text="onset matching intake"
            )
            db.add(symptom)
            db.commit()
            
    elif question.question_code == "fever_red_flags":
        if any(w in text for w in ["yes", "neck", "stiff", "breath", "headache", "confus"]):
            # Trigger emergency warning symptom
            symptom_name = "Fever with stiff neck/breathing difficulty"
            existing_sym = db.query(Symptom).filter(Symptom.intake_session_id == session.id, Symptom.symptom_name == symptom_name).first()
            if not existing_sym:
                symptom = Symptom(
                    intake_session_id=session.id,
                    symptom_name=symptom_name,
                    severity=9,
                    body_location="Systemic/Respiratory/Neurological"
                )
                db.add(symptom)
                db.commit()

    elif question.question_code == "fever_duration":
        # Extract duration
        existing_sym = db.query(Symptom).filter(Symptom.intake_session_id == session.id, Symptom.symptom_name == "Fever").first()
        if existing_sym:
            existing_sym.duration_text = answer.answer_text
            db.commit()
            
    # Headache question
    elif question.question_code == "headache_thunderclap":
        if any(w in text for w in ["yes", "sudden", "severe", "thunderclap"]):
            symptom_name = "Sudden severe headache (Thunderclap)"
            existing_sym = db.query(Symptom).filter(Symptom.intake_session_id == session.id, Symptom.symptom_name == symptom_name).first()
            if not existing_sym:
                symptom = Symptom(
                    intake_session_id=session.id,
                    symptom_name=symptom_name,
                    severity=10,
                    body_location="Head"
                )
                db.add(symptom)
                db.commit()
        else:
            # Regular headache
            existing_sym = db.query(Symptom).filter(Symptom.intake_session_id == session.id, Symptom.symptom_name == "Headache").first()
            if not existing_sym:
                symptom = Symptom(
                    intake_session_id=session.id,
                    symptom_name="Headache",
                    severity=5,
                    body_location="Head"
                )
                db.add(symptom)
                db.commit()

    elif question.question_code == "headache_red_flags":
        if any(w in text for w in ["yes", "stiff", "neck", "fever", "slur", "numb"]):
            symptom_name = "Headache with neck stiffness/neurological signs"
            existing_sym = db.query(Symptom).filter(Symptom.intake_session_id == session.id, Symptom.symptom_name == symptom_name).first()
            if not existing_sym:
                symptom = Symptom(
                    intake_session_id=session.id,
                    symptom_name=symptom_name,
                    severity=9,
                    body_location="Neurological"
                )
                db.add(symptom)
                db.commit()
