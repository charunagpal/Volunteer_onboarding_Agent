import re


class Validator:

    def validate(self, field: str, value: str) -> tuple[bool, str]:
        value = value.strip()

        if not value:
            return False, "This field cannot be empty. Please provide a valid answer."

        method = getattr(self, f"_validate_{field}", None)
        if method:
            return method(value)
        return True, ""

    def _validate_age(self, value: str) -> tuple[bool, str]:
        if not value.isdigit():
            return False, "Age must be a number. Please enter a valid age."
        age = int(value)
        if not (16 <= age <= 80):
            return False, "Age must be between 16 and 80."
        return True, ""

    def _validate_email(self, value: str) -> tuple[bool, str]:
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not re.match(pattern, value):
            return False, "Please enter a valid email address (e.g. name@example.com)."
        return True, ""

    def _validate_mobile_number(self, value: str) -> tuple[bool, str]:
        digits = re.sub(r"[\s\-\+]", "", value)
        if not digits.isdigit() or len(digits) < 10:
            return False, "Please enter a valid mobile number (at least 10 digits)."
        return True, ""

    def _validate_emergency_contact_number(self, value: str) -> tuple[bool, str]:
        return self._validate_mobile_number(value)

    def validate_unique_numbers(self, mobile: str, emergency: str) -> tuple[bool, str]:
        """Cross-field check — mobile and emergency contact must differ."""
        if mobile.strip() and emergency.strip() and mobile.strip() == emergency.strip():
            return False, "Emergency contact number must be different from your mobile number."
        return True, ""

    def _validate_gender(self, value: str) -> tuple[bool, str]:
        allowed = {"male", "female", "other"}
        if value.lower() not in allowed:
            return False, "Please enter Male, Female, or Other."
        return True, ""

    def _validate_volunteering_mode(self, value: str) -> tuple[bool, str]:
        allowed = {"in-person", "online", "hybrid"}
        if value.lower() not in allowed:
            return False, "Please enter In-person, Online, or Hybrid."
        return True, ""

    def _validate_hours_per_week(self, value: str) -> tuple[bool, str]:
        allowed = {"2 hours/week", "4 hours/week", "6 hours/week", "8 hours/week"}
        if value not in allowed:
            return False, "Please select a valid option: 2, 4, 6, or 8 hours/week."
        return True, ""

    def _validate_consent_code_of_conduct(self, value: str) -> tuple[bool, str]:
        return self._validate_yes_no(value)

    def _validate_consent_safeguarding(self, value: str) -> tuple[bool, str]:
        return self._validate_yes_no(value)

    def _validate_consent_contact(self, value: str) -> tuple[bool, str]:
        return self._validate_yes_no(value)

    def _validate_consent_photography(self, value: str) -> tuple[bool, str]:
        if not value:
            return True, ""
        return self._validate_yes_no(value)

    def _validate_consent_accuracy(self, value: str) -> tuple[bool, str]:
        ok, msg = self._validate_yes_no(value)
        if ok and value.lower() == "no":
            return False, "You must confirm that the information provided is accurate to complete registration."
        return ok, msg

    def _validate_yes_no(self, value: str) -> tuple[bool, str]:
        if value.lower() not in {"yes", "no"}:
            return False, "Please answer Yes or No."
        return True, ""
