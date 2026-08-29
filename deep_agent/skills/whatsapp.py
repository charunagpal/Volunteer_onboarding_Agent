from models.volunteer import Volunteer


def send_whatsapp(volunteer: Volunteer, vol_id: str) -> str:
    number = volunteer.whatsapp_number or volunteer.mobile_number
    print(f"\n[WHATSAPP] To: {number}")
    print(f"[WHATSAPP] Hi {volunteer.preferred_name or volunteer.full_name}! 👋")
    print(f"[WHATSAPP] Welcome to SmileOra! Your Volunteer ID: {vol_id}")
    return f"WhatsApp message sent to {number}"
