"""
QA Handler — answers questions about SmileOra using the static knowledge base.

The Supervisor calls `answer_if_kb_question()` at the start of every turn.
If the message is a question about SmileOra, it answers from the KB and returns
a string. If it is not a KB question, it returns None so the Supervisor
continues with the normal onboarding flow.
"""
from llm.client import LLMClient
from prompts.smileora_kb import SMILEORA_KB


# Keywords that suggest the user is asking about SmileOra rather than doing
# onboarding steps. Checked quickly before making an LLM call.
_KB_TRIGGERS = {
    "what", "who", "how", "when", "where", "which", "why",
    "tell", "explain", "describe", "about", "mission", "vision",
    "program", "event", "activity", "volunteer", "teach", "education",
    "health", "environment", "animal", "elderly", "fundrais", "technology",
    "cpp", "training", "policy", "safeguard", "contact", "email",
    "website", "location", "area", "bangalore", "hours", "time",
    "weekend", "online", "paid", "salary", "certificate", "qualify",
    "age", "limit", "onboard", "register", "process", "assign",
}

_SYSTEM_PROMPT = f"""You are the SmileOra Volunteer Assistant.
Answer the user's question using ONLY the information in the knowledge base below.
Be friendly, concise, and helpful. If the answer is not in the knowledge base,
say "I don't have that information — please contact smileora.ngo.info@gmail.com".
Do not make up information. Do not mention that you are using a knowledge base.

KNOWLEDGE BASE:
{SMILEORA_KB}
"""


class QAHandler:
    def __init__(self, llm: LLMClient) -> None:
        self.llm = llm

    def answer_if_kb_question(self, message: str) -> str | None:
        """
        Returns an answer string if the message is a KB question,
        or None if it should be handled by the normal onboarding flow.
        """
        if not self._looks_like_kb_question(message):
            return None

        try:
            response = self.llm.chat([
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user",   "content": message},
            ])
            return response
        except Exception as e:
            print(f"[QA] LLM error: {e}")
            return None

    def _looks_like_kb_question(self, message: str) -> bool:
        """
        Fast keyword check — avoids an LLM call for every onboarding reply
        like 'yes', 'Alice Smith', or phone numbers.
        """
        if len(message.strip()) < 4:
            return False
        lower = message.lower()
        return any(trigger in lower for trigger in _KB_TRIGGERS)
