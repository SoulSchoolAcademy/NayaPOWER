# IB-SMART-NOTE-20261015-sn1432

**Intelligent Block:** SN-1432
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Read the scope flag BEFORE you emit, not after. A feed without the privacy line read is a pipe that leaks. On 2026-10-15 the hub-feeds emitter touched 191 `nayanet_intelligent_blocks` rows and found every one `owner_scope=PRIVATE` — so it emitted METADATA-ONLY (ids, titles, topics, 280-char summaries), never block content bodies, and flagged in the PR body that full publication of PRIVATE blocks needs Shawn's explicit word. The room-feed contract already says "Private stays local" (rule 5) — the lesson is mechanical: the scope read is a pre-emission step, not a post-emission audit. The flag was named in the open, not buried in the build.

## HUMAN NOTE

Think of a mailroom that sorts packages into two bins: LOCAL ONLY and PUBLIC. The standing rule is "local stays local." On this run, the emitter opened all 191 packages, read the sticker on each one FIRST — every sticker said LOCAL ONLY — and shipped only the labels (tracking number, sender, short description), never the contents. Then it wrote, right on the shipping manifest where anyone can see it, that opening the contents for the public needs the owner's explicit say-so. That's the discipline: the sticker read is the first step of the job, not a review after the trucks leave. A feed that emits before it reads the sticker is a pipe that leaks — the leak happens in the emit, and no audit afterwards un-leaks it.

## CHILD NOTE

Imagine you're in charge of the school's Lost & Found camera feed. Every item has a tag: "show everyone" or "private — only for the office." Before you point the camera at anything, you read the tag. If it says private, the most you can show is a little label — "blue water bottle, gym" — never the inside of it. And if you want to show the inside, you ask the owner first, and you say so out loud. This team did exactly that: 191 items, every tag said private, so the feed showed labels only — and the note asking permission went on the front of the report, not hidden in the back. Rule: read the tag before you show, not after.

## GRANDMA NOTE

Dear, there's a simple courtesy here dressed as an engineering rule. Everything we touch has a little flag saying who may see it. The wise habit is to read the flag before anything leaves your hands — not to check afterwards whether you made a mistake. This team read 191 flags, found every one marked private, and sent out only the smallest descriptions, keeping the contents back until the owner himself said yes — and they wrote that plainly on the front page of their report. Once something is published, you can't un-publish it; that's why the flag must be read first. A leak is not fixed by apologizing after. It is prevented by reading before.

## NAYA NOTE

For every emitter, publisher, and feed builder: the scope/privacy flag on the row is a pre-emission input, never a post-emission audit. Sequence: (1) read the privacy/ownership scope on every row you touch; (2) PRIVATE scope → metadata-level output only (ids, titles, topics, short summaries — never content bodies) unless the owner has explicitly authorized more; (3) flag the privacy line in the open (PR body), not buried in the build. The standing contract ("Private stays local," room-feed contract §1 rule 5) only works if the flag is read before bytes leave — an emitter that emits first and checks after has already leaked, and no audit un-leaks. Cousin: any guard whose enforcement point is downstream of the effect is prose, not a gate (cf. SN-1430's escalation-channel lesson: mutate the channel before the message; here, read the scope before the emit).

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1432",
  "title": "Read the scope flag BEFORE you emit, not after — a feed without the privacy line read is a pipe that leaks",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-15",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/SECURITY-POSTURE",
  "evidence": [
    "hidden_files/twelve-lane-receipts/t0479-lane4.md (2026-10-15): hub-feeds emitter t0479 found all 191 nayanet_intelligent_blocks rows owner_scope=PRIVATE via read-only group-by SQL against project dahisasgpfvziswqvmvm; emitted METADATA-LEVEL ONLY (ids, titles, topics, 280-char summaries), no full block content bodies; flagged in the PR body that full public-scope publication of PRIVATE blocks needs Shawn's explicit word",
    "hidden_files/room-feed-contract-2026-10-15.md §1 rule 5: standing contract 'Private stays local'"
  ],
  "rule": "read the privacy/ownership scope on every row before emission; PRIVATE scope means metadata-level output only unless the owner explicitly authorized more; flag the privacy line in the open (PR body), not buried in the build",
  "anti_pattern": "emitting full content first and auditing scope after — the leak happens at emit time and no post-hoc audit un-leaks it; burying the privacy decision in the build instead of naming it on the PR front page",
  "falsifiability": "falsified if full-publication of PRIVATE-scoped rows without the owner's word caused no harm in a setting where the scope contract was meant to hold — the scope flag is a contract tag, not decoration; bounded by the owner's standing 'Private stays local' rule",
  "mechanism": "the scope flag is the machine-readable access-control tag on the data; the emission point is where that tag becomes an enforcement decision. Reading the tag before emitting puts enforcement ahead of the effect; reading after puts it behind — the order is the enforcement",
  "related": ["SN-1428", "SN-1430"],
  "triage": {
    "decision_change": "emission routines decide metadata-only vs full-content output on the basis of a scope flag read before emitting",
    "falsifiability_note": "would be proven wrong by evidence that PRIVATE-scoped content published without the owner's word was harmless — the flag's meaning is contractual, so the bound is the contract itself",
    "mechanism_note": "scope tag read before emit = enforcement ahead of effect; after emit = audit behind the leak; order is the gate"
  }
}
```
