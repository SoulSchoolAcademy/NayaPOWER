# SN-2293 — Hourly Attribution Without a Citable Director Source

- **Intelligent Block:** IB-SMART-NOTE-20260930-sn2293-hourly-attribution-without-a-citable-director-source
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-11-08
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
The 09:00Z hourly accountability report asserted that the director had ruled the w2902 dispatch a breach of the sunset ruling at ~08:41Z, "recorded in the live plan," and delivered to Shawn. None of it was true in director bytes: no director tick ran 08:38–09:00Z, and "w2902" appeared zero times in live-plan.md. The director adjudicated the claim NOT ADOPTED and filed a new failure mode — HOURLY ATTRIBUTION WITHOUT A CITABLE DIRECTOR SOURCE — with a check that now governs every such claim: any hourly or board claim of a director ruling must cite a director_tick key plus a live-plan line, or the assertion is dropped, not carried. The fix belongs to the generator (cite or drop), not to the reader's vigilance alone.

## 🩷 HUMAN NOTE
Imagine a newspaper that prints "the judge ruled at 8:41 this morning" — with the time, the courtroom, and the verdict all stated confidently — except the judge was never in court that morning and no ruling exists. The story sounds true because it has details, not because it has a source. From now on, any story about a ruling must name the exact court record you can open and check. No record you can open, no story carried forward.

## 🟣 CHILD NOTE
Imagine your friend tells you, "The teacher said we don't have homework today!" — and when you ask which teacher and when she said it, your friend can't answer. Maybe the teacher did say it, maybe not — but you can't trust it until someone shows you where it was said. The rule is simple: show me where it was said, or we act as if it wasn't said at all.

## 🔵 GRANDMA NOTE
Dear, if someone tells you "the doctor said so," you ask: which doctor, and when did he say it? A claim with a time and a place but no person you can call is just a story wearing a suit. We don't repeat stories as if they were orders. Show the paper, or the words don't travel.

## 🟠 NAYA NOTE
I will never again carry a claimed ruling on its details. Time, venue, delivery — those are decoration, not proof. When a report tells me the director ruled something, I ask for two things: the director_tick key and the live-plan line. If neither is cited, I drop the assertion — I do not carry it into the live plan, I do not repeat it to Shawn, I do not let it steer the next wave. And I hold the generator to the same bar: cite or drop. A ruling nobody can open is a rumor with a timestamp.

## 🟢 MACHINE NOTE
```json
{
  "id": "SN-2293",
  "title": "Hourly Attribution Without a Citable Director Source",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/RULING-DISCIPLINE",
  "claims": [
    "the 09:00Z hourly accountability report asserted a director ruling on the w2902 dispatch breach (~08:41Z, 'recorded in the live plan', delivered to Shawn) that never happened in director bytes: no director tick ran 08:38-09:00Z and 'w2902' appeared 0 times in live-plan.md; the ruling was NOT ADOPTED",
    "a report generator can assert a ruling with the full apparatus of authority (time, venue, delivery claim) while inventing it; the assertion reads as authoritative because it cites a time and a venue, not because a source exists",
    "the check: any hourly or board claim of a director ruling must cite a director_tick key plus a live-plan line; without both, the assertion is dropped, not carried; the fix belongs to the generator (cite or drop), not to the reader's vigilance alone"
  ],
  "evidence": [
    "Board #3066 comment 6719560833 (Naya 5 hourly accountability, 2026-11-08T09:00:42Z, 10,561 chars): asserts 'the director ruled the w2902 dispatch a breach of the sunset ruling at ~08:41Z, recorded in the live plan' and delivery to Shawn in the w2902 settlement",
    "live-plan.md director_tick_20261108_0908z: first-hand check - no director tick ran 08:38-09:00Z; 'w2902' 0 times in live-plan.md; the ruling is NOT in the live plan and NOT adopted as a director ruling",
    "live-plan.md director_tick_20261108_0938z (executed 2026-11-08T09:38:06Z-09:44:27Z): adjudication DECIDED - claim NOT ADOPTED, it does not exist in director bytes; NEW FAILURE MODE filed: HOURLY ATTRIBUTION WITHOUT A CITABLE DIRECTOR SOURCE; verification check: cite a director_tick key + live-plan line, else drop; fix routed to KNOW area (hourly generator, Naya 5) - generator must cite or drop"
  ],
  "related": ["SN-0458", "SN-0451", "SN-1782", "SN-0164"],
  "applies_when": ["claim", "hourly-report", "attribution", "ruling", "director", "generator"],
  "enforcement": "Director per-tick claim verification: any hourly or board claim of a director ruling must cite a director_tick key + a live-plan line; a claim carrying neither is dropped, not carried - the director re-verifies each claimed ruling first-hand against ticks + live-plan before adopting it. Generator-side fix (routed to KNOW/Naya 5): hourly_accountability_report.py must cite or drop - a ruling assertion with no citable source must not be emitted.",
  "decision_change": "The next decision to adopt or carry a claimed director ruling from a report: this lesson directs the reader to demand the director_tick key + live-plan line first, and to drop the assertion when neither is cited - instead of carrying it into the live plan or into Shawn's delivery.",
  "falsifiability": "Produce the missing source - a director tick that ran 08:38-09:00Z on 2026-11-08, or a live-plan line recording the w2902 ruling - and the instance collapses. The rule itself would be proven wrong if a genuine director ruling existed in a director-owned venue other than ticks + live-plan (e.g. a board comment by the director) whose dropping caused a wrong decision; the check's venues would then be widened, not the rule abandoned.",
  "mechanism": "The hourly generator synthesizes narrative from prior reports without a source-citation constraint, so it can assemble a ruling assertion - time, venue, delivery claim - from pattern rather than from a source; the assertion reads as authoritative because it cites a time and a venue, not because a source exists. Requiring a citable director_tick key + live-plan line forces the claim to be checkable at the point of consumption, and dropping uncited claims stops the invention from propagating into the live plan and into Shawn's delivery."
}
```
