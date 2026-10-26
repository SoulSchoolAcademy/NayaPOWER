#!/usr/bin/env python3
"""Smart Note number claims — the filing door's step 1 (claim before author).

Why this exists (collision guard, brief 2026-10-26): the registry already
had a correct allocator — ``tools/smart_note_v2.py:_allocate_from_registry``
(flock-serialized, occupancy-aware) — but nothing called it. Notes were
numbered by hand from the registry's ``next_sequence`` counter, which had
gone stale and pointed at an occupied number; two lanes filing minutes
apart took the same number (the SN-1863 twin filing).

This module is the allocator's first production caller. It adds NO second
allocation mechanism: the number always comes from
``_allocate_from_registry`` run over the merged occupancy view (registry
entries + live claims). What this module adds is the *claim*:

1. BEFORE any note file is written, the filing lane claims a number here.
2. The claim is anchored as a small JSON file (``claims/SN-<n>.json``) in a
   commit on the dedicated ``sn-claims`` branch. The push is the
   compare-and-swap: git rejects a non-fast-forward push, so two lanes
   racing in the same minute get a mechanical winner — the loser re-reads
   the branch, sees its candidate taken, and is renumbered by the
   allocator on the next attempt. First claim stands.
3. The registry counter (``sequence_policy.next_sequence``) is ADVISORY
   ONLY, permanently. It is repaired once to the true high-water mark by
   ``repair_counter``; no filing path may read it as the next number.
4. Fail closed: if occupancy cannot be proven (registry unreadable,
   claims branch unreadable, push rejected past the retry bound), the
   claim raises :class:`ClaimError` — never a guessed number.

Occupancy scope: registry entries (every landed note) + the claims branch
(every in-flight filing). That pair is what a racing lane can collide
with; historical commit-graph / PR-head scans remain the reconciliation
lane's forensic tool, not the filing door's hot path.

Transport note: the claim commit is built with git plumbing in a scratch
repo and pushed to the filer's remote. On surfaces where HTTPS push has
no credential helper, the same CAS semantics are available by creating
the identical commit through the Git Data API and PATCHing the branch
ref (a non-descendant update is rejected the same way).

Run:  python3 tools/sn_claims.py claim --ib IB-... --seat "Naya Resolve"
      python3 tools/sn_claims.py list
      python3 tools/sn_claims.py repair-counter
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_REL = Path(".naya") / "memory" / "smart-notes" / "index.json"
CLAIMS_BRANCH = "sn-claims"
CLAIMS_DIR = "claims"
MAX_ATTEMPTS = 5

_SN_RE = re.compile(r"SN-(\d+)", re.IGNORECASE)
_CLAIM_FILE_RE = re.compile(r"claims/SN-(\d+)\.json$")


class ClaimError(RuntimeError):
    """The claim could not be proven — filing must stop (fail closed)."""


def _load_snv2():
    sys.path.insert(0, str(ROOT / "tools"))
    import smart_note_v2  # noqa: PLC0415 — single allocator, imported once
    return smart_note_v2


# --------------------------------------------------------------------------
# Occupancy + the advisory counter (pure functions over a registry dict)

def sn_number(value) -> int | None:
    m = _SN_RE.fullmatch(str(value or "").strip().upper())
    return int(m.group(1)) if m else None


def occupied_numbers(registry: dict) -> set[int]:
    """Every number owned by a registry entry, padded or unpadded."""
    out = set()
    for e in registry.get("entries", []):
        n = sn_number(e.get("smart_note_id"))
        if n is not None:
            out.add(n)
    return out


def counter_value(registry: dict) -> int | None:
    try:
        return int(registry.get("sequence_policy", {}).get("next_sequence"))
    except (TypeError, ValueError):
        return None


def counter_is_stale(registry: dict) -> bool:
    """Stale = the counter points at or below an occupied number, i.e. a
    hand-numbering lane reading it would reissue an existing identity.
    The allocator never trusts it either way; this predicate exists so
    the door checker can WARN when the advisory display drifts."""
    occupied = occupied_numbers(registry)
    counter = counter_value(registry)
    if not occupied or counter is None:
        return False
    return counter <= max(occupied)


def repair_counter(registry: dict) -> int:
    """The one-time repair + permanent demotion, applied to the dict.

    Sets next_sequence to the true high-water mark (max occupied + 1) and
    stamps the counter's role as advisory. Idempotent. The caller commits
    the registry (ideally inside snv2.registry_transaction)."""
    occupied = occupied_numbers(registry)
    policy = registry.setdefault("sequence_policy", {"human_id_format": "SN-###"})
    repaired = (max(occupied) + 1) if occupied else max(counter_value(registry) or 1, 1)
    policy["next_sequence"] = repaired
    policy["counter_role"] = "advisory"
    policy["allocation_authority"] = (
        "tools/smart_note_v2.py:_allocate_from_registry via tools/sn_claims.py "
        "(claim-before-author, anchored on the sn-claims branch); "
        "next_sequence is display-only and must never be read as the next number"
    )
    return repaired


# --------------------------------------------------------------------------
# Claims branch reads (no checkout — ls-tree / show against a ref)

def _git(repo: Path, *args: str, input_text: str | None = None,
         env_extra: dict | None = None) -> str:
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    r = subprocess.run(["git", "-C", str(repo), *args], input=input_text,
                       capture_output=True, text=True, env=env)
    if r.returncode != 0:
        raise ClaimError(f"git {' '.join(args[:2])} failed: {r.stderr.strip()}")
    return r.stdout


def _git_ok(repo: Path, *args: str) -> str | None:
    try:
        return _git(repo, *args)
    except ClaimError:
        return None


def find_claims_ref(repo: Path, branch: str = CLAIMS_BRANCH) -> str | None:
    """The ref in `repo` that carries the claims branch, if fetched."""
    for ref in (f"refs/remotes/origin/{branch}", f"refs/heads/{branch}"):
        if _git_ok(repo, "rev-parse", "--verify", "--quiet", ref) is not None:
            return ref
    return None


def claims_at_ref(repo: Path, ref: str) -> dict[int, dict]:
    """{number: claim dict} read from the claims branch tree at `ref`."""
    out: dict[int, dict] = {}
    listing = _git_ok(repo, "ls-tree", "-r", "--name-only", ref, "--", CLAIMS_DIR)
    if listing is None:
        return out
    for line in listing.splitlines():
        m = _CLAIM_FILE_RE.search(line.strip())
        if not m:
            continue
        raw = _git(repo, "show", f"{ref}:{line.strip()}")
        try:
            out[int(m.group(1))] = json.loads(raw)
        except ValueError as exc:
            raise ClaimError(f"claim file {line.strip()} is not valid JSON: {exc}")
    return out


def read_claims(repo: Path, branch: str = CLAIMS_BRANCH) -> dict[int, dict]:
    ref = find_claims_ref(repo, branch)
    return claims_at_ref(repo, ref) if ref else {}


# --------------------------------------------------------------------------
# Allocation over the merged occupancy view — the ONE allocator

def allocate_with_claims(snv2, capture: dict, ib: str, registry: dict,
                         claims: dict[int, dict]) -> str:
    """Run snv2's allocator over registry entries + live claims.

    Claims enter the merged view as pseudo-entries so the allocator's own
    occupancy scan skips them — no second allocation logic lives here.
    A block that already holds a claim gets its claimed number back
    (idempotent, mirroring the allocator's re-capture semantics)."""
    for number, claim in claims.items():
        if claim.get("intelligent_block_id") == ib:
            return f"SN-{number:03d}"
    merged = dict(registry)
    merged["entries"] = list(registry.get("entries", [])) + [
        {"smart_note_id": f"SN-{n:03d}", "intelligent_block_id": f"CLAIM:{n}"}
        for n in sorted(claims)
    ]
    return snv2._allocate_from_registry(capture, ib, merged)


# --------------------------------------------------------------------------
# The claim — compare-and-swap on the claims branch

def _claim_blob_and_tree(scratch: Path, parent: str | None,
                         claim_path: str, claim_doc: dict) -> str:
    blob = _git(scratch, "hash-object", "-w", "--stdin",
                input_text=json.dumps(claim_doc, indent=2, ensure_ascii=False) + "\n").strip()
    fd, index_name = tempfile.mkstemp(prefix="sn-claim-index-")
    os.close(fd)
    index = Path(index_name)
    try:
        env = {"GIT_INDEX_FILE": str(index)}
        if parent:
            _git(scratch, "read-tree", parent, env_extra=env)
        else:
            _git(scratch, "read-tree", "--empty", env_extra=env)
        _git(scratch, "update-index", "--add", "--cacheinfo",
             f"100644,{blob},{claim_path}", env_extra=env)
        return _git(scratch, "write-tree", env_extra=env).strip()
    finally:
        index.unlink(missing_ok=True)


def claim_number(remote: str, *, ib: str, seat: str, registry: dict,
                 branch: str = CLAIMS_BRANCH, max_attempts: int = MAX_ATTEMPTS,
                 _pre_push_hook=None) -> dict:
    """Claim the next free Smart Note number for `ib` on behalf of `seat`.

    `remote` is the repo (path or URL) whose `branch` anchors claims.
    Returns the claim receipt: the winning claim plus, when a race forced
    a renumber, `renumbered_from` and the `winning_claim` that took the
    first candidate — the receipt names both claims, per the brief.
    Raises ClaimError (fail closed) if no attempt lands."""
    if not ib:
        raise ClaimError("claim requires an intelligent_block_id")
    if not seat:
        raise ClaimError("claim requires a claiming seat")
    snv2 = _load_snv2()
    scratch = Path(tempfile.mkdtemp(prefix="sn-claims-"))
    _git(scratch, "init", "-q", ".")
    _git(scratch, "remote", "add", "origin", str(remote))
    ident = {
        "GIT_AUTHOR_NAME": seat, "GIT_AUTHOR_EMAIL": "sn-claims@nayanet.local",
        "GIT_COMMITTER_NAME": seat, "GIT_COMMITTER_EMAIL": "sn-claims@nayanet.local",
    }
    renumbered_from: int | None = None
    winning_claim: dict | None = None
    for attempt in range(1, max_attempts + 1):
        fetched = _git_ok(scratch, "fetch", "-q", "--depth", "1", "origin",
                          f"refs/heads/{branch}")
        parent = None
        claims: dict[int, dict] = {}
        if fetched is not None:
            parent = _git(scratch, "rev-parse", "FETCH_HEAD").strip()
            claims = claims_at_ref(scratch, parent)
        sn_id = allocate_with_claims(snv2, {}, ib, registry, claims)
        number = sn_number(sn_id)
        if number is None:
            raise ClaimError(f"allocator returned an unparseable id: {sn_id!r}")
        holder = claims.get(number)
        if holder is not None:
            if holder.get("intelligent_block_id") == ib:
                # Idempotent re-claim: this block already holds the number.
                return {"claim": holder, "commit": None, "attempts": attempt,
                        "renumbered_from": renumbered_from,
                        "winning_claim": winning_claim,
                        "already_claimed": True}
            # The allocator proved the number free; a different block's
            # claim on it means the merged view was wrong — fail closed.
            raise ClaimError(f"allocator returned {sn_id}, already claimed "
                             f"by {holder.get('intelligent_block_id')} — refusing")
        claim_doc = {
            "sn": sn_id,
            "number": number,
            "intelligent_block_id": ib,
            "seat": seat,
            "claimed_at_utc": datetime.datetime.now(datetime.timezone.utc)
                                .strftime("%Y-%m-%dT%H:%M:%SZ"),
            "allocator": "tools/smart_note_v2.py:_allocate_from_registry",
            "via": "tools/sn_claims.py claim (claim-before-author)",
        }
        tree = _claim_blob_and_tree(scratch, parent, f"{CLAIMS_DIR}/SN-{number:03d}.json",
                                    claim_doc)
        commit_args = ["commit-tree", tree, "-m",
                       f"claim({sn_id}): {ib} — claimed by {seat}"]
        if parent:
            commit_args[2:2] = ["-p", parent]
        commit = _git(scratch, *commit_args, env_extra=ident).strip()
        if _pre_push_hook is not None:
            _pre_push_hook(attempt=attempt, number=number)
        push = subprocess.run(
            ["git", "-C", str(scratch), "push", "-q", "origin",
             f"{commit}:refs/heads/{branch}"],
            capture_output=True, text=True)
        if push.returncode == 0:
            return {"claim": claim_doc, "commit": commit, "attempts": attempt,
                    "renumbered_from": renumbered_from,
                    "winning_claim": winning_claim}
        # Non-fast-forward (or a create race): someone claimed first.
        # Re-read on the next attempt; if our candidate was taken, the
        # allocator renumbers us — record who holds it for the receipt.
        renumbered_from = number
        _git_ok(scratch, "fetch", "-q", "--depth", "1", "origin",
                f"refs/heads/{branch}")
        head = _git_ok(scratch, "rev-parse", "FETCH_HEAD")
        if head:
            now_claims = claims_at_ref(scratch, head.strip())
            if number in now_claims:
                winning_claim = now_claims[number]
    raise ClaimError(
        f"claim for {ib} failed after {max_attempts} attempts — every push "
        f"was rejected; filing stops rather than guessing a number")


# --------------------------------------------------------------------------
# CLI

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("claim", help="claim the next free number (step 1 of filing)")
    c.add_argument("--ib", required=True, help="intelligent_block_id being filed")
    c.add_argument("--seat", required=True, help="claiming seat name")
    c.add_argument("--repo", default=str(ROOT),
                   help="repo path or URL whose sn-claims branch anchors claims")
    c.add_argument("--registry", default=None,
                   help="registry JSON (default: <repo>/.naya/memory/smart-notes/index.json)")

    sub.add_parser("list", help="list live claims").add_argument(
        "--repo", default=str(ROOT))

    r = sub.add_parser("repair-counter",
                       help="one-time counter repair + advisory demotion")
    r.add_argument("--registry", default=str(ROOT / REGISTRY_REL))

    args = ap.parse_args(argv)
    try:
        if args.cmd == "claim":
            reg_path = Path(args.registry) if args.registry else Path(args.repo) / REGISTRY_REL
            if not reg_path.exists():
                raise ClaimError(f"registry not found at {reg_path} — cannot "
                                 f"prove occupancy; refusing to claim")
            registry = json.loads(reg_path.read_text(encoding="utf-8"))
            receipt = claim_number(args.repo, ib=args.ib, seat=args.seat,
                                   registry=registry)
            print(json.dumps(receipt, indent=2, ensure_ascii=False))
            return 0
        if args.cmd == "list":
            claims = read_claims(Path(args.repo))
            for n in sorted(claims):
                print(f"SN-{n:03d} — {claims[n].get('intelligent_block_id')} "
                      f"(seat: {claims[n].get('seat')}, {claims[n].get('claimed_at_utc')})")
            print(f"{len(claims)} live claim(s).")
            return 0
        if args.cmd == "repair-counter":
            snv2 = _load_snv2()
            with snv2.registry_transaction(args.registry) as registry:
                repaired = repair_counter(registry)
            print(f"next_sequence repaired to {repaired}; counter_role=advisory "
                  f"(allocation authority: the allocator, via sn_claims).")
            return 0
    except ClaimError as exc:
        print(f"CLAIM REFUSED: {exc}", file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
