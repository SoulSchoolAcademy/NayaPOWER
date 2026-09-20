# 🔱☀️ NAYANET — QA & RELEASE GATE

**STATUS:** CANONICAL RELEASE-GATE STANDARD
**SCOPE:** Every substantive NayaNET build before it may be represented as complete, released, or production-ready
**PURPOSE:** Prevent false completion and force evidence-based verification of the whole experience.

---

## 1. RELEASE LAW

> **DO NOT DECLARE SUCCESS BECAUSE CODE WAS WRITTEN.**
>
> **DECLARE SUCCESS ONLY WHEN THE RESULT IS UNDERSTANDABLE → SIMPLE → ALIVE → USEFUL → BEAUTIFUL → RESPONSIVE → ACCESSIBLE → ROBUST → VERIFIED → 10/10.**

This gate is mandatory for consequential NayaNET work.

A result can be IMPLEMENTED without being VERIFIED.
A result can be VERIFIED without being LIVE VERIFIED.
A result can be DEPLOYED without being PRODUCTION-PROVEN.

Never collapse these states.

---

## 2. RELEASE STATUS LADDER

| Status | Meaning |
|---|---|
| DOCUMENTED | Requirement/rule exists in authority |
| IMPLEMENTED | Code/config/content exists |
| VERIFIED | Applicable evidence passed |
| DEPLOYED | Deployment system reports delivery |
| LIVE VERIFIED | Actual target was inspected |
| PRODUCTION-PROVEN | Live behavior passed release acceptance |
| HUMAN REVIEW REQUIRED | Machine evidence cannot establish final judgment |
| BLOCKED | Responsible continuation is prevented |
| UNKNOWN | Evidence is insufficient |

### Absolute language rule

Never say “live,” “working in production,” “deployed successfully,” or “done” when the evidence only proves code existence.

---

## 3. GATE 0 — AUTHORITY

Before QA, confirm:

- current repository;
- current HEAD;
- applicable project directive;
- applicable NayaNET standards;
- protected capabilities;
- acceptance criteria;
- release target.

If the tested artifact is not the artifact authorized by the current directive, QA is invalid.

---

## 4. GATE 1 — BUILD INTEGRITY

Verify as applicable:

- syntax;
- imports;
- dependency resolution;
- build process;
- lint/type checks;
- test suite;
- asset references;
- route/entry integrity;
- configuration integrity;
- no accidental debug output;
- no unresolved merge markers;
- no obvious dead/duplicate implementation introduced by the change.

A build that cannot reliably start is **RED**.

---

## 5. GATE 2 — PRIMARY HUMAN JOURNEY

For NayaNET's primary entry experience, verify the intended journey from arrival through meaningful first action.

Canonical high-level journey:

```text
ARRIVE
 → IDENTIFY
 → ENTER
 → MEET NAYA
 → EXPLORE
 → CREATE
 → CONNECT
 → LEARN
 → SHARE WISDOM
 → GROW
 → BECOME WISER
```

For the front door, verify the core comprehension test:

```text
SEE NayaNET
 → UNDERSTAND WHAT IT IS
 → ENTER NAME
 → PRESS ENTER
 → SOMETHING MEANINGFUL HAPPENS
```

The experience must not require a tutorial to understand the basic next action.

---

## 6. GATE 3 — EXPERIENCE QUALITY

Check:

### Immediate understanding
Can a first-time person explain what NayaNET is and what to do next?

### Push-button simplicity
Can the intended result be achieved with the fewest safe actions?

### Living responsiveness
Do important objects respond meaningfully to touch, click, hover, focus, selection, progress, loading, and completion?

### Emotional impact
Does the experience feel intentional, alive, and memorable rather than like a generic app shell?

### Information hierarchy
Does the eye know where to go without being shouted at by decoration?

### Calmness
Is motion purposeful? Living does not mean constant motion.

---

## 7. GATE 4 — NAYANET DESIGN LANGUAGE

Verify the product language is coherent with the canonical standards:

- obsidian/deep black foundation;
- deep purple / violet / indigo / blue / cyan / teal / green / gold as meaningful system colors;
- magenta used as an accent rather than overwhelming the interface;
- dimensional surfaces;
- optical/glass depth where purposeful;
- jewel/radial/concentric geometry where meaningful;
- restrained illumination;
- semantic state lighting;
- meaningful energy paths;
- intelligent asymmetry;
- tactile controls.

Reject:

- flat dead rectangles where a meaningful object is required;
- default browser controls where canonical controls are required;
- decorative gradients without state/function;
- giant visual effects that overpower the task;
- generic SaaS dashboard language;
- visual complexity that reduces comprehension.

---

## 8. GATE 5 — INTERACTION PHYSICS

For each primary interactive object ask:

1. What is it?
2. Can I tell it is interactive?
3. What happens when I press it?
4. Does the response happen immediately?
5. Is the state visible?
6. Is the consequence understandable?
7. Can I recover from error?
8. Does the interaction preserve context?

