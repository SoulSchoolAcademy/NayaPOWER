import copy
import importlib.util
import json
import subprocess
import tempfile
import unittest
from unittest import mock
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / ".naya/runtime/hub_identity_projection.py"
SPEC = importlib.util.spec_from_file_location("hub_identity_projection", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
BATON_PATH = ROOT / ".naya/runtime/baton.py"
BATON_SPEC = importlib.util.spec_from_file_location("canonical_baton_for_projection", BATON_PATH)
assert BATON_SPEC is not None and BATON_SPEC.loader is not None
BATON = importlib.util.module_from_spec(BATON_SPEC)
BATON_SPEC.loader.exec_module(BATON)


class HubIdentityProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = MODULE.load_contract(ROOT)
        cls.authority = MODULE.resolve_authority(ROOT, "origin/main")
        cls.state = MODULE.load_json(ROOT / ".naya/control-plane/STATE.json")
        cls.map_data = MODULE.load_json(ROOT / ".naya/control-plane/MAP.json")
        cls.team_lock = (ROOT / ".naya/TEAM-NAYA/00-NAYANET-HUB-NORTH-STAR-MISSION-LOCK.md").read_text(encoding="utf-8")
        cls.baton = MODULE.load_json(ROOT / ".naya/control-plane/BATON.json")

    def projected(self):
        return MODULE.project_documents(
            self.authority,
            self.contract,
            copy.deepcopy(self.state),
            copy.deepcopy(self.map_data),
            self.team_lock,
        )

    def test_authority_resolves_active_preservation_source(self):
        expected = subprocess.check_output(
            ["git", "rev-parse", "origin/main:NAYANET/HUB/index.html"],
            cwd=ROOT,
            text=True,
        ).strip()
        self.assertEqual(self.authority["hub_sha"], expected)
        self.assertEqual(self.authority["hub_path"], "NAYANET/HUB/index.html")
        self.assertEqual(self.authority["manifest"]["status"], "ACTIVE")

    def test_contract_declares_canonical_file_hash(self):
        self.assertEqual(self.contract["file_hash"], MODULE.FILE_HASH_SEMANTICS)

    def test_incomplete_receipt_fails(self):
        receipt = MODULE.load_json(MODULE.RECEIPT_PATH)
        del receipt["file_hash"]
        with self.assertRaisesRegex(MODULE.ProjectionError, "PROJECTION_RECEIPT_HASH_SEMANTICS_MISMATCH"):
            MODULE.validate_receipt(ROOT, self.authority, self.contract, receipt)

    def test_altered_protected_source_fails(self):
        real_git = MODULE.git

        def altered_git(root, *args):
            result = real_git(root, *args)
            if args[:2] == ("rev-parse", f"HEAD:{self.authority['hub_path']}"):
                return "0" * 40
            return result

        with mock.patch.object(MODULE, "git", side_effect=altered_git):
            with self.assertRaisesRegex(MODULE.ProjectionError, "PROJECTED_HUB_SOURCE_CHANGED"):
                MODULE.validate_projection(ROOT, self.authority, self.contract)

    def test_projection_updates_every_required_destination(self):
        projected = self.projected()
        for destination in self.contract["destinations"]:
            if destination["producer"] == "existing_baton_builder":
                continue
            actual = MODULE.destination_value(
                destination,
                projected["state"],
                projected["map_data"],
                projected["team_lock"],
                None,
            )
            self.assertEqual(actual, self.authority["hub_path"] if destination["value_kind"] == "hub_path" else self.authority["hub_sha"])
        self.assertEqual(MODULE.get_pointer(projected["map_data"], "/authority/canonical_hub_source_sha"), self.authority["hub_sha"])

    def test_stale_projection_fails(self):
        stale_state = copy.deepcopy(self.state)
        stale_state["hub_pre_execution_gate"]["canonical_hub_source_sha"] = "7b1126a014b3b27026a0360dbc1b8226a9be9f50"
        with self.assertRaisesRegex(MODULE.ProjectionError, "PROJECTION_VALUE_MISMATCH"):
            MODULE.validate_projection(
                ROOT,
                self.authority,
                self.contract,
                stale_state,
                self.map_data,
                self.team_lock,
                self.baton,
            )

    def test_tampered_projection_fails(self):
        projected = self.projected()
        projected["map_data"]["authority"]["canonical_hub_source_sha"] = "0" * 40
        with self.assertRaisesRegex(MODULE.ProjectionError, "PROJECTION_VALUE_MISMATCH"):
            MODULE.validate_projection_values(
                self.authority,
                self.contract,
                projected["state"],
                projected["map_data"],
                projected["team_lock"],
                projected.get("baton"),
            )

    def test_conflicting_projection_fails(self):
        projected = self.projected()
        projected["state"]["hub_pre_execution_gate"]["canonical_hub"] = "NAYANET/HUB/other.html"
        with self.assertRaisesRegex(MODULE.ProjectionError, "PROJECTION_VALUE_MISMATCH"):
            MODULE.validate_projection_values(
                self.authority,
                self.contract,
                projected["state"],
                projected["map_data"],
                projected["team_lock"],
                projected.get("baton"),
            )

    def test_missing_projection_fails(self):
        projected = self.projected()
        del projected["map_data"]["authority"]["canonical_hub_source_sha"]
        with self.assertRaisesRegex(MODULE.ProjectionError, "PROJECTION_TARGET_MISSING"):
            MODULE.validate_projection_values(
                self.authority,
                self.contract,
                projected["state"],
                projected["map_data"],
                projected["team_lock"],
                projected.get("baton"),
            )

    def test_wrong_authority_source_fails(self):
        authority = copy.deepcopy(self.authority)
        authority["hub_sha"] = "0" * 40
        with self.assertRaisesRegex(MODULE.ProjectionError, "AUTHORITY_SOURCE_MISMATCH"):
            MODULE.validate_authority(ROOT, authority, "origin/main")

    def test_duplicate_team_marker_fails(self):
        with self.assertRaisesRegex(MODULE.ProjectionError, "TEAM_NAYA_HUB_SHA_AMBIGUOUS"):
            MODULE.replace_team_marker(self.team_lock + "\nSHA: `7b1126a014b3b27026a0360dbc1b8226a9be9f50`\n", self.authority["hub_sha"])

    def test_projection_is_idempotent(self):
        first = self.projected()
        second = MODULE.project_documents(
            self.authority,
            self.contract,
            first["state"],
            first["map_data"],
            first["team_lock"],
        )
        self.assertEqual(first["state"], second["state"])
        self.assertEqual(first["map_data"], second["map_data"])
        self.assertEqual(first["team_lock"], second["team_lock"])

    def test_apply_rolls_back_on_write_failure(self):
        paths = [
            ROOT / ".naya/control-plane/STATE.json",
            ROOT / ".naya/control-plane/MAP.json",
            ROOT / ".naya/TEAM-NAYA/00-NAYANET-HUB-NORTH-STAR-MISSION-LOCK.md",
            ROOT / ".naya/control-plane/BATON.json",
            ROOT / ".naya/control-plane/HUB-IDENTITY-PROJECTION-RECEIPT.json",
        ]
        before = {path: path.read_bytes() for path in paths}
        original_write = MODULE.write_json

        def fail_on_map(path, value):
            if path.name == "MAP.json":
                raise OSError("simulated projection write failure")
            original_write(path, value)

        with mock.patch.object(MODULE, "write_json", side_effect=fail_on_map):
            with self.assertRaisesRegex(OSError, "simulated projection write failure"):
                MODULE.apply_projection(ROOT, "origin/main")
        for path in paths:
            self.assertEqual(path.read_bytes(), before[path])

    def test_file_hash_is_line_ending_independent(self):
        with tempfile.TemporaryDirectory() as directory:
            lf = Path(directory) / "lf.txt"
            crlf = Path(directory) / "crlf.txt"
            lf.write_bytes(b"one\ntwo\n")
            crlf.write_bytes(b"one\r\ntwo\r\n")
            self.assertEqual(MODULE.file_sha(lf), MODULE.file_sha(crlf))

    def test_baton_builder_accepts_explicit_source_identity(self):
        candidate = BATON.build_baton(
            source_commit=self.authority["source_commit"],
            hub_source_sha=self.authority["hub_sha"],
        )
        self.assertEqual(candidate["source_snapshot"]["live_head"], self.authority["source_commit"])
        self.assertEqual(candidate["source_snapshot"]["canonical_hub_source_sha"], self.authority["hub_sha"])


if __name__ == "__main__":
    unittest.main()
