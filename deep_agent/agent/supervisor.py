from config import Config
from agent.state import AgentState
from agent.planner import Planner
from agent.executor import Executor
from agent.critic import Critic, MAX_RETRIES
from agent.conversation_manager import ConversationManager, FIELDS
from agent.reflection import Reflection
from agent.login_handler import LoginHandler, CPP_TRAINING_LINK, CPP_QUIZ_LINK
from agent.qa_handler import QAHandler
from llm.client import LLMClient

FIELD_QUESTIONS = {field: question for field, question in FIELDS}


class Supervisor:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.state = AgentState()
        self.llm = LLMClient(config)
        self.planner = Planner(self.llm)
        self.executor = Executor()
        self.conversation_manager = ConversationManager()
        self.reflection = Reflection()
        self.login_handler = LoginHandler()
        self.critic = Critic()
        self.qa_handler = QAHandler(self.llm)
        self._retry_count: int = 0

    def reset(self) -> None:
        """Reset the supervisor state for a new session."""
        self.state = AgentState()
        self._retry_count = 0

    def handle(self, message: str) -> str:
        self.state.add_message("user", message)

        # ── KNOWLEDGE BASE — answer SmileOra questions at any point ─────────
        # Always allow KB questions, even before email is entered.
        # Skip only during bare onboarding data-entry steps (collecting field values).
        _skip_statuses = {"collecting"}
        if self.state.status not in _skip_statuses:
            kb_answer = self.qa_handler.answer_if_kb_question(
                message,
                cpp_onboarded=self.state.cpp_onboarded,
            )
            if kb_answer:
                self.state.add_message("agent", kb_answer)
                return kb_answer

        # ── LOGIN GATE ──────────────────────────────────────────────────────

        # Ask for email first
        if self.state.status == "idle":
            self.state.status = "awaiting_email"
            reply = "Welcome to SmileOra! 🌟\nPlease enter your email address to continue:"
            self.state.add_message("agent", reply)
            return reply

        # Process email
        if self.state.status == "awaiting_email":
            result = self.login_handler.handle(self.state, message)
            email  = message.strip()

            # ── Not registered → show onboarding form ────────────────────────
            if result["status"] == "not_found":
                self.state.volunteer_data["email"] = email.lower()
                self.state.status = "new_volunteer"
                reply = (
                    f"No registration found for {email}.\n"
                    "Let's get you registered as a SmileOra volunteer! 🎉"
                )
                self.state.add_message("agent", reply)
                return reply

            vol  = result["volunteer"]
            name = vol.preferred_name or vol.full_name

            # ── Registered + CPP passed → fully onboarded ────────────────────
            if result["status"] == "cpp_passed":
                self.state.status       = "done"
                self.state.cpp_onboarded = True
                # Update XLSX so CPP status is persisted
                self.login_handler.complete_cpp(message.strip().lower())
                reply = (
                    f"Welcome back, {name}! 🌟\n\n"
                    f"✅ You are successfully onboarded with SmileOra!\n"
                    f"CPP Score: {result['score']} / 15 — Passed\n\n"
                    f"Our team will be in touch with upcoming volunteering opportunities.\n"
                    f"If you have questions, reach us at smileora.ngo.info@gmail.com"
                )
                self.state.add_message("agent", reply)
                return reply

            # ── Registered + CPP failed → retake ─────────────────────────────
            if result["status"] == "cpp_failed":
                self.state.status = "cpp_pending"
                reply = (
                    f"Welcome back, {name}! 👋\n\n"
                    f"⚠️  Your CPP quiz score is below the passing mark.\n"
                    f"Your score: {result['score']} / 15  (minimum required: 13)\n\n"
                    f"Please watch the training video and retake the quiz:\n"
                    f"📺 CPP Training Video: {CPP_TRAINING_LINK}\n"
                    f"📝 CPP Quiz Form: {CPP_QUIZ_LINK}\n\n"
                    f"Once you have retaken the quiz, type 'check' and we will verify your updated score."
                )
                self.state.add_message("agent", reply)
                return reply

            # ── Registered + never taken CPP quiz ────────────────────────────
            if result["status"] == "cpp_not_taken":
                self.state.status = "cpp_pending"
                reply = (
                    f"Welcome back, {name}! 👋\n\n"
                    f"You are registered with SmileOra but have not completed the\n"
                    f"CPP (Child Protection Policy) training yet.\n\n"
                    f"This is mandatory before you can begin volunteering.\n\n"
                    f"Please complete the following:\n"
                    f"📺 Step 1 — Watch the training video: {CPP_TRAINING_LINK}\n"
                    f"📝 Step 2 — Take the quiz: {CPP_QUIZ_LINK}\n\n"
                    f"Once done, type 'check' and we will verify your score."
                )
                self.state.add_message("agent", reply)
                return reply

        # Handle CPP re-check (user typed 'check' after retaking quiz)
        if self.state.status == "cpp_pending":
            if message.strip().lower() in ("check", "cpp completed", "completed", "done", "yes"):
                email        = self.state.volunteer_data.get("email", "")
                from skills.sheets import search_volunteer_in_sheet
                sheet_result = search_volunteer_in_sheet(email)

                if not sheet_result.found:
                    reply = (
                        f"⚠️  We could not find a quiz submission for {email}.\n"
                        f"Please complete the quiz first:\n"
                        f"📝 {CPP_QUIZ_LINK}"
                    )
                elif not sheet_result.cpp_passed:
                    reply = (
                        f"❌ Your latest score is {sheet_result.score} / 15 "
                        f"(minimum required: 13).\n\n"
                        f"Please review the training and retake the quiz:\n"
                        f"📺 {CPP_TRAINING_LINK}\n"
                        f"📝 {CPP_QUIZ_LINK}"
                    )
                else:
                    self.state.status        = "done"
                    self.state.cpp_onboarded = True
                    # Persist CPP completion to volunteers.xlsx
                    self.login_handler.complete_cpp(email)
                    reply = (
                        f"✅ Congratulations! You scored {sheet_result.score} / 15 — CPP Passed!\n\n"
                        f"You are now fully cleared to start volunteering with SmileOra. 🎉\n"
                        f"Our team will reach out with your first assignment.\n"
                        f"If you have questions, reach us at smileora.ngo.info@gmail.com"
                    )
                self.state.add_message("agent", reply)
                return reply
            else:
                reply = (
                    f"Please complete the CPP training and quiz first:\n"
                    f"📺 Training video: {CPP_TRAINING_LINK}\n"
                    f"📝 Quiz form: {CPP_QUIZ_LINK}\n\n"
                    f"Once done, type 'check' and we will verify your score."
                )
                self.state.add_message("agent", reply)
                return reply

        # ── ONBOARDING ──────────────────────────────────────────────────────

        # Step 1: Plan (triggered once after login for new volunteers)
        if self.state.status == "new_volunteer" and not self.state.goal:
            plan = self.planner.plan(message)
            self.state.goal = plan.goal
            self.state.tasks = plan.tasks
            self.state.status = "collecting"

        # Step 2: If currently collecting, validate and store the answer
        if self.state.status == "collecting" and self.state.volunteer_data.get("_current_field"):
            field = self.state.volunteer_data.get("_current_field")
            ok, error = self.conversation_manager.store_answer(self.state, field, message)
            if not ok:
                question = FIELD_QUESTIONS.get(field, "Please provide a valid answer.")
                reply = f"⚠️  {error}\n{question}"
                self.state.add_message("agent", reply)
                return reply
            self.state.volunteer_data.pop("_current_field")

        # Step 3: Check if more info is needed
        if not self.conversation_manager.all_collected(self.state):
            next_field = self.conversation_manager.get_next_field(self.state)
            next_question = self.conversation_manager.get_next_question(self.state)
            self.state.volunteer_data["_current_field"] = next_field
            self.state.status = "collecting"
            self.state.add_message("agent", next_question)
            return next_question

        # Step 4: Reflection — show summary and ask for confirmation
        if not self.reflection.is_confirmed(self.state):
            self.state.status = "reflecting"
            d = self.state.volunteer_data

            # 4a: Waiting for new value for a field being corrected
            if d.get("_correction_field"):
                field = d.pop("_correction_field")
                ok, error = self.conversation_manager.store_answer(self.state, field, message)
                if not ok:
                    question = FIELD_QUESTIONS.get(field, "Please provide the correct value.")
                    reply = f"⚠️  {error}\n{question}"
                    d["_correction_field"] = field
                    self.state.add_message("agent", reply)
                    return reply
                d.pop("_reflection_status", None)
                reply = self.reflection.summarize(self.state)
                d["_reflection_status"] = "shown"
                self.state.add_message("agent", reply)
                return reply

            # 4b: Waiting for field name from user (after they said No)
            if d.get("_awaiting_field_name"):
                d.pop("_awaiting_field_name")
                field = message.strip().lower().replace(" ", "_")
                if field in FIELD_QUESTIONS:
                    d["_correction_field"] = field
                    question = FIELD_QUESTIONS[field]
                    reply = f"Please enter the correct value for '{field}':\n{question}"
                    self.state.add_message("agent", reply)
                    return reply
                else:
                    reply = f"⚠️  Field '{field}' not found. Please type a valid field name from the list."
                    d["_awaiting_field_name"] = True
                    self.state.add_message("agent", reply)
                    return reply

            # 4c: Summary already shown — process Yes/No
            if d.get("_reflection_status") == "shown":
                result = self.reflection.process_response(self.state, message)
                if self.reflection.needs_correction(self.state):
                    d["_awaiting_field_name"] = True
                    self.state.add_message("agent", result)
                    return result
                if result:
                    self.state.add_message("agent", result)
                    return result
                # Empty result means confirmed — fall through to execute
                if self.reflection.is_confirmed(self.state):
                    pass  # fall through to Step 5
                else:
                    reply = self.reflection.summarize(self.state)
                    self.state.add_message("agent", reply)
                    return reply
            else:
                # 4d: First time — show summary
                reply = self.reflection.summarize(self.state)
                d["_reflection_status"] = "shown"
                self.state.add_message("agent", reply)
                return reply

        # Step 5: Confirmed — execute → critique → retry or finish
        if self.state.status != "done":
            self.state.status = "executing"
            self._retry_count = 0  # reset before each fresh execution attempt

            while self._retry_count <= MAX_RETRIES:
                attempt = self._retry_count + 1
                if attempt > 1:
                    print(f"\n[Supervisor] Retry attempt {attempt - 1}/{MAX_RETRIES}...\n")
                else:
                    print("\n[Supervisor] Reflection confirmed. Starting execution...\n")

                results = self.executor.execute(self.state)
                report = self.critic.evaluate(results)

                print(f"\n[Critic] {report.summary}\n")

                if report.passed:
                    self.state.status = "done"
                    # cpp_onboarded stays False — registration ≠ onboarding
                    response = (
                        f"✅ {self.state.volunteer_data.get('full_name', 'Volunteer')} has been "
                        f"successfully registered with SmileOra!\n"
                        f"Your Volunteer ID: {self.state.volunteer_data.get('vol_id', 'N/A')}\n"
                        f"A welcome email has been sent to {self.state.volunteer_data.get('email', '')}.\n\n"
                        f"📋 Next Steps — CPP Training (mandatory before volunteering):\n"
                        f"📺 Step 1 — Watch the training video: {CPP_TRAINING_LINK}\n"
                        f"📝 Step 2 — Take the quiz: {CPP_QUIZ_LINK}\n\n"
                        f"Once you have completed the quiz, come back and type 'check' — "
                        f"we will verify your score and fully onboard you."
                    )
                    self.state.add_message("agent", response)
                    return response

                # Hard failures cannot be retried — surface immediately
                if report.hard_failures:
                    self.state.status = "failed"
                    response = (
                        f"❌ Registration could not be completed.\n\n"
                        f"{report.summary}\n\n"
                        f"Please contact smileora.ngo.info@gmail.com for assistance."
                    )
                    self.state.add_message("agent", response)
                    return response

                # Retryable failures — increment counter and loop
                self._retry_count += 1
                if self._retry_count > MAX_RETRIES:
                    break

            # Exhausted retries
            self.state.status = "failed"
            response = (
                f"❌ Registration failed after {MAX_RETRIES} retries.\n\n"
                f"{report.summary}\n\n"
                f"Please contact smileora.ngo.info@gmail.com for assistance."
            )
            self.state.add_message("agent", response)
            return response

        # After successful registration — prompt CPP training
        reply = (
            f"🎉 You are now registered with SmileOra!\n\n"
            f"The next mandatory step is to complete your CPP (Child Protection Policy) training:\n\n"
            f"📺 Step 1 — Watch the training video: {CPP_TRAINING_LINK}\n"
            f"📝 Step 2 — Take the quiz: {CPP_QUIZ_LINK}\n\n"
            f"Once you have completed the quiz, come back and type 'check' — "
            f"we will verify your score and fully onboard you.\n\n"
            f"If you have any questions, reach us at smileora.ngo.info@gmail.com"
        )
        self.state.add_message("agent", reply)
        return reply

    def bulk_load_form(self, form_data: dict) -> None:
        """
        Accept the entire onboarding form at once (from the Streamlit UI).
        Validates every field through the ConversationManager, stores valid
        values, and advances state to 'collecting' so the next handle() call
        skips the Q&A loop and goes straight to Reflection.
        """
        from agent.conversation_manager import OPTIONAL_FIELDS

        errors: dict[str, str] = {}
        for field, value in form_data.items():
            ok, error = self.conversation_manager.store_answer(self.state, field, value)
            if not ok:
                errors[field] = error

        # Cross-field: mobile ≠ emergency contact
        ok, error = self.conversation_manager.validator.validate_unique_numbers(
            form_data.get("mobile_number", ""),
            form_data.get("emergency_contact_number", ""),
        )
        if not ok:
            errors["emergency_contact_number"] = error

        if errors:
            raise ValueError(errors)

        # Plan if not already done
        if not self.state.goal:
            from models.plan import Plan
            self.state.goal = "Volunteer Onboarding"
            self.state.tasks = [
                "Check Existing Volunteer",
                "Collect Details",
                "Validate Information",
                "Confirm Registration",
                "Register Volunteer",
                "Send Welcome Email",
            ]

        # Remove the Q&A cursor — all data is in
        self.state.volunteer_data.pop("_current_field", None)
        # Auto-confirm reflection so execution runs immediately
        self.state.volunteer_data["_reflection_status"] = "confirmed"
        self.state.status = "collecting"
