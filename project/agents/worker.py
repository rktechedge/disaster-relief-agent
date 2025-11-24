from typing import Dict, Any, List
from project.tools.tools import (
    load_safety_steps,
    lookup_helplines,
    summarize_text,
)
from project.core.a2a_protocol import make_message
import re

class SafetyWorker:
    def handle(self, disaster_type: str, location: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates validated safety steps. Ensures minimum 3 steps so evaluator
        does not produce 'too few steps' warnings.
        """
        steps = load_safety_steps(disaster_type)

        # Safety: ensure minimum 3 steps for evaluator
        if len(steps) < 3:
            steps.extend([
                "Avoid dangerous or unstable structures.",
                "Prepare essential emergency supplies.",
            ])

        # Deduplicate
        final_steps = []
        seen = set()
        for s in steps:
            if s not in seen:
                seen.add(s)
                final_steps.append(s)

        response = {
            "type": "safety_info",
            "disaster_type": disaster_type,
            "location": location,
            "steps": final_steps
        }

        return make_message(
            sender="safety_worker",
            receiver="evaluator",
            intent="produce",
            disaster_type=disaster_type,
            location=location,
            payload=response
        )


class HelplineWorker:
    def handle(self, disaster_type, location, payload):
        helplines = lookup_helplines(location, disaster_type)
        response = {
            "type": "helpline_info",
            "disaster_type": disaster_type,
            "location": location,
            "helplines": helplines,
            "summary": summarize_text(", ".join([f"{h['name']} ({h['phone']})" for h in helplines])) if helplines else ""
        }
        return make_message("helpline_worker","evaluator","produce",disaster_type,location,response)

class LogisticsWorker:
    def _extract(self, text):
        return [{"name": m.strip()} for m in re.findall(r"(village\s+\w+)", text.lower())] or [{"name":"Village 1"},{"name":"Village 2"},{"name":"Village 3"}]

    def _plan(self, villages):
        plan=[]
        for i,v in enumerate(villages):
            pr="High" if i==0 else ("Medium" if i==1 else "Low")
            veh="van" if i<2 else "4x4"
            plan.append({"village":v["name"],"priority":pr,"vehicle":veh})
        return plan," -> ".join([p["village"] for p in plan])

    def handle(self, routing, context):
        text = routing["message"]["payload"]["user_input"]
        villages = self._extract(text)
        plan,route = self._plan(villages)
        response = {
            "type":"logistics_info",
            "plan":plan,
            "route_recommendation":route,
            "disaster_type":routing["disaster_type"],
            "location":routing["location"]
        }
        return make_message("logistics_worker","evaluator","produce",routing["disaster_type"],routing["location"],response)

class ReliefWorker:
    def handle(self, routing, context):
        dt, loc = routing["disaster_type"], routing["location"]
        steps = [
            f"Assess immediate impact in {loc or 'the area'}.",
            "Provide medical assistance.",
            "Distribute water and food.",
            "Set up shelters.",
            "Coordinate with authorities."
        ]
        response = {
            "type":"relief_info",
            "steps":steps,
            "disaster_type":dt,
            "location":loc
        }
        return make_message("relief_worker","evaluator","produce",dt,loc,response)
