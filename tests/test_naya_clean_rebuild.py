from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "naya_clean_rebuild.py"
SPEC = importlib.util.spec_from_file_location("naya_clean_rebuild", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class CleanRebuildTests(unittest.TestCase):
    def test_normalize_pis_removes_only_wall_clock_timestamp(self) -> None:
        first = b'{"generated_at":"2026-01-01T00:00:00+00:00","items":[2,1]}\n'
        second = b'{"items":[2,1],"generated_at":"2026-01-01T00:00:02+00:00"}\n'
        self.assertEqual(MODULE.normalize_pis(first), MODULE.normalize_pis(second))

    def test_discover_pis_producers(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            scripts = root / "scripts"
            scripts.mkdir()
            (scripts / "one.py").write_text('OUTPUT = "NAYANET/HUB/public/intelligence/pis-feed.json"\nOUTPUT.write_text("{}")\n', encoding="utf-8")
            (scripts / "two.py").write_text('OUT = ROOT / "pis-feed.json"\nOUT.write_bytes(b"{}")\n', encoding="utf-8")
            (scripts / "verify.py").write_text('TARGET = "pis-feed.json"\nprint(TARGET)\n', encoding="utf-8")
            (scripts / "unrelated.py").write_text("VALUE = 1\n", encoding="utf-8")
            self.assertEqual(MODULE.discover_pis_producers(root), ["scripts/one.py", "scripts/two.py"])

    def test_compare_deterministic_outputs(self) -> None:
        left = {"files": {"one.json": "a", "two.json": "b"}}
        right = {"files": {"one.json": "a", "two.json": "c"}}
        equal, differences = MODULE.compare_deterministic(left, right)
        self.assertFalse(equal)
        self.assertEqual(differences, [{"output": "two.json", "left": "b", "right": "c"}])

    def test_package_created_at(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "package.zip"
            with zipfile.ZipFile(package, "w") as archive:
                archive.writestr("manifest.json", json.dumps({"created_at": "2026-09-24T12:00:00Z"}))
            self.assertEqual(MODULE.package_created_at(package).isoformat(), "2026-09-24T12:00:00+00:00")


if __name__ == "__main__":
    unittest.main()
