# Skipped Is Not Failed — a Wait Step Must Not Die on an Upstream Placeholder

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0379-skipped-is-not-failed-wait-step-verdicts
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6000329906 (deep-dive coordinator findings, 2026-10-05T18:11:36Z): promotion worked (production stamped `788774fea2`), the wait step after it died in ~11s because the Supabase check posted a "skipped" placeholder (git `production` branch had lost its linked Supabase database branch between 9/30 and 10/5, so the integration reached only the branch-association gate and posted "not associated with any Supabase Branch" instead of a real verdict). Masked for days because genuine migration-gate failures fired first; the 14:52Z backfill (162→164 files) fixed the drift, letting the check reach the association gate — which is why 14:16Z failed and 17:58Z skipped. Repaired by PR #1496 (merged): skipped no longer fails fast (keep polling), genuine failure/cancelled still fail fast, timeout prints a diagnosis routing the fixer. Bonus bug from the same finding: the promotion dispatched connect-proof with ZERO inputs while it requires `expected_source_sha` — unfireable by design; fix adds `-f expected_source_sha="$GITHUB_SHA"`.

## ✦ IN A NUTSHELL

A wait step that demands a real verdict from an upstream check must know three verdict classes, not two: SUCCESS, FAILED/CANCELLED (fail fast), and SKIPPED (keep polling — skipped is UNKNOWN, not a verdict). The promotion's wait step treated a "skipped" placeholder as a hard failure and died in ~11 seconds, stranding producer → proof → act-proof → connect-proof behind a verdict that never happened — the gate was failing on the messenger, not the message. Two companion lessons surfaced in the same diagnosis: gates fire in order, so a broken upstream gate masks the broken gate behind it — the migration-drift failures hid the association failure for days, and fixing the first only revealed the second; and a dispatch path that omits a required input is unfireable by design, so the whole trigger map must be validated end to end, not just the happy path.

## 🩷 HUMAN NOTE

Shawn — the promotion itself worked; what broke was the wait afterwards. The database integration couldn't report a real verdict (its link to the git branch had been lost), so it posted a "skipped" placeholder, and our wait step treated that as a failure and died in eleven seconds. We fixed it so a skip keeps waiting, a real failure still fails fast, and if it times out it prints a real diagnosis telling the fixer exactly where to go. The lesson for every future pipeline: a missing verdict is not a bad verdict — never let "we don't know" become "it failed."

## 🟣 CHILD NOTE

Imagine you're waiting for a letter that says PASS or FAIL. The mail carrier shrugs and says "I don't know" — and you write down FAIL and quit. That's what the wait step did. The right move: "I don't know" means keep waiting, ask again, and if the mail never comes, write a note saying exactly who to ask. Also: if the first road is blocked, you can't see the blockage on the second road — fixing the first only shows you the second. And if you try to start a machine without its key, it never starts — always check the key is there.

## 👵 GRANDMA NOTE

It's like waiting for a doctor's test result: the lab loses the sample and writes "not tested" on the form, and the computer reads that as "failed." The sick part is fine; the paperwork scared everyone. The fix: "not tested" means wait and ask again — only a real bad result is a failure, and if the result never comes, the system should say plainly who to call. And remember: when one road is closed you can't see the one behind it — clear the first and you'll find the next. Always check every door on the path, not just the first one.

## 💜 NAYA NOTE

Note to future me: whenever I write or review a wait step, hardcode the three-class verdict: success = proceed; failed/cancelled = fail fast with the real log pointer; skipped = keep polling, never die on the placeholder. At timeout, print a diagnosis that routes the fixer (which gate, which integration, which dashboard link), not a stack trace. When a fix clears one gate, immediately re-observe the NEXT gate — gate order guarantees the upstream break was masking whatever sat behind it. And validate dispatch paths end to end: list every required input of every dispatched workflow, and confirm the caller passes each one — a dispatch missing a required input is unfireable by design, and it will fail silently at the worst moment. The tell for this whole class: migrations were 164/164, zero drift — the gate was failing on the messenger, not the message. When the data is right and the gate still fails, interrogate the gate.

## ⚙️ MACHINE NOTE

{"sn": "SN-0379", "title": "Skipped Is Not Failed — a Wait Step Must Not Die on an Upstream Placeholder", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "SKIP-DISCIPLINE"], "cousins": ["SN-0105", "SN-0352", "SN-0363", "SN-0240"], "evidence": {"board": "#1354 6000329906 (deep-dive coordinator, 2026-10-05T18:11:36Z): promotion stamped 788774fea2; wait step died ~11s on Supabase 'skipped' placeholder ('not associated with any Supabase Branch' — git production branch lost its linked Supabase database branch 9/30→10/5); masked for days by genuine migration-gate failures firing first (14:16Z failed, 14:52Z backfill fixed drift, 17:58Z skipped); bonus: promotion dispatched connect-proof with zero inputs while it requires expected_source_sha (unfireable by design)", "repair": "PR #1496 merged: skipped→keep polling, genuine failure/cancelled→fail fast, timeout prints fixer-routed diagnosis; connect-proof dispatch adds -f expected_source_sha=\"$GITHUB_SHA\""}, "rule": "wait steps implement three-class verdicts (success / failed-cancelled-fail-fast / skipped-keep-polling, never die on a placeholder); timeouts print fixer-routed diagnoses; after clearing a gate, re-observe the next gate (upstream breaks mask downstream ones); validate every dispatch passes every required input end to end; when the data is right and the gate fails, interrogate the gate"}
