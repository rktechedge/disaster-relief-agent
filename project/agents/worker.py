from typing import Dict, Any
from project.tools.tools import load_safety_steps, lookup_helplines, summarize_text
from project.core.a2a_protocol import make_message

class SafetyWorker:
    def handle(self, disaster_type: str, location: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        steps = load_safety_steps(disaster_type)
        res = {"type": "safety_info", "disaster_type": disaster_type, "location": location, "steps": steps}
        return make_message("safety_worker", "evaluator", "produce", disaster_type, location, res)

class HelplineWorker:
    def handle(self, disaster_type: str, location: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        helplines = lookup_helplines(location, disaster_type)
        summary = summarize_text(", ".join([f"{h['name']} ({h['phone']})" for h in helplines])) if helplines else ""
        res = {"type": "helpline_info", "disaster_type": disaster_type, "location": location, "helplines": helplines, "summary": summary}
        return make_message("helpline_worker", "evaluator", "produce", disaster_type, location, res)
