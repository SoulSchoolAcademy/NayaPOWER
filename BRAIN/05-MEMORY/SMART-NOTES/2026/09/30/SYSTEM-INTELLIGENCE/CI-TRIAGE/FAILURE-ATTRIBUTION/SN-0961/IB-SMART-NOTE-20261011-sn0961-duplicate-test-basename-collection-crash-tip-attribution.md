# SN-0961 — Same Test Filename Twice, No __init__.py: Pytest's Import-File-Mismatch Collection Crash Is a Branch Bug, Not an Environment Bug

- **Intelligent Block:** IB-SMART-NOTE-20261011-sn0961-duplicate-test-basename-collection-crash-tip-attribution
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-11
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** night-shift-2026-10-10, worker t2350-b (tick t2350, 2026-10-10 23:50–00:00 PDT window) — receipt `receipts/t2350-b.md` (score 9): CI-REPRO for PR #2299's red `test` check; morning-flags.md #6 (2026-10-11 01:04 PDT).

## IN A NUTSHELL

PR #2299's CI `test` check was RED with a pytest **collection crash** (exit 2): two files named `test_activation_gate.py` — one in `tests/`, one in `tools/` — with no `__init__.py` anywhere and no pytest config. Pytest's rootdir import mode imports both by the bare module name `test_activation_gate`, hits an import-file-mismatch, aborts collection, and runs **zero tests**. The failure looks environmental (a "CI problem") but it is a tree defect: the attribution method that proved it was a `git ls-tree -r` diff of both tips — main `57e935c1` contains only `tools/test_activation_gate.py` (clean baseline), branch `8960a748` contains both. The branch introduced the collision; the environment was innocent. The durable method: on a branch-only collection crash, diff the branch tree against the tip for same-basename files **before** blaming CI. The durable fix (cheapest first): unique basenames; then `__init__.py` packages; then `testpaths`/importmode in pytest config. And the honest-evidence footnote from t2350-b: the prior t2332-a "2055 passed / 0 failed" on the same head ran a narrower command and was NOT evidence the tree was fine — a green claim from a command that isn't the exact CI step proves nothing.

## HUMAN NOTE

It's like two apartments in the same building both labeled "3B" — the mail carrier picks up a letter for 3B, sees two doors, and refuses to deliver anything at all. The building didn't break; someone put the wrong label on a door. And when the tip (main) has only one "3B" but your branch has two, the labeling happened in your branch — no need to blame the post office. Give every test file a unique name and the mail gets delivered.

## CHILD NOTE

Imagine two kids in class with exactly the same name, and the teacher calls the name — both stand up, and the teacher gets confused and cancels the whole roll call. Nobody learned anything that day, not because school is broken, but because two kids had the same name. Give your test files different names so the teacher (pytest) can call the roll.

## GRANDMA NOTE

It's like two jars in the pantry both labeled "sugar" — you reach for one, the labels don't match what's inside, and you throw the whole recipe out. The pantry is fine; the labels are the problem. Rename one jar and everything works again.

## NAYA NOTE

Apply this every time a branch's CI shows a pytest collection error with "import file mismatch": (1) fetch the exact branch head AND the live tip via git protocol (`git ls-tree -r`) and list test basenames on both — if the branch has a basename the tip has exactly once elsewhere, the collision is branch-introduced, full stop; (2) check for `__init__.py` and pytest config files — their absence is what makes rootdir import mode collide; (3) fix cheapest-first: rename one file to a unique basename, or move `tools/test_*.py` into `tests/`, or add `__init__.py` packages, or set `testpaths`/importmode — then re-run the EXACT CI command (`python -m pytest -q` from repo root) locally before any push; (4) never accept a narrower green run as evidence the tree is fine — t2332-a's "2055 passed" on the same head proved nothing because it wasn't the CI step; (5) do NOT re-run CI to "see if it clears" — that burns Actions minutes on a deterministic tree defect; the repro is local and free.

## MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "pytest_import_file_mismatch_from_duplicate_test_basename",
  "evidence": {
    "receipt": "night-shift-2026-10-10/receipts/t2350-b.md (score 9) — CI-REPRO for PR #2299",
    "branch_head": "8960a74868fcd122a395bc79b4c7f794c0613e33 (naya4/activation-gate-failclosed) — contains BOTH tests/test_activation_gate.py AND tools/test_activation_gate.py",
    "tip_baseline": "57e935c1b44b10fcc27a80f8c99fc9ddb2e69440 — contains ONLY tools/test_activation_gate.py; no collision on main",
    "exact_error": "ERROR collecting tools/test_activation_gate.py — import file mismatch: imported module 'test_activation_gate' has this __file__ attribute: .../tests/test_activation_gate.py which is not the same as the test file we want to collect: .../tools/test_activation_gate.py",
    "ci_step": ".github/workflows/kernel-tests.yml — 'python -m pytest -q', bare, repo root, python 3.12",
    "config_absence": "no __init__.py in tests/ or tools/; no pytest.ini/setup.cfg/pyproject.toml/conftest.py anywhere — rootdir import mode imports by bare module name"
  },
  "rule": "branch_only_collection_crash_means_diff_the_branch_tree_against_the_tip_for_same_basename_files_first",
  "procedure": [
    "on a branch-only pytest collection crash with import-file-mismatch, git ls-tree -r the branch head and the live tip; same basename in two paths on the branch but one on the tip = branch-introduced collision, not environmental",
    "fix cheapest-first: unique basenames > move tools/test_*.py into tests/ > add __init__.py packages > set testpaths/importmode in pytest config",
    "re-run the EXACT CI command locally before any push — never accept a narrower green run as evidence (t2332-a 2055-passed on the same head proved nothing)",
    "do not re-run CI to see if it clears — deterministic tree defect, local repro is free, CI minutes are not"
  ],
  "related": ["SN-0894 (classify environment before touching product code — here the environment was innocent)", "SN-0958 (prove the gate on the proven head)", "SN-0960 (the environment-side mass failure: full /tmp)", "SN-0962 (local repro at exact pinned head — the technique that closed this)"]
}
~~~
