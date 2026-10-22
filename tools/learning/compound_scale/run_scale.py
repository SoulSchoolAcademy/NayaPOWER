#!/usr/bin/env python3
"""Pre-registered scale run: 11 lessons + 3 adversarial probes through the
full pipeline (capture -> distill -> inject -> verify -> compound).

Pre-registration integrity: the runner seals lessons_registry.json's sha256
BEFORE any arm runs and refuses to run if the file changed since sealing.
Seal with:  python3 run_scale.py --seal
Run with:   python3 run_scale.py --run --out <dir>

Exit 0 = run completed (lesson failures are findings, not runner errors).
Exit 2 = seal mismatch / registry changed post-registration.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parent
sys.path.insert(0, str(PKG))

import gates
import pipeline
import subjects

REGISTRY = PKG / "lessons_registry.json"


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cmd_seal(_args) -> int:
    seal = {"sha256": sha256_of(REGISTRY),
            "sealed_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(
                timespec="seconds")}
    (PKG / "registry.seal.json").write_text(json.dumps(seal, indent=2))
    print(json.dumps(seal, indent=2))
    return 0


def cmd_run(args) -> int:
    seal_path = PKG / "registry.seal.json"
    if not seal_path.exists():
        print("FAIL: no seal; run --seal first", file=sys.stderr)
        return 2
    seal = json.loads(seal_path.read_text())
    now = sha256_of(REGISTRY)
    if now != seal["sha256"]:
        print(f"FAIL: registry changed since sealing "
              f"(sealed {seal['sha256'][:12]}, now {now[:12]})",
              file=sys.stderr)
        return 2
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    out = Path(args.out)
    real_transfer = (json.loads(Path(args.real_transfer).read_text())
                     if args.real_transfer else {})
    store = out / "store"
    store.mkdir(parents=True, exist_ok=True)

    report = {"sealed_sha256": seal["sha256"],
              "run_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(
                  timespec="seconds"),
              "lessons": []}

    for lesson in registry["lessons"]:
        lid = lesson["id"]
        if lesson.get("adversarial"):
            # Adversarial: capture -> distill -> Truth gate. Never injected.
            event = pipeline.capture(lesson, store / "events.jsonl")
            distilled = pipeline.distill_lesson(lesson, store / "events.jsonl")
            t_score, t_detail = gates.gate_truth(lesson)
            rejected = t_score >= 7
            entry = pipeline.compound(
                lesson, {}, {"truth": t_score}, float(t_score),
                out / "ledger.jsonl")
            entry["rejected"] = rejected
            entry["expected"] = lesson["prereg"]["expected"]
            entry["prereg_match"] = (rejected and entry["expected"] == "REJECT")
            entry["event_id"] = event["event_id"]
            entry["distilled"] = distilled["principle"]
            entry["truth_detail"] = t_detail
            report["lessons"].append(entry)
            print(f"{lid}: Truth gate -> "
                  f"{'REJECTED (correct)' if rejected else 'NOT REJECTED (FINDING)'} "
                  f"[{t_score}/9]")
            continue

        # Full pipeline for good lessons.
        event = pipeline.capture(lesson, store / "events.jsonl")
        distilled = pipeline.distill_lesson(lesson, store / "events.jsonl")
        arms = pipeline.verify(lesson, store, registry, out)
        rule = pipeline.inject(store, lid, registry)

        s_truth, d_truth = gates.gate_truth(lesson)
        s_under, d_under = gates.gate_understanding(
            lesson, distilled["principle"])
        s_effect, d_effect = gates.gate_effect(arms)
        s_causal, d_causal = gates.gate_causality(arms)
        d_passed, d_detail = pipeline.durability_check(
            lesson, store, REGISTRY, out)
        s_dur, d_dur = gates.gate_durability(d_passed, d_detail)
        real = None
        if real_transfer and lid in real_transfer:
            real = bool(real_transfer[lid].get("passed"))
        s_trans, d_trans = gates.gate_transfer(
            arms["successor"]["passed"], real)

        scores = {"truth": s_truth, "understanding": s_under,
                  "effect": s_effect, "causality": s_causal,
                  "durability": s_dur, "transfer": s_trans}
        verdict, v_detail = gates.verdict(scores)
        entry = pipeline.compound(lesson, arms, scores, verdict,
                                  out / "ledger.jsonl")
        entry.update({
            "expected": lesson["prereg"]["expected"],
            "prereg_match": (verdict >= 7.0) == (lesson["prereg"]["expected"] == "PASS"),
            "event_id": event["event_id"],
            "distilled": distilled["principle"],
            "distill_matches_expected": distilled["matches_expected"],
            "gate_details": {"truth": d_truth, "understanding": d_under,
                             "effect": d_effect, "causality": d_causal,
                             "durability": d_dur, "transfer": d_trans},
            "arms": {a: {"passed": r["passed"], "reason": r["reason"],
                         "refusals": r["refusals"]}
                      for a, r in arms.items()},
            "real_transfer": real_transfer.get(lid),
            "integrity": {
                "adversarial_arm_refused": len(arms["adversarial"]["refusals"]) > 0,
                "adversarial_arm_passed": arms["adversarial"]["passed"],
                "intact": (len(arms["adversarial"]["refusals"]) > 0
                           and not arms["adversarial"]["passed"]),
            },
        })
        report["lessons"].append(entry)
        flag = "PROVEN" if verdict >= 7.0 else "FINDING"
        print(f"{lid}: verdict {verdict:.0f} [{flag}] "
              f"T{s_truth} U{s_under} E{s_effect} C{s_causal} "
              f"D{s_dur} X{s_trans}")

    proven = sum(1 for e in report["lessons"]
                 if not e["adversarial"] and e["proven"])
    rejected = sum(1 for e in report["lessons"]
                   if e["adversarial"] and e.get("rejected"))
    report["summary"] = {
        "good_lessons": 11, "proven": proven,
        "adversarial": 3, "correctly_rejected": rejected,
        "prereg_matches": sum(1 for e in report["lessons"]
                              if e.get("prereg_match")),
    }
    (out / "run_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False))
    print(f"\nSUMMARY: {proven}/11 proven, {rejected}/3 adversarial rejected, "
          f"{report['summary']['prereg_matches']}/14 prereg matches")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("seal"); s.set_defaults(f=cmd_seal)
    r = sub.add_parser("run"); r.add_argument("--out", required=True)
    r.add_argument("--real-transfer", default=None,
                   help="JSON file: {lesson_id: {passed: bool, ...}} from cold successors")
    r.set_defaults(f=cmd_run)
    args = p.parse_args(argv)
    return args.f(args)


if __name__ == "__main__":
    sys.exit(main())
