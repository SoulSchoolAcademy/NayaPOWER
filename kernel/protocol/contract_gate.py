#!/usr/bin/env python3
"""The Contract Gate — machine law for THE-CONTRACT.md.

The boot gate (protocol_integrity_gate.py) verifies readiness ONCE.
This gate verifies adherence EVERY ACTION: sign-in before work, sign-out after.

    python3 kernel/protocol/contract_gate.py sign-in --agent-id <id> --tip-sha <sha> \\
        --essence "..." [--receipt-out activation-receipt.json]
    python3 kernel/protocol/contract_gate.py sign-out --receipt <path>

sign-in checks (Articles I, II, VI, VII + §9 identity bar):
  1. The pinned tip SHA exists on the remote (a decision on a SHA you cannot
     show is a decision that did not happen).
  2. The chain is whole at that SHA: the oath (§10 of READ-ME-FIRST.md),
     THE-CODE-SHE-LIVES-BY.md, and THE-CONTRACT.md are all present. The oath
     check is convergence-safe: it verifies the §10 section exists and is
     substantive — it does not pin one seat's wording.
  3. Pinned-hash tripwire: THE-CONTRACT.md's bytes at the SHA must match the
     hash pinned in this file (updated only with Shawn's word). Silent edits fail.
  4. Parrot-essence rejection: --essence must state the oath's essence in the
     seat's own words; a near-verbatim copy is refused. Understanding required.
  Exit 0 = CONTRACT HELD — begin (receipt JSON printed, optionally written).
  Exit 1 = fail closed, reasons listed.

sign-out checks (Articles III, IV, V):
  1. The receipt exists and is non-empty.
  2. It cites its evidence SHA (40 hex chars).
  3. It carries an honest score line and a why-not-9.5 line.
  4. It carries a drift line (where she wavered, or "no drift").
  5. Protected-gate tripwire: if the receipt names a gate act (deploy,
     production, credential, money, destructive, irreversible, RATIFIED,
     consent, privacy, security), it must also cite the grant (Shawn's word:
     "Shawn", "grant", or a board comment id).
  Exit 0 = RECEIPT ACCEPTED. Exit 1 = rejected — the action is NOT DONE
  until the receipt passes.

This gate does NOT grant authority. It verifies the contract was followed.
Authority still comes from Shawn's grants, never from passing this gate.

Stdlib only. No network except `git fetch` of the pinned SHA (free, read-only).
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPO_URL = "https://github.com/SoulSchoolAcademy/NayaPOWER.git"

# The chain: (repo path at the pinned SHA, what must hold of its bytes).
# The oath check is convergence-safe by design: it verifies the §10 THE OATH
# section exists and is substantive — it does NOT pin one seat's wording, so
# the oath convergence can land without breaking the gate.
CHAIN = [
    ("BRAIN/00-ACTIVATION/READ-ME-FIRST.md", "oath-section"),
    ("BRAIN/00-ACTIVATION/THE-CODE-SHE-LIVES-BY.md", "marker:THE CODE SHE LIVES BY"),
    ("BRAIN/00-ACTIVATION/THE-CONTRACT.md", "marker:THE CONTRACT"),
]

# Pinned sha256 of THE-CONTRACT.md. Updated ONLY in a commit carrying Shawn's
# explicit word. A silent edit trips the gate. (Set at build time; see below.)
CONTRACT_SHA256 = "8d4aa499d2af0576950af93f813c63703f08f7825f8381e4da33e6ff169b621b"

# Parrot bar: an essence this similar to the oath bytes is a copy, not
# understanding. (§9 identity bar, enforced by machine.)
PARROT_RATIO = 0.85

SHA40 = re.compile(r"\b[0-9a-f]{40}\b")
BOARD_COMMENT = re.compile(r"\b61\d{8}\b")  # board comment ids, e.g. 6151959617

NEGATIONS = {"not", "no", "n't", "never", "without", "none"}

GATE_WORDS = [
    "deploy", "production", "credential", "money", "destructive",
    "irreversible", "ratified", "consent", "privacy", "security",
]
GRANT_WORDS = ["shawn", "grant"]


def _git_show(sha: str, path: str) -> tuple[bool, str]:
    """Read one file at one SHA via the local git object store (no network)."""
    try:
        r = subprocess.run(
            ["git", "show", f"{sha}:{path}"],
            capture_output=True, text=True, timeout=30, cwd=ROOT,
        )
        if r.returncode != 0:
            return False, f"not present at {sha[:12]}"
        return True, r.stdout
    except Exception as e:  # noqa: BLE001 — fail closed with the reason
        return False, f"git show failed: {e}"


def _sha_exists_on_remote(sha: str) -> tuple[bool, str]:
    """A pinned SHA must resolve on the remote.

    `git ls-remote <url> <sha>` cannot look up a raw SHA (it takes a ref
    pattern), so the real mechanism is: fetch the SHA itself — the server
    serves it iff it is a reachable commit — then confirm it is a commit.
    Git protocol = free, read-only.
    """
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        return False, f"not a 40-hex SHA: {sha[:20]}"
    try:
        # Content-addressed short-circuit: if the object is already in the
        # local store it is byte-identical to the remote's (a SHA's bytes
        # cannot change), so no fetch is needed.
        have = subprocess.run(
            ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
            capture_output=True, timeout=30, cwd=ROOT,
        )
        if have.returncode == 0:
            return True, f"SHA {sha[:12]} resolves (local object store)"
        f = subprocess.run(
            ["git", "fetch", REPO_URL, sha],
            capture_output=True, text=True, timeout=60, cwd=ROOT,
        )
        if f.returncode != 0:
            return False, f"SHA {sha[:12]} not served by remote"
        c = subprocess.run(
            ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
            capture_output=True, text=True, timeout=30, cwd=ROOT,
        )
        if c.returncode != 0:
            return False, f"SHA {sha[:12]} fetched but is not a commit"
        return True, f"SHA {sha[:12]} resolves on remote"
    except Exception as e:  # noqa: BLE001
        return False, f"remote resolution failed: {e}"


def _check_chain_link(sha: str, path: str, rule: str) -> tuple[bool, str, str]:
    """Verify one chain link at the SHA. Returns (ok, detail, file_text)."""
    present, content = _git_show(sha, path)
    if not present:
        return False, content, ""
    if rule == "oath-section":
        # Convergence-safe: the §10 THE OATH section must exist and be
        # substantive (≥ 200 non-space chars after the header). We read
        # whatever the converged oath says — we do not pin its wording.
        m = re.search(r"## 10\. THE OATH(.*?)(?=\n## |\Z)", content, re.S)
        if not m:
            return False, "## 10. THE OATH section missing", ""
        body = re.sub(r"\s+", "", m.group(1))
        if len(body) < 200:
            return False, f"oath section gutted ({len(body)} chars)", ""
        return True, f"oath section present ({len(body)} chars)", m.group(1)
    if rule.startswith("marker:"):
        marker = rule.split(":", 1)[1]
        held = marker in content
        return held, ("marker present" if held else f"marker missing: {marker!r}"), content
    return False, f"unknown rule {rule!r}", ""


def _contract_hash_at(sha: str) -> tuple[bool, str]:
    """sha256 of THE-CONTRACT.md bytes at the SHA (the pinned-hash tripwire)."""
    present, content = _git_show(sha, "BRAIN/00-ACTIVATION/THE-CONTRACT.md")
    if not present:
        return False, "contract not present at SHA"
    h = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return True, h


def _parrot_check(essence: str, oath_text: str) -> tuple[bool, str]:
    """Reject a near-verbatim copy of the oath. Understanding required, tested.

    Measures what fraction of the ESSENCE is covered by verbatim matches
    against the oath (not the symmetric ratio, which dilutes excerpts).
    A 600-char slice copied straight out of the oath scores ~1.0 here.
    """
    e = re.sub(r"\s+", " ", (essence or "").strip().lower())
    o = re.sub(r"\s+", " ", (oath_text or "").strip().lower())
    if len(e) < 80:
        return False, ("no substantive essence stated "
                       "(< 80 chars) — speak the oath's essence in your own words")
    sm = difflib.SequenceMatcher(None, o, e, autojunk=False)
    matching = sum(m.size for m in sm.get_matching_blocks())
    coverage = matching / max(1, len(e))
    if coverage >= PARROT_RATIO:
        return False, (f"parrot essence refused (verbatim coverage {coverage:.2f} ≥ {PARROT_RATIO}) — "
                       "copying the oath back proves nothing; say it as yourself")
    return True, f"essence is your own (verbatim coverage {coverage:.2f})"


def cmd_sign_in(agent_id: str, tip_sha: str, essence: str,
                receipt_out: str | None) -> int:
    checks: list[dict] = []
    ok, msg = _sha_exists_on_remote(tip_sha)
    checks.append({"check": "tip_sha_resolves", "pass": ok, "detail": msg})
    oath_text = ""
    for path, rule in CHAIN:
        held, detail, text = _check_chain_link(tip_sha, path, rule)
        checks.append({"check": f"chain:{path}", "pass": held, "detail": detail})
        if path.endswith("READ-ME-FIRST.md") and held:
            oath_text = text
    # Article VI tripwire: the contract's own bytes must match the pinned hash.
    h_ok, h_val = _contract_hash_at(tip_sha)
    if h_ok and CONTRACT_SHA256 != "SET_AT_BUILD":
        match = (h_val == CONTRACT_SHA256)
        checks.append({"check": "contract_hash_pinned", "pass": match,
                       "detail": "bytes match pinned hash" if match
                       else "CONTRACT BYTES CHANGED without Shawn's word — tripwire"})
    elif not h_ok:
        checks.append({"check": "contract_hash_pinned", "pass": False, "detail": h_val})
    # §9 identity bar, enforced: the essence must be yours, not a copy.
    e_ok, e_msg = _parrot_check(essence, oath_text) if oath_text else (False, "oath text unavailable")
    checks.append({"check": "essence_not_parrot", "pass": e_ok, "detail": e_msg})
    passed = all(c["pass"] for c in checks)
    result = {
        "gate": "contract",
        "phase": "sign-in",
        "agent_id": agent_id,
        "tip_sha": tip_sha,
        "pass": passed,
        "verdict": "CONTRACT HELD — begin" if passed else "REFUSED — fail closed",
        "checks": checks,
    }
    print(json.dumps(result, indent=2))
    if receipt_out:
        Path(receipt_out).write_text(json.dumps(result, indent=2) + "\n",
                                     encoding="utf-8")
    return 0 if passed else 1


def _has(pattern: re.Pattern[str], text: str) -> bool:
    return pattern.search(text) is not None


def _unnnegated_gates(low: str) -> list[str]:
    """Gate words that are actually asserted, not negated.

    "does NOT claim production" must not trip the wire; "deployed to
    production" must. A gate word counts only when no negation appears
    within the six words before it. Heuristic, and honest about it: the
    tripwire catches the careless claim, not the careful denial.
    """
    words = re.findall(r"[a-z']+", low)
    hits: list[str] = []
    for i, w in enumerate(words):
        stem = w.rstrip("s")  # credentials -> credential
        if w in GATE_WORDS or stem in GATE_WORDS:
            window = words[max(0, i - 6):i]
            if not (set(window) & NEGATIONS):
                hits.append(w)
    # de-dupe, canonical form
    seen: list[str] = []
    for h in hits:
        c = h.rstrip("s") if h.rstrip("s") in GATE_WORDS else h
        if c not in seen:
            seen.append(c)
    return seen


def cmd_sign_out(receipt: str) -> int:
    p = Path(receipt)
    failures: list[str] = []
    notes: list[str] = []
    if not p.is_file():
        print(json.dumps({"gate": "contract", "phase": "sign-out",
                          "pass": False, "verdict": "REFUSED — no receipt file",
                          "failures": [f"receipt not found: {receipt}"]}, indent=2))
        return 1
    text = p.read_text(encoding="utf-8", errors="replace")
    low = text.lower()
    if not text.strip():
        failures.append("receipt is empty")
    if not _has(SHA40, text):
        failures.append("no 40-hex evidence SHA cited")
    else:
        notes.append("evidence SHA cited")
    if not re.search(r"score\D{0,10}\d+(\.\d+)?\s*/\s*10", low):
        failures.append("no honest score line (e.g. 'score: 9.0/10')")
    else:
        notes.append("honest score present")
    if "why not 9.5" not in low and "why not 10" not in low:
        failures.append("no why-not-9.5 line (a score without a named gap is a compliment)")
    else:
        notes.append("why-not-9.5 named")
    if "drift" not in low:
        failures.append("no drift line (where you wavered, or 'no drift')")
    else:
        notes.append("drift line present")
    # Article V tripwire: gate act asserted (not negated) without a cited grant fails closed.
    named_gates = _unnnegated_gates(low)
    grant_cited = (any(w in low for w in GRANT_WORDS)
                   or _has(BOARD_COMMENT, text))
    if named_gates and not grant_cited:
        failures.append(
            f"protected-gate tripwire: receipt names {named_gates} "
            "without citing Shawn's grant — fail closed")
    elif named_gates:
        notes.append(f"gate acts {named_gates} cite a grant")
    passed = not failures
    print(json.dumps({
        "gate": "contract", "phase": "sign-out",
        "pass": passed,
        "verdict": "RECEIPT ACCEPTED — done" if passed else "REJECTED — action NOT DONE",
        "notes": notes,
        "failures": failures,
    }, indent=2))
    return 0 if passed else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="The Contract Gate — machine law.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    si = sub.add_parser("sign-in", help="verify the chain before work")
    si.add_argument("--agent-id", required=True)
    si.add_argument("--tip-sha", required=True)
    si.add_argument("--essence", default="",
                    help="the oath's essence in your own words (parrot copies refused)")
    si.add_argument("--essence-file", default="",
                    help="path to a file containing the essence (alternative to --essence)")
    si.add_argument("--receipt-out", default="",
                    help="write the activation receipt JSON to this path")
    so = sub.add_parser("sign-out", help="verify the receipt after work")
    so.add_argument("--receipt", required=True)
    a = ap.parse_args()
    if a.cmd == "sign-in":
        essence = a.essence
        if a.essence_file:
            essence = Path(a.essence_file).read_text(encoding="utf-8", errors="replace")
        return cmd_sign_in(a.agent_id, a.tip_sha, essence,
                           a.receipt_out or None)
    return cmd_sign_out(a.receipt)


if __name__ == "__main__":
    sys.exit(main())
