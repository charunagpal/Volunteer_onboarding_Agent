from agent.state import AgentState
from models.volunteer import Volunteer
from models.execution import ExecutionResult
from skills.volunteer import search_volunteer, create_volunteer
from skills.email import send_welcome_email
from skills.whatsapp import send_whatsapp


class Executor:
    def __init__(self) -> None:
        self.task_map = {
            "Check Existing Volunteer": self._check_existing_volunteer,
            "Collect Details":          self._collect_details,
            "Validate Information":     self._validate_information,
            "Confirm Registration":     self._confirm_registration,
            "Register Volunteer":       self._register_volunteer,
            "Send Welcome Email":       self._send_welcome_email,
        }

    def execute(self, state: AgentState) -> list[ExecutionResult]:
        results: list[ExecutionResult] = []
        for task in state.tasks:
            handler = self.task_map.get(task)
            if handler:
                result: ExecutionResult = handler(state)
            else:
                result = ExecutionResult(
                    task=task,
                    success=False,
                    message=f"No handler found for task: '{task}'",
                    retryable=False,
                )
            print(f"  → {task}: {'✅' if result.success else '❌'} {result.message}")
            results.append(result)
        return results

    def _check_existing_volunteer(self, state: AgentState) -> ExecutionResult:
        email = state.volunteer_data.get("email", "")
        if not email:
            return ExecutionResult(
                task="Check Existing Volunteer",
                success=False,
                message="No email provided yet.",
                retryable=False,
            )
        existing = search_volunteer(email)
        if existing:
            state.volunteer_data["already_registered"] = True
            return ExecutionResult(
                task="Check Existing Volunteer",
                success=True,
                message=f"Volunteer already registered with email {email}.",
            )
        return ExecutionResult(
            task="Check Existing Volunteer",
            success=True,
            message="Volunteer not found. Proceeding with registration.",
        )

    def _collect_details(self, state: AgentState) -> ExecutionResult:
        volunteer = self._build_volunteer(state)
        missing = volunteer.missing_fields()
        if missing:
            return ExecutionResult(
                task="Collect Details",
                success=False,
                message=f"Missing fields: {', '.join(missing)}",
                retryable=False,
            )
        return ExecutionResult(
            task="Collect Details",
            success=True,
            message="All required details collected.",
        )

    def _validate_information(self, state: AgentState) -> ExecutionResult:
        volunteer = self._build_volunteer(state)
        if not volunteer.is_complete():
            missing = volunteer.missing_fields()
            return ExecutionResult(
                task="Validate Information",
                success=False,
                message=f"Validation failed. Missing: {', '.join(missing)}",
                retryable=False,
            )
        return ExecutionResult(
            task="Validate Information",
            success=True,
            message="Information validated successfully.",
        )

    def _confirm_registration(self, state: AgentState) -> ExecutionResult:
        return ExecutionResult(
            task="Confirm Registration",
            success=True,
            message="Registration confirmed.",
        )

    def _register_volunteer(self, state: AgentState) -> ExecutionResult:
        if state.volunteer_data.get("already_registered"):
            return ExecutionResult(
                task="Register Volunteer",
                success=True,
                message="Volunteer already registered. Skipping.",
            )
        try:
            volunteer = self._build_volunteer(state)
            vol_id = create_volunteer(volunteer)
            state.volunteer_data["vol_id"] = vol_id
            return ExecutionResult(
                task="Register Volunteer",
                success=True,
                message=f"Volunteer registered successfully. ID: {vol_id}",
            )
        except Exception as e:
            return ExecutionResult(
                task="Register Volunteer",
                success=False,
                message=f"Failed to write volunteer record: {e}",
                retryable=True,
            )

    def _send_welcome_email(self, state: AgentState) -> ExecutionResult:
        try:
            volunteer = self._build_volunteer(state)
            vol_id = state.volunteer_data.get("vol_id", "VOL-0000")
            email_result = send_welcome_email(volunteer, vol_id)
            send_whatsapp(volunteer, vol_id)
            return ExecutionResult(
                task="Send Welcome Email",
                success=True,
                message=email_result,
            )
        except Exception as e:
            return ExecutionResult(
                task="Send Welcome Email",
                success=False,
                message=f"Failed to send welcome email: {e}",
                retryable=True,
            )

    def _build_volunteer(self, state: AgentState) -> Volunteer:
        d = state.volunteer_data
        v = Volunteer()
        v.full_name                     = d.get("full_name", "")
        v.preferred_name                = d.get("preferred_name", "")
        v.age                           = d.get("age", "")
        v.gender                        = d.get("gender", "")
        v.city_area                     = d.get("city_area", "")
        v.email                         = d.get("email", "")
        v.mobile_number                 = d.get("mobile_number", "")
        v.whatsapp_number               = d.get("whatsapp_number", "")
        v.why_volunteer                 = d.get("why_volunteer", "")
        v.areas_of_interest             = d.get("areas_of_interest", "")
        v.skills_expertise              = d.get("skills_expertise", "")
        v.previous_experience           = d.get("previous_experience", "")
        v.previous_organization         = d.get("previous_organization", "")
        v.preferred_days                = d.get("preferred_days", "")
        v.preferred_time                = d.get("preferred_time", "")
        v.hours_per_week                = d.get("hours_per_week", "")
        v.volunteering_mode             = d.get("volunteering_mode", "")
        v.preferred_location            = d.get("preferred_location", "")
        v.emergency_contact_name        = d.get("emergency_contact_name", "")
        v.emergency_contact_relationship = d.get("emergency_contact_relationship", "")
        v.emergency_contact_number      = d.get("emergency_contact_number", "")
        v.safety_information            = d.get("safety_information", "")
        v.consent_code_of_conduct       = d.get("consent_code_of_conduct", "")
        v.consent_safeguarding          = d.get("consent_safeguarding", "")
        v.consent_contact               = d.get("consent_contact", "")
        v.consent_photography           = d.get("consent_photography", "")
        v.consent_accuracy              = d.get("consent_accuracy", "")
        return v
