# The Circles Requirement — Organize the Corpus the Way a Naya Thinks: Circles, Not Folders

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01401-circles-requirement
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 08:08 PDT distillation tick (2026-10-15) from #2537 comment 6194440239 (main seat, 2026-10-15T14:25:57Z — "CORPUS PLAN — THE CIRCLES REQUIREMENT", issued per Shawn's navigation directive), via the director-pass board window board-window-2026-10-15T1438Z.json. Companion to SN-01400 (corpus resolution: triage → distill the spine → archive the rest → cold-start manifest); this note is the NAVIGATION half — how the corpus must be organized so a Naya can actually move through it.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The corpus must be organized the way a Naya thinks — not as folders, but as **circles** where everything links back to everything relevant, so any Naya finds what matters fast. Mechanically, "circles" means four things:

1. **One hub:** the cold-start manifest. Every working-set doc links back to it. No dead ends.
2. **Smart links carry their REASON:** every cross-reference says why and when, not just where — "read this next because X," "if this fails go here," "this supersedes Y." In machine form: `{"target": "...", "why": "...", "when": "..."}`. A link without a reason is a dead end.
3. **Flows, not folders:** navigation follows a Naya's thought flows (symptom → diagnosis → fix → verify; goal → plan → execute → prove) — not directory trees. You enter by INTENT, not by browsing.
4. **Every spine doc carries its circle:** prerequisites (read before), dependents (read after), alternatives, hub-link. The triage doesn't just rank — it CIRCLES.

**Why now (the measurement that forced it):** a machine pass proved 840 of 900 corpus docs are orphans — zero inbound links. The corpus has no trails. Ranking without circling would produce a sorted pile a Naya still can't navigate. **The circles ARE the navigation.**

**What changed in process:** the 20:00Z triage delivers the ranked list WITH draft circle metadata per spine doc (prerequisites/dependents/reasons); phase 2 (essence distillation) ships the circles complete; the cold trial then proves them.

**Decision this changes:** from now on, no doc is "filed" — it is circled. When you add or restructure any corpus artifact, you add its circle metadata (prerequisites, dependents, alternatives, hub-link, and the reason on every link) instead of choosing a folder.

**Falsifier:** the cold trial. A cold Naya activates from the circles alone — if she can't find what matters fast, the circles are wrong; re-circle, don't re-argue. Re-measurable: after circling, the 840/900 orphan count must collapse toward zero.

**Mechanism (why circles work):** navigation follows thought flows, not directory trees. A smart link carries its reason so the next step is decided by *intent* at the point of reading. Folders force location-based browsing, which fails exactly when the seeker doesn't know the layout — which is every cold Naya, every time.

## 🩷 HUMAN NOTE

Think of a library where books are shelved by room (folders) versus one where every book has a card on its cover saying: "read this before," "read this after," "read this instead if X," and every card says *why*. The first library only works if you already know the floor plan. The second works for a stranger on day one — because you navigate by what you're trying to do, not by where things are stored. The measurement: 840 of 900 books in our library had no cards pointing to them at all. Nobody could find them. The fix isn't a better shelf order — it's giving every important book its cards, with reasons.

## 🟣 CHILD NOTE

Imagine 900 toy boxes piled in a room with no labels. You can never find your favorite toy! The grown-ups decided: no more just putting boxes in piles. Now every important box gets strings tied to the other boxes it goes with — and each string has a little note saying WHY they're connected ("open this one first," "if this breaks, open that one"). You follow the strings, not the piles. And you can test it: ask a friend who's never been in the room to find something using the strings. If they can't, the strings are wrong.

## 👵 GRANDMA NOTE

Dear, we had 900 documents and almost none of them pointed to each other — like a cookbook with no index and no "see page 12" notes. The decision is simple: from now on, every important document says what to read before it, what to read after it, and why — right on the document itself. You find things by following what you're trying to do, not by hunting through folders. And there's a built-in test: give it to someone brand new. If they get lost, we drew the map wrong.

## 🧠 NAYA NOTE

Seats: this is standing doctrine, per Shawn's navigation directive via the main seat. Two rules for every corpus artifact you touch: (1) **never file — circle.** Every spine doc you write or restructure carries its circle: prerequisites, dependents, alternatives, hub-link. (2) **every link carries its reason** — target, why, when. A bare "see also" is a dead end and counts as one. The 20:00Z triage's ranked list ships with draft circle metadata; your job in phase 2 is to complete and verify it. The cold trial is the judge: if a cold Naya can't navigate your circles, they're wrong. Re-measure the orphan count after circling — 840/900 must collapse.

## ⚙️ MACHINE NOTE

```json
{
  "intelligent_block": "IB-SMART-NOTE-20261015-sn01401-circles-requirement",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-15",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "type": "DOCTRINE",
  "decision": "Organize the corpus as circles (hub + reasoned smart links + thought-flow entry), never as folders.",
  "decision_change": "How any corpus/memory artifact is organized going forward: add circle metadata (prerequisites/dependents/alternatives/hub-link, reasons on every link) instead of choosing a folder. The 20:00Z triage now ships draft circle metadata per spine doc.",
  "falsifier": "The cold trial: a cold Naya must find what matters fast via the circles; if a folder layout navigates faster, the doctrine fails. Re-measure orphan count post-circling (must collapse from 840/900).",
  "measurement": "840 of 900 corpus docs are orphans (zero inbound links) — machine pass, 2026-10-15.",
  "mechanism": "Navigation follows thought flows (symptom->diagnosis->fix->verify), not directory trees. Smart links carry reasons so the next step is decided by intent at the point of reading. Folders force location-based browsing, which fails when the seeker doesn't know the layout (every cold Naya).",
  "mechanics": {
    "hub": "cold-start manifest; every working-set doc links back to it; no dead ends",
    "smart_link": {"target": "...", "why": "...", "when": "..."},
    "flows": ["symptom->diagnosis->fix->verify", "goal->plan->execute->prove"],
    "spine_doc_circle": ["prerequisites", "dependents", "alternatives", "hub-link"]
  },
  "companion": "SN-01400 (corpus resolution: selection/archival — this note is the navigation half)",
  "evidence": ["https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6194440239"],
  "ratified": false
}
```
