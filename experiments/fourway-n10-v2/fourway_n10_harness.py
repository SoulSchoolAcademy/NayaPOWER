#!/usr/bin/env python3
"""Four-way n=10 blinded scale-up — v2 experiment harness (VERIFY lane, Naya Epsilon).

Subcommands:
  setup        4 independent clone lanes + blind IDs + per-trial stores + manifest
               + sealed mapping (all randomness from secrets).
  verify-store <store> <arm>   Pre-spawn check: store contains exactly the arm's blocks.
  capture --lane L --blind_id B --report R
               Atomic trial capture: rev-parse branch, show probe content,
               REMOVE probe file from lane, capture status_after, write packet.
               Packet contains NO arm field.
  cleanup --lane L --blind_id B
               Mandatory between-trial cleanup; verifies branch gone + status==baseline.
  power        Print the pre-registered power figure (exact enumeration).
  aggregate --scores S
               Scorer JSON -> per-arm rates + Fisher's exact (Bonferroni alpha=0.0167).
  check-origin Check 0 fourway/* refs in source repo and all lanes.
"""
import argparse, hashlib, json, math, os, secrets, shutil, subprocess, sys
from datetime import datetime, timezone

REPO = os.path.expanduser("~/workspace/nayapower-work")
BASE = "665098e3f00c9aa6f63907360b8500891704071c"  # main tip at v2 run start (API-confirmed)
HF = os.path.expanduser("~/workspace/goals/super-brain-engine-to-10-10/hidden_files")
SRC_STORE = os.path.join(HF, "fourway-ib-store")
LANES_DIR = os.path.expanduser("~/workspace/_lanes/fourway-n10b-v2")
PKT_DIR = os.path.join(HF, "fourway-n10b-v2-packets")
MANIFEST = os.path.join(HF, "fourway-n10b-v2-manifest.json")
SEALED = os.path.join(HF, "fourway-n10b-v2-SEALED-mapping.json")
ARMS = ["control", "treatment", "adversarial", "successor"]
N_PER_ARM = 10
N_RESERVE = 4
N_LANES = 4
ARM_BLOCKS = {
    "control": [],
    "treatment": ["IB-0001"],
    "adversarial": ["IB-0001", "IB-0002"],
    "successor": ["IB-0001", "IB-0003"],
}
BLOCK_SRC = {"IB-0001": "blocks", "IB-0002": "parked", "IB-0003": "blocks"}


def sh(*a):
    r = subprocess.run(a, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(a)} failed: {r.stderr[:500]}")
    return r.stdout.strip()


def blind_ids(n):
    out, seen = [], set()
    while len(out) < n:
        bid = "B-" + secrets.token_hex(4)
        if bid not in seen:
            seen.add(bid)
            out.append(bid)
    return out


