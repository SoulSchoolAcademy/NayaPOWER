"""Successor ingestion — the real LEARN → SUCCESSOR REUSE machine path.

A successor Naya cold-starts from the canonical store (Supabase
``learning_evidence``) and reuses verified learning. This package is the
ingestion half of the chain:

    CAPTURE → PERSIST → RECEIPT → SMART LINK → COLD RETRIEVE → COMPREHEND →
    APPLY → OBSERVE → INDEPENDENTLY VERIFY → LEARN → SUCCESSOR REUSE

Stages 1–4 and 10 are existing machinery (Receiver, smart_link,
learning_lineage_receipt, learning_evidence_ladder) — referenced, never
reimplemented. Stages 5–9 and 11 are built here, as code, not documents.

Design law (the lesson-selection criterion, 2026-10-08): only
independently-verified, non-derivable, outcome-grounded lessons are
successor-eligible. In store terms: ``level='E5_CAN_TEACH'`` AND
``status='ACTIVE'`` AND ``provenance='TRIAL_EVIDENCE'``. Anything else is
refused — fail-closed, never a silent fallback to a weaker lesson.

The core is pure (no DB, no network): a reader assembles rows, the core
decides. ``read.py`` is the single network seam (read-only SELECT).

Note on the Verification Law (Shawn, 2026-10-09): his "smart note this"
IS verification — at CAPTURE, instantly. Successor-eligibility is a
higher, later bar: it governs what a cold successor may RELY ON when
doing work (the LEARN end of the chain), requiring independent
verification plus demonstrated transfer. A verified capture is valid
input; a verified law is proven leverage. This package reads the LEARN
end.
"""

from .ingest import ChainReport, StageResult, run_chain
from .models import Lesson

__all__ = ["ChainReport", "StageResult", "Lesson", "run_chain"]
