#!/usr/bin/env python3
"""The door obligation: a Smart Note page may not land without its records.

The intelligence door (direct writes to main) owes a mechanical obligation
for every note it lands, in the SAME push:

    capture  (.naya/capture/<IB>.json)
    registry (.naya/memory/smart-notes/index.json entry)
    index    (tools/regenerate_brain_index.py output)

On 2026-10-21 the obligation was skipped repeatedly: door writes landed
BRAIN projection pages with no capture and no registry entry, the vanished-id
set grew 5 -> 11 in ~2 hours, and main's own guard battery
(test_brain_index_freshness / test_smart_note_registry_drift /
test_ratified_intelligence_cannot_vanish) stayed red no matter how often
cure PRs expanded — PR #2831's falsifiers (comments 6325348465, 6326451724)
root-caused it: cure PRs cannot outrun the door. Per Shawn's House-Fire Law
(2026-10-21 ~22:28Z — "if a failure can be prevented by an automation,
build the automation"), this tool is the prevention:

  CHECK  (default) — for every published IB page on the tree, verify the
         capture exists, the registry entry exists, and the hashes bind
         (entry.content_hash == hash of the capture's intelligence;
         entry.page_hash == sha256 of the page bytes). Also reports the
         tombstone class: ids present in git history with no page, no
         capture and no registry entry (removed fixtures such as
         SN-9998/SN-9999). Every defect prints one self-explaining line:
         MISSING: ... — CURE: ... (owner: ...)

  FIX    (--fix) — generate the missing capture + registry entry for a
         page FROM THE PAGE ITSELF, using tools/smart_note_v2.py's own
         hash functions (single hashing authority — never a second
         implementation). Provenance is honest by construction: the
         entry names the actual publishing commit (earliest add in git
         history, plus the restore commit when the page was deleted and
         restored), and both records declare themselves a mechanical
         backfill derived from the published projection only. No runtime
         provenance is invented. The fixer REFUSES to fabricate records
         for an id with no page on disk — that class belongs to the LAW
         lane (lifecycle tombstone or guard carve-out), never to a
         backfill.

Usage:
  python3 tools/check_door_obligation.py [--root DIR] [--json]
  python3 tools/check_door_obligation.py --range A..B      # delta (door pre-push / CI)
  python3 tools/check_door_obligation.py --fix [--ids SN-0810,SN-0811] [--with-regen]

Exit codes: 0 = obligation met for everything in scope; 1 = defects found;
2 = machinery error (fail closed).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRAIN_NOTES_REL = Path("BRAIN/05-MEMORY/SMART-NOTES")
CAPTURE_REL = Path(".naya/capture")
REGISTRY_REL = Path(".naya/memory/smart-notes/index.json")

BACKFILL_DATE = None  # set from --date or today (UTC) at runtime


def _load_snv2(root: Path):
    """Load tools/smart_note_v2.py from the target root (single hash authority)."""
    spec = importlib.util.spec_from_file_location(
        "smart_note_v2", root / "tools" / "smart_note_v2.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_sn_claims(root: Path):
    """Load tools/sn_claims.py from the target root (single claim authority)."""
    spec = importlib.util.spec_from_file_location(
        "sn_claims", root / "tools" / "sn_claims.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _git(root: Path, *args: str) -> str | None:
    try:
        r = subprocess.run(["git", *args], cwd=root, capture_output=True,
                           timeout=120)
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode != 0:
        return None
    return r.stdout.decode("utf-8", "replace")


# --------------------------------------------------------------------------
# Page parsing — the door writes three dialects of the nine-section page:
#   plain:   ## IN A NUTSHELL / HUMAN / CHILD / GRANDMA / NAYA / MACHINE / ...
#   verbose: ## THE HUMAN VERSION / FOR A CHILD / FOR GRANDMA / ...
#   emoji:   ## ✦ IN A NUTSHELL / 🩷 HUMAN NOTE / 🟣 CHILD NOTE / ...
# Headers are normalized (symbols stripped, uppercased) and mapped by alias.
# --------------------------------------------------------------------------

_SECTION_ALIASES = {
    "IN A NUTSHELL": "essence",
    "HUMAN": "human_view",
    "THE HUMAN VERSION": "human_view",
    "HUMAN NOTE": "human_view",
    "CHILD": "simple_view",
    "FOR A CHILD": "simple_view",
    "CHILD NOTE": "simple_view",
    "GRANDMA": "grandma_view",
    "FOR GRANDMA": "grandma_view",
    "GRANDMA NOTE": "grandma_view",
    "NAYA": "naya_view",
    "FOR NAYA": "naya_view",
    "NAYA NOTE": "naya_view",
    "MACHINE": "machine",
    "FOR THE MACHINE": "machine",
    "MACHINE NOTE": "machine",
    "WHAT IT ALL MEANS": "meaning",
}

_SN_DIR_RE = re.compile(r"^SN-\d{3,}$")
_SN_IN_IB_RE = re.compile(r"(?i)sn(\d{3,4})")


def _norm_header(raw: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9 ]+", " ", raw)
    return re.sub(r"\s+", " ", cleaned).strip().upper()


def _meta(text: str, label: str) -> str | None:
    m = re.search(rf"\*\*{re.escape(label)}:\*\*\s*(.+)", text)
    return m.group(1).strip() if m else None


def parse_page(path: Path, root: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    rel = str(path.relative_to(root)).replace("\\", "/")
    parts = Path(rel).parts

    title_m = re.search(r"^#\s+(.+)$", text, flags=re.M)
    # Identity is the FILENAME stem — the same key audit_registry uses.
    # In-page metadata can name a re-stamped IB (e.g. SN-0339's page file is
    # ...20260930... while its capture was re-stamped ...20261005...);
    # keying on metadata manufactures false defects.
    ib = path.stem

    sn = None
    for part in parts:
        if _SN_DIR_RE.match(part):
            sn = part
    if sn is None:  # non-numeric id families (e.g. SN-NET-POWER-MAGIC-001)
        for part in parts:
            if part.startswith("SN-"):
                sn = part
                break
    if sn is None:
        m = _SN_IN_IB_RE.search(ib)
        if m:
            sn = "SN-" + m.group(1).zfill(3) if len(m.group(1)) <= 3 else "SN-" + m.group(1)

    created = _meta(text, "Created") or _meta(text, "Captured") or ""
    date_m = re.search(r"\d{4}-\d{2}-\d{2}", created)
    if date_m:
        captured_at = date_m.group(0)
    else:  # fall back to the filing path's date segments
        dm = re.search(r"/(\d{4})/(\d{2})/(\d{2})/", rel)
        captured_at = f"{dm.group(1)}-{dm.group(2)}-{dm.group(3)}" if dm else ""

    sections: dict[str, str] = {}
    current: str | None = None
    buf: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            if current:
                sections[current] = "\n".join(buf).strip()
            key = _SECTION_ALIASES.get(_norm_header(line[3:]))
            current = key
            buf = []
        elif current:
            buf.append(line)
    if current:
        sections[current] = "\n".join(buf).strip()

    # Taxonomy from the filing path: .../YYYY/MM/DD/<cat>/<sub>/SN-####/<IB>.md
    taxonomy: list[str] = []
    if "SMART-NOTES" in parts:
        i = parts.index("SMART-NOTES")
        taxonomy = [p for p in parts[i + 4:-2]]  # skip YYYY/MM/DD and SN dir + file
    category = taxonomy[0].upper() if taxonomy else "SMART_NOTE"
    subtopic = taxonomy[1].upper().replace("-", "_") if len(taxonomy) > 1 else ""

    return {
        "path": rel,
        "ib": ib,
        "sn": sn,
        "title": title_m.group(1).strip() if title_m else ib,
        "captured_at": captured_at,
        "truth_state": (_meta(text, "Truth state") or "CANDIDATE").upper(),
        "scope": (_meta(text, "Scope") or "PRIVATE").upper(),
        "category": category,
        "topic": category,
        "subtopic": subtopic,
        "sections": sections,
    }


def discover_pages(root: Path) -> tuple[list[dict], list[dict]]:
    """Return (canonical pages, twin warnings). Pages are IB-*.md files;
    when one IB is published at two paths, the conventional-layout path
    (fewest taxonomy segments) is canonical and the other is a warning —
    the canonical-home question belongs to the SN lane, not this tool."""
    brain = root / BRAIN_NOTES_REL
    by_ib: dict[str, list[dict]] = {}
    if brain.exists():
        for p in sorted(brain.rglob("IB-*.md")):
            page = parse_page(p, root)
            by_ib.setdefault(page["ib"], []).append(page)
    pages, twins = [], []
    for ib, group in sorted(by_ib.items()):
        group.sort(key=lambda g: (len(g["path"].split("/")), g["path"]))
        pages.append(group[0])
        for extra in group[1:]:
            twins.append({"ib": ib, "canonical": group[0]["path"],
                          "twin": extra["path"], "sn": extra["sn"]})
    pages.sort(key=lambda g: g["path"])
    return pages, twins


# --------------------------------------------------------------------------
# Registry / capture state
# --------------------------------------------------------------------------

def load_registry(root: Path) -> dict:
    p = root / REGISTRY_REL
    if not p.exists():
        return {"entries": []}
    return json.loads(p.read_text(encoding="utf-8"))


def capture_path(root: Path, ib: str) -> Path:
    return root / CAPTURE_REL / f"{ib}.json"


def intelligence_hash(snv2, capture_doc: dict) -> str:
    return snv2._canonical_content_hash(json.dumps(
        capture_doc["intelligence"], sort_keys=True,
        separators=(",", ":"), ensure_ascii=False))


class CaptureIndex:
    """All captures on disk, indexed the way the corpus actually binds
    them: by intelligence content hash (the audit's binding), by declared
    projection_path, and by intelligent_block_id. Capture FILENAMES are
    not identity — re-stamped captures carry a different IB date than the
    page they belong to (SN-0339/SN-0342 class)."""

    def __init__(self, root: Path, snv2):
        self.by_hash: dict[str, dict] = {}
        self.by_projection: dict[str, dict] = {}
        self.by_ib: dict[str, dict] = {}
        cap_dir = root / CAPTURE_REL
        if cap_dir.exists():
            for p in sorted(cap_dir.glob("*.json")):
                try:
                    doc = json.loads(p.read_text(encoding="utf-8"))
                except (ValueError, UnicodeDecodeError):
                    continue
                if not isinstance(doc.get("intelligence"), dict):
                    continue
                doc = dict(doc)
                doc["_file"] = p.name
                self.by_hash[intelligence_hash(snv2, doc)] = doc
                intel = doc["intelligence"]
                pp = intel.get("projection_path")
                if isinstance(pp, str) and pp:
                    self.by_projection[pp] = doc
                cib = intel.get("intelligent_block_id")
                if isinstance(cib, str) and cib:
                    self.by_ib[cib] = doc

    def for_page(self, page: dict) -> dict | None:
        return (self.by_projection.get(page["path"])
                or self.by_ib.get(page["ib"]))

    def with_hash(self, h: str | None) -> dict | None:
        return self.by_hash.get(h) if h else None


# --------------------------------------------------------------------------
# Check
# --------------------------------------------------------------------------

_CURE_LIVE = ("run `python3 tools/check_door_obligation.py --fix --ids {sn}` "
              "and commit the generated capture + registry entry + "
              "`python3 tools/regenerate_brain_index.py` output in the SAME push")
_OWNER = "door lane for new writes; cure lane for backfill"


def check_pages(root: Path, snv2, pages: list[dict], registry: dict,
                cap_index: CaptureIndex) -> list[dict]:
    entries = {e.get("intelligent_block_id"): e for e in registry.get("entries", [])}
    defects = []
    for page in pages:
        sn, ib = page["sn"], page["ib"]
        entry = entries.get(ib)
        capture_doc = cap_index.for_page(page)
        if entry is None:
            defects.append({
                "sn": sn, "ib": ib, "kind": "NO_ENTRY", "path": page["path"],
                "missing": f"registry entry for {sn} — page {page['path']} is "
                           f"absent from .naya/memory/smart-notes/index.json",
                "cure": _CURE_LIVE.format(sn=sn), "owner": _OWNER,
            })
            if capture_doc is None:
                defects.append({
                    "sn": sn, "ib": ib, "kind": "NO_CAPTURE", "path": page["path"],
                    "missing": f"capture for {sn} — page {page['path']} has no "
                               f"capture record on disk (.naya/capture/)",
                    "cure": _CURE_LIVE.format(sn=sn), "owner": _OWNER,
                })
        if entry is not None and entry.get("content_hash"):
            # The binding the guards measure: some capture on disk must
            # hash to the entry's content_hash. Hashless legacy entries
            # (the drift test's pinned entries_without_hash class) are a
            # separate, already-ratcheted debt — not re-litigated here.
            if cap_index.with_hash(entry["content_hash"]) is None:
                defects.append({
                    "sn": sn, "ib": ib, "kind": "HASH_MISMATCH", "path": page["path"],
                    "missing": f"hash binding for {sn} — no capture on disk "
                               f"hashes to the registry entry's content_hash",
                    "cure": "reconcile capture and entry from the published "
                            "page; if the capture is human-authored, a human "
                            "lane re-stamps the entry — never overwrite a "
                            "capture mechanically",
                    "owner": "cure lane",
                })
            page_bytes_hash = snv2._page_file_hash(root / page["path"])
            if entry.get("page_hash") != page_bytes_hash:
                defects.append({
                    "sn": sn, "ib": ib, "kind": "PAGE_HASH_STALE", "path": page["path"],
                    "missing": f"page binding for {sn} — registry page_hash "
                               f"does not match the published page bytes",
                    "cure": "re-stamp the entry's page_hash from the page and "
                            "recompute corpus_manifest_hash (the fixer does "
                            "this only for entries it generated)",
                    "owner": "cure lane",
                })
    return defects


def filing_warnings(root: Path, registry: dict, scoped_pages: list[dict],
                    range_spec: str | None) -> list[dict]:
    """WARN-level (P1) filing-guard checks — they never change the exit
    code; they name drift while it is still cheap to cure.

    COUNTER_STALE: the registry's next_sequence counter points at or
    below an occupied number. The counter is advisory display only (the
    allocator in tools/smart_note_v2.py, claimed through
    tools/sn_claims.py, is the numbering authority) — a stale counter is
    how hand-numbering lanes reissue an occupied id.

    UNCLAIMED_NUMBER (range mode only — a filing in flight): a page in
    the range carries a number with no claim anchored on the sn-claims
    branch, i.e. claim-before-author was skipped. The pre-guard corpus
    is not re-litigated: full-tree mode does not raise this warning.
    """
    warnings: list[dict] = []
    try:
        claims_mod = _load_sn_claims(root)
    except Exception as exc:  # guard unreadable: warn, never fail the door
        return [{"kind": "CLAIMS_UNREADABLE",
                 "detail": f"tools/sn_claims.py could not be loaded ({exc}) — "
                           f"filing-guard warnings skipped this run",
                 "cure": "restore tools/sn_claims.py; the filing guard must "
                         "not run blind",
                 "owner": "SN lane"}]
    occupied = claims_mod.occupied_numbers(registry)
    if claims_mod.counter_is_stale(registry):
        warnings.append({
            "kind": "COUNTER_STALE",
            "detail": f"registry next_sequence "
                      f"{claims_mod.counter_value(registry)} points at or "
                      f"below occupied SN-{max(occupied):03d} — the counter "
                      f"is advisory only; the allocator is the numbering "
                      f"authority",
            "cure": "never hand-number from the counter; claim via "
                    "tools/sn_claims.py (repair display with "
                    "`sn_claims.py repair-counter`)",
            "owner": "SN lane",
        })
    if range_spec:
        try:
            claims = claims_mod.read_claims(root)
        except Exception as exc:
            warnings.append({
                "kind": "CLAIMS_UNREADABLE",
                "detail": f"the sn-claims branch could not be read ({exc}) — "
                          f"unclaimed-number check skipped this run",
                "cure": "restore the sn-claims branch; claims are the "
                        "filing door's occupancy anchor",
                "owner": "SN lane",
            })
            return warnings
        seen = set()
        for page in scoped_pages:
            number = claims_mod.sn_number(page["sn"])
            if number is None or number in claims or page["sn"] in seen:
                continue
            seen.add(page["sn"])
            warnings.append({
                "kind": "UNCLAIMED_NUMBER",
                "sn": page["sn"],
                "detail": f"{page['sn']} is being filed in this range with "
                          f"no claim anchored on the sn-claims branch — "
                          f"claim-before-author was skipped",
                "cure": "claim the number first: python3 tools/sn_claims.py "
                        "claim --ib <IB> --seat <seat>; for an id that "
                        "predates the guard, the SN lane anchors a "
                        "retro-claim instead",
                "owner": "SN lane",
            })
    return warnings


_HISTORY_SN_RE = re.compile(r"(?i)sn[-_]?(\d{3,4})")


def _norm_history_id(token: str) -> str:
    return "SN-" + (token.zfill(3) if len(token) <= 3 else token)


def tombstone_class(root: Path, registry: dict, pages: list[dict]) -> list[dict]:
    """Ids in git history with NO page, NO capture and NO registry entry.
    These were removed without a lifecycle record. The fixer never touches
    them: forging a note for a removed fixture is exactly the failure the
    vanish guard exists to catch. The LAW lane decides: tombstone record
    or a ratified test-id carve-out in the guard."""
    out = _git(root, "log", "HEAD", "--name-only", "--format=", "--",
               ".naya/capture", str(BRAIN_NOTES_REL).replace("\\", "/"))
    if out is None:
        return []
    ever = {_norm_history_id(m) for line in out.splitlines()
            for m in _HISTORY_SN_RE.findall(line)}
    registered = {e.get("smart_note_id") for e in registry.get("entries", [])}
    on_disk = set()
    cap_dir = root / CAPTURE_REL
    if cap_dir.exists():
        for p in cap_dir.glob("*.json"):
            for m in _HISTORY_SN_RE.findall(p.name):
                on_disk.add(_norm_history_id(m))
            try:
                doc = json.loads(p.read_text(encoding="utf-8"))
                sid = doc.get("smart_note_id")
                if isinstance(sid, str) and sid:
                    mm = _HISTORY_SN_RE.search(sid)
                    if mm:
                        on_disk.add(_norm_history_id(mm.group(1)))
            except (ValueError, UnicodeDecodeError):
                pass
    with_page = {p["sn"] for p in pages}
    return [{"sn": sid, "kind": "TOMBSTONE_REQUIRED",
             "missing": f"lifecycle record for {sid} — the id exists in git "
                        f"history but has no page, no capture and no registry "
                        f"entry (removed without a lifecycle record)",
             "cure": "LAW lane records a lifecycle tombstone for the id or "
                     "ratifies a test-id carve-out in the vanish guard — "
                     "do NOT fabricate a note for it",
             "owner": "LAW lane"}
            for sid in sorted(ever - registered - on_disk - with_page)]


def _range_endpoints(range_spec: str) -> tuple[str, str]:
    """Endpoints of a git range, two-dot (A..B) or three-dot (A...B).

    The uniqueness gate needs the two endpoint refs; the delta diff keeps
    the caller's dot semantics. partition("..") alone misparses a
    three-dot range (head becomes ".B") and the gate then fails closed
    on a ref that does not exist — the door-obligation workflow's
    pull_request path passes three dots (diagnosed on PR #3088,
    2026-10-26: CI red while every local leg passed in a shallow
    checkout, where the gate's history scan never engaged).
    """
    if "..." in range_spec:
        base, _, head = range_spec.partition("...")
    else:
        base, _, head = range_spec.partition("..")
    if not base or not head:
        raise RuntimeError("uniqueness gate requires A..B revision range")
    return base, head


def pages_in_range(root: Path, range_spec: str, all_pages: list[dict]) -> list[dict]:
    out = _git(root, "diff", "--name-only", "--diff-filter=AM", range_spec,
               "--", str(BRAIN_NOTES_REL).replace("\\", "/"))
    if out is None:
        raise RuntimeError(f"git diff failed for range {range_spec}")
    changed = {line.strip() for line in out.splitlines() if line.strip()}
    return [p for p in all_pages if p["path"] in changed]


# --------------------------------------------------------------------------
# Fix — generate capture + entry from the published page only
# --------------------------------------------------------------------------

def _publishing_provenance(root: Path, rel_path: str) -> dict:
    """Earliest add commit for the page (+ restore commit if it was
    deleted and re-added). Derived from git history; never invented."""
    adds = _git(root, "log", "--diff-filter=A", "--reverse",
                "--format=%H%x09%s", "--", rel_path)
    add_list = [line.split("\t", 1) for line in (adds or "").splitlines()
                if "\t" in line]
    deletes = _git(root, "log", "--diff-filter=D", "--format=%H", "--", rel_path)
    delete_list = [line.strip() for line in (deletes or "").splitlines()
                   if line.strip()]
    if not add_list:
        return {"commit": None, "subject": None, "restored_in": None,
                "deleted_in": delete_list[0] if delete_list else None}
    first = add_list[0]
    restored = add_list[-1][0] if len(add_list) > 1 else None
    return {"commit": first[0], "subject": first[1],
            "restored_in": restored,
            "deleted_in": delete_list[0] if delete_list else None}


def _machine_view(page: dict) -> dict:
    raw = page["sections"].get("machine", "")
    base = {"sn": page["sn"], "title": page["title"],
            "projection_path": page["path"],
            "truth_state": page["truth_state"], "lifecycle_state": "ACTIVE"}
    fence = re.search(r"```json\s*(\{.*?\})\s*```", raw, flags=re.S)
    if fence:
        try:
            parsed = json.loads(fence.group(1))
            if isinstance(parsed, dict):
                merged = dict(parsed)
                for k, v in base.items():
                    merged.setdefault(k, v)
                return merged
        except ValueError:
            pass
    return {**base, "machine_section": raw}


def build_capture(page: dict, prov: dict, date: str) -> dict:
    s = page["sections"]
    views_note = (
        f"Views derived {date} from this note's published projection page "
        f"sections at backfill time; derivation happened from the published "
        f"page only — this capture remains a canonical reconstruction.")
    if not s.get("meaning"):
        views_note += (" The published page carries no WHAT-IT-ALL-MEANS "
                       "section (six-note format); ai_view is left empty "
                       "rather than synthesized.")
    intelligence = {
        "title": page["title"],
        "intelligent_block_id": page["ib"],
        "smart_note_id": page["sn"],
        "projection_path": page["path"],
        "ingest": "canonical-reconstruction",
        "ingest_note": (
            "Backfilled intake record. Published as Markdown projection "
            "without preserved runtime capture; the door write landed the "
            "page with no capture and no registry entry, skipping the "
            "door's same-push obligation. Capture generated mechanically "
            "from the published page only by "
            f"tools/check_door_obligation.py --fix on {date}. "
            "No runtime provenance invented."),
        "ingested_at": date,
        "essence": s.get("essence", ""),
        "human_view": s.get("human_view", ""),
        "simple_view": s.get("simple_view", ""),
        "grandma_view": s.get("grandma_view", ""),
        "naya_view": s.get("naya_view", ""),
        "ai_view": s.get("meaning", ""),
        "machine_view": _machine_view(page),
        "views_note": views_note,
    }
    return {
        "smart_note_id": page["sn"],
        "intelligence": intelligence,
        "source": {
            "ingestion": "canonical-reconstruction",
            "projection_path": page["path"],
            "provenance_note": (
                "backfilled from published projection by the door-obligation "
                "fixer (House-Fire Law cure, 2026-10-21); no runtime "
                "provenance invented"),
            "publishing_commit": prov.get("commit"),
        },
        "schema": "naya.smart-note-capture.v2",
        "lifecycle_state": "ACTIVE",
    }


def build_entry(page: dict, capture_doc: dict, snv2, prov: dict, date: str) -> dict:
    if prov.get("commit"):
        where = (f"published directly as a BRAIN projection in commit "
                 f"{prov['commit']} ('{prov.get('subject')}')")
    else:
        where = ("published directly as a BRAIN projection (publishing "
                 "commit not resolvable from local git history)")
    note = (f"{where} with no runtime capture and no registry entry — "
            f"a door write that skipped the same-push capture + registry "
            f"obligation")
    if prov.get("deleted_in") and prov.get("restored_in"):
        note += (f"; deleted in commit {prov['deleted_in']} and restored "
                 f"in commit {prov['restored_in']}")
    note += (f"; capture and entry backfilled mechanically from the "
             f"published projection by tools/check_door_obligation.py "
             f"--fix on {date} under the House-Fire Law door-obligation "
             f"cure (Shawn, 2026-10-21); no runtime provenance invented")
    return {
        "smart_note_id": page["sn"],
        "intelligent_block_id": page["ib"],
        "title": page["title"],
        "content_hash": intelligence_hash(snv2, capture_doc),
        "projection_path": page["path"],
        "projection_status": "GITHUB_BRAIN_PUBLISHED",
        "truth_state": page["truth_state"],
        "scope": page["scope"],
        "category": page["category"],
        "topic": page["topic"],
        "subtopic": page["subtopic"],
        "captured_at": page["captured_at"],
        "lifecycle_state": "ACTIVE",
        "provenance": {"ingestion": "canonical-reconstruction", "note": note},
        "page_hash": snv2._page_file_hash(Path(page["_abs_path"])),
    }


def _atomic_write_json(path: Path, obj, indent: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=indent, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    tmp.replace(path)


def run_fix(root: Path, snv2, pages: list[dict], registry: dict,
            ids: set[str] | None, date: str, cap_index: CaptureIndex) -> dict:
    entries = registry.setdefault("entries", [])
    by_ib = {e.get("intelligent_block_id"): e for e in entries}
    actions = []
    new_entries = []
    for page in pages:
        if ids is not None and page["sn"] not in ids:
            continue
        page["_abs_path"] = str(root / page["path"])
        cap_p = capture_path(root, page["ib"])
        entry = by_ib.get(page["ib"])
        capture_doc = cap_index.for_page(page)
        if capture_doc is None and cap_p.exists():
            actions.append({"sn": page["sn"], "action": "CONFLICT",
                            "detail": "a capture file exists at the canonical "
                                      "path but is unparseable or carries no "
                                      "intelligence; human lane must reconcile"})
            continue
        prov = _publishing_provenance(root, page["path"])
        if capture_doc is None:
            capture_doc = build_capture(page, prov, date)
            if entry is not None and entry.get("content_hash") != intelligence_hash(snv2, capture_doc):
                actions.append({"sn": page["sn"], "action": "CONFLICT",
                                "detail": "registry entry exists but its "
                                          "content_hash does not match the "
                                          "page-derived capture; NOT written "
                                          "— human lane must reconcile"})
                continue
            _atomic_write_json(cap_p, capture_doc, indent=1)
            actions.append({"sn": page["sn"], "action": "CAPTURE_WRITTEN",
                            "detail": str(cap_p.relative_to(root))})
        if entry is None:
            new_entry = build_entry(page, capture_doc, snv2, prov, date)
            new_entries.append(new_entry)
            by_ib[page["ib"]] = new_entry
            actions.append({"sn": page["sn"], "action": "ENTRY_WRITTEN",
                            "detail": page["ib"]})
    if new_entries:
        new_entries.sort(key=lambda e: (e.get("smart_note_id", ""),
                                        e.get("intelligent_block_id", "")))
        entries.extend(new_entries)
        policy = registry.setdefault("sequence_policy",
                                     {"human_id_format": "SN-###"})
        nxt = int(policy.get("next_sequence", 1))
        for e in new_entries:
            m = re.fullmatch(r"SN-(\d+)", str(e.get("smart_note_id", "")))
            if m:
                nxt = max(nxt, int(m.group(1)) + 1)
        policy["next_sequence"] = nxt
        registry["corpus_manifest_hash"] = snv2._corpus_manifest_hash(entries)
        _atomic_write_json(root / REGISTRY_REL, registry, indent=2)
    return {"actions": actions,
            "registry_changed": bool(new_entries)}


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=None,
                    help="repo root (default: grandparent of tools/)")
    ap.add_argument("--ids", default=None,
                    help="comma-separated SN ids to scope to")
    ap.add_argument("--range", default=None, dest="range_spec",
                    help="git range A..B — check only pages the range touched "
                         "(the door's pre-push / CI delta contract)")
    ap.add_argument("--fix", action="store_true",
                    help="generate missing captures + registry entries "
                         "from the published pages")
    ap.add_argument("--with-regen", action="store_true",
                    help="with --fix, also run tools/regenerate_brain_index.py")
    ap.add_argument("--date", default=None,
                    help="backfill date stamp YYYY-MM-DD (default: today UTC)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve() if args.root else ROOT
    if not (root / BRAIN_NOTES_REL).exists() and not args.fix:
        print(f"ERROR: {root} does not look like the NayaPOWER checkout "
              f"(no {BRAIN_NOTES_REL}) — failing closed", file=sys.stderr)
        return 2
    try:
        snv2 = _load_snv2(root)
    except Exception as exc:  # machinery error: fail closed
        print(f"ERROR: cannot load tools/smart_note_v2.py: {exc}",
              file=sys.stderr)
        return 2

    import datetime
    date = args.date or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    ids = ({s.strip().upper() for s in args.ids.split(",") if s.strip()}
           if args.ids else None)

    registry = load_registry(root)
    pages, twins = discover_pages(root)
    cap_index = CaptureIndex(root, snv2)
    if ids is not None:
        pages = [p for p in pages if p["sn"] in ids]

    if args.fix:
        # The fixer refuses ids that have no page on disk — fabricating a
        # record for a pageless id is the exact failure the vanish guard
        # exists to catch (SN-9998/SN-9999 class).
        refusals = []
        if ids is not None:
            have = {p["sn"] for p in pages}
            refusals = sorted(ids - have)
        result = run_fix(root, snv2, pages, registry, ids, date, cap_index)
        registry = load_registry(root)
        if args.json:
            print(json.dumps({"fix": result, "refusals": refusals},
                             indent=2))
        else:
            for a in result["actions"]:
                print(f"{a['action']}: {a['sn']} — {a['detail']}")
            for sid in refusals:
                print(f"REFUSED: {sid} — no published page on disk; the "
                      f"fixer does not fabricate records for pageless ids "
                      f"(owner: LAW lane — lifecycle tombstone decision)")
            if result["registry_changed"]:
                print("Registry updated: entries appended, "
                      "corpus_manifest_hash recomputed, next_sequence bumped.")
            print("NEXT: run `python3 tools/regenerate_brain_index.py` and "
                  "commit captures + registry + regen output together "
                  "(the same-push obligation).")
        if args.with_regen:
            r = subprocess.run([sys.executable,
                                str(root / "tools" / "regenerate_brain_index.py"),
                                "--root", str(root)],
                               capture_output=True, text=True)
            sys.stdout.write(r.stdout)
            sys.stderr.write(r.stderr)
            if r.returncode != 0:
                return 2
        return 0 if not refusals else 1

    # ---- check mode ----
    scoped = pages
    tombstones: list[dict] = []
    if args.range_spec:
        try:
            scoped = pages_in_range(root, args.range_spec, pages)
        except RuntimeError as exc:
            print(f"ERROR: {exc} — failing closed", file=sys.stderr)
            return 2
    else:
        tombstones = tombstone_class(root, registry, pages)
    defects = check_pages(root, snv2, scoped, registry, cap_index)

    # A door obligation is incomplete if a newly added human-visible note ID
    # resolves to two distinct paths. Check the complete target tree against
    # the changed files; leave untouched legacy collisions for separate cure.
    if args.range_spec:
        try:
            import importlib.util
            unique_path = root / "tools" / "check_smart_note_unique_ids.py"
            spec = importlib.util.spec_from_file_location("smart_note_unique_ids", unique_path)
            if spec is None or spec.loader is None:
                raise RuntimeError("cannot load Smart Note uniqueness gate")
            unique = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(unique)
            base, head = _range_endpoints(args.range_spec)
            all_paths = unique.git("ls-tree", "-r", "--name-only", head)
            added_paths = unique.git("diff", "--name-only", "--diff-filter=AR",
                                     base, head, "--", unique.ROOT)
            for number, paths in sorted(unique.check(all_paths, added_paths).items()):
                defects.append({
                    "sn": f"SN-{number:04d}",
                    "kind": "DUPLICATE_PUBLIC_ID",
                    "path": paths[0],
                    "missing": f"public SN-{number:04d} collides across {len(paths)} paths: "
                               + " | ".join(paths),
                    "cure": "the original owner must reconcile the two records "
                            "without losing intelligence; re-run this gate before publication",
                    "owner": "Smart Note identity lane",
                })
        except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
            print(f"ERROR: Smart Note uniqueness check failed closed: {exc}",
                  file=sys.stderr)
            return 2

    warnings = filing_warnings(root, registry, scoped, args.range_spec)

    if args.json:
        print(json.dumps({
            "pages_in_scope": len(scoped),
            "defects": defects,
            "tombstones": tombstones,
            "warnings": warnings,
            "twins": twins if not args.range_spec else [],
            "ok": not defects and not tombstones,
        }, indent=2))
    else:
        for d in defects + tombstones:
            print(f"MISSING: {d['missing']} — CURE: {d['cure']} "
                  f"(owner: {d['owner']})")
        for w in warnings:
            print(f"WARN {w['kind']}: {w['detail']} — CURE: {w['cure']} "
                  f"(owner: {w['owner']})")
        for t in twins:
            if not args.range_spec and (ids is None or t["sn"] in ids):
                print(f"TWIN: {t['ib']} is also published at {t['twin']} — "
                      f"entry binds the canonical path {t['canonical']}; "
                      f"canonical-home reconciliation still owed "
                      f"(owner: SN lane)")
        total = len(defects) + len(tombstones)
        if total:
            print(f"DOOR OBLIGATION: {total} defect(s) across "
                  f"{len(scoped)} page(s) in scope.")
        else:
            print(f"DOOR OBLIGATION: OK — {len(scoped)} page(s) in scope, "
                  f"every page carries its capture + registry entry.")
    return 1 if (defects or tombstones) else 0


if __name__ == "__main__":
    sys.exit(main())
