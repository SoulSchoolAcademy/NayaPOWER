"""Live-row reader for the canonical learning-lineage receipt (convergence B).

The receipt (tools/learning_lineage_receipt.py) is the judge: "A reader
assembles the bundle; this module reconstructs and judges." Until now that
reader existed only as hand-built test fixtures -- every reconstruct()
proof ran on synthetic bundles shaped like the production writer emits.
This module is the missing READER side: it maps REAL persisted rows
(Supabase public tables, as the sb-api skill returns them) into the exact
bundle contract reconstruct() consumes.

Role -> source table -> bundle key (normalization is the whole job):
  learning           learning_evidence            learning            pass-through
  cognition_event    nayanet_cognition_events     cognition_event     {id, event_id}
  commit_receipt     nayanet_execution_receipts   commit_receipt      {id, action}
  intelligent_block  nayanet_intelligent_blocks   intelligent_block   {intelligent_block_id,
                                                                     understanding_state,
                                                                     evidence_refs, provenance}
  relationship       nayanet_brain_relationships  relationship        {relationship_id}
  checkpoint         nayanet_checkpoint_receipts  checkpoint          {id: checkpoint_id}  (*)
  verification       (caller-supplied)            verification        {cvo_id, method}
  authority_ref_links (caller-supplied)           authority_ref_links [str, ...]
  retrieval_receipts / application_receipts /
    outcome_records  (convergence-D emitter)      same keys           pass-through lists

(*) the one true rename: the checkpoint table's primary key is
`checkpoint_id`, but the receipt resolves bundle["checkpoint"]["id"].
Mapping it here -- not in the receipt -- keeps the receipt's contract
stable and puts the schema seam in exactly one place.

Fail-closed contract (never fabricate, never raise):
  - a missing row -> the bundle key is OMITTED and an assembly note names
    it; reconstruct() then reports the honest GAP (e.g. a learning whose
    observed_value names a checkpoint_id with no checkpoint row attached
    reconstructs BROKEN / CHECKPOINT_LINK_BROKEN, not PRESENT).
    ("verification" is caller-supplied and optional by design -- the
    receipt falls back to block evidence_refs -- so its absence is the
    normal path and is never noted.)
  - a malformed row (not a dict, or missing its key field) -> treated as
    absent + note. The reader never invents a row to satisfy the receipt.
  - rows itself malformed -> bundle carries assembly_notes only;
    reconstruct() answers BROKEN / BUNDLE_MISSING_LEARNING.
  - extra keys in rows are ignored; D receipts pass through untouched
    (the receipt verifies their digests and linkages, not this module).

Pure functions only: no DB, no network, no credentials. The caller fetches
rows (read-only) and hands them in; this module maps and judges nothing.

Live shapes verified read-only 2026-10-09 against production:
143 learning_evidence rows, 112 carrying the full observed_value link set
(lineage_id, relationship_id, checkpoint_id, commit_receipt_id,
intelligent_block_id, source_event_id, source_event_key, index_id).
Exemplar learning 37dfeec3-f120-42e0-a971-5aee95f0b537 (ACTIVE /
E1_UNDERSTANDS): every hop resolves -- event, intelligence_commit
receipt, LEARNED block, PRODUCES relationship, checkpoint row, lineage
row, causal_verification_id in block evidence_refs -- and reconstructs
PARTIAL with zero gaps (7 stages uninstrumented: retrieval..outcome and
reuse..successor have no emitters yet). That is the honest live boundary
this reader makes machine-checkable.
"""

from __future__ import annotations

from typing import Any

SCHEMA = "NAYANET_LEARNING_LINEAGE_BUNDLE_ASSEMBLY_V1"

# rows-key -> (bundle-key, source table, kind of mapping)
_ROLE_MAP: tuple[tuple[str, str, str], ...] = (
    ("learning", "learning", "learning_evidence"),
    ("cognition_event", "cognition_event", "nayanet_cognition_events"),
    ("commit_receipt", "commit_receipt", "nayanet_execution_receipts"),
    ("intelligent_block", "intelligent_block", "nayanet_intelligent_blocks"),
    ("relationship", "relationship", "nayanet_brain_relationships"),
    ("checkpoint", "checkpoint", "nayanet_checkpoint_receipts"),
    ("verification", "verification", "caller-supplied"),
)

# bundle-key -> fields the receipt actually reads, mapped from raw columns.
# A field listed as (bundle_field, raw_column) is renamed; a bare string
# is passed through under the same name.
_FIELD_MAP: dict[str, tuple] = {
    "cognition_event": ("id", "event_id"),
    "commit_receipt": ("id", "action"),
    "intelligent_block": ("intelligent_block_id", "understanding_state",
                           "evidence_refs", "provenance"),
    "relationship": ("relationship_id",),
    "checkpoint": (("id", "checkpoint_id"),),
    "verification": ("cvo_id", "method"),
}

