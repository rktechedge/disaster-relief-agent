class SessionMemory:
    def __init__(self):
        self.sessions = {}
    def get(self, id):
        return self.sessions.setdefault(id, {})
    def update(self, id, data):
        self.sessions.setdefault(id, {}).update(data)

_MEMORY = SessionMemory()

def get_session(id="default"):
    return _MEMORY.get(id)

def update_session(id, data):
    _MEMORY.update(id, data)
