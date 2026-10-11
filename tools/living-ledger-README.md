# Living Ledger — UD-18 "Nothing consequential happens untracked" (D51)

The capstone. The master record above the sibling ledgers (belief,
baseline, work-honesty, exactly-once): every consequential decision,
action, evidence item, and outcome is appended as a chained,
tamper-evident receipt. Nothing consequential happens untracked.

## The law, in one paragraph

Append-only — there is no mutation API, history can only grow. Every
receipt hash-chains to the previous one (sha256 over a canonical
encoding); any edit anywhere breaks the chain at an exactly named
sequence number. DECISION and ACTION receipts must link evidence —
an unlinked decision is refused, not recorded. Internal links must
reference entries that exist. Timestamps are monotonic. Sibling ledgers
feed the master through `anchor_summary()`: they submit a summary plus
its hash, and the hash is recomputed before acceptance.

## Usage

```python
from living_ledger import LivingLedger

ledger = LivingLedger()

d = ledger.emit(actor="naya-4", kind="DECISION", action="merge fix #2255",
                evidence_refs=("scorecard:8.1", "gate:green"),
                scope="NayaPOWER", content={"pr": 2255})
a = ledger.emit(actor="naya-4", kind="ACTION", action="merged",
                evidence_refs=("merge-commit:ba96a81",), links=(d.entry_hash,))
ledger.emit(actor="naya-2", kind="OUTCOME", action="verified +3",
            evidence_refs=("verify:36/36",), links=(a.entry_hash,))

ok, break_seq, detail = ledger.verify_chain()   # (True, None, "3 entries verified")
ledger.by_actor("naya-4")                        # query surface
ledger.causal_chain(a.seq)                       # decision -> action -> outcome

# Sibling-ledger feed: the sibling seals its summary, the master verifies.
payload = LivingLedger.seal_payload({"ledger": "work-honesty",
                                     "head_seq": 42, "head_hash": "abc123"})
ledger.anchor_summary(ledger_name="work-honesty", payload=payload)

ledger.save("ledger.jsonl")                      # append-only file
ledger2 = LivingLedger.load("ledger.jsonl")      # verifies on load; raises on break
ledger.render_surface("ledger.html")             # the living surface: every
                                                 # receipt + evidence, live
```

## Refusal codes

| code | meaning |
|---|---|
| `UNLINKED_DECISION` | DECISION/ACTION without `evidence_refs` — refused, never recorded |
| `BACKDATED_ENTRY` | timestamp older than head — refused |
| `UNKNOWN_LINK` | link to a nonexistent entry hash — refused |
| `ANCHOR_HASH_MISMATCH` | sibling summary hash doesn't recompute — refused |
| `ANCHOR_MALFORMED` | anchor payload missing `payload_hash` — refused |
| `DUPLICATE_SEQUENCE` | seq appears twice in a file — refused on load |
| `CHAIN_BREAK` | chain fails verification on load — refused, never silently accepted |
| `EMPTY_ACTOR` / `UNKNOWN_KIND` | malformed receipt — refused |

## Acceptance gate (UD-18)

PASS requires: every consequential action emits a chained receipt;
any seat can verify any receipt live (`verify_chain` /
`verify_receipt` / the rendered surface); nothing consequential is
untracked (DECISION/ACTION without evidence is refused at the door).
One failure = FAIL. The suite in `test_living_ledger.py` encodes each:
16/16 green, including a tampered entry detected at its exact sequence
number and a forged sibling anchor refused.

## What this does NOT claim

- It proves tamper-evidence and queryability of what IS recorded. It
  does not prove every code path in the system calls `emit()` — wiring
  the emitter into every consequential path is the integration job that
  follows, and until then "nothing untracked" is enforced at this
  module's door, not across the whole machine.
- A receipt proves a chained record exists with the stated content. It
  does not prove the content is true — truth is the sibling ledgers'
  job (UD-02/UD-06), and the anchor feed verifies hashes, not claims.
- The living surface is regenerated from the ledger; "live" means
  current at render time, not a push channel.