# D-shaped receipt bundle keys: passed through untouched (the receipt
# verifies digests + linkages). Present here so the reader contract is
# complete in one place.
_D_BUNDLE_KEYS = ("retrieval_receipts", "application_receipts", "outcome_records")


def _note(notes: list[str], text: str) -> None:
    notes.append(text)


def _map_row(bundle_key: str, row: Any, notes: list[str]) -> dict[str, Any] | None:
    """Normalize one raw row to the bundle shape the receipt consumes."""
    if not isinstance(row, dict):
        _note(notes, "ROW_MALFORMED: %s expected object, got %s"
              % (bundle_key, type(row).__name__))
        return None
    out: dict[str, Any] = {}
    for spec in _FIELD_MAP[bundle_key]:
        if isinstance(spec, tuple):
            bfield, rfield = spec
        else:
            bfield = rfield = spec
        if rfield not in row:
            _note(notes, "ROW_FIELD_MISSING: %s.%s absent from source row"
                  % (bundle_key, rfield))
            return None
        out[bfield] = row[rfield]
    return out


def assemble_bundle(rows: Any) -> dict[str, Any]:
    """Assemble the lineage-receipt bundle from real persisted rows.

    rows: dict keyed by role (see _ROLE_MAP) plus optionally
    "authority_ref_links" and the three D receipt keys. Returns the bundle
    dict for learning_lineage_receipt.reconstruct(), carrying
    "assembly_notes" (list[str]) and "assembly_schema". Never raises;
    never fabricates a row.
    """
    notes: list[str] = []
    bundle: dict[str, Any] = {
        "assembly_schema": SCHEMA,
        "assembly_notes": notes,
    }

    if not isinstance(rows, dict):
        _note(notes, "ROWS_NOT_OBJECT: expected dict keyed by role, got %s"
              % type(rows).__name__)
        return bundle

    learning = rows.get("learning")
    if not isinstance(learning, dict):
        _note(notes, "LEARNING_ROW_MISSING: bundle has no learning to reconstruct")
        return bundle
    if not isinstance(learning.get("observed_value"), dict):
        _note(notes, "LEARNING_OBSERVED_VALUE_MISSING: learning %r carries no observed_value object"
              % (learning.get("id"),))
    bundle["learning"] = learning

    for rows_key, bundle_key, _table in _ROLE_MAP[1:]:
        if rows_key not in rows or rows.get(rows_key) is None:
            # "verification" is caller-supplied and optional by design --
            # the receipt falls back to block evidence_refs -- so its
            # absence is the normal path, not a gap worth noting. The five
            # table rows are expected whenever the learning names them.
            if rows_key != "verification":
                _note(notes, "ROW_ABSENT: no %s row attached" % rows_key)
            continue
        if rows_key == "verification":
            mapped = _map_row(bundle_key, rows[rows_key], notes)
            if mapped is None:
                continue
            if not mapped.get("cvo_id"):
                _note(notes, "VERIFICATION_ROW_EMPTY: no cvo_id; falling back to block evidence_refs")
                continue
            bundle[bundle_key] = mapped
            continue
        mapped = _map_row(bundle_key, rows[rows_key], notes)
        if mapped is not None:
            bundle[bundle_key] = mapped

    links = rows.get("authority_ref_links")
    if links is not None:
        if isinstance(links, list) and all(isinstance(x, str) for x in links):
            bundle["authority_ref_links"] = list(links)
        else:
            _note(notes, "AUTHORITY_REFS_MALFORMED: expected list[str]; dropped, not repaired")

    for key in _D_BUNDLE_KEYS:
        val = rows.get(key)
        if val is None:
            continue
        if isinstance(val, list):
            bundle[key] = val
        else:
            _note(notes, "D_KEY_NOT_LIST: %s must be a list; dropped" % key)

    return bundle


def summarize_assembly(bundle: dict[str, Any]) -> str:
    """One-line human summary of what the reader assembled."""
    notes = bundle.get("assembly_notes") or []
    keys = sorted(k for k in bundle
                  if k not in ("assembly_schema", "assembly_notes"))
    learning = bundle.get("learning") or {}
    return ("bundle for learning %s | keys: %s | %d assembly note(s)%s"
            % (learning.get("id"), ",".join(keys) or "(none)", len(notes),
               (": " + "; ".join(notes[:3])) if notes else ""))
