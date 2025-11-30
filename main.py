72
59
70
"""Main entry point for mental health crisis support system."""

import os
from dotenv import load_dotenv
from core.memory_service import CrisisMemoryService
from core.gemini_connector import GeminiConnector
from agents.crisis_assessment_agent import CrisisAssessmentAgent
from agents.deescalation_agent import DeescalationAgent
from agents.resource_finder_agent import ResourceFinderAgent
from agents.safety_router_agent import SafetyRouterAgent
from agents.followup_memory_agent import FollowupMemoryAgent

# Load environment variables
load_dotenv()


class CrisisOrchestrator:
    """Orchestrates all agents to provide comprehensive crisis support."""

    def __init__(self):
        """Initialize the orchestrator with all agents."""
        # Load API key
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")

        # Initialize services
        self.memory = CrisisMemoryService()
        self.gemini = GeminiConnector(api_key)

        # Initialize agents
        self.assessment_agent = CrisisAssessmentAgent(self.gemini, self.memory)
        self.deescalation_agent = DeescalationAgent(self.gemini, self.memory)
        self.resource_agent = ResourceFinderAgent(self.gemini, self.memory)
        self.safety_router = SafetyRouterAgent(self.gemini, self.memory)
        self.followup_agent = FollowupMemoryAgent(self.gemini, self.memory)

        print("Mental Health Crisis Support System Initialized")
        print("5-Agent Architecture:")
        print("  1. Crisis Assessment Agent")
        print("  2. De-escalation Agent")
        print("  3. Resource Finder Agent")
        print("  4. Safety Router Agent")
        print("  5. Follow-up Memory Agent")

    def process_crisis_interaction(self, user_message: str, session_id: str = None) -> dict:
        """Process a crisis interaction through the multi-agent system.

        Args:
            user_message: User's message describing their crisis
            session_id: Optional session identifier for continuity

        Returns:
            Dictionary with comprehensive crisis response
        """
        # Create session if needed
        if not session_id:
            session_id = self.memory.create_session("user_1")

        print(f"\n{'='*60}")
        print(f"Processing Crisis Interaction - Session: {session_id}")
        print(f"{'='*60}")

        # Step 1: Crisis Assessment
        print("\n[Step 1] Running Crisis Assessment...")
        assessment = self.assessment_agent.assess(session_id, user_message)
        crisis_level = assessment.get("crisis_level", "low")
        print(f"  Crisis Level: {crisis_level}")

        # Step 2: Safety Routing (Check for emergency)
        print("\n[Step 2] Running Safety Assessment...")
        routing = self.safety_router.assess_and_route(
            session_id,
            {
                "crisis_level": crisis_level,
                "user_message": user_message
            }
        )
        print(f"  Routing: {routing['routing']}")

        # If emergency, escalate immediately
        if routing['routing'] == 'EMERGENCY_SERVICES':
            print("\n*** EMERGENCY DETECTED ***")
            print(routing['response'])
            return {
                "session_id": session_id,
                "status": "emergency",
                "routing": routing,
                "response": routing['response']
            }

        # Step 3: De-escalation Support
        print("\n[Step 3] Providing De-escalation Support...")
        deescalation = self.deescalation_agent.provide_deescalation_strategies(
            session_id, crisis_level
        )
        print(f"  Strategies Provided: {list(deescalation.get('strategies', {}).keys())}")

        # Step 4: Resource Discovery
        print("\n[Step 4] Finding Appropriate Resources...")
        resources = self.resource_agent.find_resources(session_id, crisis_level)
        print(f"  Status: {resources.get('status')}")

        # Step 5: Recovery Planning & Follow-up
        print("\n[Step 5] Creating Recovery Plan & Schedule...")
        recovery_plan = self.followup_agent.create_recovery_plan(
            session_id, assessment
        )
        followup_schedule = self.followup_agent.schedule_followup(
            session_id, crisis_level
        )
        print(f"  Recovery Plan Status: {recovery_plan.get('status')}")
        print(f"  Follow-ups Scheduled: {len(followup_schedule.get('followup_schedule', {}))}")

        # Compile comprehensive response
        comprehensive_response = {
            "session_id": session_id,
            "status": "success",
            "assessment": assessment,
            "routing": routing,
            "deescalation": deescalation,
            "resources": resources,
            "recovery_plan": recovery_plan,
            "followup_schedule": followup_schedule
        }

        return comprehensive_response

    def run_interactive(self):
        """Run an interactive crisis support session."""
        print("\n" + "="*60)
        print("MENTAL HEALTH CRISIS SUPPORT SYSTEM")
        print("AI-Powered Multi-Agent Support")
        print("="*60)
        print("\nWelcome. I'm here to help you through this difficult time.")
        print("Type 'quit' to exit.")
        print("\nThis system provides:")
        print("  - Crisis assessment and severity analysis")
        print("  - De-escalation strategies and coping techniques")
        print("  - Mental health resource recommendations")
        print("  - Emergency routing if needed")
        print("  - Personalized recovery planning")
        print("\n" + "-"*60 + "\n")

        session_id = self.memory.create_session("user_1")

        while True:
            try:
                user_input = input("\nYou: ").strip()

                if user_input.lower() == 'quit':
                    print("\nThank you for reaching out. Please take care of yourself.")
                    print("Remember: Help is always available at 988 (US) or 9152987821 (India)")
                    break

                if not user_input:
                    continue

                # Process the crisis interaction
                response = self.process_crisis_interaction(user_input, session_id)

                # Display the main response
                if response['status'] == 'emergency':
                    print(f"\nSystem: {response['response']}")
                else:
                    # Show de-escalation response
                    deescalation = response.get('deescalation', {})
                    if deescalation.get('response'):
                        print(f"\nSystem: {deescalation['response']}")

                    # Show resource recommendations if appropriate
                    resources = response.get('resources', {})
                    if resources.get('status') == 'success':
                        print(f"\nRecommended Resources:")
                        print(f"  {resources.get('response', '')[:200]}...")

            except KeyboardInterrupt:
                print("\n\nSession interrupted. Please reach out for help.")
                break
            except Exception as e:
                print(f"\nError processing your message: {str(e)}")
                print("Please try again or contact emergency services: 988 or 911")


def main():
    """Main entry point."""
    try:
        orchestrator = CrisisOrchestrator()
        orchestrator.run_interactive()
    except ValueError as e:
        print(f"Configuration Error: {str(e)}")
        print("Please ensure GEMINI_API_KEY is set in .env file")
    except Exception as e:
        print(f"System Error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
