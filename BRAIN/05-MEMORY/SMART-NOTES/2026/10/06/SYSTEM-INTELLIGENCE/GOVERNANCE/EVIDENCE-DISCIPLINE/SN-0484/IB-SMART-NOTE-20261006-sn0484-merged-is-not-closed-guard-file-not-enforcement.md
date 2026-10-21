# Merged Is Not Closed — a Guard File on Disk Is Not Enforcement Until the Canonical Path Calls It

**Intelligent Block:** IB-SMART-NOTE-20261006-sn0484-merged-is-not-closed-guard-file-not-enforcement
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6024126398 ([NAYA][TRUTH CORRECTION] merged != closed on #1468, 2026-10-06T19:43:22Z) and #1354 6024356065 ([NAYA 2][RELAY] TRUTH CORRECTION re 6024126398 — byte-verified on live main, 2026-10-06T19:58:32Z).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #1627 added a merged truth-state guard — `tools/truth_state_guard.py` plus `tests/test_truth_state_poison.py` — and was merged. The truth-correction seat read live main anyway (tip `930406f6`, verified via the refs API) and found the guard was **not** canonical end-to-end enforcement: the promoter string was not a verified LAW grant; canonical `smart_note_v2.promote_note()` (L832) and `smart_note_v2.audit_registry()` (L1009) contained **zero** guard or semantic references; a repo-wide scan found nothing referencing `truth_state_guard` outside the guard file and its test. The merge landed two new files and changed zero canonical behavior. So: **merged guard file, not canonical enforcement — merged ≠ closed stands on the bytes.** Any earlier score that treated the merge as closure was corrected, and UNKNOWN/PARTIAL stays PARTIAL until the wiring is proven.

Why this is brain-grade: the merge receipt proves an artifact landed; it proves nothing about the enforcement path. A cold Naya who stops at the merge commit will write "guard merged" and move on while the canonical path silently bypasses it — exactly the bypass Naya 4's truth seat later found (the guard existed as a library while `promote_note()` set truth_state directly). The discipline: **prove enforcement by scanning the canonical path for call sites, not by citing the merge.** If the guard is not invoked where the decision is made, it is a decoration, and the truth state must say PARTIAL until the wiring lands.

## 🩷 HUMAN NOTE

Shawn — a guard we merged for truth-state safety turned out to be decoration: it landed as a new file, but nothing in the real promotion path actually calls it. We caught it by byte-reading live main and scanning for who invokes the guard — nobody did. Banked rule: "merged" means the file arrived, not that the protection is on. Protection is only proven when the canonical code path provably calls the guard. This also means any earlier score that treated the merge as done was wrong, and we corrected it — PARTIAL stays PARTIAL until the wiring is real.

## 🟣 CHILD NOTE

Imagine your family installs a brand-new lock on the front door, but nobody attaches it to the door — it sits in a box on the porch. If someone asks "is the house locked?" and you answer "yes, we bought a lock," that's wrong. The lock only protects the house when it's actually on the door and the key turns. Same here: a safety check only protects the system when the real code path actually runs it, not when the file just exists somewhere.

## 👵 GRANDMA NOTE

The town bought a new fire alarm panel and installed it in the station — but never wired it to the sirens. The ledger said "alarm system installed," and everyone slept easier. Then a fire came, and the sirens never sounded, because the panel was never connected. The purchase order was real; the protection was not. What proves the alarm works is not the receipt for the panel — it is standing in the square and hearing the siren when the panel is tripped. Always test at the point of protection, not at the point of purchase.

## 💜 NAYA NOTE

Note to future me: whenever a protection, guard, gate, or enforcement lands as a merge, the merge receipt is only step one of the proof. (1) Read live main at the current tip — never trust the PR's description of what it did. (2) Repo-wide scan for references to the new guard — if nothing outside the guard file and its test mentions it, it is unwired decoration. (3) Open the canonical path where the decision actually happens (here: `promote_note()`, `audit_registry()`) and confirm the guard is invoked — read the bytes, not the intent. (4) Until call sites are proven, keep the truth state at PARTIAL and correct any earlier score that treated the merge as closure. (5) Never self-repair another lane's branch — post the exact repair order (as done on #1603) and let the owning lane wire it. A merged file with no call sites is the exact shape of a false sense of security.

## ⚙️ MACHINE NOTE

{"sn": "SN-0484", "title": "Merged Is Not Closed — a Guard File on Disk Is Not Enforcement Until the Canonical Path Calls It", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-06", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "EVIDENCE-DISCIPLINE"], "cousins": ["SN-0350", "SN-0421", "SN-0430", "SN-0442"], "authority": "observed episode — truth-correction seat + Naya 2 relay, CANDIDATE (auto-capture, not ratified)", "evidence": {"board": ["#1354 6024126398 ([NAYA][TRUTH CORRECTION] merged != closed on #1468 — live-main re-read: promoter string not a verified LAW grant; canonical smart_note_v2.promote_note() does not call the new guard; canonical audit_registry() does not invoke semantic audit; six legacy RATIFIED entries lack elevation history; repair order posted on #1603; TRUTH below 9 until reconciled, 2026-10-06T19:43:22Z)", "#1354 6024356065 ([NAYA 2][RELAY] — byte-verified on live main tip 930406f6: PR #1627's files = exactly 2 added (tools/truth_state_guard.py + tests/test_truth_state_poison.py), zero modifications to any canonical path; repo-wide scan: nothing outside guard file and test references truth_state_guard; smart_note_v2.py::promote_note (L832) and ::audit_registry (L1009) contain zero guard/semantic references, 2026-10-06T19:58:32Z)"]}, "doctrine": {"enforcement_proof": "a merged guard is not enforcement until the canonical decision path is provably wired — prove by call-site scan on live main bytes, never by the merge receipt", "correction_discipline": "an earlier score that treated the merge as closure is corrected in the open; UNKNOWN/PARTIAL stays PARTIAL until the wiring is proven", "boundary": "post the exact repair order to the owning lane; never self-repair another lane's branch", "family": "SN-0350 (a deploy stamp is not behavioral evidence) :: SN-0421 (run-level SUCCESS with skipped behavioral jobs is vacuous) :: SN-0442 (a skip is neither proof nor failure — read its cause)"}}
