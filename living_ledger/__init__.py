"""D51 — The Living Ledger / Smart Net (first machine slice).

Canonical D51 receipt envelope (`receipt.LivingReceipt`) plus the hash-chain
verifier (`chain.verify_chain`) for the shared chained ledger.

The ledger itself lives in the database (`nayanet_smart_ledger`, Supabase):
this package feeds that ledger and verifies its chain — it does not replace it.
No function here performs database reads or writes.
"""
from __future__ import annotations

from living_ledger.receipt import LivingReceipt, SCOPE_TO_PRIVACY, SCOPES
from living_ledger.chain import (
    ChainVerdict,
    canonical_event_hash,
    normalize_postgres_event,
    verify_chain,
)

__all__ = [
    "LivingReceipt",
    "SCOPE_TO_PRIVACY",
    "SCOPES",
    "ChainVerdict",
    "canonical_event_hash",
    "normalize_postgres_event",
    "verify_chain",
]
