# Naya Email System — Communication Hub V1

- **Date:** 2026-08-22
- **Primary category:** DECISION / GOAL / SOLUTION
- **Status:** PLANNING ONLY — no implementation yet
- **Canonical retrieval label:** **NAYA EMAIL SYSTEM**
- **Keywords:** Naya Email System, Communication Hub, email hub, Namecheap, SMTP, IMAP, Vercel, Supabase, GitHub, Groove, CSV, contacts, campaigns, replies, scheduling, AI Score, MAXESS
- **Aliases:** Naya Communication Hub = Naya Email System; email hub = communication hub

## Purpose

Create a simple, custom personal communication control hub for inviting relevant people to the free MAXESS AI assessment. The first useful workflow is:

**UPLOAD CONTACTS → SELECT PEOPLE → WRITE MESSAGE → SEND → SEE REPLIES → RESPOND**

The system should be simple on the surface, visually polished, and properly engineered underneath.

## Core message / purpose

The outreach is intended to help people succeed with AI, not to pressure them into a sale. The primary invitation concept is:

> **What's your AI Score? Free 3-minute AI assessment.**

The assessment is the value-first entry point. A dedicated sales page can provide the fuller explanation for people who want more context than the Results experience provides, but the sales page is not required to begin initial outreach.

## V1 scope

### Contacts

- Upload CSV.
- Initial fields: email, first name, last name, company, city.
- Validate email addresses.
- Remove duplicates.
- Store contacts persistently.
- Select recipients for a campaign.
- Prevent accidental duplicate sends where practical.

### Campaigns / sending

- Subject and message editor.
- Personalization such as `{{first_name}}` where available.
- Preview before sending.
- Send through the connected mailbox infrastructure.
- Record send status and basic message metadata.

### Inbox

- Read incoming replies from the connected mailbox.
- Display sender, subject, message, and status.
- Reply from the hub.
- Keep the actual mailbox as the underlying email account.

### Scheduling

Not required for the first usable release. Add after direct sending is proven. Scheduling should be a cloud-side job using stored `scheduled_at` state so the user's computer does not need to remain on.

### Naya assistance

Optional later layer. Naya may eventually help write, rewrite, personalize, classify replies, and suggest responses. V1 must work without AI so Naya is not a dependency for basic sending.

### Prospect research

Not part of V1. Contacts may initially be researched and imported manually. A future prospect-intelligence layer can be added after the core communication machine is proven.

## Architecture direction

Preferred initial architecture:

**Groove → Vercel cloud app/API → Supabase database → Namecheap mailbox (SMTP/IMAP)**

**GitHub** is the source-code repository and source of truth for the application; it is not the production runtime.

### Groove

Visible cockpit/interface. User uploads contacts, creates campaigns, reads replies, and manages communication.

### Vercel

Cloud application/backend runtime. Receives secure requests from the Groove interface, handles application logic, and can host API endpoints/functions.

### Supabase

Persistent application memory/database for contacts, campaigns, messages, schedules, statuses, and related metadata.

### Namecheap

Actual mailbox identity and mail transport. SMTP is for sending; IMAP is for reading replies. Credentials/secrets must remain server-side and must never be exposed in the Groove embed/browser.

### GitHub

Canonical source-code repository, version history, governance, and deployment source.

## Important architecture boundary

The Groove embed is the cockpit, not the entire system. The email engine must live in a secure cloud backend because credentials, mailbox access, scheduling, and persistent data cannot safely live only in browser/embed code.

The user's computer does **not** need to remain on for the cloud application or future scheduler to operate.

## Mail provider decision

The current plan is **do not add SendGrid or Brevo for V1 unless a real requirement emerges**. Use the user's Namecheap mailbox directly through SMTP/IMAP where the current mailbox/provider terms and technical capabilities permit it.

This avoids an unnecessary third-party email delivery layer for the first version.

Before production sending, verify the actual Namecheap mailbox plan, SMTP/IMAP settings, authentication, DNS/domain configuration, sending limits, and acceptable-use requirements in the live account. Do not guess configuration values.

## Current infrastructure cost direction

Initial development can use the accounts already established:

- GitHub — source control.
- Vercel Hobby — starting deployment/runtime tier, subject to current terms and commercial-use limits at launch.
- Supabase Free — starting database tier, subject to current limits.
- Namecheap mailbox — current trial/paid plan as actually shown in the account.
- Groove — existing interface/hosting layer.

Do not purchase additional infrastructure until actual requirements or limits require it.

## Sending-volume law

The system must not be designed around blindly maximizing volume. Start with small, controlled, relevant outreach, verify deliverability and sender reputation, and increase only when the sending process and compliance/acceptable-use requirements are understood. The previously discussed idea of “1,000/day” is a future capacity question, not a V1 requirement or promise.

## Future build sequence

1. Finish MAXESS assessment and real-data handoff.
2. Complete/verify the Results experience.
3. Build the dedicated sales page for fuller explanation and conversion support.
4. Build Naya Email System V1: CSV → Contacts → Message → Send.
5. Add Inbox → Read Replies → Reply.
6. Add Scheduling.
7. Add Naya writing assistance.
8. Add campaign analytics.
9. Add prospect research/qualification.
10. Add Naya reply intelligence.

## Design standard

The functions are intentionally simple, but the interface must not look cheap or unfinished. Use the established Naya/NayaNET design core: premium simplicity, strong hierarchy, polished controls, responsive layout, accessible interaction, clear status, and excellent mobile behavior.

## Security rules

- Never expose SMTP/IMAP credentials in client-side code.
- Store secrets only in secure server-side environment configuration.
- Do not put mailbox passwords in GitHub, Groove HTML, CSV files, screenshots, or Smart Notes.
- Validate and sanitize uploaded contact data.
- Authenticate the private communication hub.
- Log enough information to diagnose failures without storing unnecessary sensitive data.

## Verification requirements

Before calling the system complete, verify applicable layers:

**SOURCE → STRUCTURE → BUILD/TECHNICAL → BEHAVIOR → VISUAL → RESPONSIVE/ACCESSIBLE → LIVE**

Initial end-to-end proof should use the user's own mailbox and a test recipient before any broader outreach.

## Recall behavior

If the user says **“Naya, access the Naya Email System,” “Bring up the Naya Email System,” “Recall the Naya Email System,”** or equivalent, retrieve this Smart Note and inspect the current repository state before giving implementation instructions.

This note is planning memory, not permission to assume implementation exists.
