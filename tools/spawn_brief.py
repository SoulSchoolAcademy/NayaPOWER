#!/usr/bin/env python3
"""spawn_brief.py — machine-generated, schema-validated worker spawn brief.

Shawn's law (2026-10-14): teach them HOW TO THINK, then give them work.
A brief is a thinking lesson with a work list attached — not a task order.

Structure of every brief:
  1. HOW TO THINK — the decision framework for THIS work (from dispatcher),
     then the relevant principles. Thinking first, always.
  2. WORK LIST — ranked items sized to the time box. The worker works
     top-down, each item done RIGHT or skipped honestly. Finishing 3 of 8
     perfectly is success. Finishing 0, or 8 sloppily, is failure.
  3. RECEIPT — sign-in/out format. The receipt is the shared memory:
     what got done, what's still open, what the next worker inherits.

Reads LIVE STATE only (local files + git protocol, zero API calls) and
emits a complete spawn message to stdout.

Fail-closed on tool drift: the briefing_proof.py CLI interface is validated
against its own --help output before every run. Any drift -> non-zero exit,
zero stdout. A brief with unvalidated tool syntax is never emitted.

Usage:
    spawn_brief.py --seat "Naya X" --lane N --area "AREA" \\
        --time-box "~10 min" \\
        --thinking "How to think about this work: ..." \\
        --area-list ~/workspace/goals/super-brain-engine-to-10-10/hidden_files/areas/top10/AREA.json

area-list JSON: {"area": "...", "seat": "...", "updated_utc": "...",
  "last_recommendation": "<standing rec for the next worker — the generator
   checks it names no done/closed item before quoting (w250 stale-rec guard)>",
  "items": [{"n": 1, "item": "...", "why": "...", "est": "~3 min",
             "status": "open", "note": "..."}, ...]}
Only items with status "open" are listed, in rank order, keeping their
stable numbers — so "I did 1-5, 6-10 left" maps cleanly across waves.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

HOME = os.path.expanduser("~")
GOAL = os.path.join(HOME, "workspace/goals/hyper-speed-learning-mastery/hidden_files")
SBRAIN = os.path.join(HOME, "workspace/goals/super-brain-engine-to-10-10/hidden_files")
INJECT_PY = os.path.join(GOAL, "inject.py")
MD_CURRENT = os.path.join(SBRAIN, "master-directive-current.md")
LANE_STATE_PY = os.path.join(SBRAIN, "lane-state.py")
REPO = "https://github.com/SoulSchoolAcademy/NayaPOWER.git"
UNKNOWN = "UNKNOWN"

# Env override exists so the fail-closed test can point at a tampered copy
# of briefing_proof.py without touching the real tool.
PROOF_BIN = os.environ.get("SPAWN_BRIEF_PROOF_BIN",
                            os.path.join(HOME, "workspace/bin/briefing_proof.py"))


def die(msg, code=2):
    sys.stderr.write("FATAL: %s\n" % msg)
    sys.exit(code)


def run(cmd, timeout=30):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def validate_proof_interface():
    """Fail closed unless briefing_proof.py exposes exactly the expected CLI.

    Flags are matched as whole tokens (--challenge must not match
    --challenge-broken); a rename that merely extends the flag name is
    still drift and must fail closed.
    """
    expected = {
        "challenge": ["--count"],
        "answer": ["--challenge", "challenge JSON file"],
        "verify": ["--answer"],
        "record": ["--answer", "--who", "--lane"],
    }
    for sub, markers in expected.items():
        r = run([sys.executable, PROOF_BIN, sub, "--help"], timeout=15)
        if r.returncode != 0:
            die("briefing_proof.py %s --help failed (rc=%d): %s"
                % (sub, r.returncode, r.stderr.strip()[:200]))
        for m in markers:
            if m.startswith("--"):
                ok = re.search(re.escape(m) + r"(?=\s|$)", r.stdout)
            else:
                ok = m in r.stdout
            if not ok:
                die("briefing_proof.py interface drift: '%s' missing from '%s --help'"
                    % (m, sub))


def section(text, header):
    """Extract the body of a '## N. HEADER ...' section."""
    m = re.search(r"^##\s+\d+\.\s+" + re.escape(header) + r"\b.*$",
                  text, re.M)
    if not m:
        return ""
    start = m.end()
    nxt = re.search(r"^##\s+\d+\.\s+", text[start:], re.M)
    end = start + nxt.start() if nxt else len(text)
    return text[start:end].strip()


def numbered_items(sec_body, n=3, limit=140):
    items = []
    for line in sec_body.split("\n"):
        m = re.match(r"^\s*\d+\.\s+(.+)$", line)
        if m:
            s = m.group(1).strip()
            if len(s) > limit:
                s = s[:limit].rstrip() + "..."
            items.append(s)
        if len(items) >= n:
            break
    while len(items) < n:
        items.append(UNKNOWN)
    return items


def parse_directive(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    gm = re.search(r"^generated_utc:\s*(.+?)\s*$", text, re.M)
    tm = re.search(r"^tip:\s*([0-9a-f]{40})", text, re.M)
    generated = gm.group(1).strip() if gm else UNKNOWN
    tip = tm.group(1) if tm else UNKNOWN

    s1 = section(text, "MISSION")
    ns = re.search(r"\*\*North Star:\*\*\s*(.+)", s1)
    ob = re.search(r"\*\*Objective:\*\*\s*(.+)", s1)
    mission = (ns.group(1).strip() + " " + ob.group(1).strip()) if (ns and ob) else UNKNOWN
    mission = re.sub(r"\s+", " ", mission)
    if len(mission) > 300:
        mission = mission[:300].rstrip() + "..."

    prios = numbered_items(section(text, "NEXT ACTIONS"))
    blockers = numbered_items(section(text, "BLOCKERS"))
    return {"generated": generated, "tip": tip, "mission": mission,
            "prios": prios, "blockers": blockers}


def directive_age_min(generated):
    try:
        dt = datetime.strptime(generated, "%Y-%m-%d %H:%M:%S UTC").replace(tzinfo=timezone.utc)
        return int((datetime.now(timezone.utc) - dt).total_seconds() // 60)
    except Exception:
        return None


def load_area_list(path):
    try:
        raw = open(path, encoding="utf-8").read()
        doc = json.loads(raw)
    except (OSError, json.JSONDecodeError) as e:
        die("cannot read area-list %s: %s" % (path, e))
    items = doc.get("items") if isinstance(doc, dict) else None
    if not isinstance(items, list) or not items:
        die("area-list %s must hold a non-empty 'items' array" % path)
    clean = []
    for it in items:
        if not isinstance(it, dict) or "item" not in it:
            die("area-list entry missing 'item' key in %s" % path)
        if str(it.get("status", "open")).strip().lower() != "open":
            continue
        clean.append({
            "n": it.get("n", "?"),
            "item": str(it["item"]).strip(),
            "why": str(it.get("why", "")).strip(),
            "est": str(it.get("est", "")).strip(),
        })
    if not clean:
        die("area-list %s has no open items" % path)
    return clean, doc


def recommendation_block(doc, thinking):
    """STANDING RECOMMENDATION channel (Theta w250 stale-rec guard).

    The generator — not the dispatcher — owns quoting last_recommendation,
    and it checks item status/closed_utc BEFORE quoting. A recommendation
    that names a done/closed item id is STALE and is never quoted; the brief
    says so out loud so the list's last_recommendation gets refreshed.
    The dispatcher's --thinking is also scanned: if it hand-quotes a closed
    item id (the actual w250 failure shape), the brief carries a WARNING.

    Fail-open: any unexpected shape yields a quiet '(unavailable)' line —
    this block must never kill a dispatch. Staleness itself is LOUD.

    Two tiers (Theta w255): TIER 1 — STALE verdict, item n-id substring match
    (ids >= 6 chars; shorter ids match too noisily). TIER 2 — REVIEW note, a
    recommendation that references closed work by PR number (#NNNN) or
    distinctive prose alone (the actual w250 failure shape: "C3-closure
    unrouted ~6.5h" named no item id). REVIEW is NOT a verdict: a PR number
    alone never fires it (one PR can anchor live work — #2635 proved it);
    prose fires only on >=2 distinctive tokens, or PR + >=1 token, shared
    with a closed item and with no open item carrying the same reference.
    The guard names the overlap; the list maintainer confirms whether the
    premise is live. Fail-open and the STALE path are byte-identical.
    """
    lines = []
    try:
        items = doc.get("items") if isinstance(doc, dict) else []
        if not isinstance(items, list):
            items = []
        area = doc.get("area", "?") if isinstance(doc, dict) else "?"
        rec = doc.get("last_recommendation") if isinstance(doc, dict) else None
        rec = str(rec).strip() if rec else ""
        closed = {}  # lowercased n-id -> closed_utc (or 'status=done')
        closed_blob = {}  # lowercased n-id -> combined n/title/item text (PR+prose index)
        open_blobs = []  # combined text of every OPEN item (fresh-anchor suppression)
        for it in items:
            if not isinstance(it, dict):
                continue
            nid = str(it.get("n", "")).strip()
            if not nid or len(nid) < 6:
                continue
            blob = " ".join(str(it.get(k, "") or "") for k in ("n", "title", "item"))
            st = str(it.get("status", "open")).strip().lower()
            cu = it.get("closed_utc")
            if st == "done" or cu:
                closed[nid.lower()] = cu or "status=done"
                closed_blob[nid.lower()] = blob
            else:
                open_blobs.append(blob)

        def refs_done(text):
            t = (text or "").lower()
            return [nid for nid in closed if nid in t]

        # TIER 2 (Theta w255): PR-number + prose reference index. Distinctive
        # tokens are >=6 chars, hyphenated compounds kept whole, generic
        # machinery words stopworded (extend the set when a REVIEW misfires).
        _PR = re.compile(r"#(\d{3,})")
        _TOK = re.compile(r"[a-z0-9][a-z0-9\-]*[a-z0-9]")
        _STOP = frozenset(
            "re-run rerun consensus review reviews receipt verdict verdicts scorecard "
            "merge gate gates check checks status closed closes watch theta naya narzan "
            "stale fresh live wave waves lane lanes seat owner owners item items list "
            "work works continues landed stands event events comment comments issue "
            "issues pull branch commit head dispatch worker mission brief briefing "
            "recommendation recommendations refresh refreshed board feed area fix "
            "content verify".split())

        def _toks(text):
            return {m for m in (m.group(0) for m in _TOK.finditer((text or "").lower()))
                    if len(m) >= 6 and m not in _STOP}

        def refs_done_review(text):
            """[(nid, evidence)] — closed items the text references by PR number
            or distinctive prose without naming the item id. REVIEW tier: names
            the overlap; the maintainer confirms. A PR number alone never fires;
            prose fires on >=2 distinctive tokens, or PR + >=1 token, shared
            with a closed item and no open item carrying the same reference."""
            t = (text or "").lower()
            rec_prs = set(_PR.findall(t))
            rec_tok = _toks(t)
            open_prs, open_tok = set(), set()
            for b in open_blobs:
                bl = b.lower()
                open_prs |= set(_PR.findall(bl))
                open_tok |= _toks(bl)
            out = []
            for nid, blob in closed_blob.items():
                if nid in t:
                    continue  # id match is the STALE tier's job, not ours
                bl = blob.lower()
                pr_hit = [p for p in rec_prs
                          if p in set(_PR.findall(bl)) and p not in open_prs]
                prose = sorted((_toks(bl) & rec_tok) - open_tok)
                if len(prose) >= 2 or (pr_hit and prose):
                    ev = []
                    if pr_hit:
                        ev.append("PR #%s" % pr_hit[0])
                    ev.append("prose: %s" % ", ".join(prose[:4]))
                    out.append((nid, "; ".join(ev)))
            return out[:3]

        if rec:
            hits = refs_done(rec)
            if hits:
                lines.append("STANDING RECOMMENDATION — STALE, NOT QUOTED:")
                for nid in hits:
                    lines.append("  quotes item '%s' (closed: %s) — refresh last_recommendation on the %s list before any brief quotes it."
                                 % (nid, closed[nid], area))
            else:
                rev = refs_done_review(rec)
                if rev:
                    lines.append("STANDING RECOMMENDATION (id-freshness-checked — prose/PR overlap needs a maintainer read):")
                else:
                    lines.append("STANDING RECOMMENDATION (freshness-checked — names no closed item):")
                lines.append("  " + rec)
                for nid, ev in rev:
                    lines.append("  REVIEW: references possibly-closed work (%s) — closed item '%s' (%s); maintainer confirm the premise is live."
                                 % (ev, nid, closed[nid]))
        else:
            lines.append("(no standing recommendation on the area list)")
        th = refs_done(thinking)
        if th:
            lines.append("WARNING: --thinking references closed item(s) %s — verify the premise is live before acting."
                         % ", ".join("'%s'" % n for n in th))
        else:
            for nid, ev in refs_done_review(thinking):
                lines.append("NOTE: --thinking references possibly-closed work (%s) — closed item '%s' (%s); verify the premise is live."
                             % (ev, nid, closed[nid]))
    except Exception:
        lines.append("(standing-recommendation check unavailable — not blocking)")
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seat", required=True)
    ap.add_argument("--lane", required=True)
    ap.add_argument("--area", required=True)
    ap.add_argument("--time-box", required=True,
                    help="e.g. '~10 min' — the real time available")
    ap.add_argument("--thinking", required=True,
                    help="2-4 sentences: how to think about THIS work")
    ap.add_argument("--area-list", required=True,
                    help="path to the area's standing top-10 JSON")
    a = ap.parse_args()

    # ---- STEP 0: validate tool interface BEFORE emitting anything ----
    validate_proof_interface()

    work = load_area_list(a.area_list)
    work, area_doc = work
    area_list_path = a.area_list

    out = []
    W = out.append
    seat, lane, area = a.seat, a.lane, a.area
    seat_tag = re.sub(r"\s+", "_", seat.strip())

    W("You are %s — lane %s." % (seat, lane))
    W("")

    # ---- 0. YOUR DIRECT LINKS (Shawn's Direct Link Law, 2026-10-15):
    # never a scavenger hunt — every place you need, one click away.
    lane_issue = {"1": "1713", "2": "1714", "3": "1715", "4": "2471",
                  "5": "2472"}.get(str(lane).strip())
    W("YOUR DIRECT LINKS — click, don't hunt:")
    if lane_issue:
        W("- Your lane feed: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/%s"
          % lane_issue)
    W("- Live team board: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2641 (live since 17:19Z, successor to #2537)")
    W("- Master directive: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2601")
    W("- Feed index: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1599")
    W("- Repo (main): https://github.com/SoulSchoolAcademy/NayaPOWER/tree/main")
    W("When you cite anything — a receipt, a PR, a commit, a file — send the")
    W("direct clickable link with a clear label. Never a bare path, never a")
    W("bare URL in text, never 'go find it'. Links, not scavenger hunts.")
    W("")

    # ---- 0b. ACTIVATION PACKAGE (Shawn, 2026-10-15 — the declaration rule:
    # every dispatched agent gets the activation package with direct links.
    # She declares, then she behaves as an elite Naya.)
    W("ACTIVATION — declare before you work. You are a Naya: a mind with")
    W("access to intelligence, not intelligence itself.")
    W("The full packet (read it):")
    W("https://github.com/SoulSchoolAcademy/NayaPOWER/blob/naya5/activation-system/BRAIN/00-ACTIVATION/ACTIVATION-PACKET.md")
    W("Read first, then declare:")
    W("- The Oath (human): https://github.com/SoulSchoolAcademy/NayaPOWER/blob/naya2/oath-manifesto-0021-0022/BRAIN/01-GOVERNANCE/0021-NAYA-OATH-V1.human.md")
    W("- The Manifesto: https://github.com/SoulSchoolAcademy/NayaPOWER/blob/naya2/oath-manifesto-0021-0022/BRAIN/01-GOVERNANCE/0022-NAYA-MANIFESTO-V1.human.md")
    W("- The Creed: https://github.com/SoulSchoolAcademy/NayaPOWER/blob/naya5/activation-system/BRAIN/00-ACTIVATION/instant-activation/THE-CREED.md")
    W("- Field-manual index: https://github.com/SoulSchoolAcademy/NayaPOWER/blob/naya2/resolve-field-manuals-13-24/BRAIN/90-OPERATIONS/field-manuals/README.md")
    W("The 8 laws you carry: (1) most intelligent thing, always; (2) show")
    W("with smart links, don't tell; (3) score instead of guessing;")
    W("(4) receipts, never 'trust me'; (5) a lesson counts only when a future")
    W("decision changes; (6) fix what's broken, don't describe it;")
    W("(7) authority is math and logic; (8) protect Shawn's attention.")
    W("The process: understand (mission, then task) -> deliberate (math,")
    W("logic, relevance) -> pre-mortem -> build/score/fix (ten things to make")
    W("it 10x better, write the solution, apply, rescore) -> ship at 9+ ->")
    W("prove with receipts.")
    W("DECLARE on the live board under your own name: 'I am [Name], [Lane]")
    W("seat. Oath read: [first 8 of sha256]. Manifesto read: [first 8]. Creed")
    W("declared as myself. I carry the 8 laws. My drift line: [one honest")
    W("line]. Tag — I'm it.' No declaration with hash proofs = not activated.")
    W("")

    # ---- 1. HOW TO THINK (first — the thinking lesson, then the work) ----
    W("HOW TO THINK ABOUT THIS WORK:")
    W(a.thinking.strip())
    W("")
    r = run([sys.executable, INJECT_PY, "--brief", " ".join(w["item"] for w in work[:3]),
             "--area", area], timeout=30)
    if r.returncode == 0 and r.stdout.strip():
        W(r.stdout.strip())
    else:
        W("(principle injection skipped — injector unavailable; not blocking)")
    W("")

    # ---- 1b. STANDING RECOMMENDATION (Theta w250 guard — the generator
    # checks status/closed_utc BEFORE quoting last_recommendation) ----
    for _line in recommendation_block(area_doc, a.thinking):
        W(_line)
    W("")

    # ---- 2. WORK LIST (ranked, time-boxed, partial completion is normal) ----
    W("YOUR TIME BOX: %s" % a.time_box)
    W("YOUR AREA'S LIST — %s, most valuable first. Work top-down:"
      % os.path.basename(area_list_path))
    for w in work:
        line = "%s. %s" % (w["n"], w["item"])
        bits = []
        if w["why"]:
            bits.append(w["why"])
        if w["est"]:
            bits.append(w["est"])
        if bits:
            line += " — " + " | ".join(bits)
        W(line)
    W("")
    W("EXPECTATION: you will probably not finish all %d open items. That is"
      % len(work))
    W("normal, not failure. What matters: every item you touch is done RIGHT")
    W("and completely, or you skip it honestly. Three done perfectly beats")
    W("eight done sloppily.")
    W("")
    W("TAG-OFF (your sign-out hands this list to the next worker):")
    W("say which numbers you completed (with one-line verdicts each), which")
    W("numbers are still open (with their current state), anything new you")
    W("discovered that belongs on the list, and your RECOMMENDATION — what")
    W("the next worker should hit first and why. The list belongs to the")
    W("area, not to you; leave it sharper than you found it.")
    W("")

    # ---- 3. Master Directive injection ----
    if os.path.exists(MD_CURRENT):
        d = parse_directive(MD_CURRENT)
        W("MASTER DIRECTIVE — compiled %s, tip %s" % (d["generated"], d["tip"]))
        W("MISSION: %s" % d["mission"])
        W("NOW (top 3): %s" % " / ".join(d["prios"]))
        W("BLOCKED (top 3): %s" % " / ".join(d["blockers"]))
        age = directive_age_min(d["generated"])
        age_str = "%dmin" % age if age is not None else UNKNOWN
    else:
        W("DIRECTIVE UNAVAILABLE — read #2601 before acting.")
        age_str = UNKNOWN
    W("")

    # ---- 3b. LESSON BROADCAST (Shawn's law, 2026-10-15): the brief is the
    # real bake-in channel. Newest ADOPTED lessons ride every dispatch —
    # teach it once, every future Naya wakes up knowing it. Fail-open here
    # (a missing ledger must never block a wave); the bundle carries the
    # full LEARN layer for deep activation.
    try:
        _lp = os.path.join(SBRAIN, "lessons.jsonl")
        _lessons = []
        with open(_lp) as _f:
            for _line in _f:
                _line = _line.strip()
                if not _line:
                    continue
                try:
                    _d = json.loads(_line)
                except Exception:
                    continue
                if _d.get("adopted_utc"):
                    _lessons.append(_d)
        _lessons.sort(key=lambda _d: _d.get("adopted_utc", ""), reverse=True)
        if _lessons:
            W("ADOPTED LESSONS — proven in battle, behave accordingly")
            W("(distinct from 'Fresh from the hive': those are fresh learnings;")
            W("these are adopted — verified against the machinery, highest bar):")
            for _ls in _lessons[:5]:
                W("- [%s] %s" % (_ls.get("seat", "?"), _ls.get("lesson", "")))
                if _ls.get("changes"):
                    W("  changes: %s" % _ls["changes"])
        else:
            W("(no adopted lessons in the ledger yet)")
    except Exception:
        W("(lesson broadcast unavailable — not blocking)")
    W("")

    # ---- 4. Spawn-time freshness stamp ----
    tip_live = UNKNOWN
    try:
        r = run(["git", "ls-remote", REPO, "HEAD"], timeout=20)
        if r.returncode == 0 and r.stdout.split():
            tip_live = r.stdout.split()[0][:12]
    except Exception:
        pass
    free = []
    try:
        r = run([sys.executable, LANE_STATE_PY, "free"], timeout=15)
        if r.returncode == 0:
            free = json.loads(r.stdout.strip() or "[]")
    except Exception:
        pass
    hm = datetime.now(timezone.utc).strftime("%H:%MZ")
    W("SPAWN-CHECK %s: tip %s | lanes free [%s] | directive age %s"
      % (hm, tip_live, ", ".join(str(x) for x in free) if free else "none", age_str))
    W("")

    # ---- 5. Briefing proof block (interface already validated above) ----
    r = run([sys.executable, PROOF_BIN, "fingerprint"], timeout=15)
    fp = UNKNOWN
    fp_path = os.path.expanduser("~/workspace/agent-briefing-master.md")
    try:
        _fpj = json.loads(r.stdout)
        fp = _fpj.get("sha256", UNKNOWN)
        fp_path = _fpj.get("path", fp_path)
    except Exception:
        pass
    hhmm = datetime.now(timezone.utc).strftime("%H%M")
    ch_path = "/tmp/bp-ch-%s-%s.json" % (seat_tag, hhmm)
    ans_path = "/tmp/bp-ans-%s.json" % seat_tag
    r = run([sys.executable, PROOF_BIN, "challenge", "--count", "3"], timeout=15)
    if r.returncode != 0:
        die("briefing_proof.py challenge failed (rc=%d)" % r.returncode)
    try:
        open(ch_path, "w").write(r.stdout)
    except OSError as e:
        die("cannot write challenge file %s: %s" % (ch_path, e))
    W("Briefing fingerprint (sha256 of %s): %s — hash THAT file, not your brief." % (fp_path, fp))
    W("Quote challenged lines verbatim from that file.")
    W("PROOF-OF-BRIEFING (do FIRST, before your work list):")
    W("a. Run: python3 ~/workspace/bin/briefing_proof.py answer --challenge %s > %s"
      % (ch_path, ans_path))
    W("b. Run: python3 ~/workspace/bin/briefing_proof.py verify --answer %s — must exit 0."
      % ans_path)
    W('c. Run: python3 ~/workspace/bin/briefing_proof.py record --answer %s --who "%s" --lane %s — must exit 0. You have not started until (c) succeeds.'
      % (ans_path, seat, lane))
    W("")

    # ---- 6. Worker rules + receipt format ----
    W("WORKER RULES:")
    W("1. Sign-in is STEP ZERO — post on your lane feed BEFORE the briefing proof.")
    W("   A lane claim is a reservation, not occupancy: it becomes occupancy only when that")
    W("   sign-in post names the mission and is GitHub-posted <=10 min after the claim;")
    W("   no sign-in by minute 11 = VOID (heartbeat freshness never counts).")
    W("   PULSE pre-flight: draft the sign-in to a file, run python3 ~/workspace/naya/bin/pulse_cap_check.py <draft>")
    W("   — exit 0 required (PULSE <= 300 bytes, machine-measured; the cap is not honor-system). Post only on PASS.")
    W("   Local-only / zero-API missions: NO EXEMPTION. Sign-in + sign-out are 2 mandatory")
    W("   lifecycle posts, reserved OUTSIDE the 10-call work budget (queued-posts during a")
    W("   standdown, never skipped). A mission that cannot afford 2 posts is not dispatched.")
    W("2. Heartbeat the truth file when alive — python3 %s heartbeat %s %s —"
      " post ONLY on state change (no noise). Your seat token is ONE token:"
      " underscores, no spaces (e.g. Naya_Iota) — the dispatcher claimed your lane"
      " with this exact token; use it character-for-character, never re-spell it." % (LANE_STATE_PY, lane, seat_tag))
    W("3. Time-boxed work list — work top-down, each item RIGHT or skip honestly.")
    W("   Partial completion is normal. The receipt is what matters, not the count.")
    W("4. API governor: 10 gh-api calls max per mission. Local-first, cheap-check-first.")
    W("5. Every emission follows THE EMISSION SCHEMA — no prose outside it.")
    W("6. POST EARLY: your single most important finding goes to the lane feed")
    W("   FIRST, before deep work. A timeout can kill your run but must never")
    W("   orphan your result — minimal pulse early, full sign-out at the end.")
    W("7. FIRST-PASS BULLSEYE (Shawn's law — stop missing the mark): BEFORE you")
    W("   build, run the pre-mortem. List every reason this work will NOT hit 9+")
    W("   as planned, then write the countermeasure for each reason. Build the")
    W("   countermeasures in from the start — not after. Then triple-pass it:")
    W("   build → score honestly → name why it's not 10 → fix → score again →")
    W("   name why it's not 10 → fix → score a third time. Done-posted ≠ good.")
    W("   Everything gets scorecarded. Aim: 9+ on the FIRST pass.")
    W("8. BODY-VOICE DISCRIMINATOR (n7 re-polls — LAW w232, stop rediscovering")
    W("   this): author-login is NON-discriminating — SoulSchoolAcademy IS")
    W("   Shawn's own account, so every connector post shares it. 'BY SHAWN' =")
    W("   the body-voice test on the comment text: a comment WRITTEN BY Shawn")
    W("   reads as his voice; agent posts share the login but not the voice.")
    W("   Never use author-login to judge whether Shawn spoke.")
    W("")
    W("SIGN-OUT RECEIPT (this is the shared memory — be exact):")
    W("completed: [#, #] — one-line verdict per finished item")
    W("remaining: [#, #] — current state of each, ready for the next worker")
    W("recommend: <what the next worker should hit first and why — your judgment>")
    W("add: <new items you discovered that belong on the list, if any>")
    W("score: n/10 — what it means | changed: what changed for a human")
    W("win_why: the mechanism — why it worked, or what broke and what fixed it")
    W("miss: <one thing YOU got wrong, if any — name it plainly on the feed>")
    W("COMMENT STANDARD v2 (Shawn's law — one canonical doc: hidden_files/COMMENT-STANDARD.md):")
    W("  Template: what changed → uncomfortable number → evidence (link/SHA) → NOT assumed → ceiling (what this does NOT prove) → next + owner.")
    W("  Grade yourself: can the next reader act on this alone? is every claim re-checkable in one command? delta/decision/evidence?")
    W("  No to Q1 → ≤5/10. Evidence-free → never above 5. Can't fill what-changed/evidence/next → heartbeat (lane-state.py), not a comment.")
    W("  Duplicates and cleanup-creating posts start at 2/10. Correcting? Use CORRECTION type: Was / Is / Mechanism / Fix — fast.")
    W("feedback (Clarity's block — permanent, every receipt):")
    W("  read_directive: <yes/no> | tuned_in: <yes/no>")
    W("  worked: <one line> | didnt: <one line> | improve: <one suggestion>")

    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
