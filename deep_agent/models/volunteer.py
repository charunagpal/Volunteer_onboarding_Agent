from dataclasses import dataclass


@dataclass
class Volunteer:
    # Personal Information
    full_name: str = ""
    preferred_name: str = ""
    age: str = ""
    gender: str = ""

    # Location
    city_area: str = ""

    # Contact
    email: str = ""
    mobile_number: str = ""

    # Motivation
    why_volunteer: str = ""

    # Areas of Interest (comma-separated)
    areas_of_interest: str = ""

    # Skills & Experience
    skills_expertise: str = ""
    previous_experience: str = ""
    previous_organization: str = ""

    # Availability
    preferred_days: str = ""
    preferred_time: str = ""
    hours_per_week: str = ""

    # Mode & Location Preference
    volunteering_mode: str = ""
    preferred_location: str = ""

    # Emergency & Safety
    emergency_contact_name: str = ""
    emergency_contact_relationship: str = ""
    emergency_contact_number: str = ""
    safety_information: str = ""

    # Consent & Declarations
    consent_code_of_conduct: str = ""
    consent_safeguarding: str = ""
    consent_contact: str = ""
    consent_photography: str = ""
    consent_accuracy: str = ""

    # CPP Training
    cpp_training_completed: str = "No"
    cpp_training_date: str = ""

    def is_complete(self) -> bool:
        required = [
            self.full_name, self.age, self.gender,
            self.city_area, self.email, self.mobile_number,
            self.why_volunteer, self.areas_of_interest,
            self.volunteering_mode,
            self.emergency_contact_name, self.emergency_contact_number,
            self.consent_code_of_conduct, self.consent_safeguarding,
            self.consent_contact, self.consent_accuracy,
            # skills_expertise and previous_experience are optional
        ]
        return all(f.strip() for f in required)

    def missing_fields(self) -> list[str]:
        checks = {
            "Full Name":                    self.full_name,
            "Age":                          self.age,
            "Gender":                       self.gender,
            "City / Area":                  self.city_area,
            "Email ID":                     self.email,
            "Mobile Number":                self.mobile_number,
            "Why you want to volunteer":    self.why_volunteer,
            "Areas of Interest":            self.areas_of_interest,
            "Volunteering Mode":            self.volunteering_mode,
            "Emergency Contact Name":       self.emergency_contact_name,
            "Emergency Contact Number":     self.emergency_contact_number,
            "Code of Conduct Consent":      self.consent_code_of_conduct,
            "Safeguarding Consent":         self.consent_safeguarding,
            "Contact Consent":              self.consent_contact,
            "Accuracy Declaration":         self.consent_accuracy,
        }
        return [field for field, value in checks.items() if not value.strip()]
