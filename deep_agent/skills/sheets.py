"""
Google Sheets skill — volunteer lookup.

Uses the same OAuth credentials as the Gmail skill (credential.json / token.json)
but requests an additional scope: spreadsheets.readonly.

The token.json will be refreshed automatically once the new scope is granted.
"""
import os
from dataclasses import dataclass

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ── OAuth scopes — must include both Gmail and Sheets ────────────────────────
_SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/spreadsheets.readonly",
]

_DIR             = os.path.dirname(os.path.abspath(__file__))
_CREDENTIALS_FILE = os.path.join(_DIR, "credential.json")
_TOKEN_FILE       = os.path.join(_DIR, "token.json")

# Sheet config — overridden by Config values at call time
_DEFAULT_SHEET_ID  = "1G2ypmcQB6KaUGqOvdfcWIn3OowLFdmSiMBu_jx3uaDo"
_DEFAULT_SHEET_TAB = "Form Responses 1"


CPP_PASS_SCORE = 13   # score must be >= this to pass CPP


@dataclass
class SheetVolunteer:
    """Minimal record returned from the Google Sheet lookup."""
    email: str
    full_name: str
    found: bool
    score: int = 0          # raw numeric score (left side of "14 / 15")
    cpp_passed: bool = False  # True if score >= CPP_PASS_SCORE


def _get_credentials() -> Credentials:
    """Return valid OAuth credentials, re-prompting if the scope changed."""
    creds = None

    if os.path.exists(_TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(_TOKEN_FILE, _SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                # Scope may have changed — force re-auth
                creds = None

        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(
                _CREDENTIALS_FILE, _SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(_TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return creds


def search_volunteer_in_sheet(
    email: str,
    sheet_id: str = _DEFAULT_SHEET_ID,
    sheet_tab: str = _DEFAULT_SHEET_TAB,
) -> SheetVolunteer:
    """
    Search for a volunteer by email in the Google Sheet.

    Returns a SheetVolunteer with found=True and the volunteer's name if the
    email exists, or found=False if not.

    The sheet is expected to have headers in row 1.
    Email column is auto-detected by looking for a header containing 'email'.
    Name column is auto-detected by looking for a header containing 'name'.
    """
    try:
        creds = _get_credentials()
        # Use the Google Sheets API v4 directly via googleapiclient
        # (avoids gspread.authorize() incompatibility with oauth2 Credentials)
        service = build("sheets", "v4", credentials=creds)
        result  = service.spreadsheets().values().get(
            spreadsheetId=sheet_id,
            range=sheet_tab,
        ).execute()
        all_rows = result.get("values", [])
        if not all_rows:
            return SheetVolunteer(email=email, full_name="", found=False)

        headers = [h.strip().lower() for h in all_rows[0]]

        # Auto-detect columns by header keyword
        email_col = next((i for i, h in enumerate(headers) if "email" in h), None)
        name_col  = next((i for i, h in enumerate(headers) if "name"  in h), None)
        score_col = next((i for i, h in enumerate(headers) if "score" in h), None)

        if email_col is None:
            print("[SHEETS] ⚠️  Could not find an 'email' column in the sheet.")
            return SheetVolunteer(email=email, full_name="", found=False)

        # A volunteer may have multiple rows (retakes) — keep the highest score
        best: SheetVolunteer | None = None

        for row in all_rows[1:]:
            if len(row) <= email_col:
                continue
            if row[email_col].strip().lower() != email.strip().lower():
                continue

            full_name = row[name_col].strip() if (
                name_col is not None and len(row) > name_col) else ""

            # Parse score — format is "14 / 15" or plain "14"
            score = 0
            if score_col is not None and len(row) > score_col:
                raw = row[score_col].strip()
                try:
                    score = int(raw.split("/")[0].strip())
                except ValueError:
                    score = 0

            cpp_passed = score >= CPP_PASS_SCORE
            candidate  = SheetVolunteer(
                email=email,
                full_name=full_name,
                found=True,
                score=score,
                cpp_passed=cpp_passed,
            )

            # Keep the attempt with the highest score
            if best is None or score > best.score:
                best = candidate

        if best:
            status = "✅ PASSED" if best.cpp_passed else "❌ FAILED"
            print(f"[SHEETS] Found: {best.full_name} <{email}> "
                  f"| Score: {best.score} | CPP: {status}")
            return best

        print(f"[SHEETS] Email not found: {email}")
        return SheetVolunteer(email=email, full_name="", found=False)

    except Exception as e:
        print(f"[SHEETS] ❌ Error accessing sheet: {e}")
        # Fail gracefully — fall back to XLSX lookup
        return SheetVolunteer(email=email, full_name="", found=False)
