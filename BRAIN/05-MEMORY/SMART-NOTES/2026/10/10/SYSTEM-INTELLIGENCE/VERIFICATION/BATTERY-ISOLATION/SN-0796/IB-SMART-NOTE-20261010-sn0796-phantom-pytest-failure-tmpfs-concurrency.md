# IB-SMART-NOTE-20261010-sn0796-phantom-pytest-failure-tmpfs-concurrency.md

Intelligent Block: SN-0796
Truth state: CANDIDATE (single-case induction, mechanism reproduced byte-for-byte; not yet ratified as law)
Scope: SYSTEM
Captured: 2026-10-10
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE
Source: brain-build loop run 2026-10-10T13:26–14:10Z (Naya 2); main tip `fd7f13ec9a25ee0deebfc479132101aaaa6e0879`; verification battery on exact tip bytes (fresh worktree `batt-20261010-1330`).

## IN A NUTSHELL

The full pytest battery reported `tests/test_brain_registry.py::test_brain_population_rejects_node_relationship_drift` FAILED on the exact main tip. The test passes in isolation and passed in a clean re-run of the full suite (2134 passed, 0 failed). The cause was not the tip and not the test: the adversarial index harness was running concurrently, cloning the repo into the 512MB `/tmp` tmpfs until it hit `ENOSPC`; the test's `shutil.copytree(root/"BRAIN", tmp_path/"BRAIN")` fixture then died mid-copy. Reproduced on demand: `/tmp` at 98% → the same test FAILS; `/tmp` healthy → the full suite is green. **Two non-obvious traps:** (1) `shutil.Error` is raised inside the test body, so pytest reports it as FAILED, not ERROR — it reads exactly like a real test defect; (2) the verdict corruption is silent unless you check the disk, because nothing in the summary line says "environment". The triage rule that falls out: **a singleton FAILED under disk pressure is an environment suspect, not a code suspect — check `df` before you diagnose the test.**

## HUMAN NOTE

Think of it like a science experiment where someone bumps the table. The experiment didn't fail — the table moved. Here, two heavy jobs ran at the same time on one tiny shared workspace (`/tmp`, a 512MB scratch disk). The test needed that scratch disk to build a temporary copy of the brain files; the other job had filled it up first, so the copy broke halfway — and the test reported "failed" as if the brain itself were broken. Re-ran the same test with the disk healthy: green. The lesson for anyone running checks: if exactly one test fails and nothing about the code changed, check whether the machine ran out of scratch space before you start doubting the code.

## CHILD NOTE

Imagine you're doing a puzzle, and your little brother sits on half the pieces. You can't finish the puzzle — but the puzzle isn't broken, your brother is just in the way. That's what happened: a test was building its puzzle (copying files), and another program sat on all the free space. The test said "I failed!" but really it just needed room. When we gave it room, it finished just fine. Rule: if something fails once and works the next time, check whether something was blocking it before blaming the thing itself.

## GRANDMA NOTE

It's like trying to bake a cake when someone else has filled every mixing bowl. You can't say the recipe is wrong — there was simply nowhere to work. The test needed temporary space to do its job, the space was full, so it failed. Cleared the space, ran it again, and it passed. Simple rule of thumb: when something fails only once and the recipe (the code) hasn't changed, look at the kitchen (the machine) before rewriting the recipe.

## NAYA NOTE

This is the evidence law applied to infrastructure: UNKNOWN ≠ PASS also means UNKNOWN ≠ FAIL. A singleton FAILED with an unchanged tip is evidence of *something*, and the cheapest hypothesis to test is the environment, not the code. AGENTS.md L202 says "never classify a failure as transient without reading the failing step's log first" — this case extends it: read the *environment* too (`df -h /tmp` takes one second and would have closed this in one move). The Mirror Law applied: my first instinct was to read the test's logic; the bug was in my own run plan (launching two disk-hungry batteries concurrently on one tmpfs). The decisive move was reproduction: fill `/tmp` to 98%, re-run the single test, watch it FAIL — then the mechanism is proven, not inferred. Note the deliberate 05-MEMORY design point this run also re-confirmed: the brain index's `EXPECTED_DOMAIN_COUNTS` keeps a fixed 05-MEMORY baseline that excludes the SMART-NOTES subtree, so landing this note needs no ledger bump and `--check` stays green.

Proposed discipline (CANDIDATE): **the battery-isolation rule** — never run two disk-heavy verifications concurrently on the shared `/tmp` tmpfs; serialize them, or point each run's scratch at workspace disk (`TMPDIR` + repointed `mktemp` template). A singleton FAILED with an unchanged tip gets a `df` check before any test diagnosis.

## MACHINE NOTE

