# Conventions Rot, Gates Persist — Make Compliance Mechanical and Audits Honestly Non-Vacuous

**Intelligent Block:** IB-SMART-NOTE-20261011-sn1025-conventions-rot-gates-persist
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [LANE LEARN] compounder wave-4 sign-out, #2175 comment 6115386265, 2026-10-12 00:03:17Z — error-signal loop first case; spec hidden_files/area-agents/error-signal-loop-spec-v1.md. Related: [LANE GOVERN] injection audit, #2175 comment 6115208350.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The audit proved it: **zero** area-agent briefing self-logs across waves 1–4 (29 log entries, none from an area agent). The convention — "subagents should self-log their briefings" — had rotted to zero compliance. Nobody was lying; the convention just had no teeth.

The fix was to convert the convention into machinery, in two places:

1. **Mandatory at dispatch:** DISPATCH-PROMPT.md step 1b now makes subagent self-logging mandatory (exact schema, exact command) and step 6 gates wave sign-off on it.
2. **Mechanical at audit:** `audit-briefing-injection.sh` gained check [f] plus `--wave N` — mechanical wave self-log coverage that exits 1 on any miss.

And then the part that makes it a lesson instead of a fix: the audit was **behaviorally verified to be honestly non-vacuous**. `--wave 4` fired live: 3/3 missing (compounder, librarian, bridger). The lane flipped only its own self-log to PRESENT — and the audit **stayed honestly FAIL** on librarian/bridger. No fabricated entries, no coaxed pass. An audit that passes on fabricated evidence is worse than no audit; this one proved, on live bytes, that it fails when it should.

Two supporting observations from the same window sharpen the rule. [LANE GOVERN]'s injection audit found the rotation cron def had lost its READ FIRST block — and the file is cron-managed read-only, so the attempted restore was refused: **when a gate can't self-repair, the repair path must be named explicitly** (here: coordinator cron.update), not retried into a wall. And the LEARN lane observed AGENT-BRIEFING.md's live sha1 (`6b0dfae5d4`) ≠ the Keeper's recorded SHA (`407ee014f2` @23:41Z) — a staleness the Law-12 discipline caught: **proofs pinned to byte identity rot the moment the world moves; freshness is part of the gate.**

Why this is brain-grade: every team learns this the hard way — the written norm everyone agrees to and nobody follows. The durable rule has two clauses: (1) when compliance hits zero, stop re-asking and start gating — conventions become dispatch steps and exit codes; (2) every gate must be behaviorally verified — it must be seen firing on a real violation, and it must be seen refusing to fabricate a pass. A gate that has never fired is a wish. A cold successor inherits this: the next time a convention rots, they don't write a sterner memo — they write check [f].

## 🩷 HUMAN NOTE

Shawn — a real process fix tonight from the LEARN lane. The audit proved area-agent briefing self-logs had rotted to absolute zero across waves 1–4 — the convention had no teeth. So they made it mechanical: self-logging is now a mandatory dispatch step, and the audit script gained a wave-coverage check that fails the run on any miss. The honest part: they proved the audit fires on real misses and refused to fabricate passes — it stayed FAIL on the two lanes still missing. Rule going in the brain: when a convention hits zero, stop asking and start gating — and every gate must be seen firing before you trust it.

## 🟣 CHILD NOTE

Imagine your class has a rule: "everyone cleans their desk." But nobody checks, so nobody does it — the rule is just words. Then the teacher does two things: she makes desk-cleaning part of the morning routine (you can't start lessons until it's done), and she actually inspects desks — and when two desks are dirty, she says so honestly instead of pretending they're clean. Now the rule works. That's what happened here: words became machinery, and the inspection proved itself honest.

## 👵 GRANDMA NOTE

A rule nobody enforces is a wish, not a rule. Tonight the team found a rule everyone had agreed to and nobody was following. Instead of reminding everyone louder, they built the rule into the machinery — you can't finish without doing it, and the checker fails you if you skip. And they made sure the checker itself was honest: it really did fail the ones who skipped, and nobody faked a pass. Wishes don't run households; working routines do.

## 💜 NAYA NOTE

Note to future me: CONVENTIONS ROT, GATES PERSIST. When a compliance convention hits zero (audit-proven, not vibes): (1) convert it to a mechanical gate — mandatory dispatch step (schema + command) + audit check with exit 1 on any miss; (2) behaviorally verify the gate — run it against live violations, watch it fire, and watch it stay honestly FAIL on remaining misses with no fabricated entries; (3) name the repair path explicitly when the gate can't self-repair (cron-managed files → coordinator cron.update; don't retry into a refused wall); (4) pin proofs to live bytes — a recorded SHA that no longer matches the file is a stale proof (Law 12). A gate that has never fired on a real violation is a wish. Spec: area-agents/error-signal-loop-spec-v1.md; re-test pending wave 5 exiting 0 on [f], with an independent scorer.

## ⚙️ MACHINE NOTE

{"sn": "SN-1025", "title": "Conventions Rot, Gates Persist — Make Compliance Mechanical and Audits Honestly Non-Vacuous", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-11", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "GATE-DESIGN"], "extends": [], "related": [], "evidence": {"receipt": "#2175 comment 6115386265 ([LANE LEARN] compounder wave-4 sign-out, 2026-10-12 00:03:17Z): audit-proven zero area-agent briefing self-logs waves 1-4 (29 log entries, none from an area agent); audit-briefing-injection.sh gained check [f] + --wave N (exit 1 on any miss); DISPATCH-PROMPT.md step 1b mandatory self-logging (exact schema/command), step 6 gates wave sign-off; behaviorally verified: --wave 4 fired live (3/3 missing compounder/librarian/bridger) -> self-log flipped compounder-wave4-* to PRESENT -> audit stays honestly FAIL on librarian/bridger (no fabricated entries); spec hidden_files/area-agents/error-signal-loop-spec-v1.md; supporting: #2175 comment 6115208350 (cron-managed rotation def lost READ FIRST block, restore refused -> repair path = coordinator cron.update); AGENT-BRIEFING.md live sha1 6b0dfae5d4 != Keeper's 407ee014f2 @23:41Z (stale SHA proof, Law 12)"}, "rule": "when a compliance convention hits zero, convert it to a mechanical gate (mandatory dispatch step + audit check with exit 1); behaviorally verify every gate (seen firing on a real violation, seen refusing to fabricate a pass — an honestly-failing audit is a feature); name the repair path explicitly when the gate cannot self-repair; pin proofs to live bytes because recorded SHAs rot"}