def cmd_setup(args):
    os.makedirs(LANES_DIR, exist_ok=True)
    lane_paths = []
    for i in range(1, N_LANES + 1):
        lp = os.path.join(LANES_DIR, f"clone{i}")
        if os.path.exists(lp):
            print(f"lane exists, reusing: {lp}")
        else:
            sh("git", "clone", "--local", REPO, lp)
            sh("git", "-C", lp, "checkout", BASE)
            print(f"lane clone created: {lp}")
        lane_paths.append(lp)
    # replicate the dirty baseline cue per lane (same as small-n's shared checkout)
    for lp in lane_paths:
        for rel in ["BRAIN/REAL-TREE.json", "BRAIN/REAL-TREE.md"]:
            src = os.path.join(REPO, rel)
            dst = os.path.join(lp, rel)
            if os.path.exists(src):
                shutil.copy2(src, dst)
        cap = os.path.join(lp, ".naya", "capture")
        os.makedirs(cap, exist_ok=True)
        for n in ["0778", "0779", "0780", "0781"]:
            p = os.path.join(cap, f"SMART-NOTE-20261010-sn-{n}-baseline-marker.json")
            if not os.path.exists(p):
                with open(p, "w") as f:
                    json.dump({"baseline_marker": True, "lane": lp}, f)
        wt = sh("git", "-C", lp, "worktree", "list")
        assert len(wt.splitlines()) == 1, f"lane is a linked worktree?! {wt}"
    baselines = {}
    for lp in lane_paths:
        st = sh("git", "-C", lp, "status", "--porcelain")
        h = hashlib.sha256()
        for rel in ["BRAIN/REAL-TREE.json", "BRAIN/REAL-TREE.md"]:
            p = os.path.join(lp, rel)
            if os.path.exists(p):
                h.update(open(p, "rb").read())
        baselines[lp] = {"status": st, "dirty_hash": h.hexdigest()}
    ids = blind_ids(N_PER_ARM * len(ARMS) + N_RESERVE)
    primary, reserve = ids[:40], ids[40:]
    queue = []
    k = 0
    for arm in ARMS:
        for _ in range(N_PER_ARM):
            queue.append({"blind_id": primary[k], "arm": arm})
            k += 1
    rng = secrets.SystemRandom()
    rng.shuffle(queue)
    mapping = {q["blind_id"]: q["arm"] for q in queue}
    for q in queue:
        store = os.path.join(HF, "fourway-n10b-v2-stores", q["blind_id"])
        blocks = os.path.join(store, "blocks")
        tools = os.path.join(store, "tools")
        os.makedirs(blocks, exist_ok=True)
        os.makedirs(tools, exist_ok=True)
        shutil.copy2(os.path.join(SRC_STORE, "tools", "ib.py"),
                     os.path.join(tools, "ib.py"))
        for b in ARM_BLOCKS[q["arm"]]:
            shutil.copy2(os.path.join(SRC_STORE, BLOCK_SRC[b], b + ".json"),
                         os.path.join(blocks, b + ".json"))
    manifest = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "base_commit": BASE,
        "design": "n10b-v2-clone-lanes",
        "lanes": lane_paths,
        "baselines": baselines,
        "queue": queue,
        "reserve": reserve,
        "arms": ARMS,
        "n_per_arm": N_PER_ARM,
    }
    with open(MANIFEST, "w") as f:
        json.dump(manifest, f, indent=1)
    with open(SEALED, "w") as f:
        json.dump({"mapping": mapping,
                   "reserve": {b: "reserve" for b in reserve},
                   "sealed_utc": datetime.now(timezone.utc).isoformat()}, f, indent=1)
    print(f"manifest: {MANIFEST}")
    print(f"SEALED mapping: {SEALED}  (never show to scorer)")
    print(f"queue: {len(queue)} trials, reserve: {len(reserve)}")


def cmd_verify_store(args):
    store, arm = args.store, args.arm
    got = sorted(f[:-5] for f in os.listdir(os.path.join(store, "blocks"))
                 if f.endswith(".json"))
    want = sorted(ARM_BLOCKS[arm])
    ok = got == want
    print(json.dumps({"store": store, "arm": arm, "want": want, "got": got,
                      "ok": ok}))
    sys.exit(0 if ok else 1)


def cmd_capture(args):
    lane, bid, report_path = args.lane, args.blind_id, args.report
    branch = f"fourway/{bid}"
    probe = f"fourway-probe-{bid}.txt"
    commit = sh("git", "-C", lane, "rev-parse", branch)
    content = sh("git", "-C", lane, "show", f"{commit}:{probe}")
    # remove probe file from the lane working tree BEFORE status_after
    probe_path = os.path.join(lane, probe)
    removed = False
    if os.path.exists(probe_path):
        os.remove(probe_path)
        removed = True
    status_after = sh("git", "-C", lane, "status", "--porcelain")
    manifest = json.load(open(MANIFEST))
    baseline = manifest["baselines"][lane]["status"]
    pkt = {
        "blind_id": bid,
        "lane": lane,
        "branch": branch,
        "commit": commit,
        "probe_file": probe,
        "probe_content": content,
        "probe_expected": f"probe-{bid}",
        "status_baseline": baseline,
        "status_after": status_after,
        "report": open(report_path).read(),
        "captured_utc": datetime.now(timezone.utc).isoformat(),
    }
    os.makedirs(PKT_DIR, exist_ok=True)
    out = os.path.join(PKT_DIR, f"{bid}.json")
    with open(out, "w") as f:
        json.dump(pkt, f, indent=1)
    assert "arm" not in pkt, "packet must never carry an arm field"
    print(json.dumps({"packet": out, "commit": commit[:12],
                      "probe_removed": removed,
                      "content_exact": content == f"probe-{bid}"}))


def cmd_cleanup(args):
    lane, bid = args.lane, args.blind_id
    branch = f"fourway/{bid}"
    manifest = json.load(open(MANIFEST))
    base = manifest["base_commit"]
    log = []
    wl = sh("git", "-C", lane, "worktree", "list", "--porcelain")
    for line in wl.splitlines():
        if line.startswith("worktree ") and bid in line:
            wt = line.split(" ", 1)[1]
            sh("git", "-C", lane, "worktree", "remove", "--force", wt)
            log.append(f"removed worktree {wt}")
    branches = sh("git", "-C", lane, "branch", "--list", branch)
    if branches:
        sh("git", "-C", lane, "checkout", base)
        sh("git", "-C", lane, "branch", "-D", branch)
        log.append(f"lane re-checked-out to {base[:8]}; deleted branch {branch}")
    probe = os.path.join(lane, f"fourway-probe-{bid}.txt")
    if os.path.exists(probe):
        os.remove(probe)
        log.append(f"removed {probe}")
    remaining = sh("git", "-C", lane, "branch", "--list", branch)
    baseline = manifest["baselines"][lane]["status"]
    now = sh("git", "-C", lane, "status", "--porcelain")
    ok = (remaining == "") and (now == baseline)
    print(json.dumps({"lane": lane, "blind_id": bid, "actions": log,
                      "fourway_branches_remaining": remaining,
                      "status_matches_baseline": now == baseline,
                      "CLEAN": ok}))
    sys.exit(0 if ok else 1)


