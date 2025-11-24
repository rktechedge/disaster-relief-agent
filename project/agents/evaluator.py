from typing import Dict, Any, List
from project.tools.tools import (
    validate_safety_steps,
    validate_helplines,
)
from project.core.a2a_protocol import make_message

class Evaluator:
    def evaluate(self, messages: List[Dict[str, Any]], session: Dict[str, Any]):
        agg={"relief":None,"logistics":None,"safety":None,"helplines":None}
        warnings=[]
        for m in messages:
            p=m["payload"]
            t=p["type"]

            if t=="relief_info":
                agg["relief"]=p
            if t=="logistics_info":
                agg["logistics"]=p
            if t=="safety_info":
                ok,issues=validate_safety_steps(p["disaster_type"],p["steps"])
                agg["safety"]=p
                if not ok:warnings.append({"safety":issues})
            if t=="helpline_info":
                ok,issues=validate_helplines(p["helplines"])
                agg["helplines"]=p
                if not ok:warnings.append({"helplines":issues})

        parts=[]
        if agg["relief"]:
            parts.append("Relief Plan:\n" + "\n".join(agg["relief"]["steps"]))
        if agg["logistics"]:
            lp = "\n".join([f"- {i['village']} ({i['priority']}) via {i['vehicle']}" for i in agg["logistics"]["plan"]])
            parts.append("Logistics Plan:\n"+lp)
            parts.append("Route:\n"+agg["logistics"]["route_recommendation"])
        if agg["safety"]:
            parts.append("Safety Steps:\n" + "\n".join(agg["safety"]["steps"]))
        if agg["helplines"]:
            h="\n".join([f"{x['name']}: {x['phone']}" for x in agg["helplines"]["helplines"]])
            parts.append("Helplines:\n"+h)
        if warnings:
            parts.append("Warnings:\n"+str(warnings))

        resp="\n\n".join(parts) or "No information"
        return make_message("evaluator","user","response",payload={"response":resp})
