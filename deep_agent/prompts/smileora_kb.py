"""
SmileOra Static Knowledge Base
===============================
Single source of truth for all information about SmileOra.

PUBLIC_KB   — shown to anyone, even before registration.
              Covers: what SmileOra is, mission, vision, who it helps,
              types of events/activities, certificates, contact, how to join.
              Does NOT reveal specific event dates, times, or locations.

MEMBERS_KB  — shown ONLY to fully onboarded volunteers (registered + CPP passed).
              Adds: specific upcoming event dates, times, venue details,
              and coordinator contact details for active events.
"""

# ── Public information — safe for anyone ──────────────────────────────────────

PUBLIC_KB = """
# SmileOra – Public Information

## 1. About SmileOra

Organization/Project Name: SmileOra
Tagline: Spreading Smile
Started: 2024

What is SmileOra?

SmileOra is a community-driven volunteering initiative focused on spreading happiness,
creating meaningful connections, and encouraging a culture of kindness and mutual support.

The initiative connects volunteers with different communities, including children from
underserved communities, elderly people in retirement or old-age homes, and other groups
that may benefit from companionship, mentorship, education, and support.

Philosophy: "Do whatever you can. Help wherever you can. Spread happiness wherever you can."

---

## 2. Mission

SmileOra's mission is to create meaningful human connections and contribute to a
happier and more compassionate society.

The initiative focuses on:
- Spreading happiness and kindness
- Building meaningful relationships
- Bridging the generation gap
- Mentoring and supporting children
- Providing companionship to elderly people
- Encouraging volunteers to contribute their time and skills
- Building a culture of mutual respect and assistance

---

## 3. Vision

SmileOra aims to contribute toward building a happier India, one smile at a time.

The vision is to create communities where people care about each other, help each other,
respect each other, and actively contribute to society.

---

## 4. Types of Activities & Events SmileOra Conducts

SmileOra regularly conducts the following types of volunteering activities:

### Children-focused activities
- Teaching and mentoring sessions at community learning centres
- Educational games and creative activities
- Value education and storytelling sessions
- Health and hygiene awareness activities
- Interactive and fun sessions with children

### Elderly-focused activities
- Weekly visits and social interaction at old-age and retirement homes
- Games, conversations, and celebrations
- Companionship and sharing experiences

### Community events
- Awareness drives and community initiatives
- Fundraising and outreach activities
- Environmental and animal welfare activities

Events are held on **Fridays, Saturdays, and Sundays**.
Specific dates, timings, and venue details are shared with registered and
CPP-trained volunteers once onboarding is complete.

---

## 5. Who Does SmileOra Help?

- **Children** from underserved communities — through NGO and learning centre collaborations
- **Elderly people** in old-age and retirement homes
- **Animals** and broader community groups

---

## 6. Certificates & Benefits

- **CPP Training Completion Certificate** — issued to every volunteer who passes the
  Child Protection Policy (CPP) quiz with a score of 13 or more out of 15
- **Certificate of Appreciation** — awarded to volunteers who complete **8 or more
  events within any 4-month timeframe**. To claim it, email smileora.ngo.info@gmail.com
  with your name, volunteer ID, and the list of events attended.
- **Certificate of Participation** — issued to volunteers who complete their
  volunteering commitment with SmileOra
- Opportunity to join the SmileOra **core team**
- Appropriate **training** for volunteers working with children and vulnerable communities
- Meaningful experiences, relationships, and a sense of social contribution

---

## 7. Volunteer Responsibilities

Volunteers are expected to:
- Respect the communities they work with
- Follow safety and child-protection guidelines
- Maintain appropriate boundaries
- Participate responsibly and follow coordinator instructions

---

## 8. Volunteer Community

SmileOra has a community of 100+ volunteers across Bangalore.

---

## 9. History

SmileOra started in 2024 as part of the Volship Fellowship conducted by
Volunteer For India (VFI), which is associated with YuWaah and UNICEF.

---

## 10. Online Presence

Blog: https://spreadingsmilesbangalore.blogspot.com
Instagram: https://www.instagram.com/spreadingsmiles.bangalore_ngo/

---

## 11. How to Join

To become a SmileOra volunteer:
1. Enter your email on the SmileOra Volunteer Portal.
2. If you are new, fill in the registration form.
3. After registering, complete the mandatory CPP (Child Protection Policy) training.
4. Once you pass the CPP quiz (score ≥ 13/15), you will be fully onboarded and
   will receive details of upcoming events, timings, and locations.

The CPP training video and quiz links are shared with you automatically after
you complete registration on the SmileOra Volunteer Portal.

---

## 12. Frequently Asked Questions (Public)

Q: What is SmileOra?
A: SmileOra is a volunteering initiative focused on spreading happiness, building
   meaningful connections, mentoring communities, and creating a culture of kindness.

Q: When did SmileOra start?
A: SmileOra started in 2024.

Q: Does SmileOra work only with children?
A: No. SmileOra works with children, elderly people, animals, and other communities.

Q: What kind of events does SmileOra conduct?
A: Teaching and mentoring sessions with children, visits to old-age homes, community
   awareness events, and other volunteering activities. Events happen on Fridays,
   Saturdays, and Sundays. Specific dates and venues are shared after onboarding.

Q: Do volunteers get certificates?
A: Yes. SmileOra provides three certificates:
   1. **CPP Training Completion Certificate** — issued after passing the CPP quiz
      (score ≥ 13/15). This is mandatory and is the first certificate you receive.
   2. **Certificate of Appreciation** — awarded to volunteers who attend 8 or more
      events within any 4-month timeframe. Email smileora.ngo.info@gmail.com with
      your name, volunteer ID, and list of events attended to claim it.
   3. **Certificate of Participation** — issued to volunteers who complete their
      volunteering commitment with SmileOra.

Q: How do I get the Certificate of Appreciation?
A: Attend at least 8 SmileOra events within any 4-month period. Once you have reached
   that milestone, email smileora.ngo.info@gmail.com with your name, volunteer ID,
   and the list of events you attended. SmileOra will verify and issue the certificate.

Q: Is volunteering paid?
A: No. Volunteering is unpaid. Volunteers receive a certificate and the satisfaction
   of creating real impact.

Q: What is the CPP training?
A: The Child Protection Policy (CPP) training educates volunteers on safeguarding
   children from abuse, neglect, and harm. It is mandatory for all volunteers.
   You need to score at least 13 out of 15 to pass.
   The CPP training video and quiz links are shared with you after you register
   on the SmileOra Volunteer Portal.

Q: Can I volunteer online?
A: SmileOra offers in-person, online, and hybrid volunteering options.

Q: What areas does SmileOra serve?
A: Bangalore — including Bannerghatta Road, Haraluru, Whitefield, and Koramangala.

Q: How do I contact SmileOra?
A: Email: smileora.ngo.info@gmail.com
   Blog: https://spreadingsmilesbangalore.blogspot.com
   Instagram: https://www.instagram.com/spreadingsmiles.bangalore_ngo/
"""


