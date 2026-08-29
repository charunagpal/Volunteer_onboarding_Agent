from agent.state import AgentState


class Reflection:

    def summarize(self, state: AgentState) -> str:
        d = state.volunteer_data
        lines = [
            "📋 Please review your registration details:\n",
            f"  Full Name         : {d.get('full_name', '')}",
            f"  Preferred Name    : {d.get('preferred_name', '') or d.get('full_name', '')}",
            f"  Age               : {d.get('age', '')}",
            f"  Gender            : {d.get('gender', '')}",
            f"  City / Area       : {d.get('city_area', '')}",
            f"  Email             : {d.get('email', '')}",
            f"  Mobile            : {d.get('mobile_number', '')}",
            f"  WhatsApp          : {d.get('whatsapp_number', '')}",
            "",
            f"  Why Volunteer     : {d.get('why_volunteer', '')}",
            f"  Areas of Interest : {d.get('areas_of_interest', '')}",
            f"  Skills            : {d.get('skills_expertise', '')}",
            f"  Experience        : {d.get('previous_experience', '')}",
            f"  Prev Organization : {d.get('previous_organization', '') or 'N/A'}",
            "",
            f"  Preferred Days    : {d.get('preferred_days', '')}",
            f"  Preferred Time    : {d.get('preferred_time', '')}",
            f"  Hours/Week        : {d.get('hours_per_week', '')}",
            f"  Mode              : {d.get('volunteering_mode', '')}",
            f"  Location          : {d.get('preferred_location', '') or 'N/A'}",
            "",
            f"  Emergency Contact : {d.get('emergency_contact_name', '')} "
            f"({d.get('emergency_contact_relationship', '')}) "
            f"— {d.get('emergency_contact_number', '')}",
            "",
            "  Consents          : Code of Conduct ✓  Safeguarding ✓  Contact ✓  Accuracy ✓",
            "",
            "Is all the above information correct? (Yes / No)",
        ]
        return "\n".join(lines)

    def needs_correction(self, state: AgentState) -> bool:
        return state.volunteer_data.get("_reflection_status") == "pending_correction"

    def is_confirmed(self, state: AgentState) -> bool:
        return state.volunteer_data.get("_reflection_status") == "confirmed"

    def process_response(self, state: AgentState, response: str) -> str:
        response = response.strip().lower()

        # User is correcting a specific field
        if state.volunteer_data.get("_correction_field"):
            return ""

        if response == "yes":
            state.volunteer_data["_reflection_status"] = "confirmed"
            return ""

        if response == "no":
            state.volunteer_data["_reflection_status"] = "pending_correction"
            return (
                "Which field would you like to correct?\n"
                "Options: full_name, preferred_name, age, gender, city_area, email, "
                "mobile_number, whatsapp_number, why_volunteer, areas_of_interest, "
                "skills_expertise, previous_experience, preferred_days, preferred_time, "
                "hours_per_week, volunteering_mode, emergency_contact_name, "
                "emergency_contact_relationship, emergency_contact_number"
            )

        return "⚠️  Please answer Yes or No.\nIs all the above information correct? (Yes / No)"
