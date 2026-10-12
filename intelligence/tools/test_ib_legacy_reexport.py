#!/usr/bin/env python3
"""Legacy-row re-export heal tests (t982, lane 4).

t922 closed the #2386 round-trip gap for modern rows: the exporter emits
rich detail verbatim inside provenance. Legacy rows (persisted before #2386,
no evidence_detail / applicability_detail / file_status_history keys) still
import via the documented ref/empty fallbacks — by design.

The hole this heals: on re-export, the fallback-reconstructed detail
({"kind": "ref", "note": ""} entries) was stamped into provenance
INDISTINGUISHABLE from authored rich detail. A consumer reading
evidence_detail could not tell fabricated-from-fallback detail from the
author's own words, and the first import->export->import cycle was not a
stable fixpoint.

The heal: the exporter marks fallback-derived detail honestly with
provenance["detail_source"] = "legacy-fallback". The marker means: "the
emitted rich-detail keys were populated from ref-only fallback content, not
from authored rich detail." Modern rows get no marker (the t922 byte-exact
contract is untouched); a marker already present is carried verbatim.

Corpus: the 20 canonical seed blocks, exported then stripped of the detail
keys — exactly the shape of a pre-#2386 persisted row.
"""
import copy
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ib_reconcile import (
    DETAIL_KEYS,
    from_persisted_row,
    normalize_file_block,
    to_persisted_row,
)
import seed_blocks


def make_legacy_row(seed):
    """A pre-#2386 row: modern export with the rich-detail keys stripped."""
    bid, raw = seed
    b = normalize_file_block(copy.deepcopy(raw),
                             default_owner_id="",
                             default_owner_scope="TEAM")
    b["owner_id"] = "NAYA"  # canonical system owner (Shawn's word 2026-10-11)
    modern = to_persisted_row(b)
    legacy = json.loads(json.dumps(modern))
    for k in DETAIL_KEYS:
        assert k in legacy["provenance"], f"seed {bid} export missing {k}"
        del legacy["provenance"][k]
    return bid, legacy


LEGACY_ROWS = [make_legacy_row(s) for s in seed_blocks.SEED]


def j(x):
    return json.dumps(x, sort_keys=True)


class TestLegacyReexportHeal(unittest.TestCase):
    def test_corpus_is_twenty_legacy_rows(self):
        self.assertEqual(len(LEGACY_ROWS), 20)
        for bid, legacy in LEGACY_ROWS:
            for k in DETAIL_KEYS:
                self.assertNotIn(k, legacy["provenance"], bid)

    def test_reexport_carries_rich_detail_keys(self):
        # The healed re-export populates the rich-detail keys (byte-compare
        # target of the brief: legacy rows re-export WITH rich detail).
        for bid, legacy in LEGACY_ROWS:
            healed = to_persisted_row(from_persisted_row(legacy))
            for k in DETAIL_KEYS:
                self.assertIn(k, healed["provenance"], f"{bid}: {k}")

    def test_reexport_marks_fallback_detail_honestly(self):
        # THE heal: fallback-derived detail is labeled, never masquerading
        # as authored rich detail.
        for bid, legacy in LEGACY_ROWS:
            healed = to_persisted_row(from_persisted_row(legacy))
            self.assertEqual(
                healed["provenance"].get("detail_source"), "legacy-fallback",
                f"{bid}: fallback detail must be marked",
            )

    def test_fallback_detail_invents_no_refs(self):
        # The marked detail carries ONLY refs the legacy row already had.
        for bid, legacy in LEGACY_ROWS:
            healed = to_persisted_row(from_persisted_row(legacy))
            original_refs = set(legacy.get("evidence_refs") or [])
            for e in healed["provenance"]["evidence_detail"]:
                self.assertIn(e.get("ref"), original_refs, bid)
                self.assertEqual(e.get("kind"), "ref", bid)
                self.assertEqual(e.get("note"), "", bid)

    def test_healed_cycle_is_byte_exact_fixpoint(self):
        # import -> export -> import -> export -> import: byte-compare passes
        # from the healed row onward (the first transition IS the heal).
        for bid, legacy in LEGACY_ROWS:
            f1 = from_persisted_row(legacy)
            r1 = to_persisted_row(f1)
            f2 = from_persisted_row(r1)
            r2 = to_persisted_row(f2)
            f3 = from_persisted_row(r2)
            self.assertEqual(j(r2), j(r1), f"{bid}: healed row not stable")
            self.assertEqual(j(f3), j(f2), f"{bid}: healed block not stable")

    def test_marker_survives_roundtrip_verbatim(self):
        for bid, legacy in LEGACY_ROWS:
            healed = to_persisted_row(from_persisted_row(legacy))
            back = from_persisted_row(healed)
            self.assertEqual(
                back["provenance"].get("detail_source"), "legacy-fallback", bid)
            rehealed = to_persisted_row(back)
            self.assertEqual(
                rehealed["provenance"].get("detail_source"), "legacy-fallback",
                f"{bid}: marker must be carried, never recomputed or flipped")

    def test_modern_reexport_adds_no_marker(self):
        # The t922 path is untouched: modern rows gain no new provenance key.
        for bid, raw in seed_blocks.SEED:
            b = normalize_file_block(copy.deepcopy(raw),
                                     default_owner_id="",
                                     default_owner_scope="TEAM")
            b["owner_id"] = "NAYA"  # canonical system owner (Shawn's word 2026-10-11)
            row1 = to_persisted_row(b)
            self.assertNotIn("detail_source", row1["provenance"], bid)
            row2 = to_persisted_row(from_persisted_row(row1))
            self.assertNotIn("detail_source", row2["provenance"], bid)
            self.assertEqual(j(row2["provenance"]), j(row1["provenance"]), bid)

    def test_hand_authored_rich_detail_first_export_unmarked(self):
        # A hand-authored block with REAL rich detail (kind/note populated)
        # but no detail keys yet in provenance is NOT legacy — its content is
        # authored, so no fallback marker may be stamped.
        b = normalize_file_block(copy.deepcopy(seed_blocks.SEED[0][1]),
                                 default_owner_id="",
                                 default_owner_scope="TEAM")
        b["owner_id"] = "NAYA"  # canonical system owner (Shawn's word 2026-10-11)
        assert "evidence_detail" not in b["provenance"]
        assert b["evidence"][0]["kind"] != "ref"  # real authored detail
        row = to_persisted_row(b)
        self.assertNotIn("detail_source", row["provenance"])
        self.assertEqual(row["provenance"]["evidence_detail"], b["evidence"])

    def test_tampered_detail_source_fails_closed(self):
        _, legacy = LEGACY_ROWS[0]
        row = to_persisted_row(from_persisted_row(legacy))
        row["provenance"]["detail_source"] = ["not", "a", "string"]
        with self.assertRaises(ValueError):
            from_persisted_row(row)


if __name__ == "__main__":
    unittest.main(verbosity=2)
