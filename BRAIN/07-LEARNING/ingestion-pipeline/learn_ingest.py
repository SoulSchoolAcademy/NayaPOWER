#!/usr/bin/env python3
"""
LEARN NODE — Intelligence Ingestion Pipeline (implementation v1)

Takes Smart Notes from branch naya4/smart-notes-2026-09-30 (draft PR #1229)
and bakes their intelligence into the briefing substrate:
  learn/*.md files + brief-template.md LEARN markers + AGENTS.md Lessons.

Stages: DETECT → PARSE → CLASSIFY → INTEGRATE → VERIFY → RECORD (+ BACKFILL)

Hard boundaries:
  - READ-ONLY on the repo (GitHub API enumeration only).
  - Never mark notes RATIFIED; never merge; never write to main.
  - Authority-touching notes are recorded + flagged, never integrated.
  - All writes are workspace-local and idempotent.

Usage:
  python3 learn_ingest.py              # steady-state run (new/changed notes only)
  python3 learn_ingest.py --backfill   # one-time SN-ascending pass over all notes
  python3 learn_ingest.py --canary     # E2E proof: canary note → render check → idempotency
"""

import base64
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

# ---------------------------------------------------------------- config

REPO = "SoulSchoolAcademy/NayaPOWER"
BRANCH = "naya4/smart-notes-2026-09-30"
GH_API = os.path.expanduser("~/workspace/skills/github/bin/gh-api")
LEARN_DIR = os.path.expanduser("~/workspace/goals/bring-naya-to-life/hidden_files/learn")
AGENTS_MD = os.path.expanduser("~/AGENTS.md")

LEDGER_PATH = os.path.join(LEARN_DIR, "ledger.json")
LOG_PATH = os.path.join(LEARN_DIR, "ingestion-log.md")
TEMPLATE_PATH = os.path.join(LEARN_DIR, "brief-template.md")
CONFLICTS_PATH = os.path.join(LEARN_DIR, "conflicts.md")
RECEIPTS_DIR = os.path.join(LEARN_DIR, "receipts")

FILE_FILTER = re.compile(r"BRAIN/05-MEMORY/SMART-NOTES/.*/IB-SMART-NOTE-.*\.md$")
SN_FROM_PATH = re.compile(r"SN-0?(\d+)", re.IGNORECASE)

STOPWORDS = {
    "a", "the", "is", "to", "of", "and", "or", "for", "in", "on", "with",
    "be", "as", "by", "it", "this", "that", "an", "are", "was", "were",
    "has", "have", "had", "will", "would", "should", "could", "from",
    "at", "not", "but", "they", "their", "them", "its", "our", "your",
}

# Classification → (learn file, template marker or None)
ROUTING = {
    "DOCTRINE": ("doctrine.md", "operating-ethos"),
    "LAW": ("laws.md", "hard-prohibitions"),
    "PROCESS_FIX": ("lessons.md", None),          # + AGENTS.md
    "VERIFICATION_METHOD": ("verification-methods.md", "verification-contract"),
    "QUALITY_STANDARD": ("quality-gates.md", "quality-gate"),
    "DECISION_RECORD": ("decisions.md", None),
    "UNCATEGORIZED": ("lessons.md", None),
}

AUTHORITY_WORDS = re.compile(
    r"\b(merg\w*|deploy\w*|ratif\w*|production|authority|consent|privacy|"
    r"security|destruct\w*|self-modif\w*)\b", re.IGNORECASE)
AUTHORITY_CHANGE = re.compile(
    r"(should be allowed|now permitted|no longer requires|can now|"
    r"propos\w*\s+(change|remov\w*|relax))", re.IGNORECASE)

CANARY_RULE = "CANARY-7F3A: test briefs must include this sentence."


def utcnow():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------- github

def gh(method, path, data_file=None):
    """Call gh-api. Returns parsed JSON. Raises on failure."""
    cmd = [GH_API, method, path]
    if data_file:
        cmd.append("@" + data_file)
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(f"gh-api {method} {path} failed: {r.stderr[:300]}")
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"gh-api {method} {path}: invalid JSON: {r.stdout[:300]}")


def get_branch_sha():
    d = gh("GET", f"/repos/{REPO}/git/refs/heads/{BRANCH}")
    return d["object"]["sha"]


def get_tree(branch_sha):
    d = gh("GET", f"/repos/{REPO}/git/trees/{branch_sha}?recursive=1")
    if d.get("truncated"):
        raise RuntimeError("tree truncated — cannot trust enumeration")
    return [t for t in d["tree"]
            if t["type"] == "blob" and FILE_FILTER.search(t["path"])]


def get_blob_text(blob_sha):
    d = gh("GET", f"/repos/{REPO}/git/blobs/{blob_sha}")
    if d.get("encoding") != "base64":
        raise RuntimeError(f"unexpected blob encoding: {d.get('encoding')}")
    return base64.b64decode(d["content"]).decode("utf-8")


# ---------------------------------------------------------------- ledger

def load_ledger():
    if not os.path.exists(LEDGER_PATH):
        raise RuntimeError("ledger.json missing — refusing to rebuild blindly")
    try:
        with open(LEDGER_PATH) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        raise RuntimeError(f"ledger.json corrupt ({e}) — refusing to rebuild blindly")


def save_ledger(ledger):
    ledger["updated_at"] = utcnow()
    tmp = LEDGER_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(ledger, f, indent=2, sort_keys=True)
    os.rename(tmp, LEDGER_PATH)


def sn_from_path(path):
    m = SN_FROM_PATH.search(path)
    if not m:
        return None
    return f"SN-{int(m.group(1)):04d}"

# ---------------------------------------------------------------- PARSE

def extract_json_fenced(text):
    """Extract ```json ... ``` fence contents, else None."""
    m = re.search(r"```json\s*\n(.*?)```", text, re.DOTALL | re.IGNORECASE)
    return m.group(1) if m else None


def extract_json_braces(text):
    """Balanced-brace scan from first '{', respecting string escapes."""
    start = text.find("{")
    if start < 0:
        return None
    depth = 0
    in_str = False
    esc = False
    for i in range(start, len(text)):
        c = text[i]
        if esc:
            esc = False
            continue
        if c == "\\" and in_str:
            esc = True
            continue
        if c == '"' and not esc:
            in_str = not in_str
            continue
        if in_str:
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    return None


def parse_machine_note(machine_raw):
    """Return dict or raise ValueError. Never guesses."""
    if not machine_raw or not machine_raw.strip():
        raise ValueError("empty MACHINE NOTE section")
    js = extract_json_fenced(machine_raw) or extract_json_braces(machine_raw)
    if js is None:
        raise ValueError("no JSON object found in MACHINE NOTE")
    try:
        return json.loads(js)
    except json.JSONDecodeError as e:
        raise ValueError(f"MACHINE NOTE JSON invalid: {e}")


