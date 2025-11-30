# Mental Health Crisis Agent - Implementation Guide Part 2

## Overview
This guide completes the 5-agent crisis support system with detailed implementations for Agents 2-5.

## Agent Architecture Diagram

```
┌─────────────────────────────────────────────────┐
│  User Input: "I'm having suicidal thoughts"   │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │ Agent 1: CRISIS ASSESSMENT │
        │ ✓ Analyzes severity        │
        │ ✓ Extracts symptoms        │
        │ ✓ Determines urgency       │
        └────────────┬─────────────────┘
                     │
         ┌───────────┴────────────┐
         │                        │
   LOW/MEDIUM RISK        HIGH/EMERGENCY RISK
         │                        │
         ▼                        ▼
   ┌──────────────┐      ┌─────────────────┐
   │ Agent 2:     │      │ Agent 4:        │
   │ DE-ESCALATE  │      │ SAFETY ROUTER   │
   │ ✓ Coping     │      │ ✓ Verify risk   │
   │ ✓ Breathing  │      │ ✓ Emergency SOS │
   │ ✓ Mindful    │      │ ✓ Call 911      │
   └──────┬───────┘      └─────────────────┘
          │
          ▼
   ┌──────────────────┐
   │ Agent 3:         │
   │ RESOURCE FINDER  │
   │ ✓ Find therapists│
   │ ✓ Crisis lines   │
   │ ✓ Support groups │
   └──────┬───────────┘
          │
          ▼
   ┌──────────────────┐
   │ Agent 5:         │
   │ FOLLOW-UP        │
   │ ✓ Check-ins      │
   │ ✓ Track progress │
   │ ✓ Prevent relapse│
   └──────────────────┘
```

## Next Steps to Complete Implementation

### 1. Create agents/deescalation_agent.py
### 2. Create agents/resource_finder_agent.py  
### 3. Create agents/safety_router_agent.py
### 4. Create agents/followup_memory_agent.py
### 5. Create tools/coping_techniques.py
### 6. Create tools/emergency_hotlines.py
### 7. Create orchestrator.py (main agent coordinator)

## File Structure After Completion

```
mental-health-crisis-agent/
├── agents/
│   ├── __init__.py
│   ├── crisis_assessment_agent.py (✓ DONE)
│   ├── deescalation_agent.py (NEXT)
│   ├── resource_finder_agent.py
│   ├── safety_router_agent.py
│   └── followup_memory_agent.py
├── core/
│   ├── __init__.py
│   ├── memory_service.py (✓ DONE)
│   └── gemini_connector.py (✓ DONE)
├── tools/
│   ├── __init__.py
│   ├── coping_techniques.py
│   └── emergency_hotlines.py
├── data/
│   ├── crisis_resources.json
│   ├── coping_strategies.json
│   └── therapy_providers.json
├── orchestrator.py (Multi-agent coordinator)
├── main.py (✓ DONE)
├── requirements.txt (✓ DONE)
├── .env.example (✓ DONE)
├── .gitignore (✓ DONE)
└── README.md (✓ DONE)
```

## Summary

✅ **Completed:**
- Repository created
- Folder structure set up
- Core services: Memory & Gemini integration
- Agent 1: Crisis Assessment
- Main entry point
- Configuration files

📝 **In Progress:**
- This implementation guide

⏳ **To Complete:**
- Agents 2-5 (De-escalation, Resource Finder, Safety Router, Follow-up)
- Tool modules (Coping techniques, Emergency hotlines)
- Data resources (JSON files)
- Orchestrator (Multi-agent coordinator)
- Testing suite

## Implementation Tips

1. **Agent Order**: Implement agents in order 2→5 for logical progression
2. **Testing**: Each agent should be testable independently
3. **Memory**: Use memory_service to track conversation state
4. **Error Handling**: All Gemini calls should have fallbacks
5. **Emergency**: Always have quick access to crisis hotlines

## Running the System

```bash
# Set up environment
cp .env.example .env
echo "GEMINI_API_KEY=your_key" >> .env

# Install dependencies
pip install -r requirements.txt

# Run the system
python main.py
```

## Architecture Notes

The multi-agent system uses:
- **Sequential Routing**: Crisis level determines which agent handles the user
- **Memory Persistence**: All agents share conversation history
- **LLM-Powered**: Gemini 1.5 Pro provides empathetic responses
- **Resource Optimization**: Crisis lines and therapist directories
- **Follow-up Capability**: Check-ins to prevent relapse

## Next Document

See Part 3 for:
- Detailed agent implementations (2-5)
- Test cases
- Deployment guide
