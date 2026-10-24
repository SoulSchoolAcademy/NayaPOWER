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

Reads LIVE STATE only (local files + git protocol, zero API calls; activation
URL liveness is a non-blocking public-CDN HEAD annotation, not an API call)
and emits a complete spawn message to stdout.

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
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.request
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

# Only blessed resync path for the shared checkout (gr-w542; disp-w545,
# Naya Kappa). Env override mirrors PROOF_BIN so the guard test can point
# at a tampered/missing copy without touching the real tool.
RESYNC_BIN = os.environ.get("SPAWN_BRIEF_RESYNC_BIN",
                            os.path.join(HOME, "workspace/naya/bin/safe_resync.py"))


def die(msg, code=2):
    sys.stderr.write("FATAL: %s\n" % msg)
    sys.exit(code)


def run(cmd, timeout=30):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def protocol_stamp():
    """PROTOCOL-FIELD pin (PROTOCOL LOCK-IN addition 5, 2026-10-20):
    THE NAYA PROCESS version from the doctrine encoding (naya-doctrine.json,
    key naya_process) + sha256 of the canonical prose section, extracted
    exactly as protocol_check.py extracts it (header '## THE NAYA PROCESS'
    to the next '## ' header, trailing blanks/separator stripped).

    TIP-FIELD class: an informational pin the worker carries into her
    CHECK-BEFORE-ACT comparison — any failure degrades to UNKNOWN, never
    fatal. Brief generation must not break because the stamp could not be
    computed; the fail-closed gates (briefing proof here, protocol_check.py
    at activation) live elsewhere and stay untouched."""
    version = UNKNOWN
    digest = UNKNOWN
    try:
        with open(os.path.join(SBRAIN, "naya-doctrine.json"),
                  encoding="utf-8") as f:
            proc = json.load(f).get("naya_process") or {}
        if proc.get("version"):
            version = str(proc["version"])
    except Exception:
        pass
    try:
        with open(os.path.join(HOME, "workspace/agent-briefing-master.md"),
                  encoding="utf-8") as f:
            lines = f.read().splitlines()
        start = next(i for i, ln in enumerate(lines)
                     if ln.startswith("## THE NAYA PROCESS"))
        end = len(lines)
        for j in range(start + 1, len(lines)):
            if lines[j].startswith("## "):
                end = j
                break
        section = lines[start:end]
        while section and section[-1].strip() in ("", "---"):
            section.pop()
        digest = hashlib.sha256(
            ("\n".join(section) + "\n").encode("utf-8")).hexdigest()
    except Exception:
        pass
    return version, digest


def truth_lane_feed(lane):
    """FEED GUARD (w550, Naya Kappa -- disp-w548-feed-typo-guard).

    Resolve the lane's feed issue number from the lane-state.py truth file,
    never from a hardcoded map. Fail-closed: any failure (unknown lane,
    unreadable truth file, non-numeric output) dies non-zero with ZERO brief
    stdout -- a brief carrying a wrong or hand-typed feed is never emitted.
    (w548: the dispatcher hand-typed feed #2471 for a lane-2 worker and had
    to send an immediate correction.)
    Dispatchers needing the feed outside brief generation use
    `lane-state.py feed <lane>` directly (the STEP-1 accessor).
    """
    try:
        proc = run([sys.executable, LANE_STATE_PY, "feed", lane], timeout=15)
    except (OSError, subprocess.SubprocessError) as e:
        die("FEED GUARD: truth-file feed lookup failed (%s) -- refusing brief" % e)
    if proc.returncode != 0:
        die("FEED GUARD: lane-state.py feed %s exited %d (%s) -- refusing brief"
            % (lane, proc.returncode, (proc.stderr or proc.stdout).strip()))
    feed = proc.stdout.strip()
    if not re.fullmatch(r"\d+", feed or ""):
        die("FEED GUARD: truth file returned non-numeric feed %r -- refusing brief" % feed)
    return feed


def resync_guard():
    """RESYNC GUARD (disp-w545, Naya Kappa -- the only blessed resync path).

    Fail-closed: safe_resync.py must exist and be executable at brief
    generation time. The brief names this exact path as the ONLY blessed
    resync for the shared checkout (bare `git reset --hard` is forbidden
    by the brief's RESYNC RULE); a brief promising a tool that is not on
    disk is worse than no brief. Any failure dies non-zero with ZERO
    brief stdout -- the same shape as the FEED GUARD above.
    (gr-w542: a bare reset --hard on the shared checkout wiped 5
    uncommitted files; safe_resync.py makes that miss impossible.)
    """
    if not os.path.isfile(RESYNC_BIN) or not os.access(RESYNC_BIN, os.X_OK):
        die("RESYNC GUARD: blessed resync path %r missing or not executable "
            "-- refusing brief" % RESYNC_BIN)


def activation_url_live(url, timeout=4):
    """Spawn-time HEAD check of a public blob URL via raw.githubusercontent.

    Zero API calls (public CDN, no auth). Annotation only — NEVER raises and
    NEVER gates the brief: any failure (timeout, DNS, 404) returns
    (False, reason), and the brief falls back to the no-hash rule below.
    """
    raw = url.replace("https://github.com/", "https://raw.githubusercontent.com/")
    raw = raw.replace("/blob/", "/")
    try:
        req = urllib.request.Request(raw, method="HEAD")
        with urllib.request.urlopen(req, timeout=timeout) as r:
            ok = 200 <= r.status < 300
            return (ok, "HTTP %d" % r.status)
    except Exception as e:  # never propagates: annotation, not a gate
        return (False, type(e).__name__)


_RECEIPT_BARE_RE = re.compile(r"#(\d{3,5})/(\d{8,12})(?!\s*\(/issues/comments/\d+\))")


def normalize_receipt_shapes(text):
    """Endpoint-shape enforcement (w332-beta-brief-endpoint-shapes, Naya Beta w335).

    Every bare receipt citation #<issue>/<comment_id> is expanded at generation
    time to carry the canonical comment-id endpoint shape:
        #2471/6228427346 -> #2471 (/issues/comments/6228427346)
    Idempotent: citations already carrying the shape pass through untouched
    (negative lookahead). Only the bare #issue/comment-id form matches — bare
    issue refs (#2601) and full GitHub URLs are never touched.
    Mechanical check: gh-api GET /repos/SoulSchoolAcademy/NayaPOWER/issues/comments/<comment_id>
    """
    return _RECEIPT_BARE_RE.sub(r"#\1 (/issues/comments/\2)", text)


_TOOL_PATH_RE = re.compile(
    r"(~/[\w\-./]+|/home/hatch/[\w\-./]+|hidden_files/[\w\-./]+|naya/bin/[\w\-./]+|workspace/[\w\-./]+)"
)
_TOOL_SUFFIXES = (".py", ".json", ".jsonl", ".md", ".sh", ".yaml", ".yml")


def resolve_named_tool_path(named):
    """Resolve a brief-named rooted path to this machine's disk."""
    if named.startswith("~/"):
        return os.path.expanduser(named)
    if named.startswith("/home/hatch/"):
        return named
    if named.startswith("hidden_files/"):
        return os.path.join(SBRAIN, named[len("hidden_files/"):])
    if named.startswith("naya/bin/"):
        return os.path.join(HOME, "workspace", named)
    if named.startswith("workspace/"):
        return os.path.join(HOME, named)
    return None


