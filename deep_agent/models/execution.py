from dataclasses import dataclass, field


@dataclass
class ExecutionResult:
    """The outcome of a single task run by the Executor."""
    task: str
    success: bool
    message: str
    retryable: bool = True          # False means a hard failure — no point retrying


@dataclass
class CriticReport:
    """Summary produced by the Critic after evaluating all ExecutionResults."""
    passed: bool
    failed_tasks: list[str] = field(default_factory=list)
    hard_failures: list[str] = field(default_factory=list)
    summary: str = ""
