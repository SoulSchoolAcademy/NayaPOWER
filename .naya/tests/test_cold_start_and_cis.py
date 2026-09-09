#!/usr/bin/env python3
"""Cold-start and next-day CIS acceptance checks."""
from __future__ import annotations
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/".naya"/"runtime")); sys.path.insert(0,str(ROOT/".naya"/"memory"))
from cis_state import build

def run_restore(root:Path):
    script=root/".naya"/"runtime"/"restore_context.py"
    env=os.environ.copy(); env["PYTHONDONTWRITEBYTECODE"]="1"
    return subprocess.run([sys.executable,str(script),"restore","Superbrain","--limit","5"],cwd=root,text=True,capture_output=True,env=env)

def assert_code_of_honor(root:Path):
    start=(root/"SUPERBRAIN"/"AI-BOOT"/"START-HERE.md").read_text(encoding="utf-8")
    honor=(root/"SUPERBRAIN"/"MASTER-NOTES"/"SN-20260827-NAYA-CODE-OF-HONOR.md").read_text(encoding="utf-8")
    assert "SN-20260827-NAYA-CODE-OF-HONOR.md" in start
    assert "CREATE THE MOST HUMAN VALUE POSSIBLE WITH EVERY MEANINGFUL ACTION." in honor
    assert "ZOOM OUT → ZOOM IN → CONNECT → PRIORITIZE → OPTIMIZE → EXECUTE → VERIFY → LEARN → COMPOUND" in honor
    assert "Every Naya operating through a NayaPOWER-governed Naya Brain inherits this Code of Honor" in honor

def assert_restored(proc):
    if proc.returncode!=0: raise SystemExit(f"cold-start restore must be VERIFIED; exit={proc.returncode}: {proc.stderr or proc.stdout}")
    data=json.loads(proc.stdout)
    required=["current_state","repository_reality","memory","validation","next_best_action"]
    missing=[k for k in required if k not in data]
    if missing: raise SystemExit("cold-start missing: "+", ".join(missing))
    failures=[]
    if data.get("status")!="VERIFIED": failures.append(f"status={data.get('status')!r}")
    if data.get("repository_reality",{}).get("available") is not True: failures.append(f"repository_available={data.get('repository_reality',{}).get('available')!r}")
    if data.get("repository_reality",{}).get("clean") is not True: failures.append(f"repository_clean={data.get('repository_reality',{}).get('clean')!r} working_tree_status={data.get('repository_reality',{}).get('working_tree_status')!r}")
    if data.get("validation",{}).get("passed") is not True: failures.append(f"validation={data.get('validation')!r}")
    if not data.get("current_state"): failures.append("current_state empty")
    if not data.get("next_best_action"): failures.append(f"next_best_action={data.get('next_best_action')!r}")
    if failures: raise SystemExit("cold-start assertion details: " + "; ".join(failures))
    return data

def main():
    assert_code_of_honor(ROOT)
    live=assert_restored(run_restore(ROOT))
    with tempfile.TemporaryDirectory() as tmp:
        fresh=Path(tmp); shutil.copytree(ROOT/".naya",fresh/".naya"); shutil.copytree(ROOT/"SUPERBRAIN",fresh/"SUPERBRAIN")
        subprocess.run(["git","init","-q"],cwd=fresh,check=True); subprocess.run(["git","config","user.email","naya-test@example.invalid"],cwd=fresh,check=True); subprocess.run(["git","config","user.name","Naya Cold Start Test"],cwd=fresh,check=True); subprocess.run(["git","config","maintenance.auto","false"],cwd=fresh,check=True); subprocess.run(["git","config","gc.auto","0"],cwd=fresh,check=True); subprocess.run(["git","add",".naya","SUPERBRAIN"],cwd=fresh,check=True); subprocess.run(["git","commit","-qm","cold-start fixture"],cwd=fresh,check=True); assert_code_of_honor(fresh); cold=assert_restored(run_restore(fresh))
    state=build("2026-08-25"); assert state["source_period"]=="2026-08-25" and state["next_day"]=="2026-08-26"; assert state["verification_required"] is True
    print(json.dumps({"status":"GREEN","restore_status":live["status"],"fresh_checkout_restore_status":cold["status"],"code_of_honor":"VERIFIED_FROM_FRESH_FIXTURE","head_sha":live["repository_reality"].get("head_sha"),"required_fields_verified":["current_state","repository_reality","memory","validation","next_best_action"],"next_day_state":"DERIVED_PENDING_VERIFICATION","source_event_count":state["source_event_count"]},indent=2))
if __name__=="__main__": main()
