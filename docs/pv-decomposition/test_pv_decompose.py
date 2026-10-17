"""Adversarial fail-closed tests for PV-DECOMPOSITION-SPEC-0.1.

Each test feeds a malformed or hostile receipt and asserts the implementation
REFUSES it (ValueError) or degrades safely — never silently accepts.

Run: python3 -m unittest test_pv_decompose -v   (stdlib only)
"""

import copy
import json
import os
import unittest

from pv_decompose import decompose

HERE = os.path.dirname(os.path.abspath(__file__))


def load_example(name):
    with open(os.path.join(HERE, name)) as f:
        return json.load(f)


def term(**kw):
    d = {
        "id": kw.pop("id", "tx"),
        "bucket": "B",
        "unit": "value_points",
        "raw_magnitude": 5.0,
        "confidence": 0.9,
        "evidence_ref": "ev-1",
    }
    d.update(kw)
    return d


class TestFailClosed(unittest.TestCase):
    # 1. Duplicate evidence ref = term-splitting (one fact, one term)
    def test_duplicate_evidence_ref_rejected(self):
        doc = load_example("worked-example-2576-repair.json")
        doc["terms"].append(copy.deepcopy(doc["terms"][0]))
        with self.assertRaises(ValueError):
            decompose(doc)

    # 2. Unknown unit: fail-closed, no guessing
    def test_unknown_unit_rejected(self):
        doc = {"spec_version": "PV-DECOMP-0.1", "terms": [term(unit="story_points")]}
        with self.assertRaises(ValueError):
            decompose(doc)

    # 3. Missing rate on a non-fixed unit: no silent default
    def test_missing_rate_rejected(self):
        doc = {"spec_version": "PV-DECOMP-0.1", "terms": [term(unit="hours")]}
        with self.assertRaises(ValueError):
            decompose(doc)

    # 4. Wrong spec version: refuse, don't reinterpret
    def test_bad_version_rejected(self):
        doc = load_example("worked-example-2576-repair.json")
        doc["spec_version"] = "PV-DECOMP-0.2"
        with self.assertRaises(ValueError):
            decompose(doc)

    # 5. Empty term list: nothing to decompose
    def test_empty_terms_rejected(self):
        doc = {"spec_version": "PV-DECOMP-0.1", "terms": []}
        with self.assertRaises(ValueError):
            decompose(doc)

    # 6. Confidence outside [0,1]: refuse
    def test_bad_confidence_rejected(self):
        doc = {"spec_version": "PV-DECOMP-0.1",
               "terms": [term(confidence=1.5), term(id="t2", evidence_ref="ev-2", confidence=-0.1)]}
        with self.assertRaises(ValueError):
            decompose(doc)

    # 7. Unattested empty bucket: fail-closed confidence 0.0, residual charges the
    # uncertainty, and pv can NEVER exceed the full-confidence reading of the
    # same measured magnitudes (residual >= R always). The 0.0 confidence is
    # exposed in the receipt so a consumer can gate on it.
    def test_unattested_empty_bucket_fail_closed(self):
        doc = load_example("worked-example-2576-repair.json")
        # drop the C term -> C becomes the unattested empty bucket
        doc["terms"] = [t for t in doc["terms"] if t["bucket"] != "C"]
        out = decompose(doc)
        self.assertEqual(out["component_confidence"]["C"], 0.0)
        self.assertEqual(out["C"], 0.0)
        # residual = max(R, 1.0 * (1 - min_conf)) = max(0.4, 1.0) = 1.0
        # pv = 6.0 - 0 - 0 - 1.0 = 5.0, and the invariant: uncertainty never
        # inflates pv past the full-confidence reading of the same magnitudes
        self.assertEqual(out["pv"], 5.0)
        self.assertLessEqual(out["pv"], out["B"] - out["H"] - out["C"] - out["R"])

    # Positive controls: both worked examples cold-recomputable, exact
    def test_example_2576_exact(self):
        out = decompose(load_example("worked-example-2576-repair.json"))
        self.assertEqual((out["B"], out["H"], out["C"], out["R"], out["pv"]),
                         (6.0, 0.0, 1.4, 0.4, 4.2))

    def test_example_lane1_drill_exact(self):
        out = decompose(load_example("worked-example-lane1-drill.json"))
        self.assertEqual((out["B"], out["H"], out["C"], out["R"], out["pv"]),
                         (9.0, 0.0, 2.0, 0.9, 6.1))


if __name__ == "__main__":
    unittest.main()
