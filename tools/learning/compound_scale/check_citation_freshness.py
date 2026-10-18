"""CI freshness gate for the learn-compound-scale citation registry.

Re-runs gates.gate_truth() over every registry lesson against its cited
receipt file and fails loudly on drift: every lesson must score 9/9
(must_hold: cited evidence present verbatim; must_contradict: pre-registered
contradiction evidence present so the adversarial lesson is REJECTED).

Citations are hermetic repo fixtures
(tools/learning/compound_scale/receipts/<id>.md), so this gate is
byte-identical on CI runners and developer VMs. If a fixture or registry
quote drifts, this job goes red instead of the drift hiding as a
developer-VM-only silent red (2026-10-18 citation-drift defect).
"""
import json
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parent
sys.path.insert(0, str(PKG))

import gates  # noqa: E402

registry = json.loads((PKG / "lessons_registry.json").read_text(encoding="utf-8"))
drifted = []
for lesson in registry["lessons"]:
    score, detail = gates.gate_truth(lesson)
    print(f"{lesson['id']}: truth={score}/9 — {detail[:90]}")
    if score != 9:
        drifted.append((lesson["id"], score, detail))

if drifted:
    print(f"\nFAIL: {len(drifted)} citation(s) drifted:", file=sys.stderr)
    for lid, score, detail in drifted:
        print(f"  {lid}: {score}/9 — {detail}", file=sys.stderr)
    sys.exit(1)
print(f"\nOK: all {len(registry['lessons'])} citations hold at 9/9")