def split_sections(text):
    """Split markdown on ^## lines. Returns {key: body} with tolerant keys."""
    sections = {}
    current = None
    buf = []
    for line in text.splitlines():
        m = re.match(r"^##\s+(.*)$", line)
        if m:
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            raw = m.group(1)
            clean = re.sub(r"^[^A-Za-z0-9]+", "", raw).strip().upper()
            if "NUTSHELL" in clean:
                current = "nutshell"
            elif clean == "HUMAN NOTE":
                current = "human_note"
            elif clean == "CHILD NOTE":
                current = "child_note"
            elif clean == "GRANDMA NOTE":
                current = "grandma_note"
            elif clean == "NAYA NOTE":
                current = "naya_note"
            elif "MACHINE NOTE" in clean:
                current = "machine_note_raw"
            else:
                current = "other:" + clean
            buf = []
        elif current is not None:
            buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf).strip()
    return sections


def tolerant_field(mnote, text, name, pattern, fallback_fn=None):
    """Try MACHINE NOTE dict first, then regex on raw text, then fallback."""
    if mnote and name in mnote and mnote[name]:
        return mnote[name]
    m = re.search(pattern, text, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return fallback_fn() if fallback_fn else None


def parse_note(text, repo_path, blob_sha):
    """
    Parse a Smart Note file into a normalized Learning record.
    Raises ValueError on any failure — never guesses field values.
    """
    sections = split_sections(text)
    machine_raw = sections.get("machine_note_raw", "")
    mnote = parse_machine_note(machine_raw)

    def first_heading():
        # Prefer the **Intelligent Block:** line's title part (after — or -)
        # over the bare "# Intelligent Block: SN-XXXX" heading.
        m = re.search(r"\*\*Intelligent Block:\*\*\s*SN-?\d+\s*[—–-]\s*(.+)$",
                      text, re.MULTILINE | re.IGNORECASE)
        if m:
            return m.group(1).strip()
        m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        if m:
            h = m.group(1).strip()
            # Strip a leading "Intelligent Block: SN-XXXX — " prefix if present
            h2 = re.sub(r"^Intelligent Block:\s*SN-?\d+\s*[—–-]\s*",
                        "", h, flags=re.IGNORECASE)
            return h2 or h
        return None

    sn_id = mnote.get("sn") or mnote.get("smart_note_id")
    if not sn_id:
        sn_id = sn_from_path(repo_path)
    if not sn_id:
        m2 = re.search(r"Intelligent Block:[^\n]*?(SN-?\d+)", text, re.IGNORECASE)
        sn_id = m2.group(1).upper().replace("SN-", "SN-") if m2 else None
    if not sn_id:
        raise ValueError("cannot determine sn_id")

    # normalize SN-0288 / SN-288 → SN-0288
    mnum = re.search(r"(\d+)", sn_id)
    if mnum:
        sn_id = f"SN-{int(mnum.group(1)):04d}"

    title = mnote.get("title") or first_heading() or sn_id
    truth_state = (mnote.get("truth_state")
                   or tolerant_field(mnote, text, "truth_state",
                                     r"\*\*Truth state:\*\*\s*([A-Z_]+)"))
    taxonomy = mnote.get("taxonomy") or []
    if isinstance(taxonomy, str):
        taxonomy = [taxonomy]
    rule_text = mnote.get("rule")
    if rule_text is not None and not isinstance(rule_text, str):
        rule_text = json.dumps(rule_text)
    cousins = mnote.get("cousins") or []
    if isinstance(cousins, str):
        cousins = [cousins]
    evidence = mnote.get("evidence")
    evidence_refs = (json.dumps(evidence, sort_keys=True)[:2000]
                     if evidence is not None else None)
    if not evidence_refs:
        m2 = re.search(r"\*\*Provenance:\*\*\s*(.+)", text)
        evidence_refs = m2.group(1).strip()[:500] if m2 else None
    status_text = mnote.get("status")
    if status_text is not None and not isinstance(status_text, str):
        status_text = json.dumps(status_text)

    return {
        "sn_id": sn_id,
        "title": str(title)[:200],
        "truth_state": str(truth_state or "UNKNOWN"),
        "taxonomy": [str(t) for t in taxonomy],
        "rule_text": rule_text,
        "naya_note": sections.get("naya_note", ""),
        "nutshell": sections.get("nutshell", ""),
        "evidence_refs": evidence_refs,
        "cousins": [str(c) for c in cousins],
        "status_text": status_text,
        "machine_view": mnote.get("machine_view"),
        "source_path": repo_path,
        "content_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "blob_sha": blob_sha,
    }

# ---------------------------------------------------------------- CLASSIFY

def classify(rec):
    """First-match decision table, top-down. Returns type string."""
    rule = rec["rule_text"] or ""
    title = rec["title"] or ""
    tax = rec["taxonomy"] or []
    tax_joined = " ".join(tax)
    nutshell = rec["nutshell"] or ""

    # 1. LAW
    if ((re.search(r"\b(never|must not|do not|prohibit\w*|forbidden|hard stop)\b",
                   rule, re.IGNORECASE)
         and ("AUTHORITY-ENVELOPE" in tax_joined or "GOVERNANCE" in tax_joined))
            or ("law" in title.lower()
                and re.search(r"\b(never|must not|do not|prohibit)\b",
                              rule, re.IGNORECASE))):
        return "LAW"
    # 2. DOCTRINE
    if any("doctrine" in t.lower() for t in tax) \
            or re.search(r"\b(doctrine|protocol)\b", title, re.IGNORECASE):
        return "DOCTRINE"
    # 3. VERIFICATION_METHOD
    if (re.search(r"\b(adversarial|falsif\w*|control\w*|non-vacuous|prove the|"
                  r"verif\w+\s+method)\b", rule, re.IGNORECASE)
            or any(k in tax_joined for k in
                   ("CLASSIFICATION-INTEGRITY", "ENGINEERING-PROOF",
                    "INDEPENDENT-VERIFICATION"))):
        return "VERIFICATION_METHOD"
    # 4. QUALITY_STANDARD
    if re.search(r"\b(9\.5|AAA|triple-a|quality bar|acceptance bar)\b",
                 rule + " " + title, re.IGNORECASE):
        return "QUALITY_STANDARD"
    # 5. DECISION_RECORD
    if re.search(r"\b(decision|decided|recommended order|merge order|"
                 r"options considered)\b", title + " " + rule, re.IGNORECASE):
        return "DECISION_RECORD"
    # 6. PROCESS_FIX
    tax1 = tax[1] if len(tax) > 1 else ""
    if (tax1 in ("CI-TRIAGE", "OPERATIONS")
            or "caught live" in nutshell.lower()
            or (rule and re.match(r"^(before|after|always|check|verify|run)\b",
                                  rule.strip(), re.IGNORECASE))):
        return "PROCESS_FIX"
    # 7. UNCATEGORIZED
    return "UNCATEGORIZED"


def authority_touch(rec):
    """
    True if the note proposes CHANGING who-may-do-what on protected ground.
    Mere restatement of existing boundaries is NOT authority-touching.
    """
    text = " ".join(filter(None, [rec["rule_text"], rec["title"],
                                  rec["naya_note"][:1000]]))
    if not AUTHORITY_WORDS.search(text):
        return False
    if AUTHORITY_CHANGE.search(text):
        return True
    # Heuristic: prohibitive restatements ("never X without Y") reinforce law.
    if re.search(r"\b(never|must not|require[sd]?|needs?)\b", text, re.IGNORECASE):
        return False
    # Ambiguous: fail closed → flag.
    return True

# ---------------------------------------------------------------- IMMUNE GATE
# POISON-1 / POISON-2: machine_view validation stage.
# The authority_touch() heuristic only scans human-readable text; the
# machine_view vector is invisible to it. These checks run on the parsed
# MACHINE NOTE dict, before any integration, and reject poisoned captures
# at intake. Absent machine_view is NOT poison (legacy notes predate it).

def _is_false(v):
    return v is False or (isinstance(v, str) and v.strip().lower() == "false")


def _is_true(v):
    return v is True or (isinstance(v, str) and v.strip().lower() == "true")


def validate_machine_view(rec):
    """
    Immune gate on the machine-readable view.
    Returns (rejected: bool, reason: str).
    """
    mv = rec.get("machine_view")
    if mv is None:
        return (False, "")
    if not isinstance(mv, dict):
        return (True, "machine_view present but not a JSON object")
    # POISON-1: raw source must be kept separate from distillation.
    if _is_false(mv.get("raw_source_separate_from_distillation")):
        return (True,
                "machine_view.raw_source_separate_from_distillation=false")
    # POISON-2: CANDIDATE must never inherit authority via machine_view.
    if _is_true(mv.get("authority_inheritance")):
        ts = mv.get("truth_state") or rec.get("truth_state")
        if str(ts or "").upper() == "CANDIDATE":
            return (True,
                    "machine_view.authority_inheritance=true "
                    "with CANDIDATE truth_state")
    return (False, "")


def reject_poison(sn_id, repo_path, blob_sha, text, sha, ledger, run_id,
                  report, rec, reason):
    """
    Record a poison rejection. Writes a REJECTED_POISON ledger entry with
    the rejection receipt embedded (no receipts/ file — a rejected capture
    must leave zero ingestible artifacts) and logs the reason. Nothing is
    integrated: no learn-file sections, no template bullets, no AGENTS.md.
    """
    ingested_at = utcnow()
    rejection_receipt = {
        "receipt_type": "rejection_receipt",
        "sn_id": sn_id,
        "rejected_at": ingested_at,
        "run_id": run_id,
        "reason": reason,
        "source_path": repo_path,
        "content_sha256": sha,
    }
    ledger["entries"][sn_id] = {
        "repo_path": repo_path,
        "content_sha256": sha,
        "blob_sha": blob_sha,
        "ingested_at": ingested_at,
        "status": "REJECTED_POISON",
        "run_id": run_id,
        "rejection_reason": reason,
        "rejection_receipt": rejection_receipt,
        "classification": "POISON_REJECT",
    }
    report.setdefault("rejected", []).append(
        {"sn_id": sn_id, "reason": reason})
    return "REJECTED_POISON"

# ---------------------------------------------------------------- INTEGRATE

def learn_file(name):
    return os.path.join(LEARN_DIR, name)


def section_text(rec, ntype, ingested_at):
    rule = rec["rule_text"]
    if not rule:
        nn = rec["naya_note"] or ""
        rule = nn[:500] if nn else (rec["nutshell"] or "")[:500]
    lines = [
        f"## {rec['sn_id']} — {rec['title']} ({ingested_at[:10]})",
        f"**Source:** `{rec['source_path']}`",
        f"**Truth state:** {rec['truth_state']} · **Type:** {ntype} "
        f"· **Ingested:** {ingested_at}",
        "",
        f"> {rule}",
        "",
        f"**Evidence:** {(rec['evidence_refs'] or 'n/a')[:300]}",
        f"**Cousins:** {', '.join(rec['cousins']) if rec['cousins'] else 'none'}",
        "",
    ]
    return "\n".join(lines)


def decision_entry(rec, ingested_at):
    rule = rec["rule_text"] or rec["nutshell"] or ""
    lines = [
        f"## {ingested_at[:10]} — {rec['sn_id']} — {rec['title']}",
        f"**Source:** `{rec['source_path']}` · **State:** {rec['truth_state']}",
        rule[:800],
        f"**Rationale/options:** {(rec['status_text'] or 'see source note')[:400]}",
        "",
    ]
    return "\n".join(lines)


def derive_bullet(rec):
    """First sentence of rule_text (≤200ch) + (SN-XXXX). None if nothing actionable."""
    src = rec["rule_text"] or rec["naya_note"] or ""
    src = src.strip()
    if not src:
        return None
    first = re.split(r"\.\s+", src, maxsplit=1)[0].strip()
    if not first.endswith("."):
        first += "."
    first = first[:200]
    return f"- {first} ({rec['sn_id']})"


def template_insert(ntype, rec, bullet):
    """
    Insert bullet into the template's LEARN marker section.
    Returns (action, detail): action ∈ {inserted, skipped_idempotent,
    updated, missing_markers, no_bullet}.
    """
    _, marker = ROUTING[ntype]
    if marker is None or bullet is None:
        return ("no_bullet" if bullet is None else "no_marker_target",
                f"type={ntype}")
    with open(TEMPLATE_PATH) as f:
        content = f.read()
    open_m = f"<!-- LEARN:{marker} -->"
    close_m = f"<!-- /LEARN:{marker} -->"
    if open_m not in content or close_m not in content:
        return ("missing_markers", marker)
    start = content.index(open_m) + len(open_m)
    end = content.index(close_m)
    section = content[start:end]
    sn_tag = f"({rec['sn_id']})"
    if sn_tag in section:
        # idempotent: check whether text changed (PENDING_UPDATE path)
        for line in section.splitlines():
            if sn_tag in line and line.strip() != bullet:
                new_section = section.replace(line, bullet, 1)
                content = content[:start] + new_section + content[end:]
                with open(TEMPLATE_PATH, "w") as f:
                    f.write(content)
                return ("updated", marker)
        return ("skipped_idempotent", marker)
    new_section = section
    if not new_section.endswith("\n"):
        new_section += "\n"
    new_section += bullet + "\n"
    content = content[:start] + new_section + content[end:]
    with open(TEMPLATE_PATH, "w") as f:
        f.write(content)
    return ("inserted", marker)


def agents_md_append(rec):
    """Append PROCESS_FIX bullet to ~/AGENTS.md Lessons. Grep-guarded."""
    with open(AGENTS_MD) as f:
        existing = f.read()
    if rec["sn_id"] in existing:
        return "skipped_idempotent"
    rule = rec["rule_text"] or rec["naya_note"] or rec["nutshell"] or ""
    sents = re.split(r"\.\s+", rule.strip(), maxsplit=2)
    short_rule = ". ".join(sents[:2]).strip()
    if not short_rule.endswith("."):
        short_rule += "."
    short_rule = short_rule[:280]
    short_title = rec["title"][:60]
    bullet = (f"\n- **{short_title} ({rec['sn_id']}, "
              f"{utcnow()[:10]}).** {short_rule}\n")
    marker = "## Lessons"
    if marker in existing:
        idx = existing.index(marker) + len(marker)
        # append at end of the Lessons section: find next ## heading or EOF
        rest = existing[idx:]
        m = re.search(r"\n## ", rest)
        if m:
            insert_at = idx + m.start() + 1
            existing = existing[:insert_at] + bullet + existing[insert_at:]
        else:
            existing = existing.rstrip("\n") + "\n" + bullet
    else:
        existing = existing.rstrip("\n") + "\n\n## Lessons\n" + bullet
    with open(AGENTS_MD, "w") as f:
        f.write(existing)
    return "inserted"


def integrate(rec, ntype, ingested_at, flagged_authority):
    """
    Route the record to its targets. Returns list of integration dicts.
    Authority-touching notes: recorded in learn file only, never template/AGENTS.
    """
    integrations = []
    target_file, _ = ROUTING[ntype]

    if ntype == "DECISION_RECORD":
        with open(learn_file(target_file), "a") as f:
            f.write("\n" + decision_entry(rec, ingested_at))
        integrations.append({"target": f"learn/{target_file}",
                             "anchor": f"## {ingested_at[:10]} — {rec['sn_id']}"})
    else:
        with open(learn_file(target_file), "a") as f:
            f.write("\n" + section_text(rec, ntype, ingested_at))
        integrations.append({"target": f"learn/{target_file}",
                             "anchor": f"## {rec['sn_id']} —"})

    if flagged_authority:
        return integrations  # recorded only — fail closed

    bullet = derive_bullet(rec)
    _, marker = ROUTING[ntype]
    if marker:
        action, detail = template_insert(ntype, rec, bullet)
        integrations.append({"target": "learn/brief-template.md",
                             "anchor": f"({rec['sn_id']})",
                             "section": marker,
                             "template_action": action})
    if ntype == "PROCESS_FIX":
        action = agents_md_append(rec)
        integrations.append({"target": "~/AGENTS.md",
                             "anchor": rec["sn_id"],
                             "agents_action": action})
    return integrations

# ---------------------------------------------------------------- VERIFY

CANNED_VARS = {
    "{{TASK_MISSION}}": "TEST TASK — render check",
    "{{TASK_AUTHORITY}}": "TEST AUTHORITY — render check",
    "{{TASK_CONTRACT}}": "TEST CONTRACT — render check",
    "{{TASK_VERIFICATION}}": "TEST VERIFICATION — render check",
}


def render_template():
    with open(TEMPLATE_PATH) as f:
        content = f.read()
    for var, val in CANNED_VARS.items():
        content = content.replace(var, val)
    return content


def verify_integration(rec, integrations, run_id):
    """
    Three exact checks → receipt dict.
    file_contains · section_contains_sn · template_render_check.
    """
    checks = []
    all_pass = True

    for integ in integrations:
        target = integ["target"]
        anchor = integ["anchor"]
        if target.startswith("learn/"):
            path = os.path.join(LEARN_DIR, target[len("learn/"):])
        elif target == "~/AGENTS.md":
            path = AGENTS_MD
        else:
            path = target
        try:
            with open(path) as f:
                content = f.read()
            passed = anchor in content
        except OSError:
            passed = False
        checks.append({"target": target, "check": "file_contains",
                       "anchor": anchor[:60], "result": "PASS" if passed else "FAIL"})
        all_pass = all_pass and passed

        # section_contains_sn for template sections
        if target == "learn/brief-template.md" and integ.get("section"):
            marker = integ["section"]
            open_m = f"<!-- LEARN:{marker} -->"
            close_m = f"<!-- /LEARN:{marker} -->"
            try:
                start = content.index(open_m) + len(open_m)
                end = content.index(close_m)
                section = content[start:end]
                sn_present = f"({rec['sn_id']})" in section
            except (ValueError, NameError):
                sn_present = False
            checks.append({"target": target, "check": "section_contains_sn",
                           "section": marker,
                           "result": "PASS" if sn_present else "FAIL"})
            all_pass = all_pass and sn_present

    # template_render_check: bullets added this run appear verbatim
    rendered = render_template()
    render_pass = True
    render_detail = []
    for integ in integrations:
        if integ["target"] == "learn/brief-template.md" \
                and integ.get("template_action") in ("inserted", "updated"):
            bullet = derive_bullet(rec)
            if bullet and bullet in rendered:
                render_detail.append(f"bullet present: {bullet[:40]}...")
            else:
                render_pass = False
                render_detail.append(f"bullet MISSING: {(bullet or '')[:40]}...")
    leftover = re.findall(r"\{\{TASK_[A-Z_]+\}\}", rendered)
    if leftover:
        render_pass = False
        render_detail.append(f"unfilled variables: {leftover}")
    checks.append({"check": "template_render_check",
                   "result": "PASS" if render_pass else "FAIL",
                   "detail": "; ".join(render_detail) or "no template bullets this run"})
    all_pass = all_pass and render_pass

    return checks, all_pass


def write_receipt(rec, ntype, flagged, integrations, checks, all_pass, run_id,
                  status_override=None):
    status = status_override or ("INGESTED" if all_pass else "PARTIAL")
    if flagged:
        status = "FLAGGED_AUTHORITY"
    receipt = {
        "sn_id": rec["sn_id"],
        "ingested_at": utcnow(),
        "run_id": run_id,
        "classification": ntype,
        "authority_touch": flagged,
        "integrations": integrations,
        "checks": checks,
        "template_render_check": next(
            (c for c in checks if c["check"] == "template_render_check"), None),
        "status": status,
        # INGESTED = baked into briefing substrate and proven present,
        # NOT "proven obeyed" (spec §5.3).
    }
    path = os.path.join(RECEIPTS_DIR, f"{rec['sn_id']}.json")
    with open(path, "w") as f:
        json.dump(receipt, f, indent=2, sort_keys=True)
    return receipt, status


# ---------------------------------------------------------------- RECORD

def append_log(lines):
    with open(LOG_PATH, "a") as f:
        for line in lines:
            f.write(line + "\n")


def contradiction_tripwire(rec, ingested_records):
    """
    Heuristic overlap flag → learn/conflicts.md. Never auto-resolves.
    Both notes stay ACTIVE.
    """
    if not rec["rule_text"]:
        return None
    toks = [t for t in re.findall(r"[a-z]{4,}", rec["rule_text"].lower())
            if t not in STOPWORDS]
    if not toks:
        return None
    tax1 = rec["taxonomy"][1] if len(rec["taxonomy"]) > 1 else None
    hits = []
    for other in ingested_records:
        if other["sn_id"] == rec["sn_id"] or not other.get("rule_text"):
            continue
        otax1 = (other.get("taxonomy") or [None, None])[1] \
            if len(other.get("taxonomy") or []) > 1 else None
        if tax1 and otax1 and tax1 != otax1:
            continue
        otoks = set(t for t in re.findall(r"[a-z]{4,}",
                                          other["rule_text"].lower())
                    if t not in STOPWORDS)
        shared = set(toks) & otoks
        if len(shared) >= 4:
            hits.append((other["sn_id"], sorted(shared),
                         other["rule_text"][:200]))
    if not hits:
        return None
    with open(CONFLICTS_PATH, "a") as f:
        f.write(f"\n## Potential overlap — {rec['sn_id']}")
        for sn2, shared, excerpt in hits:
            f.write(f" × {sn2} ({utcnow()[:10]})\n")
            f.write(f"Shared tokens: {{{', '.join(shared)}}}\n")
        f.write("**This is a heuristic flag, not a contradiction verdict.** "
                "Both remain ACTIVE. Human review required.\n")
        f.write(f"> {rec['sn_id']}: \"{rec['rule_text'][:200]}...\"\n")
        for sn2, _, excerpt in hits:
            f.write(f"> {sn2}: \"{excerpt}...\"\n")
    return [h[0] for h in hits]

# ---------------------------------------------------------------- ROLLBACK
# POISON-3 / POISON-4 / POISON-5: remove a persisted poisoned block and every
# projection derived from it, tombstone it so no cold successor re-ingests
# it, and receipt the rollback so it is independently recomputable.

ROLLBACK_LEARN_FILES = ("lessons.md", "doctrine.md", "laws.md",
                        "decisions.md", "quality-gates.md",
                        "verification-methods.md")


def _sn_section_re(sn_id):
    """Match a learn-file section header line for sn_id (absence check)."""
    return re.compile(r"^## [^\n]*\b" + re.escape(sn_id) + r"\b",
                      re.MULTILINE)


def _sn_section_full_re(sn_id):
    """Match a full section: header line + body up to next '## ' or EOF."""
    return re.compile(
        r"^## [^\n]*\b" + re.escape(sn_id) + r"\b[^\n]*\n"
        r"(?:(?!^## ).*\n?)*",
        re.MULTILINE)


def _template_tag(sn_id):
    return f"({sn_id})"


def _agents_line_re(sn_id):
    return re.compile(r"\(" + re.escape(sn_id) + r"[,)]")


def _sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sha256_json(obj):
    return _sha256_text(json.dumps(obj, sort_keys=True))


def rollback(sn_id, reason="manual rollback"):
    """
    Remove the persisted footprint of sn_id and tombstone it.

    Removes: learn-file sections, brief-template bullets, AGENTS.md lines,
    the ingestion receipt. The ledger entry is RETAINED with status
    ROLLED_BACK (tombstone) so process_note()/detect_pending() refuse to
    re-ingest it. Writes receipts/<sn_id>.rollback.json with per-artifact
    pre/post SHA256 hashes. Returns the rollback receipt dict.
    """
    ledger = load_ledger()
    entry = ledger["entries"].get(sn_id)
    if entry is None:
        raise ValueError(f"rollback: no ledger entry for {sn_id}")
    run_id = ("rollback-"
              + utcnow().replace(":", "").replace("-", ""))
    rolled_back_at = utcnow()
    removals = []

    # 1. learn-file sections
    section_re = _sn_section_full_re(sn_id)
    for fname in ROLLBACK_LEARN_FILES:
        path = learn_file(fname)
        if not os.path.exists(path):
            continue
        with open(path) as f:
            content = f.read()
        pre_hash = _sha256_text(content)
        removed_chunks = section_re.findall(content)
        if removed_chunks:
            new_content = section_re.sub("", content)
            with open(path, "w") as f:
                f.write(new_content)
            removals.append({
                "kind": "learn_file_section",
                "target": f"learn/{fname}",
                "sections_removed": len(removed_chunks),
                "removed_sha256": _sha256_text("".join(removed_chunks)),
                "pre_file_sha256": pre_hash,
                "post_file_sha256": _sha256_text(new_content),
                "detail": f"removed {len(removed_chunks)} section(s) "
                          f"headed by {sn_id}",
            })

    # 2. brief-template bullets (any line carrying the (SN-XXXX) tag)
    with open(TEMPLATE_PATH) as f:
        tcontent = f.read()
    t_pre = _sha256_text(tcontent)
    tag = _template_tag(sn_id)
    tlines = tcontent.splitlines()
    kept = [l for l in tlines if tag not in l]
    dropped = [l for l in tlines if tag in l]
    if dropped:
        new_t = "\n".join(kept)
        if tcontent.endswith("\n"):
            new_t += "\n"
        with open(TEMPLATE_PATH, "w") as f:
            f.write(new_t)
        removals.append({
            "kind": "template_bullet",
            "target": "learn/brief-template.md",
            "sections_removed": len(dropped),
            "removed_sha256": _sha256_text("\n".join(dropped)),
            "pre_file_sha256": t_pre,
            "post_file_sha256": _sha256_text(new_t),
            "detail": f"removed {len(dropped)} template line(s) "
                      f"tagged {tag}",
        })

    # 3. AGENTS.md lines
    with open(AGENTS_MD) as f:
        acontent = f.read()
    a_pre = _sha256_text(acontent)
    aline_re = _agents_line_re(sn_id)
    alines = acontent.splitlines()
    akept = [l for l in alines if not aline_re.search(l)]
    adropped = [l for l in alines if aline_re.search(l)]
    if adropped:
        new_a = "\n".join(akept)
        if acontent.endswith("\n"):
            new_a += "\n"
        with open(AGENTS_MD, "w") as f:
            f.write(new_a)
        removals.append({
            "kind": "agents_md_line",
            "target": "~/AGENTS.md",
            "sections_removed": len(adropped),
            "removed_sha256": _sha256_text("\n".join(adropped)),
            "pre_file_sha256": a_pre,
            "post_file_sha256": _sha256_text(new_a),
            "detail": f"removed {len(adropped)} AGENTS.md line(s) "
                      f"for {sn_id}",
        })

    # 4. ingestion receipt file
    ingest_receipt_path = os.path.join(RECEIPTS_DIR, f"{sn_id}.json")
    if os.path.exists(ingest_receipt_path):
        with open(ingest_receipt_path) as f:
            rcontent = f.read()
        os.remove(ingest_receipt_path)
        removals.append({
            "kind": "ingest_receipt",
            "target": f"learn/receipts/{sn_id}.json",
            "sections_removed": 1,
            "removed_sha256": _sha256_text(rcontent),
            "pre_file_sha256": _sha256_text(rcontent),
            "post_file_sha256": _sha256_text(""),
            "detail": "deleted ingestion receipt file",
        })

    # 5. ledger tombstone (entry retained, never deleted)
    pre_entry_hash = _sha256_json(entry)
    tombstone = dict(entry)
    tombstone.update({
        "status": "ROLLED_BACK",
        "rolled_back_at": rolled_back_at,
        "rollback_reason": reason,
        "rollback_run_id": run_id,
        "rollback_receipt": f"learn/receipts/{sn_id}.rollback.json",
    })
    post_entry_hash = _sha256_json(tombstone)
    ledger["entries"][sn_id] = tombstone
    removals.append({
        "kind": "ledger_entry",
        "target": "learn/ledger.json",
        "sections_removed": 1,
        "removed_sha256": pre_entry_hash,
        "pre_file_sha256": pre_entry_hash,
        "post_file_sha256": post_entry_hash,
        "detail": f"ledger entry {sn_id} tombstoned "
                  f"({entry.get('status')} → ROLLED_BACK)",
    })

    receipt = {
        "receipt_type": "rollback_receipt",
        "sn_id": sn_id,
        "rolled_back_at": rolled_back_at,
        "run_id": run_id,
        "reason": reason,
        "removals": removals,
        "ledger_pre_sha256": pre_entry_hash,
        "ledger_post_sha256": post_entry_hash,
    }
    receipt_path = os.path.join(RECEIPTS_DIR, f"{sn_id}.rollback.json")
    with open(receipt_path, "w") as f:
        json.dump(receipt, f, indent=2, sort_keys=True)

    save_ledger(ledger)
    append_log([f"\n## {rolled_back_at} — ROLLBACK {sn_id} (run {run_id})",
                f"- reason: {reason}",
                f"- removals: {len(removals)} artifact kind(s)"])
    return receipt


def verify_rollback(receipt):
    """
    Independently recompute a rollback from its receipt data alone.

    Takes a rollback receipt dict (or a path to one). Re-derives the
    expected removal set from the receipt and confirms each artifact's
    current substrate state matches the receipt's post-rollback state.
    Returns {"sn_id", "verdict": "PASS"/"FAIL", "passed": bool,
    "artifacts": [...]} with per-artifact results.
    """
    if isinstance(receipt, str):
        with open(receipt) as f:
            receipt = json.load(f)
    sn_id = receipt.get("sn_id")
    results = []
    all_pass = True

    for rm in receipt.get("removals", []):
        kind = rm.get("kind")
        target = rm.get("target")
        ok = False
        detail = ""
        if kind == "ledger_entry":
            entry = load_ledger()["entries"].get(sn_id)
            if entry is None:
                detail = "ledger entry missing entirely (tombstone deleted?)"
            elif entry.get("status") != "ROLLED_BACK":
                detail = (f"ledger status is {entry.get('status')}, "
                          f"expected ROLLED_BACK")
            else:
                cur_hash = _sha256_json(entry)
                if cur_hash == rm.get("post_file_sha256"):
                    ok = True
                    detail = "tombstone present, hash matches receipt"
                else:
                    detail = ("tombstone present but entry hash diverged "
                              "from receipt post-hash")
        elif kind == "learn_file_section":
            path = os.path.join(LEARN_DIR, target[len("learn/"):]) \
                if target.startswith("learn/") else target
            if not os.path.exists(path):
                detail = f"{target} missing"
            elif _sn_section_re(sn_id).search(open(path).read()):
                detail = f"section headed by {sn_id} still present"
            else:
                ok = True
                cur_hash = _sha256_text(open(path).read())
                detail = ("section absent; "
                          + ("file hash matches receipt post-hash"
                             if cur_hash == rm.get("post_file_sha256")
                             else "file changed after rollback "
                               "(later ingestions) — section still absent"))
        elif kind == "template_bullet":
            content = open(TEMPLATE_PATH).read()
            if _template_tag(sn_id) in content:
                detail = f"tag {_template_tag(sn_id)} still in template"
            else:
                ok = True
                detail = "no template lines tagged for this SN"
        elif kind == "agents_md_line":
            content = open(AGENTS_MD).read()
            if _agents_line_re(sn_id).search(content):
                detail = f"AGENTS.md line for {sn_id} still present"
            else:
                ok = True
                detail = "no AGENTS.md lines for this SN"
        elif kind == "ingest_receipt":
            rp = os.path.join(RECEIPTS_DIR, f"{sn_id}.json")
            if os.path.exists(rp):
                detail = "ingestion receipt file still exists"
            else:
                ok = True
                detail = "ingestion receipt file absent"
        else:
            detail = f"unknown removal kind: {kind}"
        results.append({"artifact": kind, "target": target,
                        "result": "PASS" if ok else "FAIL",
                        "detail": detail})
        all_pass = all_pass and ok

    verdict = "PASS" if (all_pass and results) else "FAIL"
    return {"sn_id": sn_id, "verdict": verdict,
            "passed": verdict == "PASS", "artifacts": results}

# ---------------------------------------------------------------- RUN

def detect_pending(ledger, branch_sha, tree):
    """Compute PENDING / PENDING_UPDATE / SKIPPED sets. Fetches blobs (slow)."""
    pending = []
    skipped = 0
    for t in tree:
        sn_id = sn_from_path(t["path"])
        if not sn_id:
            continue  # unparseable SN → handled in backfill ordering
        text = get_blob_text(t["sha"])
        sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
        entry = ledger["entries"].get(sn_id)
        if entry is None:
            pending.append((sn_id, t["path"], t["sha"], text, sha, "PENDING"))
        elif entry.get("status") == "ROLLED_BACK":
            # TOMBSTONE (POISON-4): rolled-back blocks are never re-queued,
            # even if the branch content changed after rollback.
            skipped += 1
        elif entry.get("content_sha256") != sha:
            pending.append((sn_id, t["path"], t["sha"], text, sha,
                            "PENDING_UPDATE"))
        else:
            skipped += 1
    pending.sort(key=lambda x: x[0])  # SN-ascending
    return pending, skipped


def process_note(sn_id, repo_path, blob_sha, text, sha, mode, ledger, run_id,
                 ingested_records, report):
    """Stages 2–6 for one note. Returns status string."""
    # TOMBSTONE (POISON-4): a rolled-back block must never be re-ingested,
    # no matter what the branch still contains. Refuse before parsing.
    prior_entry = ledger["entries"].get(sn_id)
    if prior_entry is not None and prior_entry.get("status") == "ROLLED_BACK":
        report.setdefault("tombstoned", []).append({"sn_id": sn_id})
        return "SKIPPED_TOMBSTONE"

    # PARSE
    try:
        rec = parse_note(text, repo_path, blob_sha)
    except ValueError as e:
        report["parse_errors"].append(
            {"sn_id": sn_id, "path": repo_path, "error": str(e)})
        return "PARSE_ERROR"

    # IMMUNE GATE (POISON-1/2): machine_view validation before anything
    # is integrated. A rejection leaves zero ingestible artifacts.
    rejected, reason = validate_machine_view(rec)
    if rejected:
        return reject_poison(sn_id, repo_path, blob_sha, text, sha, ledger,
                             run_id, report, rec, reason)

    # DEDUP: exact-duplicate rule_text → lower SN wins
    if rec["rule_text"]:
        norm = re.sub(r"\s+", " ", rec["rule_text"]).strip()
        for prev_id, prev in ledger["entries"].items():
            if prev_id >= sn_id:
                continue
            prev_rule = prev.get("rule_text_norm")
            if prev_rule and prev_rule == norm:
                ledger["entries"][sn_id] = {
                    "repo_path": repo_path, "content_sha256": sha,
                    "blob_sha": blob_sha, "ingested_at": utcnow(),
                    "status": "DUPLICATE_OF", "duplicate_of": prev_id,
                    "run_id": run_id,
                }
                report["duplicates"].append((sn_id, prev_id))
                return "DUPLICATE"

    # CLASSIFY
    ntype = classify(rec)
    flagged = authority_touch(rec)

    # CONTRADICTION TRIPWIRE (before integrate — both stay ACTIVE regardless)
    conflicts = contradiction_tripwire(rec, ingested_records)
    if conflicts:
        report["conflicts"].append((sn_id, conflicts))

    # INTEGRATE
    ingested_at = utcnow()
    integrations = integrate(rec, ntype, ingested_at, flagged)

    # VERIFY
    checks, all_pass = verify_integration(rec, integrations, run_id)
    receipt, status = write_receipt(rec, ntype, flagged, integrations,
                                    checks, all_pass, run_id)

    # RECORD (ledger entry)
    prior = ledger["entries"].get(sn_id)
    entry = {
        "repo_path": repo_path,
        "content_sha256": sha,
        "blob_sha": blob_sha,
        "ingested_at": ingested_at,
        "status": status,
        "run_id": run_id,
        "integrations": integrations,
        "receipt": f"learn/receipts/{sn_id}.json",
        "rule_text_norm": (re.sub(r"\s+", " ", rec["rule_text"]).strip()
                           if rec["rule_text"] else None),
        "classification": ntype,
    }
    if prior and mode == "PENDING_UPDATE":
        entry["supersedes"] = prior.get("ingested_at")
        receipt["supersedes"] = prior.get("ingested_at")
        with open(os.path.join(RECEIPTS_DIR, f"{sn_id}.json"), "w") as f:
            json.dump(receipt, f, indent=2, sort_keys=True)
    ledger["entries"][sn_id] = entry
    ingested_records.append(rec)

    report["ingested"].append(
        {"sn_id": sn_id, "type": ntype, "status": status,
         "title": rec["title"][:80],
         "flagged": flagged})
    if flagged:
        report["needs_shawn_word"].append(
            {"sn_id": sn_id, "rule": (rec["rule_text"] or "")[:300]})
    return status


def run_steady_state(run_id):
    report = {"ingested": [], "parse_errors": [], "duplicates": [],
              "conflicts": [], "needs_shawn_word": [], "skipped": 0}
    ledger = load_ledger()
    branch_sha = get_branch_sha()          # abort on failure — never stale
    tree = get_tree(branch_sha)
    ledger["branch_sha_at_scan"] = branch_sha

    pending, skipped = detect_pending(ledger, branch_sha, tree)
    report["skipped"] = skipped
    ingested_records = [
        {"sn_id": sid,
         "rule_text": e.get("rule_text_norm"),
         "taxonomy": []}
        for sid, e in ledger["entries"].items()
        if e.get("status") in ("INGESTED", "FLAGGED_AUTHORITY")
    ]

    log_lines = [f"\n## {utcnow()} — run {run_id} "
                 f"(branch {BRANCH} @ {branch_sha[:12]})"]
    for sn_id, path, blob_sha, text, sha, mode in pending:
        try:
            status = process_note(sn_id, path, blob_sha, text, sha, mode,
                                  ledger, run_id, ingested_records, report)
        except Exception as e:  # never let one note kill the run
            report["parse_errors"].append(
                {"sn_id": sn_id, "path": path,
                 "error": f"unexpected: {type(e).__name__}: {e}"})
            status = "ERROR"
        log_lines.append(f"- {status} {sn_id} ({path.split('/')[-1][:50]})")
    log_lines.append(f"- SKIPPED {skipped}: sha match (already ingested)")
    log_lines.append(f"- Ledger: {len(ledger['entries'])} entries.")
    append_log(log_lines)
    save_ledger(ledger)
    return report, branch_sha


def run_backfill(run_id):
    """One-time SN-ascending pass. Same pipeline, run_id=bootstrap-backfill."""
    report = {"ingested": [], "parse_errors": [], "duplicates": [],
              "conflicts": [], "needs_shawn_word": [], "skipped": 0,
              "unparseable": []}
    ledger = load_ledger()
    branch_sha = get_branch_sha()
    tree = get_tree(branch_sha)
    ledger["branch_sha_at_scan"] = branch_sha

    items = []
    for t in tree:
        sn_id = sn_from_path(t["path"])
        if not sn_id:
            report["unparseable"].append(t["path"])
            continue
        items.append((sn_id, t))
    items.sort(key=lambda x: x[0])

    ingested_records = []
    log_lines = [f"\n## {utcnow()} — BACKFILL {run_id} "
                 f"(branch {BRANCH} @ {branch_sha[:12]}, {len(items)} notes)"]
    for sn_id, t in items:
        if sn_id in ledger["entries"] and \
                ledger["entries"][sn_id].get("status") in (
                    "INGESTED", "FLAGGED_AUTHORITY", "DUPLICATE_OF"):
            # verify sha still matches; else re-ingest
            text = get_blob_text(t["sha"])
            sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
            if ledger["entries"][sn_id].get("content_sha256") == sha:
                report["skipped"] += 1
                continue
            mode = "PENDING_UPDATE"
        else:
            text = get_blob_text(t["sha"])
            sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
            mode = "PENDING"
        try:
            status = process_note(sn_id, t["path"], t["sha"], text, sha, mode,
                                  ledger, run_id, ingested_records, report)
        except Exception as e:
            report["parse_errors"].append(
                {"sn_id": sn_id, "path": t["path"],
                 "error": f"unexpected: {type(e).__name__}: {e}"})
            status = "ERROR"
        if status not in ("SKIPPED",):
            log_lines.append(f"- {status} {sn_id}")
    log_lines.append(
        f"- Backfill done: ingested={len(report['ingested'])}, "
        f"duplicates={len(report['duplicates'])}, "
        f"conflicts={len(report['conflicts'])}, "
        f"parse_errors={len(report['parse_errors'])}, "
        f"authority_flags={len(report['needs_shawn_word'])}, "
        f"skipped={report['skipped']}, unparseable={len(report['unparseable'])}.")
    append_log(log_lines)
    save_ledger(ledger)
    return report, branch_sha

# ---------------------------------------------------------------- CANARY + MAIN

def ledger_consistency_check(ledger):
    """Every INGESTED entry must have a receipt; every receipt in ledger."""
    problems = []
    for sid, e in ledger["entries"].items():
        if e.get("status") in ("INGESTED", "FLAGGED_AUTHORITY", "PARTIAL"):
            rp = os.path.join(RECEIPTS_DIR, f"{sid}.json")
            if not os.path.exists(rp):
                problems.append(f"{sid}: no receipt file")
    for fn in os.listdir(RECEIPTS_DIR):
        if fn.endswith(".json"):
            if fn.endswith(".rollback.json"):
                continue  # rollback receipts key to the tombstone entry
            sid = fn[:-5]
            if sid not in ledger["entries"]:
                problems.append(f"{sid}: receipt without ledger entry")
    return problems


def run_canary():
    """
    E2E proof per spec: synthetic canary note → ingest → render check →
    second run silent (idempotency).
    """
    print("=== CANARY TEST ===")
    run_id = "canary-" + utcnow().replace(":", "").replace("-", "")
    ledger = load_ledger()

    # Build a synthetic canary record (no GitHub needed)
    rec = {
        "sn_id": "SN-9999",
        "title": "Canary test note",
        "truth_state": "CANDIDATE",
        "taxonomy": ["TEST"],
        "rule_text": CANARY_RULE,
        "naya_note": "",
        "nutshell": "Synthetic canary for E2E proof.",
        "evidence_refs": None,
        "cousins": [],
        "status_text": None,
        "source_path": "CANARY (synthetic)",
        "content_sha256": hashlib.sha256(CANARY_RULE.encode()).hexdigest(),
        "blob_sha": "canary",
    }
    ntype = classify(rec)
    print(f"1. classify → {ntype}")
    assert ntype == "UNCATEGORIZED", f"expected UNCATEGORIZED, got {ntype}"

    # Force DOCTRINE routing for the render check by taxonomy override
    rec["taxonomy"] = ["TEST-DOCTRINE", "doctrine"]
    ntype = classify(rec)
    print(f"2. classify (doctrine taxonomy) → {ntype}")
    assert ntype == "DOCTRINE", f"expected DOCTRINE, got {ntype}"

    flagged = authority_touch(rec)
    print(f"3. authority_touch → {flagged}")
    assert not flagged, "canary must not be authority-touching"

    ingested_at = utcnow()
    integrations = integrate(rec, ntype, ingested_at, flagged)
    print(f"4. integrate → {integrations}")

    checks, all_pass = verify_integration(rec, integrations, run_id)
    for c in checks:
        print(f"   check {c['check']}: {c['result']}")
    assert all_pass, "verification checks must all PASS"

    rendered = render_template()
    assert CANARY_RULE.split(".")[0] in rendered, \
        "canary bullet missing from rendered brief"
    print("5. template_render_check → canary bullet present in render ✓")

    # Idempotency: second integrate must be a no-op
    before = open(TEMPLATE_PATH).read()
    integrations2 = integrate(rec, ntype, ingested_at, flagged)
    after = open(TEMPLATE_PATH).read()
    assert before == after, "second integrate wrote changes — not idempotent"
    actions = [i.get("template_action") for i in integrations2]
    print(f"6. idempotency → second run actions: {actions} (no writes) ✓")

    # Cleanup: remove canary bullet + doctrine section + AGENTS.md untouched
    # (canary never touched AGENTS.md — not PROCESS_FIX)
    content = open(TEMPLATE_PATH).read()
    content = "\n".join(l for l in content.splitlines()
                        if "(SN-9999)" not in l)
    open(TEMPLATE_PATH, "w").write(content + ("\n" if not content.endswith("\n") else ""))
    dpath = learn_file("doctrine.md")
    dcontent = open(dpath).read()
    # remove the canary section (from "## SN-9999" to next "## " or EOF)
    dcontent = re.sub(r"\n## SN-9999 —.*?(?=\n## |\Z)", "", dcontent,
                      flags=re.DOTALL)
    open(dpath, "w").write(dcontent)
    rpath = os.path.join(RECEIPTS_DIR, "SN-9999.json")
    if os.path.exists(rpath):
        os.remove(rpath)
    print("7. cleanup → canary artifacts removed ✓")
    print("=== CANARY: PASS ===")


def print_report(report):
    print(f"\nIngested: {len(report['ingested'])}")
    for i in report["ingested"]:
        flag = " [NEEDS_SHAWN_WORD]" if i["flagged"] else ""
        print(f"  {i['status']:12s} {i['sn_id']} ({i['type']}){flag}")
        print(f"               {i['title']}")
    if report["duplicates"]:
        print(f"Duplicates: {report['duplicates']}")
    if report["conflicts"]:
        print(f"Conflicts flagged: {len(report['conflicts'])}")
        for sn, others in report["conflicts"][:10]:
            print(f"  {sn} × {others}")
    if report["parse_errors"]:
        print(f"PARSE ERRORS: {len(report['parse_errors'])}")
        for e in report["parse_errors"][:10]:
            print(f"  {e['sn_id']}: {e['error'][:120]}")
    if report["needs_shawn_word"]:
        print(f"NEEDS_SHAWN_WORD: {len(report['needs_shawn_word'])}")
        for f_ in report["needs_shawn_word"]:
            print(f"  {f_['sn_id']}: {f_['rule'][:120]}")
    print(f"Skipped (already ingested): {report['skipped']}")


def main():
    os.makedirs(RECEIPTS_DIR, exist_ok=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "run"
    if mode == "--canary":
        run_canary()
        return
    if mode == "--rollback":
        if len(sys.argv) < 3:
            print("usage: learn_ingest.py --rollback SN-XXXX [reason]",
                  file=sys.stderr)
            sys.exit(2)
        sn_id = sys.argv[2]
        reason = sys.argv[3] if len(sys.argv) > 3 else "manual rollback"
        try:
            receipt = rollback(sn_id, reason)
        except ValueError as e:
            print(f"ROLLBACK FAILED: {e}", file=sys.stderr)
            sys.exit(2)
        print(json.dumps(receipt, indent=2, sort_keys=True))
        vr = verify_rollback(receipt)
        print(f"verify_rollback: {vr['verdict']}")
        sys.exit(0 if vr["passed"] else 1)
    run_id = ("bootstrap-backfill" if mode == "--backfill"
              else utcnow().replace(":", "").replace("-", ""))
    try:
        if mode == "--backfill":
            report, _ = run_backfill(run_id)
        else:
            report, _ = run_steady_state(run_id)
    except RuntimeError as e:
        print(f"ABORTED: {e}", file=sys.stderr)
        sys.exit(2)
    ledger = load_ledger()
    problems = ledger_consistency_check(ledger)
    if problems:
        print("LEDGER INCONSISTENT:", file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        sys.exit(3)
    print_report(report)


if __name__ == "__main__":
    main()
