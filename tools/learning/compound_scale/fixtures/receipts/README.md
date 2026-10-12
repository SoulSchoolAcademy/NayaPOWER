# Receipt fixtures — pinned truth-gate evidence (hermetic)

**The defect (t0292):** `lessons_registry.json` pointed `receipt_file` at the
registry author's personal, rotating home files (`~/MEMORY.md`, `~/AGENTS.md`,
`~/TOOLS.md`, `~/workspace/agent-briefing-master.md`) and at
`~/workspace/naya/bin/gh-api`, which does not exist on other machines. The
truth gate returned 4 ("cited quote is not in it") or 0 ("receipt file
missing") on CI and on every machine that wasn't the author's at capture
time — five of the kernel `test`-step reds.

**The mechanism fix:** receipt evidence now ships WITH the repo. Each fixture
is frozen verbatim at pin time; the registry references it via the `pkg:`
scheme (resolved by `gates._read_receipt` against the compound_scale package
dir). The gate mechanics are unchanged — citation integrity is still
"the cited quote exists verbatim in the cited source"; only the sources are
stable.

**Rules:** do not edit the quoted lines. If a lesson's evidence genuinely
changes, capture a new fixture version and update the registry entry —
never mutate a pinned fixture in place (the registry seal covers the registry,
not the fixtures; the truth gate covers the verbatim quotes).

Files:

- `gh-api.md` — lessons L1, L2 (must_hold), A1 (must_contradict)
- `agents-lessons.md` — lessons L3, L4, L5 (must_hold)
- `memory-lessons.md` — lessons L6, L8, L11 (must_hold), A2 (must_contradict)
- `tools-lessons.md` — lesson L7 (must_hold), A3 (must_contradict)
- `agent-briefing-lessons.md` — lessons L9, L10 (must_hold)
