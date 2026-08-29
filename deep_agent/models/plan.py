from dataclasses import dataclass, field


@dataclass
class Plan:
    goal: str = ""
    tasks: list[str] = field(default_factory=list)
