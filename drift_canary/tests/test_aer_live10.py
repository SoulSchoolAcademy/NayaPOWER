"""AER-LIVE-10 tests: SCC Joint Proof Qualification."""
import sys
sys.path.insert(0, "drift_canary")

from aer_live10_scc import (
    SCCVerdict,
    scc01_impossible_bootstrap,
    scc02_valid_seeded_exchange,
    tarjan_scc,
)


def test_tarjan_finds_cycle():
    # budget -> resource -> budget (cycle)
    graph = {
        "budget": ["resource"],
        "resource": ["budget"],
        "lifecycle": [],
    }
    sccs = tarjan_scc(graph)
    # One SCC with budget+resource, one singleton lifecycle
    sizes = sorted(len(s) for s in sccs)
    assert sizes == [1, 2]


def test_tarjan_dag_singletons():
    graph = {"a": ["b"], "b": ["c"], "c": []}
    sccs = tarjan_scc(graph)
    assert all(len(s) == 1 for s in sccs)


def test_scc01_rejects_impossible_bootstrap():
    """SCC-01: no authorized seed → NOT repeatable."""
    r = scc01_impossible_bootstrap()
    assert r != SCCVerdict.REPEATABLE_CYCLE_PROVEN


def test_scc02_accepts_valid_seed():
    """SCC-02: authorized seed → repeatable."""
    assert scc02_valid_seeded_exchange() == SCCVerdict.REPEATABLE_CYCLE_PROVEN


def test_decisive_pair_differs():
    """Same topology, different verdicts → checks transitions not topology."""
    assert scc01_impossible_bootstrap() != scc02_valid_seeded_exchange()