# ── Members-only information — shown only after registration + CPP passed ─────

MEMBERS_KB = PUBLIC_KB + """
---

# SmileOra – Member Information (Registered & CPP-Trained Volunteers Only)

## Event Schedule & Locations

Welcome! As a fully onboarded volunteer you now have access to event details.

### Upcoming Events

**Children's Education Sessions**
- Days: Every Friday and Saturday
- Time: 10:00 AM – 12:00 PM
- Locations: SmileOra community learning centres at Bannerghatta Road and Haraluru
- What to expect: Teaching, mentoring, educational games, and interactive activities

**Old-Age Home Visits**
- Days: Every Sunday
- Time: 10:30 AM – 12:30 PM
- Location: Partner retirement/old-age homes (Whitefield and Koramangala)
- What to expect: Conversations, games, celebrations, and companionship

**Community & Awareness Events**
- Scheduled periodically — dates and venues communicated via volunteer WhatsApp group
- Types: Awareness drives, fundraising, environmental activities

### How You Will Receive Event Details

- Confirmed event invitations are sent to your registered email.
- Day-of updates and reminders are shared on the volunteer coordination group.
- For any questions about a specific event, email smileora.ngo.info@gmail.com

---

## Frequently Asked Questions (Members)

Q: Where exactly are the events held?
A: Children's sessions are at Bannerghatta Road and Haraluru learning centres.
   Old-age home visits are in Whitefield and Koramangala. Exact addresses are
   shared in the event confirmation email.

Q: What time do events start?
A: Children's sessions: 10:00 AM – 12:00 PM (Fridays & Saturdays).
   Old-age home visits: 10:30 AM – 12:30 PM (Sundays).

Q: How do I sign up for an event?
A: Event invitations are sent to your registered email. Confirm your attendance
   by replying or clicking the confirmation link in the email.

Q: Who do I contact if I can't attend an event I signed up for?
A: Email smileora.ngo.info@gmail.com as soon as possible so the coordinator
   can adjust the team.

Q: How do I earn the Certificate of Appreciation?
A: Attend 8 or more SmileOra events within any 4-month timeframe. Once you hit
   that milestone, email smileora.ngo.info@gmail.com with your name, volunteer ID,
   and the list of events attended. The team will verify and issue your certificate.
"""


# Keep SMILEORA_KB as an alias pointing to the full KB (used in older imports)
SMILEORA_KB = MEMBERS_KB
