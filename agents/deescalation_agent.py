"""De-escalation Agent for Crisis Support System.

This agent provides de-escalation strategies and coping techniques
to help users manage their emotional state during crisis situations.
"""

import json
from typing import Dict, Any, Optional
from core.gemini_connector import GeminiConnector
from core.memory_service import CrisisMemoryService


class DeescalationAgent:
    """Agent for providing de-escalation and coping strategies."""

    # De-escalation strategies organized by crisis level
    COPING_STRATEGIES = {
        "grounding": {
            "name": "Grounding Techniques (5-4-3-2-1 Method)",
            "description": "Engage your senses to bring yourself to the present moment",
            "steps": [
                "Notice 5 things you can see",
                "Notice 4 things you can touch",
                "Notice 3 things you can hear",
                "Notice 2 things you can smell",
                "Notice 1 thing you can taste"
            ]
        },
        "breathing": {
            "name": "Box Breathing Technique",
            "description": "Calm your nervous system with controlled breathing",
            "steps": [
                "Inhale for 4 counts",
                "Hold for 4 counts",
                "Exhale for 4 counts",
                "Hold for 4 counts",
                "Repeat 5-10 times"
            ]
        },
        "muscle_relaxation": {
            "name": "Progressive Muscle Relaxation",
            "description": "Reduce physical tension through systematic muscle relaxation",
            "steps": [
                "Tense your toes for 5 seconds, then release",
                "Tense your legs for 5 seconds, then release",
                "Tense your abdomen for 5 seconds, then release",
                "Tense your chest for 5 seconds, then release",
                "Continue up through arms, shoulders, and face"
            ]
        },
        "positive_affirmations": {
            "name": "Positive Affirmations",
            "description": "Build resilience through positive self-talk",
            "affirmations": [
                "This feeling is temporary and will pass",
                "I have survived difficult moments before",
                "I am stronger than I think",
                "I deserve support and compassion",
                "I am taking positive steps toward healing"
            ]
        },
        "distraction": {
            "name": "Healthy Distraction Techniques",
            "description": "Redirect attention to safe, engaging activities",
            "activities": [
                "Listen to calming music or nature sounds",
                "Watch a favorite movie or show",
                "Read a book or article",
                "Go for a walk in nature",
                "Practice a hobby or creative activity"
            ]
        }
    }

    def __init__(self, gemini_connector: GeminiConnector, memory_service: CrisisMemoryService):
        """Initialize the De-escalation Agent.

        Args:
            gemini_connector: Connection to Gemini API
            memory_service: Service for managing crisis memory
        """
        self.gemini = gemini_connector
        self.memory = memory_service

    def provide_deescalation_strategies(self, session_id: str, crisis_level: str) -> Dict[str, Any]:
        """Provide de-escalation strategies tailored to crisis level.

        Args:
            session_id: Unique session identifier
            crisis_level: Level of crisis (low, medium, high)

        Returns:
            Dictionary with de-escalation strategies and support
        """
        try:
            # Get conversation history
            conversation = self.memory.get_conversation(session_id)
            user_messages = [msg for msg in conversation if msg.get("role") == "user"]
            latest_concern = user_messages[-1].get("content", "") if user_messages else ""

            # Select appropriate strategies based on crisis level
            strategies = self._select_strategies_by_level(crisis_level)

            # Generate personalized de-escalation response
            prompt = f"""Based on this crisis situation at {crisis_level} level, provide empathetic de-escalation support.
            User's concern: {latest_concern}
            Crisis level: {crisis_level}
            
            Provide:
            1. Immediate validation of their feelings
            2. 2-3 recommended coping techniques from: {list(strategies.keys())}
            3. Step-by-step guidance for one technique
            4. Encouragement to reach out for professional help
            
            Keep response concise, supportive, and actionable. Use simple language."""

            response = self.gemini.call_gemini(prompt)

            # Store response in memory
            self.memory.add_message(session_id, "assistant", response)

            result = {
                "agent": "deescalation",
                "response": response,
                "strategies": strategies,
                "crisis_level": crisis_level,
                "status": "success"
            }

            return result

        except Exception as e:
            print(f"Error in de-escalation: {str(e)}")
            return {
                "agent": "deescalation",
                "response": self._get_fallback_response(crisis_level),
                "status": "fallback",
                "error": str(e)
            }

    def _select_strategies_by_level(self, crisis_level: str) -> Dict[str, Any]:
        """Select appropriate coping strategies based on crisis level.

        Args:
            crisis_level: Level of crisis (low, medium, high)

        Returns:
            Dictionary of recommended strategies
        """
        if crisis_level == "low":
            return {
                "breathing": self.COPING_STRATEGIES["breathing"],
                "distraction": self.COPING_STRATEGIES["distraction"],
                "positive_affirmations": self.COPING_STRATEGIES["positive_affirmations"]
            }
        elif crisis_level == "medium":
            return {
                "grounding": self.COPING_STRATEGIES["grounding"],
                "breathing": self.COPING_STRATEGIES["breathing"],
                "muscle_relaxation": self.COPING_STRATEGIES["muscle_relaxation"]
            }
        else:  # high or emergency
            return {
                "grounding": self.COPING_STRATEGIES["grounding"],
                "breathing": self.COPING_STRATEGIES["breathing"],
                "muscle_relaxation": self.COPING_STRATEGIES["muscle_relaxation"]
            }

    def _get_fallback_response(self, crisis_level: str) -> str:
        """Provide fallback de-escalation response if API fails.

        Args:
            crisis_level: Level of crisis

        Returns:
            Supportive fallback message
        """
        if crisis_level == "high" or crisis_level == "emergency":
            return """I understand you're in crisis. Please reach out immediately:
            - Call 988 (Suicide & Crisis Lifeline) in the US
            - Call 911 if you're in immediate danger
            - Go to your nearest emergency room
            Your life matters. Help is available right now."""
        else:
            return """I'm here to help you through this. Let's try a simple breathing exercise:
            1. Breathe in slowly for 4 counts
            2. Hold for 4 counts
            3. Exhale for 4 counts
            4. Hold for 4 counts
            Repeat this 5-10 times. You're doing well by reaching out."""
