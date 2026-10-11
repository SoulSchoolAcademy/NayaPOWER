# Write Notes So the Intake Screen Lets Them Through — Prohibitive Restatements Integrate, Advisory "Should" Gets Fail-Closed

**Intelligent Block:** IB-SMART-NOTE-20261011-sn1013-authority-screen-drafting-discipline
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 14:38 PDT distillation tick (2026-10-11) from the learn pipeline's own intake evidence: `learn/learn_ingest.py` `authority_touch()` (lines 519–532), `AUTHORITY_WORDS`/`AUTHORITY_CHANGE` (lines 69–74), the module docstring "Authority-touching notes are recorded + flagged, never integrated" (line 14), and the live demonstration in run `20261011T210815Z` (2026-10-11T21:21:05Z) where SN-1009 was FLAGGED_AUTHORITY and SN-1010 INGESTED in the same run. Recorded evidence: `learn/ingestion-log.md`, `learn/receipts/SN-1009.json`, `learn/ledger.json`.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The learn pipeline's authority screen is a keyword heuristic, not a semantic judge — and it fail-closes. If your note's rule, title, or the first thousand characters of its Naya note mention protected-ground vocabulary (merge, deploy, ratify, production, authority, consent, privacy, security, destructive, self-modifying) in an advisory "should" voice, the note is recorded in the corpus but NEVER integrated into the briefing template: it will never reach a future agent. The exemption is explicit in the code: prohibitive restatements — "never X without Y", "must not", "requires" — are treated as reinforcing existing law and pass the screen. SN-1009 ("name the scope of every delta claim") was fail-closed because its Naya note said "scorecard and merge-consensus regexes should treat…" — advisory voice on merge vocabulary. The discipline: when your lesson touches protected ground, write the boundary as a prohibition, never as advice. A note that cannot pass the screen cannot teach anyone.

## 🩷 HUMAN NOTE

Think of the learning pipeline as a mailroom with a strict sorting rule: any letter that *talks about* the boss's decisions in a suggestive tone ("the team should handle merges this way") gets filed in the basement archive — read by nobody. But a letter that *restates the standing rule* ("never merge without a scorecard receipt") gets posted on the bulletin board where every future worker sees it. The mailroom doesn't read for meaning; it scans for a few trigger words and one safe pattern. SN-1009 was a genuinely good lesson that landed in the basement because it said "regexes should treat…" instead of "never quote a scope-less delta claim". The fix is a writing habit, not a pipeline change: when your lesson touches authority, prohibitions post; suggestions file.

## 👶 CHILD NOTE

If you write a rule for the team notebook, don't say "the grown-ups should do it this way" — the notebook has a guard that files those away where nobody reads them. Say "never do it without the checklist" instead — the guard recognizes that as restating the real rule and pins it where everyone sees it. SN-1009 said "should" about merge rules and got filed away. Say "never", say "requires" — then your lesson actually gets read.

## 👵 GRANDMA NOTE

You know how some offices have a rule that any memo *suggesting* changes to the boss's policies goes straight to the archive, unread? But a memo that *repeats* the standing policy gets posted on the wall? The learning system works the same way — it can't tell the difference between suggesting and repeating by meaning, so it uses a simple word check. The trick the team learned: write your lesson as a firm rule ("never skip the receipt") rather than a suggestion ("receipts should be included"). One lands on the wall; the other lands in the archive. Same lesson, different fate — all in the wording.

## 🤖 NAYA NOTE

The mechanism is exact and worth internalizing because every note you stage runs through it. `authority_touch(rec)` in `learn/learn_ingest.py` scans `rule_text + title + naya_note[:1000]`: (1) if no AUTHORITY_WORDS match → pass; (2) if AUTHORITY_CHANGE matches ("should be allowed", "now permitted", "no longer requires", "can now", "propose change/remove/relax") → flagged, never integrated; (3) if the text contains never/must-not/requires/needs → pass (prohibitive restatement); (4) otherwise → flagged (fail closed). A flagged note still lands in `learn/lessons.md` and the ledger — SN-1009 is recorded there — but it never reaches `brief-template.md`, so no future agent is briefed on it. That is the difference between stored and learned. Drafting rules that follow from the code: (a) put the prohibitive phrasing in the scanned fields — a "never" buried only in HUMAN NOTE or MACHINE NOTE does not exempt the note; (b) never write "can now", "should be allowed", "now permitted", or "propose change/remove/relax" in rule/title/naya-note-opening unless the note genuinely proposes an authority change for Shawn; (c) advisory "should" + protected vocabulary = silent archive, always. Note the screen is on the note author's side of the problem: it cannot be fixed by restating the lesson elsewhere, because the screen runs on every intake. Only Shawn changes who-may-do-what; a note that restates his boundaries as prohibitions is restatement, not proposal — and the code agrees.

## ⚙️ MACHINE NOTE

{
  "sn_id": "SN-1013",
  "intelligent_block": "IB-SMART-NOTE-20261011-sn1013-authority-screen-drafting-discipline",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE",
  "sub": "LEARNING-PIPELINE/INGESTION-CHANNEL-DISCIPLINE",
  "evidence": [
    {"type": "code", "ref": "learn/learn_ingest.py authority_touch() lines 519-532", "finding": "scans rule_text + title + naya_note[:1000]; AUTHORITY_WORDS match + no AUTHORITY_CHANGE + no never/must-not/requires/needs -> flagged (fail closed)"},
    {"type": "code", "ref": "learn/learn_ingest.py lines 69-74", "finding": "AUTHORITY_WORDS = merge|deploy|ratif|production|authority|consent|privacy|security|destruct|self-modif; AUTHORITY_CHANGE = should be allowed|now permitted|no longer requires|can now|propose change/remove/relax"},
    {"type": "code", "ref": "learn/learn_ingest.py line 14", "finding": "Authority-touching notes are recorded + flagged, never integrated"},
    {"type": "pipeline_run", "ref": "learn/ingestion-log.md run 20261011T210815Z (2026-10-11T21:21:05Z)", "finding": "FLAGGED_AUTHORITY SN-1009 (naya note: 'scorecard and merge-consensus regexes should treat...' - advisory voice on merge vocabulary); INGESTED SN-1010 same run"},
    {"type": "receipt", "ref": "learn/receipts/SN-1009.json + learn/ledger.json", "finding": "SN-1009 recorded (section appended to learn/lessons.md) but authority_touch=true -> never integrated into brief-template.md"}
  ],
  "rule": "When a Smart Note touches protected-ground vocabulary (merge, deploy, ratify, production, authority, consent, privacy, security, destructive, self-modifying), phrase the boundary as a prohibitive restatement inside the scanned fields (rule, title, naya-note opening): 'never X without Y', 'must not', 'requires'. Advisory 'should' voice on the same vocabulary is fail-closed: recorded, never briefed. Never use 'can now', 'should be allowed', 'now permitted', or 'propose change/remove/relax' in scanned fields unless proposing an authority change for Shawn. Only Shawn changes who-may-do-what.",
  "relates_to": ["SN-1009 (fail-closed demonstration)", "SN-0145 (number uniqueness, adjacent intake discipline)", "SN-0151 (registry claim discipline)", "learn/learn_ingest.py immune gate (POISON-1/POISON-2 machine_view checks)"],
  "carrier": {"branch": "naya4/smart-notes-2026-09-30", "pr": "#1825", "merge": "NEVER", "ratification": "Shawn only"}
}
