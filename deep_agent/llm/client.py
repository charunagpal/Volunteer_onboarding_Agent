from groq import Groq
from config import Config


class LLMClient:
    def __init__(self, config: Config) -> None:
        self.client = Groq(api_key=config.GROQ_API_KEY)
        self.model  = config.MODEL_NAME

    def chat(self, messages: list[dict]) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return response.choices[0].message.content.strip()
