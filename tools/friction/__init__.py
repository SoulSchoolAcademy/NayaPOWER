"""tools.friction — the missing third leg (SN-1855 Q3), code-first, dark.

balance.py   verified-balance + level projection over the ledger stream
             (consumes points-profile-v1 semantics; never re-derives them).
friction.py  automatic friction tiers T0..T3 driven by the verified
             balance; transitions emit ledger-shaped events.
watchers.py  product watchers v1: velocity, balance-dive, repeat-negative.
             Alerts are data, never side effects.
cli.py       JSONL in -> {actors, alerts, friction_events} JSON out,
             byte-identical for identical input.

Nothing here touches production: no database, no network, no writes
outside an explicit CLI output. Activation is a wiring step — WIRING.md.
"""

__all__ = ["balance", "friction", "watchers", "cli"]
