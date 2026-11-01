"""Isolated adversarial controls: no production data or network requests."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENGINE = HERE.parent
MODULE = ENGINE / "recipe_preflight_v1.py"
SAMPLE = ENGINE / "examples/smart_lists_recipe_v1.sample.json"
s = importlib.util.spec_from_file_location("recipe_preflight", MODULE)
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)
BASE = json.loads(SAMPLE.read_text(encoding="utf-8"))
INDEX = {"pieces": {p: {"status": "canonical"} for p in ("NAYA-BRD-001","NAYA-BTN-009","NAYA-INP-008")}}
INDEX["pieces"]["NAYA-INP-001"] = {"status": "superseded"}
INDEX["pieces"]["NAYA-BTN-034"] = {"status": "retired"}
INDEX["pieces"]["NAYA-BRD-031"] = {"status": "verified"}
STORE = {k: {"name": k, "html": "fixture"} for k in ("NAYA-BRD-001","NAYA-BTN-009","NAYA-INP-008","NAYA-INP-001")}

class RecipePreflightTests(unittest.TestCase):
    def setUp(self):
        self.r = copy.deepcopy(BASE)
        self.index = copy.deepcopy(INDEX)
        self.store = copy.deepcopy(STORE)
    def errors(self,mode="draft"):
        return m.inspect(self.r,self.index,self.store,mode)[0]
    def test_draft_shape_only_passes(self):
        errors,warnings=m.inspect(self.r,self.index,self.store)
        self.assertEqual(errors,[])
        self.assertTrue(any("unwired" in w for w in warnings))
    def test_release_cannot_promote_unwired_sample(self):
        self.assertTrue(self.errors("release_candidate"))
    def test_superseded_in_store_denied(self):
        self.r["parts"][2]["id"]="NAYA-INP-001"
        self.r["recipe"]["scenes"][1]["part_ids"][0]="NAYA-INP-001"
        self.assertTrue(any("not canonical" in x for x in self.errors()))
    def test_retired_not_selectable(self):
        self.r["parts"][1]["id"]="NAYA-BTN-034"
        self.r["recipe"]["scenes"][0]["part_ids"][1]="NAYA-BTN-034"
        self.r["recipe"]["scenes"][1]["part_ids"][1]="NAYA-BTN-034"
        self.assertTrue(any("not canonical" in x for x in self.errors()))
    def test_verified_without_store_denied(self):
        self.r["parts"][0]["id"]="NAYA-BRD-031"
        self.r["recipe"]["scenes"][0]["part_ids"][0]="NAYA-BRD-031"
        errors=self.errors()
        self.assertTrue(any("not canonical" in x for x in errors))
        self.assertTrue(any("missing from current working store" in x for x in errors))
    def test_canonical_missing_store_denied(self):
        self.store.pop("NAYA-INP-008")
        self.assertTrue(any("missing from current working store" in x for x in self.errors()))
    def test_unknown_action_denied(self):
        self.r["recipe"]["scenes"][0]["primary_action_id"]="invented-verb"
        self.assertTrue(any("invented-verb undeclared" in x for x in self.errors()))
    def test_missing_small_phone_denied(self):
        self.r["shell"]["responsive_viewports"]=[[390,844],[768,1024],[1440,900]]
        self.assertTrue(any("missing canonical device coverage" in x for x in self.errors()))
    def test_too_many_context_items_denied(self):
        self.r["recipe"]["scenes"][0]["context"]=["one","two","three","four"]
        self.assertTrue(any("0–3" in x for x in self.errors()))
    def test_duplicate_scene_denied(self):
        self.r["recipe"]["scenes"][1]["id"]="lists-home"
        self.assertTrue(any("duplicate" in x for x in self.errors()))

if __name__ == "__main__":
    unittest.main(verbosity=2)
