from project.agents.planner import Planner
from project.agents.worker import SafetyWorker, HelplineWorker, LogisticsWorker, ReliefWorker
from project.agents.evaluator import Evaluator
from project.memory.session_memory import get_session, update_session
from project.core.context_engineering import build_context
from project.core.observability import log_event

class MainAgent:
    def __init__(self, session_id: str = "default"):
        self.session_id = session_id
        self.planner = Planner()
        self.safety_worker = SafetyWorker()
        self.helpline_worker = HelplineWorker()
        self.logistics_worker = LogisticsWorker()
        self.relief_worker = ReliefWorker()
        self.evaluator = Evaluator()

    def handle_message(self, user_input: str):
        session = get_session(self.session_id)
        log_event("MainAgent", "info", f"Received input: {user_input}")

        routing = self.planner.plan(user_input, session)
        update_session(self.session_id, {
            "last_disaster": routing.get("disaster_type"),
            "preferred_location": routing.get("location")
        })

        context = build_context(session, routing)
        messages = []
        required = routing.get("required_workers", []) or []

        if "safety_worker" in required:
            msg = self.safety_worker.handle(
                routing.get("disaster_type"),
                routing.get("location"),
                routing.get("message", {}).get("payload", {})
            )
            messages.append(msg)

        if "helpline_worker" in required:
            msg = self.helpline_worker.handle(
                routing.get("disaster_type"),
                routing.get("location"),
                routing.get("message", {}).get("payload", {})
            )
            messages.append(msg)

        if "logistics_worker" in required:
            msg = self.logistics_worker.handle(routing, context)
            messages.append(msg)

        if "relief_worker" in required:
            msg = self.relief_worker.handle(routing, context)
            messages.append(msg)

        eval_msg = self.evaluator.evaluate(messages, session)
        result = eval_msg.get("payload", {})
        log_event("MainAgent", "info", "Returning response")
        return result.get("response", "")

def run_agent(user_input: str):
    agent = MainAgent()
    return agent.handle_message(user_input)
