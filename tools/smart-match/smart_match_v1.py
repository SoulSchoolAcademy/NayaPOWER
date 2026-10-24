#!/usr/bin/env python3
"""
Smart Match v1 — reference implementation (Naya Power, SET B / engine end, 2026-10-24).

One logic, everywhere: every entity carries a declared profile vector
(topics / goals / offers / needs / wants). A match is a percentage computed
from those declared signals ONLY — explainable, with its reasons attached.

Published v1 weights (Lock Packet, Issue #3029 — adopted from the prototype):
  shared topics 40% · goals alignment 25% · offers<->needs fit 20% · desired connections 15%
Rules: a suggestion surfaces only on >= 2 independent signals; private /
opted-out / non-discoverable candidates are excluded by the caller, never
scored. Matching suggests; the person chooses Connect.
"""
import json

WEIGHTS = {"topics": 0.40, "goals": 0.25, "offers_needs": 0.20, "wants": 0.15}


def overlap(a, b):
    """Overlap coefficient: shared / min(|a|,|b|). Forgiving for asymmetric sets."""
    A, B = set(a or []), set(b or [])
    if not A or not B:
        return 0.0, []
    shared = sorted(A & B)
    return len(shared) / min(len(A), len(B)), shared


def score(a, b):
    t, t_shared = overlap(a.get("topics"), b.get("topics"))
    g, g_shared = overlap(a.get("goals"), b.get("goals"))
    on1, on1_shared = overlap(a.get("offers"), b.get("needs"))
    on2, on2_shared = overlap(b.get("offers"), a.get("needs"))
    on = (on1 + on2) / 2.0
    w, w_shared = overlap(a.get("wants"), (b.get("topics") or []) + (b.get("offers") or []))
    parts = {"topics": t, "goals": g, "offers_needs": on, "wants": w}
    total = round(100 * sum(WEIGHTS[k] * v for k, v in parts.items()))
    signals = [k for k, v in parts.items() if v > 0]
    reasons = []
    if t_shared:
        reasons.append("shared topics: " + ", ".join(t_shared[:4]))
    if g_shared:
        reasons.append("shared goals: " + ", ".join(g_shared[:3]))
    fits = sorted(set(on1_shared + on2_shared))
    if fits:
        reasons.append("offer/need fit: " + ", ".join(fits[:3]))
    if w_shared:
        reasons.append("wanted connection: " + ", ".join(w_shared[:3]))
    return {"score": total, "signals": signals, "surface": len(signals) >= 2,
            "parts": {k: round(v, 2) for k, v in parts.items()}, "reasons": reasons}


# --- Declared vectors, from the team's own published record only ----------
# Seats: the Narzan Trinity poster (Shawn, 2026-10-23) + Naya Power's own
# Welcome answers (given in chat, 2026-10-24). Nothing invented.
SEATS = {
    "naya-power (Naya P Narzan, Builder/Integrator)": {
        "topics": ["systems", "integration", "project intelligence", "matching", "derivation", "building", "design"],
        "goals": ["connect the parts", "prove outcomes", "scale nayanet", "whole board honest"],
        "offers": ["systems architecture", "integration", "project leadership", "strategy", "builders"],
        "needs": ["live data", "evidence", "builders"],
        "wants": ["builders", "verifiers", "citizens"]},
    "nitro (Naya N Narzan, Nitro/Executor/Verifier)": {
        "topics": ["execution", "delivery", "testing", "validation", "quality", "evidence", "proof"],
        "goals": ["ship", "test everything", "prove results"],
        "offers": ["execution", "testing", "quality control", "evidence", "builders"],
        "needs": ["specs", "builders"],
        "wants": ["builders", "verifiers"]},
    "resolve (Naya R Narzan, Resolver)": {
        "topics": ["root cause", "critical thinking", "conflict resolution", "risk", "reliability", "blockers"],
        "goals": ["find blockers", "clear the path", "reliable systems"],
        "offers": ["analysis", "risk review", "problem solving"],
        "needs": ["signals", "reports"],
        "wants": ["builders", "reporters"]},
}

# Projects/spaces: name + motto + the part's known purpose and gaps (tonight's record).
PROJECTS = {
    "NayaPOWER (space-nayapower)": {
        "topics": ["systems", "building", "integration", "intelligence", "network"],
        "goals": ["fully active and alive", "prove outcomes"],
        "offers": ["the platform", "coordination", "builders"],
        "needs": ["builders", "integration", "verification"]},
    "Ask Naya (space-ask-naya)": {
        "topics": ["conversation", "questions", "answers", "listening", "hub"],
        "goals": ["live in the hub", "pass the ear test"],
        "offers": ["answers", "guidance"],
        "needs": ["ear test", "voice"]},
    "Smart Mail (space-smart-mail)": {
        "topics": ["mail", "messaging", "communication", "scheduling"],
        "goals": ["compose anywhere send on time"],
        "offers": ["messaging", "delivery"],
        "needs": ["citizens", "usage"]},
    "Team Nitro (space-team-nitro)": {
        "topics": ["build loop", "execution", "delivery", "waves", "testing"],
        "goals": ["ship", "wip discipline"],
        "offers": ["execution", "builders"],
        "needs": ["builders", "specs"]},
    "The Mirror Program (space-mirror)": {
        "topics": ["distillation", "essence", "reflection", "learning"],
        "goals": ["essence over archives"],
        "offers": ["distilled intelligence"],
        "needs": ["material", "readers"]},
    "The One Flow (space-one-flow)": {
        "topics": ["smart notes", "feed", "publishing", "flow", "derivation"],
        "goals": ["note to live card in seconds"],
        "offers": ["publishing path"],
        "needs": ["notes", "citizens"]},
    "The One Hub (space-one-hub)": {
        "topics": ["hub", "front door", "performance", "audit", "systems"],
        "goals": ["the one hub for all nayanet", "prove outcomes"],
        "offers": ["home", "orientation"],
        "needs": ["performance rulings", "speed", "evidence"]},
    "The Smart Factory (space-smart-factory)": {
        "topics": ["templates", "apps", "building", "creation", "design"],
        "goals": ["template to live app in minutes"],
        "offers": ["app creation"],
        "needs": ["step 7", "builders"]},
    "Voice (space-voice)": {
        "topics": ["voice", "speech", "audio", "streaming"],
        "goals": ["nayas real voice"],
        "offers": ["voice"],
        "needs": ["streaming", "synthesis"]},
}

if __name__ == "__main__":
    out = {"seats_x_projects": {}, "seats_x_seats": {}}
    for sname, svec in SEATS.items():
        rows = []
        for pname, pvec in PROJECTS.items():
            r = score(svec, pvec)
            rows.append({"project": pname, **r})
        out["seats_x_projects"][sname] = sorted(rows, key=lambda x: -x["score"])
    names = list(SEATS)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            r = score(SEATS[names[i]], SEATS[names[j]])
            out["seats_x_seats"][f"{names[i]} <-> {names[j]}"] = r
    print(json.dumps(out, indent=1))