Use:

**INTENT → RESPONSE → TRANSFORMATION**

and:

**DEPTH → LIGHT → STATE → RESPONSE → CONSEQUENCE**

---

## 9. GATE 6 — NAYA / LIVING SUN

Where applicable, verify that Naya is not merely a static graphic.

The canonical interaction vocabulary includes:

- luminous core;
- focal/iris intelligence;
- layered optical depth;
- orbital geometry;
- responsive illumination;
- breathing/idle behavior where appropriate;
- approach/touch response;
- speaking/listening states;
- relationship to player/worlds.

Verify states are meaningful and do not create constant distracting motion.

---

## 10. GATE 7 — POWER PLAYER

Where the Power Player is in scope, verify:

- real artwork/assets where required;
- title/context;
- waveform/equalizer behavior where specified;
- progress;
- play/pause;
- loading;
- error handling;
- Naya response/relationship where specified;
- persistent bottom dock behavior where specified;
- expandable/full-player behavior where specified;
- continuity of selected content and playback state where required;
- no unnecessary page reload;
- mobile behavior;
- keyboard accessibility.

A player that looks premium but cannot reliably play or preserve state is not a 10.

---

## 11. GATE 8 — WORLDS / NAVIGATION

Verify that NayaNET worlds/capabilities are understandable without becoming a wall of feature cards.

Current canonical world model when applicable:

1. Naya Power
2. Super Brain
3. Smart Identity
4. Intelligence
5. Power Player
6. MAXESS
7. Challenge
8. Intelligent Spaces
9. Your Network

Each world should communicate:

**WHAT IT IS → WHY IT MATTERS → WHAT HAPPENS WHEN I ENTER**

---

## 12. GATE 9 — REAL DATA & CAPABILITIES

Verify that claimed capabilities connect to real underlying systems.

Check as applicable:

- Smart Notes persistence;
- Intelligent Feed/receipts;
- Smart Identity;
- consent;
- authentication boundaries;
- Supabase persistence/RLS;
- API contracts;
- Powercast media references;
- MAXESS scoring logic;
- Intelligent Spaces;
- relevant integrations.

Never substitute fake state for a real capability unless the requirement explicitly defines a simulation.

Never claim anonymous authentication is equivalent to an unfinished Smart ID/password contract.

---

## 13. GATE 10 — RESPONSIVE QA

Verify at minimum:

- desktop wide;
- desktop standard;
- tablet-sized viewport;
- narrow mobile;
- larger mobile.

Check:

- no horizontal overflow;
- no clipped controls;
- no broken text hierarchy;
- touch targets remain usable;
- player remains usable;
- navigation remains understandable;
- important content is not buried;
- keyboard remains usable;
- orientation changes do not destroy layout where relevant.

**Mobile is not a shrunk desktop.**

---

## 14. GATE 11 — ACCESSIBILITY QA

Verify as applicable:

- semantic landmarks;
- headings hierarchy;
- accessible names;
- keyboard access;
- visible focus;
- logical tab order;
- no keyboard traps;
- appropriate ARIA;
- dynamic announcements/live regions;
- contrast;
- text scaling;
- reduced motion;
- alternative input;
- captions/transcripts/audio alternatives where required.

A visually impressive experience that excludes users is not a 10.

---

## 15. GATE 12 — FAILURE / EDGE STATES

Every consequential feature must be inspected for:

- loading;
- empty;
- unavailable;
- network failure;
- invalid input;
- permission denial;
- missing media;
- persistence failure;
- retry;
- cancellation;
- duplicate action;
- stale state;
- partial success.

The interface must fail clearly and safely.

Never hide errors simply to preserve the appearance of polish.

---

## 16. GATE 13 — CONTINUITY

Verify preservation of relevant state, including where required:

- identity/name;
- selected Powercast;
- playback position;
- Smart Notes;
- recent meaningful state;
- where the person left off;
- consent state;
- authenticated session boundaries.

Continuity is part of intelligence.

---

## 17. GATE 14 — PERFORMANCE / RELIABILITY

Verify or inspect evidence for:

- fast first interaction;
- stable layout;
- non-blocking audio/media;
- sensible asset loading;
- bounded animation work;
- no obvious event-handler leaks;
- no repeated unnecessary requests;
- graceful media failure;
- no console-critical errors where runtime inspection is available.

If performance cannot be live-measured with available tooling, say so.

---

## 18. GATE 15 — REGRESSION PROTECTION

After implementation, verify protected capabilities that intersect the change surface.

At minimum ask:

- What worked before?
- Could this change have broken it?
- Did we test it?
- Is the previous contract preserved?

Never assume “unrelated” means safe when shared shell/state/styles were changed.

---

## 19. GATE 16 — SECURITY / OWNERSHIP BOUNDARIES

Verify that the change does not expose:

- secrets;
- credentials;
- private user data;
- unauthorized records;
- insecure direct object access;
- unsafe client-side assumptions about authorization;
- sensitive deployment configuration.

