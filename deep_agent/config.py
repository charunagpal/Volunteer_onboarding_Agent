import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Groq
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    MODEL_NAME: str   = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")

    # Google Sheets
    SHEET_ID: str  = os.getenv("SHEET_ID", "1G2ypmcQB6KaUGqOvdfcWIn3OowLFdmSiMBu_jx3uaDo")
    SHEET_TAB: str = os.getenv("SHEET_TAB", "Form Responses 1")

    # Agent identity
    AGENT_NAME: str = "SmileOra Onboarding"

    # CLI
    EXIT_COMMANDS: tuple[str, ...] = ("exit", "quit", "bye")
