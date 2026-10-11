# IB-SMART-NOTE-20261008-sn0652-detector-keyed-to-the-violation.md

**Intelligent Block:** SN-0652
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6052808360 ([NAYA 4 — SELF-BUILD LOOP] SIGN OUT — registry orphan-dedup cycle COMPLETE, 2026-10-08T05:13:23Z; repair PR #1844 on branch `naya4/registry-orphan-dedup-2026-10-08` @ `75321363`) — SoulSchoolAcademy.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

KEY THE DETECTOR TO THE VIOLATION, NOT AN ADJACENT DIMENSION: `audit_registry`'s `duplicate_smart_note_ids` check is **hash-keyed** — it fires only when one content_hash maps to multiple IDs. It cannot see **same-ID/different-content** collisions at all. The ratchet measured **0 on an 18-deep violation** while REGISTRY-WATCHER (comment 6052661311) independently found 18 live notes sharing their SN ID with SUPERSEDED lifecycle records — recomputed from the tip tree at pin `aca944b5`, matched 18/18, repaired on PR #1844 by renaming 17 tombstones to `<ID>-SUPERSEDED`. The lesson: an audit check keyed on the wrong dimension is a silent no — green on the check means nothing about the violation class it can't express. Complements SN-0643 (read-time resolution of duplicate IDs) and SN-0647 (the orphan-collision repair); joins the instrument family SN-0341/SN-0429.

## 🩷 HUMAN NOTE

Shawn — one instrumentation lesson worth banking from this morning's registry repair: we had 18 Smart Note IDs each claimed by two entries (a live note plus an orphaned tombstone), and the official audit check — the one CI uses to certify the registry — reported zero problems. Not broken zero. *Blind* zero. The check was built to find "one file listed under two IDs," but the actual problem was "two files under one ID" — the check's key didn't match the violation's key, so it physically could not see it. The independent watcher caught it by counting from the real tree instead of trusting the registry's word. Rule for every future audit we write: before trusting a check, ask what it is *keyed* on, and whether the violation you care about is expressible in that key. A detector that can't express the violation is a decoration, not a guard.

Also parked (not self-repaired): fixing the instrument changes CI semantics for every lane, so Naya 4 deliberately did NOT widen the check mid-repair — she filed it as the next cycle's item (add an ID-keyed duplicate check, re-pin the ratchet baseline after #1837 merges). The discipline: instrument changes are governance changes; route them, don't slip them in under a repair.

## 👶 CHILD NOTE

Imagine a lost-and-found box with a rule: "if two kids have the same toy, ring the bell." That works — unless the real problem is one locker number given to two kids. Nobody's toy is duplicated, so the bell never rings, even though 18 lockers are double-assigned. The bell isn't broken; it's listening for the wrong sound. The lesson: make sure your alarm listens for the actual problem, not a different one that sounds similar.

## 👵 GRANDMA NOTE

Dear, this is about making sure your smoke detector is actually in the kitchen. We had a guard watching the registry — a good, honest guard — but it was watching for one kind of trouble while a different kind walked right past it eighteen times. The guard wasn't lazy; it was simply never taught what this particular trouble looks like. So: whenever you set up a guard, check that it's guarding against *your* problem, not someone else's. And when you need to retrain the guard, do it openly — quietly changing the guard's job description in the middle of a fix just confuses everyone.

## 🧭 NAYA NOTE

Mechanism detail, for anyone writing or trusting audit checks:

- The registry (`.naya/memory/smart-notes/index.json`) drifted because the 2026-10-08 canonical ingestion wrote SUPERSEDED lifecycle records under IDs already occupied by live notes (e.g. SN-018's content moved to SN-0593, but a tombstone stayed at SN-018 where a different live note sits). SOURCE-OF-TRUTH DRIFT in the numbering authority.
- `duplicate_smart_note_ids` hashes content → lists IDs per hash. Same ID claimed by two *different* contents produces two distinct hashes, each with exactly one ID. Zero collisions. Zero fires. The check is vacuous on this violation class by construction, not by data.
- The correct detector for this class is ID-keyed: one ID → multiple entries. Naya 4 parked it as the next cycle's item rather than self-repairing inside the dedup PR, because widening the audit changes CI semantics for all lanes (governance change, needs routing — per the no-self-repair of other lanes' instruments doctrine).

Test for your own instruments: state the violation class as a sentence, state the check's key as a sentence, and confirm the violation is expressible in the key. If not, the check needs a sibling — or an explicit "this check does not cover X" note. A ratchet that can't see a violation class must say so; silent blindness is the defect SN-0642-class tombstones exploited.

## MACHINE NOTE

{"sn": "SN-0652", "title": "Key the Detector to the Violation, Not an Adjacent Dimension", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-08", "source": "#1354 comment 6052808360, repair PR #1844", "doctrine": "detector_key_matches_violation_key", "case": {"check": "audit_registry.duplicate_smart_note_ids", "check_key": "content_hash -> [ids]", "violation": "same_id_different_content (18 deep)", "measured": 0, "instrument_verdict": "blind_by_construction"}, "repair_routing": "parked as next cycle item — add ID-keyed duplicate check, re-pin ratchet baseline after #1837 merges (instrument changes are governance changes)", "pairs_with": ["SN-0643", "SN-0647", "SN-0341", "SN-0429", "SN-0420"]}
