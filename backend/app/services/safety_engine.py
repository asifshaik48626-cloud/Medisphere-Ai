from typing import Dict, Any, List, Tuple

class SafetyEngine:
    # Rule definitions
    EMERGENCY_KEYWORDS = {
        "chest pain", "tightness in chest", "shortness of breath", "breathing difficulty",
        "difficulty breathing", "unconscious", "unconsciousness", "severe bleeding",
        "stroke symptoms", "slurred speech", "numbness in face", "loss of vision",
        "anaphylaxis", "severe allergic reaction", "throat swelling", "poisoning",
        "severe head injury", "coughing blood", "vomiting blood"
    }
    
    URGENT_KEYWORDS = {
        "high fever", "severe stomach pain", "sudden severe headache", "dizziness",
        "unable to keep fluids down", "confusion", "stiff neck", "moderate breathing difficulty"
    }

    @classmethod
    def evaluate(cls, patient_info: Dict[str, Any], symptoms: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluates the intake session and symptoms to determine the safety/urgency profile.
        
        patient_info fields:
            - age: int
            - pregnancy_status: bool
            - allergies: List[str]
            - existing_conditions: List[str]
        
        symptoms fields:
            - symptom_name: str
            - severity: int (1-10)
            - duration_days: int
            - associated_symptoms: List[str]
        """
        urgency_level = "monitor"  # Default lowest
        red_flags = []
        recommendations_blocked = False
        requires_professional_review = True
        escalation_message = ""
        required_professional_type = "Doctor"

        # 1. Check for Emergency Signs
        is_emergency, emergency_reason = cls._check_emergency_rules(patient_info, symptoms)
        if is_emergency:
            urgency_level = "emergency"
            recommendations_blocked = True
            requires_professional_review = True
            required_professional_type = "Emergency Physician"
            escalation_message = f"EMERGENCY WARNING: {emergency_reason}. Please seek immediate emergency medical care or call emergency services (like 112/911) immediately."
            
            red_flags.append({
                "rule_code": "RF_EMERGENCY",
                "title": "Immediate Emergency Action Required",
                "description": emergency_reason,
                "severity": "critical",
                "evidence": {"patient_info": patient_info, "triggering_symptoms": symptoms}
            })
            
            return {
                "urgency_level": urgency_level,
                "recommendations_blocked": recommendations_blocked,
                "requires_professional_review": requires_professional_review,
                "required_professional_type": required_professional_type,
                "escalation_message": escalation_message,
                "red_flags": red_flags,
                "rule_version": "1.0.0"
            }

        # 2. Check for Urgent Signs
        is_urgent, urgent_reason = cls._check_urgent_rules(patient_info, symptoms)
        if is_urgent:
            urgency_level = "urgent"
            recommendations_blocked = False  # Not fully blocked, but restricted
            required_professional_type = "General Practitioner / Urgent Care"
            escalation_message = f"URGENT CLINICAL WARNING: {urgent_reason}. We recommend consulting a healthcare professional today."
            
            red_flags.append({
                "rule_code": "RF_URGENT",
                "title": "Urgent Clinical Attention Needed",
                "description": urgent_reason,
                "severity": "high",
                "evidence": {"triggering_symptoms": symptoms}
            })
        
        # 3. Check for same-day consultation signs
        elif cls._check_same_day_rules(patient_info, symptoms):
            urgency_level = "same-day"
            escalation_message = "Recommendation: Consult with a doctor within the next 24 hours."
            
        # 4. Check for routine consultation
        elif cls._check_routine_rules(patient_info, symptoms):
            urgency_level = "routine"
            escalation_message = "Recommendation: Schedule a routine consultation with a doctor."
            
        else:
            urgency_level = "monitor"
            escalation_message = "Recommendation: Continue monitoring symptoms and practice self-care. Consult a doctor if symptoms worsen."

        return {
            "urgency_level": urgency_level,
            "recommendations_blocked": recommendations_blocked,
            "requires_professional_review": requires_professional_review,
            "required_professional_type": required_professional_type,
            "escalation_message": escalation_message,
            "red_flags": red_flags,
            "rule_version": "1.0.0"
        }

    @classmethod
    def _check_emergency_rules(cls, patient_info: Dict[str, Any], symptoms: List[Dict[str, Any]]) -> Tuple[bool, str]:
        # Rule 1.1: Direct keywords indicating life-threatening emergency
        for sym in symptoms:
            name = sym.get("symptom_name", "").lower()
            if any(keyword in name for keyword in cls.EMERGENCY_KEYWORDS):
                return True, f"Detected warning sign: '{sym.get('symptom_name')}' which indicates a potentially life-threatening emergency."
            
            # Rule 1.2: Extreme severity (e.g. 10/10) with fast onset
            if sym.get("severity", 0) >= 10:
                return True, f"Detected extreme severity pain ({sym.get('severity')}/10)."
            
        # Rule 1.3: Pregnancy with high blood pressure or breathing difficulty
        if patient_info.get("pregnancy_status", False):
            for sym in symptoms:
                name = sym.get("symptom_name", "").lower()
                if "fever" in name or "breathing" in name or "bleeding" in name or "severe abdominal pain" in name:
                    return True, "Pregnancy with acute warning symptoms (fever/breathing/bleeding/severe pain)."

        # Rule 1.4: Extreme age warning (newborn < 3 months with fever)
        age = patient_info.get("age", 30)
        if age is not None and age <= 0.25:  # Less than 3 months
            for sym in symptoms:
                if "fever" in sym.get("symptom_name", "").lower():
                    return True, "Infant under 3 months presenting with a fever requires immediate emergency assessment."

        return False, ""

    @classmethod
    def _check_urgent_rules(cls, patient_info: Dict[str, Any], symptoms: List[Dict[str, Any]]) -> Tuple[bool, str]:
        for sym in symptoms:
            name = sym.get("symptom_name", "").lower()
            if any(keyword in name for keyword in cls.URGENT_KEYWORDS):
                return True, f"Detected urgent clinical symptom: '{sym.get('symptom_name')}'."
            
            # Severity >= 7 is classified as urgent
            if sym.get("severity", 0) >= 7:
                return True, f"Detected high symptom severity ({sym.get('severity')}/10)."
            
            # High fever (temp representation in text or value)
            if "fever" in name and sym.get("severity", 0) >= 5:
                return True, "Moderate to high-grade fever detected."

        return False, ""

    @classmethod
    def _check_same_day_rules(cls, patient_info: Dict[str, Any], symptoms: List[Dict[str, Any]]) -> bool:
        # Duration of symptom is moderate, and severity is medium
        for sym in symptoms:
            if sym.get("severity", 0) >= 5:
                return True
            if sym.get("duration_days", 0) > 3:
                return True
        return False

    @classmethod
    def _check_routine_rules(cls, patient_info: Dict[str, Any], symptoms: List[Dict[str, Any]]) -> bool:
        # Long-duration low-severity symptoms
        for sym in symptoms:
            if sym.get("duration_days", 0) >= 7:
                return True
        return False
