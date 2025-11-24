import time
import json
from loguru import logger

def log_event(agent: str, level: str, message: str, meta=None):
    """
    Structured JSON logging for multi-agent pipeline.
    Dashboard reads these JSON entries from spaces_app.log.

    Example:
    {"time":"2025-11-21 18:35:10","agent":"Planner","level":"INFO","message":"Planning route","meta":{"workers":["safety","helpline"]}}
    """
    if meta is None:
        meta = {}

    entry = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "agent": agent,
        "level": level.upper(),
        "message": message,
        "meta": meta
    }

    # Write as a JSON line to the log file
    logger.log(level.upper(), json.dumps(entry))