#!/usr/bin/env python3
"""SN-0460 "Index the Lesson" enforcement gate.

Law: captured != retrievable. A captured Smart Note that has no index entry
or cannot be retrieved by the retrieval corpus is NOT LEARNED. It is archived.

Checks for a given Smart Note (by SN id):
  I1  Lesson-index entry present AND retrieval-ready
      (.naya/index/lesson-index-20261006.json, falling back to the
      projection index for older notes):
      content.title/essence/lesson (weight-A), applicable_scope (weight-B),
      disposition set; GATE dispositions must name a falsifier.
  I2  Corpus presence: an intelligent block in nayanet_intelligent_blocks
      references the SN.
  I3  Weighted retrievability: the note's core terms live in the
      retrieval-weighted fields (A: title/essence/summary, B: lesson/
      applicability), not only in unweighted prose. Runs against the
      index entry itself when no corpus row is available yet.

Modes:
  repo    (default)  I1 only. CI-safe, stdlib, no credentials.
  corpus             I1 + I2 + I3 via a --corpus-json dump or --corpus-live
                     (read-only Supabase skill). If the corpus is
                     unreachable, exits 2 (cannot verify) -- never a
                     silent pass.

Exit codes: 0 = PASS (indexed and retrievable); 1 = FAIL (not learned);
            2 = usage or infrastructure error.

Usage:
  python3 scripts/gate-lesson-index.py SN-0500 [--mode repo|corpus]
      [--index PATH] [--corpus-json PATH] [--corpus-live] [--self-test]

Follows the drift-tripwire pattern: stdlib only, exit-code contract,
suitable for CI.
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import subprocess
import sys
import urllib.request

REPO = "SoulSchoolAcademy/NayaPOWER"
# Primary: the lesson index (43 triaged notes, corpus-shaped entries).
LESSON_INDEX_PATH = ".naya/index/lesson-index-20261006.json"
LESSON_INDEX_REF = "naya5/lesson-index-20261006"  # -> main after PR merge
# Fallback: the projection index (older notes).
PROJ_INDEX_PATH = ".naya/memory/smart-notes/index.json"
API = "https://api.github.com"

# Retrieval weighting contract (mirrors the cold-retrieve migration):
#   A = title/essence/summary/name ; B = text/lesson/decision/observation +
#   applicable_scope ; C = full content catch-all.
A_FIELDS = ("title", "essence", "summary", "name")
B_FIELDS = ("text", "lesson", "decision", "observation", "applicable_scope")

REQUIRED_INDEX_FIELDS = ("topic", "keywords", "smart_link", "canonical_brain_path")

SN_RE = re.compile(r"^SN-0*(\d+)$", re.IGNORECASE)


def fail(msg):
    print(f"GATE-INDEX FAIL: {msg}")
    return 1


def ok(msg):
    print(f"GATE-INDEX PASS: {msg}")
    return 0


def norm_sn(sn):
    m = SN_RE.match(sn.strip())
    if not m:
        return None
    return f"SN-{int(m.group(1)):03d}"


def load_index_local(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except OSError:
        return None


def load_index_api(path, ref="main"):
    url = f"{API}/repos/{REPO}/contents/{path}?ref={ref}"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.load(r)
        return json.loads(base64.b64decode(d["content"]).decode("utf-8"))
    except Exception as e:  # noqa: BLE001 - surfacing as infra error is the contract
        return None


def find_entry(index, sn):
    """Search lesson-index entries first, then projection-index entries."""
    want = norm_sn(sn)
    if index is None:
        return None, None
    entries = index.get("entries", [])
    for e in entries:
        got = norm_sn(str(e.get("smart_note_id", "")))
        if got == want:
            # lesson-index shape: content.{title,essence,lesson,...}
            # projection-index shape: flat title/keywords
            kind = "lesson" if isinstance(e.get("content"), dict) else "projection"
            return e, kind
    return None, None


def check_i1(entry, kind, sn):
    """Index entry present and retrieval-ready."""
    if entry is None:
        return fail(f"{sn}: no entry in any lesson index -- "
                    "captured but unindexed (NOT LEARNED)")
    if kind == "lesson":
        content = entry.get("content") or {}
        missing = [f for f in ("title", "essence", "lesson")
                   if not str(content.get(f, "")).strip()]
        if not entry.get("applicable_scope"):
            missing.append("applicable_scope")
        disp = str(content.get("disposition", "")).strip()
        if not disp:
            missing.append("disposition")
        if missing:
            return fail(f"{sn}: lesson-index entry degraded, empty: "
                        f"{', '.join(missing)}")
        extra = ""
        if disp == "GATE" and not str(content.get("falsifier", "")).strip():
            return fail(f"{sn}: GATE disposition with no falsifier -- "
                        "unenforceable")
        if disp == "GATE":
            extra = f", gate_status={content.get('gate_status', '?')}"
        return ok(f"{sn}: lesson-index entry retrieval-ready "
                  f"(disposition={disp}{extra})")
    # projection-index fallback
    missing = [f for f in REQUIRED_INDEX_FIELDS if not entry.get(f)]
    if missing:
        return fail(f"{sn}: projection-index entry degraded, empty fields: "
                    f"{', '.join(missing)}")
    return ok(f"{sn}: projection-index entry retrieval-ready "
              f"(topic={entry['topic']})")


def load_corpus_json(path):
    try:
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
        return d if isinstance(d, list) else d.get("rows", [])
    except OSError as e:
        print(f"GATE-INDEX ERROR: cannot read corpus json: {e}", file=sys.stderr)
        return None


def load_corpus_live(sn):
    """Read-only targeted probe: fetch corpus blocks referencing the SN.

    Targeted server-side (ILIKE) so the result stays small; the skill
    truncates very long outputs, so we never SELECT * over the corpus.
    """
    import os
    sb = os.path.expanduser("~/workspace/skills/supabase/bin/sb-api")
    if not os.path.exists(sb):
        print("GATE-INDEX ERROR: sb-api skill not available", file=sys.stderr)
        return None
    num = norm_sn(sn)[3:]  # digits without padding, e.g. "471"
    # Match SN-0471, SN471, SN_0471 in content or block id, any zero-padding.
    pat = f"%SN-{num}%"
    pat2 = f"%SN{int(num)}%"
    pat3 = f"%SN_{num}%"
    q = ("SELECT intelligent_block_id, understanding_state, content, "
         "applicable_scope FROM nayanet_intelligent_blocks "
         "WHERE status IN ('ACTIVE','DURABLE','RELEASED') AND ("
         f"content::text ILIKE '{pat}' OR content::text ILIKE '{pat2}' "
         f"OR intelligent_block_id ILIKE '{pat}' "
         f"OR intelligent_block_id ILIKE '{pat2}' "
         f"OR intelligent_block_id ILIKE '{pat3}') LIMIT 10;")
    cmd = [sb, "POST",
           "/v1/projects/dahisasgpfvziswqvmvm/database/query",
           json.dumps({"query": q})]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        print("GATE-INDEX ERROR: corpus query timed out", file=sys.stderr)
        return None
    if p.returncode != 0:
        print(f"GATE-INDEX ERROR: corpus query failed: {p.stderr[:200]}",
              file=sys.stderr)
        return None
    try:
        d = json.loads(p.stdout)
        return d if isinstance(d, list) else d.get("data", [])
    except json.JSONDecodeError:
        print("GATE-INDEX ERROR: corpus query returned non-JSON", file=sys.stderr)
        return None


def block_text(block):
    content = block.get("content") or {}
    if isinstance(content, str):
        try:
            content = json.loads(content)
        except json.JSONDecodeError:
            content = {"text": content}
    scope = block.get("applicable_scope") or {}
    return content, scope


def find_block(rows, sn):
    """Find a corpus block referencing the SN id (any zero-padding)."""
    num = norm_sn(sn)[3:]
    patterns = [re.compile(r"SN-0*" + num + r"\b", re.IGNORECASE),
                re.compile(r"sn0*" + num + r"\b", re.IGNORECASE)]
    for b in rows:
        content, _ = block_text(b)
        blob = json.dumps(content)
        bid = str(b.get("intelligent_block_id", ""))
        if any(p.search(blob) or p.search(bid) for p in patterns):
            return b
    return None


def core_terms(entry, kind):
    """Terms a cold successor would plausibly query."""
    terms = set()
    if kind == "lesson":
        content = entry.get("content") or {}
        for f in ("title", "essence", "lesson", "topic"):
            for w in re.findall(r"[a-zA-Z]{4,}", str(content.get(f, ""))):
                terms.add(w.lower())
        scope = entry.get("applicable_scope") or {}
        for tc in scope.get("trigger_conditions", []) or []:
            for w in re.findall(r"[a-zA-Z]{4,}", str(tc)):
                terms.add(w.lower())
    else:
        for w in re.findall(r"[a-zA-Z]{4,}", str(entry.get("title", ""))):
            terms.add(w.lower())
        kw = entry.get("keywords") or []
        if isinstance(kw, str):
            kw = [kw]
        for k in kw:
            for w in re.findall(r"[a-zA-Z]{4,}", str(k)):
                terms.add(w.lower())
    stop = {"smart", "note", "naya", "system", "with", "from", "that", "this",
            "into", "have", "will", "when"}
    return {t for t in terms if t not in stop}


def check_i2(block, sn):
    if block is None:
        return fail(f"{sn}: no intelligent block in retrieval corpus -- "
                    "captured but not corpus-present (NOT LEARNED)")
    state = block.get("understanding_state", "?")
    return ok(f"{sn}: corpus block {block.get('intelligent_block_id')} "
              f"(state={state})")


def check_i3(block, entry, kind, sn):
    """Core terms must live in A- or B-weighted fields, not just C catch-all.

    When checking the lesson index itself (no DB row yet), the entry's own
    content is validated against the weighting contract: title/essence/lesson
    feed weight-A, applicable_scope feeds weight-B.
    """
    terms = core_terms(entry, kind)
    if not terms:
        return fail(f"{sn}: index entry has no usable core terms")
    if block is not None:
        content, scope = block_text(block)
    elif kind == "lesson":
        content, scope = (entry.get("content") or {}), (entry.get("applicable_scope") or {})
    else:
        content = {"title": entry.get("title", ""),
                   "text": " ".join(entry.get("keywords") or [])}
        scope = {}
    a_text = " ".join(str(content.get(f, "")) for f in A_FIELDS).lower()
    b_text = " ".join(str(content.get(f, "")) for f in B_FIELDS).lower()
    b_text += " " + json.dumps(scope).lower()
    a_hits = {t for t in terms if t in a_text}
    b_hits = {t for t in terms if t in b_text}
    if a_hits or b_hits:
        src = "corpus block" if block is not None else "index entry"
        return ok(f"{sn}: retrievable from {src} -- {len(a_hits)} A-weighted + "
                  f"{len(b_hits)} B-weighted term hits "
                  f"({sorted(a_hits | b_hits)[:6]})")
    return fail(f"{sn}: core terms absent from weighted fields "
                f"(A:{A_FIELDS} B:{B_FIELDS}) -- unretrievable by ranked query")


def run_one(sn, index, corpus_rows, corpus_live_sn=None):
    entry, kind = find_entry(index, sn)
    rc = check_i1(entry, kind, sn)
    if rc != 0:
        return rc
    # I3 can run against the index entry itself (weighting contract check).
    # I2 needs the live corpus; if corpus_rows was provided use it, else
    # do a targeted live probe when requested.
    block = None
    if corpus_rows is not None:
        block = find_block(corpus_rows, sn)
        rc = check_i2(block, sn)
        if rc != 0:
            return rc
    elif corpus_live_sn:
        rows = load_corpus_live(sn)
        if rows is None:
            return 2
        block = find_block(rows, sn)
        rc = check_i2(block, sn)
        if rc != 0:
            return rc
    return check_i3(block, entry, kind, sn)


def self_test():
    """Falsifier battery. Every case asserts the gate's verdict."""
    failures = []

    def expect(name, got, want):
        status = "ok" if got == want else "MISMATCH"
        print(f"  [{status}] {name}: got={got} want={want}")
        if got != want:
            failures.append(name)

    lesson_idx = {"entries": [
        {"smart_note_id": "SN-900",
         "content": {"title": "Idempotency Keys Must Never Be Null",
                     "essence": "A null idempotency key disables replay protection",
                     "lesson": "Reject null keys fail-closed at the boundary",
                     "topic": "SAFETY",
                     "disposition": "GATE",
                     "falsifier": "null key accepted",
                     "gate_status": "BUILT"},
         "applicable_scope": {"task_classes": ["safety"],
                              "trigger_conditions": ["replay protection"]},
         "status": "ACTIVE", "understanding_state": "INDEXED"},
        {"smart_note_id": "SN-901",
         "content": {"title": "Degraded", "essence": "", "lesson": ""},
         "applicable_scope": {}, "disposition": ""},
    ]}
    corpus = [
        {"intelligent_block_id": "IB-SN-900",
         "understanding_state": "VERIFIED",
         "content": {"title": "Idempotency Keys Must Never Be Null",
                     "essence": "A null idempotency key disables replay protection",
                     "lesson": "Reject null keys fail-closed at the boundary"},
         "applicable_scope": {"domain": "safety"}},
    ]

    print("T1: unindexed SN fails I1")
    expect("T1", run_one("SN-999", lesson_idx, None), 1)

    print("T2: degraded lesson-index entry fails I1")
    expect("T2", run_one("SN-901", lesson_idx, None), 1)

    print("T3: GATE disposition with no falsifier fails I1")
    idx3 = {"entries": [dict(lesson_idx["entries"][0],
                             smart_note_id="SN-903")]}
    idx3["entries"][0]["content"] = dict(
        idx3["entries"][0]["content"], falsifier="")
    expect("T3", run_one("SN-903", idx3, None), 1)

    print("T4: indexed entry, repo mode (I1+I3 on entry) -> PASS")
    expect("T4", run_one("SN-900", lesson_idx, None), 0)

    print("T5: corpus block present -> I2+I3 PASS")
    expect("T5", run_one("SN-900", lesson_idx, corpus), 0)

    print("T6: corpus mode, no block for SN -> fails I2")
    expect("T6", run_one("SN-900", lesson_idx, []), 1)

    print("T7: malformed SN id -> usage error path")
    expect("T7", 2 if norm_sn("bogus") is None else 0, 2)

    if failures:
        print(f"SELF-TEST FAILED: {failures}")
        return 1
    print("SELF-TEST 7/7 green")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="SN-0460 lesson-index gate")
    ap.add_argument("sn", nargs="?", help="Smart Note id, e.g. SN-0500")
    ap.add_argument("--mode", choices=["repo", "corpus"], default="repo",
                    help="repo: I1+I3 on the index (CI-safe). "
                         "corpus: also I2 against the live corpus.")
    ap.add_argument("--lesson-index", default=None,
                    help="path to lesson-index JSON (default: fetch from "
                         f"{LESSON_INDEX_REF})")
    ap.add_argument("--lesson-ref", default=LESSON_INDEX_REF,
                    help="git ref for lesson-index API fetch")
    ap.add_argument("--corpus-json", default=None,
                    help="JSON dump of corpus rows (list or {rows:[...]})")
    ap.add_argument("--corpus-live", action="store_true",
                    help="targeted live-DB probe via sb-api skill (read-only)")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)

    if a.self_test:
        return self_test()
    if not a.sn:
        ap.error("SN id required (or --self-test)")
    sn = norm_sn(a.sn)
    if not sn:
        print(f"GATE-INDEX ERROR: malformed SN id {a.sn!r}", file=sys.stderr)
        return 2

    index = (load_index_local(a.lesson_index) if a.lesson_index
             else load_index_api(LESSON_INDEX_PATH, a.lesson_ref))
    if index is None:
        # fall back to the projection index on main for older notes
        index = load_index_api(PROJ_INDEX_PATH, "main")
    if index is None:
        print("GATE-INDEX ERROR: cannot load any lesson index", file=sys.stderr)
        return 2

    corpus_rows = None
    corpus_live = False
    if a.mode == "corpus":
        if a.corpus_json:
            corpus_rows = load_corpus_json(a.corpus_json)
            if corpus_rows is None:
                return 2
        elif a.corpus_live:
            corpus_live = True
        else:
            print("GATE-INDEX ERROR: corpus mode needs --corpus-json or "
                  "--corpus-live", file=sys.stderr)
            return 2

    return run_one(sn, index, corpus_rows, corpus_live_sn=corpus_live)


if __name__ == "__main__":
    sys.exit(main())
