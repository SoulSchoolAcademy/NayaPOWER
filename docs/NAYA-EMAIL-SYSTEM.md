# Naya Email System

> **RECALL LABEL:** `Naya email system`
>
> This document is the persistent planning note for the future Naya Communication Hub. When Shawn says **“Naya email system”**, retrieve this document before answering or continuing the work.

## PURPOSE

Build a small, custom **Naya Communication Hub** whose primary purpose is:

**Find relevant people → upload them → send a genuinely helpful invitation → receive replies → respond.**

The core invitation is intentionally simple:

> **What’s Your AI Score?**  
> Free 3-minute AI assessment.

The assessment is the value being offered. The email is simply the door into it.

The system should prioritize helpful, human communication rather than aggressive sales automation. Outreach must use appropriate consent, lawful acquisition/use of contact data, accurate sender identity, and reasonable sending practices.

---

## V1 SCOPE — KEEP IT SMALL

### V1 core flow

**CSV → Contacts → Select → Write → Preview → Send → Inbox → Reply**

### Contacts

Initial CSV fields:

- `email`
- `first_name`
- `last_name`
- `company`
- `city`

The application should:

- validate email addresses
- remove duplicates
- identify missing/invalid email addresses
- remember contacts
- prevent accidental duplicate sending

### Campaigns

Initial campaign UI should support:

- select contacts
- subject
- message editor
- merge fields such as `{{first_name}}`
- preview
- send
- sent status

Example campaign:

**Subject:** What’s Your AI Score?

**Message:**

> Hey {{first_name}},
>
> I’m Shawn, and I’ve been working on something to help people understand where they actually are with AI.
>
> I created a free 3-minute AI assessment that gives you your personal AI Score.
>
> If you’re curious, I’d love for you to try it:
>
> **[ASSESSMENT URL — use the current canonical assessment URL when this system is built.]**
>
> No cost. No complicated signup. Just three minutes to see where you stand.
>
> — Shawn

### Inbox

The hub should eventually retrieve replies from the connected mailbox and display:

- sender
- subject
- message
- date/time
- conversation/thread context where practical
- reply action

V1 reply flow:

**Open reply → type response → Send**

---

## V1.1 — SCHEDULING

Scheduling should NOT block the first working version.

Once sending works correctly, scheduling is a relatively small additional layer. Store:

- `campaign_id`
- recipient list
- message
- `scheduled_at`
- status

A cloud job/cron process can send due messages.

Desired UX example:

**TODAY’S OUTREACH**

- Target: 50
- Sent: 17
- Replies: 2
- Remaining: 31
- Sending window: configurable

Do not equate provider rate limits with a recommended sending volume. Sending should be paced responsibly and monitored for delivery/reputation/compliance.

---

## FUTURE PHASES

### Phase 1 — Tiny machine

CSV → Contacts → Message → Send

### Phase 2 — Inbox

Read replies → Respond

### Phase 3 — Scheduling

Send later / scheduled campaigns

### Phase 4 — Naya writing assistance

Examples:

- Make this friendlier.
- Make this sound more like Shawn.
- Write a version for Kelowna business owners.
- Make this less salesy.

Naya must NOT be a dependency for core email sending.

### Phase 5 — Campaign analytics

Basic delivery/sent/reply tracking and useful campaign metrics.

### Phase 6 — Prospect research / qualification

Research and qualification can be added after the basic system works. Do not build prospect scraping/research into V1.

### Phase 7 — Naya reply intelligence

Potential future features:

- classify replies
- identify interest level
- suggest next response
- identify useful context from the reply

Example:

**HIGH INTEREST**

> “I’ve been trying to figure out how to use AI in my accounting practice...”

Suggested next action: invite a conversation about the person’s workflow.

---

## ARCHITECTURE

The preferred conceptual architecture is:

```text
                    NAYA COMMUNICATION HUB
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
         CONTACTS         OUTBOUND           INBOX
         CSV upload       Email API          IMAP
         Selection        Delivery           Replies
             │                │                │
             └────────────────┼────────────────┘
                              ▼
                         DASHBOARD
```

### Frontend / control surface

The visible interface may initially be embedded in Groove.

Groove is the **cockpit/interface**, not the core backend.

### Source control

GitHub stores the source code and project documentation.

GitHub is **not** the production runtime.

### Runtime

Use the simplest cloud backend that meets the actual requirements. The current preferred starting architecture is:

**GitHub → Vercel → Supabase → Namecheap**

with Groove as the interface.

Do not add infrastructure merely for sophistication. Re-evaluate the exact backend implementation when the project is ready to build.

### Vercel

Intended role:

- host the web application
- run secure server-side/API logic
- handle requests from the Groove interface
- potentially run scheduled/background API logic depending on final architecture

A Vercel Hobby account is currently available as the initial development/testing tier. Verify current commercial/production terms before public commercial operation.

### Supabase

Intended role:

- contact database
- campaigns
- message metadata
- scheduled jobs/state
- application data

Current planning assumption: Supabase Free is sufficient for the initial workload. Re-check current limits when implementation begins.

### Namecheap

Intended role:

- actual mailbox
- SMTP for outbound mailbox sending where appropriate
- IMAP for receiving/retrieving replies