Do not put secrets into frontend source.

Do not weaken RLS/auth/consent merely to make a demo work.

---

## 20. GATE 17 — HOLISTIC 10/10 SCORE

Use the canonical weighted scorecard:

| Category | Weight |
|---|---:|
| Immediate Understanding | 12% |
| Push-Button Simplicity | 12% |
| Interaction / Living Responsiveness | 12% |
| Visual Excellence & Craft | 11% |
| Power Player Experience | 10% |
| Navigation & Spatial Architecture | 9% |
| Mobile & Responsive Experience | 9% |
| Emotional Impact / Wow | 8% |
| Accessibility & Inclusivity | 6% |
| Performance & Technical Quality | 6% |
| Consistency / Design System Integrity | 5% |
| **Total** | **100%** |

### 10/10 human test

A child, grandmother, technology expert, and technology-hater should be able to discover and demonstrate the core experience without instruction.

The ideal micro-loop is:

**SEE → UNDERSTAND → PRESS → SOMETHING HAPPENS**

### Mandatory question

> **WHY IS THIS NOT A 10?**

Do not stop at the first acceptable result.

---

## 21. GATE 18 — REPAIR LOOP

For every material sub-10 finding:

```text
FIND
 ↓
CLASSIFY IMPACT
 ↓
CAN WE REPAIR NOW?
 ├─ YES → REPAIR
 └─ NO → DOCUMENT / BLOCK / HUMAN REVIEW
 ↓
VERIFY AGAIN
```

Prioritize defects by:

1. human outcome;
2. broken primary journey;
3. misleading/fake capability;
4. state/interaction failure;
5. data integrity;
6. accessibility;
7. mobile/responsive failure;
8. visual hierarchy;
9. performance;
10. polish.

Do not spend the release cycle polishing a secondary shadow while the primary action is broken.

---

## 22. GATE 19 — RELEASE EVIDENCE

Before release, record:

- tested commit SHA;
- changed files;
- automated checks;
- runtime checks;
- visual/interaction checks;
- responsive checks;
- accessibility checks;
- regression checks;
- deployment result;
- target URL/environment if actually established;
- live verification result;
- human-review items;
- blockers;
- unknowns.

---

## 23. GATE 20 — DEPLOYMENT TRUTH

Use the following distinctions:

**COMMITTED** = source history contains the change.

**BUILT** = build process produced the artifact.

**DEPLOYED** = deployment system reports delivery.

**LIVE VERIFIED** = actual target was inspected.

**PRODUCTION-PROVEN** = live target passed applicable release acceptance.

Therefore:

> **CONNECTED ≠ DEPLOYED.**
>
> **COMMITTED ≠ RELEASED.**
>
> **VERIFIED ≠ PRODUCTION-PROVEN.**

If a deployment plane is unavailable, do not fabricate proof. Mark the release BLOCKED or NOT LIVE VERIFIED as appropriate.

---

## 24. RED / YELLOW / GREEN RELEASE DECISION

### 🔴 RED — DO NOT RELEASE

Any of the following:

- primary journey broken;
- build/runtime broken;
- critical data/persistence failure;
- security/privacy issue;
- fake capability presented as real;
- material accessibility failure;
- major mobile breakage;
- deployment target unknown when release requires it;
- evidence missing for a critical claim.

### 🟡 YELLOW — CONDITIONAL / HUMAN REVIEW

Used when:

- functionality is verified but subjective experience needs human judgment;
- a noncritical limitation remains documented;
- live verification is unavailable;
- external infrastructure is blocking final proof.

Yellow must include the exact limitation and next action.

### 🟢 GREEN — RELEASE-READY

Only when:

- applicable acceptance criteria pass;
- critical regressions are absent;
- repairable high-impact 10/10 findings are addressed;
- required automated/runtime evidence passes;
- deployment target is established;
- deployment evidence exists where required;
- live verification passes where required;
- remaining limitations are explicitly nonblocking and documented.

---

## 25. FINAL RELEASE REPORT

The final report must be factual and concise.

```text
OBJECTIVE:

IMPLEMENTED:

VERIFIED:

LIVE VERIFIED:

DEPLOYED:

PROTECTED CAPABILITIES CHECKED:

10/10 REVIEW:

REPAIRS MADE AFTER REVIEW:

REMAINING LIMITATIONS:

BLOCKERS:

UNKNOWN:

COMMIT:

DEPLOYMENT EVIDENCE:

NEXT BEST ACTION:
```

Do not use vague language such as “everything looks good.”

---

## 26. RELEASE OATH

> **I will not call code complete when the experience is incomplete.**
>
> **I will not call a commit a release.**
>
> **I will not call a deployment live without checking the target when checking is required.**
>
> **I will not hide uncertainty.**
>
> **I will repair what I can.**
>
> **I will ask WHY IS THIS NOT A 10?**
>
> **I will leave evidence strong enough for the next Naya to trust.**

**RELEASE ONLY WHAT CAN BE PROVEN.**
