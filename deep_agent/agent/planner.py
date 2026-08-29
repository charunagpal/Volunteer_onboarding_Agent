import json
from models.plan import Plan
from llm.client import LLMClient


SYSTEM_PROMPT = """You are a planning assistant for an NGO volunteer onboarding agent.

When given a user goal, respond ONLY with a valid JSON object in this exact format:
{
  "goal": "<goal name>",
  "tasks": ["task1", "task2", "task3"]
}

For volunteer onboarding always use exactly these tasks:
["Check Existing Volunteer", "Collect Details", "Validate Information", "Confirm Registration", "Register Volunteer", "Send Welcome Email"]

Return JSON only. No explanation. No markdown."""


class Planner:
    def __init__(self, llm: LLMClient) -> None:
        self.llm = llm

    def plan(self, goal: str) -> Plan:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Goal: {goal}"},
        ]
        response = self.llm.chat(messages)
        return self._parse(response)

    def _parse(self, response: str) -> Plan:
        try:
            data = json.loads(response)
            return Plan(goal=data["goal"], tasks=data["tasks"])
        except (json.JSONDecodeError, KeyError):
            return Plan(
                goal="Volunteer Onboarding",
                tasks=[
                    "Check Existing Volunteer",
                    "Collect Details",
                    "Validate Information",
                    "Confirm Registration",
                    "Register Volunteer",
                    "Send Welcome Email",
                ],
            )
