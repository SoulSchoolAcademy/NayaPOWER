#!/usr/bin/env python3
"""
The Intake Bridge — B1 of the auto-match completion plan (2026-10-25).

The missing consumer: public.intake_events (migration 20261022213000) is
where the live intake writes, and welcome_engine.build_vector() is where
answers become matcher vectors — and until this module, nothing connected
them. The bridge folds the event stream per citizen and produces
engine-ready vectors through the EXISTING build_vector() path. It invents
no second matcher and no second phrase extractor.

THE KEY TRUTH (proven by test_intake_bridge.py against the live files):
the live JS walk (HUB/app/js/naya-intake.js) and the Python spine
(welcome_engine.SLOTS) share ZERO answer keys. The JS door walk asks
name / email / intent / note; SLOTS expects the 14 Questions-V2 keys
(into, matters, ...). Key equality was assumed for a day and is false, so
this bridge carries the divergence explicitly instead of dropping data:

  * KEY_TRANSLATION — door keys that DO carry match signal, translated to
    the SLOTS key whose question they answer:
        note   -> into           (the free-text "remember this about me"
                                  is the only declared-interest text the
                                  door collects; it lands in topics)
        intent -> goal_personal  (the declared choice — learn / build /
                                  community / team — carried VERBATIM as
                                  the goal answer; no wording invented)
  * KEY_CLASSIFICATION — door keys that are knowingly NOT vector answers:
        name / display_name        identity (never a match signal)
        email / invitee_email_hash contact (hash-only canon: "never email")
        flow / owner_alias         row metadata, not answers
  * SLOTS keys pass through untranslated — a Questions-V2 walk writing
    into the same table needs no translation at all.
  * ANY other key is reported in diagnostics["unmapped_keys"]. Nothing is
    ever dropped silently.

FOLD RULES (the event stream is append-only; answers ride ONLY the
'finished' event today, as the joinRecord summary — see naya-intake.js
finish()/joinRecord()):
  * Rows fold per owner_alias, in created_at order (input order breaks
    ties; a missing timestamp folds first). Latest answer per question
    wins — a re-walk updates the citizen, it does not duplicate them.
  * Only flow='welcome' rows fold. In 'invite_accept' the row's
    owner_alias is the INVITER (the invite-flip lookup in naya-intake.js
    keys on it) while the answers describe the invitee, who is identified
    only by email hash — folding them would corrupt the inviter's vector
    with another person's answers. Those rows are counted, not folded.
  * Malformed rows (non-dict row, missing/blank owner_alias, non-dict
    answers, non-string answer values) degrade to diagnostics, never a
    crash — the engine's own contract, kept.
  * A citizen whose folded answers yield an all-empty vector is skipped
    and counted (citizens_skipped_no_signal), never emitted as a
    zero-vector that would sit in the corpus matching nothing.
  * Output is keyed by alias ONLY. No email, hash, or display name ever
    enters a vector (privacy law: matching runs on aliases and declared
    public signals).

ATTRIBUTION NOTE: rows are keyed by the recorded owner_alias exactly as
the table's own owner index (intake_events_owner_time_idx) keys them. In
the first-citizens pattern the walk runs under the answering citizen's
own alias; if a door surface ever mounts the walk under a referrer's
alias, that is a writer-side semantics question (N1, Nitro's sign-off),
and this bridge's per-flow diagnostics are where it will be visible.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from welcome_engine import SLOTS, build_vector  # the one spine, reused verbatim
from smart_match import FIELDS  # the one matcher's five fields

# Door answer/step key -> SLOTS answer key (see header for the why).
KEY_TRANSLATION = {
    "note": "into",
    "intent": "goal_personal",
}

# Door key -> why it is knowingly not a vector answer.
KEY_CLASSIFICATION = {
    "name": "identity",
    "display_name": "identity",
    "email": "contact",
    "invitee_email_hash": "contact",
    "flow": "metadata",
    "owner_alias": "metadata",
}

# Flows whose rows may be folded into the row-owner's own answers.
ATTRIBUTABLE_FLOWS = ("welcome",)


def _new_diag():
    return {"rows_seen": 0, "rows_malformed": 0, "rows_no_alias": 0,
            "rows_excluded_flow": 0, "rows_without_answers": 0,
            "answers_folded": 0, "malformed_values": 0,
            "citizens_seen": 0, "citizens_with_vectors": 0,
            "citizens_skipped_no_signal": 0,
            "_translated": set(), "_classified": {}, "_unmapped": set()}


def _public_diag(diag):
    out = {k: v for k, v in diag.items() if not k.startswith("_")}
    out["translated_keys"] = sorted(diag["_translated"])
    out["classified_keys"] = dict(sorted(diag["_classified"].items()))
    out["unmapped_keys"] = sorted(diag["_unmapped"])
    return out


def translate_answers(raw, diag):
    """One answers dict (as recorded in intake_events.answers) -> a
    SLOTS-keyed answers dict. Every key is accounted for: passed through,
    translated, classified, or named in unmapped_keys. Never raises."""
    out = {}
    if not isinstance(raw, dict):
        return out
    for key, value in raw.items():
        if key in SLOTS:
            target = key
        elif key in KEY_TRANSLATION:
            target = KEY_TRANSLATION[key]
            diag["_translated"].add(key)
        elif key in KEY_CLASSIFICATION:
            diag["_classified"][key] = KEY_CLASSIFICATION[key]
            continue
        else:
            diag["_unmapped"].add(key)
            continue
        if isinstance(value, str):
            out[target] = value
        elif target == "links" and isinstance(value, list):
            out[target] = value  # links rides as a list in the answers shape
        else:
            diag["malformed_values"] += 1
    return out


def _sort_key(item):
    idx, row = item
    ts = row.get("created_at") if isinstance(row, dict) else None
    return (str(ts) if ts is not None else "", idx)


def fold_answers(rows):
    """Fold an intake_events row stream -> ({alias: SLOTS answers}, diagnostics).
    `rows` is a list of row dicts in the migration's shape (a single dict
    is accepted as a one-row stream). Deterministic for a given input."""
    if isinstance(rows, dict):
        rows = [rows]
    diag = _new_diag()
    per_alias = {}
    for _, row in sorted(enumerate(rows or []), key=_sort_key):
        diag["rows_seen"] += 1
        if not isinstance(row, dict):
            diag["rows_malformed"] += 1
            continue
        alias = row.get("owner_alias")
        if not isinstance(alias, str) or not alias.strip():
            diag["rows_no_alias"] += 1
            continue
        flow = row.get("flow")
        if flow is not None and flow not in ATTRIBUTABLE_FLOWS:
            diag["rows_excluded_flow"] += 1
            continue
        raw = row.get("answers")
        if raw is None:
            diag["rows_without_answers"] += 1
            continue
        if not isinstance(raw, dict):
            diag["rows_malformed"] += 1
            continue
        folded = translate_answers(raw, diag)
        if folded:
            per_alias.setdefault(alias, {}).update(folded)  # latest wins per key
            diag["answers_folded"] += len(folded)
    diag["citizens_seen"] = len(per_alias)
    return per_alias, diag


def vectors_from_intake(rows):
    """intake_events rows -> ({alias: engine vector}, diagnostics).
    Vectors come from welcome_engine.build_vector() and nothing else;
    citizens with no usable signal are skipped and counted."""
    per_alias, diag = fold_answers(rows)
    vectors = {}
    for alias, answers in per_alias.items():
        vec = build_vector(answers)
        if any(vec[f] for f in FIELDS):
            vectors[alias] = vec
        else:
            diag["citizens_skipped_no_signal"] += 1
    diag["citizens_with_vectors"] = len(vectors)
    return vectors, _public_diag(diag)


if __name__ == "__main__":
    # Usage: python3 intake_bridge.py rows.json  — rows.json is a JSON list
    # of intake_events rows; prints {"vectors": ..., "diagnostics": ...}.
    with open(sys.argv[1]) as fh:
        rows_in = json.load(fh)
    vecs, d = vectors_from_intake(rows_in)
    print(json.dumps({"vectors": vecs, "diagnostics": d}, indent=1, sort_keys=True))
