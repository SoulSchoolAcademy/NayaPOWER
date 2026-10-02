# 09 — Smart Mail

**Metaphor:** THE SIGNAL ROOM  
**Route:** `/mail`  
**Theme:** sapphire / cyan  
**Human question:** **What communication needs my attention, and what does it mean?**

## Human promise

Present real messages as intelligent signals: what matters, why, what context they belong to and what action is needed.

**No fake mailbox.**

## Signature visual

A refined **signal console**, not a conventional email clone.

Default view groups by meaning:
- Needs response
- Important
- Waiting on someone
- FYI / low urgency
- Related to active Space
- Sent / drafts

A chronological inbox remains available.

Each message preview may show:
- sender;
- subject/essence;
- why it matters;
- Space/context;
- time;
- attachment/intelligence links;
- response/action state.

## Primary actions

- **Open**
- **Reply**
- **Compose**
- **Archive**
- **Mark / prioritize**
- **Ask Naya**
- **Add to List**
- **Attach/link to Space**
- **Open sender in Connections**
- **View proof/activity** where applicable

## Naya intelligence

Naya may:
- summarize a long thread;
- identify unanswered questions;
- draft a response;
- connect message to existing intelligence;
- flag contradictions/commitments;
- identify action items.

Naya must not send consequential messages without applicable user authorization.

## Runtime states

- RUNTIME UNAVAILABLE
- NO MAIL
- ACCESS BLOCKED
- LOADING
- READY
- ERROR/OFFLINE

Never show sample messages to make the room feel populated.

## Intelligence-production boundary

Mail may surface a message as useful context and may hand context to Naya, but the Hub/Mail client does not create a canonical Smart Note locally. If the human asks Naya to Smart Note a message, that request goes through the upstream governed Smart Note pipeline; the resulting IB later projects back into the Hub.

## Cross-room handoffs

Sender → Connections  
Thread/project → Space  
Insight → Library / originating canonical intelligence  
Action → List  
Receipts → Ledger

## Mobile

Thread-first message reader, intelligent triage tabs, compose in full-screen sheet.

## Acceptance journey

A human can identify what needs attention, open a real thread, understand its context, ask Naya for help, reply or draft under authority, convert useful content into durable intelligence and trace relevant evidence.

## Human Director source-note reconciliation

The Drive notes specify top modes **IMPORTANT / RESPOND / FOLLOW UP / DRAFTS / SENT**. Opening a message should use a message + context composition: MESSAGE as the main reading surface; CONTEXT explains **Who is this? Why does this matter? Previous relevant interaction. Related intelligence. Potential response.** Then a **DRAFT RESPONSE** capability. Naya must never send without required authority.

## Shared five-layer mapping

- **ORIENTATION:** mail identity, account/channel/Space and current triage mode
- **CURRENT STATE:** real message counts/threads and availability/access state
- **INTELLIGENCE:** importance, response need, relationship context, commitments, related intelligence and Naya summary
- **ACTION:** open, reply/draft, compose, archive, prioritize, follow up, list/link Space; Smart Note creation remains upstream
- **PROOF:** real sender/thread provenance, send authority, message state and receipted action where applicable
