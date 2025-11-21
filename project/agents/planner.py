from typing import Dict, Any
from project.tools.tools import extract_location, classify_disaster
from project.core.a2a_protocol import make_message

class Planner:
    def plan(self, user_input: str, session: Dict[str, Any]) -> Dict[str, Any]:
        disaster_type = classify_disaster(user_input)
        location = extract_location(user_input) or session.get("preferred_location")
        msg = make_message("planner","worker","route",disaster_type,location,{"user_input": user_input})
        return {
            "message": msg,
            "required_workers": ["safety_worker","helpline_worker"],
            "disaster_type": disaster_type,
            "location": location
        }
