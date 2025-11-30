"""Session and memory management for crisis conversations."""
from datetime import datetime
from typing import Dict, List

class CrisisMemoryService:
    """Maintains conversation history and user state."""
    
    def __init__(self):
        self.sessions: Dict[str, dict] = {}
    
    def create_session(self, user_id: str) -> str:
        """Create a new crisis session."""
        session_data = {
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "crisis_level": None,
            "messages": [],
            "symptoms": [],
            "interventions_used": [],
            "resources_provided": [],
            "emergency_triggered": False,
            "follow_up_needed": False,
        }
        self.sessions[user_id] = session_data
        return user_id
    
    def add_message(self, user_id: str, role: str, content: str):
        """Add message to conversation history."""
        if user_id not in self.sessions:
            self.create_session(user_id)
        
        self.sessions[user_id]["messages"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def update_crisis_level(self, user_id: str, level: str):
        """Update crisis severity level."""
        if user_id in self.sessions:
            self.sessions[user_id]["crisis_level"] = level
    
    def get_session_context(self, user_id: str) -> str:
        """Get conversation context for agents."""
        if user_id not in self.sessions:
            return ""
        
        session = self.sessions[user_id]
        context_lines = [
            f"Crisis Level: {session['crisis_level']}",
            f"Symptoms: {', '.join(session['symptoms'])}",
            f"Interventions Used: {', '.join(session['interventions_used'])}"
        ]
        return "\n".join(context_lines)
    
    def get_conversation_history(self, user_id: str, last_n: int = 5) -> List[Dict]:
        """Get recent conversation history."""
        if user_id not in self.sessions:
            return []
        
        messages = self.sessions[user_id]["messages"]
        return messages[-last_n:] if messages else []
