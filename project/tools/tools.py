import json, os
BASE = os.path.join(os.path.dirname(__file__), "..", "safety_data")

def classify_disaster(t: str) -> str:
    t = t.lower()
    if "flood" in t:
        return "flood"
    if "earthquake" in t or "quake" in t:
        return "earthquake"
    if "cyclone" in t or "storm" in t:
        return "cyclone"
    if "fire" in t or "wildfire" in t:
        return "fire"
    return "unknown"

def extract_location(t: str) -> str:
    t = t.lower()
    if " in " in t:
        loc = " ".join(t.split(" in ")[-1].strip().split()[:3])
        return loc.title()
    return ""

def load_safety_steps(d: str):
    path = os.path.join(BASE, "safety_instructions.json")
    if not os.path.exists(path):
        return ["Follow official guidance from local authorities."]
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get(d, data.get("default", ["Follow official guidance."]))

def lookup_helplines(loc, d):
    path = os.path.join(BASE, "helplines.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if loc and loc in data:
        return data[loc].get(d, data[loc].get("general", []))
    return data.get("global", {}).get("general", [])

def summarize_text(t: str) -> str:
    return t if len(t) <= 200 else t[:197] + "..."

def validate_safety_steps(d, steps):
    if not steps:
        return False, ["no steps"]
    issues = []
    if len(steps) < 2:
        issues.append("too few steps")
    banned = ["consult your doctor", "take prescription"]
    for s in steps:
        for b in banned:
            if b in s.lower():
                issues.append(f"contains banned phrase: {b}")
    ok = len(issues) == 0
    return ok, issues

def validate_helplines(h):
    if not h:
        return False, ["no helplines"]
    issues = []
    for x in h:
        if not x.get("phone"):
            issues.append(f"missing phone for {x.get('name')}")
    return (len(issues) == 0), issues
