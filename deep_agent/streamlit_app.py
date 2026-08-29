import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from PIL import Image
from config import Config
from agent.supervisor import Supervisor

# ── Logo path ─────────────────────────────────────────────────────────────────
_DIR      = os.path.dirname(os.path.abspath(__file__))
_LOGO_PATH = os.path.join(_DIR, "SmileOraLego.png")
_logo = Image.open(_LOGO_PATH) if os.path.exists(_LOGO_PATH) else None

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SmileOra — Volunteer Onboarding",
    page_icon=_logo if _logo else "🌟",
    layout="centered",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.stApp { background-color: #f9fafb; }

/* Chat bubbles */
.user-bubble {
    background: #3b82f6; color: #fff;
    border-radius: 18px 18px 4px 18px;
    padding: 10px 16px; margin: 4px 0;
    max-width: 78%; margin-left: auto;
    font-size: .93rem; line-height: 1.55;
    word-wrap: break-word;
}
.agent-bubble {
    background: #fff; color: #1f2328;
    border-radius: 18px 18px 18px 4px;
    padding: 10px 16px; margin: 4px 0;
    max-width: 82%; border: 1px solid #e5e7eb;
    font-size: .93rem; line-height: 1.55;
    white-space: pre-wrap; word-wrap: break-word;
}
.chat-row-user  { display:flex; justify-content:flex-end;  margin:6px 0; }
.chat-row-agent { display:flex; justify-content:flex-start; margin:6px 0; }
.avatar {
    width:32px; height:32px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-size:1rem; flex-shrink:0;
}
.avatar-agent { background:#fef3c7; margin-right:8px; }
.avatar-user  { background:#dbeafe; margin-left:8px;  }

/* Section headers inside the form */
.form-section {
    font-weight: 600; font-size: .85rem;
    color: #57606a; letter-spacing: .06em;
    text-transform: uppercase;
    margin: 18px 0 4px 0;
    padding-bottom: 4px;
    border-bottom: 1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _add_chat(role: str, content: str) -> None:
    st.session_state.messages.append({"role": role, "content": content})


def _render_chat() -> None:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="chat-row-user">'
                f'<div class="user-bubble">{msg["content"]}</div>'
                f'<div class="avatar avatar-user">🙂</div>'
                f'</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="chat-row-agent">'
                f'<div class="avatar avatar-agent">🌟</div>'
                f'<div class="agent-bubble">{msg["content"]}</div>'
                f'</div>', unsafe_allow_html=True)


def _init_session() -> None:
    if "supervisor" not in st.session_state:
        config = Config()
        sup = Supervisor(config)
        first = sup.handle("hello")
        st.session_state.supervisor = sup
        st.session_state.messages   = [{"role": "agent", "content": first}]
        st.session_state.show_form  = False   # True = render registration form
        st.session_state.form_errors = {}     # field → error message


# ── Registration form ─────────────────────────────────────────────────────────

def _render_registration_form() -> None:
    """Render the full onboarding form using Streamlit native widgets."""

    errors: dict = st.session_state.get("form_errors", {})
    pre: dict    = st.session_state.get("form_prefill", {})  # e.g. email already known

    def _err(field: str) -> None:
        if field in errors:
            st.error(errors[field])

    st.markdown("---")
    st.markdown("### 📋 Volunteer Registration Form")
    st.caption("Fill in all sections and click **Submit** — no back-and-forth needed.")

    with st.form("registration_form", clear_on_submit=False):

        # ── Personal ──────────────────────────────────────────────────────────
        st.markdown('<div class="form-section">Personal Information</div>',
                    unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        full_name      = c1.text_input("Full Name *",
                                       value=pre.get("full_name", ""))
        preferred_name = c2.text_input("Preferred Name (optional)",
                                       value=pre.get("preferred_name", ""))
        _err("full_name")

        CITY_OPTIONS = [
            "",
            "Bangalore - Bannerghatta Road",
            "Bangalore - Haraluru",
            "Bangalore - Whitefield",
            "Bangalore - Koramangala",
            "Other",
        ]
        saved_city = pre.get("city_area", "")
        city_default_idx = CITY_OPTIONS.index(saved_city) if saved_city in CITY_OPTIONS else 0

        c3, c4 = st.columns(2)
        age    = c3.text_input("Age *", value=pre.get("age", ""))
        gender = c4.selectbox("Gender *",
                              ["", "Male", "Female", "Other"],
                              index=["", "Male", "Female", "Other"].index(
                                  pre.get("gender", "")) if pre.get("gender", "") in
                                  ["", "Male", "Female", "Other"] else 0)
        _err("age"); _err("gender")

        city_area = st.selectbox("City / Area *", CITY_OPTIONS,
                                 index=city_default_idx)
        _err("city_area")

        # ── Contact ───────────────────────────────────────────────────────────
        st.markdown('<div class="form-section">Contact Details</div>',
                    unsafe_allow_html=True)
        c6, c7 = st.columns(2)
        email         = c6.text_input("Email *",
                                      value=pre.get("email", ""))
        mobile_number = c7.text_input("Mobile Number *",
                                      value=pre.get("mobile_number", ""))
        _err("email"); _err("mobile_number")

        # ── Motivation ────────────────────────────────────────────────────────
        st.markdown('<div class="form-section">Motivation & Interests</div>',
                    unsafe_allow_html=True)
        why_volunteer = st.text_area(
            "Why do you want to volunteer with SmileOra? *",
            value=pre.get("why_volunteer", ""), height=90)
        _err("why_volunteer")

        INTEREST_OPTIONS = [
            "Teaching / Education", "Child Mentoring", "Healthcare",
            "Environment", "Animal Welfare", "Elderly Care",
            "Fundraising", "Social Media / Marketing",
            "Technology / IT", "Event Management", "Other",
        ]
        raw_interests = pre.get("areas_of_interest", "")
        default_interests = [i for i in raw_interests.split(", ") if i in INTEREST_OPTIONS]
        areas_of_interest = st.multiselect(
            "Areas of Interest *", INTEREST_OPTIONS,
            default=default_interests)
        _err("areas_of_interest")

        # ── Skills & Experience ───────────────────────────────────────────────
        st.markdown('<div class="form-section">Skills & Experience</div>',
                    unsafe_allow_html=True)
        c8, c9 = st.columns(2)
        skills_expertise   = c8.text_area("Key Skills / Expertise (optional)",
                                          value=pre.get("skills_expertise", ""),
                                          height=80)
        previous_experience = c9.text_area("Previous Volunteering Experience (optional)",
                                           value=pre.get("previous_experience", ""),
                                           height=80)
        previous_organization = st.text_input(
            "Previous Organisation (optional)",
            value=pre.get("previous_organization", ""))
        _err("skills_expertise"); _err("previous_experience")

        # ── Availability ──────────────────────────────────────────────────────
        st.markdown('<div class="form-section">Availability</div>',
                    unsafe_allow_html=True)
        DAY_OPTIONS  = ["Friday", "Saturday", "Sunday"]
        raw_days     = pre.get("preferred_days", "")
        default_days = [d for d in raw_days.split(", ") if d in DAY_OPTIONS]
        preferred_days = st.multiselect("Preferred Days *", DAY_OPTIONS,
                                        default=default_days)
        _err("preferred_days")

        c10, c11, c12 = st.columns(3)
        preferred_time  = c10.selectbox(
            "Preferred Time *",
            ["", "Morning", "Afternoon"],
            index=["", "Morning", "Afternoon"].index(
                pre.get("preferred_time", ""))
            if pre.get("preferred_time","") in ["","Morning","Afternoon"] else 0)
        hours_per_week  = c11.selectbox(
            "Hours / Week *",
            ["", "2 hours/week", "4 hours/week", "6 hours/week", "8 hours/week"],
            index=["", "2 hours/week", "4 hours/week", "6 hours/week", "8 hours/week"].index(
                pre.get("hours_per_week", ""))
            if pre.get("hours_per_week", "") in ["", "2 hours/week", "4 hours/week", "6 hours/week", "8 hours/week"] else 0)
        volunteering_mode = c12.selectbox(
            "Mode *",
            ["", "In-person", "Online", "Hybrid"],
            index=["","In-person","Online","Hybrid"].index(
                pre.get("volunteering_mode",""))
            if pre.get("volunteering_mode","") in ["","In-person","Online","Hybrid"] else 0)
        _err("preferred_time"); _err("hours_per_week"); _err("volunteering_mode")

        preferred_location = st.text_input(
            "Preferred Location (optional)",
            value=pre.get("preferred_location", ""))

        # ── Emergency Contact ─────────────────────────────────────────────────
        st.markdown('<div class="form-section">Emergency Contact</div>',
                    unsafe_allow_html=True)
        c13, c14, c15 = st.columns(3)
        emergency_contact_name         = c13.text_input(
            "Contact Full Name *",
            value=pre.get("emergency_contact_name", ""))
        emergency_contact_relationship = c14.text_input(
            "Relationship *",
            value=pre.get("emergency_contact_relationship", ""))
        emergency_contact_number       = c15.text_input(
            "Phone Number *",
            value=pre.get("emergency_contact_number", ""))
        _err("emergency_contact_name")
        _err("emergency_contact_relationship")
        _err("emergency_contact_number")

        safety_information = st.text_input(
            "Safety / Medical Information (optional)",
            value=pre.get("safety_information", ""))

        # ── Consents ──────────────────────────────────────────────────────────
        st.markdown('<div class="form-section">Consents & Declarations</div>',
                    unsafe_allow_html=True)
        st.caption("All fields marked * below are required to complete registration.")

        consent_code_of_conduct = st.checkbox(
            "✅ I agree to follow SmileOra's **Volunteer Code of Conduct** *",
            value=pre.get("consent_code_of_conduct","").lower() == "yes")
        consent_safeguarding    = st.checkbox(
            "✅ I agree to follow SmileOra's **Child & Vulnerable Person Safeguarding** policies *",
            value=pre.get("consent_safeguarding","").lower() == "yes")
        consent_contact         = st.checkbox(
            "✅ I consent to SmileOra contacting me about volunteering activities *",
            value=pre.get("consent_contact","").lower() == "yes")
        consent_photography     = st.checkbox(
            "📷 I consent to the use of photographs/videos taken during SmileOra activities (optional)",
            value=pre.get("consent_photography","").lower() == "yes")
        consent_accuracy        = st.checkbox(
            "✅ I confirm that all information provided is **accurate and truthful** *",
            value=pre.get("consent_accuracy","").lower() == "yes")

        for f in ["consent_code_of_conduct","consent_safeguarding",
                  "consent_contact","consent_accuracy"]:
            _err(f)

        st.markdown("---")
        submitted = st.form_submit_button(
            "🚀 Submit Registration", use_container_width=True,
            type="primary")

    # ── Handle form submission ─────────────────────────────────────────────────
    if submitted:
        mob = mobile_number.strip()
        emg = emergency_contact_number.strip()

        # Client-side uniqueness check before hitting the server
        if mob and emg and mob == emg:
            st.session_state.form_errors = {
                "emergency_contact_number":
                    "Emergency contact number must be different from your mobile number."
            }
            st.rerun()

        form_data = {
            "full_name":                       full_name.strip(),
            "preferred_name":                  preferred_name.strip(),
            "age":                             age.strip(),
            "gender":                          gender,
            "city_area":                       city_area.strip(),
            "email":                           email.strip(),
            "mobile_number":                   mob,
            "why_volunteer":                   why_volunteer.strip(),
            "areas_of_interest":               ", ".join(areas_of_interest),
            "skills_expertise":                skills_expertise.strip(),
            "previous_experience":             previous_experience.strip(),
            "previous_organization":           previous_organization.strip(),
            "preferred_days":                  ", ".join(preferred_days),
            "preferred_time":                  preferred_time,
            "hours_per_week":                  hours_per_week.strip(),
            "volunteering_mode":               volunteering_mode,
            "preferred_location":              preferred_location.strip(),
            "emergency_contact_name":          emergency_contact_name.strip(),
            "emergency_contact_relationship":  emergency_contact_relationship.strip(),
            "emergency_contact_number":        emg,
            "safety_information":              safety_information.strip(),
            "consent_code_of_conduct":         "Yes" if consent_code_of_conduct else "No",
            "consent_safeguarding":            "Yes" if consent_safeguarding else "No",
            "consent_contact":                 "Yes" if consent_contact else "No",
            "consent_photography":             "Yes" if consent_photography else "No",
            "consent_accuracy":                "Yes" if consent_accuracy else "No",
        }

        # Store prefill so form re-renders with values if there are errors
        st.session_state.form_prefill = form_data

        try:
            sup = st.session_state.supervisor
            sup.bulk_load_form(form_data)
            st.session_state.form_errors = {}
            st.session_state.show_form   = False

            # Log a friendly summary into the chat
            _add_chat("user", f"[Submitted registration form for {form_data['full_name']}]")

            # Trigger the reflection step
            with st.spinner("Processing your registration..."):
                response = sup.handle("form submitted")
            _add_chat("agent", response)
            st.rerun()

        except ValueError as exc:
            st.session_state.form_errors = exc.args[0]
            st.rerun()


# ── Main ──────────────────────────────────────────────────────────────────────

_init_session()

# ── Header ────────────────────────────────────────────────────────────────────
_hcol1, _hcol2 = st.columns([1, 6])
with _hcol1:
    if _logo:
        st.image(_logo, width=72)
    else:
        st.markdown("## 🌟")
with _hcol2:
    st.markdown("## SmileOra Volunteer Assistant")
    st.markdown(
        "<p style='color:#57606a; margin-top:-10px; font-size:.9rem;'>"
        "Onboarding · Help · Support</p>",
        unsafe_allow_html=True)
st.divider()

sup    = st.session_state.supervisor
status = sup.state.status

# ── Show registration form when agent has identified a new volunteer ──────────
if status in ("new_volunteer", "collecting") and not sup.conversation_manager.all_collected(sup.state):
    st.session_state.show_form = True
    # Pre-fill email from state (already captured at login)
    if "form_prefill" not in st.session_state:
        st.session_state.form_prefill = {
            "email": sup.state.volunteer_data.get("email", "")
        }

# ── Render chat + form ────────────────────────────────────────────────────────
_render_chat()

if st.session_state.show_form:
    _render_registration_form()
else:
    # ── Normal chat input ─────────────────────────────────────────────────────
    with st.form(key="chat_form", clear_on_submit=True):
        c1, c2 = st.columns([8, 1])
        with c1:
            user_input = st.text_input(
                "message", placeholder="Type your message here...",
                label_visibility="collapsed")
        with c2:
            send = st.form_submit_button("➤", use_container_width=True)

    if send and user_input.strip():
        txt = user_input.strip()
        _add_chat("user", txt)
        with st.spinner(""):
            reply = sup.handle(txt)
        _add_chat("agent", reply)

        # If agent moved to new_volunteer, pop the form open next render
        if sup.state.status in ("new_volunteer", "collecting") \
                and not sup.conversation_manager.all_collected(sup.state):
            st.session_state.show_form = True
            if "form_prefill" not in st.session_state:
                st.session_state.form_prefill = {
                    "email": sup.state.volunteer_data.get("email", "")
                }

        st.rerun()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    if _logo:
        st.image(_logo, width=90)
    else:
        st.markdown("### SmileOra")
    st.markdown(
        "<p style='color:#57606a;font-size:.85rem;'>Volunteer Onboarding Assistant</p>",
        unsafe_allow_html=True)
    st.divider()

    status_labels = {
        "idle":           ("⬜", "Idle"),
        "awaiting_email": ("🔵", "Identifying volunteer"),
        "new_volunteer":  ("🟡", "New volunteer"),
        "cpp_pending":    ("🟠", "CPP training pending"),
        "collecting":     ("🟡", "Filling form"),
        "reflecting":     ("🔵", "Reviewing details"),
        "executing":      ("🟣", "Registering"),
        "done":           ("🟢", "Registered"),
        "failed":         ("🔴", "Failed"),
    }
    icon, label = status_labels.get(status, ("⬜", status))
    st.markdown(f"**Status:** {icon} {label}")

    progress_map = {
        "idle": 0, "awaiting_email": 10, "new_volunteer": 15,
        "collecting": 45, "reflecting": 75, "executing": 90,
        "done": 70, "failed": 100, "cpp_pending": 50,
    }
    # CPP passed = full 100%
    progress_val = 100 if sup.state.cpp_onboarded else progress_map.get(status, 0)
    st.progress(progress_val)

    st.divider()

    # ── Volunteer info card (shown once email is known) ───────────────────────
    vol_name  = (sup.state.volunteer_data.get("full_name", "")
                 or sup.state.volunteer_data.get("preferred_name", ""))
    vol_email = sup.state.volunteer_data.get("email", "")
    vol_id    = sup.state.volunteer_data.get("vol_id", "")
    cpp_score = sup.state.volunteer_data.get("cpp_score", "")
    registered = status in ("done", "cpp_pending", "executing")
    cpp_done   = sup.state.cpp_onboarded

    if vol_email:
        # Registration row
        reg_icon  = "✅" if registered else "🔲"
        reg_label = "Done" if registered else "Pending"
        reg_color = "#15803d" if registered else "#92400e"

        # CPP row
        cpp_icon  = "✅" if cpp_done else "🔲"
        cpp_label = "Completed" if cpp_done else "Pending"
        cpp_color = "#15803d" if cpp_done else "#92400e"

        rows  = ""
        if vol_name:
            rows += f"<tr><td>👤</td><td><b>Name</b></td><td>{vol_name}</td></tr>"
        if vol_email:
            rows += f"<tr><td>📧</td><td><b>Email</b></td><td style='word-break:break-all'>{vol_email}</td></tr>"
        if vol_id:
            rows += f"<tr><td>🪪</td><td><b>ID</b></td><td>{vol_id}</td></tr>"
        if cpp_score:
            rows += f"<tr><td>📊</td><td><b>CPP Score</b></td><td>{cpp_score} / 15</td></tr>"
        rows += (
            f"<tr><td>{reg_icon}</td><td><b>Registration</b></td>"
            f"<td style='color:{reg_color}'>{reg_label}</td></tr>"
            f"<tr><td>{cpp_icon}</td><td><b>CPP Training</b></td>"
            f"<td style='color:{cpp_color}'>{cpp_label}</td></tr>"
        )

        title      = "🎉 Onboarding Complete" if cpp_done else "📋 Volunteer Status"
        card_bg    = "#f0fdf4" if cpp_done else "#fffbeb"
        card_border = "#86efac" if cpp_done else "#fcd34d"
        title_color = "#15803d" if cpp_done else "#92400e"

        st.markdown(
            "<div style='background:" + card_bg + ";border:1px solid " + card_border + ";"
            "border-radius:10px;padding:14px 16px;'>"
            "<div style='font-weight:700;color:" + title_color + ";font-size:.9rem;"
            "text-align:center;margin-bottom:10px;'>" + title + "</div>"
            "<table style='font-size:.8rem;color:#1f2328;width:100%;"
            "border-collapse:collapse;line-height:1.9;'>"
            + rows +
            "</table></div>",
            unsafe_allow_html=True,
        )

    st.divider()
    if st.button("🔄 Start over", use_container_width=True):
        for k in ("supervisor","messages","show_form","form_errors","form_prefill"):
            st.session_state.pop(k, None)
        st.rerun()

    st.markdown(
        "<p style='color:#57606a;font-size:.75rem;margin-top:24px;'>"
        "SmileOra NGO · smileora.ngo.info@gmail.com</p>",
        unsafe_allow_html=True)
