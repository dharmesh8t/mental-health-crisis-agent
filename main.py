"""Main entry point for mental health crisis support system."""
import os
from dotenv import load_dotenv
from core.memory_service import CrisisMemoryService
from core.gemini_connector import GeminiConnector
from agents.crisis_assessment_agent import CrisisAssessmentAgent

# Load environment variables
load_dotenv()

def main():
    """Initialize and run the crisis support system."""
    
    # Load API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment")
    
    # Initialize services
    memory_service = CrisisMemoryService()
    gemini_connector = GeminiConnector(api_key)
    crisis_assessment_agent = CrisisAssessmentAgent(gemini_connector, memory_service)
    
    print("Mental Health Crisis Support System Initialized")
    print("Starting crisis support agent...\n")
    
    # Main conversation loop
    while True:
        user_input = input("User: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ['exit', 'quit']:
            break
        
        # Process with crisis assessment agent
        # Result routing happens here
        print("System processing...\n")

if __name__ == "__main__":
    main()
