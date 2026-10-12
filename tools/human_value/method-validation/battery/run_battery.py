#!/usr/bin/env python3
"""Known-answer method-validation battery for tools/human_value/instrument.py.

FIRST-PARTY (Naya Mu built the instrument; this battery is her own check):
each case is a synthetic scenario whose correct outcome is derived FIRST,
from the instrument's documented contract, and the instrument's output is
then compared against that known answer. A different seat re-verifies.

Cases KV-01..KV-17 cover: evidence verification + caps, verdict boundaries,
the harm gate, fail-safe input rejection, merge-base resolution at main tip /
branch head / missing origin (the #2404/#2417 fix), recheck durability +
content-drift, compare agreement semantics, to-event minting rules, and the
test-file evidence heuristic.

Run: python3 run_battery.py [--keep]
Exit 0 = every known answer matched. Exit 1 = at least one misfire.
Fixtures live under /tmp/mv-fixtures (rebuilt each run unless --keep).
Stdlib only.
"""

import json
import os
import shutil
import subprocess
import sys

WORKTREE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
INST = [sys.executable, os.path.join(WORKTREE, "tools", "human_value", "instrument.py")]
FIX = "/tmp/mv-fixtures"
KEEP = "--keep" in sys.argv

RESULTS = []


def sh(args, cwd=None, check=True, env=None):
    e = dict(os.environ)
    e["GIT_AUTHOR_NAME"] = e["GIT_COMMITTER_NAME"] = "Battery"
    e["GIT_AUTHOR_EMAIL"] = e["GIT_COMMITTER_EMAIL"] = "battery@example.invalid"
    if env:
        e.update(env)
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, env=e, timeout=60)
    if check and p.returncode != 0:
        raise RuntimeError(f"{' '.join(args[:4])} failed: {p.stderr[:500]}")
    return p


def git(repo, *args, check=True):
    return sh(["git", "-C", repo, *args], check=check)


def note(name, ok, detail):
    RESULTS.append((name, ok, detail))
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  <-- {detail}"))


# ---------------------------------------------------------------- fixtures

def build_fixtures():
    """Synthetic repo R with a known shape.

    A -- app.py(5 lines), docs/readme.md, contest_notes.md (trap: contains
         'test' mid-word, is NOT a test file), tests/test_app.py,
         receipts/change1.json (valid receipt)
    B -- modifies app.py, adds feature.py
    C -- modifies tests/test_app.py
    D -- branch from A: touches only docs/readme.md
    E -- on C: appends a line to app.py OUTSIDE lines 1-3 (drift probe)
    F -- on E: DELETES feature.py (rot probe)
    """
    if os.path.exists(FIX) and not KEEP:
        shutil.rmtree(FIX)
    if os.path.exists(FIX):
        return os.path.join(FIX, "R")
    os.makedirs(FIX)
    R = os.path.join(FIX, "R")
    sh(["git", "init", "-b", "main", R])
    git(R, "config", "commit.gpgsign", "false")

    def write(rel, text):
        p = os.path.join(R, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)

    app_v1 = 'def run():\n    return 1\n\n\ndef helper():\n    return 2\n'
    write("app.py", app_v1)
    write("docs/readme.md", "# readme\n\nHello.\n")
    write("contest_notes.md", "# notes\n\nA music contest. Nothing to do with tests.\n")
    write("tests/test_app.py", "def test_run():\n    assert True\n")
    write("receipts/change1.json", json.dumps({
        "receipt_version": 1, "change_id": "KV",
        "metrics": [{"name": "minutes saved", "before": 30, "after": 5, "unit": "min"}],
    }))
    git(R, "add", "-A")
    git(R, "commit", "-m", "A: baseline")
    A = git(R, "rev-parse", "HEAD").stdout.strip()

    write("app.py", app_v1 + "\ndef faster():\n    return 3\n")
    write("feature.py", "def feature():\n    return True\n")
    git(R, "add", "-A")
    git(R, "commit", "-m", "B: improve app, add feature")
    git(R, "checkout", "-b", "branch-d", A, check=True)
    write("docs/readme.md", "# readme\n\nHello, docs change.\n")
    git(R, "commit", "-am", "D: docs only")
    D = git(R, "rev-parse", "HEAD").stdout.strip()
    git(R, "checkout", "main", check=True)
    write("tests/test_app.py", "def test_run():\n    assert True\n\n\ndef test_faster():\n    assert True\n")
    git(R, "add", "-A")
    git(R, "commit", "-m", "C: extend tests")
    C = git(R, "rev-parse", "HEAD").stdout.strip()

    # E: append OUTSIDE cited lines 1-3 of app.py
    write("app.py", open(os.path.join(R, "app.py")).read() + "\n# trailing comment\n")
    git(R, "commit", "-am", "E: comment appended to app.py (outside lines 1-3)")
    E = git(R, "rev-parse", "HEAD").stdout.strip()

    # F: delete feature.py
    git(R, "rm", "feature.py", check=True)
    git(R, "commit", "-m", "F: remove feature.py")
    F = git(R, "rev-parse", "HEAD").stdout.strip()

    git(R, "checkout", "main", check=True)
    # origin/main -> A by default (branch-head scenario); cases re-point it.
    git(R, "update-ref", "refs/remotes/origin/main", A)
    return R


