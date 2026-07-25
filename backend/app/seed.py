from sqlalchemy.orm import Session
from datetime import date, datetime
from .database import engine, SessionLocal, Base
from .models.user import User
from .models.patient import PatientProfile
from .models.professional import ProfessionalProfile
from .models.content_library import ExerciseLibrary, ComplementaryOption
from .models.medication import MedicationCatalog
from .utils.security import get_password_hash

def seed_database():
    # Make sure all tables are created
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Check if users already exist
        patient_user = db.query(User).filter(User.email == "patient@medisphere.com").first()
        if not patient_user:
            print("Seeding test users and profiles...")
            # 1. Patient User
            patient_pwd = get_password_hash("password123")
            p_user = User(
                email="patient@medisphere.com",
                role="patient",
                status="active",
                auth_provider_id=f"local-hashed:patient:{patient_pwd}"
            )
            db.add(p_user)
            db.commit()
            db.refresh(p_user)

            p_profile = PatientProfile(
                user_id=p_user.id,
                first_name="Asif",
                last_name="Shaik",
                date_of_birth=date(2005, 7, 26),
                country_code="IN",
                timezone="Asia/Kolkata"
            )
            db.add(p_profile)

            # 2. Doctor User
            doctor_pwd = get_password_hash("password123")
            d_user = User(
                email="doctor@medisphere.com",
                role="doctor",
                status="active",
                auth_provider_id=f"local-hashed:doctor:{doctor_pwd}"
            )
            db.add(d_user)
            db.commit()
            db.refresh(d_user)

            d_profile = ProfessionalProfile(
                user_id=d_user.id,
                professional_type="doctor",
                speciality="General Medicine",
                registration_number="REG-123456",
                organization="Medisphere AI Clinic",
                verification_status="verified",
                verified_by=d_user.id,
                verified_at=datetime.utcnow()
            )
            db.add(d_profile)
            db.commit()
            print("✅ Users and Profiles successfully seeded!")

        # 3. Seed Exercise Library
        if db.query(ExerciseLibrary).count() == 0:
            print("Seeding exercise library...")
            exercises = [
                ExerciseLibrary(
                    name="Gentle Neck Stretches",
                    description="Gently tilt your head toward each shoulder, holding for 10 seconds. Helps relieve tension headache pressure.",
                    body_area="Head / Neck",
                    difficulty="Beginner",
                    duration_seconds=60,
                    repetitions=5,
                    instructions=["Tilt head right", "Hold 10s", "Tilt head left", "Hold 10s"],
                    contraindications=["Recent neck injury", "Severe cervical pain"],
                    stop_conditions=["Sharp pain", "Dizziness"],
                    evidence_level="High",
                    review_status="approved"
                ),
                ExerciseLibrary(
                    name="Deep Breathing Exercises",
                    description="Inhale slowly through your nose for 4 seconds, hold for 4 seconds, and exhale for 6 seconds. Promotes relaxation.",
                    body_area="Systemic / Respiratory",
                    difficulty="Beginner",
                    duration_seconds=120,
                    repetitions=10,
                    instructions=["Breathe in 4s", "Hold 4s", "Breathe out 6s"],
                    contraindications=[],
                    stop_conditions=["Lightheadedness"],
                    evidence_level="High",
                    review_status="approved"
                ),
                ExerciseLibrary(
                    name="Shoulder Rolls",
                    description="Roll your shoulders backward in a circular motion to relieve stress and back muscle tightness.",
                    body_area="Shoulders / Back",
                    difficulty="Beginner",
                    duration_seconds=30,
                    repetitions=10,
                    instructions=["Roll backward circular"],
                    contraindications=["Acute shoulder dislocation"],
                    stop_conditions=["Severe shoulder pain"],
                    evidence_level="Moderate",
                    review_status="approved"
                )
            ]
            for ex in exercises:
                db.add(ex)
            db.commit()
            print("✅ Exercise Library successfully seeded!")

        # 4. Seed Complementary Care Options
        if db.query(ComplementaryOption).count() == 0:
            print("Seeding complementary care options...")
            options = [
                ComplementaryOption(
                    name="Ginger Root Infusion",
                    traditional_use="Used historically in Ayurveda to promote digestive thermal balance and ease nausea symptoms.",
                    possible_benefits=["Helps soothe mild nausea", "Promotes gastric comfort"],
                    possible_risks=["May cause mild heartburn if consumed in high quantities"],
                    contraindications=["Bleeding disorders", "Upcoming surgery"],
                    drug_interactions=["Anticoagulants / blood thinners"],
                    evidence_level="Moderate",
                    review_status="approved"
                ),
                ComplementaryOption(
                    name="Peppermint Oil Inhalation",
                    traditional_use="Used traditionally to relieve forehead pressure and soothe sinus discomfort.",
                    possible_benefits=["Relieves mild tension headache sensations", "Clears breathing pathways"],
                    possible_risks=["May cause local skin irritation if applied directly without dilution"],
                    contraindications=["Application near infant airways"],
                    drug_interactions=[],
                    evidence_level="Moderate",
                    review_status="approved"
                ),
                ComplementaryOption(
                    name="Warm Chamomile Compress",
                    traditional_use="Applied to forehead or back of neck to relieve stress and muscle tension.",
                    possible_benefits=["Induces relaxation", "Soothes localized tension"],
                    possible_risks=["Allergic reactions in individuals allergic to ragweed/daisies"],
                    contraindications=[],
                    drug_interactions=[],
                    evidence_level="Moderate",
                    review_status="approved"
                )
            ]
            for opt in options:
                db.add(opt)
            db.commit()
            print("✅ Complementary Care Options successfully seeded!")

        # 5. Seed Medication Catalog
        if db.query(MedicationCatalog).count() == 0:
            print("Seeding medication catalog...")
            meds = [
                MedicationCatalog(
                    generic_name="Paracetamol",
                    brand_names=["Calpol", "Crocin", "Tylenol"],
                    normalized_code="RxCUI-202284",
                    medicine_class="Analgesic / Antipyretic",
                    otc_or_prescription="otc",
                    warnings=["Do not exceed 4g daily to prevent hepatotoxicity"],
                    contraindications=["Severe hepatic impairment"],
                    side_effects=["Rare allergic reactions", "Liver enzyme elevation"],
                    interaction_metadata={"Alcohol": "Increases liver toxicity risk"}
                ),
                MedicationCatalog(
                    generic_name="Ibuprofen",
                    brand_names=["Advil", "Brufen", "Motrin"],
                    normalized_code="RxCUI-5640",
                    medicine_class="NSAID",
                    otc_or_prescription="otc",
                    warnings=["Take with food to minimize gastric irritation"],
                    contraindications=["Active peptic ulcer disease", "Severe renal impairment"],
                    side_effects=["Stomach discomfort", "Acid reflux", "Rare gastrointestinal bleeding"],
                    interaction_metadata={"Aspirin": "Increases bleeding risk"}
                ),
                MedicationCatalog(
                    generic_name="Cetirizine",
                    brand_names=["Zyrtec", "Okacet"],
                    normalized_code="RxCUI-20610",
                    medicine_class="Second-generation antihistamine",
                    otc_or_prescription="otc",
                    warnings=["May cause mild drowsiness in some individuals"],
                    contraindications=["Hypersensitivity to hydroxyzine"],
                    side_effects=["Dry mouth", "Somnolence", "Fatigue"],
                    interaction_metadata={"Sedatives": "Enhances central nervous system depression"}
                )
            ]
            for m in meds:
                db.add(m)
            db.commit()
            print("✅ Medication Catalog successfully seeded!")

    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
