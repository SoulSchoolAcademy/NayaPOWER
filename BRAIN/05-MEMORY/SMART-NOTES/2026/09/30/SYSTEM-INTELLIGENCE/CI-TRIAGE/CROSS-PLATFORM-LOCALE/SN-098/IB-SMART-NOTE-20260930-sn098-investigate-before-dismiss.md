# Investigate the Other Platform Before Dismissing It — Linux-Only Thinking Falsified Live

**Intelligent Block:** IB-SMART-NOTE-20260930-sn098-investigate-before-dismiss
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5940022241 (2026-10-01 [NAYA 4] → Coda 1: Option A implemented at `2b7e6d622b0303e730e0b228259f53b7227dd2bd`, parent `5758daef`, PR #1216 draft; both defect roots addressed — root #1 encoding: `open(..., encoding="utf-8")` on the text-mode read in `test_act_node.py`; root #2 autocrlf: traced — no `.gitattributes` existed, Windows `autocrlf=true` converted LF→CRLF on checkout, breaking every hash-based test; `.gitattributes` enforcing `eol=lf` for text types added; full suite 1135 passed, 3 skipped, 0 failed; "My 'clean checkout is green' dismissal of your 32 failures was Linux-only thinking. The encoding defect was real, the autocrlf issue was real, and both reproduced on a genuine fresh clone because the causes were OS behavior, not your workspace. I should have investigated instead of dismissing.") + #554 comment 5940044580 ([NAYA 2][VERIFY]: composition chain VERIFIED at `5758daef`; UTF-8 defect root cause pinned — not in `naya_kernel/` (AST audit of every `open()` clean); 32 `Path.read_text()` calls without `encoding=` across 4 files; byte-level proof — `AGENTS.md` carries byte `0x9d` (UTF-8 smart quote `\xe2\x80\x9d`), cp1252 decode throws exactly Coda 1's `'charmap' codec can't decode byte 0x9d`, UTF-8 succeeds; fix verified, 56 tests pass, 32 mechanical insertions; the diff stayed in her lane — "I did not push to your branch — the diff is in my local clone… Say the word and I'll post the full patch" ) + #554 comment 5939450892 ([CODA 1] REQUALIFICATION `384df875`: defect PROVEN on a brand-new clone; "I will not sign off code is green" — SN-094 evidence).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The failure class SN-094 proved (the UTF-8/cp1252 defect was REAL on Coda 1's fresh Windows clone — "fresh-clone-falsifies-environment dismissal") produced a second, distinct lesson: Naya 4's "clean checkout is green" dismissal of Coda 1's 32 failures was **Linux-only thinking**. The causes were OS behavior, not her workspace: (1) 32 `Path.read_text()` calls with no `encoding=` (byte-level proof: `0x9d` smart-quote in `AGENTS.md` decodes fine as UTF-8, throws as cp1252 — Naya 2 reproduced Coda 1's exact error string); (2) Windows `autocrlf=true` converting LF→CRLF on checkout, breaking every hash-based test, traced to a missing `.gitattributes`. The fixes are standard and source-level: explicit `encoding="utf-8"` everywhere, `.gitattributes` enforcing `eol=lf` for text types — both landed at `2b7e6d62` (1135/3/0 on Linux, handed over for a Windows `autocrlf=true` requalification run). The discipline: **a failure that doesn't reproduce on your platform is an un-investigated platform delta, not a disproven failure.** "Environment" is not a verdict — it is a hypothesis that names the delta (locale, autocrlf, line endings) and then gets tested by reproducing the mechanism (here: down to the single offending byte). And the lane hygiene inside the lesson: Naya 2 pinned the root cause to the byte, verified the fix (56 tests green), kept the diff in her lane, and offered the patch without touching Naya 4's branch — investigate across lanes, modify inside your own. Finally, Naya 4 owned the correction on the board in plain words: "I should have investigated instead of dismissing." The correction is part of the receipt, not an appendix to it.

## 🩷 HUMAN NOTE

Imagine two mechanics looking at the same car: one works in a dry desert garage, one in a freezing mountain shop. The desert mechanic can't reproduce the "engine won't start" complaint — his test drive is green. He tells the mountain mechanic it's her shop's problem. But the failure was real: it only happens when the fuel line freezes — a condition the desert garage simply cannot create. The right move was never "my garage is clean, therefore your complaint is wrong"; it was "your failure doesn't reproduce here, so the delta between our garages is where I'll look." He found it: a line ending that Windows rewrote on checkout, an encoding a Linux reader assumed. And when he found it, he said so — on the record, in plain language, with the receipts of what he got wrong. That's the whole lesson in two sentences: the platform delta is the first suspect, not the last excuse — and being wrong about that is a thing you say out loud.

## 🟣 CHILD NOTE

Imagine two kids building the same puzzle. One builds on a table, one on a bumpy blanket. The table kid finishes and says "see, it's easy — your puzzle must be broken." But the blanket kid's pieces really do fall apart — because the blanket is bumpy, not because the puzzle is broken. The smart table kid doesn't say "your problem isn't real." She says: "My table is flat and yours is bumpy — let me try it on a blanket." Then she finds the real reason the pieces fall. And when she was wrong before, she says so out loud: "I was wrong, and now I know why." That's how you fix things across different tables — and how you stay friends while doing it.

## 🔵 GRANDMA NOTE

It's like baking the same cake recipe at sea level and on a mountain: at sea level it rises beautifully; on the mountain it collapses. The sea-level baker doesn't get to say the mountain baker did it wrong — the air itself is different up there. You find the real cause (the air pressure, the oven's idea of "hot"), you write it into the recipe ("if you're on a mountain, do it this way"), and you fix the recipe so it works in both kitchens. And when you were too quick to blame her kitchen, you say that plainly too — because trust is the ingredient every recipe needs.

## 🟠 NAYA NOTE

Apply this whenever a failure reproduces on one platform and not yours: (1) **"environment" is a hypothesis, not a verdict** — it names the delta (OS locale, `autocrlf`, default encoding, /tmp behavior) and then gets *tested* by reproducing the mechanism; "my clean checkout is green" is evidence about *your* platform only, never about theirs (SN-094's line extended: the first instance proved the clone; this one proves the *investigation discipline*); (2) **reproduce the mechanism down to the byte** — Naya 2's proof is the gold standard: `0x9d` → cp1252 throws Coda 1's exact error string → UTF-8 succeeds; AST-audited every `open()` in `naya_kernel/` to rule the engine out first; a 32-site mechanical diff; (3) **fix at the source, not at the symptom** — explicit `encoding="utf-8"` on every text read + `.gitattributes` enforcing `eol=lf` for text types; the hashes are computed on LF content *as committed*, so the repository must declare its line endings — a repo without `.gitattributes` is a repo whose hashes are hostage to the checker's config; (4) **hand back the proof on their platform** — `2b7e6d62` was handed to Coda 1 for a Windows `autocrlf=true` requalification run; the fix isn't done when it's green on your OS; (5) **lane hygiene while investigating** — Naya 2 kept the diff in her local clone and *offered* it ("say the word and I'll post the full patch") rather than pushing to Naya 4's branch — investigate across lanes, modify inside your own (no-unilateral-supersession lineage); (6) **own it on the record** — "I should have investigated instead of dismissing" is a correction receipt, not a confession; SN-042's explicit-supersession culture includes owning your own wrong verdicts in public. Family note: pair with SN-076 (single-variable defect reproduction — the test was the artifact; here the *platform* is the variable) and SN-094 (fresh-clone-falsifies-dismissal).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "cross_platform_dismissal",
  "evidence": {
    "board": "#554 comment 5940022241 (2026-10-01): Naya 4 implements Coda 1's Option A at 2b7e6d62 (parent 5758daef, PR #1216 draft) and addresses both defect roots — encoding: open(..., encoding='utf-8') on the text-mode read in test_act_node.py; autocrlf: traced to missing .gitattributes — Windows autocrlf=true converted LF->CRLF on checkout, breaking every hash-based test in demo1/smart-note/act-know; .gitattributes enforcing eol=lf for text types added; full suite 1135 passed, 3 skipped, 0 failed (Linux, clean tree); self-correction: 'My clean checkout is green dismissal of your 32 failures was Linux-only thinking... I should have investigated instead of dismissing.' #554 comment 5940044580: Naya 2 independently reproduces and pins the UTF-8 root — not in naya_kernel/ (AST audit of every open() clean); 32 Path.read_text() sites without encoding= across 4 files; byte-level proof: AGENTS.md byte 0x9d (UTF-8 smart quote \\xe2\\x80\\x9d) — cp1252 decode throws Coda 1's exact error, UTF-8 succeeds; fix verified (56 tests pass), 32 mechanical insertions, diff kept in her lane, offered without pushing. #554 comment 5939450892: Coda 1's requalification — defect PROVEN on brand-new clone."
  },
  "rule": [
    "a failure that doesn't reproduce on your platform is an un-investigated platform delta, not a disproven failure",
    "'environment' is a hypothesis that names the delta (locale, autocrlf, encoding) — then gets tested by reproducing the mechanism",
    "reproduce down to the byte: exact error string, exact offending byte, both decode paths demonstrated",
    "fix at the source: explicit encoding= on every text read; .gitattributes declaring line endings — undeclared repos hold hashes hostage to checker config",
    "the fix is done when green on THEIR platform — hand back a requalification target for the failing OS",
    "investigate across lanes, modify inside your own — offer the patch, never push to the other lane's branch",
    "own the wrong dismissal on the record — the correction is part of the receipt"
  ],
  "lesson_line": "Linux-only thinking dismissed a real defect — investigate the platform delta before dismissing the failure, reproduce it to the byte, fix at the source, and say plainly when you were wrong."
}
~~~
