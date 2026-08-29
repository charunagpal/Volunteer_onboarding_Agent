# SmileOra Volunteer Onboarding Agent

A production-quality Deep Agent built from first principles for the **SmileOra NGO**. It onboards volunteers through a Streamlit chat UI, stores registrations in Excel, and verifies CPP (Child Protection Policy) quiz results from a live Google Sheet.

No LangGraph, CrewAI, AutoGen, Semantic Kernel, or MCP — everything is built from scratch.

---

## Architecture

```
streamlit_app.py          ← Streamlit UI (form + chat + sidebar)
    │
    └── agent/supervisor.py       ← Orchestrator / state machine
            ├── agent/planner.py          ← LLM → Plan
            ├── agent/executor.py         ← Runs tasks → ExecutionResult
            ├── agent/critic.py           ← Evaluates results → CriticReport
            ├── agent/conversation_manager.py  ← Field collection + validation
            ├── agent/validator.py        ← Per-field validation rules
            ├── agent/reflection.py       ← Summary + confirmation step
            ├── agent/login_handler.py    ← XLSX lookup + Google Sheets CPP check
            └── agent/qa_handler.py       ← KB question detection + LLM answer
                │
                ├── llm/client.py             ← Groq SDK wrapper
                ├── skills/volunteer.py       ← XLSX read/write (volunteers.xlsx)
                ├── skills/email.py           ← Gmail API (OAuth 2.0) welcome email
                ├── skills/sheets.py          ← Google Sheets API v4 CPP score lookup
                ├── models/volunteer.py       ← Volunteer dataclass
                ├── models/plan.py            ← Plan dataclass
                ├── models/execution.py       ← ExecutionResult, CriticReport
                └── prompts/smileora_kb.py    ← Static SmileOra knowledge base
```

### Login flow

```
Email entered
  ├── not_found        → Registration form (one-shot)
  ├── cpp_passed       → ✅ Onboarded — mark CPP complete in XLSX
  ├── cpp_failed       → ⚠️ Score X/15 — retake links
  └── cpp_not_taken    → 📋 Complete CPP training — links
```

After registration → CPP training prompt. CPP onboarding completes only when score ≥ 13/15 confirmed from the Google Sheet.

---

## Prerequisites

- Python 3.11+
- A [Groq](https://console.groq.com) API key
- Google Cloud project with **Gmail API** and **Google Sheets API** enabled
- OAuth 2.0 Desktop credentials (`credentials.json`) in `skills/`
- The CPP quiz Google Sheet ID (already pre-configured in `config.py`)

---

## Setup

### 1. Clone and create a virtual environment

```bash
cd deep_agent
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set environment variables

Create a `.env` file in `deep_agent/`:

```
GROQ_API_KEY=gsk_...your_key_here...
```

Optional overrides (defaults already set in `config.py`):

```
MODEL_NAME=llama-3.1-8b-instant
SHEET_ID=1G2ypmcQB6KaUGqOvdfcWIn3OowLFdmSiMBu_jx3uaDo
SHEET_TAB=Form Responses 1
```

### 3. Configure Google OAuth

Place your `credentials.json` (Desktop OAuth client) inside `skills/`.

On first run the browser will open for consent. The token is saved to `skills/token.json` and reused automatically on subsequent runs.

The OAuth consent requires these scopes:
- `https://www.googleapis.com/auth/gmail.send`
- `https://www.googleapis.com/auth/spreadsheets.readonly`

### 4. Volunteer data directory

The XLSX is stored in `volunteerdata/volunteers.xlsx` and created automatically on first registration. Do **not** commit this file.

---

## Running the app

```bash
cd deep_agent
source venv/bin/activate
streamlit run streamlit_app.py
```

Opens at `http://localhost:8501`.

### CLI mode (optional)

```bash
python app.py
```

---

## Running tests

```bash
cd deep_agent
source venv/bin/activate
pytest tests/ -v
```

7 tests covering the Critic component.

---

## Project structure

```
deep_agent/
├── app.py                      # CLI entry point
├── streamlit_app.py            # Streamlit UI
├── config.py                   # API keys, model, sheet config
├── requirements.txt
├── SmileOraLego.png            # NGO logo
│
├── agent/
│   ├── supervisor.py           # Main orchestrator — state machine
│   ├── state.py                # AgentState dataclass
│   ├── planner.py              # LLM → Plan(goal, tasks)
│   ├── executor.py             # Runs tasks → list[ExecutionResult]
│   ├── critic.py               # Evaluates results → CriticReport
│   ├── conversation_manager.py # FIELDS, validation, Q&A loop
│   ├── validator.py            # Per-field validation rules
│   ├── reflection.py           # Pre-execution summary + confirm
│   ├── login_handler.py        # XLSX + Google Sheets CPP check
│   └── qa_handler.py           # SmileOra KB question answering
│
├── skills/
│   ├── volunteer.py            # search_volunteer(), create_volunteer(), mark_cpp_complete()
│   ├── email.py                # Gmail API — send_welcome_email()
│   ├── sheets.py               # Sheets API v4 — search_volunteer_in_sheet()
│   └── token.json              # OAuth token (auto-generated, not committed)
│
├── llm/
│   └── client.py               # Groq SDK wrapper — chat(messages) → str
│
├── models/
│   ├── volunteer.py            # Volunteer dataclass
│   ├── plan.py                 # Plan dataclass
│   └── execution.py            # ExecutionResult, CriticReport
│
├── prompts/
│   └── smileora_kb.py          # SMILEORA_KB — 17 sections of SmileOra info
│
├── tests/
│   └── test_critic.py          # 7 pytest tests for Critic
│
└── volunteerdata/
    └── volunteers.xlsx         # Registration data — NOT committed
```

---

## Key design decisions

| Decision | Rationale |
|---|---|
| No orchestration framework | Built from scratch to demonstrate deep agent principles |
| Groq + `llama-3.1-8b-instant` | Fast, free-tier LLM — no watsonx dependency |
| One-shot Streamlit form | Better UX than Q&A chat for structured data collection |
| XLSX as registration store | Simple, portable, no DB setup required |
| Google Sheets CPP lookup | Real quiz results from the NGO's existing Google Form |
| Gmail API (OAuth 2.0) | Deliverable welcome email — no SMTP credentials needed |
| Static KB in `smileora_kb.py` | Single source of truth for all SmileOra info |
| CPP score ≥ 13/15 to pass | Best score across all attempts wins |

---

## .gitignore (create manually)

```
venv/
__pycache__/
*.pyc
.env
.enves
skills/token.json
skills/credentials.json
volunteerdata/volunteers.xlsx
.DS_Store
```
