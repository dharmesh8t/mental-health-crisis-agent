"""Gemini API integration for empathetic responses."""
import google.generativeai as genai
from typing import Optional, Dict
import json
import re
import os

class GeminiConnector:
    """Manages Gemini API interactions for crisis support."""
    
    def __init__(self, api_key: Optional[str] = None):
        api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    def generate_empathetic_response(
        self,
        user_message: str,
        system_prompt: str,
        context: Optional[str] = None
    ) -> str:
        """Generate empathetic response using Gemini."""
        
        full_prompt = f"""{system_prompt}

{f"Context: {context}" if context else ""}

User Message: "{user_message}"

Please respond now:"""
        
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"I'm here to help. Please tell me more."
    
    def assess_crisis_severity(self, user_message: str) -> Dict:
        """Assess crisis severity level."""
        
        assessment_prompt = """You are a mental health crisis assessment expert.
Analyze this message and respond ONLY with valid JSON:
{
    "severity_level": "low",
    "key_symptoms": [],
    "risk_factors": [],
    "immediate_recommendations": [],
    "confidence": 0.8
}

User message: """ + user_message
        
        try:
            response = self.model.generate_content(assessment_prompt)
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception as e:
            pass
        
        return {
            "severity_level": "unknown",
            "key_symptoms": [],
            "risk_factors": [],
            "immediate_recommendations": [],
            "confidence": 0.0
        }
    
    def extract_resource_needs(self, user_message: str) -> Dict:
        """Extract what resources user needs."""
        
        extraction_prompt = """Extract resource needs from this message.
Respond with ONLY JSON:
{
    "needs_therapist": false,
    "needs_hotline": false,
    "needs_support_group": false,
    "urgency": "soon",
    "location_info": null
}

Message: """ + user_message
        
        try:
            response = self.model.generate_content(extraction_prompt)
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        return {
            "needs_therapist": False,
            "needs_hotline": False,
            "needs_support_group": False,
            "urgency": "soon",
            "location_info": None
        }
