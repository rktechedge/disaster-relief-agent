import json, time
def log_event(agent, level, msg, meta=None):
    print(json.dumps({"time": time.time(), "agent": agent, "level": level, "message": msg}))
