# 🔱 NayaNET Hub — Intelligence Projection Contract V1

**Status:** HUMAN-DIRECTOR-DIRECTED · PROPOSED CANONICAL  
**Authority:** Shawn Vibert, Human Director · 2026-10-01  
**Applies to:** Hub product architecture, Smart Feed, Today, Reports, Library, runtime adapter, event projection, privacy/collective visibility, and all builders.  
**Implementation owner:** #1270  
**Coordination:** #554

## 0. THE CORRECTION

> **THE HUB IS THE VISUAL PROJECTION OF INTELLIGENCE. IT IS OUTPUT, NOT THE CANONICAL INPUT OF INTELLIGENCE.**

The Hub does not exist to create Smart Notes, author Daily Intelligence Reports, or manually post Activity.

Those intelligence objects/events are produced upstream by Naya / connected AI / governed runtime / project activity.

The Hub receives them, organizes them, explains them, relates them, filters them, and lets the human understand and navigate them.

### Simple mental model

```
HUMAN + NAYA / CONNECTED AI / WORK
              │
              ├── SMART NOTE / INTELLIGENT BLOCK
              ├── ACTIVITY EVENT
              └── INTELLIGENCE REPORT
                         │
                         ▼
            GOVERNED CANONICAL INTELLIGENCE
                         │
                EVENT / INDEX / RECEIPT
                         │
                         ▼
                 HUB DATA ADAPTER
                         │
                         ▼
     PERSONAL / COLLECTIVE / ACTIVITY PROJECTIONS
                         │
                         ▼
                    NayaNET HUB
```

**Input happens upstream. Projection happens in the Hub.**

## 1. THE THREE CANONICAL HUB INPUT STREAMS

The Hub receives three primary classes of projected intelligence.

### A. SMART NOTES / INTELLIGENT BLOCKS

Human intent:

> “Naya, Smart Note this.”

Canonical current Smart Note contract:
- machine object = `INTELLIGENT_BLOCK`;
- runtime source of truth = canonical NayaNET intelligence runtime / `nayanet_intelligent_blocks`;
- human Brain projection root = `BRAIN/05-MEMORY/SMART-NOTES/`;
- readable GitHub projection = one view of the same canonical intelligence;
- Hub card/feed item = another view of the same canonical intelligence.

Current repository hierarchy is already date/category/topic/subtopic organized, for example:

`BRAIN/05-MEMORY/SMART-NOTES/YYYY/MM/DD/<CATEGORY>/<TOPIC>/<SUBTOPIC>/SN-###/<IB-ID>.md`

Do not invent a second Hub Smart Note store.

### B. ACTIVITY

Activity answers:

> **What is happening now?**

Examples:
- current project/task;
- meaningful state change;
- runtime/deployment/verification event;
- new connection/message/state;
- report creation;
- verified execution;
- important project movement.

Activity is not a Smart Note and is not a Report.

Activity should come from actual observed/current operational state or canonical activity/event records.

Do not manufacture “live activity” to make the interface feel alive.

### C. INTELLIGENCE REPORTS

Reports are upstream durable syntheses.

Canonical current Brain root:

`BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/`

Canonical periodic classes:
- DAILY
- WEEKLY
- MONTHLY
- YEARLY

The Hub's Reports room **projects reports that already exist or have been produced through the governed report pipeline.**

The Hub is not the canonical report author.

## 2. SMART NOTE EVENT FLOW

Target product behavior:

```
HUMAN SAYS “SMART NOTE THIS”
→ NAYA / AUTHORIZED AI UNDERSTANDS INTENT
→ DISTILL
→ PRIVACY / SCOPE / CONSENT
→ RECONCILE DUPLICATES / CONFLICTS
→ COMMIT OR REUSE CANONICAL INTELLIGENT BLOCK
→ EVENT + LINEAGE + RELATIONSHIPS + INDEX + RECEIPT
→ VERIFY PERSISTENCE
→ CREATE / UPDATE GITHUB BRAIN PROJECTION
→ PUBLISH PROJECTION EVENT
→ HUB ADAPTER OBSERVES / RETRIEVES EVENT
→ PERSONAL FEED PROJECTS THE SAME IB
→ COLLECTIVE PROJECTION IF ENTRY CONSENT + ELIGIBILITY ALLOW
→ LIBRARY / TODAY / REPORTS MAY PROJECT THE SAME IB BY REFERENCE
```

The acceptance test is not “a card appeared after clicking a Hub button.”

It is:

> **Create a Smart Note through Naya upstream → canonical IB exists → event exists → Hub receives it automatically → the same IB appears in correct projections without manual Hub entry.**