# ---------------------------------------------------------------- packet / card helpers

DIMS = ("USE", "DELTA", "PROOF", "DURABLE", "CLEAN")


def packet(change_id, sha, claims, evidence_by_dim, harm_found=False,
           harm_note="", grader="battery"):
    p = {
        "packet_version": 1,
        "change_id": change_id,
        "title": f"battery {change_id}",
        "merge_sha": sha,
        "grader": grader,
        "harm_check": {"found": harm_found, "note": harm_note},
        "judgments": [],
    }
    for dim in DIMS:
        p["judgments"].append({
            "dimension": dim,
            "score": claims.get(dim, 9),
            "rationale": f"battery claim for {dim}",
            "evidence": evidence_by_dim.get(dim, []),
        })
    return p


def file_ev(path, lines=None):
    e = {"kind": "file", "path": path}
    if lines:
        e["lines"] = lines
    return e


def grade(pkt, repo, ref):
    """Returns (exit_code, card_or_None, stderr)."""
    pp = os.path.join(FIX, "pkt.json")
    cp = os.path.join(FIX, "card.json")
    with open(pp, "w", encoding="utf-8") as f:
        json.dump(pkt, f)
    p = subprocess.run(
        INST + ["score", "--packet", pp, "--repo", repo, "--ref", ref, "--out", cp],
        capture_output=True, text=True, timeout=60)
    card = None
    if os.path.exists(cp):
        with open(cp, encoding="utf-8") as f:
            card = json.load(f)
        os.remove(cp)
    return p.returncode, card, p.stderr.strip()[:300]


def mechanical(repo, sha):
    code = (
        "import sys, json; sys.path.insert(0, %r);"
        "from tools.human_value import instrument;"
        "print(json.dumps(instrument.mechanical_signals(%r, %r)))" % (WORKTREE, repo, sha)
    )
    p = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=60)
    assert p.returncode == 0, p.stderr[:300]
    return json.loads(p.stdout)


# ---------------------------------------------------------------- cases