Current Namecheap Private Email host information identified during planning:

- IMAP host: `mail.privateemail.com`
- IMAP SSL port: `993`

Do not expose mailbox credentials in the Groove frontend. Credentials/secrets belong server-side only.

### SendGrid / Brevo

**Not required for V1.**

The earlier SendGrid architecture was considered, but the current preferred direction is to avoid a separate email-delivery provider unless implementation/testing proves one is necessary.

The custom application should own the organization/control layer while the connected Namecheap mailbox remains the mailbox.

---

## DATA FLOW

### Sending

```text
Groove UI
  ↓ HTTPS/API
Vercel backend
  ↓
Validate authorization + campaign + recipients
  ↓
Namecheap SMTP / approved email transport
  ↓
Recipient
```

### Receiving

```text
Recipient reply
  ↓
Namecheap mailbox
  ↓ IMAP
Vercel backend / mailbox worker
  ↓
Supabase
  ↓
Groove Communication Hub inbox
```

### Assessment → Communication Hub

The assessment should NOT require an email at the beginning.

At the results stage, the user may optionally enter an email to receive their report.

Future integration:

```text
Assessment
  ↓
Optional email capture
  ↓
Communication backend
  ↓
Contact + assessment metadata
```

This allows the system to associate an email with an assessment result without forcing an email gate at the beginning of the assessment.

---

## UI CONCEPT

### Dashboard

**NAYA COMMUNICATION HUB**

Today:

- Contacts
- Campaigns
- Sent
- Replies

Primary action:

**NEW CAMPAIGN**

### Contacts

- Upload CSV
- Contact count
- Search/filter
- Select contacts
- Validation results

### Campaign

- Recipient selection
- Subject
- Message editor
- Personalization fields
- Preview
- Send

### Inbox

- conversation list
- sender
- subject
- latest message
- reply button

The interface should be visually polished, responsive, accessible, and consistent with the broader Naya/NayaNET design language. “Simple” means simple functionality, **not** visually crude or unfinished.

---

## DESIGN / PRODUCT LAW

The system should feel like a **personal communication control hub**, not a generic bulk-email marketing platform.

Core principles:

1. Human first.
2. Help first.
3. Assessment first, email second.
4. Simple on the surface.
5. Properly engineered underneath.
6. No unnecessary dependencies.
7. Preserve the ability to expand later.
8. Never compromise sender identity, security, privacy, or responsible email practices for convenience.

---

## CURRENT BUILD ORDER AROUND MAXESS

The current priority is to finish MAXESS before building this system.

Recommended sequence:

1. **Finish the AI assessment / MAXESS.**
2. **Build the dedicated sales page.**
3. **Build Naya Communication Hub V1.**
4. **Begin targeted marketing/outreach using the working assessment invitation.**
5. Expand the hub only after the core machine is proven.

### Why the dedicated sales page is still valuable

The results page should provide the immediate personalized value and the next-step experience.

A dedicated sales page can provide the **full meal deal** for people who want to understand more before taking the next step:

- what the product is
- why it matters
- what the assessment reveals
- how the larger solution works
- what the user receives
- FAQs / objections
- the complete invitation to continue

Therefore the sales page is not a prerequisite for the communication engine to technically function, but it is strategically valuable as the fuller destination for interested people.

The email campaign can still begin as soon as the assessment and essential destination are ready; the sales page can be completed as the fuller conversion destination rather than allowing it to unnecessarily block the system.

---

## COST / INFRASTRUCTURE PLANNING

Initial planning assumption:

- GitHub: existing/free
- Vercel: Hobby/free for development and testing
- Supabase: Free for initial workload
- Namecheap mailbox: trial, then current paid mailbox cost
- SendGrid/Brevo: not required for V1

Do not purchase additional infrastructure until actual requirements demonstrate the need.

Current cost assumptions must be re-verified when implementation begins because provider pricing, limits, and terms can change.

---

## SECURITY REQUIREMENTS

Never put these into the Groove/client-side code:

- Namecheap mailbox password
- SMTP password
- IMAP password
- API secrets
- database service-role keys
- private authentication tokens

All secrets must be stored in the backend's secure environment-variable/secret system.

The frontend communicates with the backend through authenticated HTTPS/API requests.

---

## FIRST TEST PLAN

Before sending to real contacts:

1. Deploy backend.
2. Connect database.
3. Connect test mailbox.
4. Upload a CSV containing only controlled test addresses.
5. Send one test email to Shawn/self-controlled addresses.
6. Verify delivery.
7. Reply to the test email.
8. Verify IMAP retrieval.
9. Verify reply appears in the hub.
10. Reply from the hub.
11. Verify delivery and thread behavior.
12. Only then test a small real campaign.

Do not call the system production-ready from source inspection alone.

Required status language:

**IMPLEMENTED · VERIFIED · LIVE VERIFIED · HUMAN REVIEW REQUIRED**

---

## RECALL INSTRUCTION

When Shawn says any of the following:

- “Naya email system”
- “access the Naya email system”
- “bring back the email system plan”
- “continue the communication hub”

retrieve this document first and establish the current state before proposing or executing changes.

This document is a planning/source-of-truth note, not permission to start implementation automatically. Confirm current repository state and current provider limits when the build begins.
