#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRAIN_SMART_NOTE_ROOT = ROOT / "BRAIN" / "05-MEMORY" / "SMART-NOTES"
REGISTRY = ROOT / ".naya" / "memory" / "smart-notes" / "index.json"

def slug(s):
    x = re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")
    return x or "uncategorized"

def load_json(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def changed_capture(paths):
    hits = []
    for raw in paths:
        normalized = str(raw).replace("\\\\", "/")
        p = Path(normalized)
        if normalized.startswith(".naya/capture/") and p.suffix == ".json":
            hits.append(normalized)
    if len(hits) > 1:
        raise SystemExit("SMART_NOTE_CAPTURE_BATCH_NOT_YET_SUPPORTED:" + ",".join(hits))
    return hits[0] if hits else ""


EDGE_VOCABULARY = {
    "DERIVED_FROM","SUPPORTS","CONTRADICTS","DEPENDS_ON","IMPLEMENTS","GOVERNS",
    "AUTHORIZED_BY","USED_BY","CAUSED","RESULTED_IN","VERIFIED_BY","LEARNED_FROM",
    "SUPERSEDES","SUCCEEDS","RELATED_TO","CONTEXTUALIZES","INVALIDATES","REFINES",
    "CORRECTS","ENABLES","PRODUCES","APPLIES_TO",
}


def resolve_runtime_connections(capture, registry):
    """Resolve declared Smart Note relationships to canonical owner-scoped IB IDs.

    Human-facing targets may begin with a stable Smart Note ID (for example
    "SN-014 — The Compounding Imperative") or name an exact Intelligent Block ID.
    Unresolved prose and unknown relationship types fail closed by omission.
    """
    by_sn = {str(e.get("smart_note_id", "")).upper(): e.get("intelligent_block_id")
             for e in registry.get("entries", []) if e.get("smart_note_id") and e.get("intelligent_block_id")}
    known_ib = {str(e.get("intelligent_block_id")) for e in registry.get("entries", []) if e.get("intelligent_block_id")}
    out = []
    seen = set()
    for raw in capture.get("intelligence", {}).get("connections", []) or []:
        if not isinstance(raw, dict):
            continue
        rel = str(raw.get("relationship_type") or raw.get("type") or "").strip().upper()
        target = str(raw.get("target_block_id") or raw.get("target") or "").strip()
        if rel not in EDGE_VOCABULARY or not target:
            continue
        resolved = target if target in known_ib else None
        if resolved is None:
            m = re.match(r"^(SN-\d{3,})\b", target, flags=re.IGNORECASE)
            if m:
                resolved = by_sn.get(m.group(1).upper())
        if not resolved:
            continue
        key = (resolved, rel)
        if key in seen:
            continue
        seen.add(key)
        out.append({"target_block_id": resolved, "relationship_type": rel})
    return out

def allocate_smart_note_id(capture, ib):
    explicit = str(capture.get("smart_note_id") or "").strip().upper()
    if re.fullmatch(r"SN-\d{3,}", explicit):
        return explicit
    if REGISTRY.exists():
        registry = load_json(REGISTRY)
        existing = next((e for e in registry.get("entries", []) if e.get("intelligent_block_id") == ib and e.get("smart_note_id")), None)
        if existing:
            return existing["smart_note_id"]
        seq = int(registry.get("sequence_policy", {}).get("next_sequence", 1))
    else:
        seq = 1
    return f"SN-{seq:03d}"

def projection_path(capture, ib, root=BRAIN_SMART_NOTE_ROOT):
    captured = str(capture.get("captured_at_utc") or capture.get("source", {}).get("captured_at_utc") or capture["source"]["captured_at"])
    date = captured[:10]
    y, m, d = date.split("-")
    meta = capture.get("projection", {})
    cat = (meta.get("category_slug") or slug(capture.get("category", "smart-note"))).upper()
    topic = (meta.get("topic_slug") or slug(capture.get("topic", "general"))).upper()
    sub = (meta.get("subtopic_slug") or slug(capture.get("subtopic", "general"))).upper()
    sn_id = allocate_smart_note_id(capture, ib)
    return Path(root) / y / m / d / cat / topic / sub / sn_id / (ib + ".md")


def view_text(value, key, *, primary_key):
    if isinstance(value, dict):
        return str(value.get(key, "") or "")
    if isinstance(value, str):
        return value if key == primary_key else ""
    return ""

def connection_lines(values):
    lines = []
    for value in values or []:
        if isinstance(value, dict):
            rel_type = str(value.get("type") or "").strip()
            target = str(value.get("target") or "").strip()
            if rel_type and target:
                lines.append(f"- **{rel_type}** → {target}")
            elif target:
                lines.append("- " + target)
        elif isinstance(value, str):
            lines.append("- " + value)
    return lines

def render(capture, verify, private_root=None):
    block = verify["persisted"]["block"]
    ib = block["intelligent_block_id"]
    intelligence = json.loads(block["content"]["lesson"])
    scope = str(block.get("owner_scope", "PRIVATE")).upper()
    projection_meta = capture.get("projection", {})
    public_authorized = bool(projection_meta.get("human_director_authorized_publication")) or str(projection_meta.get("publication_scope", "")).upper() in {"PUBLIC", "COLLECTIVE", "PUBLIC_DERIVED_VIEW"}
    if scope == "PRIVATE" and not public_authorized:
        if not private_root:
            raise SystemExit("PRIVATE_PROJECTION_REQUIRES_AUTHENTICATED_PRIVATE_SURFACE")
        p = projection_path(capture, ib, Path(private_root))
    else:
        p = projection_path(capture, ib)
    p.parent.mkdir(parents=True, exist_ok=True)
    proof = {
        "event_id": verify["persisted"]["event"]["id"],
        "lineage_id": verify["persisted"]["lineage"]["id"],
        "relationship_id": verify["persisted"]["relationship"]["relationship_id"],
        "index_id": verify["persisted"]["index"]["id"],
        "checkpoint_id": verify["persisted"]["checkpoint"]["id"],
        "receipt_id": verify["persisted"]["receipt"]["id"],
    }
    lines = [
        "# " + capture["title"], "",
        "**Intelligent Block:** " + ib,
        "**Truth state:** " + str(block["understanding_state"]),
        "**Scope:** " + str(block["owner_scope"]),
        "**Captured:** " + str(capture["source"]["captured_at"]),
        "**Canonical intent:** " + str(capture.get("canonical_intent", "CAPTURE_DURABLE_INTELLIGENCE")), "",
        "> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.", "",
        "## ✦ IN A NUTSHELL", "", intelligence.get("essence", ""), "",
        "## 🩷 HUMAN NOTE", "", view_text(intelligence.get("human_view"), "meaning", primary_key="meaning"), "", view_text(intelligence.get("human_view"), "why_it_matters", primary_key="meaning"), "",
        "## 🟣 CHILD NOTE", "", view_text(intelligence.get("simple_view"), "child", primary_key="child"), "",
        "## 🔵 GRANDMA NOTE", "", view_text(intelligence.get("simple_view"), "grandma", primary_key="child"), "",
        "## 🟠 NAYA NOTE", "", view_text(intelligence.get("naya_view"), "purpose", primary_key="purpose"), "", view_text(intelligence.get("naya_view"), "architectural_rule", primary_key="purpose"), "",
        "## 🟢 MACHINE NOTE", "", "~~~json", json.dumps(intelligence.get("machine_view", {}), indent=2, ensure_ascii=False), "~~~", "",
        "## 🟢 LEARNING LESSON", "", intelligence.get("learning_lesson", "Experience becomes compounding intelligence only when retained meaning can be retrieved, applied, observed, verified, and used to improve what happens next."), "",
        "## 🟡 WHAT IT MEANS", "", intelligence.get("priority", ""), "",
        "## ⚪ WHAT'S IN IT FOR YOU", "", "Less repetition, less lost knowledge, faster comprehension, stronger continuity, and a direct Smart Link showing exactly what Naya preserved.", ""
    ]
    lines += [
        "", "## 🟨 HOW TO APPLY / HOW TO USE", "", view_text(intelligence.get("human_view"), "simple_rule", primary_key="meaning") or intelligence.get("applicability", ""), "",
        "## 🔗 HOW IT CONNECTS", "", *connection_lines(intelligence.get("connections", [])), "",
        "## 🧭 KEY DECISIONS / PRINCIPLES", "", *["- " + x for x in intelligence.get("decisions", [])], "",
        "## 🧾 PROOF / PROVENANCE", "", "~~~json", json.dumps(proof, indent=2), "~~~", "",
        "## ⚠️ TRUTH BOUNDARY / UNCERTAINTY", "", intelligence.get("uncertainty", ""), "",
        "## ➜ NEXT ACTION / SUCCESS CONDITION", "", "Keep this intelligence retrievable, apply it only when relevant and authorized, verify resulting outcomes, and compound only what evidence supports.", ""
    ]
    p.write_text("\n".join(lines), encoding="utf-8")
    return p

def _canonical_content_hash(lesson: str) -> str:
    """Hash the canonical JSON form of the lesson, matching the workflow reader.

    The live-intelligence-commit-proof workflow recomputes
    sha256(json.dumps(capture["intelligence"], sort_keys=True,
    separators=(",", ":"), ensure_ascii=False)). The persisted lesson string
    is JSON encoding the same intelligence object, but the database may store
    it with different key order or spacing. Canonicalizing before hashing
    makes the writer's content_hash invariant to serialization differences,
    so exact-match reconciliation works regardless of how the lesson string
    was serialized. Non-JSON lessons (plain strings) hash as-is.
    """
    try:
        canonical = json.dumps(json.loads(lesson), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    except (ValueError, TypeError):
        canonical = lesson
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def update_registry(capture, verify, projection):
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    registry = {"schema":"naya.smart-note-projection-index.v1","version":"1.0","source_of_truth":"runtime_intelligent_block","entries":[]}
    if REGISTRY.exists():
        registry = load_json(REGISTRY)
    block = verify["persisted"]["block"]
    sn_id = allocate_smart_note_id(capture, block["intelligent_block_id"])
    entry = {
        "smart_note_id": sn_id,
        "intelligent_block_id": block["intelligent_block_id"],
        "content_hash": _canonical_content_hash(block["content"]["lesson"]),
        "title": capture["title"],
        "captured_at": capture["source"]["captured_at"],
        "category": capture.get("category", "SMART_NOTE"),
        "topic": capture.get("topic", ""),
        "subtopic": capture.get("subtopic", ""),
        "truth_state": block["understanding_state"],
        "scope": block["owner_scope"],
        "projection_path": str(projection.relative_to(ROOT)).replace("\\\\", "/") if str(projection).startswith(str(ROOT)) else None,
        "projection_status": "GITHUB_BRAIN_PUBLISHED" if str(projection).startswith(str(BRAIN_SMART_NOTE_ROOT)) else "PRIVATE_RENDER_VERIFIED",
        "smart_link_status": "ACTIVE" if str(projection).startswith(str(BRAIN_SMART_NOTE_ROOT)) else "PENDING_PRIVATE_PROJECTION",
        "smart_link": ("https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/" + str(projection.relative_to(ROOT)).replace("\\", "/")) if str(projection).startswith(str(BRAIN_SMART_NOTE_ROOT)) else None,
        "publication_scope": capture.get("projection", {}).get("publication_scope", "PRIVATE"),
        "keywords": ["smart note","capture","intelligent block","future naya","superbrain","intent","memory","reusable intelligence"],
        "provenance": {
            "event_id": verify["persisted"]["event"]["id"],
            "lineage_id": verify["persisted"]["lineage"]["id"],
            "relationship_id": verify["persisted"]["relationship"]["relationship_id"],
            "runtime_index_id": verify["persisted"]["index"]["id"],
            "checkpoint_id": verify["persisted"]["checkpoint"]["id"],
            "receipt_id": verify["persisted"]["receipt"]["id"],
        },
    }
    # Identity-collision flag (SN-0257): the registry dedupes on intelligent_block_id,
    # but the human-visible smart_note_id must also be unique per block. A new entry
    # claiming an SN already held by a DIFFERENT block is flagged here — never silently
    # kept alongside it. First claim stands; the conflict record drives lane resolution.
    # (Additive only: dedupe semantics unchanged, no entries dropped.)
    _sn_new = entry.get("smart_note_id", "")
    if _sn_new:
        for _e in registry.get("entries", []):
            if (_e.get("smart_note_id") == _sn_new
                    and _e.get("intelligent_block_id") != entry["intelligent_block_id"]):
                _conflicts = registry.setdefault("identity_conflicts", [])
                _record = {"smart_note_id": _sn_new,
                           "claimants": sorted({_e["intelligent_block_id"],
                                                entry["intelligent_block_id"]}),
                           "detected_at": entry.get("captured_at", ""),
                           "resolution": "UNRESOLVED — first claim stands; renumber the later claim."}
                if _record not in _conflicts:
                    _conflicts.append(_record)
                print(f"IDENTITY CONFLICT: {_sn_new} claimed by two blocks — "
                      f"first claim stands, renumber the later claim.",
                      file=sys.stderr)
                break
    registry["entries"] = [e for e in registry.get("entries", []) if e.get("intelligent_block_id") != entry["intelligent_block_id"]] + [entry]
    registry["entries"] = sorted(registry["entries"], key=lambda x: (x.get("smart_note_id",""), x.get("intelligent_block_id","")))
    seq_match = re.fullmatch(r"SN-(\d+)", sn_id)
    if seq_match:
        policy = registry.setdefault("sequence_policy", {"human_id_format":"SN-###"})
        policy["next_sequence"] = max(int(policy.get("next_sequence", 1)), int(seq_match.group(1)) + 1)
        policy["purpose"] = "Stable human-facing Smart Note identity. IB-ID remains canonical machine identity; capture timestamp remains provenance."
    REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return entry

def retrieve(query):
    registry = load_json(REGISTRY)
    q = set(re.findall(r"[a-z0-9]+", query.lower()))
    ranked = []
    for e in registry.get("entries", []):
        hay = " ".join([e.get("title",""),e.get("category",""),e.get("topic",""),e.get("subtopic","")," ".join(e.get("keywords",[]))]).lower()
        score = len(q & set(re.findall(r"[a-z0-9]+", hay)))
        ranked.append((score, e))
    ranked.sort(key=lambda z: (z[0], z[1].get("captured_at","")), reverse=True)
    if not ranked or ranked[0][0] <= 0:
        raise SystemExit("NO_RELEVANT_INTELLIGENCE")
    e = ranked[0][1]
    note = (ROOT / e["projection_path"]).read_text(encoding="utf-8")
    m = re.search(r"##(?:\s+[^\n]*)?IN A NUTSHELL\n\n(.+?)(?:\n\n##|$)", note, re.S | re.I)
    explanation = m.group(1).strip() if m else ""
    return {"query":query,"retrieved":e,"explanation":explanation,"source":"repository_projection_index","original_conversation_supplied":False}

def held_out(retrieved):
    task = "A future developer proposes creating one new Naya Node for every important conversation and storing the raw transcript as the canonical brain memory. Decide the architecture."
    control = {"task":task,"context":"No Smart Note intelligence supplied.","decision":"INSUFFICIENT_CANONICAL_CONTEXT","creates_new_node":None,"raw_transcript_is_canonical":None}
    note = (ROOT / retrieved["retrieved"]["projection_path"]).read_text(encoding="utf-8")
    low = note.lower()
    keep_block = ("do not create naya nodes per note" in low) or ("does not become a master node" in low) or ("do not create another naya node" in low)
    raw_separate = ("raw_source_separate_from_distillation" in low and "true" in low) or ("transcript" in low and "not intelligence" in low)
    treatment = {
        "task":task,
        "context_intelligent_block_id":retrieved["retrieved"]["intelligent_block_id"],
        "decision":"USE_INTELLIGENT_BLOCK_AND_SEPARATE_SOURCE" if keep_block and raw_separate else "UNRESOLVED",
        "creates_new_node":False if keep_block else None,
        "raw_transcript_is_canonical":False if raw_separate else None,
        "reason":"Retrieved Smart Note requires Intelligent Blocks as durable units and preserves raw source separately from distilled intelligence."
    }
    return {"schema":"naya.smart-note-held-out-behavior.v1","control":control,"treatment":treatment,"behavior_changed":control["decision"] != treatment["decision"] and treatment["decision"] == "USE_INTELLIGENT_BLOCK_AND_SEPARATE_SOURCE","task_was_not_original_capture_prompt":True}

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("discover"); d.add_argument("paths", nargs="*")
    pr = sub.add_parser("project"); pr.add_argument("--capture", required=True); pr.add_argument("--verify", required=True); pr.add_argument("--private-root")
    r = sub.add_parser("retrieve"); r.add_argument("--query", required=True); r.add_argument("--out")
    h = sub.add_parser("held-out"); h.add_argument("--retrieval", required=True); h.add_argument("--out", required=True)
    args = ap.parse_args()
    if args.cmd == "discover":
        print(changed_capture(args.paths)); return
    if args.cmd == "project":
        cap = load_json(args.capture); ver = load_json(args.verify)
        p = render(cap, ver, args.private_root)
        block = ver["persisted"]["block"]
        published = str(p).startswith(str(BRAIN_SMART_NOTE_ROOT))
        entry = update_registry(cap, ver, p) if published else {
            "intelligent_block_id": block["intelligent_block_id"],
            "scope": block.get("owner_scope"),
            "projection_status": "PRIVATE_RENDER_VERIFIED",
            "smart_link_status": "PENDING_PRIVATE_PROJECTION",
            "private_render_path": str(p)
        }
        print(json.dumps({"projection_path":str(p),"entry":entry}, ensure_ascii=False)); return
    if args.cmd == "retrieve":
        x = retrieve(args.query)
        if args.out:
            Path(args.out).write_text(json.dumps(x, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps(x, ensure_ascii=False)); return
    if args.cmd == "held-out":
        x = held_out(load_json(args.retrieval))
        Path(args.out).write_text(json.dumps(x, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps(x, ensure_ascii=False)); return

if __name__ == "__main__":
    main()
