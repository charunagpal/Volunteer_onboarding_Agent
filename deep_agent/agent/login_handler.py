from agent.state import AgentState
from skills.volunteer import search_volunteer, mark_cpp_complete
from skills.sheets import search_volunteer_in_sheet

# ── CPP links (single source of truth) ───────────────────────────────────────
CPP_TRAINING_LINK = "https://cpp-traning.netlify.app/cpp_training_video.html"
CPP_QUIZ_LINK     = "https://forms.gle/wqeSzfMKQkVKTtdw5"


class LoginHandler:

    def handle(self, state: AgentState, email: str) -> dict:
        email = email.strip().lower()

        # ── Step 1: Is the volunteer registered in XLSX? ──────────────────────
        volunteer = search_volunteer(email)

        if not volunteer:
            # Unknown email — needs registration
            return {"status": "not_found", "email": email}

        # Registered — load their data into state
        state.volunteer_data = {
            field: getattr(volunteer, field)
            for field in volunteer.__dataclass_fields__
        }

        # ── Step 2: Check CPP quiz score from Google Sheet ────────────────────
        sheet_result = search_volunteer_in_sheet(email)

        if not sheet_result.found:
            # Registered but never taken the CPP quiz
            state.volunteer_data["cpp_score"]  = None
            state.volunteer_data["cpp_passed"] = False
            return {"status": "cpp_not_taken", "volunteer": volunteer}

        # Has taken the quiz — store score
        state.volunteer_data["cpp_score"]  = sheet_result.score
        state.volunteer_data["cpp_passed"] = sheet_result.cpp_passed

        if not sheet_result.cpp_passed:
            # Taken but failed
            return {"status": "cpp_failed", "volunteer": volunteer,
                    "score": sheet_result.score}

        # Passed CPP
        return {"status": "cpp_passed", "volunteer": volunteer,
                "score": sheet_result.score}

    def complete_cpp(self, email: str) -> bool:
        return mark_cpp_complete(email)
