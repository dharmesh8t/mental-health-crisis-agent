"""Follow-up and Memory Agent for Crisis Support System.

This agent manages follow-up interactions, tracks recovery progress,
and helps prevent relapse through personalized recovery plans.
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from core.gemini_connector import GeminiConnector
from core.memory_service import CrisisMemoryService


class FollowupMemoryAgent:
    """Agent for managing follow-ups and long-term recovery tracking."""

    # Follow-up schedule (in days)
    FOLLOWUP_SCHEDULE = {
        "immediate": 0,  # Same day
        "short_term": 1,  # 24 hours
        "week_one": 3,  # 3 days
        "week_two": 7,  # 1 week
        "month": 14  # 2 weeks
    }

    # Recovery plan components
    RECOVERY_PLAN_COMPONENTS = {
        "triggers": "Identify personal warning signs and triggers",
        "coping_skills": "Develop and practice healthy coping mechanisms",
        "support_system": "Build and maintain support network",
        "professional_help": "Schedule regular therapy/counseling",
        "lifestyle": "Maintain healthy habits (sleep, exercise, nutrition)",
        "emergency_protocol": "Clear plan for crisis situations",
        "medication_adherence": "Take medications as prescribed",
        "self_monitoring": "Regular check-ins on mental health status"
    }

    def __init__(self, gemini_connector: GeminiConnector, memory_service: CrisisMemoryService):
        """Initialize the Follow-up Memory Agent.

        Args:
            gemini_connector: Connection to Gemini API
            memory_service: Service for managing crisis memory
        """
        self.gemini = gemini_connector
        self.memory = memory_service

    def create_recovery_plan(self, session_id: str, assessment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a personalized recovery plan.

        Args:
            session_id: Unique session identifier
            assessment_data: Crisis assessment and intervention data

        Returns:
            Dictionary with recovery plan
        """
        try:
            # Get conversation context
            conversation = self.memory.get_conversation(session_id)
            user_messages = [msg["content"] for msg in conversation if msg.get("role") == "user"]

            # Generate personalized recovery plan
            prompt = f"""Based on this crisis interaction and recovery needs, create a detailed recovery plan.
            
            Assessment data: {json.dumps(assessment_data, indent=2)}
            Conversation context: {' '.join(user_messages[-3:])}
            
            Create a recovery plan that includes:
            1. Specific triggers and warning signs identified
            2. Personalized coping strategies
            3. Support system recommendations
            4. Professional help suggestions
            5. Daily/weekly goals for recovery
            6. Relapse prevention strategies
            7. Emergency contacts and protocols
            
            Make it specific, actionable, and compassionate."""

            response = self.gemini.call_gemini(prompt)

            # Store recovery plan
            recovery_plan = {
                "created_at": datetime.now().isoformat(),
                "plan": response,
                "components": self.RECOVERY_PLAN_COMPONENTS,
                "followup_schedule": self.FOLLOWUP_SCHEDULE
            }

            self.memory.add_recovery_plan(session_id, recovery_plan)
            self.memory.add_message(session_id, "assistant", response)

            result = {
                "agent": "followup_memory",
                "recovery_plan": recovery_plan,
                "response": response,
                "status": "plan_created"
            }

            return result

        except Exception as e:
            print(f"Error creating recovery plan: {str(e)}")
            return {
                "agent": "followup_memory",
                "recovery_plan": self._get_fallback_recovery_plan(),
                "status": "fallback",
                "error": str(e)
            }

    def schedule_followup(self, session_id: str, crisis_level: str) -> Dict[str, Any]:
        """Schedule appropriate follow-up interventions.

        Args:
            session_id: Session identifier
            crisis_level: Level of crisis

        Returns:
            Dictionary with follow-up schedule
        """
        try:
            now = datetime.now()
            followup_times = {}

            if crisis_level == "emergency":
                # Intensive follow-up for emergencies
                followup_times["immediate"] = now.isoformat()
                followup_times["short_term"] = (now + timedelta(days=self.FOLLOWUP_SCHEDULE["short_term"])).isoformat()
                followup_times["week_one"] = (now + timedelta(days=self.FOLLOWUP_SCHEDULE["week_one"])).isoformat()
                followup_times["week_two"] = (now + timedelta(days=self.FOLLOWUP_SCHEDULE["week_two"])).isoformat()
            elif crisis_level == "high":
                # Regular follow-up for high crisis
                followup_times["short_term"] = (now + timedelta(days=self.FOLLOWUP_SCHEDULE["short_term"])).isoformat()
                followup_times["week_one"] = (now + timedelta(days=self.FOLLOWUP_SCHEDULE["week_one"])).isoformat()
                followup_times["week_two"] = (now + timedelta(days=self.FOLLOWUP_SCHEDULE["week_two"])).isoformat()
            else:
                # Standard follow-up
                followup_times["week_one"] = (now + timedelta(days=self.FOLLOWUP_SCHEDULE["week_one"])).isoformat()
                followup_times["month"] = (now + timedelta(days=self.FOLLOWUP_SCHEDULE["month"])).isoformat()

            # Store follow-up schedule
            self.memory.add_followup_schedule(session_id, followup_times)

            result = {
                "agent": "followup_memory",
                "followup_schedule": followup_times,
                "crisis_level": crisis_level,
                "status": "scheduled"
            }

            return result

        except Exception as e:
            print(f"Error scheduling follow-up: {str(e)}")
            return {
                "agent": "followup_memory",
                "status": "error",
                "error": str(e)
            }

    def check_recovery_progress(self, session_id: str) -> Dict[str, Any]:
        """Check and document recovery progress.

        Args:
            session_id: Session identifier

        Returns:
            Dictionary with progress assessment
        """
        try:
            # Get historical data
            conversation = self.memory.get_conversation(session_id)
            recovery_plan = self.memory.get_recovery_plan(session_id)

            if not recovery_plan:
                return {
                    "agent": "followup_memory",
                    "status": "no_plan",
                    "message": "No recovery plan found for this session"
                }

            # Generate progress assessment
            prompt = f"""Based on the recovery plan and follow-up conversation, assess progress:
            
            Recovery Plan: {json.dumps(recovery_plan, indent=2)}
            Recent conversation: {conversation[-5:] if conversation else 'No recent data'}
            
            Assess:
            1. Progress toward recovery goals
            2. Adherence to recovery plan
            3. New challenges or concerns
            4. Adjustments needed to the plan
            5. Positive developments to celebrate
            
            Be supportive and specific."""

            response = self.gemini.call_gemini(prompt)

            # Store progress assessment
            progress_entry = {
                "assessed_at": datetime.now().isoformat(),
                "assessment": response
            }

            self.memory.add_progress_entry(session_id, progress_entry)
            self.memory.add_message(session_id, "assistant", response)

            result = {
                "agent": "followup_memory",
                "progress_assessment": response,
                "response": response,
                "status": "assessed"
            }

            return result

        except Exception as e:
            print(f"Error assessing progress: {str(e)}")
            return {
                "agent": "followup_memory",
                "status": "error",
                "error": str(e)
            }

    def _get_fallback_recovery_plan(self) -> Dict[str, Any]:
        """Provide fallback recovery plan if API fails.

        Returns:
            Basic recovery plan structure
        """
        return {
            "plan": """Basic Recovery Plan:
            
            1. IMMEDIATE (Today):
            - Reach out to someone you trust
            - Practice one coping technique from your toolkit
            - Ensure your safety
            
            2. DAILY:
            - Morning: Set one manageable goal
            - Afternoon: Check in with your support system
            - Evening: Practice self-care (sleep, hygiene)
            
            3. WEEKLY:
            - Attend therapy/counseling session
            - Practice all coping strategies at least once
            - Reflect on what's working
            
            4. RESOURCES:
            - National Suicide Prevention Lifeline: 988
            - Crisis Text Line: Text HOME to 741741
            - Emergency: 911 or go to nearest ER
            
            Remember: Recovery isn't linear. Small steps matter. You deserve support.""",
            "components": self.RECOVERY_PLAN_COMPONENTS,
            "status": "fallback"
        }