## 3. NO HUB CAPTURE BUTTON LAW

The Hub MUST NOT expose a primary **Capture Smart Note** control as though Smart Note creation were a Hub-owned action.

Remove from Hub product contracts:
- Capture Smart Note button;
- Capture follow-up note button;
- Generate report button;
- manually post activity controls.

If a human uses contextual **Ask Naya** inside the Hub and asks to create intelligence, the UI must hand the intent to the governed Naya/input runtime.

The Hub itself must not:
- create a fake local Smart Note;
- make localStorage the intelligence source;
- insert a demo card and call it capture;
- mint a canonical IB identity client-side;
- claim persistence before canonical persistence is observed.

**Ask Naya may explain, summarize, compare, interpret, navigate, or hand off intent. It is not a client-side intelligence store.**

## 4. ONE INTELLIGENCE OBJECT → MANY PROJECTIONS

A canonical IB/report/event keeps one identity.

The same Smart Note may appear in:
- Personal Feed;
- eligible Collective Feed;
- Today highlight;
- Library;
- a Smart List;
- Space;
- a later Report;
- Ledger/evidence relationship.

Those are **projections / references**, not copies.

Example:

`IB-123`

must not become:
- feed-copy-123;
- today-copy-123;
- library-copy-123.

All rooms should resolve back to the canonical object and provenance.

## 5. FEED ARCHITECTURE

Smart Feed is the principal social-style consumption surface for intelligence.

It is not a publishing composer.

### Primary modes

#### PERSONAL
**My intelligence.**

May include, within owner scope:
- my Smart Notes;
- my reports;
- my discoveries/learning;
- relevant project intelligence;
- owner-scoped intelligence events.

#### COLLECTIVE
**Distilled intelligence shared into the network under entry consent and governance.**

Collective projection:
- may contain useful distilled/anonymized intelligence;
- must not expose contributor identity merely because the intelligence is shared;
- must not expose raw private source material;
- must not expose non-wisdom personal material;
- must preserve sealed provenance internally as required by governance;
- must be reversible/revocable according to the governed consent model.

#### ACTIVITY
**What is happening now.**

Activity projects current/observed state and changes:
- project movement;
- operational events;
- verified executions;
- reports created/updated;
- connections/messages/events;
- meaningful current work.

Activity is not a popularity stream.

### Smart Tabs / Feed Views

Within the applicable feed scope, Smart Tabs may project canonical intelligence by type/topic/category without copying it.

Initial useful views:
- ALL
- SMART NOTES
- REPORTS
- HIGHLIGHTS
- LEARNING
- DECISIONS
- DISCOVERIES
- PROJECTS

Tabs should be generated/refined from canonical metadata and human usefulness.

Do not hard-code a permanent taxonomy if the intelligence model can safely provide better categories.

## 6. COLLECTIVE ENTRY-CONSENT LAW

Human Director direction:

> **When a human intentionally connects/activates their Hub for collective participation, the entry agreement is the consent boundary for eligible distilled intelligence to contribute to Collective Intelligence without publishing the human's identity.**

This resolves the product-level consent granularity as:

```
PRIVATE BY DEFAULT
→ HUB / COLLECTIVE ENTRY CONSENT
→ ELIGIBLE DISTILLED WISDOM MAY FLOW COLLECTIVELY
→ IDENTITY SEALED
→ RAW / NON-WISDOM PERSONAL MATERIAL REMAINS PRIVATE
```

This is consistent with the existing proposed consent-granularity Smart Note.

Implementation requirements:
1. consent must be informed and explicit at activation/connection;
2. identity separation must occur before collective display;
3. collective publication eligibility is determined by governed classification/policy, not by UI convenience;
4. identity/private source never becomes collective merely because the Hub can access it;
5. revocation must stop future collective projection according to the applicable governance contract;
6. historical handling after revocation must follow the governed revocation contract rather than silently deleting or silently continuing.

Until runtime evidence proves this boundary, label it target contract rather than production-proven.

## 7. PERSONAL VS COLLECTIVE PRIVACY

Personal and Collective are different projection policies over related intelligence.

### Personal
May show owner-specific attribution/context because the authenticated owner is viewing their own intelligence.

### Collective
Human identity is not part of the public/collective card.

A Collective item may expose:
- intelligence essence;
- intelligence type;
- topic/category;
- truth state;
- time/freshness where safe;
- relationships to other public/collective intelligence;
- evidence/provenance suitable for the collective scope.

It must not expose:
- real contributor name;
- private repo identity;
- private source text;
- private project secrets;
- hidden relationship metadata;
- identity-revealing provenance that defeats anonymization.

