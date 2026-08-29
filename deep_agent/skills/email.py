import base64
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from models.volunteer import Volunteer

# Gmail API scope — send-only is sufficient
_SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# Paths are relative to this file so they work regardless of cwd
_DIR = os.path.dirname(os.path.abspath(__file__))
_CREDENTIALS_FILE = os.path.join(_DIR, "credential.json")
_TOKEN_FILE = os.path.join(_DIR, "token.json")


def _get_gmail_service():
    """Return an authorised Gmail API service, refreshing or requesting
    credentials as needed."""
    creds = None

    if os.path.exists(_TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(_TOKEN_FILE, _SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                _CREDENTIALS_FILE, _SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(_TOKEN_FILE, "w") as token_file:
            token_file.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def send_welcome_email(volunteer: Volunteer, vol_id: str) -> str:
    name = volunteer.preferred_name or volunteer.full_name
    subject = f"Welcome to SmileOra, {name}! 🎉"
    body = _build_email_body(name, vol_id, volunteer)

    try:
        service = _get_gmail_service()

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["To"] = volunteer.email
        msg.attach(MIMEText(body, "plain"))

        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        service.users().messages().send(
            userId="me", body={"raw": raw}
        ).execute()

        print(f"[EMAIL] ✅ Sent to {volunteer.email}")
        return f"Welcome email sent to {volunteer.email}"

    except HttpError as e:
        print(f"[EMAIL] ❌ Gmail API error: {e}")
        return f"Email failed: {e}"
    except Exception as e:
        print(f"[EMAIL] ❌ Unexpected error: {e}")
        return f"Email failed: {e}"


# CPP links — kept in sync with login_handler.py
_CPP_TRAINING_LINK = "https://cpp-traning.netlify.app/cpp_training_video.html"
_CPP_QUIZ_LINK     = "https://forms.gle/wqeSzfMKQkVKTtdw5"


def _build_email_body(name: str, vol_id: str, volunteer: Volunteer) -> str:
    return f"""Dear {name},

Welcome to SmileOra! 🌟

We are thrilled to have you join our volunteer family.

Your registration details:
  Volunteer ID   : {vol_id}
  Name           : {volunteer.full_name}
  Email          : {volunteer.email}
  Areas of Focus : {volunteer.areas_of_interest}
  Volunteering   : {volunteer.volunteering_mode}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IMPORTANT — Your Next Steps
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Before you can begin volunteering, you must complete the
CPP (Child Protection Policy) training. This is mandatory.

  📺 Step 1 — Watch the training video:
     {_CPP_TRAINING_LINK}

  📝 Step 2 — Take the CPP quiz:
     {_CPP_QUIZ_LINK}

  ✅ Step 3 — Come back to the SmileOra portal and type 'check'
     We will verify your score and fully onboard you.

You need a score of at least 13 / 15 to pass.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If you have any questions, reply to this email or reach us at smileora.ngo.info@gmail.com.

Warm regards,
Team SmileOra
"""
