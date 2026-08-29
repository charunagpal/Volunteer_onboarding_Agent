from dataclasses import dataclass, field


@dataclass
class AgentState:
    conversation_history: list[dict] = field(default_factory=list)
    goal: str = ""
    tasks: list[str] = field(default_factory=list)
    volunteer_data: dict = field(default_factory=dict)
    status: str = "idle"
    cpp_onboarded: bool = False   # True once volunteer is registered AND CPP passed

    def add_message(self, role: str, content: str) -> None:
        self.conversation_history.append({"role": role, "content": content})

    def reset(self) -> None:
        self.conversation_history.clear()
        self.goal = ""
        self.tasks.clear()
        self.volunteer_data.clear()
        self.status = "idle"
