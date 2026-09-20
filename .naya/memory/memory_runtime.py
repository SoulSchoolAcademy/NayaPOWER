#!/usr/bin/env python3
"""Naya Power Smart Notes runtime: validate, retrieve, and restore context.

Standard-library only. Designed to be deterministic, inspectable, and CI-friendly.
It does not claim vector/embedding semantics; alias and relationship retrieval are
explicitly represented so a future semantic index can be added without changing
note contracts.
"""
from __future__ import annotations
import argparse, json, re, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MEMORY = ROOT / ".naya" / "memory"
INDEX = MEMORY / "INDEX.json"
STATE = MEMORY / "STATE.json"
SCHEMA = MEMORY / "note.schema.json"
NOTE_DIR = MEMORY / "notes"
NOTE_ID_RE = re.compile(r"^SN-[0-9]{8}-[0-9]{6}-[a-z0-9-]+$")
REQUIRED = {"id","type","title","status","created_at","effective_at","source","summary","what_happened","what_we_learned","why_it_matters","what_changed","next_best_action","tags","aliases","relationships"}
STATUSES = {"ACTIVE","CANONICAL","HISTORICAL","SUPERSEDED","CONFLICTED","STALE"}
TYPES = {"decision","lesson","discovery","correction","architecture","preference","milestone","handoff","failure","fact","strategy"}


def iso(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        raise ValueError("timestamp must include timezone")
    return dt


def tokens(text: str):
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def notes():
    if not NOTE_DIR.exists():
        return []
    out=[]
    for p in sorted(NOTE_DIR.glob("*.json")):
        try:
            out.append((p, load_json(p)))
        except Exception as exc:
            out.append((p, {"__parse_error__": str(exc)}))
    return out


def validate_note(note, path):
    errors=[]
    missing=REQUIRED-set(note)
    if missing: errors.append(f"{path}: missing {sorted(missing)}")
    if note.get("id") and not NOTE_ID_RE.match(note["id"]): errors.append(f"{path}: invalid id")
    if note.get("type") not in TYPES: errors.append(f"{path}: invalid type")
    if note.get("status") not in STATUSES: errors.append(f"{path}: invalid status")
    for key in ("created_at","effective_at"):
        if key in note:
            try: iso(note[key])
            except Exception as exc: errors.append(f"{path}: invalid {key}: {exc}")
    if note.get("superseded_at"):
        try: iso(note["superseded_at"])
        except Exception as exc: errors.append(f"{path}: invalid superseded_at: {exc}")
    if not isinstance(note.get("tags"), list) or not note.get("tags"): errors.append(f"{path}: tags must be a non-empty list")
    if not isinstance(note.get("aliases"), list): errors.append(f"{path}: aliases must be a list")
    if not isinstance(note.get("what_we_learned"), list): errors.append(f"{path}: what_we_learned must be a list")
    if not isinstance(note.get("what_changed"), list): errors.append(f"{path}: what_changed must be a list")
    if not isinstance(note.get("relationships"), dict): errors.append(f"{path}: relationships must be an object")
    if note.get("status") == "SUPERSEDED" and not (note.get("superseded_at") or note.get("relationships",{}).get("superseded_by")):
        errors.append(f"{path}: SUPERSEDED note must identify when/by what it was superseded")
    if note.get("status") == "CANONICAL" and note.get("relationships",{}).get("superseded_by"):
        errors.append(f"{path}: CANONICAL note cannot have superseded_by")
    return errors


def validate():
    errors=[]
    for required in (INDEX, STATE, SCHEMA):
        if not required.exists(): errors.append(f"missing runtime file: {required}")
    all_notes=notes()
    ids={}
    for p,n in all_notes:
        if "__parse_error__" in n:
            errors.append(f"{p}: {n['__parse_error__']}"); continue
        errors.extend(validate_note(n,p))
        nid=n.get("id")
        if nid in ids: errors.append(f"duplicate note id: {nid} ({ids[nid]} and {p})")
        ids[nid]=str(p)
        for rel_key in ("related","depends_on"):
            for target in n.get("relationships",{}).get(rel_key,[]) or []:
                if target not in ids: pass  # second-pass check below
        for target_key in ("supersedes","superseded_by"):
            target=n.get("relationships",{}).get(target_key)
            if target and target == nid: errors.append(f"{p}: self-referential {target_key}")
    for p,n in all_notes:
        if "__parse_error__" in n: continue
        for rel_key in ("related","depends_on"):
            for target in n.get("relationships",{}).get(rel_key,[]) or []:
                if target not in ids: errors.append(f"{p}: {rel_key} references missing note {target}")
        for target_key in ("supersedes","superseded_by"):
            target=n.get("relationships",{}).get(target_key)
            if target and target not in ids: errors.append(f"{p}: {target_key} references missing note {target}")
    try:
        idx=load_json(INDEX)
        indexed=[x for x in idx.get("notes",[]) if isinstance(x,str)]
        actual=list(ids)
        if sorted(indexed)!=sorted(actual): errors.append("INDEX.json does not exactly match note IDs")
    except Exception as exc: errors.append(f"INDEX.json invalid: {exc}")
    return errors


def score(note, query):
    q=tokens(query)
    if not q: return 0
    title=tokens(note.get("title","")); tags=tokens(" ".join(note.get("tags",[])))
    aliases=tokens(" ".join(note.get("aliases",[])))
    body=tokens(" ".join([note.get("summary",""),note.get("content",""),note.get("why_it_matters","")," ".join(note.get("what_we_learned",[]))]))
    s=0
    s += len(q & title)*100
    s += len(q & aliases)*70
    s += len(q & tags)*60
    s += len(q & body)*25
    if q.issubset(title|aliases|tags): s += 80
    s += {"ACTIVE":30,"CANONICAL":25,"HISTORICAL":0,"SUPERSEDED":-60,"STALE":-40,"CONFLICTED":-20}.get(note.get("status"),0)
    return s


def retrieve(query, limit=10):
    found=[]
    for p,n in notes():
        if "__parse_error__" in n: continue
        s=score(n,query)
        if s>0: found.append((s,n))
    found.sort(key=lambda x:(-x[0], x[1].get("effective_at",""), x[1].get("id","")), reverse=False)
    return found[:limit]


def restore(query=""):
    state=load_json(STATE)
    result={"current_state":state,"retrieved":[]}
    if query:
        result["retrieved"]=[{"score":s,"note":n} for s,n in retrieve(query,10)]
    result["next_best_action"]=state.get("next_best_action")
    return result


def main():
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest="cmd",required=True)
    sub.add_parser("validate")
    r=sub.add_parser("retrieve"); r.add_argument("query"); r.add_argument("--limit",type=int,default=10)
    b=sub.add_parser("restore"); b.add_argument("query",nargs="?",default="")
    a=ap.parse_args()
    if a.cmd=="validate":
        errors=validate()
        if errors:
            print("FAIL"); print("\n".join(f"- {e}" for e in errors)); return 1
        print("PASS — Smart Notes runtime is structurally valid")
        return 0
    if a.cmd=="retrieve":
        for s,n in retrieve(a.query,a.limit): print(f"{s:4} {n['id']} | {n['title']} | {n['status']}")
        return 0
    print(json.dumps(restore(a.query),indent=2,ensure_ascii=False))
    return 0

if __name__=="__main__": sys.exit(main())
