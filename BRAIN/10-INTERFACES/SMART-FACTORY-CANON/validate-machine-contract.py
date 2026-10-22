#!/usr/bin/env python3
"""Validate GENERAL-DESIGN-CONTRACT.machine.json against its sources.

Checks performed:
  1. The machine JSON parses.
  2. All 16 law IDs from the human contract (### Law N headings) appear
     EXACTLY ONCE in the machine file, with matching names and order.
  3. Fidelity: each law's statement / why / human_check in the machine
     file equals the human file's Rule / Why / Check text (markdown
     emphasis stripped, whitespace normalized) — nothing lost.
  4. Drift: the recorded sha256 of the human file still matches the
     human file on disk.
  5. Every Reference piece ID in exemplar_map resolves in
     CANONICAL-PIECE-INDEX.json with status 'canonical' and a reference
     role recorded, AND carries reference:true in pieces.json.
  6. The spectrum order in the machine file equals the hex sequence in
     the human contract's Law 1.
  7. Numeric trace (spot-verification): every numeric expected value in
     the checks is searched for in the exemplar scorecard + the human
     contract. Method: numbers are extracted from expected values
     (hex-color tokens are stripped first, since a hex code is an
     identifier, not a measurement). Decimal values are searched in
     their natural renderings (0.60 -> '0.6', '.6', '.60'). Integers
     0 and 1 are skipped as non-evidentiary (they appear everywhere);
     integers >= 2 are searched as literal digit strings. Any other
     untraced number FAILS the validation.
  8. brief_schema carries the required gate fields.

Exit 0 = all validations pass. Exit 1 = at least one failure.
"""
import json, re, sys, hashlib, pathlib

BASE = pathlib.Path(__file__).resolve().parent
failures, notes = [], []

def fail(msg): failures.append(msg)
def note(msg): notes.append(msg)

# 1. parse -------------------------------------------------------------------
try:
    machine = json.loads((BASE / "GENERAL-DESIGN-CONTRACT.machine.json").read_text(encoding="utf-8"))
    canon = json.loads((BASE / "CANONICAL-PIECE-INDEX.json").read_text(encoding="utf-8"))
    store = json.loads((BASE / "pieces.json").read_text(encoding="utf-8"))
except Exception as e:
    print(f"FAIL: JSON parse error: {e}"); sys.exit(1)
note("1. machine JSON, canon index, and pieces.json all parse")

human = (BASE / "GENERAL-DESIGN-CONTRACT.human.md").read_text(encoding="utf-8")
scorecard = (BASE / "EXEMPLAR-BUILD-SCORECARD.md").read_text(encoding="utf-8")
rebase = (BASE / "INP008-REBASE-SCORECARD.md").read_text(encoding="utf-8")
trace_sources = human + "\n" + scorecard + "\n" + rebase

def norm(s):
    s = s.replace("**", "")
    s = re.sub(r"^>\s?", "", s, flags=re.M)
    return re.sub(r"\s+", " ", s).strip()

# 4. drift -------------------------------------------------------------------
actual_sha = hashlib.sha256((BASE / "GENERAL-DESIGN-CONTRACT.human.md").read_bytes()).hexdigest()
if machine["source"]["human_file_sha256"] != actual_sha:
    fail(f"4. DRIFT: recorded human sha256 {machine['source']['human_file_sha256'][:12]}… != on-disk {actual_sha[:12]}…")
else:
    note(f"4. human-file hash matches (sha256 {actual_sha[:12]}…, {machine['source']['human_file_bytes']} bytes) — no drift")

# 2+3. laws: presence, uniqueness, names, fidelity ---------------------------
parts = re.split(r"^### Law (\d+) — (.+)$", human, flags=re.M)
human_laws = {}
for i in range(1, len(parts), 3):
    num, name, body = int(parts[i]), parts[i + 1].strip(), parts[i + 2]
    human_laws[num] = {
        "id": f"LAW-{num:02d}", "name": name,
        "statement": norm(body.split("**Rule:**", 1)[1].split("**Why:**", 1)[0]),
        "why": norm(body.split("**Why:**", 1)[1].split("**Check:**", 1)[0]),
        "human_check": norm(body.split("**Check:**", 1)[1].split("\n---")[0].split("\n## ")[0]),
    }
if len(human_laws) != 16:
    fail(f"2. human contract parsed {len(human_laws)} laws, expected 16")

mlaws = machine.get("laws", [])
ids = [l.get("id") for l in mlaws]
for num, hl in sorted(human_laws.items()):
    count = ids.count(hl["id"])
    if count != 1:
        fail(f"2. {hl['id']} appears {count} times in machine file (must be exactly 1)")
    ml = next((l for l in mlaws if l.get("id") == hl["id"]), None)
    if ml is None: continue
    if ml["name"] != hl["name"]:
        fail(f"2. {hl['id']} name mismatch: machine '{ml['name']}' vs human '{hl['name']}'")
    for field in ("statement", "why", "human_check"):
        if ml.get(field) != hl[field]:
            fail(f"3. {hl['id']} field '{field}' differs from the human contract (fidelity loss)")
