from typing import List, Dict, Any

# Mock Guideline Database
GUIDELINE_DATABASE = [
    {
        "source": "WHO Guidelines on Fever Triage (2024)",
        "content": "Pediatric patients under 3 months presenting with a body temperature exceeding 38.0°C (100.4°F) require immediate emergency department referral for neonatal sepsis workup.",
        "category": "Fever",
        "evidence_level": "Grade A"
    },
    {
        "source": "CDC Clinical Protocol for Acute Fever (2023)",
        "content": "Fever accompanied by meningeal signs (stiff neck, photophobia, confusion) is highly suggestive of acute meningitis. Initiate emergency protocols immediately.",
        "category": "Fever",
        "evidence_level": "Grade A"
    },
    {
        "source": "IHS Guidelines for Acute Migraine and Headache (2023)",
        "content": "Sudden onset headache reaching maximum intensity within 60 seconds (thunderclap headache) is a red flag for subarachnoid hemorrhage. Do not delay emergency imaging.",
        "category": "Headache",
        "evidence_level": "Grade A"
    },
    {
        "source": "American Academy of Family Physicians (AAFP) Headache Review (2022)",
        "content": "Tension-type headaches are typically bilateral, pressing or tightening in quality, and of mild to moderate intensity. They do not worsen with physical activity.",
        "category": "Headache",
        "evidence_level": "Grade B"
    }
]

class GuidelineRetrieval:
    @classmethod
    def retrieve(cls, query: str) -> List[Dict[str, Any]]:
        """
        Retrieves matching guidelines based on text matching.
        """
        query_lower = query.lower()
        matches = []
        for doc in GUIDELINE_DATABASE:
            # Match by category or keywords in content
            if doc["category"].lower() in query_lower or any(word in doc["content"].lower() for word in query_lower.split()):
                matches.append(doc)
        
        # Fallback to general documents if no specific match
        if not matches:
            return GUIDELINE_DATABASE[:1]
            
        return matches
