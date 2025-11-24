from typing import Dict, Any
from project.tools.tools import extract_location, classify_disaster
from project.core.a2a_protocol import make_message

class Planner:
    def __init__(self):
        pass

    def plan(self, user_input: str, session: Dict[str, Any]) -> Dict[str, Any]:
        disaster_type = classify_disaster(user_input)
        location = extract_location(user_input) or session.get("preferred_location")
        text = (user_input or "").lower()

        required_workers = set(["safety_worker", "helpline_worker"])

        logistics_keywords = ["send relief", "delivery", "transport", "route", "logistics", "warehouse"]
        if any(k in text for k in logistics_keywords):
            required_workers.add("logistics_worker")

        relief_keywords = ["plan", "steps", "what should", "how to"]
        if any(k in text for k in relief_keywords):
            required_workers.add("relief_worker")

        if disaster_type in ["flood", "earthquake", "cyclone", "storm", "landslide"]:
            required_workers.add("relief_worker")

        msg = make_message(
            sender="planner",
            receiver="worker",
            intent="route",
            disaster_type=disaster_type,
            location=location,
            payload={"user_input": user_input}
        )
        return {
            "message": msg,
            "required_workers": list(required_workers),
            "disaster_type": disaster_type,
            "location": location
        }
