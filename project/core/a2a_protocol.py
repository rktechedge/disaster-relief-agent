import uuid, time
def make_message(sender, receiver, intent, disaster_type=None, location=None, payload=None):
    return {
        "id": str(uuid.uuid4()),
        "timestamp": time.time(),
        "sender": sender,
        "receiver": receiver,
        "intent": intent,
        "disaster_type": disaster_type,
        "location": location,
        "payload": payload or {}
    }
