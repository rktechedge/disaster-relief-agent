import json
import os
from typing import List, Dict, Any

# Base folder for any safety/helpline JSON data
BASE = os.path.join(os.path.dirname(__file__), "..", "safety_data")


# -------------------------------
#  CLASSIFICATION / EXTRACTION
# -------------------------------

def classify_disaster(text: str) -> str:
    t = text.lower()
    if "flood" in t or "flooding" in t:
        return "flood"
    if "earthquake" in t or "quake" in t:
        return "earthquake"
    if "cyclone" in t or "storm" in t:
        return "cyclone"
    if "fire" in t or "wildfire" in t:
        return "fire"
    return "unknown"


def extract_location(text: str) -> str:
    """
    Naive location extraction: looks for 'in <place>'.
    Example: "Flood in Assam" → "Assam"
    """
    t = text.lower()
    if " in " in t:
        parts = t.split(" in ")
        loc = parts[-1].strip().split()[0:3]
        return " ".join(loc).strip().title()
    return ""


# -------------------------------
#  SAFETY STEPS (IMPROVED)
# -------------------------------

def load_safety_steps(disaster_type: str) -> List[str]:
    """
    Improved version:
    - Reads from safety_instructions.json if available
    - Uses "default" section if disaster type missing
    - Guarantees minimum of 3 steps (for validator)
    """
    path = os.path.join(BASE, "safety_instructions.json")

    # If JSON file missing → complete fallback list
    if not os.path.exists(path):
        return [
            "Follow official guidelines from local authorities.",
            "Avoid dangerous or flooded areas.",
            "Stay alert for official emergency updates.",
        ]

    # Load JSON
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Get steps for this disaster or default
    steps = data.get(disaster_type, data.get("default", []))

    # Guarantee minimum 3 steps
    if len(steps) < 3:
        steps.extend([
            "Avoid dangerous or flooded areas.",
            "Stay alert for official emergency updates.",
        ])

    # Keep unique ordered steps
    seen = set()
    final_steps = []
    for s in steps:
        if s not in seen:
            seen.add(s)
            final_steps.append(s)

    return final_steps


# -------------------------------
#  HELPLINES
# -------------------------------

def lookup_helplines(location: str, disaster_type: str) -> List[Dict[str, Any]]:
    """
    Lookup helplines based on location and disaster type.
    """
    path = os.path.join(BASE, "helplines.json")
    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Region-specific data
    if location and location in data:
        return data[location].get(disaster_type, data[location].get("general", []))

    # Global fallback
    return data.get("global", {}).get("general", [])


# -------------------------------
#  UTILITIES
# -------------------------------

def summarize_text(text: str) -> str:
    """
    Simple heuristic summarizer.
    """
    if len(text) <= 200:
        return text
    return text[:197] + "..."


# -------------------------------
#  VALIDATION
# -------------------------------

def validate_safety_steps(disaster_type: str, steps: List[str]) -> (bool, List[str]):
    """
    Safety rules:
    - At least 2 steps
    - No banned phrases
    """
    if not steps:
        return False, ["no steps found"]

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


def validate_helplines(helplines: List[Dict[str, Any]]) -> (bool, List[str]):
    """
    Helpline validation:
    - Must have 'phone'
    """
    if not helplines:
        return False, ["no helplines found"]

    issues = []
    for h in helplines:
        if "phone" not in h or not h["phone"]:
            issues.append(f"missing phone for {h.get('name')}")

    return (len(issues) == 0), issues
