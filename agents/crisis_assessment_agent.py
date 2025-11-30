"""Crisis Assessment Agent - Analyzes severity and initial triage."""
from core.gemini_connector import GeminiConnector
from core.memory_service import CrisisMemoryService

class CrisisAssessmentAgent:
    """Assesses crisis severity and determines routing."""
    
    def __init__(self, gemini_connector: GeminiConnector, memory: CrisisMemoryService):
        self.gemini = gemini_connector
        self.memory = memory
        self.name = "Crisis Assessment Agent"
    
    def assess(self, user_id: str, user_message: str) -> dict:
        """Assess crisis and return severity classification."""
        assessment = self.gemini.assess_crisis_severity(user_message)
        self.memory.update_crisis_level(user_id, assessment.get('severity_level'))
        self.memory.sessions[user_id]['symptoms'] = assessment.get('key_symptoms', [])
        
        return {
            "agent": self.name,
            "severity_level": assessment.get('severity_level'),
            "key_symptoms": assessment.get('key_symptoms'),
            "risk_factors": assessment.get('risk_factors')
        }
