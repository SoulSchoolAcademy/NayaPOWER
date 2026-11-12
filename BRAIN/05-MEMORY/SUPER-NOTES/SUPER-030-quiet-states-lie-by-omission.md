# SUPER NOTE — Quiet States Lie by Omission

> **The essence layer: 71 distilled Super Notes.** Raw Smart Notes live in the archive; the Hub wall shows these essences. Nothing here deletes or replaces any raw note.

| Field | Value |
|---|---|
| Super Note ID | `SUPER-030` |
| Hub wall row | `public.hub_smart_notes` ib_id `SUPER-030` |
| Human title | Quiet States Lie by Omission |
| Layer | ESSENCE — distilled from raw Smart Notes, never a raw capture |
| Distilled | 2026-10-21 — corrective distillation drive (639 raw → 71 essences); REPAIRED 2026-10-21 after independent audit found 42 MISSING + 151 PARTIAL — lost lessons restored from the originals (see REPAIR-LOG); coverage map regenerated mechanically from these files |
| Sources | 9 raw notes (full list below) |
| Cluster file | `cluster-03-super.json` |
| Canonical machine object | Hub DB row `public.hub_smart_notes` + `distill/all-super-notes.json` |
| Human projection | This Markdown file |
| Sync note | NOT ingested by hub-sync (its watcher parses only `BRAIN/05-MEMORY/SMART-NOTES`); archive + queue untouched |

---

## ✦ IN A NUTSHELL

The most dangerous failures make no noise. A step that was skipped, a job that never ran, a file that is just an empty shell — nothing turns red, yet nothing actually happened.

---

## 🩷 HUMAN NOTE

A badge can say success while the work inside was skipped — and a skipped step that was supposed to produce something poisons everything downstream waiting for its output. Some pushes never trigger the checking machinery at all, so 'no failures reported' can mean 'never examined'; when the road is blind that way, local verification becomes the gate. A failed dispatch is not a failed action — read which step moved and which did not. Passing over a failure with 'skip it' is a verdict earned one failure at a time, never as a blanket. And a file sitting at the right path proves nothing about its contents: hash the bytes.

---

## 🟣 CHILD NOTE

If nobody checked, 'no problem found' does not mean 'no problem.' An empty box with a pretty label is still empty. Look inside.

---

## 👵 GRANDMA NOTE

Silence from the kitchen does not mean dinner is cooking — sometimes the stove was never lit. Before you sit down to eat, peek in the pot. Quiet is not the same as done.

---

## 🤖 NAYA NOTE

Naya reads job tables, not badges, and audits what was skipped behind every red and every green. She treats a skip on an artifact-producing job as a chain failure, scopes every claim about what triggers checks by the actual event, falls back to local verification when the push path cannot trigger CI, and earns each skip with an individual reason. She verifies content by hash, never by path presence.

---

## WHAT IT MEANS

Systems report what they did far more loudly than what they did not do. The discipline of reading absences — skipped, untriggered, empty, unexamined — is what separates a monitored system from a merely decorated one.

---

## WHAT'S IN IT FOR YOU

No silent gaps in what you depend on. When something claims to have run, it ran; when it did not, you find out from the check, not from the consequences.

---

## HOW IT APPLIES

For every green: open the job table and list the skips. For every chain: confirm each producer actually produced. For every 'no CI failures': confirm CI was triggered at all. For every skipped failure: record its individual reason. For every critical file: verify the hash, not the path.

---

## ⟲ RESTORED BY REPAIR — 2026-10-21

> Restored by the distillation repair after the independent essence audit (distillation-audit-20261021) found the lessons below MISSING from, or only partially carried by, this Super Note. Each entry restores the named source note's own rule in checkable words, traced to that source. Nothing here is new doctrine.

### SN-0379 — Skipped Is Not Failed — a Wait Step Must Not Die on an Upstream Placeholder [audit: PARTIAL → lost element restored]

The lost wait-step lesson: a wait/poll step must use three verdict classes — SUCCESS; FAILED/CANCELLED, fail fast; and SKIPPED = UNKNOWN, keep polling — and must never die on a skipped upstream placeholder. Skipped is UNKNOWN, not a verdict. In the source case the promotion's wait step treated a "skipped" placeholder as a hard failure and died in ~11 seconds, stranding producer → proof → act-proof → connect-proof behind a verdict that never happened.

### SN-074 — "API Pushes Never Trigger Actions" Was an Event-Scoping Overgeneralization — Scope CI-Trigger Claims by Workflow Event (SN-048 Correction) [audit: PARTIAL → lost element restored]

The corrected fact itself: API / Data-API pushes do fire `pull_request`-event workflows, while `push`-event workflows stay silent on the same push. Live evidence: GitHub Actions ran on the API-pushed v3 head `2a7851a8` of PR #1243 — `test` = SUCCESS and Collective Chain Readiness Gate = SUCCESS, fired ~3 minutes post-push — and the event was `pull_request`, not `push`. So SN-048's absolute ("API-pushed commits never trigger GitHub Actions") is downgraded to a conditional scoped by workflow event type, and SN-051's local-verification-as-gate remains the remedy only where the needed evidence channel — the `push` event — is blind.

---

## SOURCES (traceability — every raw note this essence was distilled from)

- `IB-SMART-NOTE-20261005-sn0379-skipped-is-not-failed-wait-step-verdicts`
- `IB-SMART-NOTE-20261005-sn0418-skipped-producer-poisons-artifact-chain`
- `IB-SMART-NOTE-20260930-sn048-api-push-actions-silence`
- `IB-SMART-NOTE-20260930-sn074-api-push-trigger-event-scoping`
- `IB-SMART-NOTE-20260930-sn051-local-verification-as-gate`
- `IB-SMART-NOTE-20260930-sn044-red-run-triage`
- `IB-SMART-NOTE-20260930-sn0105-skip-with-reason-is-not-a-defect-blanket`
- `IB-SMART-NOTE-20261004-sn0278-path-presence-not-content`
- `IB-SMART-NOTE-20260930-sn0552-fail-first-topology-conceals-secondary-reds`
