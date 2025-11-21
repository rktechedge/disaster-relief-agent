from typing import Dict, Any, List
from project.tools.tools import validate_safety_steps, validate_helplines
from project.core.a2a_protocol import make_message

class Evaluator:
    def evaluate(self, messages: List[Dict[str, Any]], session: Dict[str, Any]) -> Dict[str, Any]:
        agg = {"safety": None, "helplines": None}
        warnings = []
        for m in messages:
            p = m.get("payload", {})
            if p.get("type") == "safety_info":
                ok, issues = validate_safety_steps(p.get("disaster_type"), p.get("steps", []))
                agg["safety"] = {"steps": p.get("steps", []), "valid": ok, "issues": issues}
                if not ok:
                    warnings.append({"safety": issues})
            if p.get("type") == "helpline_info":
                ok_h, issues_h = validate_helplines(p.get("helplines", []))
                agg["helplines"] = {"helplines": p.get("helplines", []), "valid": ok_h, "issues": issues_h}
                if not ok_h:
                    warnings.append({"helplines": issues_h})

        parts = []
        if agg["safety"]:
            parts.append("Safety steps:\n" + "\n".join(agg["safety"]["steps"]))
        if agg["helplines"] and agg["helplines"]["helplines"]:
            hp = "\n".join([f"{h['name']}: {h['phone']} ({h.get('note','')})" for h in agg["helplines"]["helplines"]])
            parts.append("Helplines:\n" + hp)
        if warnings:
            parts.append("Warnings:\n" + str(warnings))

        final = "\n\n".join(parts) if parts else "No information available."
        return make_message("evaluator", "user", "response", payload={"response": final})