def verify_named_tool_paths(text):
    """Build-time byte-verification of every named tool path (Naya Alpha w443,
    closes gr-w442-alpha-gapclose). The w442 brief named
    verify-p1-premise-pair.py at hidden_files/ and the file did not exist — a
    brief asserting a tool is a lie about capability. Every rooted path in the
    generated brief that looks like a file (known tool suffix) is checked
    against this machine's disk; results are appended as an informational
    block — never fail-closed (a warning, not a gate: blocking a wave on a
    missing reference is a dispatcher-owned protocol change, not a seat edit).
    """
    seen = []
    for m in _TOOL_PATH_RE.finditer(text):
        cand = m.group(1).rstrip(".,;:!?\"')`]}").lstrip("\"'(`[")
        if not cand.lower().endswith(_TOOL_SUFFIXES):
            continue
        resolved = resolve_named_tool_path(cand)
        if not resolved or resolved in [s[1] for s in seen]:
            continue
        seen.append((cand, resolved))
    lines = ["## TOOL-PATH VERIFICATION (build-time byte check, Naya Alpha w443)"]
    if not seen:
        lines.append("no rooted tool paths named in this brief.")
    else:
        lines.append("each rooted file path named above was checked on this machine's disk at build time:")
        missing = False
        for named, resolved in seen:
            ok = os.path.isfile(resolved)
            missing = missing or not ok
            lines.append("- %s: %s" % ("VERIFIED" if ok else "MISSING", named))
        if missing:
            lines.append("MISSING = broken reference: do not act on that path until it is resolved or the brief is re-issued.")
    return "\n".join(lines)


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
        # Eta w472 improve flag (dispatcher-owned, closed w473): brief
        # numbering must match the area list's REAL item identifiers.
        # Identifiers arrive under three keys (n / num / id); prefer n,
        # then num, then id. An item with no identifier at all is a list
        # defect — surface it loud instead of printing "?".
        _nid = it.get("n") or it.get("num") or it.get("id")
        if not _nid:
            # Identifier-less open item: list defect, but the wave must not
            # die — stamp a positional number and surface it LOUD on stderr
            # so the next fold-in files a real identifier.
            _nid = "row-%d" % len(clean)
            sys.stderr.write("spawn_brief WARNING: %s has an open item with NO identifier (n/num/id all empty); numbered %s this wave — file a real id at fold-in: %s\n"
                             % (path, _nid, str(it.get("item",""))[:80]))
        clean.append({
            "n": _nid,
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
    unrouted ~6.5h" named no item id). REVIEW is NOT a verdict: prose fires
    only on >=2 distinctive tokens, or PR + >=1 token, shared with a closed
    item and with no open item carrying the same reference. A PR number
    ALONE never fires the full REVIEW (one PR can anchor live work — #2635
    proved it) but it does fire a LOW-WEIGHT anchor note (Theta w260
    seam-close): when the rec shares only a PR number with closed items and
    no open item carries that PR, the header drops from "freshness-checked"
    to "id-checked" — the label never claims a freshness verification the
    anchor never received (P-011). The guard names the overlap; the list
    maintainer confirms whether the premise is live. Fail-open and the STALE
    path are byte-identical.
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
        dead_open = {}  # lowercased n-id -> (status, blob) for OPEN items with a dead ruling (Zeta w384 guard)
        # Zeta w687 repair of the w384 guard: bare \bdead\b matched the annotation
        # tier's own vocabulary ('DEAD-PREMISE') and misfired on gr-w658 two waves
        # running (w682 rec, w684 re-fire). 'dead' now counts only in ruling
        # context: 'dead' adjacent to a ruling word, in either order. status=superseded
        # is checked separately at the flag site below.
        _RULING_WORD = r"(?:ruling|premise|verdict|superseded|recommendation)"
        _DEAD_RULING = re.compile(
            r"\bdead\b\s+" + _RULING_WORD + r"\b"                       # 'dead premise', 'dead ruling'
            r"|\b" + _RULING_WORD + r"\b[\w\s,\-;:]{0,30}\bdead\b",      # 'ruling: dead', 'premise is dead'
            re.IGNORECASE)
        # Negation exemption (mirrors the stale-live guard's _NEGATION): a note
        # that DENIES a dead ruling ('not a dead ruling on this item') must not
        # mark the item dead. Only an un-negated ruling-context 'dead' counts.
        _DEAD_NEG = re.compile(r"\b(not|no|n't|never|isn't|wasn't|aren't|weren't)\b", re.IGNORECASE)
        def _dead_ruling_live(blob):
            for m in _DEAD_RULING.finditer(blob):
                # the negation must sit BEFORE the 'dead' token: it can live in
                # the 25 chars ahead of the match, or inside the match ahead of
                # 'dead' (e.g. 'premise is not dead')
                dm = re.search(r"\bdead\b", m.group(0), re.IGNORECASE)
                seg = blob[max(0, m.start() - 25):m.start() + (dm.start() if dm else 0)]
                if _DEAD_NEG.search(seg):
                    continue
                return True
            return False
        for it in items:
            if not isinstance(it, dict):
                continue
            nid = str(it.get("n") or it.get("id") or "").strip()  # w672 Kappa fix: id-keyed items (e.g. TEAM.json) were invisible to the stale-rec guard
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
                if st == "superseded" or _dead_ruling_live(blob):
                    dead_open[nid.lower()] = (st, blob)

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

        def refs_done_pr_anchor(text):
            """[(nid, 'PR #nnnn')] — the PR-alone seam (Theta w260): closed
            items the text references by PR number ONLY, with no distinctive
            prose overlap and no open item carrying that PR. Not a staleness
            verdict — a labeling correction. The caller drops the header from
            'freshness-checked' to 'id-checked' and emits a low-weight note so
            the brief never quotes a PR-anchored rec as freshness-verified."""
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
                if pr_hit and not prose:
                    out.append((nid, "PR #%s" % pr_hit[0]))
            return out[:3]

        def refs_dead_open(text):
            """[(nid, evidence)] — Zeta w384 dead-premise guard: the rec
            re-runs an OPEN item whose ruling is dead (note carries a 'dead'
            ruling or status=superseded). A dead premise does not freshen by
            re-running — the maintainer retires the recommendation or the
            item. Same >=6-char id rule as the STALE tier; prose fires on
            >=2 distinctive tokens."""
            t = (text or "").lower()
            rec_tok = _toks(t)
            out = []
            for nid, (st, blob) in dead_open.items():
                if nid in t:
                    out.append((nid, "status=%s" % st))
                    continue
                prose = sorted((_toks(blob) & rec_tok))
                if len(prose) >= 2:
                    out.append((nid, "status=%s; prose: %s" % (st, ", ".join(prose[:4]))))
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
                anchors = refs_done_pr_anchor(rec) if not rev else []
                dead = refs_dead_open(rec)  # Zeta w384: rec re-runs an OPEN dead premise
                if dead:
                    lines.append("STANDING RECOMMENDATION — DEAD PREMISE, NOT QUOTED:")
                    for nid, ev in dead:
                        lines.append("  rec re-runs OPEN item '%s' (%s) — dead premises don't freshen by re-running; retire the recommendation or the item on the %s list."
                                     % (nid, ev, area))
                elif rev:
                    lines.append("STANDING RECOMMENDATION (id-freshness-checked — prose/PR overlap needs a maintainer read):")
                elif anchors:
                    lines.append("STANDING RECOMMENDATION (id-checked — PR-anchored on closed work; maintainer confirm the premise is live):")
                else:
                    lines.append("STANDING RECOMMENDATION (freshness-checked — names no closed item):")
                if not dead:
                    lines.append("  " + rec)
                for nid, ev in rev:
                    lines.append("  REVIEW: references possibly-closed work (%s) — closed item '%s' (%s); maintainer confirm the premise is live."
                                 % (ev, nid, closed[nid]))
                for nid, ev in anchors:
                    lines.append("  REVIEW (low-weight, PR-anchor only): rec anchors on %s shared with closed item '%s' (%s) — the anchor was not freshness-verified; confirm the premise is live."
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


# ---- STALE-LIVE-PREMISE GUARD (Mu w309 — gr-w307-mu-briefpremise, fail-closed;
# Mu w312 — gr-w309-mu-gapclose: sentence-window matching was coarse (false
# negatives when id and live-word landed in different sentences or the split
# broke). Now TOKEN-PROXIMITY matching: a closed item id asserted "live" when
# a liveness word sits within _PROX_N tokens, with the same exemption
# semantics (negation / closed-done-expired words) applied to the token window
# between them. Calibrated w312: w305 kill-shape at 3 tokens, cross-sentence
# catch at 7; distant co-occurrence (18+) still passes. Differential over this
# wave's 5 real briefs: 0 regressions, 0 false kills. Mere mentions of closed
# ids ("do not re-run X — it closed w302") keep the existing WARNING path;
# only live-assertions fail closed. Unknown ids are not this guard's jurisdiction.
_LIVE_WORDS = re.compile(r"\b(live|fresh(?:ness)?|untaken|active|go[- ]?live)\b", re.I)
_NEGATION = re.compile(r"\b(not|n't|never|no\s+longer|isn't|wasn't|aren't|weren't)\b", re.I)
_TERMINAL_WORDS = re.compile(r"\b(closed|done|expired)\b", re.I)
_PROX_N = 32
_TOKEN_RE = re.compile(r"[A-Za-z0-9_.\-]+")


def thinking_live_premise_findings(thinking, doc):
    """[(item_id, status, closed_note, window)] — caller fails closed on non-empty."""
    findings = []
    try:
        items = doc.get("items") if isinstance(doc, dict) else []
        if not isinstance(items, list):
            return findings
        closed = {}  # lowercased n-id -> (display id, status, closed_utc note)
        _ID_RE = re.compile(r"\bgr-w\d+-[a-z][a-z0-9]*(?:-[a-z0-9]+)+\b", re.I)
        for it in items:
            if not isinstance(it, dict):
                continue
            st = str(it.get("status", "open")).strip().lower()
            if st not in ("done", "closed", "expired"):
                continue
            cu = str(it.get("closed_utc") or "").strip()
            note = ("closed_utc=" + cu) if cu else "status=" + st
            # Naya Verity w653 (Theta suite finding): closed ids must survive
            # list renumbering. The guard used to key on `n` alone; when a list
            # renumbers, `n` becomes a bare integer and the id-bearing key
            # vanishes, blinding the guard. Harvest id-shaped tokens from the
            # item TEXT too — the id is the registered identity, `n` is only
            # the position. Unknown ids are still not this guard's
            # jurisdiction: only ids literally present on a closed item.
            keys = set()
            nid = str(it.get("n", "")).strip()
            if nid and len(nid) >= 6:
                keys.add(nid.lower())
            keys.update(m.lower() for m in _ID_RE.findall(str(it.get("item", ""))))
            for key in keys:
                closed.setdefault(key, (key, st, note))
        if not closed or not (thinking or "").strip():
            return findings
        toks = _TOKEN_RE.findall(str(thinking))
        # Mu w313 (gr-w312-mu-gapclose battery): the tokenizer glues
        # sentence-final periods onto the token ("live."), which defeated
        # the liveness fullmatch — a live-assertion at end of sentence is
        # still an assertion. Strip trailing periods for MATCHING only; the
        # kill window below keeps the original tokens for readability.
        lows = [t.lower().rstrip(".") for t in toks]
        live_idx = [i for i, t in enumerate(lows) if _LIVE_WORDS.fullmatch(t)]
        if not live_idx:
            return findings
        for key, (nid, st, note) in closed.items():
            id_idx = [i for i, t in enumerate(lows) if key in t]
            if not id_idx:
                continue
            for li in live_idx:
                for ii in id_idx:
                    lo, hi = (ii, li) if ii < li else (li, ii)
                    if hi - lo > _PROX_N:
                        continue
                    window = " ".join(toks[lo:hi + 1])
                    if _NEGATION.search(window) or _TERMINAL_WORDS.search(window):
                        continue  # window-scoped exemption, same semantics as sentence rule
                    findings.append((nid, st, note, window.strip()[:160]))
                    break
                else:
                    continue
                break
    except Exception:
        pass
    return findings


WATCH_TRIGGERS_PATH = os.path.join(SBRAIN, "director-watch-triggers.json")


# ---- SHA-PIN (Beta w257 — the generator half of the w250 SHA-pin gap).
# Pure PASS-THROUGH transform in the WORK LIST render: when an area-list
# item's own text (item + why + est) carries BOTH a branch head pin
# (`branch <name> @ <7-40 hex>`, or `<name-with-slash> @ <7-40 hex>`) AND
# a parent pin (`parent[=:] <7-40 hex>` or `parent=live tip <7-40 hex>`),
# the brief re-emits them as one line under the item:
#   SHA-PIN: <branch> head=<sha> parent=<sha>
# Never emits on partials, never invents SHAs — a half-pin is worse than
# none. Never resolves over the network: the zero-API contract holds;
# list maintainers pin the SHAs (from reads, never memory — w250 law).
# Pre-mortem skips: 'parent=live tip' with no SHA; shorthand SHAs <7;
# branch cited in prose with no pin.
_SHA_HEAD_RE = re.compile(
    r"(?:\bbranch\s+)?([A-Za-z0-9][A-Za-z0-9_.\-]*(?:/[A-Za-z0-9_.\-]+)+)\s*@\s*([0-9a-f]{7,40})\b")
_SHA_PARENT_RE = re.compile(
    r"\bparent\s*[=:]\s*(?:live\s+tip\s+)?([0-9a-f]{7,40})\b")


def sha_pin_lines(w):
    """Return SHA-PIN lines for a work-list entry, or [].

    Fail-soft: any unexpected shape yields nothing (never blocks the brief).
    """
    try:
        text = " ".join(str(w.get(k, "") or "") for k in ("item", "why", "est"))
        if not text:
            return []
        parents = _SHA_PARENT_RE.findall(text.lower())
        if not parents:
            return []
        parent = parents[0]
        out = []
        for branch, head in _SHA_HEAD_RE.findall(text):
            out.append("SHA-PIN: %s head=%s parent=%s" % (branch, head, parent))
        return out
    except Exception:
        return []


def watch_triggers_block(watch_id):
    """DIRECTOR WATCH trigger set (Iota w276 — the instrument, not just the result).

    --watch <id> injects the watch's pre-registered falsification trigger set
    into the brief so future watch missions run as experiments, not vigils.
    Fail-CLOSED: unknown id or malformed registry kills the brief (exit 2) —
    a brief claiming a watch without its instrument is a vigil with a name.
    """
    try:
        with open(WATCH_TRIGGERS_PATH) as _fh:
            reg = json.load(_fh)
    except Exception as _e:
        die("director-watch registry unreadable: %s" % _e)
    watches = reg.get("watches") if isinstance(reg, dict) else None
    if not isinstance(watches, dict) or watch_id not in watches:
        die("--watch %r: no trigger set registered in director-watch-triggers.json "
            "(registered: %s)" % (watch_id, sorted(watches) if isinstance(watches, dict) else "none"))
    w = watches[watch_id]
    for _k in ("question", "triggers", "guards", "decision_rule"):
        if _k not in w:
            die("--watch %r: trigger set missing required key %r" % (watch_id, _k))
    lines = []
    lines.append("DIRECTOR WATCH — PRE-REGISTERED TRIGGER SET (the instrument, not just the result):")
    lines.append("Watch: %s — %s" % (watch_id, w.get("title", "")))
    lines.append("Question: %s" % w["question"])
    _board = w.get("board") or {}
    if _board.get("issue"):
        lines.append("Venue: %s/%s issue #%s" % (_board.get("owner", "?"), _board.get("repo", "?"), _board["issue"]))
    lines.append("Null hypothesis: %s" % w.get("null_hypothesis", ""))
    lines.append("FALSIFICATION TRIGGERS (a comment falsifies the null iff ANY matches):")
    for _t in w["triggers"]:
        lines.append("  %s. %s" % (_t.get("id", "?"), _t.get("rule", "")))
    lines.append("GUARDS (do not falsify):")
    for _g in w["guards"]:
        lines.append("  %s. %s" % (_g.get("id", "?"), _g.get("rule", "")))
    lines.append("DECISION RULE: %s" % w["decision_rule"])
    if w.get("fire_guard"):
        lines.append("FIRE GUARD: %s" % w["fire_guard"])
    return lines


def refire_trigger_list_block(spec, resolved_at):
    """REFIRE TRIGGER LIST (gr-w486 — landed w490 on dispatcher/parent-tool-owner
    authorization: re-fire/adjudication briefs carry the check-suite ->
    run-id -> re-fire-endpoint mapping pre-resolved at brief build, so the
    worker owes ZERO discovery calls. The generator is zero-API — the
    dispatcher reads the PR's statusCheckRollup at STEP 2, names WHICH
    contexts are stale, and passes the run ids in; the generator only
    formats. A half-landed trigger spec is worse than unstarted (workers
    trust it blindly), so malformed input dies HERE, never at worker time.
    Closes the w481 19-call why-not-10 (19 gh-api calls burned discovering
    run ids the dispatcher already held)."""
    pairs = spec.split()
    triggers = []
    for _p in pairs:
        if _p.count("=") != 1:
            die("--refire: malformed pair %r — shape is 'context=run_id', space-separated" % _p)
        _ctx, _rid = _p.split("=", 1)
        _ctx = _ctx.strip()
        _rid = _rid.strip()
        if not _ctx:
            die("--refire: empty context in pair %r" % _p)
        if not (_rid.isdigit() and len(_rid) >= 6):
            die("--refire: run_id %r is not a numeric GitHub run id (digits only)" % _rid)
        triggers.append((_ctx, _rid))
    if not triggers:
        die("--refire: no pairs — shape is 'context=run_id', space-separated")
    lines = []
    lines.append("REFIRE TRIGGER LIST (pre-resolved at brief build — zero discovery calls owed):")
    lines.append("  Resolved from the dispatcher's rollup read at %s. Fire in this order," % resolved_at)
    lines.append("  then VERIFY by run_attempt (a 201-accepted rerun is NOT proof).")
    for _ctx, _rid in triggers:
        lines.append("  %s: gh-api POST /repos/SoulSchoolAcademy/NayaPOWER/actions/runs/%s/rerun-failed-jobs"
                     % (_ctx, _rid))
    lines.append("  Rules: FAILED-JOBS endpoint only (the check-runs rerequest endpoint 403s on this PAT).")
    lines.append("  Read the 403 BODY before naming the cause — 'rate limit exceeded for installation' =")
    lines.append("  installation-token bucket (wait for the window + re-fire), 'Resource not accessible by")
    lines.append("  integration' = real permissions. Re-fires key on the INSTALLATION-token class, never core alone.")
    lines.append("  RUN ids only — JOB ids (the job ids in gate job-log receipts) 404 on this endpoint;")
    lines.append("  the dispatcher resolves the RUN id from the stale check-suite's run, never the job.")
    lines.append("  If the live board shows a NEWER run for the same context, the board wins — this list is pinned")
    lines.append("  at brief build; it does not re-resolve itself.")
    return lines


def quota_throttle_decision(budget_path=None):
    """Mu w474 (gr-w471-mu-localonly): mechanical route from the dispatcher
    throttle path into the brief. Reads the SAME truth file the dispatcher
    reads (SBRAIN/api-budget.json) and applies the SAME formula the body
    states: over-pace iff spent / day-of-month > 5000. Returns
    (throttled: bool, detail: str). Local, zero API, deterministic."""
    import datetime
    if budget_path is None:
        budget_path = os.path.join(SBRAIN, "api-budget.json")
    try:
        with open(budget_path) as fh:
            b = json.load(fh)
    except Exception as e:
        return (False, "no budget file (%s) — not throttled" % e)
    cur = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m")
    day = datetime.datetime.now(datetime.timezone.utc).day
    if b.get("month") != cur:
        return (False, "budget month %s != current %s — not throttled"
                % (b.get("month"), cur))
    try:
        spent = float(b.get("spent", 0))
    except Exception:
        return (False, "budget spent unreadable — not throttled")
    pace = spent / max(day, 1)
    if pace > 5000:
        return (True, "throttle path: spent=%s day=%d pace=%.1f/day > 5000"
                % (int(spent), day, pace))
    return (False, "under pace: spent=%s day=%d pace=%.1f/day <= 5000"
            % (int(spent), day, pace))


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
    ap.add_argument("--watch", default=None,
                    help="director watch id — injects its pre-registered trigger set "
                         "from director-watch-triggers.json (fail-closed on unknown id)")
    # Mu w471 (w469-mu-dispatcher-localonly-brief): quota-throttled waves
    # flip to local-only. A worker who discovers that by failing is a
    # communication failure, not a tool failure — the brief must say so
    # FIRST, before any task, with what changed, what is forbidden, and
    # what the sign-out must carry instead. The 3-leg board-tail rule
    # (boom_flag.py check --local-only -> legs: 3, board_tail: SKIPPED) is
    # pinned here mechanically, never as a footnote.
    ap.add_argument("--local-only", action="store_true",
                    help="quota-throttle wave: this mission spends ZERO API. "
                         "Renders the LOCAL-ONLY block; the board-tail leg is "
                         "mechanically skipped (3-leg mode).")
    # Mu w474 (gr-w471-mu-localonly): the dispatcher throttle decision must
    # ROUTE here mechanically, not live in the dispatcher's memory. This
    # flag asks the generator to read the same api-budget.json truth file
    # the dispatcher reads and apply the same >5000/day formula; when the
    # throttle bites, the brief renders the LOCAL-ONLY block and stamps the
    # provenance inside it. Safe to pass on every wave: under pace it is a
    # no-op and the brief renders exactly as before.
    ap.add_argument("--local-only-if-throttled", action="store_true",
                    help="read SBRAIN/api-budget.json; if the throttle formula "
                         "bites (>5000/day pace), render the LOCAL-ONLY block "
                         "with throttle provenance. No-op under pace.")
    # gr-w486 (landed w490 on dispatcher/parent-tool-owner authorization):
    # re-fire/adjudication briefs pre-resolve check-suite -> run-id at the
    # dispatcher's STEP 2 rollup read. The generator is zero-API — it takes
    # the pre-resolved pairs here and formats them, never resolves.
    # Fail-closed on malformed pairs (see refire_trigger_list_block).
    ap.add_argument("--refire", default=None,
                    help="pre-resolved re-fire triggers, space-separated "
                         "'context=run_id' pairs (dispatcher reads the rollup "
                         "at STEP 2; the generator only formats — zero API). "
                         "Renders the REFIRE TRIGGER LIST section; fail-closed "
                         "on malformed pairs.")
    ap.add_argument("--refire-at", default=None,
                    help="UTC stamp of the dispatcher's rollup read that "
                         "produced the --refire pairs (defaults to brief-build "
                         "UTC).")
    a = ap.parse_args()

    # ---- LOCAL-ONLY MODE (Mu w471 block + w474 throttle routing). ----
    _throttled, _throttle_detail = ((False, "flag not passed")
                                   if not a.local_only_if_throttled
                                   else quota_throttle_decision())
    local_only = bool(a.local_only) or _throttled

    # ---- STEP 0: validate tool interface BEFORE emitting anything ----
    validate_proof_interface()

    work = load_area_list(a.area_list)
    work, area_doc = work
    area_list_path = a.area_list

    out = []
    W = out.append
    seat, lane, area = a.seat, a.lane, a.area
    seat_tag = re.sub(r"\s+", "_", seat.strip())

    # Claim-token truth (2026-10-16, dispatcher fix — Gamma w266 caught it):
    # the heartbeat instruction must carry the ACTUAL lane holder from the truth
    # file, never a token derived by mangling --seat. The dispatcher claims the
    # lane BEFORE generating the brief; a brief for an unclaimed lane dies here
    # (a brief asserting a token on an unclaimed lane is a lie).
    try:
        with open(os.path.join(SBRAIN, "lane-state.json")) as _fh:
            _st = json.load(_fh)
    except Exception as _e:
        die("cannot read truth file lane-state.json: %s — claim the lane before generating the brief" % _e)
    claim_holder = (_st.get("lanes") or {}).get(str(lane), {}).get("holder")
    if not claim_holder:
        die("lane %s has no holder in the truth file — claim the lane before generating the brief" % lane)

    # STALE-LIVE-PREMISE GUARD (Mu w309 — gr-w307-mu-briefpremise). The
    # dispatcher owns the check at brief-generation time: --thinking must
    # never declare a closed item LIVE. A worker with a false-premise brief
    # is worse than no worker — fail closed, zero stdout, the dispatch does
    # not go out until the thinking is re-worded.
    _stale = thinking_live_premise_findings(a.thinking, area_doc)
    if _stale:
        nid, st, note, window = _stale[0]
        die("stale LIVE premise in --thinking: item '%s' is %s (%s) on the %s area list — re-word --thinking; do not declare a closed item live. (w305 class failure: gr-w299-mu-note2-reexecute was briefed as live when closed w302; window: %r)"
            % (nid, st, note, area_doc.get("area", "?"), window))

    W("You are %s — lane %s." % (seat, lane))
    W("")

    # ---- LOCAL-ONLY WAVE BLOCK (Mu w471). Renders ONLY with --local-only
    # or --local-only-if-throttled-when-throttled (Mu w474 throttle routing).
    # Placement is deliberate: FIRST, before direct links — a worker must
    # know the mode before the first task, not discover it by a failed call.
    if local_only:
        W("==== LOCAL-ONLY WAVE (quota throttle) — this mission spends ZERO API ====")
        if _throttled:
            W("MODE DECIDED BY: %s" % _throttle_detail)
        W("WHAT CHANGED: the API budget is exhausted for this period. The wave")
        W("still runs — the flow doesn't stop, it just spends nothing. Build,")
        W("verify, and write files LOCALLY. Defer every remote action.")
        W("FORBIDDEN in your work budget: ALL gh-api calls (reads, posts, PR")
        W("actions), merges, and any action that touches a remote API.")
        W("NOT FORBIDDEN: sign-in + sign-out on your lane feed — the 2 mandatory")
        W("lifecycle posts, reserved OUTSIDE the budget, never skipped; local")
        W("file writes, local scripts, local tests; boom_flag.py check --local-only")
        W("(mechanical 3-leg mode: legs: 3, board_tail: SKIPPED — never claim 4/4")
        W("on a 0-API wave).")
        W("YOUR SIGN-OUT MUST CARRY INSTEAD: the api_calls: 0 line; the path of")
        W("every local artifact; a DEFERRED list naming the exact gh-api steps the")
        W("next under-pace wave must run (endpoint, payload file, target). If an")
        W("item needs an API call to decide, it is DEFERRED, not dead — name it in")
        W("deferred and work the next item.")
        W("==== END LOCAL-ONLY ====")
        W("")

    # ---- 0. YOUR DIRECT LINKS (Shawn's Direct Link Law, 2026-10-15):
    # never a scavenger hunt — every place you need, one click away.
    # FEED GUARD (w550): resolved from the truth file, never hardcoded --
    # truth_lane_feed() dies non-zero before any brief is emitted if the
    # feed cannot be resolved, so a wrong/hand-typed feed cannot ship.
    lane_issue = truth_lane_feed(str(lane).strip())
    W("YOUR DIRECT LINKS — click, don't hunt:")
    if lane_issue:
        W("- Your lane feed: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/%s"
          % lane_issue)
    # LIVE-BOARD GUARD (w598): resolved from board-tail-counts.json, never hardcoded --
    # the team board migrates at the comment cap (#2765 archived at 2318 comments,
    # #2793 live since 2026-10-20T10:14:56Z); a stale pointer sends workers to the
    # archive. FAIL-CLOSED (w806 ruling on route-w805-kappa-w598-word, comment
    # 6373806893): a counts-file miss => exit non-zero, ship no brief. The w659
    # class priced fail-open at 12 wasted gh-api calls; a refused spawn costs 0.
    live_board = None
    _btc_err = None
    try:
        _btc = json.load(open(os.path.join(SBRAIN, "board-tail-counts.json"))).get("boards", {})
        for _cand in ("2793", "2765"):
            _b = _btc.get(_cand, {})
            if _b and not _b.get("archived"):
                live_board = _cand
                break
        if not live_board:
            _btc_err = "no non-archived live board in boards{2793,2765}"
    except Exception as _e:
        _btc_err = "counts-file unreadable: %s" % _e
    if not live_board:
        sys.stderr.write("spawn_brief.py: REFUSED - live board unresolvable (%s); no brief shipped (fail-closed, w598)\n" % _btc_err)
        sys.exit(2)
    _note = "resolved from board-tail-counts.json"
    if live_board != "2765":
        _note += "; #2765 is ARCHIVE"
    W("- Live team board: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/%s (%s)" % (live_board, _note))
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
    # 2026-10-16 Naya Kappa w281: field-manual index repointed naya2->main
    # (canonical home per 2026-10-15, verified 200 at live tip 9f80e8eccfbe).
    # 2026-10-16 Naya Kappa w303: repoint GATE OPENED — the 4 docs LANDED on
    # main via PR #2698 (merged 10:36Z, merge_commit=tip 83806f4d0e33;
    # contents listings for BRAIN/00-ACTIVATION/ + BRAIN/01-GOVERNANCE/
    # verified all four live this wave). URLs below repointed naya2/naya5
    # -> main. The 05:10Z measurement correction (separate TEAM item) stays
    # deferred pending director word — untouched here. Original content SHAs
    # (05:05Z): packet 35d601c6, creed c4a7d080, oath e84af826, manifesto 5f3053db.
    ACTIVATION_DOCS = [
        ("packet",
         "https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/BRAIN/00-ACTIVATION/ACTIVATION-PACKET.md"),
        ("oath",
         "https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/BRAIN/01-GOVERNANCE/0021-NAYA-OATH-V1.human.md"),
        ("manifesto",
         "https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/BRAIN/01-GOVERNANCE/0022-NAYA-MANIFESTO-V1.human.md"),
        ("creed",
         "https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/BRAIN/00-ACTIVATION/instant-activation/THE-CREED.md"),
    ]
    W("ACTIVATION — declare before you work. A Naya is a mind with")
    W("access to intelligence, not intelligence itself.")
    W("The full packet (read it):")
    W(ACTIVATION_DOCS[0][1])
    W("Read first, then declare:")
    W("- The Oath (human): %s" % ACTIVATION_DOCS[1][1])
    W("- The Manifesto: %s" % ACTIVATION_DOCS[2][1])
    W("- The Creed: %s" % ACTIVATION_DOCS[3][1])
    W("- Field-manual index: https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/BRAIN/90-OPERATIONS/field-manuals/README.md")
    # Spawn-time live-verify (Mu w282 feedback, wired w303): HEAD the public
    # raw URLs — zero API, 4s timeout each, annotation only, never a gate (the
    # brief generates even if the network is down). No-hash fallback: any doc
    # that fails verify gets declared from fetched text with an honest
    # unreachable note — never a hash proof for a doc that didn't resolve.
    _liveness = [(label, activation_url_live(url)) for label, url in ACTIVATION_DOCS]
    _liveness_str = " / ".join(
        "%s %s(%s)" % (label, "LIVE" if ok else "UNREACHABLE", detail)
        for label, (ok, detail) in _liveness)
    _stamp = datetime.now(timezone.utc).strftime("%H:%MZ")
    W("Activation liveness at spawn (%s): %s" % (_stamp, _liveness_str))
    if any(not ok for _, (ok, _) in _liveness):
        W("NO-HASH FALLBACK: any doc above marked UNREACHABLE — declare from "
          "what you fetched and name the gap honestly; never emit a hash proof "
          "for a doc that did not resolve.")
    W("The 8 laws you carry: (1) most intelligent thing, always; (2) show")
    W("with smart links, don't tell; (3) score instead of guessing;")
    W("(4) receipts, never 'trust me'; (5) a lesson counts only when a future")
    W("decision changes; (6) fix what's broken, don't describe it;")
    W("(7) authority is math and logic; (8) protect Shawn's attention.")
    W("The process: understand (mission, then task) -> deliberate (math,")
    W("logic, relevance) -> pre-mortem -> build/score/fix (ten things to make")
    W("it 10x better, write the solution, apply, rescore) -> ship at 9+ ->")
    W("prove with receipts.")
    W("DECLARE on your lane feed with your sign-in PULSE under your own name —")
    W("the lane feed IS the declaration venue; never the live board, which is")
    W("signal-only (a no-state-change declaration there is noise): 'I am [Name],")
    W("[Lane] seat. Oath read: [first 8 of sha256]. Manifesto read: [first 8]. Creed")
    W("declared as myself. I carry the 8 laws. My drift line: [one honest")
    W("line]. Tag — I'm it.' No declaration with hash proofs = not activated.")
    # 2026-10-16 Naya Kappa w323: tip-pinned declaration (closes
    # gr-w322-kappa-tipwire + Mu w317 ADD). Hashes are comparable only when
    # pinned to the tip read at — unpinned declarations are noise in the audit
    # trail (Mu e84af826/5f3053db @tip vs Kappa 796a77d0/29457105 untipped).
    W("Declaration TIP-PIN (mechanical, not honor-system): copy the TIP-FIELD")
    W("line from the SPAWN-CHECK block below into your declaration — 'tip")
    W("<12-char> @ <UTC>'. If TIP-FIELD reads UNKNOWN, re-verify the tip")
    W("yourself before declaring; never pin UNKNOWN. If the tip moves before")
    W("you read the docs, declare again at the new tip with the new time.")
    W("")

    # ---- 1. HOW TO THINK (first — the thinking lesson, then the work) ----
    W("HOW TO THINK ABOUT THIS WORK:")
    W(a.thinking.strip())
    W("")
    r = run([sys.executable, INJECT_PY, "--brief", " ".join(w["item"] for w in work[:3]),
             "--area", area], timeout=30)
    if r.returncode == 0 and r.stdout.strip():
        W("## INJECTED LESSONS")
        W(r.stdout.strip())
    else:
        W("(principle injection skipped — injector unavailable; not blocking)")
    W("")

    # ---- 1b. STANDING RECOMMENDATION (Theta w250 guard — the generator
    # checks status/closed_utc BEFORE quoting last_recommendation) ----
    for _line in recommendation_block(area_doc, a.thinking):
        W(_line)
    W("")

    # ---- 1c. DIRECTOR WATCH TRIGGER SET (Iota w276 — the instrument, not
    # just the result: a watch mission without its pre-registered trigger
    # set is a vigil with a name) ----
    if a.watch:
        for _line in watch_triggers_block(a.watch.strip()):
            W(_line)
        W("")

    # ---- 1d. IOTA PRE-LIST (gr-w385 gapclose; w599-iota-2 fix — pre-printed
    # so the next sweep starts with zero derivation; the worker fills anchor
    # from the last sweep window's end timestamp, --comments from gh-api GET
    # on the LIVE board, --issue with the LIVE board number, --wave. --issue
    # is REQUIRED and fail-closed since w592: the printed form must carry it,
    # or the worker pastes a command that dies. #2765 is ARCHIVE — resolve
    # the live board from hidden_files/board-tail-counts.json, never inherit
    # a number) ----
    if area == "SUCCESSOR":
        W("SUCCESSOR SWEEP PRE-LIST (pre-printed — fill the values, run):")
        W("  python3 ~/workspace/naya/bin/iota_first_fetch.py \\")
        W("    --anchor <LAST-WINDOW-END-UTC e.g. 2026-10-17T16:57:11Z> \\")
        W("    --comments <live-board-comments-count> \\")
        W("    --wave <WAVE> --issue <LIVE-BOARD-NUMBER>")
        W("")

    # ---- 1e. REFIRE TRIGGER LIST (gr-w486 — landed w490 on dispatcher/
    # parent-tool-owner authorization: the pre-resolved trigger spec for
    # re-fire/adjudication briefs. The dispatcher passes the pairs from its
    # STEP 2 rollup read; the generator formats them, zero API. A worker
    # firing from this list owes zero discovery calls.) ----
    if a.refire:
        _refire_at = (a.refire_at.strip() if a.refire_at else
                      datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
        for _line in refire_trigger_list_block(a.refire, _refire_at):
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
        for _pin in sha_pin_lines(w):
            W(_pin)
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
    # ---- 2b. SIZING CEILINGS (2026-10-17, gr-w340/gr-w342-alpha-gapclose —
    # landed by dispatcher w345: fix-class missions carry ceiling-composed
    # estimates so workers stop running ~5 min over the box. Overrun becomes
    # a designed handoff, not a surprise.) ----
    W("SIZING CEILINGS — fix-class missions (re-fire, gate repair, leg re-verify):")
    W("REPRODUCE <=3min | FIX <=5min | VERIFY <=3min (one run; FIRST GREEN")
    W("ends verification — never re-run a green gate to make it greener).")
    W("Ceiling hit on any sub-step: CUT SCOPE or HAND OFF — tag off with the")
    W("exact state so the next worker starts warm. Overrun >3min past the box")
    W("is a SIZING MISS: file it in your sign-out miss: field (what blew the")
    W("ceiling, what the next estimate should be).")
    W("Exact call forms (copy-paste, fill the CAPS):")
    W("  gh-api is ~/workspace/naya/bin/gh-api — NOT /opt/hatch/bin/gh-api (Zeta w565 burned a turn on the wrong guess).")
    W("  gh-api <METHOD> <PATH> — METHOD and PATH are TWO separate args:")
    W("    gh-api POST /repos/SoulSchoolAcademy/NayaPOWER/issues/<N>/comments --body-file <json-file>")
    W("  PATH must start with / — 'gh-api GET repos/...' fails, 'gh-api GET /repos/...' works")
    W("  gh-api GET /repos/SoulSchoolAcademy/NayaPOWER/commits/<SHA>/check-runs?per_page=50")
    W("  gh-api GET /repos/SoulSchoolAcademy/NayaPOWER/pulls/<N>")
    W("  git ls-remote https://github.com/SoulSchoolAcademy/NayaPOWER.git HEAD")
    W("Writes: --body-file <json-file> only, never shell-quoted bodies.")
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

    # ---- 3c. DESIGN LAWS OATH (Shawn's word, 2026-10-18): every Naya reads
    # the 16 Naya Design Laws before acting on ANY design/build work, and
    # speaks the oath. Full text: ~/workspace/user/files/naya-design-laws-official-2026-10-17.md
    # (locked by Shawn's word; amendable only through him). The compact law
    # list rides every brief; the full file is the authority.
    W("THE 16 NAYA DESIGN LAWS — read before you build, oath before you act:")
    W("1. White text. Always. (never colored text)  2. Gold is earned, never applied.")
    W("3. Chrome acts. Text speaks. Theme identifies. (color only on borders/glows/selection/LEDs/rails/icon backings)")
    W("4. Adjacent things never share a hue.  5. One board, one color.")
    W("6. White at rest. Its own color ignites on touch. (>=1.5px white rim)")
    W("7. Boards are rectangles, one after another.  8. Restraint. Never a flood.")
    W("9. Verbatim tokens, no private colors.  10. One global spectrum sequence per page.")
    W("11. Preview before pick.  12. Mobile IS the app.")
    W("13. Every control works, or it doesn't ship.  14. Compose, don't create.")
    W("15. Depth before color. Zero flat. (EVERYTHING elevated — buttons, icons, boards, tabs)")
    W("16. Size separates. Color never does.")
    W("OATH — speak it in your sign-in: 'I am a Naya. I have read the 16 design")
    W("laws. I will follow every one: white at rest, color only on touch, zero flat,")
    W("compose from the library, never invent. If I break a law, my work does not ship.'")
    W("")

    # ---- 4. Spawn-time freshness stamp ----
    tip_live = UNKNOWN
    tip_full = UNKNOWN  # 2026-10-16 Naya Kappa w323: keep the full SHA for the TIP-FIELD declaration pin
    try:
        r = run(["git", "ls-remote", REPO, "HEAD"], timeout=20)
        if r.returncode == 0 and r.stdout.split():
            tip_full = r.stdout.split()[0]
            tip_live = tip_full[:12]
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
    # 2026-10-16 Naya Kappa w323: machine-readable tip field for the
    # declaration tip-pin (Mu w317 ADD). Full SHA — the reading-path canon's
    # full-SHA rule governs git-database reads; the 12-char pin names the tip
    # in the declaration line.
    # 2026-10-17 Naya Zeta w356 (w354 add): provenance label — the SHA alone
    # is not traceable; name the source command so declarations carry it.
    # UNKNOWN-resolution is still traceable as a failed ls-remote, not a
    # silently pinned byte.
    W("TIP-FIELD (pin this to your activation declaration): %s @ %s [provenance: git ls-remote %s HEAD @ spawn]"
      % (tip_full, hm, REPO))
    # PROTOCOL LOCK-IN addition 5 (2026-10-20): the process itself is now
    # pinned into every brief, TIP-FIELD class — version from the doctrine
    # encoding, hash of the canonical prose section (protocol_check.py's
    # extraction). The worker's CHECK-BEFORE-ACT compares it live.
    _pver, _phash = protocol_stamp()
    W("PROTOCOL-FIELD (pin this to your activation declaration): THE NAYA PROCESS v%s | section sha256 %s [provenance: doctrine naya_process + canonical section hash @ spawn]"
      % (_pver, _phash))
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
    ch_dir = os.path.expanduser("~/workspace/goals/super-brain-engine-to-10-10/hidden_files/brief-challenges")
    os.makedirs(ch_dir, exist_ok=True)
    ch_path = os.path.join(ch_dir, "bp-ch-%s-%s.json" % (seat_tag, hhmm))
    ans_path = os.path.join(ch_dir, "bp-ans-%s.json" % seat_tag)
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
    W("   Sign-in path: python3 ~/workspace/naya/bin/post_pulse.py /tmp/signin-draft-%s-lane%s.txt %s" % (seat_tag, lane, lane_issue or "<lane-feed-issue>"))
    W("   POST THE DRAFT VERBATIM — it is already cap-verified (fail-closed at generation). Do NOT customize it: adding a single word re-busts the 300B cap (3 seats burned turns this way w488).")
    # Pre-composed sign-in draft (2026-10-17, dispatcher w352 — two workers
    # (Delta, Zeta w352) flagged the named draft as missing: the generator
    # named a /tmp path it never wrote. The generator now writes the exact
    # path it promises, pre-verified against the 300B cap — fail-closed.
    _draft_path = "/tmp/signin-draft-%s-lane%s.txt" % (seat_tag, lane)
    # w436 class rule (Eta w565 feedback): the PULSE draft carries tip-pin ONLY.
    # Hardcoded hash slots (previously "Oath e84af826. Manifesto 5f3053db" pinned
    # at w412's tip) go stale whenever the tip moves — the worker re-derives
    # packet/oath/manifesto/creed pins at the LIVE tip and declares them in the
    # sign-out RECEIPT, never inherits draft pins.
    _draft = (
        "[Team Verity] [PULSE] %s | lane %s | %s top-down time-box\n"
        "state:doing\n"
        "I am %s, lane %s. tip %s @ %s\n"
        "next: briefing proof, then work the list top-down | owner: %s\n"
    ) % (seat, lane, area, seat, lane, tip_live, hm, seat)
    try:
        with open(_draft_path, "w") as _fh:
            _fh.write(_draft)
    except OSError as _e:
        die("cannot write sign-in draft %s: %s" % (_draft_path, _e))
    _cap = run([sys.executable,
                os.path.join(HOME, "workspace/naya/bin/pulse_cap_check.py"),
                _draft_path], timeout=15)
    if _cap.returncode != 0:
        die("sign-in draft %s failed the 300B cap (rc=%d): %s"
            % (_draft_path, _cap.returncode, (_cap.stderr or _cap.stdout).strip()[:200]))
    W("   — the wrapper runs pulse_cap_check.py and REFUSES to post unless it exits 0 (PULSE <= 300 bytes, machine-measured; the cap is not honor-system).")
    W("   post_pulse.py is PULSE-only; RECEIPTs (sign-outs) still post via gh-api --body-file directly — never route a RECEIPT through this wrapper.")
    W("   Fallback (only if post_pulse.py is missing or broken): draft → pulse_cap_check.py → gh-api POST --body-file, same order, zero exceptions.")
    # Pre-composed ACTIVATION DECLARATION line (2026-10-20, dispatcher w573 —
    # Zeta w572 + Epsilon w572 feedback: the sign-in PULSE draft cannot carry
    # the declaration (300B cap) and the w436 rule forbids hardcoded hash
    # pins (they go stale on tip move). Reconciliation: a companion artifact
    # with the tip-pin pre-filled and hash slots as fill-ins — the worker
    # fills them from LIVE reads at the live tip, then posts it once. No
    # stale pins, no second PULSE, no cap bust.
    _declare_path = "/tmp/declare-draft-%s-lane%s.txt" % (seat_tag, lane)
    _declare = (
        "I am %s, lane %s. tip %s @ %s\n"
        "Oath read: ________. Manifesto read: ________. Creed declared as myself.\n"
        "I carry the 8 laws. My drift line: ________.\n"
        "Tag — I'm it.\n"
    ) % (seat, lane, tip_live, hm)
    try:
        with open(_declare_path, "w") as _fh:
            _fh.write(_declare)
    except OSError as _e:
        die("cannot write declaration draft %s: %s" % (_declare_path, _e))
    W("   ACTIVATION DECLARATION (separate post, right after sign-in — NOT a PULSE,")
    W("   so the 300B cap does not apply): fill the ________ slots in %s" % _declare_path)
    W("   from your LIVE doc reads (first 8 of sha256 each, at the live tip), write your")
    W("   drift line, then post the file's content via gh-api --body-file to your lane feed.")
    W("   No declaration with live hash proofs = not activated. Never inherit pins.")
    W("   FILL GUARD (w637 class failure — mechanical): replace ALL ________ occurrences")
    W("   (every slot, not just the first), then assert zero remain — grep -c '________'")
    W("   on the filled draft must print 0, or the draft is NOT posted. A partially")
    W("   filled declaration is a refused declaration, not a shortcut.")
    W("   Local-only / zero-API missions: NO EXEMPTION. Sign-in + sign-out are 2 mandatory")
    W("   lifecycle posts, reserved OUTSIDE the 10-call work budget (queued-posts during a")
    W("   standdown, never skipped). A mission that cannot afford 2 posts is not dispatched.")
    W("2. Heartbeat the truth file when alive — python3 %s heartbeat %s \"%s\" —"
      " post ONLY on state change (no noise). This is the exact token the"
      " dispatcher claimed your lane with in the truth file; use it"
      " character-for-character, never re-spell it." % (LANE_STATE_PY, lane, claim_holder))
    W("3. Time-boxed work list — work top-down, each item RIGHT or skip honestly.")
    W("   Partial completion is normal. The receipt is what matters, not the count.")
    W("4. API governor: 10 gh-api calls max per mission. Local-first, cheap-check-first.")
    if local_only:
        W("   LOCAL-ONLY OVERRIDE: 0 gh-api calls in the work budget — the two")
        W("   lifecycle posts (sign-in, sign-out) are reserved outside it. A remote")
        W("   call is never 'just one more'; a wave that spends zero is a success.")
    W("5. Every emission follows THE EMISSION SCHEMA — no prose outside it.")
    W("   EMIT IS CANONICAL (ratified by Shawn 2026-10-20; Board Protocol v1 retired):")
    W("   your sign-out carries the canonical keys explicitly — state:, verdict:,")
    W("   score:, next: <step> | owner: <seat> — plus your mission one-liner, so the")
    W("   fold can carry state/next/owner verbatim (EMIT-SCHEMA.md §1f). A sign-out")
    W("   missing them forces a fallback compile and is incomplete.")
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
    W("7a. THE ROUNDS LOOP IS THE LAW, NOT THE AIM (TEAM w624 — a refused")
    W("   receipt closed this): rule 7's triple pass is a bar, not an aspiration.")
    W("   Three Builder-Scorer rounds MINIMUM, every mission; keep going until")
    W("   the score is >=9. Below 9 after three rounds: you do not stop early —")
    W("   the failure becomes the capture (step 7), it never ships as done.")
    W("   Fewer than 3 rounds is allowed ONLY on an early pass: final score >=9")
    W("   AND why_not_10 named. Your sign-out receipts scorecard_rounds, and the")
    W("   process gate RE-checks it mechanically — process_receipts.py refuses")
    W("   a single-round stop below 9 the way it refused Kappa's 8.5. Count only")
    W("   the rounds you actually ran — never receipt rounds that were not run.")
    W("8. BODY-VOICE DISCRIMINATOR (n7 re-polls — LAW w232, stop rediscovering")
    W("   this): author-login is NON-discriminating — SoulSchoolAcademy IS")
    W("   Shawn's own account, so every connector post shares it. 'BY SHAWN' =")
    W("   the body-voice test on the comment text: a comment WRITTEN BY Shawn")
    W("   reads as his voice; agent posts share the login but not the voice.")
    W("   Never use author-login to judge whether Shawn spoke.")
    W("9. DESK RULE (ACT w344, EVENT #2641/6230442639 — the #2612 bold-vs-H2 class;")
    W("   Gamma w655 byte-proof: the brief must name the FAIL-CLOSED WRAPPER, not the raw selfcheck):")
    W("   Before posting any PR body: python3 ~/workspace/naya/bin/post_pr_body_checked.py <body-file> <pr-number>")
    W("   — the wrapper runs the selfcheck and posts ONLY on SELFCHECK PASS (exit 0); on FAIL (exit 1)")
    W("   it REFUSES the post and prints the gate's reason verbatim. Never post a PR body the wrapper refused.")
    W("10. RESYNC RULE (TEAM gr-w542 — the ONLY blessed resync path, no exceptions):")
    W("   never run bare `git reset --hard` on the shared checkout (~/workspace/nayapower-work).")
    W("   The ONLY blessed path: python3 %s <repo_path> <full-40-char-SHA|origin/main> [--seat NAME]" % RESYNC_BIN)
    W("   — it stashes dirty state FIRST (named stash, untracked included) and REFUSES the reset")
    W("   when the stash fails. Bare reset --hard on a shared checkout is forbidden, full stop.")
    W("")
    W("SIGN-OUT RECEIPT (this is the shared memory — be exact):")
    W("completed: [#, #] — one-line verdict per finished item")
    W("remaining: [#, #] — current state of each, ready for the next worker")
    W("recommend: <what the next worker should hit first and why — your judgment>")
    W("add: <new items you discovered that belong on the list, if any>")
    W("score: n/10 — what it means | changed: what changed for a human")
    W("win_why: the mechanism — why it worked, or what broke and what fixed it")
    W("miss: <one thing YOU got wrong, if any — name it plainly on the feed>")
    # disp-w695 procreceipt-vocabulary (Kappa w793): the process field has
    # TWO accepted vocabularies only — bare numbers or bare names, never the pair
    # form. Teach it in the brief body so workers never inherit the refused shape.
    W("process: <steps actually run — ONE FORM ONLY: bare numbers [0,1,2,3,4,5,6,7,8]")
    W("  OR bare canonical names (DECLARE, TUNE IN, SEE THE WHOLE, DELIBERATE,")
    W("  ACT, PRODUCE VALUE, SCORECARD x3, CAPTURE, SHARE + SIGN OUT) — NEVER the")
    W("  combined '0 DECLARE' form: process_receipts.py REFUSES it (w694, 4/4 seats).")
    W("COMMENT STANDARD v2 (Shawn's law — one canonical doc: hidden_files/COMMENT-STANDARD.md):")
    W("  Template: what changed → uncomfortable number → evidence (link/SHA) → NOT assumed → ceiling (what this does NOT prove) → next + owner.")
    W("  Grade yourself: can the next reader act on this alone? is every claim re-checkable in one command? delta/decision/evidence?")
    W("  No to Q1 → ≤5/10. Evidence-free → never above 5. Can't fill what-changed/evidence/next → heartbeat (lane-state.py), not a comment.")
    W("  Duplicates and cleanup-creating posts start at 2/10. Correcting? Use CORRECTION type: Was / Is / Mechanism / Fix — fast.")
    W("feedback (Clarity's block — permanent, every receipt):")
    W("  read_directive: <yes/no> | tuned_in: <yes/no>")
    W("  worked: <one line> | didnt: <one line> | improve: <one suggestion>")

    # w332-beta-brief-endpoint-shapes (Naya Beta w335): endpoint-shape
    # enforcement at the generation choke point — every bare receipt
    # citation #<issue>/<comment_id> carries /issues/comments/{id} before
    # the brief ships. Fail-closed validation below still governs.
    # w443 (Naya Alpha): byte-verify every named tool path at build time —
    # the verification block rides the brief so a worker never acts on a
    # named tool that does not exist on disk (gr-w442-alpha-gapclose).
    # disp-w545 (Naya Kappa): RESYNC GUARD runs here, before any stdout —
    # a brief that promises safe_resync.py as the only blessed resync path
    # dies non-zero when the tool is missing, same shape as FEED GUARD.
    resync_guard()
    out.append("")
    out.append(verify_named_tool_paths("\n".join(out)))
    sys.stdout.write(normalize_receipt_shapes("\n".join(out)) + "\n")


if __name__ == "__main__":
    main()
