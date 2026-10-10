# Verification Queue

Operational working state for admitted learning candidates. Worked, not watched.

- Admitted candidates enter via `tools/learning_verification_queue.py::enqueue`.
- SLA: verified within **48h of admission** or retired (`sweep_overdue`).
- Verifier must differ from both doer and scorer (`claim` enforces).
- Verdicts require a reason (`record_verdict` enforces).
- `queue.json` is an internal projection. The canonical learning store remains
  the Receiver/Supabase — this file is not a second source of truth.

Queue starts empty 2026-10-09: the 36-row backlog was triaged and retired
(see `../BACKLOG-TRIAGE-2026-10-09.md`); new candidates enter only through
the admission gate (`tools/learning_admission_gate.py`).
