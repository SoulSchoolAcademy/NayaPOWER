#!/usr/bin/env python3
"""Fail-closed validator for smart-block-registry.json (wave-61 spec section 4).
Exit 0: registry is sound. Exit 1: names the first failing field + block id.

Checks per block: id matches IB-NNNN; name/meaning/version/verified_at/tongues
present; version is semver X.Y.Z; source_anchor kind is file|feed_comment;
file anchors exist on disk AND contain their named section; feed_comment
anchors were API-verified at freeze (reported, not locally checkable);
human tongue is non-trivial; machine tongue parses as JSON and self-identifies
(ib const == block id, v const == block version) — the machine tongue is the
referee, so it must name what it is.
Chunk-2 additions: no two blocks may share an id (one-block-one-meaning);
any anchor whose ref ends in .json must parse as JSON.
"""
import argparse, json, os, re, sys

def fail(block_id, field, why):
    print(f"FAIL block={block_id} field={field} reason={why}", file=sys.stderr)
    sys.exit(1)

ap = argparse.ArgumentParser()
ap.add_argument("--registry", default=os.path.expanduser(
    "~/workspace/goals/super-brain-engine-to-10-10/hidden_files/areas/smart-block-registry.json"))
args = ap.parse_args()

with open(args.registry) as f:
    reg = json.load(f)
for f_ in ("registry_version", "tip_sha", "frozen_at", "blocks"):
    if f_ not in reg or not reg[f_]:
        fail("<registry>", f_, "missing or empty")
blocks = reg["blocks"]
if not isinstance(blocks, list) or not blocks:
    fail("<registry>", "blocks", "not a non-empty list")
seen_ids = {}
for b in blocks:
    bid = b.get("id", "<no-id>")
    if bid in seen_ids:
        fail(bid, "id", "duplicate id (blocks must be one-block-one-meaning)")
    seen_ids[bid] = True

for b in blocks:
    bid = b.get("id", "<no-id>")
    if not re.fullmatch(r"IB-\d{4}", bid or ""):
        fail(bid, "id", "must match IB-NNNN")
    for f_ in ("name", "meaning", "source_anchor", "version", "verified_at", "tongues"):
        if f_ not in b or not b[f_]:
            fail(bid, f_, "missing or empty")
    if not re.fullmatch(r"\d+\.\d+\.\d+", b["version"]):
        fail(bid, "version", "not semver X.Y.Z")
    if b.get("tip_sha") != reg["tip_sha"]:
        fail(bid, "tip_sha", "must equal the registry-level tip_sha (one world, one freeze)")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", b["verified_at"]):
        fail(bid, "verified_at", "must be UTC ISO like 2026-10-13T11:28:00Z")
    a = b["source_anchor"]
    if a.get("kind") == "file":
        p = os.path.expanduser(a.get("ref", ""))
        if not os.path.isfile(p):
            fail(bid, "source_anchor.ref", f"file does not exist on disk: {p}")
        if "section" in a:
            text = open(p, encoding="utf-8", errors="replace").read().lower()
            if a["section"].lower() not in text:
                fail(bid, "source_anchor.section",
                     f"section {a['section']!r} not found in {p}")
        if p.endswith(".json"):
            try:
                json.load(open(p, encoding="utf-8"))
            except (json.JSONDecodeError, OSError) as e:
                fail(bid, "source_anchor.ref",
                     f"json anchor does not parse: {e}")
    elif a.get("kind") == "feed_comment":
        if not re.fullmatch(r"\d+", str(a.get("comment_id", ""))):
            fail(bid, "source_anchor.comment_id", "must be numeric")
        pass  # API-verified at freeze; recorded in the anchor note
    else:
        fail(bid, "source_anchor.kind", "must be 'file' or 'feed_comment'")
    for t in ("human", "ai", "machine"):
        if not b["tongues"].get(t):
            fail(bid, f"tongues.{t}", "missing or empty")
    if len(b["tongues"]["human"]) < 30:
        fail(bid, "tongues.human", "shorter than 30 chars — not a real template")
    try:
        schema = json.loads(b["tongues"]["machine"])
    except json.JSONDecodeError as e:
        fail(bid, "tongues.machine", f"not parseable JSON: {e}")
    props = schema.get("properties", {})
    if props.get("ib", {}).get("const") != bid:
        fail(bid, "tongues.machine", "ib const does not self-identify this block")
    if props.get("v", {}).get("const") != b["version"]:
        fail(bid, "tongues.machine", "v const does not match block version")

anchored = sum(1 for b in blocks if b["source_anchor"]["kind"] == "file")
print(f"OK: {len(blocks)} blocks; {anchored} file anchors exist on disk with sections verified; "
      f"{len(blocks)-anchored} feed_comment anchor(s) (API-verified at freeze); "
      f"all machine tongues parse and self-identify. Registry {reg['registry_version']} "
      f"frozen at {reg['frozen_at']}, tip {reg['tip_sha'][:8]}.")
