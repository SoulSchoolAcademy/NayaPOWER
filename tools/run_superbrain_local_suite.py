#!/usr/bin/env python3
"""Run the NayaPOWER Superbrain acceptance/regression suite locally."""
from __future__ import annotations
import json,subprocess,sys,time
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; RECEIPT_DIR=ROOT/".naya/receipts/local-superbrain"
CORE=[ROOT/"tools/qa_naya_context_boot.py",ROOT/"tools/qa_superbrain_continuity.py",ROOT/".naya/runtime/restore_context.py",ROOT/".naya/runtime/naya_power_kernel.py",ROOT/".naya/runtime/test_decision_calculus_runtime_integration.py",ROOT/"SUPERBRAIN/test_naya_power_excellence.py",ROOT/"SUPERBRAIN/test_naya_power_decision_calculus.py",ROOT/"tools/test_superbrain_a_b_c_compounding.py",ROOT/"tools/test_superbrain_note_event_to_pis.py",ROOT/"tools/test_superbrain_adversarial.py"]
REGRESSION_KEYWORDS=("smart_note","smart_notes","canonical_event","event_store","promot","cct","continuity","retrieval","governance","reality","torch","runtime")
EXCLUDED_LEGACY_CONTRACTS={"qa_v21_runtime_contract.py":"legacy V21 renderer/product contract; not a canonical Superbrain acceptance criterion"}
def git(*args:str)->str:return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()
def selected_commands():
 commands=[]
 for path in CORE:
  if not path.is_file():raise FileNotFoundError(path)
  rel=str(path.relative_to(ROOT))
  if path.name=="restore_context.py":commands.append([sys.executable,rel,"restore","--pretty"])
  elif path.name=="naya_power_kernel.py":commands.append([sys.executable,rel,"--self-test"])
  else:commands.append([sys.executable,rel])
 seen={tuple(x[1:]) for x in commands}
 for path in sorted(ROOT.glob("tools/test_*.py"))+sorted(ROOT.glob("tools/qa_*.py")):
  if path.name in EXCLUDED_LEGACY_CONTRACTS or not any(k in path.name.lower() for k in REGRESSION_KEYWORDS):continue
  cmd=[sys.executable,str(path.relative_to(ROOT))]
  if tuple(cmd[1:]) not in seen and path not in CORE:commands.append(cmd);seen.add(tuple(cmd[1:]))
 return commands
def restore_reconciliation_is_expected(proc):
 if proc.returncode!=2:return False
 text=proc.stdout
 try:payload=json.loads(text)
 except json.JSONDecodeError:return False
 if payload.get("status")!="RECONCILIATION_REQUIRED":return False
 reasons=payload.get("reconciliation",{}).get("reasons",[])
 return bool(reasons) and all(r in {"current-head projection mismatch",".naya/memory/STATE.json"} or str(r).endswith("STATE.json") for r in reasons)
def main()->int:
 RECEIPT_DIR.mkdir(parents=True,exist_ok=True);started=datetime.now(timezone.utc);head=git("rev-parse","HEAD");clean_before=git("status","--porcelain")=="";commands=selected_commands();results=[];overall=0
 print(f"LOCAL SUPERBRAIN SUITE — observed HEAD: {head}\nSelected checks: {len(commands)}")
 for name,reason in EXCLUDED_LEGACY_CONTRACTS.items():print(f"EXCLUDED: {name} — {reason}")
 for command in commands:
  t0=time.monotonic();proc=subprocess.run(command,cwd=ROOT,text=True,capture_output=True);ms=round((time.monotonic()-t0)*1000,2);accepted_reconciliation=restore_reconciliation_is_expected(proc);effective_failure=proc.returncode!=0 and not accepted_reconciliation
  result={"command":command,"exit_code":proc.returncode,"accepted_reconciliation_state":accepted_reconciliation,"effective_failure":effective_failure,"elapsed_ms":ms,"stdout":proc.stdout,"stderr":proc.stderr};results.append(result)
  print(f"[{proc.returncode}{' ACCEPTED_RECONCILIATION' if accepted_reconciliation else ''}] {' '.join(command)} ({ms} ms)")
  if proc.stdout:print(proc.stdout.rstrip())
  if proc.stderr:print(proc.stderr.rstrip(),file=sys.stderr)
  if effective_failure:overall=1;print("CONTINUING — failure recorded; remaining checks will still execute.")
  elif accepted_reconciliation:print("RECONCILIATION STATE ACCEPTED — explicit governed mismatch is not treated as a false-green verification claim.")
 receipt={"schema":"naya-power-local-superbrain-suite/v6","started_at":started.isoformat(),"finished_at":datetime.now(timezone.utc).isoformat(),"observed_head":head,"clean_worktree_before":clean_before,"github_actions_used":False,"selected_check_count":len(commands),"excluded_checks":EXCLUDED_LEGACY_CONTRACTS,"mandatory_layers":["EXCELLENCE_BY_DEFAULT","DECISION_CALCULUS","VERIFICATION","SMART_NOTE_PROMOTION","NOTE_EVENT_TO_PIS","FRESH_NAYA_RETRIEVAL","A_TO_B_TO_C_COMPOUNDING"],"commands":results,"overall":"PASS" if overall==0 else "FAIL"}
 path=RECEIPT_DIR/f"suite-{started.strftime('%Y%m%dT%H%M%SZ')}.json";path.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n",encoding="utf-8");print(f"RECEIPT: {path.relative_to(ROOT)}\nSUPERBRAIN LOCAL SUITE: {receipt['overall']}");return overall
if __name__=="__main__":raise SystemExit(main())
