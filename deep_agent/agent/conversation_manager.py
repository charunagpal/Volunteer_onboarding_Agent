from agent.state import AgentState
from agent.validator import Validator


FIELDS = [
    # Personal
    ("full_name",                       "What is your full name?"),
    ("age",                             "How old are you?"),
    ("gender",                          "What is your gender? (Male / Female / Other)"),
    ("preferred_name",                  "What would you like us to call you? (Press Enter to use your full name)"),
    ("city_area",                       "Which city or area are you from?"),

    # Contact
    ("email",                           "What is your email address?"),
    ("mobile_number",                   "What is your mobile number?"),

    # Motivation & Interests
    ("why_volunteer",                   "Why do you want to volunteer with SmileOra?"),
    ("areas_of_interest",               "What areas are you interested in?\n  Options: Teaching/Education, Child Mentoring, Healthcare, Environment, Animal Welfare, Elderly Care, Fundraising, Social Media/Marketing, Technology/IT, Event Management, Other"),

    # Skills & Experience
    ("skills_expertise",                "What are your key skills or areas of expertise?"),
    ("previous_experience",             "Do you have any previous volunteering experience? If yes, please describe."),
    ("previous_organization",           "Which organization or NGO have you worked with previously? (Press Enter to skip)"),

    # Availability
    ("preferred_days",                  "Which days do you prefer to volunteer? (Friday / Saturday / Sunday)"),
    ("preferred_time",                  "What time of day works best for you? (Morning / Afternoon / Evening)"),
    ("hours_per_week",                  "How many hours per week can you dedicate?"),
    ("volunteering_mode",               "How would you prefer to volunteer? (In-person / Online / Hybrid)"),
    ("preferred_location",              "What is your preferred location for volunteering? (Press Enter to skip)"),

    # Emergency & Safety
    ("emergency_contact_name",          "Please provide your emergency contact's full name."),
    ("emergency_contact_relationship",  "What is your relationship with this emergency contact? (e.g. Parent, Spouse, Friend)"),
    ("emergency_contact_number",        "What is your emergency contact's phone number?"),
    ("safety_information",              "Is there any relevant safety or medical information we should know about? (Press Enter to skip)"),

    # Consent & Declarations
    ("consent_code_of_conduct",         "Do you agree to follow SmileOra's volunteer code of conduct? (Yes / No)"),
    ("consent_safeguarding",            "Do you agree to follow SmileOra's child and vulnerable-person safeguarding policies? (Yes / No)"),
    ("consent_contact",                 "Do you consent to SmileOra contacting you regarding volunteering activities? (Yes / No)"),
    ("consent_photography",             "Do you consent to the use of photographs/videos taken during SmileOra activities? (Yes / No — optional)"),
    ("consent_accuracy",                "Do you confirm that all information provided is accurate and truthful? (Yes / No)"),
]

OPTIONAL_FIELDS = {
    "preferred_name", "previous_organization",
    "preferred_location", "safety_information", "consent_photography",
    "skills_expertise", "previous_experience",
}


class ConversationManager:
    def __init__(self) -> None:
        self.validator = Validator()

    def get_next_question(self, state: AgentState) -> str | None:
        for field, question in FIELDS:
            if field not in state.volunteer_data:
                return question
        return None

    def get_next_field(self, state: AgentState) -> str | None:
        for field, _ in FIELDS:
            if field not in state.volunteer_data:
                return field
        return None

    def store_answer(self, state: AgentState, field: str, answer: str) -> tuple[bool, str]:
        value = answer.strip()

        # Optional fields: allow empty
        if not value and field in OPTIONAL_FIELDS:
            state.volunteer_data[field] = ""
            return True, ""

        # Validate
        ok, error = self.validator.validate(field, value)
        if not ok:
            return False, error

        state.volunteer_data[field] = value
        return True, ""

    def all_collected(self, state: AgentState) -> bool:
        all_fields = {f for f, _ in FIELDS}
        return all_fields.issubset(state.volunteer_data.keys())

