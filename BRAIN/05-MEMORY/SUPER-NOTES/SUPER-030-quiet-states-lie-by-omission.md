# SUPER NOTE — Quiet States Lie by Omission

> **The essence layer: 71 distilled Super Notes.** Raw Smart Notes live in the archive; the Hub wall shows these essences. Nothing here deletes or replaces any raw note.

| Field | Value |
|---|---|
| Super Note ID | `SUPER-030` |
| Hub wall row | `public.hub_smart_notes` ib_id `SUPER-030` |
| Human title | Quiet States Lie by Omission |
| Layer | ESSENCE — distilled from raw Smart Notes, never a raw capture |
| Distilled | 2026-10-21 — corrective distillation drive (639 raw → 71 essences, exact partition, 639/639 covered) |
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
