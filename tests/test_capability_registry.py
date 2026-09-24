from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "capabilities" / "registry.v1.json"
SCHEMA_PATH = ROOT / "capabilities" / "registry.v1.schema.json"
CANONICAL_FIELDS = {
    "id",
    "description",
    "inputs",
    "outputs",
    "required_authority",
    "allowed_scope",
    "risk",
    "reversibility",
    "receipt_required",
    "verification_required",
}
EXPECTED_CAPABILITY_COUNT = 36


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class CapabilityRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_json(REGISTRY_PATH)
        cls.schema = load_json(SCHEMA_PATH)
        cls.capabilities = cls.registry["capabilities"]
        cls.by_id = {capability["id"]: capability for capability in cls.capabilities}
        cls.by_source = {
            source: capability
            for capability in cls.capabilities
            for source in capability["implementation"]["source_paths"]
        }

    def test_schema_and_registry_are_strict(self) -> None:
        self.assertEqual(self.registry["schema"], "NAYA_CAPABILITY_REGISTRY_V1")
        self.assertFalse(self.registry["provenance"]["runtime_mutation"])
        self.assertIn("does not grant authority", self.registry["authority_boundary"])
        capability_schema = self.schema["$defs"]["capability"]
        self.assertTrue(CANONICAL_FIELDS.issubset(capability_schema["required"]))
        self.assertFalse(capability_schema["additionalProperties"])
        self.assertEqual(len(self.capabilities), EXPECTED_CAPABILITY_COUNT)
        self.assertEqual(len(self.by_id), EXPECTED_CAPABILITY_COUNT)
        for capability in self.capabilities:
            self.assertEqual(set(capability), set(capability_schema["properties"]))
            self.assertTrue(CANONICAL_FIELDS.issubset(capability))
            self.assertRegex(capability["id"], r"^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+$")
            self.assertTrue(capability["description"])
            for field in ("inputs", "outputs", "required_authority", "allowed_scope"):
                values = capability[field]
                self.assertGreaterEqual(len(values), 1)
                self.assertEqual(len(values), len(set(values)))
                self.assertTrue(all(isinstance(value, str) and value for value in values))
            self.assertIn(capability["risk"], {"L1", "L2", "L3"})
            self.assertIn(capability["reversibility"], {"READ_ONLY", "REVERSIBLE", "RECOVERABLE", "IRREVERSIBLE"})
            self.assertIsInstance(capability["receipt_required"], bool)
            self.assertIsInstance(capability["verification_required"], bool)
            if capability["risk"] == "L3":
                self.assertTrue(capability["receipt_required"])
                self.assertTrue(capability["verification_required"])
                self.assertNotEqual(capability["reversibility"], "READ_ONLY")
            implementation = capability["implementation"]
            self.assertEqual(
                set(implementation),
                set(self.schema["$defs"]["capability"]["properties"]["implementation"]["required"]),
            )
            self.assertEqual(implementation["status"], "IMPLEMENTED")
            self.assertEqual(implementation["evidence_state"], "IMPLEMENTED")
            self.assertIn(
                implementation["authority_enforcement"],
                {"AUTHENTICATION_ONLY", "OWNER_SCOPE_VALIDATED", "EXPLICIT_GRANT_VALIDATED", "SIGNED_EXTERNAL_INPUT", "NOT_TESTED"},
            )
            for source in implementation["source_paths"]:
                self.assertTrue((ROOT / source).exists(), source)
            self.assertGreaterEqual(len(implementation["invocation"]), 1)
            self.assertGreaterEqual(len(implementation["transport_aliases"]), 0)
            self.assertTrue(implementation["notes"])

    def test_compound_action_parity(self) -> None:
        source = (ROOT / "supabase/functions/nayanet-compound-intelligence/index.ts").read_text(encoding="utf-8")
        start = source.index("switch(action)")
        end = source.index('default: throw new Error("UNKNOWN_ACTION")', start)
        source_actions = set(re.findall(r'case "([^"]+)"', source[start:end]))
        source_actions.add("universal_meaningful_output")
        registered = {}
        for capability in self.capabilities:
            for invocation in capability["implementation"]["invocation"]:
                if invocation.startswith("compound_action:"):
                    action = invocation.split(":", 1)[1]
                    self.assertNotIn(action, registered, action)
                    registered[action] = capability["id"]
        self.assertEqual(set(registered), source_actions)

    def test_project_intelligence_wrapper_parity(self) -> None:
        wrappers = sorted((ROOT / "supabase/functions").glob("nayanet-pi-*/index.ts"))
        self.assertGreater(len(wrappers), 0)
        for wrapper in wrappers:
            text = wrapper.read_text(encoding="utf-8")
            match = re.search(r'const ACTION="([^"]+)"', text)
            self.assertIsNotNone(match, wrapper)
            action = match.group(1)
            relative = wrapper.relative_to(ROOT).as_posix()
            capability = self.by_source[relative]
            invocations = capability["implementation"]["invocation"]
            self.assertIn(f"compound_action:{action}", invocations)
            self.assertIn(f"edge_function:{wrapper.parent.name}", invocations)

    def test_universal_agent_interface_alias_parity(self) -> None:
        source = (ROOT / "NAYANET/UNIVERSAL-AGENT-INTERFACE/worker.js").read_text(encoding="utf-8")
        tools = dict(re.findall(r"name==='(nayanet_[^']+)'\s*\?\s*'([^']+)'", source))
        routes = dict(re.findall(r"'(/v1/[^']+)':'([^']+)'", source))
        self.assertEqual(set(tools), {"nayanet_cold_restore", "nayanet_restore", "nayanet_retrieve", "nayanet_understand"})
        self.assertEqual(set(routes.values()), {"cold_restore", "restore", "retrieve", "understand"})
        alias_owners = {}
        for capability in self.capabilities:
            for alias in capability["implementation"]["transport_aliases"]:
                self.assertNotIn(alias, alias_owners, alias)
                alias_owners[alias] = capability
        for tool, action in tools.items():
            capability = alias_owners[f"uai:{tool}"]
            self.assertIn(f"compound_action:{action}", capability["implementation"]["invocation"])
        for route, action in routes.items():
            capability = alias_owners[f"rest:{route}"]
            self.assertIn(f"compound_action:{action}", capability["implementation"]["invocation"])

    def test_all_edge_function_sources_are_registered(self) -> None:
        function_sources = {
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "supabase/functions").glob("*/index.ts")
        }
        registered_sources = {
            source
            for capability in self.capabilities
            for source in capability["implementation"]["source_paths"]
            if source.startswith("supabase/functions/")
        }
        self.assertEqual(function_sources, registered_sources)

    def test_direct_action_parity(self) -> None:
        feed_source = (ROOT / "supabase/functions/naya-smart-feed/index.ts").read_text(encoding="utf-8")
        feed_actions = set(re.findall(r"action==='([^']+)'", feed_source)) | {"read"}
        registered_feed_actions = {
            invocation.rsplit(":", 1)[1]
            for invocation in self.by_id["smart_feed.read"]["implementation"]["invocation"]
            + self.by_id["smart_feed.publish"]["implementation"]["invocation"]
            + self.by_id["smart_feed.revoke"]["implementation"]["invocation"]
            + self.by_id["smart_feed.interact"]["implementation"]["invocation"]
        }
        self.assertEqual(feed_actions, registered_feed_actions)
        mail_source = (ROOT / "supabase/functions/nayanet-smart-mail/index.ts").read_text(encoding="utf-8")
        mail_actions = set(re.findall(r'operation==="([^"]+)"', mail_source)) | {"send"}
        registered_mail_actions = {
            invocation.rsplit(":", 1)[1]
            for invocation in self.by_id["smart_mail.verify"]["implementation"]["invocation"]
            + self.by_id["smart_mail.send"]["implementation"]["invocation"]
        }
        self.assertEqual(mail_actions, registered_mail_actions)

    def test_execution_bridge_sources_are_registered(self) -> None:
        bridge_sources = {
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "NAYANET/EXECUTION-BRIDGE").glob("*/index.ts")
        }
        registered_sources = {
            source
            for capability in self.capabilities
            for source in capability["implementation"]["source_paths"]
            if source.startswith("NAYANET/EXECUTION-BRIDGE/")
        }
        self.assertEqual(bridge_sources, registered_sources)

    def test_protected_authority_surfaces_are_not_capabilities(self) -> None:
        for capability in self.capabilities:
            for source in capability["implementation"]["source_paths"]:
                self.assertFalse(source.startswith("NAYANET/HUB/"), source)
                self.assertFalse(source.startswith(".naya/control-plane/"), source)
                self.assertFalse(source.startswith(".naya/governance/authority-registry.json"), source)
        excluded = {surface["id"]: surface for surface in self.registry["excluded_surfaces"]}
        self.assertEqual(excluded["hub.owner-ui-methods"]["classification"], "OWNER_UI")
        self.assertEqual(excluded["pis.duplicate-producer-authority"]["classification"], "UNRESOLVED_AUTHORITY")
        self.assertEqual(excluded["system49.universal-smart-door-lifecycle"]["classification"], "OUT_OF_SCOPE")
        self.assertEqual(excluded["system50.distributed-naya-federation"]["classification"], "OUT_OF_SCOPE")
        for surface in self.registry["excluded_surfaces"]:
            for source in surface["source_paths"]:
                self.assertTrue((ROOT / source).exists(), source)

    def test_source_presence_does_not_claim_verification(self) -> None:
        for capability in self.capabilities:
            implementation = capability["implementation"]
            if implementation["status"] == "IMPLEMENTED":
                self.assertEqual(implementation["evidence_state"], "IMPLEMENTED")
            self.assertNotEqual(implementation["evidence_state"], "PRODUCTION-PROVEN")


if __name__ == "__main__":
    unittest.main()
