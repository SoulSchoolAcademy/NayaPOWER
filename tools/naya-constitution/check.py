#!/usr/bin/env python3
"""The Naya Constitution, executable — the pre-action decision gate.

Implements Article IV of BRAIN/01-GOVERNANCE/0036-NAYA-CONSTITUTION-V1:
before a Naya acts on anything consequential, the decision runs through
this gate. The gate has exactly three verdicts:

  PROCEED — the checklist ran, the math picked the option, act on it.
  STOP    — the checklist did not run (scope unseen, options unscored,
            or approval sought that the law does not require). Fix the
            named defect and run again. STOP is never a dead end.
  GATE    — the action sits on the director's gate list. Prepare the
            packet and route it; continue all non-gated work.

Distinct from tools/strategy-engine (disposition clock + value
accounting, post-decision). This gate is pre-action: it decides whether
and how to act. Weights and gates mirror the machine tongue exactly.
"""
import json
import sys

WEIGHTS = {"value": 0.25, "intelligence": 0.30, "collective": 0.30, "reversibility": 0.15}
GATES = {"money", "credentials", "production_db", "irreversible", "ratification", "authority_security"}
TIE_EPSILON = 0.05


def total(option):
    scores = option["scores"]
    return sum(WEIGHTS[d] * scores[d] for d in WEIGHTS)


def decide(action):
    """action: {
        "action": str, "objective": str,
        "scope_complete": bool, "elements": [str, ...],
        "options": [{"name": str, "scores": {"value": n, "intelligence": n,
                     "collective": n, "reversibility": n}}, ...],
        "human_gate": None | one of GATES,
        "seeks_director_approval": bool
    } -> verdict dict"""
    gate = action.get("human_gate")
    if gate is not None:
        if gate not in GATES:
            return _verdict("STOP", None, {},
                            f"unknown gate '{gate}' — the gate list is exhaustive: {sorted(GATES)}")
        return _verdict("GATE", None, {},
                        f"'{gate}' belongs to the director. Prepare the packet (options + scores "
                        "+ recommendation + evidence), route it, and continue all non-gated work.")

    if action.get("seeks_director_approval"):
        return _verdict("STOP", None, {},
                        "tap-inflation (Article III, B4): the checklist decides this — "
                        "score the options and act. Do not seek the director's approval off the gate list.")

    if not action.get("scope_complete") or not action.get("elements"):
        return _verdict("STOP", None, {},
                        "full scope first (Article IV step 3): name every element, seam, and "
                        "other owner on the surface before acting.")

    options = action.get("options") or []
    if not options:
        return _verdict("STOP", None, {},
                        "no options enumerated (Article IV step 4): name the real options, "
                        "including the root repair and doing less, before acting.")
    for opt in options:
        missing = [d for d in WEIGHTS if d not in (opt.get("scores") or {})]
        if missing:
            return _verdict("STOP", None, {},
                            f"option '{opt.get('name')}' is unscored on {missing} "
                            "(Article IV step 5): math decides, so every option carries every score.")

    totals = {opt["name"]: round(total(opt), 4) for opt in options}
    best = max(options, key=lambda o: totals[o["name"]])
    tied = [o for o in options if abs(totals[o["name"]] - totals[best["name"]]) <= TIE_EPSILON]
    if len(tied) > 1:
        tied.sort(key=lambda o: (o["scores"]["reversibility"], o["scores"]["intelligence"]), reverse=True)
        best = tied[0]
    return _verdict("PROCEED", best["name"], totals,
                    f"highest total wins (Article IV step 5): {best['name']} at {totals[best['name']]}. "
                    "Act, verify against reality, record the same pass, learn.")


def _verdict(verdict, chosen, totals, reason):
    return {"verdict": verdict, "chosen": chosen, "totals": totals,
            "reason": reason, "law": "0036-NAYA-CONSTITUTION-V1 Article IV"}


if __name__ == "__main__":
    print(json.dumps(decide(json.load(sys.stdin)), indent=1))