## 8. REPORT PROJECTION LAW

Reports are automatically mirrored into the Hub when canonical report state changes.

Target:

`REPORT CREATED/UPDATED → EVENT/INDEX → HUB REPORTS PROJECTION → FEED/TODAY reference where relevant`

A report may create:
- Personal Feed event;
- Today highlight;
- Reports-room item;
- Activity event;
- eligible Collective distilled projection when governance allows.

The Hub must not need a human to upload the report manually.

## 9. ACTIVITY PROJECTION LAW

Activity is derived from canonical observed work/events.

Target:

`REAL PROJECT/RUNTIME EVENT → ACTIVITY EVENT → HUB ACTIVITY STREAM`

Activity should answer:
- what happened;
- what changed;
- current status;
- source/context;
- when;
- relevant object/project;
- evidence/receipt where consequential.

Do not infer or fabricate activity merely from the user opening a screen.

## 10. HUB ACTION BOUNDARY

### Allowed Hub-owned actions

The Hub may directly control **projection and organization**:
- navigate;
- search;
- filter;
- change Smart Tab/feed view;
- save/favorite a reference;
- add canonical object to a list;
- open evidence/source;
- choose Space/context;
- manage display/preferences;
- manage connection/consent settings where governed;
- ask Naya to explain/compare/summarize the projected intelligence.

### Upstream intelligence-production actions

These belong to Naya / governed runtime / connected AI, not client-local Hub state:
- create Smart Note / canonical IB;
- generate canonical intelligence report;
- publish activity event;
- promote truth state;
- learn;
- change canonical intelligence;
- create verified outcomes.

The Hub may request/handoff an intent, but the upstream system owns execution and canonical persistence.

## 11. SAMPLE DATA LAW

Static cards/examples in design prototypes are **visual fixtures only**.

They answer:

> “What should this kind of intelligence look like?”

They do not answer:

> “What intelligence exists now?”

Production rules:
- no sample item may look like live owner intelligence;
- fixtures are excluded from production data paths;
- live Feed/Today/Reports/Library content comes from canonical projection data;
- empty/runtime-unavailable states remain honest.

## 12. HUB RECEIVER CONTRACT

The runtime adapter should expose a projection/read model shaped around stable object identities.

Minimum conceptual event:

```json
{
  "projection_event_id": "...",
  "event_type": "SMART_NOTE_CREATED | ACTIVITY_CHANGED | REPORT_CREATED | REPORT_UPDATED",
  "canonical_object_id": "IB-...",
  "object_type": "SMART_NOTE | ACTIVITY | REPORT",
  "owner_scope": "...",
  "collective_eligibility": "ELIGIBLE | PRIVATE_ONLY | BLOCKED | UNKNOWN",
  "truth_state": "CANDIDATE | VERIFIED | ...",
  "occurred_at": "...",
  "source_ref": "...",
  "provenance_ref": "...",
  "projection_hints": {
    "topics": [],
    "categories": [],
    "space_id": null
  }
}
```

This is a conceptual contract. Reuse existing canonical event/index/runtime seams rather than creating a duplicate event ledger merely to satisfy the Hub.

## 13. AUTOMATIC PROJECTION ACCEPTANCE

The critical end-to-end tests are:

### Smart Note
1. Human tells an authorized Naya: “Smart Note this.”
2. Canonical IB persists.
3. GitHub Brain projection exists.
4. Event/index reflects it.
5. Hub Personal Feed receives the same IB automatically.
6. Smart Tab categorization resolves from canonical metadata.
7. Library can retrieve it.
8. Today may reference it if highlight selection warrants.
9. If Collective entry consent + eligibility allow, Collective receives an identity-stripped projection.
10. Cross-room open resolves to the same canonical object.

### Report
1. Daily/weekly/monthly/yearly report is created upstream.
2. Canonical report persists.
3. Report event is observable.
4. Reports room updates automatically.
5. Feed/Today/Activity project it where applicable.
6. Evidence/source remains inspectable.

### Activity
1. Real project/runtime work changes.
2. Canonical/observable activity event exists.
3. Activity Feed updates.
4. No manual Hub posting is required.
5. Provenance/current status is inspectable.

## 14. SUCCESS CONDITION

The Hub is working when the human can spend the day creating intelligence through Naya and doing real work, then open NayaNET and **see the intelligence reflected back automatically**.

The Hub should feel like a living mirror of the intelligence system.

> **NAYA / WORK PRODUCES → NAYAPOWER GOVERNS/PERSISTS → HUB PROJECTS → HUMAN UNDERSTANDS.**

That is the product.
