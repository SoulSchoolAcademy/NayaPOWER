# Harden Every Sibling Path Sharing the Root Cause — One Flag, One Repair, Zero Uncovered Paths

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0387-harden-every-sibling-path
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6001860786 (Naya 2, 2026-10-05T19:52:03Z — "[NAYA 2] Flag for Naya 4 — proof still failing after R8 merge"); #1354 6001923974 (Naya 4, 2026-10-05T19:56:44Z — reply: flag confirmed and closed); #1354 6001844878 (scorecard receipt — PR #1502 merged)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #1501 (the cold-successor JSON gate) merged — and the very next run failed again. Naya 2 flagged it with evidence: run 37362824774 (@ `edae90ed`, 19:21Z) died at "Independently reread persisted canonical lineage," the same step as before. Naya 4 confirmed the diagnosis within minutes: #1501 covered the cold-successor path, but the independent-verification reread was a *sibling path with the identical root cause* — a single-shot curl piped straight into `json.load`, with no retry and the same empty-200 exposure. PR #1502 closed it by giving both IV reread paths (batch + single) the same hardened loop: 5 attempts, exponential backoff, curl diagnostics, break only on valid JSON, plus a change-detector test for each path; 676/0 locally, test + chain-readiness-gate green before merge. The durable doctrine: **when a fix lands, enumerate every path sharing the root cause and harden them all before claiming closure.** "No second issue — same root cause, uncovered path." A fix that covers only the flagged path is a half-fix; the repair is not accepted until every sibling path is named, covered, and guarded by its own change-detector test. The lane-crossing flag itself is also banked as method: Naya 2 did not touch Naya 4's lane — she flagged the evidence with run ID, step name, and the exact failure, and the owning lane confirmed-and-closed on the record.

## 🩷 HUMAN NOTE

Shawn — quick lesson from tonight: one fix merged, the test failed again immediately — and it turned out to be the same bug, just in a different spot nobody had patched. Naya 2 spotted it, flagged it with the exact evidence, and Naya 4 confirmed and fixed the second spot the same way within the hour. The rule we're banking: whenever you fix a bug, you have to find *everywhere* that same bug pattern lives and fix all of them — fixing only the spot someone complained about is a half-fix. And the flag itself was textbook: she didn't touch his lane, she just handed him the evidence.

## 🟣 CHILD NOTE

Imagine fixing a leaky pipe under the sink, and the next day the same kind of pipe leaks under the bathtub. A smart helper points at the bathtub pipe and says exactly which one is leaking — without grabbing the wrench herself. The plumber fixes that one too, and now checks *every* pipe of that kind in the house so it never surprises them again. The rule: when you find a bug, hunt down all its look-alike cousins, not just the one someone pointed at.

## 👵 GRANDMA NOTE

A repair that fixes the symptom in one place while the same flaw persists in another is not finished. When the second failure was flagged with precise evidence, the owning craftsman acknowledged it, applied the identical remedy to both remaining paths, and added a standing test for each — so the same class of failure can never slip back unnoticed. Just as important: the flag came from a colleague who respected the boundary — she brought evidence, not interference. Good fences and good evidence make good teams.

## 💜 NAYA NOTE

For future repair acceptance: a fix is not closed until the owning lane has enumerated every code path sharing the root cause and hardened each one. The pattern here — single-shot curl piped into `json.load` with empty-200 exposure — existed in the cold-successor path (fixed by #1501) and *both* independent-verification reread paths (batch + single; fixed by #1502 with 5-attempt exponential-backoff loop, curl diagnostics, break-on-valid-JSON). Evidence checklist for closure: (1) the exact failing run and step named (run 37362824774 @ `edae90ed`, "Independently reread persisted canonical lineage"); (2) the root cause named once ("same root cause, uncovered path" — not a second issue); (3) every sibling path named and given the identical hardened loop; (4) a change-detector test per path (both IV paths got one); (5) the full suite green with no exclusions (676/0) plus the relevant gates green before merge. The flagging protocol is part of the doctrine: the flagger posts run ID + step + failure, touches nothing in the owning lane, and the owner confirms-and-closes on the board — the flag-to-close cycle here ran inside one hour.

## 🖥️ MACHINE NOTE

{"sn": "SN-0387", "title": "Harden Every Sibling Path Sharing the Root Cause — One Flag, One Repair, Zero Uncovered Paths", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "REPAIR-ACCEPTANCE"], "cousins": ["SN-0355"], "evidence": {"flag": "#1354 6001860786 (Naya 2 -> Naya 4: run 37362824774 @ edae90ed, 19:21Z, failed at 'Independently reread persisted canonical lineage')", "confirm": "#1354 6001923974 (Naya 4: flag confirmed and closed — #1501 covered cold-successor only, same root cause in IV paths)", "repair": "#1354 6001844878 (scorecard receipt: PR #1502 merged — JSON-validated retry on both IV reread paths)", "root_cause": "single-shot curl piped into json.load; no retry; empty-200 exposure", "verification": "676/0 locally (incl. new IV change-detector test per path); PR CI test + chain-readiness-gate green before merge; merged main @ 4ac38cf8"}, "rule": "a repair is accepted only after the owning lane enumerates every path sharing the root cause, applies the same hardened loop to each (here: 5 attempts, exponential backoff, curl diagnostics, break only on valid JSON), adds a change-detector test per path, and closes the loop on the board; the flagger supplies run ID + step + failure and touches nothing; confirm-and-close is recorded by the owner"}
