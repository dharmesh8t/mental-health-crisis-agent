"""Resource Finder Agent for Crisis Support System.

This agent identifies and provides relevant mental health resources
based on user needs, location, and crisis type.
"""

import json
from typing import Dict, Any, List, Optional
from core.gemini_connector import GeminiConnector
from core.memory_service import CrisisMemoryService


class ResourceFinderAgent:
    """Agent for finding and recommending mental health resources."""

    # Crisis resources database
    CRISIS_RESOURCES = {
        "emergency": {
            "hotlines": [
                {
                    "name": "National Suicide Prevention Lifeline",
                    "number": "988",
                    "country": "USA",
                    "available": "24/7",
                    "languages": "English, Spanish"
                },
                {
                    "name": "Crisis Text Line",
                    "code": "Text HOME to 741741",
                    "country": "USA",
                    "available": "24/7",
                    "type": "SMS"
                },
                {
                    "name": "iCall",
                    "number": "9152987821",
                    "country": "India",
                    "available": "24/7",
                    "languages": "Hindi, English"
                }
            ],
            "action": "IMMEDIATE"
        },
        "therapy": {
            "types": [
                "Cognitive Behavioral Therapy (CBT)",
                "Dialectical Behavior Therapy (DBT)",
                "Psychodynamic Therapy",
                "Acceptance and Commitment Therapy (ACT)"
            ],
            "delivery_methods": [
                "In-person",
                "Telehealth",
                "Group therapy",
                "Individual therapy"
            ]
        },
        "support_groups": {
            "types": [
                "Alcoholics Anonymous (AA)",
                "Narcotics Anonymous (NA)",
                "Depression and Bipolar Support Alliance (DBSA)",
                "NAMI Support Groups",
                "Grief Support Groups",
                "Anxiety Support Groups"
            ],
            "formats": ["In-person", "Online", "Hybrid"]
        },
        "apps_platforms": {
            "mental_health": [
                {"name": "Headspace", "type": "Meditation & mindfulness"},
                {"name": "Calm", "type": "Meditation & sleep"},
                {"name": "Talkspace", "type": "Online therapy"},
                {"name": "BetterHelp", "type": "Online counseling"},
                {"name": "Insight Timer", "type": "Free meditation"}
            ]
        }
    }

    def __init__(self, gemini_connector: GeminiConnector, memory_service: CrisisMemoryService):
        """Initialize the Resource Finder Agent.

        Args:
            gemini_connector: Connection to Gemini API
            memory_service: Service for managing crisis memory
        """
        self.gemini = gemini_connector
        self.memory = memory_service

    def find_resources(self, session_id: str, crisis_level: str, needs: Optional[List[str]] = None) -> Dict[str, Any]:
        """Find and provide relevant mental health resources.

        Args:
            session_id: Unique session identifier
            crisis_level: Level of crisis (low, medium, high, emergency)
            needs: Specific needs or preferences

        Returns:
            Dictionary with recommended resources
        """
        try:
            # Extract user needs from conversation
            if needs is None:
                needs = self._extract_needs(session_id)

            # Get appropriate resources
            resources = self._get_resources_for_level(crisis_level, needs)

            # Generate personalized resource recommendations
            prompt = f"""Based on this crisis situation at {crisis_level} level with needs: {needs},
            provide empathetic recommendations for mental health resources.
            
            Available resources: {json.dumps(resources, indent=2)}
            
            Provide:
            1. Most relevant resources for immediate needs
            2. How to access each resource
            3. What to expect when contacting
            4. Additional resources for longer-term support
            
            Be specific and actionable. Prioritize accessibility."""

            response = self.gemini.call_gemini(prompt)

            # Store in memory
            self.memory.add_message(session_id, "assistant", response)
            self.memory.add_resource_recommendations(session_id, resources, needs)

            result = {
                "agent": "resource_finder",
                "response": response,
                "resources": resources,
                "identified_needs": needs,
                "status": "success"
            }

            return result

        except Exception as e:
            print(f"Error in resource finder: {str(e)}")
            return {
                "agent": "resource_finder",
                "response": self._get_fallback_resources(crisis_level),
                "status": "fallback",
                "error": str(e)
            }

    def _extract_needs(self, session_id: str) -> List[str]:
        """Extract user needs from conversation history.

        Args:
            session_id: Session identifier

        Returns:
            List of identified needs
        """
        conversation = self.memory.get_conversation(session_id)
        user_messages = [msg["content"] for msg in conversation if msg.get("role") == "user"]

        # Keywords to identify needs
        need_keywords = {
            "therapy": ["therapist", "counseling", "talk"],
            "medication": ["medication", "pills", "treatment"],
            "peer_support": ["group", "others", "community", "support"],
            "crisis": ["emergency", "danger", "harm", "suicidal"]
        }

        identified_needs = []
        combined_text = " ".join(user_messages).lower()

        for need_type, keywords in need_keywords.items():
            if any(keyword in combined_text for keyword in keywords):
                identified_needs.append(need_type)

        return identified_needs if identified_needs else ["general_support"]

    def _get_resources_for_level(self, crisis_level: str, needs: List[str]) -> Dict[str, Any]:
        """Get resources appropriate for crisis level and needs.

        Args:
            crisis_level: Level of crisis
            needs: List of identified needs

        Returns:
            Dictionary of relevant resources
        """
        resources = {}

        if crisis_level == "emergency":
            resources["immediate"] = self.CRISIS_RESOURCES["emergency"]
            resources["hotlines"] = self.CRISIS_RESOURCES["emergency"]["hotlines"]
        elif crisis_level == "high":
            resources["hotlines"] = self.CRISIS_RESOURCES["emergency"]["hotlines"]
            resources["therapy"] = self.CRISIS_RESOURCES["therapy"]
        elif crisis_level == "medium":
            resources["therapy"] = self.CRISIS_RESOURCES["therapy"]
            resources["support_groups"] = self.CRISIS_RESOURCES["support_groups"]
        else:
            resources["apps"] = self.CRISIS_RESOURCES["apps_platforms"]
            resources["support_groups"] = self.CRISIS_RESOURCES["support_groups"]

        # Add needs-specific resources
        for need in needs:
            if need == "peer_support":
                resources["support_groups"] = self.CRISIS_RESOURCES["support_groups"]
            elif need == "therapy":
                resources["therapy"] = self.CRISIS_RESOURCES["therapy"]

        return resources

    def _get_fallback_resources(self, crisis_level: str) -> str:
        """Provide fallback resources if API fails.

        Args:
            crisis_level: Level of crisis

        Returns:
            Fallback resource information
        """
        if crisis_level in ["high", "emergency"]:
            return """Immediate resources available:
            
            National Suicide Prevention Lifeline: 988 (call or text)
            Crisis Text Line: Text HOME to 741741
            
            If you're in immediate danger:
            - Call 911 (emergency)
            - Go to nearest emergency room
            - Tell someone you trust right now
            
            You can also reach:
            - Crisis Text Line: Text HOME to 741741
            - International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/"""
        else:
            return """Resources for ongoing support:
            
            Therapy and Counseling:
            - BetterHelp: Online counseling platform
            - Talkspace: Therapy via app
            - SAMHSA National Helpline: 1-800-662-4357 (free, confidential)
            
            Support Groups:
            - NAMI: https://www.nami.org/support-groups
            - DBSA: https://www.dbsalliance.org/
            
            Mindfulness and Wellness:
            - Headspace or Calm for meditation
            - Insight Timer for free meditation
            - Your local community mental health center"""
