"""KNOW retrieval admission identity — whole-family pin (SN-0390).

nayanet-know-runtime admits OIDC-minted retrieval callers by workflow identity.
PR #1759 admitted the canonical ACT proof workflow and pinned only that one
member. This test pins the ENTIRE admission family: exactly the four canonical
proof workflows, no more, no fewer — plus a coherent-forgery negative.

A future lane copy-pasting the LAW runtime's wider admission set into KNOW
would silently widen the retrieval-caller surface; this test fails first.
Deliberate widening requires updating EXPECTED with a comment naming the PR.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KNOW = ROOT / "supabase" / "functions" / "nayanet-know-runtime" / "index.ts"

# The four proof workflows that legitimately call KNOW retrieve/inspect.
EXPECTED = {
    ".github/workflows/live-know-proof.yml",
    ".github/workflows/live-act-proof.yml",
    ".github/workflows/live-prove-proof.yml",
    ".github/workflows/live-connect-proof.yml",
}

# Real sibling-runtime identity, coherent but NOT a KNOW caller: admitted by
# nayanet-law-runtime, must never be admitted by nayanet-know-runtime.
# (SN-0559: forge coherent inputs, not garbage.)
COHERENT_FORGERY = ".github/workflows/live-law-proof.yml"


def _admitted(source: str) -> set:
    m = re.search(r"const WORKFLOWS=new Set\(\[(.*?)\]\)", source, re.S)
    assert m, "WORKFLOWS admission set not found in nayanet-know-runtime/index.ts"
    return set(re.findall(r'"([^"]+)"', m.group(1)))


def test_know_admits_exactly_the_four_canonical_proof_identities():
    admitted = _admitted(KNOW.read_text(encoding="utf-8"))
    assert admitted == EXPECTED, f"KNOW admission drift: {sorted(admitted ^ EXPECTED)}"


def test_know_rejects_coherent_sibling_runtime_identity():
    admitted = _admitted(KNOW.read_text(encoding="utf-8"))
    assert COHERENT_FORGERY not in admitted, (
        "KNOW must not admit the LAW proof workflow identity"
    )


def test_know_admitted_workflows_exist_on_disk():
    admitted = _admitted(KNOW.read_text(encoding="utf-8"))
    for w in sorted(admitted):
        assert (ROOT / w).is_file(), f"admitted KNOW workflow missing: {w}"


def test_know_binding_mechanics_still_pinned():
    source = KNOW.read_text(encoding="utf-8")
    assert "expectedRefs.includes(workflowRef)" in source
    assert "WORKFLOW_BINDING_MISMATCH" in source
