"""Safety Router Agent for Crisis Support System.

This agent routes high-risk situations to emergency services,
manages safety protocols, and coordinates immediate interventions.
"""

import json
from typing import Dict, Any, Optional
from datetime import datetime
from core.gemini_connector import GeminiConnector
from core.memory_service import CrisisMemoryService


class SafetyRouterAgent:
    """Agent for managing emergency routing and safety protocols."""

    # Emergency indicators that require immediate routing
    EMERGENCY_INDICATORS = [
        "suicidal",
        "suicide",
        "kill myself",
        "take my life",
        "self-harm",
        "hurt myself",
        "cutting",
        "overdose",
        "poison",
        "noose",
        "gun",
        "going to die",
        "want to die",
        "don't want to live"
    ]

    EMERGENCY_SERVICES = {
        "immediate": {
            "911": {
                "location": "USA",
                "use_case": "Immediate life threat, active self-harm",
                "description": "Emergency services dispatch"
            },
            "988": {
                "location": "USA",
                "use_case": "Suicidal thoughts, crisis intervention",
                "description": "National Suicide Prevention Lifeline",
                "available": "24/7"
            }
        },
        "hospital_equivalent": {
            "emergency_room": {
                "use_case": "Medical emergency, acute psychiatric crisis",
                "when": "When immediate threat exists but not on phone"
            },
            "psychiatric_hospital": {
                "use_case": "Severe mental health emergency",
                "when": "For stabilization and intensive treatment"
            }
        }
    }

    def __init__(self, gemini_connector: GeminiConnector, memory_service: CrisisMemoryService):
        """Initialize the Safety Router Agent.

        Args:
            gemini_connector: Connection to Gemini API
            memory_service: Service for managing crisis memory
        """
        self.gemini = gemini_connector
        self.memory = memory_service

    def assess_and_route(self, session_id: str, assessment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess safety risk and route appropriately.

        Args:
            session_id: Unique session identifier
            assessment_data: Crisis assessment data

        Returns:
            Dictionary with routing decision and actions
        """
        try:
            crisis_level = assessment_data.get("crisis_level", "low")
            user_message = assessment_data.get("user_message", "")

            # Check for emergency indicators
            emergency_detected = self._detect_emergency(user_message, crisis_level)

            if emergency_detected:
                return self._handle_emergency(session_id, user_message, assessment_data)
            else:
                return self._handle_non_emergency(session_id, crisis_level)

        except Exception as e:
            print(f"Error in safety routing: {str(e)}")
            return {
                "agent": "safety_router",
                "routing": "FALLBACK_EMERGENCY",
                "message": "When in doubt, reach out to emergency services",
                "status": "error",
                "error": str(e)
            }

    def _detect_emergency(self, user_message: str, crisis_level: str) -> bool:
        """Detect emergency indicators in user message.

        Args:
            user_message: User's message text
            crisis_level: Current crisis level assessment

        Returns:
            True if emergency detected, False otherwise
        """
        message_lower = user_message.lower()

        # Check for explicit indicators
        for indicator in self.EMERGENCY_INDICATORS:
            if indicator in message_lower:
                return True

        # High/emergency level also requires routing
        if crisis_level in ["high", "emergency"]:
            # Check for active planning language
            planning_keywords = ["plan", "ready", "decided", "going to", "when", "where", "how"]
            if any(keyword in message_lower for keyword in planning_keywords):
                return True

        return False

    def _handle_emergency(self, session_id: str, user_message: str, assessment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle emergency situation.

        Args:
            session_id: Session identifier
            user_message: User's message
            assessment_data: Assessment data

        Returns:
            Emergency handling response
        """
        # Log emergency incident
        self.memory.add_emergency_flag(session_id, {
            "detected_at": datetime.now().isoformat(),
            "indicator_message": user_message,
            "assessment": assessment_data
        })

        # Generate emergency response
        emergency_response = self._generate_emergency_response(user_message)

        # Store emergency response in memory
        self.memory.add_message(session_id, "assistant", emergency_response)

        result = {
            "agent": "safety_router",
            "routing": "EMERGENCY_SERVICES",
            "crisis_level": "emergency",
            "immediate_actions": [
                "CALL 988 or 911 immediately",
                "Tell someone you trust right now",
                "Go to nearest emergency room if safe to do so",
                "Remove access to means of self-harm"
            ],
            "response": emergency_response,
            "status": "emergency_escalated"
        }

        return result

    def _handle_non_emergency(self, session_id: str, crisis_level: str) -> Dict[str, Any]:
        """Handle non-emergency routing.

        Args:
            session_id: Session identifier
            crisis_level: Crisis level

        Returns:
            Non-emergency routing response
        """
        routing_path = "deescalation" if crisis_level == "low" else "professional_support"

        result = {
            "agent": "safety_router",
            "routing": routing_path.upper(),
            "crisis_level": crisis_level,
            "next_agent": "deescalation" if crisis_level == "low" else "resource_finder",
            "actions": self._get_actions_for_level(crisis_level),
            "status": "routed"
        }

        return result

    def _generate_emergency_response(self, user_message: str) -> str:
        """Generate emergency response message.

        Args:
            user_message: User's concerning message

        Returns:
            Emergency response text
        """
        return f"""I hear that you're going through something very serious right now. Your safety is the top priority.

PLEASE REACH OUT FOR IMMEDIATE HELP:

🚨 CALL OR TEXT 988 (Suicide & Crisis Lifeline)
   Available 24/7 - Free and confidential
   Crisis Counselors available right now

🚨 CALL 911
   If you're in immediate danger
   Operator will send help to your location

🚨 GO TO NEAREST EMERGENCY ROOM
   Tell staff you're having a mental health crisis
   They will provide immediate care

YOU ARE NOT ALONE. Help is available RIGHT NOW.
Your life has value. This is temporary. Help works.

If you reach out to one of these services:
- They understand what you're experiencing
- They are trained to help
- They have resources that can help immediately
- It's confidential and free

Please take action now. You deserve support."""

    def _get_actions_for_level(self, crisis_level: str) -> list:
        """Get recommended actions for crisis level.

        Args:
            crisis_level: Current crisis level

        Returns:
            List of recommended actions
        """
        actions = {
            "low": [
                "Engage in coping strategies",
                "Practice self-care activities",
                "Reach out to trusted friend or family",
                "Schedule therapy if needed"
            ],
            "medium": [
                "Contact mental health professional",
                "Reach out to support network",
                "Use crisis resources",
                "Develop safety plan"
            ],
            "high": [
                "CONTACT 988 OR CRISIS HOTLINE",
                "Reach out to mental health professional immediately",
                "Tell someone you trust about your feelings",
                "Consider emergency services if thoughts worsen"
            ]
        }
        return actions.get(crisis_level, actions["low"])
