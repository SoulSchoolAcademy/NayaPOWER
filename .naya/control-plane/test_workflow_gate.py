import unittest

from workflow_gate import load_authority_registry, resolve_authority


class WorkflowGateTests(unittest.TestCase):
    def test_registry_contains_explicit_authority(self):
        registry = load_authority_registry()
        authority = resolve_authority(
            registry,
            actor="SoulSchoolAcademy",
            permission="repo_write",
            scope="repo:SoulSchoolAcademy/NayaPOWER:path:index.html",
        )
        self.assertEqual(authority.authority_id, "HUMAN-SOULSCHOOLACADEMY-REPO-WRITE")

    def test_unknown_actor_cannot_mint_authority(self):
        registry = load_authority_registry()
        with self.assertRaises(RuntimeError):
            resolve_authority(
                registry,
                actor="untrusted-workflow-actor",
                permission="repo_write",
                scope="repo:SoulSchoolAcademy/NayaPOWER:path:index.html",
            )

    def test_scope_mismatch_cannot_mint_authority(self):
        registry = load_authority_registry()
        with self.assertRaises(RuntimeError):
            resolve_authority(
                registry,
                actor="SoulSchoolAcademy",
                permission="repo_write",
                scope="repo:SoulSchoolAcademy/NayaPOWER:path:governance",
            )


if __name__ == "__main__":
    unittest.main()
