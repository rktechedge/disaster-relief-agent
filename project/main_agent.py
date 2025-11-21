from project.agents.planner import Planner
from project.agents.worker import SafetyWorker, HelplineWorker
from project.agents.evaluator import Evaluator
from project.memory.session_memory import get_session, update_session
from project.core.context_engineering import build_context
from project.core.observability import log_event

class MainAgent:
    def __init__(self, sid="default"):
        self.sid = sid
        self.planner = Planner()
        self.safety = SafetyWorker()
        self.helpline = HelplineWorker()
        self.eval = Evaluator()

    def handle_message(self, text):
        session = get_session(self.sid)
        routing = self.planner.plan(text, session)
        update_session(self.sid, {"last_disaster": routing["disaster_type"], "preferred_location": routing["location"]})
        msgs = []
        if "safety_worker" in routing.get("required_workers", []):
            msgs.append(self.safety.handle(routing["disaster_type"], routing["location"], routing["message"]["payload"]))
        if "helpline_worker" in routing.get("required_workers", []):
            msgs.append(self.helpline.handle(routing["disaster_type"], routing["location"], routing["message"]["payload"]))
        eval_msg = self.eval.evaluate(msgs, session)
        return eval_msg.get("payload", {})

def run_agent(user_input: str):
    agent = MainAgent()
    result = agent.handle_message(user_input)
    return result.get("response", "")