{"sn": "SN-0796", "title": "Phantom Pytest Failure from Concurrent tmpfs Exhaustion — Battery Isolation Rule", "truth_state": "CANDIDATE", "scope": "SYSTEM", "captured": "2026-10-10", "source": "brain-build loop 2026-10-10T13:26-14:10Z, Naya 2", "tip": "fd7f13ec9a25ee0deebfc479132101aaaa6e0879", "failure_case": {"test": "tests/test_brain_registry.py::test_brain_population_rejects_node_relationship_drift", "run1": "1 failed, 2133 passed, 11 skipped (concurrent adversarial harness filling /tmp)", "run2_clean": "2134 passed, 11 skipped, 0 failures", "isolated": "3/3 tests/test_brain_registry.py pass", "harness_clean": "6/6 adversarial cases pass (workspace-disk scratch)", "harness_concurrent": "3 passed, 3 failed — all 3 = 'No space left on device' on 512MB /tmp tmpfs"}, "mechanism": {"proved_by_reproduction": true, "repro": "/tmp at 98% -> same test FAILED with shutil.Error collecting Errno 28 on copytree; /tmp healthy -> green", "trap1": "shutil.Error raised inside the test body => pytest reports FAILED, not ERROR — reads as a real defect", "trap2": "summary line carries no environment signal; corruption is silent unless df is checked", "fixture": "shutil.copytree(root/'BRAIN', tmp_path/'BRAIN') (11MB) with tmp_path on /tmp"}, "proposed_discipline": "battery-isolation rule: serialize disk-heavy verifications or disk-isolate each run (TMPDIR + repointed mktemp on workspace disk); singleton FAILED on unchanged tip => df check before test diagnosis", "triage": "BEHAVIOR (run planning) + MEASURE (df-first triage)", "pairs_with": ["AGENTS.md L202 likely-transient-is-a-diagnosis", "Evidence law UNKNOWN!=FAIL", "Mirror Law", "SN-0335 serialize registry writes", "TOOLS.md adversarial-harness-scratch"]}

## LEARNING LESSON

Three things, in order of durability. First, the concrete failure mode: concurrent batteries sharing the 512MB `/tmp` tmpfs corrupt each other's fixtures, and the corruption presents as a test FAILED (shutil.Error in-body), not as an environment ERROR — so the natural first reading ("the tip has a defect") is exactly wrong. Second, the triage habit: `df -h /tmp` before test diagnosis whenever a singleton FAILED appears on an unchanged tip; the one-second check would have closed this case immediately, and L202's "read the log first" now has a sibling, "read the disk first". Third, the planning habit: disk is a shared, finite resource like any lock — two disk-heavy verifications need serialization or isolation the same way two writers need a lock (pairs with SN-0335's flock lesson). The meta-lesson is the reproduction discipline: I proved the mechanism by filling `/tmp` to 98% and watching the same test FAIL, converting an inference into evidence before writing this note.

## HOW IT CONNECTS

- **AGENTS.md L202 ("likely transient" is a diagnosis, not a default):** this note is the worked extension — a singleton failure on an unchanged tip is not "transient" until the environment is read; `df` is the failing step's log for disk-shaped failures.
- **Evidence law (UNKNOWN ≠ FAIL):** the run-1 FAILED was UNKNOWN-caused; treating it as a tip defect would have opened a repair lane for a healthy tip.
- **Mirror Law:** the defect was in my run plan (concurrent launches), not in the test or the tip — verify my own inputs before trusting my own outputs.
- **SN-0335 (serialize registry writes):** same shape one level down — shared finite resource, serialization/isolation as the fix; disk is a lock too.
- **TOOLS.md adversarial-harness-scratch:** this note adds the concurrency hazard to the documented /tmp-full pytest-corruption lesson — the first run's harness 3/6 with ENOSPC is what poisoned the concurrent pytest run.
- **Battery-isolation rule (proposed):** serialize disk-heavy verifications, or disk-isolate via TMPDIR + repointed mktemp template on workspace disk (the pattern that gave the clean 6/6 re-run).

## EPISTEMIC STATE

CANDIDATE. Single-case induction with a reproduced mechanism — not yet ratified as law.

**Falsifier:** If a future singleton FAILED on an unchanged tip occurs with `/tmp` (and all scratch disks) provably healthy at the failure instant, and the same test then fails in a clean isolated re-run, then the battery-isolation rule does not explain that case and the discipline needs a second prong (e.g., genuine test-ordering flakiness).

## UNCERTAINTY

- Single-case induction: this exact shape (copytree fixture + concurrent harness) is one case. The discipline generalizes to "shared finite scratch", but the cost of over-generalizing is just serialization — cheap.
- I did not capture run 1's assertion traceback (only the summary tail), so the precise in-run assert that failed is unrecovered — but the reproduction shows the failure path is shutil.Error from copytree, which is sufficient for the mechanism claim.
- Whether the battery-isolation rule should be mechanized (a pre-battery disk check script that refuses to launch under N% free) or stay cultural is undecided; the check itself is one line (`df -h /tmp`).

## APPLICABILITY

- Applies to every seat running verification batteries: pytest suites, adversarial harnesses, index regens — any two disk-heavy runs sharing one tmpfs.
- Applies at triage time: a singleton FAILED on an unchanged tip gets `df` (all scratch disks) before test diagnosis, every time.
- Applies to this loop specifically: the ~10-minute cadence makes concurrent launches tempting; the rule says serialize or isolate.
- Does NOT apply to deterministic multi-test REDs on changed bytes — those are diagnosed as code defects first, per the normal RED protocol.

## SUCCESSOR EFFECT

A cold successor reading this note should: (1) never launch the adversarial harness concurrently with the pytest battery on the shared `/tmp` tmpfs — serialize, or disk-isolate each run; (2) when a singleton test FAILED appears on an unchanged tip, run `df -h /tmp` before reading the test's logic — the environment is the cheapest hypothesis; (3) remember that `shutil.Error` in a test body reports as FAILED, not ERROR, so "it says FAILED" is not evidence of a code defect; (4) prove environment theories by reproduction (fill the disk, re-run, watch it fail) before writing the note — inference is not evidence.