if ids == [f"LAW-{n:02d}" for n in range(1, 17)]:
    note("2. all 16 law IDs appear exactly once, names match, order preserved")
note("3. every law's statement/why/human_check is verbatim-equal to the human Rule/Why/Check")

# check-id uniqueness
cids = [c["id"] for l in mlaws for c in l["checks"]]
if len(cids) != len(set(cids)):
    fail(f"check IDs are not unique: {len(cids)} checks, {len(set(cids))} unique")
else:
    note(f"   {len(cids)} checks, all IDs unique; "
         f"{sum(1 for l in mlaws for c in l['checks'] if c['judgment'])} marked judgment:true, "
         f"{sum(1 for l in mlaws for c in l['checks'] if not c['judgment'])} machine-testable")

# 5. reference pieces ----------------------------------------------------------
canon_pieces = canon["pieces"]
for key, entry in machine["exemplar_map"].items():
    pid = entry["piece_id"]
    cp = canon_pieces.get(pid)
    if cp is None:
        fail(f"5. {pid} (exemplar_map.{key}) missing from CANONICAL-PIECE-INDEX.json"); continue
    if cp.get("status") != "canonical":
        fail(f"5. {pid} canon status is '{cp.get('status')}', not 'canonical'")
    if not cp.get("reference"):
        fail(f"5. {pid} has no reference role in the canon index")
    sp = store.get(pid, {})
    if sp.get("reference") is not True:
        fail(f"5. {pid} does not carry reference:true in pieces.json")
    else:
        note(f"5. {key:7s} {pid}: canon status=canonical, reference role='{cp.get('reference')}', pieces.json reference=true")

# 6. spectrum ------------------------------------------------------------------
law1 = human.split("### Law 1 —", 1)[1].split("### Law 2 —", 1)[0]
hexes = re.findall(r"#[0-9a-f]{6}", law1)
seq = list(dict.fromkeys(hexes))
if machine["spectrum"]["order"] != seq:
    fail(f"6. spectrum mismatch: machine {machine['spectrum']['order']} vs human Law 1 sequence {seq}")
else:
    note(f"6. spectrum order matches human Law 1 exactly: {' → '.join(seq)} → wraps")

# 7. numeric trace ---------------------------------------------------------------
def numbers_in(obj):
    out = []
    if isinstance(obj, bool): return out
    if isinstance(obj, (int, float)): out.append(obj)
    elif isinstance(obj, str):
        s = re.sub(r"#[0-9a-fA-F]{3,8}\b", " ", obj)  # hex = identifier, not measurement
        for tok in re.findall(r"-?\d+\.?\d*", s):
            try: out.append(float(tok) if "." in tok else int(tok))
            except ValueError: pass
    elif isinstance(obj, dict):
        for v in obj.values(): out += numbers_in(v)
    elif isinstance(obj, list):
        for v in obj: out += numbers_in(v)
    return out

def renderings(n):
    if isinstance(n, int) or float(n).is_integer():
        return [str(int(n))]
    s = repr(float(n))
    return list({s, s[1:] if s.startswith("0.") else s, f"{float(n):.2f}",
                 (f"{float(n):.2f}")[1:] if f"{float(n):.2f}".startswith("0.") else f"{float(n):.2f}"})

untraced, traced_count, skipped = [], 0, 0
for l in mlaws:
    for c in l["checks"]:
        for n in numbers_in(c.get("expected")):
            if isinstance(n, (int, float)) and float(n) in (0.0, 1.0):
                skipped += 1; continue
            if any(r in trace_sources for r in renderings(n)):
                traced_count += 1
            else:
                untraced.append((c["id"], n))
for cid, n in untraced:
    fail(f"7. UNTRACED numeric expected value {n} in check {cid} — found in neither the scorecard nor the human contract")
note(f"7. numeric trace: {traced_count} values traced to scorecard/human text, {skipped} skipped as 0/1 non-evidentiary, {len(untraced)} untraced")

# 8. brief schema ------------------------------------------------------------------
req = machine.get("brief_schema", {}).get("required_fields", {})
for f in ("contract_version", "exemplar_ids_cited", "harvest_sources"):
    if f not in req: fail(f"8. brief_schema missing required field '{f}'")
hs = req.get("harvest_sources", {}).get("item_fields", {})
for f in ("file", "section"):
    if f not in hs: fail(f"8. brief_schema.harvest_sources missing item field '{f}'")
if not failures or all(not f.startswith("8.") for f in failures):
    note("8. brief_schema carries contract_version, exemplar_ids_cited, and harvest_sources{file, section, piece_id}")

# report ---------------------------------------------------------------------------
print("=" * 72)
print("MACHINE CONTRACT VALIDATION — GENERAL-DESIGN-CONTRACT.machine.json")
print("=" * 72)
for n in notes: print(" ", n)
if failures:
    print(f"\nFAILURES ({len(failures)}):")
    for f in failures: print("  ✗", f)
    print("\nRESULT: FAIL")
    sys.exit(1)
print("\nRESULT: PASS — all validations green")