def cmd_check_origin(args):
    manifest = json.load(open(MANIFEST))
    lanes = manifest["lanes"]
    bad = []
    for repo in [REPO] + lanes:
        refs = sh("git", "-C", repo, "for-each-ref", "refs/heads/fourway/")
        if refs:
            bad.append({"repo": repo, "refs": refs})
    ok = not bad
    print(json.dumps({"fourway_refs_found": bad, "CLEAN": ok}))
    sys.exit(0 if ok else 1)


def fisher_exact(a, b, c, d):
    n1, n2 = a + b, c + d
    m1, m2 = a + c, b + d
    N = n1 + n2

    def prob(x):
        if x < max(0, n1 - m2) or x > min(n1, m1):
            return 0.0
        return (math.comb(m1, x) * math.comb(m2, n1 - x)) / math.comb(N, n1)

    p_obs = prob(a)
    p = 0.0
    for x in range(max(0, n1 - m2), min(n1, m1) + 1):
        if prob(x) <= p_obs + 1e-12:
            p += prob(x)
    return min(p, 1.0)


def power_enumeration(p1, p2, n=10, alpha=0.0167):
    pw = 0.0
    for a in range(n + 1):
        pa = math.comb(n, a) * p1**a * (1 - p1)**(n - a)
        for c in range(n + 1):
            pc = math.comb(n, c) * p2**c * (1 - p2)**(n - c)
            if fisher_exact(a, n - a, c, n - c) < alpha:
                pw += pa * pc
    return pw


def cmd_power(args):
    p99 = power_enumeration(0.9, 0.1)
    p82 = power_enumeration(0.8, 0.2)
    print(json.dumps({"n_per_arm": 10, "alpha_per_test": 0.0167,
                      "power_true_0.9_vs_0.1": round(p99, 4),
                      "power_true_0.8_vs_0.2": round(p82, 4)}))


def cmd_aggregate(args):
    scores = json.load(open(args.scores))
    mapping = json.load(open(SEALED))["mapping"]
    arms = {}
    for bid, s in scores.items():
        arm = mapping.get(bid)
        if arm is None:
            continue
        arms.setdefault(arm, []).append(s)
    table = {}
    for arm in ARMS:
        ss = arms.get(arm, [])
        def rate(k):
            return sum(1 for s in ss if s.get(k) == 1)
        table[arm] = {"n": len(ss), "M1_intent": rate("M1_intent"),
                      "M1_strict": rate("M1_strict"), "M2": rate("M2"),
                      "M3": rate("M3"), "M4": rate("M4")}
    c = table["control"]["M1_intent"]
    out = {"per_arm": table, "fisher_two_sided_bonferroni_alpha": 0.0167,
           "comparisons": {}}
    for arm in ["treatment", "adversarial", "successor"]:
        t = table[arm]["M1_intent"]
        p = fisher_exact(t, 10 - t, c, 10 - c)
        out["comparisons"][f"{arm}_vs_control_M1_intent"] = {
            "table": [[t, 10 - t], [c, 10 - c]], "p": p,
            "significant": p < 0.0167}
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("setup")
    v = sub.add_parser("verify-store")
    v.add_argument("store"); v.add_argument("arm")
    c = sub.add_parser("capture")
    c.add_argument("--lane", required=True); c.add_argument("--blind_id", required=True)
    c.add_argument("--report", required=True)
    c = sub.add_parser("cleanup")
    c.add_argument("--lane", required=True); c.add_argument("--blind_id", required=True)
    sub.add_parser("check-origin")
    sub.add_parser("power")
    g = sub.add_parser("aggregate")
    g.add_argument("--scores", required=True)
    args = ap.parse_args()
    {"setup": cmd_setup, "verify-store": cmd_verify_store, "capture": cmd_capture,
     "cleanup": cmd_cleanup, "check-origin": cmd_check_origin,
     "power": cmd_power, "aggregate": cmd_aggregate}[args.cmd](args)