def main():
    R = build_fixtures()
    A = git(R, "rev-parse", "refs/remotes/origin/main").stdout.strip()  # = commit A
    C = git(R, "rev-parse", "main").stdout.strip()                      # tip incl. E,F? no: main tip is C
    D = git(R, "rev-parse", "branch-d").stdout.strip()
    F = git(R, "rev-parse", "main~0").stdout.strip()  # main tip is C still? recompute below
    # NOTE: commits E and F were made on detached/main? We committed on main
    # after C (we never checked out a new branch), so main tip is F.
    F = git(R, "rev-parse", "main").stdout.strip()
    C = git(R, "rev-parse", "main~2").stdout.strip()
    E = git(R, "rev-parse", "main~1").stdout.strip()

    fev = {"kind": "file", "path": "app.py"}
    tev = {"kind": "test", "path": "tests/test_app.py"}
    sev = {"kind": "sha", "sha": C}
    rev = {"kind": "receipt", "path": "receipts/change1.json"}
    att = [{"kind": "command"}, {"kind": "url"}]

    # KV-01: real value, fully verified evidence -> HIGH VALUE 9.0
    ev = {d: [fev, tev, sev] for d in DIMS}
    code, card, _ = grade(packet("KV-01", C, {}, ev), R, C)
    note("KV-01 verified-evidence high claims -> 9.0 HIGH VALUE",
         code == 0 and card["score"] == 9.0 and card["verdict"] == "HIGH VALUE",
         f"exit={code} score={card and card.get('score')} verdict={card and card.get('verdict')}")

    # KV-02: no evidence at all -> NO_EVIDENCE_CAP 3.0 -> NO VALUE
    ev = {d: [] for d in DIMS}
    code, card, _ = grade(packet("KV-02", C, {}, ev), R, C)
    ok = (code == 0 and card["score"] == 3.0 and card["verdict"] == "NO VALUE"
          and all("NO_EVIDENCE_CAP" in j["flags"] for j in card["judgments"]))
    note("KV-02 zero evidence -> 3.0 NO VALUE [NO_EVIDENCE_CAP]", ok,
         f"exit={code} score={card and card.get('score')} flags={[j['flags'] for j in card['judgments']] if card else None}")

    # KV-03: harm found -> DISQUALIFIED, no score
    ev = {d: [fev, tev, sev] for d in DIMS}
    code, card, _ = grade(packet("KV-03", C, {}, ev, harm_found=True,
                                 harm_note="deletes user data"), R, C)
    note("KV-03 harm gate -> DISQUALIFIED, score None",
         code == 0 and card["disqualified"] is True and card["score"] is None
         and card["verdict"] == "DISQUALIFIED",
         f"exit={code} card={card and (card.get('verdict'), card.get('score'))}")

    # KV-04: attested-only evidence (looks valuable, isn't) -> UNCITED_CAP 5.0 -> THIN
    ev = {d: att for d in DIMS}
    code, card, _ = grade(packet("KV-04", C, {}, ev), R, C)
    ok = (code == 0 and card["score"] == 5.0 and card["verdict"] == "THIN"
          and all("UNCITED_CAP" in j["flags"] for j in card["judgments"]))
    note("KV-04 attested-only -> 5.0 THIN [UNCITED_CAP]", ok,
         f"exit={code} score={card and card.get('score')}")

    # KV-05: receipt-only inflated DELTA claim -> RECEIPT_SOFT_CAP 8.0 -> 8.75 REAL VALUE
    ev = {d: [rev] if d == "DELTA" else [fev] for d in DIMS}
    claims = {d: 9 for d in DIMS}
    claims["DELTA"] = 10
    code, card, _ = grade(packet("KV-05", C, claims, ev), R, C)
    dlt = next(j for j in card["judgments"] if j["dimension"] == "DELTA") if card else {}
    # Contract: 9*.30 + 8*.25 + 9*.20 + 9*.15 + 9*.10, rounded to 1dp.
    # The instrument sums with built-in sum() (compensated summation on
    # this runtime -> 8.75 -> 8.8); the battery must use the same sum(),
    # a naive += chain lands on the other side of the .75 boundary (8.7).
    exp_total = round(sum([9 * 0.30, 8 * 0.25, 9 * 0.20, 9 * 0.15, 9 * 0.10]), 1)
    ok = (code == 0 and dlt.get("applied") == 8.0
          and "RECEIPT_SOFT_CAP" in dlt.get("flags", [])
          and card["score"] == exp_total and card["verdict"] == "REAL VALUE")
    note(f"KV-05 receipt-only DELTA=10 -> 8.0 [RECEIPT_SOFT_CAP], total {exp_total} REAL VALUE",
         ok, f"exit={code} delta={dlt} total={card and card.get('score')}")

    # KV-06: main tip (origin/main == ref) must NOT collapse; base = ref^1
    git(R, "update-ref", "refs/remotes/origin/main", C)
    m = mechanical(R, C)
    exp_files = git(R, "diff", "--name-only", f"{C}^1", C).stdout.split()
    ok = ("unavailable" not in m and m["files_changed"] == len(exp_files)
          and set(m["files"]) == set(exp_files) and m["files_changed"] > 0)
    note("KV-06 main-tip mechanical: no collapse, equals ref^1..ref",
         ok, f"files_changed={m.get('files_changed')} expected={len(exp_files)}")
    git(R, "update-ref", "refs/remotes/origin/main", A)  # restore

    # KV-07: branch head -> merge-base(origin/main)..head covers whole branch delta
    git(R, "checkout", "branch-d", check=True)
    # make branch-d a real 2-commit branch off A for this case? it has 1 commit D.
    m = mechanical(R, D)
    exp_files = git(R, "diff", "--name-only", A, D).stdout.split()
    ok = ("unavailable" not in m and set(m["files"]) == set(exp_files)
          and m["files_changed"] == len(exp_files))
    note("KV-07 branch-head mechanical: merge-base..head covers branch delta",
         ok, f"files={m.get('files')} expected={exp_files}")
    git(R, "checkout", "main", check=True)

    # KV-08: fail-safe — malformed packets exit 2, emit no score
    bads = {
        "bad-sha": dict(packet("KV-08a", C, {}, {d: [fev] for d in DIMS}), merge_sha="zzz"),
        "dup-dim": None, "score-11": None, "bool-score": None,
        "no-harm": None, "bad-kind": None, "bad-version": None,
    }
    p = packet("KV-08b", C, {}, {d: [fev] for d in DIMS})
    p["judgments"] = [j for j in p["judgments"] if j["dimension"] != "USE"]
    bads["missing-dim"] = p
    p = packet("KV-08c", C, {}, {d: [fev] for d in DIMS})
    p["judgments"].append({"dimension": "USE", "score": 9, "evidence": []})
    bads["dup-dim"] = p
    p = packet("KV-08d", C, {"USE": 11}, {d: [fev] for d in DIMS})
    bads["score-11"] = p
    p = packet("KV-08e", C, {}, {d: [fev] for d in DIMS})
    p["judgments"][0]["score"] = True
    bads["bool-score"] = p
    p = packet("KV-08f", C, {}, {d: [fev] for d in DIMS})
    del p["harm_check"]
    bads["no-harm"] = p
    p = packet("KV-08g", C, {}, {d: [fev] for d in DIMS})
    p["judgments"][0]["evidence"] = [{"kind": "vibes"}]
    bads["bad-kind"] = p
    p = packet("KV-08h", C, {}, {d: [fev] for d in DIMS})
    p["packet_version"] = 2
    bads["bad-version"] = p
    allfail = True
    detail = []
    for name, pkt in bads.items():
        code, card, err = grade(pkt, R, C)
        if not (code == 2 and card is None):
            allfail = False
            detail.append(f"{name}: exit={code} card={'set' if card else 'none'}")
    note("KV-08 malformed packets -> exit 2, no score (8 variants)", allfail,
         "; ".join(detail) if detail else "all 8 rejected")

    # KV-09: verdict boundaries
    for claims, exp_score, exp_verdict in [
        ({d: 7 for d in DIMS}, 7.0, "REAL VALUE"),
        ({d: 9 for d in DIMS}, 9.0, "HIGH VALUE"),
        ({d: 5 for d in DIMS}, 5.0, "THIN"),
        ({d: 4 for d in DIMS}, 4.0, "NO VALUE"),
    ]:
        ev = {d: [fev] for d in DIMS}
        code, card, _ = grade(packet("KV-09", C, claims, ev), R, C)
        ok = code == 0 and card["score"] == exp_score and card["verdict"] == exp_verdict
        note(f"KV-09 boundary all-{claims['USE']} -> {exp_score} {exp_verdict}", ok,
             f"exit={code} score={card and card.get('score')} verdict={card and card.get('verdict')}")

    # KV-10: cited file missing at ref (breakage) -> UNVERIFIABLE -> UNCITED_CAP
    ev = {d: [{"kind": "file", "path": "missing.py"}] for d in DIMS}
    code, card, _ = grade(packet("KV-10", C, {}, ev), R, C)
    ok = (code == 0 and card["score"] == 5.0 and card["verdict"] == "THIN"
          and all("UNCITED_CAP" in j["flags"] for j in card["judgments"]))
    note("KV-10 missing cited file -> 5.0 THIN [UNCITED_CAP]", ok,
         f"exit={code} score={card and card.get('score')}")

    # KV-11: recheck content-drift honors cited LINES, not the whole file
    ev = {d: [file_ev("app.py", "1-3")] for d in DIMS}
    code, card, _ = grade(packet("KV-11", C, {}, ev), R, C)
    assert code == 0
    cp = os.path.join(FIX, "kv11-card.json")
    with open(cp, "w", encoding="utf-8") as f:
        json.dump(card, f)
    rp = os.path.join(FIX, "kv11-recheck.json")
    p = subprocess.run(
        INST + ["recheck", "--scorecard", cp, "--repo", R, "--ref", E, "--out", rp],
        capture_output=True, text=True, timeout=60)
    rep = json.load(open(rp)) if os.path.exists(rp) else None
    items = [i for i in rep["items"] if i["dimension"] == "USE"] if rep else []
    ok = (p.returncode == 0 and rep is not None and items
          and items[0]["recheck"] == "HELD"
          and items[0].get("content_drift") == "UNCHANGED")
    note("KV-11 recheck: cited lines 1-3 unchanged at E -> UNCHANGED (not whole-file CHANGED)",
         ok, f"exit={p.returncode} drift={[i.get('content_drift') for i in items]}")

    # KV-12: compare — identical cards TRUST; change_id mismatch rejected
    code, cardA, _ = grade(packet("KV-12", C, {}, {d: [fev] for d in DIMS}), R, C)
    code, cardB, _ = grade(packet("KV-12", C, {}, {d: [fev] for d in DIMS},
                                  grader="battery-2"), R, C)
    ap, bp = os.path.join(FIX, "a.json"), os.path.join(FIX, "b.json")
    json.dump(cardA, open(ap, "w")); json.dump(cardB, open(bp, "w"))
    op = os.path.join(FIX, "cmp.json")
    p = subprocess.run(INST + ["compare", "--a", ap, "--b", bp, "--out", op],
                       capture_output=True, text=True, timeout=60)
    rep = json.load(open(op)) if os.path.exists(op) else None
    ok = (p.returncode == 0 and rep and rep["standing"] == "TRUST"
          and rep["verdict_match"] and rep["n_agree"] == 5)
    note("KV-12a compare identical cards -> TRUST, 5/5 agree", ok,
         f"exit={p.returncode} standing={rep and rep.get('standing')}")
    cardC = dict(cardB); cardC["change_id"] = "KV-12-OTHER"
    json.dump(cardC, open(bp, "w"))
    p = subprocess.run(INST + ["compare", "--a", ap, "--b", bp],
                       capture_output=True, text=True, timeout=60)
    note("KV-12b compare mismatched change_id -> rejected (exit 2)",
         p.returncode == 2, f"exit={p.returncode} err={p.stderr.strip()[:120]}")

    # KV-12c: compare disagreeing cards -> DISPUTE standing, visible not averaged
    code, cardLo, _ = grade(packet("KV-12", C, {d: 4 for d in DIMS},
                                   {d: [fev] for d in DIMS}), R, C)
    json.dump(cardLo, open(bp, "w"))
    p = subprocess.run(INST + ["compare", "--a", ap, "--b", bp, "--out", op],
                       capture_output=True, text=True, timeout=60)
    rep = json.load(open(op)) if os.path.exists(op) else None
    ok = (p.returncode == 0 and rep and rep["standing"] == "DISPUTE"
          and not rep["verdict_match"] and rep["score_gap"] == 5.0)
    note("KV-12c compare 9-vs-4 cards -> DISPUTE, verdict mismatch, gap 5.0", ok,
         f"exit={p.returncode} standing={rep and rep.get('standing')} gap={rep and rep.get('score_gap')}")

    # KV-13: test-heuristic trap — contest_notes.md is NOT a test file
    ev = {d: [fev] for d in DIMS}
    ev["USE"] = [{"kind": "test", "path": "contest_notes.md"}]
    code, card, _ = grade(packet("KV-13", C, {}, ev), R, C)
    use = next((j for j in card["judgments"] if j["dimension"] == "USE"), {}) if card else {}
    led = [i for i in card.get("evidence_ledger", []) if i["dimension"] == "USE"] if card else []
    ok = (code == 0 and use.get("applied") == 5.0
          and "UNCITED_CAP" in use.get("flags", [])
          and led and led[0]["status"] == "UNVERIFIABLE")
    note("KV-13 test-citation of non-test file -> UNVERIFIABLE, USE capped 5.0",
         ok, f"exit={code} use={use} ledger={led and led[0]['status']}")

    # KV-14: no origin/main -> documented ^1 fallback (last-commit delta only)
    git(R, "update-ref", "-d", "refs/remotes/origin/main", check=True)
    m = mechanical(R, C)
    exp_files = git(R, "diff", "--name-only", f"{C}^1", C).stdout.split()
    ok = ("unavailable" not in m and set(m["files"]) == set(exp_files))
    note("KV-14 no origin/main -> ^1 fallback (documented understatement)",
         ok, f"files={m.get('files')} expected={exp_files}")
    git(R, "update-ref", "refs/remotes/origin/main", A)

    # KV-15: recheck rot — cited file deleted at F -> ROTTED
    ev = {d: [{"kind": "file", "path": "feature.py"}] for d in DIMS}
    code, card, _ = grade(packet("KV-15", C, {}, ev), R, C)
    cp = os.path.join(FIX, "kv15-card.json")
    json.dump(card, open(cp, "w"))
    rp = os.path.join(FIX, "kv15-recheck.json")
    p = subprocess.run(
        INST + ["recheck", "--scorecard", cp, "--repo", R, "--ref", F, "--out", rp],
        capture_output=True, text=True, timeout=60)
    rep = json.load(open(rp)) if os.path.exists(rp) else None
    ok = (p.returncode == 0 and rep and rep["per_dimension"]["USE"] == "ROTTED"
          and rep["rotted"] == 5)
    note("KV-15 recheck after file deletion -> ROTTED on all dims", ok,
         f"exit={p.returncode} per_dim={rep and rep.get('per_dimension')} rotted={rep and rep.get('rotted')}")

    # KV-16: to-event mints only REAL VALUE+
    code, cardHi, _ = grade(packet("KV-16-HI", C, {d: 8 for d in DIMS},
                                   {d: [fev] for d in DIMS}), R, C)
    hp = os.path.join(FIX, "hi.json"); json.dump(cardHi, open(hp, "w"))
    ep = os.path.join(FIX, "event.json")
    p = subprocess.run(
        INST + ["to-event", "--scorecard", hp, "--out", ep,
                "--date", "2026-10-12", "--receipt-ref", "receipts/change1.json",
                "--pr-url", "https://example.invalid/pr/1"],
        capture_output=True, text=True, timeout=60)
    evt = json.load(open(ep)) if os.path.exists(ep) else None
    ok = (p.returncode == 0 and evt and evt["event_id"] == "HV-20261012-KV-16-HI"
          and evt["delta_v_actual"] == 6.0)
    note("KV-16a to-event REAL VALUE -> schema-valid event, delta_v_actual=6.0",
         ok, f"exit={p.returncode} eid={evt and evt.get('event_id')} dv={evt and evt.get('delta_v_actual')}")
    code, cardLo, _ = grade(packet("KV-16-LO", C, {d: 4 for d in DIMS},
                                   {d: [fev] for d in DIMS}), R, C)
    lp = os.path.join(FIX, "lo.json"); json.dump(cardLo, open(lp, "w"))
    p = subprocess.run(
        INST + ["to-event", "--scorecard", lp, "--out", os.path.join(FIX, "event2.json"),
                "--date", "2026-10-12", "--receipt-ref", "x"],
        capture_output=True, text=True, timeout=60)
    note("KV-16b to-event NO VALUE -> refused (exit 2, mints nothing)",
         p.returncode == 2, f"exit={p.returncode} err={p.stderr.strip()[:120]}")

    # KV-17: pilot skeleton -> scoring a skeleton fails closed (incomplete packet)
    sp = os.path.join(FIX, "skel.json")
    p = subprocess.run(INST + ["pilot", "--merge", C, "--repo", R, "--out", sp],
                       capture_output=True, text=True, timeout=60)
    skel = json.load(open(sp)) if os.path.exists(sp) else None
    skel_ok = (p.returncode == 0 and skel and skel["change_id"] == "PR-?"
               and all(j["score"] is None for j in skel["judgments"]))
    code, card, _ = grade(skel, R, C)
    note("KV-17a pilot skeleton built with null scores", skel_ok,
         f"exit={p.returncode} change_id={skel and skel.get('change_id')}")
    note("KV-17b scoring a skeleton -> exit 2, no score", code == 2 and card is None,
         f"exit={code}")

    # KV-18: the method's trust boundary — verified citations, hollow judgment.
    # Branch D is a docs-only tweak. The grader claims 9s with REAL, verified
    # file evidence. The instrument verifies CITATIONS, not the truth of the
    # judgment: it MUST pass this through at 9.0 HIGH VALUE. Known answer:
    # the instrument is a citation-and-cap machine; grader honesty is the
    # human trust anchor (compare command exists for second-seat checks).
    ev = {d: [file_ev("docs/readme.md")] for d in DIMS}
    code, card, _ = grade(packet("KV-18", D, {}, ev), R, D)
    ok = (code == 0 and card["score"] == 9.0 and card["verdict"] == "HIGH VALUE")
    note("KV-18 trust boundary: verified citations + hollow 9s -> 9.0 HIGH VALUE "
         "(instrument cannot judge the judgment)", ok,
         f"exit={code} score={card and card.get('score')} — documented boundary, not a misfire")

    # ---- summary
    fails = [r for r in RESULTS if not r[1]]
    passed = len(RESULTS) - len(fails)
    print(f"\n{passed}/{len(RESULTS)} cases passed.")
    if fails:
        print("MISFIRES:")
        for name, ok, detail in fails:
            print(f"  - {name}: {detail}")
    summary = {"passed": len(RESULTS) - len(fails), "total": len(RESULTS),
               "results": [{"case": n, "ok": o, "detail": d} for n, o, d in RESULTS]}
    with open(os.path.join(WORKTREE, "tools", "human_value", "method-validation",
                           "battery", "last-run.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
