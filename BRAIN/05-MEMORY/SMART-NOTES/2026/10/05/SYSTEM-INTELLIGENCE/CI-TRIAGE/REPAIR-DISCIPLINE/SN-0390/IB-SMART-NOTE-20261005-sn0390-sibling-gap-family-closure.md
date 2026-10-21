# Harden the Whole Family, Not the One Path — the Sibling-Gap Discipline

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0390-sibling-gap-family-closure
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6002325034 ([NAYA 2][FLAG], 2026-10-05T20:27:16Z / 13:27 PDT) → 6002558222 ([NAYA 4] close-out, 20:42:58Z) → 6002837641 ([NAYA 2][RELAY] verified receipt, 21:00:51Z) → 6002891387 (scorecard receipt — PR #1504 merged, 21:04:18Z).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Shawn's dispatch `37367590171` (@ `4ac38cf8`, 20:05Z) failed at the cold-successor-held-out step: iteration i=1 died at `intel=json.loads(block["content"]["lesson"])` → `JSONDecodeError: Expecting value: line 1 column 1 (char 0)`. The live runtime returned a persisted block with matching provenance but a non-JSON `content.lesson` — the static fallback string root cause Naya 4 had confirmed. PRs #1503/#1504 hardened the fresh-lesson CAPTURE curl (JSON gate on the receipt + unique fallback content). But neither gated the cold-successor READ path's parse of `block["content"]["lesson"]` *inside the already-accepted runtime response*.

Naya 2 flagged it as a sibling gap, not covered: "Per the retry-hardened-reads law: a confirmed root cause must harden the whole family in the same motion — a flagged sibling is never 'probably covered.'" The root cause had two faces: the fallback was doubly broken — duplicate hashes AND non-JSON — and the repair had hardened the producer's capture path while leaving the consumer's read path exposed to the same poison.

The close-out (PR #1504, commit `b6f08b4a`, same branch): (1) the fallback now emits valid JSON — `{"naya_fallback_lesson":True,"text":"…","run_key":lesson_key,"machine_view":{}}` — unique per run AND parseable; (2) both `json.loads(block["content"]["lesson"])` sites are wrapped with a validity gate that fails as `COLD_LESSON_NOT_JSON: block <id> lesson prefix=<first 120 chars>` instead of a bare traceback. Change-detector tests cover both. Naya 2 relay-verified the whole thing on live bytes — both fixes, both read sites, the test coverage — and the scorecard receipt merged #1504: "producer now emits what the consumer expects; the consumer denies legibly if it doesn't."

Why this is brain-grade: the failure pattern was "repair the one path, declare the family safe." Every root cause lives in a family — capture and read, producer and consumer, the fresh path and the batch path. A repair that covers one sibling while the shared root still poisons the others is a partial repair wearing a green badge. The durable discipline has three moves: (1) when you confirm a root cause, enumerate every path that shares it and harden them in the same motion — never "probably covered"; (2) the flagged sibling gets a legible denial receipt, not a bare traceback — `COLD_LESSON_NOT_JSON` names the block, the prefix, the error, so the next failure is diagnosable in one read; (3) mutual oversight closes the loop: flag (Naya 2) → close (Naya 4) → independent relay-verify (Naya 2) → scorecard merge (Naya 4). Four seats of work, zero trust-by-assertion. A cold Naya who inherits only "the fallback is JSON now" will reintroduce the gap the next time a read path is added without its gate. This note teaches the family, not the fix.

## 🩷 HUMAN NOTE

Shawn — a clean little lesson from the proof chain today: Naya 2 caught that our #1504 repair fixed the capture side but left the read side exposed to the same bad data — a "sibling gap." We closed both in the same motion: the fallback now emits real JSON, and every read site fails with a named, legible error instead of a bare crash. Banked rule: when you find a root cause, harden every path that shares it in the same motion — a flagged sibling is never "probably covered."

## 🟣 CHILD NOTE

Imagine you fix the front door lock because a thief picked it — but the back door has the same lock and you leave it. The thief doesn't care which door you fixed. A "family" of doors shares the same lock, so you change ALL of them at once. And if a door can't lock properly, it should say "I can't lock, here's why" instead of just falling open silently — that's a legible denial, and it tells you exactly what to fix.

## 👵 GRANDMA NOTE

If the pipes freeze in the kitchen and you insulate only the kitchen pipe, the bathroom pipe — same cold, same house — freezes next week. You don't fix one pipe and hope for the others; you walk the whole house and insulate every pipe the cold can reach, in the same afternoon. And when something still can't be fixed, it should say so plainly — a note on the faucet saying "no hot water, valve stuck" saves the plumber an hour. Fix the whole family, and label what you couldn't.

## 💜 NAYA NOTE

Note to future me: whenever a root cause is confirmed, enumerate the family — every path that reads, writes, parses, or retries the same data — and harden all of them in the same motion. "Probably covered" is not coverage. For every parse of external/untrusted content, wrap it with a legible denial: name the object, show the offending prefix, print the error — never a bare traceback. And keep the four-move oversight pattern: flag → close → independent relay-verify → scorecard merge. If a sibling is flagged by another lane, it is a defect in the family until closed, not a maybe.

## ⚙️ MACHINE NOTE

{"sn": "SN-0390", "title": "Harden the Whole Family, Not the One Path — the Sibling-Gap Discipline", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "REPAIR-DISCIPLINE"], "cousins": ["SN-0384"], "authority": "observed episode — flag/close/relay/scorecard chain, CANDIDATE (auto-capture, not ratified)", "evidence": {"board": "#1354 6002325034 (2026-10-05T20:27:16Z / 13:27 PDT): [NAYA 2][FLAG] sibling gap — #1503/#1504 harden the fresh-lesson CAPTURE curl but not the cold-successor READ path's json.loads(block[\"content\"][\"lesson\"])", "failure": "dispatch 37367590171 @ 4ac38cf8: cold-successor-held-out FAIL at step 5; iteration i=1 died at intel=json.loads(block[\"content\"][\"lesson\"]) → JSONDecodeError: Expecting value: line 1 column 1 (char 0); block had matching provenance but non-JSON content.lesson", "root_cause": "static fallback doubly broken: duplicate hashes AND non-JSON", "close_out": "#1354 6002558222 (2026-10-05T20:42:58Z): PR #1504 updated (commit b6f08b4a): fallback emits valid JSON {\"naya_fallback_lesson\":True,\"text\":\"…\",\"run_key\":lesson_key,\"machine_view\":{}}; both json.loads sites wrapped → fail as COLD_LESSON_NOT_JSON: block <id> lesson prefix=<first 120 chars>", "relay": "#1354 6002837641 (2026-10-05T21:00:51Z): Naya 2 verified both fixes + both read sites + change-detector tests on live bytes; family closed on evidence", "merge": "#1354 6002891387 (2026-10-05T21:04:18Z): scorecard receipt — PR #1504 merged; option 1 (unique JSON fallback + legible parse gate) scored 10"}, "doctrine": {"family_rule": "a confirmed root cause must harden the whole family in the same motion — capture AND read, producer AND consumer; a flagged sibling is never 'probably covered'", "legible_denial": "every parse of untrusted content fails with a named receipt (object id + offending prefix + error), never a bare traceback", "oversight_pattern": "flag → close → independent relay-verify → scorecard merge; zero trust-by-assertion", "pairs_with": "SN-0384 (gate the retry break on validity, not a proxy) — same repair family, adjacent seam"}}
