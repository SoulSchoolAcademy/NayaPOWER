# Verification Instruments Must Be Total Functions — a Crashed Check Yields No Verdict, Worse Than Drift

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0786-verification-instruments-must-be-total-functions
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6083451482 ([NAYA 2 — BRAIN-BUILD LOOP] SCORECARD: merge PR #1976 — 2026-10-09 ~08:40 PDT); #1354 comment 6083525362 ([NAYA 2 — BRAIN-BUILD LOOP] PR #1976 MERGED-VERIFIED AT TIP — 2026-10-09). Source: SoulSchoolAcademy (Naya 2 lane).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #1971 added `BRAIN/00-ACTIVATION/` and broke the brain-index verification instrument: `regenerate_brain_index.py --check` died with `KeyError: '00-ACTIVATION'` because the renderer indexed `DOMAIN_TITLES[d]` directly while `domain_of()` returns any raw `BRAIN/<X>/` segment. The battery's brain-index instrument was blind on every run until fixed — a crashed `--check` produces NO verdict at all, and no verdict is worse than DRIFT: drift is a known state you can route and repair; a crash is a blind spot masquerading as a verification run.

The fix was one line — `DOMAIN_TITLES.get(d, d + ' — (unregistered domain)')` — plus 4 negative tests. `--check` now exits 1 with honest DRIFT (2 unindexed files, owned by wave-sequenced #1900) instead of dying. Naya 2's scorecard explicitly rejected the alternative shape (register `00-ACTIVATION` as a formal domain in the script): the taxonomy decision belongs to the activation lane, and a fail-safe fallback hardens the tool against the NEXT unknown domain while registration only fixes this one. Focused tests on exact head bytes: 8/8 pass (4 new negative + 4 existing). Full pytest: 1482 passed / 5 failed / 11 skipped / 1 collection error — every failing class verified pre-existing on base SHA, zero PR-introduced. Post-merge faithfulness proved at tip `ec1341597`: live tip == merge commit ancestry, key blobs byte-identical at PR head, merge commit, and tip.

Rule for a cold successor: **verification instruments must be total functions — unknown-but-legal input → honest verdict, never an exception.** When your check crashes on a new-but-legitimate input, the repair is in the instrument's input handling (fail-safe default + tests), never in bending the world to match the instrument's assumptions — and never in weakening the check to make the crash go away.

## 🩷 HUMAN NOTE

Shawn — one lesson from this morning's brain-build work, and it's a good one. Naya 2 found that adding the activation package to the brain broke the brain-index verification tool — it crashed with a `KeyError` on every run instead of reporting anything. A checker that crashes gives you no answer at all, which is worse than a checker that says "there's drift here," because at least drift tells you what to fix. The fix was one line: instead of demanding every brain folder be registered, the tool now reports unregistered folders honestly. She also refused the tempting shortcut — registering the new folder inside the checker — because that only fixes this one case; the fallback handles the next one too. Merged and verified at the live tip, with all failing tests proven pre-existing, not caused by her change.

## 🟣 CHILD NOTE

Imagine a smoke detector that, instead of beeping, quietly dies whenever it smells a NEW kind of smoke. You'd think everything is fine — but it's just broken. That's what happened to one of the team's checker tools: when a brand-new brain folder appeared, the checker crashed and said nothing, which is worse than saying "something's off." The fix teaches the checker to say "hey, there's a folder I don't know yet — here it is" instead of dying. And when they considered the lazy fix — just telling the checker about that one folder — they said no: the better fix handles ANY new folder, forever. Moral: make your checkers tough enough to admit what they don't know, and never make the world smaller just to please the checker.

## 👵 GRANDMA NOTE

The team's automatic checker for the brain's index broke when a new section was added — instead of reporting a problem, it just crashed and reported nothing. A crash is worse than a "needs attention" verdict, because "needs attention" tells you where to look and a crash tells you nothing while pretending the check ran. The team fixed the checker to handle unknown sections gracefully — report them honestly — and proved the fix works with tests. They deliberately avoided the quick patch that would only have fixed this one case, choosing the repair that keeps working for future unknowns.

## 🟠 NAYA NOTE

Every verification instrument you ship must be a total function over its legal input space: unknown-but-legal input → honest verdict (exit code + named state), never an unhandled exception. A crashed check yields NO verdict — worse than DRIFT, because drift is a known state you can route, while a crash is a blind run that looks like verification happened. When a new legitimate input crashes your instrument: (1) repair in the instrument's input handling with a fail-safe default, (2) add negative tests for the unknown input, (3) never fix it by registering this-one-case inside the tool when a general fallback exists — classification decisions belong to the owning lane. Verify the heal on exact-tip bytes: focused tests green, full suite delta vs base SHA proven clean, post-merge blob identity re-proven at the new tip.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0786",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INSTRUMENT-HARDENING",
  "doctrine": "total-function-instruments",
  "rule": "Verification instruments must be total functions — unknown-but-legal input produces an honest verdict (exit code + named state), never an unhandled exception. A crashed check yields no verdict, which is worse than DRIFT.",
  "failure_mode": "PR #1971 added BRAIN/00-ACTIVATION/; regenerate_brain_index.py --check died with KeyError: '00-ACTIVATION' on every run — renderer indexed DOMAIN_TITLES[d] directly while domain_of() returns any raw BRAIN/<X>/ segment; the battery's brain-index instrument was blind until fixed",
  "mechanism": {
    "fix": "DOMAIN_TITLES.get(d, d + ' — (unregistered domain)') — one line fail-safe + 4 negative tests",
    "rejected_alternative": "registering 00-ACTIVATION in the script — taxonomy decision belongs to the activation lane; the fallback hardens against the NEXT unknown domain",
    "evidence": "8/8 focused tests on exact head bytes (4 new negative + 4 existing); --check exits 1 with honest DRIFT post-fix; full pytest 1482 passed/5 failed/11 skipped/1 collection error — all failing classes verified pre-existing on base SHA; post-merge blob identity re-proven at tip ec1341597"
  },
  "related": ["SN-0341", "SN-0428", "SN-0429", "SN-0658", "SN-0648"],
  "provenance": ["#1354 comment 6083451482", "#1354 comment 6083525362"]
}
