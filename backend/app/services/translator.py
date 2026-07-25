from typing import Dict

# Simple Static Translation Dictionary for Demonstrating Language Support
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "es": {
        "What symptoms are you experiencing?": "¿Qué síntomas está experimentando?",
        "Please describe your headache location.": "Por favor, describa la ubicación de su dolor de cabeza.",
        "What is your temperature?": "¿Cuál es su temperatura?",
        "Do you have chest pain?": "¿Tiene dolor de pecho?",
        "Emergency warning signs detected.": "Se detectaron signos de advertencia de emergencia.",
        "Seeded Patient authenticated successfully!": "¡El paciente sembrado se autenticó con éxito!"
    },
    "hi": {
        "What symptoms are you experiencing?": "आप किन लक्षणों का अनुभव कर रहे हैं?",
        "Please describe your headache location.": "कृपया अपने सिरदर्द के स्थान का वर्णन करें।",
        "What is your temperature?": "आपका तापमान क्या है?",
        "Do you have chest pain?": "क्या आपके सीने में दर्द है?",
        "Emergency warning signs detected.": "आपातकालीन चेतावनी संकेत पाए गए।",
        "Seeded Patient authenticated successfully!": "सीडेड रोगी सफलतापूर्वक प्रमाणित!"
    },
    "te": {
        "What symptoms are you experiencing?": "మీరు ఏ లక్షణాలను అనుభవిస్తున్నారు?",
        "Please describe your headache location.": "దయచేసి మీ తలనొప్పి ఉన్న ప్రదేశాన్ని వివరించండి.",
        "What is your temperature?": "మీ ఉష్ణోగ్రత ఎంత?",
        "Do you have chest pain?": "మీకు ఛాతీ నొప్పి ఉందా?",
        "Emergency warning signs detected.": "అత్యవసర హెచ్చరిక సంకేతాలు కనుగొనబడ్డాయి.",
        "Seeded Patient authenticated successfully!": "సీడెడ్ పేషెంట్ విజయవంతంగా ప్రామాణీకరించబడింది!"
    }
}

class MedicalTranslator:
    @classmethod
    def identify_language(cls, text: str) -> str:
        """
        Simple heuristic language identification for demo purposes.
        """
        text_lower = text.lower()
        # Heuristics for Spanish
        if any(word in text_lower for word in ["que", "dolor", "tengo", "cabeza"]):
            return "es"
        # Heuristics for Hindi (characters)
        elif any(char in text for char in ["क", "ख", "ग", "घ", "त", "द"]):
            return "hi"
        # Heuristics for Telugu (characters)
        elif any(char in text for char in ["అ", "ఆ", "క", "ఖ", "గ", "ఘ"]):
            return "te"
        return "en"

    @classmethod
    def translate(cls, text: str, target_lang: str) -> str:
        """
        Translates text to the target language, falling back to English.
        """
        if target_lang == "en":
            return text
        lang_dict = TRANSLATIONS.get(target_lang, {})
        translated = lang_dict.get(text, text)  # Fallback to original text if match not found
        return translated
