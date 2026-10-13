#!/usr/bin/env python3
"""Four-surface SN-collision coverage check (B-31).

Standing rule (AGENTS.md): the SN-collision registry must cover four
surfaces -- (1) #554 comments, (2) open Smart-Note PR heads, (3) repo
commit-graph search for SN-NNN, (4) date-partition scan. The claiming
mechanism (tools/smart_note_v2.py) historically consulted only the local
registry index.json + next_sequence, so a claim could land on any surface
without the allocator seeing it (the SN-0181 collision: a board claim
announced 12:42:55Z, seven minutes inside another seat's stale 12:41Z scan).

This check is the mechanization: given a candidate SN id it scans all four
surfaces and REFUSES (exit 1) when a *foreign* claimant already holds the
id. It fails closed: any surface that cannot be read yields exit 2
(SURFACE_ERROR), never a silent pass.

Canonical claim order (prevents self-deadlock):
    scan -> clean -> allocate -> announce
The check runs inside allocation, i.e. BEFORE the seat announces on the
board, so the seat's own announcement can never self-block. Re-capture of
an id the registry already maps to the requesting intelligent block
returns CLEAR (ownership is authoritative); foreign surface claims on an
already-owned id are reported as warnings, not refusals.

A hit is a CLAIM (refusal) when the token sits in a claim-structural
position:
  - surface 1 (board #554): ANY mention. The board is the announcement
    venue; mentions there are rare and always worth a human look.
  - surface 2 (open PR heads): token in added content of a smart-note-
    bearing path, or claim-verb + token in the PR title/body. A token in
    a generated registry mirror (B-56) is MIRROR-class (advisory,
    non-blocking) when the mirror's bytes are identical to the scan
    base's; a divergent or unverifiable mirror stays claim-class
    (fail-closed).
  - surface 3 (commit graph): token added in a diff on a smart-note-
    bearing path, token in an added smart-note-bearing file path, or
    claim-verb + token in the commit message. Pure prose mentions in a
    commit message are MENTION-class (advisory, reported, non-blocking):
    they reference an id without taking it.
  - surface 4 (date partitions): token in a note path whose front-matter
    intelligent_block_id differs from the requester, or is missing
    (fail-closed: unattributed = foreign).
A hit attributed to the requester (intelligent block id, or a
--requester-name token such as the seat name appearing in the venue
header) is SELF-class (reported, non-blocking).

SN identity is the integer, never the padding: SN-798 == SN-0798.

Usage:
    check_sn_claim_coverage.py --sn SN-0798 [--requester-name "Naya Librarian"]
    check_sn_claim_coverage.py --audit [--limit N]
    check_sn_claim_coverage.py --sn SN-0798 --fixtures fixtures.json
                                --repo /path/to/repo-root

Exit codes: 0 = CLEAR, 1 = COLLISION (refuse), 2 = SURFACE_ERROR (refuse).
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
DEFAULT_ROOT = TOOLS_DIR.parent

SN_TOKEN_RE = re.compile(r"\bSN-0*(\d+)\b")
CLAIM_VERB_RE = re.compile(
    r"\b(claim(?:s|ed|ing)?|allocat\w*|reserv\w*|stag\w*|assign\w*)\b",
    re.IGNORECASE,
)
# Paths that carry Smart-Note identity: note files and the registry itself.
SN_BEARING_RE = re.compile(
    r"(^|/)(BRAIN/05-MEMORY/SMART-NOTES/|\.naya/memory/smart-notes/)",
    re.IGNORECASE,
)
# Generated registry mirrors (B-56): the registry's own serialization. A
# token here is the registry's voice, not a claim -- UNLESS the mirror
# itself diverges from base, which is claim-worthy (fail-closed). Exact
# repo-relative paths; matched after stripping a leading "./".
MIRROR_PATHS = (
    ".naya/memory/smart-notes/index.json",
)


def is_mirror_path(path):
    """True iff `path` is a generated registry mirror."""
    return (path or "").removeprefix("./") in MIRROR_PATHS
# Front-matter IB/SN identity comes in three real formats:
#   YAML:  intelligent_block_id: IB-...
#   bold:  **Intelligent Block:** IB-...
#   table: | Intelligent Block | `IB-...` |
# (plus the IB id embedded in note filenames: IB-<id>.md)
IB_RE = re.compile(
    r"(?:intelligent_block_id\s*:|\*\*Intelligent Block:\*\*"
    r"|\|\s*Intelligent Block\s*\|)"
    r"\s*`?([A-Za-z0-9][A-Za-z0-9\-_]*)`?",
    re.IGNORECASE,
)
SN_ID_FIELD_RE = re.compile(
    r"(?:smart_note_id\s*:|\*\*Smart Note:\*\*|\|\s*Smart Note ID\s*\|)"
    r"\s*`?SN-0*(\d+)`?",
    re.IGNORECASE,
)
IB_FILENAME_RE = re.compile(r"(^|/)(IB-[A-Za-z0-9][A-Za-z0-9\-_]*)\.md$")

BOARD_ISSUE = int(os.environ.get("SN_BOARD_ISSUE", "554"))
DEFAULT_REPO_SLUG = os.environ.get(
    "GITHUB_REPOSITORY", "SoulSchoolAcademy/NayaPOWER"
)


def norm_sn(sn):
    """Canonical form: SN-<int>, padding-insensitive. Returns (num, label)."""
    m = re.fullmatch(r"\s*SN-0*(\d+)\s*", str(sn), re.IGNORECASE)
    if not m:
        raise ValueError(f"not an SN id: {sn!r}")
    num = int(m.group(1))
    return num, f"SN-{num:04d}"


def sn_num(sid):
    """Integer identity of an SN id string, or None if not an SN id."""
    try:
        return norm_sn(sid)[0]
    except (ValueError, TypeError):
        return None


def all_token_nums(text):
    """Every SN integer mentioned in text (padding-insensitive)."""
    return {int(m.group(1)) for m in SN_TOKEN_RE.finditer(text or "")}


def near_claim_verb(text, num, window=80):
    """True if a claim verb appears within `window` chars of the token."""
    for m in SN_TOKEN_RE.finditer(text or ""):
        if int(m.group(1)) != num:
            continue
        lo = max(0, m.start() - window)
        hi = m.end() + window
        if CLAIM_VERB_RE.search(text[lo:hi]):
            return True
    return False


def snippet(text, num, width=120):
    for m in SN_TOKEN_RE.finditer(text or ""):
        if int(m.group(1)) == num:
            s = max(0, m.start() - width // 2)
            return " ".join(text[s:s + width].split())
    return (text or "")[:width]


def is_self(names, *texts):
    """True if any requester token appears in the given attribution texts."""
    for t in names:
        if not t:
            continue
        tl = t.lower()
        for x in texts:
            if x and tl in x.lower():
                return True
    return False


# ---------------------------------------------------------------- API layer

def api_get(path):
    """GET a GitHub API path, returning parsed JSON.

    Prefers `gh api` (CI + local dev); SN_COVERAGE_API_BIN overrides the
    binary. Raises RuntimeError when the call fails -- the caller converts
    this into an unreadable surface (fail closed).
    """
    override = os.environ.get("SN_COVERAGE_API_BIN")
    cmd = [override, "GET", path] if override else ["gh", "api", path]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True,
                             timeout=60, check=False)
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        raise RuntimeError(f"API client failed for {path}: {e}")
    if out.returncode != 0:
        raise RuntimeError(
            f"GET {path}: exit {out.returncode}: {out.stderr.strip()[:200]}")
    try:
        return json.loads(out.stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"GET {path}: bad JSON: {e}")


def paginate(path, per_page=100):
    """Yield items across all pages of a list endpoint."""
    page = 1
    while True:
        sep = "&" if "?" in path else "?"
        items = api_get(f"{path}{sep}per_page={per_page}&page={page}")
        if not isinstance(items, list) or not items:
            return
        yield from items
        if len(items) < per_page:
            return
        page += 1


def _git(repo, *args, timeout=180):
    # Binary-safe: history contains non-UTF-8 blobs; decode with replacement
    # instead of crashing the scan (a crash here would fail the gate open
    # or closed for the wrong reason -- neither is acceptable).
    # TimeoutExpired is converted to RuntimeError so the caller fails the
    # surface closed (SURFACE_ERROR), never crashes the whole scan --
    # observed 2026-10-13: `git log --all -G` over the full history exceeds
    # 180s and killed the live --audit with an unhandled traceback.
    try:
        out = subprocess.run(
            ["git", "-C", str(repo)] + list(args),
            capture_output=True, timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError(
            f"git {' '.join(args)}: timed out after {timeout}s")
    if out.returncode != 0:
        err = out.stderr.decode("utf-8", errors="replace").strip()[:200]
        raise RuntimeError(f"git {' '.join(args)}: {err}")
    return out.stdout.decode("utf-8", errors="replace")


# ---------------------------------------------------------------- collectors
# Each collector scans its surface ONCE and returns {sn_num: [hit,...]}.

def _mirror_copies(repo, pairs):
    """Map (head_sha, path) -> True iff head's blob equals HEAD's blob.

    B-56: a registry mirror copy (byte-identical to the scan base) is the
    registry's own voice, not a claim. One batched `git cat-file
    --batch-check` resolves every pair; any unreadable side (missing head
    blob, missing base blob, short read, timeout) maps to False --
    fail-closed: a mirror we cannot verify identical is treated as a
    claim, never as a copy.
    """
    uniq = sorted({(sha, (path or "").removeprefix("./"))
                   for sha, path in pairs if sha and path})
    if not uniq:
        return {}
    revs = []
    for sha, path in uniq:
        revs.append(f"{sha}:{path}")
        revs.append(f"HEAD:{path}")
    proc = subprocess.Popen(
        ["git", "-C", str(repo), "cat-file", "--batch-check=%(objectname)"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL)
    try:
        out, _ = proc.communicate(
            "".join(r + "\n" for r in revs).encode("utf-8", "replace"),
            timeout=120)
    except subprocess.TimeoutExpired:
        proc.kill()
        raise RuntimeError("mirror blob compare: timed out")
    if proc.returncode != 0:
        raise RuntimeError(
            f"mirror blob compare: exit {proc.returncode}")
    lines = out.decode("utf-8", errors="replace").splitlines()
    if len(lines) != len(revs):
        raise RuntimeError("mirror blob compare: short read")
    result = {}
    for (sha, path), head_blob, base_blob in zip(
            uniq, lines[0::2], lines[1::2]):
        result[(sha, path)] = (
            head_blob != "missing" and head_blob == base_blob)
    return result


def collect_board(fixtures=None):
    """Surface 1: all #554 comments, tokenized by SN id."""
    if fixtures is not None and "comments" in fixtures:
        comments = fixtures["comments"]
    else:
        comments = list(
            paginate(f"/repos/{DEFAULT_REPO_SLUG}/issues/{BOARD_ISSUE}/comments"))
    by_num = {}
    for c in comments:
        body = c.get("body") or ""
        author = (c.get("user") or {}).get("login", "")
        for num in all_token_nums(body):
            by_num.setdefault(num, []).append({
                "surface": "board_comments",
                "comment_id": c.get("id"),
                "author": author,
                "created_at": c.get("created_at"),
                "text": body,
                "sig_text": f"{author}\n{body[:800]}",
            })
    return by_num


def collect_prs(fixtures=None, repo=DEFAULT_ROOT):
    """Surface 2: open PR heads, tokenized by SN id (smart-note paths only).

    Live path: one API call lists open PRs (title/body claim scan), then one
    `git fetch` pulls every open PR head and one `git grep` searches all head
    trees at once -- O(1) API round-trips instead of O(open PRs). A failed
    fetch fails the surface closed (unreadable), never silently skipped.
    """
    by_num = {}
    if fixtures is not None and "prs" in fixtures:
        prs = fixtures["prs"]
        for pr in prs:
            number = pr.get("number")
            author = (pr.get("user") or {}).get("login", "")
            title = pr.get("title") or ""
            pbody = pr.get("body") or ""
            head_ref = ((pr.get("head") or {}).get("ref")) or ""
            sig_text = f"{author}\n{title}\n{pbody}\n{head_ref}"
            seen = set()
            for num in all_token_nums(title + "\n" + pbody):
                if near_claim_verb(title + "\n" + pbody, num):
                    by_num.setdefault(num, []).append({
                        "surface": "pr_heads", "pr": number, "author": author,
                        "where": "title/body", "sig_text": sig_text,
                        "text": title + "\n" + pbody,
                    })
                    seen.add(("tb", num))
            for f in pr.get("files") or []:
                fname = f.get("filename") or ""
                patch = f.get("patch") or ""
                if not SN_BEARING_RE.search(fname):
                    continue
                # B-56: a registry mirror copy at the head is the
                # registry's voice, not a claim. In fixtures the copy is
                # declared ("mirror_copy": true); a mirror-path entry
                # WITHOUT the flag is a divergent/tampered mirror and
                # stays claim-class (fail-closed).
                mirror = is_mirror_path(fname) and bool(f.get("mirror_copy"))
                for num in all_token_nums(patch) | all_token_nums(fname):
                    key = (fname, num)
                    if key in seen:
                        continue
                    seen.add(key)
                    by_num.setdefault(num, []).append({
                        "surface": "pr_heads", "pr": number, "author": author,
                        "where": fname, "sig_text": sig_text,
                        "text": patch or fname,
                        **({"pre_class": "mirror"} if mirror else {}),
                    })
        return by_num

    prs = list(paginate(f"/repos/{DEFAULT_REPO_SLUG}/pulls?state=open"))
    for pr in prs:
        number = pr.get("number")
        author = (pr.get("user") or {}).get("login", "")
        title = pr.get("title") or ""
        pbody = pr.get("body") or ""
        head_ref = ((pr.get("head") or {}).get("ref")) or ""
        text = title + "\n" + pbody
        for num in all_token_nums(text):
            if near_claim_verb(text, num):
                by_num.setdefault(num, []).append({
                    "surface": "pr_heads", "pr": number, "author": author,
                    "where": "title/body",
                    "sig_text": f"{author}\n{title}\n{pbody}\n{head_ref}",
                    "text": text,
                })
    # Head trees: fetch once (shallow: only each head's tree is needed),
    # grep once.
    try:
        _git(repo, "fetch", "--quiet", "--no-tags", "--depth", "1",
             "--prune", "origin", "+refs/pull/*/head:refs/sncover/pr/*")
    except RuntimeError as e:
        raise RuntimeError(f"open-PR head fetch failed: {e}")
    refs_out = _git(repo, "for-each-ref",
                    "--format=%(objectname) %(refname:short)",
                    "refs/sncover/pr/")
    sha_to_pr = {}
    for line in refs_out.splitlines():
        parts = line.split(" ", 1)
        if len(parts) != 2:
            continue
        sha, ref = parts
        try:
            num = int(ref.rsplit("/", 1)[1])
        except ValueError:
            continue
        sha_to_pr[sha] = num
    if not sha_to_pr:
        return by_num
    # STREAMED, never materialized: the head-tree grep over ~2K revisions
    # can emit hundreds of MB; capture_output=True holds it all in RAM ->
    # the OOM-killer (observed exit 137 on the live audit, 2026-10-13).
    # Popen + incremental parse keeps memory flat (same pattern as the
    # commit-graph grep below).
    import time as _time
    proc = subprocess.Popen(
        ["git", "-C", str(repo), "grep", "-n", "--no-color",
         "-e", r"SN-[0-9][0-9]*"] + list(sha_to_pr)
        + ["--", "BRAIN/05-MEMORY/SMART-NOTES", ".naya/memory/smart-notes"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pr_by_number = {pr.get("number"): pr for pr in prs}
    seen = set()
    mirror_pairs = []  # (sha, path) candidates for the B-56 copy check
    mirror_hits = {}   # (sha, normpath) -> [hit dicts on mirror paths]
    _deadline = _time.monotonic() + 240
    try:
        for raw in proc.stdout:
            if _time.monotonic() > _deadline:
                proc.kill()
                raise RuntimeError("git grep PR heads: exceeded 240s budget")
            line = raw.decode("utf-8", errors="replace").rstrip("\n")
            # <sha>:<path>:<lineno>:<line>
            m = re.match(r"([0-9a-f]{40}):(.+?):(\d+):(.*)$", line)
            if not m:
                continue
            sha, path, _ln, text_line = m.groups()
            pr_number = sha_to_pr.get(sha)
            pr = pr_by_number.get(pr_number, {})
            author = (pr.get("user") or {}).get("login", "")
            head_ref = ((pr.get("head") or {}).get("ref")) or ""
            for num in all_token_nums(text_line):
                key = (sha, path, num)
                if key in seen:
                    continue
                seen.add(key)
                hit = {
                    "surface": "pr_heads", "pr": pr_number, "author": author,
                    "where": f"head tree {path}",
                    "sig_text": f"{author}\n{head_ref}",
                    "text": text_line.strip()[:300],
                }
                by_num.setdefault(num, []).append(hit)
                if is_mirror_path(path):
                    np = path.removeprefix("./")
                    mirror_pairs.append((sha, np))
                    mirror_hits.setdefault((sha, np), []).append(hit)
    finally:
        try:
            _, err = proc.communicate(timeout=60)
        except subprocess.TimeoutExpired:
            proc.kill()
            _, err = proc.communicate()
            raise RuntimeError("git grep PR heads: timed out")
        if proc.returncode not in (0, 1):
            raise RuntimeError(
                f"git grep PR heads: exit {proc.returncode}: "
                f"{err.decode('utf-8', errors='replace').strip()[:200]}")
    # B-56: verify which mirror-path hits are byte-identical copies of the
    # scan base. Verified copies are mirror-class (advisory, non-blocking);
    # divergent or unverifiable mirrors stay claim-class (fail-closed). A
    # compare failure raises -> scan_all marks the surface unreadable.
    copies = _mirror_copies(repo, mirror_pairs)
    for key, hits in mirror_hits.items():
        if copies.get(key):
            for h in hits:
                h["pre_class"] = "mirror"
    # proc.returncode == 1 means no matches: no hits.
    return by_num


def _resolve_owner_ibs(repo, attrib_keys):
    """Batched front-matter attribution for (sha, path) hits.

    A commit's author string ("Naya 4 <...>") cannot be matched against a
    registry intelligent_block_id ("IB-..."), so graph hits would always
    look foreign -- a false-positive factory (observed: 1101/1118 audit
    ids flagged on the clean tip). The note file's own front matter at
    that commit is the authoritative attribution: one `git cat-file
    --batch` resolves every unique key. `attrib_keys` is a list of
    (sha, path, hit_dict); resolved ids are written onto the hit as
    owner_ib. Missing/unreadable blobs stay unattributed (the hit falls
    back to author-string matching, i.e. foreign unless self-attributed).
    """
    uniq = {}
    for sha, path, hit in attrib_keys:
        uniq.setdefault((sha, path), []).append(hit)
    if not uniq:
        return
    proc = subprocess.Popen(
        ["git", "-C", str(repo), "cat-file", "--batch"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL)
    req = "".join(f"{sha}:{path}\n" for sha, path in uniq)
    try:
        out, _ = proc.communicate(req.encode("utf-8", errors="replace"),
                                  timeout=180)
    except subprocess.TimeoutExpired:
        proc.kill()
        raise RuntimeError("git cat-file --batch attribution: timed out")
    if proc.returncode != 0:
        raise RuntimeError(
            f"git cat-file --batch attribution: exit {proc.returncode}")
    pos, keys = 0, list(uniq)
    for sha, path in keys:
        nl = out.find(b"\n", pos)
        if nl == -1:
            break
        parts = out[pos:nl].decode("utf-8", errors="replace").split()
        pos = nl + 1
        if len(parts) == 2 and parts[1] == "missing":
            continue
        if len(parts) != 3 or parts[1] != "blob":
            continue
        try:
            size = int(parts[2])
        except ValueError:
            continue
        blob = out[pos:pos + size]
        pos += size + 1  # trailing newline after the content
        head = blob[:4000].decode("utf-8", errors="replace")
        m = IB_RE.search(head)
        m2 = SN_ID_FIELD_RE.search(head)
        if m or m2:
            for hit in uniq[(sha, path)]:
                if m:
                    hit["owner_ib"] = m.group(1)
                if m2:
                    hit["file_sn"] = int(m2.group(1))


def collect_graph(repo):
    """Surface 3: commit graph, tokenized by SN id.

    Bounded design (B-55): the full-history `git log --all -G` diff walk
    the wave-13 mechanism used never finishes on this history (>460s
    measured, 600s budget blown) -- the surface fails closed on every id,
    so the allocation gate refuses everything: safe but dead. This
    collector is path-scoped instead. Claim-class graph claims are, by
    definition (module docstring), (a) token placements on
    smart-note-bearing paths, (b) tokens in added smart-note-bearing
    file paths, or (c) claim-verbs + tokens in commit messages. All three
    are enumerable without walking every diff in history:

    1) messages: `git log --all --grep "SN-"` -- metadata walk only, no
       diffs (measured 0.17s on 13,568 commits);
    2) added note paths: `git log --all --diff-filter=A --name-status`
       limited to the two SN-bearing trees -- path-scoped, no diff
       content (measured 0.5s);
    3) content placements: `git log --all -- <paths>` enumerates every
       revision whose tree can carry a note (1,503 revisions measured);
       one batched STREAMED `git grep` reads the token lines (~4s for
       ~110MB streamed, never materialized -- the wave-13 OOM fix).

    The narrowed scope loses no claim-class detection: the old -G walk's
    breadth reached non-SN-bearing paths, but hits there were never
    claim-class under the definition above. The content set is in fact a
    superset (every revision touching the trees, not just
    diff-content-touching ones). Budgets stay fail-closed: any timeout
    raises RuntimeError inside _git, which scan_all converts to
    SURFACE_ERROR.
    """
    by_num = {}
    commits = {}  # sha -> (an, ae, subj, body)
    SN_PATHS = ("BRAIN/05-MEMORY/SMART-NOTES", ".naya/memory/smart-notes")

    # 1) message claims/mentions: metadata walk, no diffs.
    out = _git(repo, "log", "--all",
               "--format=%H%x00%an%x00%ae%x00%s%x00%b%x1e",
               "--grep", "SN-", timeout=120)
    for rec in out.split("\x1e"):
        rec = rec.strip("\n")
        if not rec.strip():
            continue
        parts = rec.split("\x00")
        if len(parts) >= 5 and parts[0] not in commits:
            commits[parts[0]] = (parts[1], parts[2], parts[3], parts[4])

    # 2) + 3) one path-scoped pass: added note paths (staging class) and
    # the full tree-revision set (content grep below). Commits appear here
    # iff they touch the SN-bearing trees -- no diff walk.
    out = _git(repo, "log", "--all",
               "--format=COMMIT %H%x00%an%x00%ae",
               "--name-status", "--", *SN_PATHS, timeout=120)
    path_shas = []   # every revision whose tree can carry a note
    added_files = {}  # sha -> [(status, path)] for adds only
    cur = None
    for line in out.splitlines():
        if line.startswith("COMMIT "):
            bits = line[7:].split("\x00")
            cur = bits[0].strip()
            if cur not in commits:
                commits[cur] = (bits[1] if len(bits) > 1 else "",
                                bits[2] if len(bits) > 2 else "", "", "")
            path_shas.append(cur)
            continue
        if cur is None or not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) >= 2 and cur in commits:
            # Renames: parts = [R100, old, new] -- the new path carries it.
            status = parts[0]
            path = parts[2] if status.startswith("R") and len(parts) >= 3 \
                else parts[1]
            if status.startswith("A"):
                added_files.setdefault(cur, []).append((status, path))

    # 4) structural hits: added SN-bearing paths + message claims.
    #
    # Attribution: hits on note files resolve owner_ib from the file's
    # front matter at that commit (_resolve_owner_ibs below). The registry
    # index.json itself is EXCLUDED from claim-class hits: its history is
    # the registry's own record (authority), not a competing claim.
    # Structural hits dedup on (path, num): one claim per placement, with
    # the first-seen sha as exemplar.
    REGISTRY_BLOB = ".naya/memory/smart-notes/index.json"
    attrib_keys = []  # (full_sha, path, hit_dict) for front-matter resolve
    seen_pn = set()

    def _note_hit(num, sha, path, where, an, ae, sig_text, text):
        if path == REGISTRY_BLOB:
            return
        key = (path, num)
        if key in seen_pn:
            return
        seen_pn.add(key)
        hit = {"surface": "commit_graph", "pre_class": "claim",
               "sha": sha[:12], "author": f"{an} <{ae}>",
               "where": where, "sig_text": sig_text, "text": text}
        # Cheap attribution first: the IB id embedded in the note filename
        # (IB-<id>.md). Front matter (authoritative) overrides below when
        # it resolves.
        mf = IB_FILENAME_RE.search(path)
        if mf:
            hit["owner_ib"] = mf.group(2)
        by_num.setdefault(num, []).append(hit)
        attrib_keys.append((sha, path, hit))

    for sha, (an, ae, subj, body) in commits.items():
        files = added_files.get(sha, [])
        msg = subj + "\n" + body
        sig_text = f"{an}\n{ae}\n{msg[:800]}"
        added_claims = set()
        for status, path in files:
            if status.startswith("A") and SN_BEARING_RE.search(path):
                for num in all_token_nums(path):
                    added_claims.add(num)
                    _note_hit(num, sha, path, f"added path {path}",
                              an, ae, sig_text, path)
        if not msg.strip():
            continue
        for num in all_token_nums(msg):
            if num in added_claims:
                continue
            if near_claim_verb(msg, num):
                klass, where = "claim", "commit message (claim verb)"
            else:
                klass, where = "mention", "commit message (prose mention)"
            by_num.setdefault(num, []).append({
                "surface": "commit_graph", "pre_class": klass,
                "sha": sha[:12], "author": f"{an} <{ae}>", "where": where,
                "sig_text": sig_text, "text": msg,
            })

    # 5) content placements: one batched grep over SN-touching revisions.
    # STREAMED, never materialized: the batched grep over the tree set
    # emits ~110MB / ~370K lines on this history. capture_output=True
    # holds it all in RAM -> the OOM-killer (observed exit 137). Popen +
    # incremental parse keeps memory flat. Hits dedup on (path, num): the
    # same claim recurring across revisions is one claim with an exemplar
    # sha, not N claims -- the verdict signal is "claimed at this path",
    # not "claimed in this many revisions".
    if path_shas:
        import time as _time
        proc = subprocess.Popen(
            ["git", "-C", str(repo), "grep", "-n", "--no-color",
             "-e", r"SN-[0-9][0-9]*"] + path_shas + ["--"] + list(SN_PATHS),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _deadline = _time.monotonic() + 240
        try:
            for raw in proc.stdout:
                if _time.monotonic() > _deadline:
                    proc.kill()
                    raise RuntimeError(
                        "git grep commit graph: exceeded 240s budget")
                line = raw.decode("utf-8", errors="replace").rstrip("\n")
                m = re.match(r"([0-9a-f]{40}):(.+?):(\d+):(.*)$", line)
                if not m:
                    continue
                sha, path, _ln, text_line = m.groups()
                an, ae = commits[sha][0], commits[sha][1]
                for num in all_token_nums(text_line):
                    _note_hit(num, sha, path, f"tree content at {path}",
                              an, ae, f"{an}\n{ae}",
                              text_line.strip()[:300])
        finally:
            try:
                _, err = proc.communicate(timeout=60)
            except subprocess.TimeoutExpired:
                proc.kill()
                _, err = proc.communicate()
                raise RuntimeError("git grep commit graph: timed out")
            if proc.returncode not in (0, 1):
                raise RuntimeError(
                    f"git grep commit graph: exit {proc.returncode}: "
                    f"{err.decode('utf-8', errors='replace').strip()[:200]}")
    # 6) front-matter attribution for every structural note-file hit.
    _resolve_owner_ibs(repo, attrib_keys)
    # 7) claim vs cross-reference: a token inside ANOTHER note's content
    # (DEPENDS_ON / SUPPORTS / REFINES edges -- the intelligence graph) is
    # a reference, not a claim. Only a file asserting its OWN id
    # (file_sn == num) or carrying the token in its path is structural.
    for _num, _hits in by_num.items():
        for _h in _hits:
            if _h["surface"] != "commit_graph" or not _h.get(
                    "where", "").startswith("tree content at "):
                continue
            _fsn = _h.get("file_sn")
            if _fsn is not None and _fsn != _num:
                _h["pre_class"] = "mention"
            elif _fsn is None and _num not in all_token_nums(_h["where"]):
                _h["pre_class"] = "mention"
    return by_num


def collect_partitions(repo):
    """Surface 4: SMART-NOTES date partitions, tokenized by SN id.

    Note files carry their owner in front-matter (intelligent_block_id).
    Directories carry no front matter: a directory is attributed to an ib
    only when every note file beneath it with an owner agrees on ONE ib;
    mixed or absent ownership stays unattributed and fails closed (foreign
    claim) -- an SN directory nobody owns is exactly the drift shape.
    """
    base = Path(repo) / "BRAIN" / "05-MEMORY" / "SMART-NOTES"
    by_num = {}
    if not base.is_dir():
        return by_num  # absent tree holds no notes: genuinely empty
    dir_owners = {}  # dir rel path -> set of contained files' owner_ibs
    for path in sorted(base.rglob("*")):
        if not path.is_file():
            continue
        try:
            head = path.read_text(encoding="utf-8", errors="replace")[:4000]
        except OSError:
            head = ""
        m = IB_RE.search(head)
        owner = m.group(1) if m else None
        m2 = SN_ID_FIELD_RE.search(head)
        owned_num = int(m2.group(1)) if m2 else None
        try:
            rel = str(path.relative_to(base))
        except ValueError:
            rel = str(path)
        if owner:
            parent = Path(rel).parent
            while str(parent) != ".":
                dir_owners.setdefault(str(parent), set()).add(owner)
                parent = parent.parent
        nums = all_token_nums(path.name) | ({owned_num} if owned_num else set())
        for num in nums:
            name_claims = num in all_token_nums(path.name)
            if not name_claims and owned_num != num:
                klass = "mention"  # file merely references the id
            else:
                klass = "claim"
            by_num.setdefault(num, []).append({
                "surface": "date_partitions", "pre_class": klass,
                "path": rel, "owner_ib": owner,
                "sig_text": owner or "", "text": rel,
            })
    for path in sorted(base.rglob("*")):
        if not path.is_dir():
            continue
        nums = all_token_nums(path.name)
        if not nums:
            continue
        try:
            rel = str(path.relative_to(base))
        except ValueError:
            rel = str(path)
        owners = dir_owners.get(rel, set())
        owner = next(iter(owners)) if len(owners) == 1 else None
        for num in nums:
            by_num.setdefault(num, []).append({
                "surface": "date_partitions", "pre_class": "claim",
                "path": rel, "owner_ib": owner,
                "sig_text": owner or "", "text": rel,
            })
    return by_num


# ---------------------------------------------------------------- verdict

def load_registry(repo):
    p = Path(repo) / ".naya" / "memory" / "smart-notes" / "index.json"
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def classify(raw_hits, names, requester_ib):
    """Split raw hits into claim/self/mention/mirror classes with attribution.

    mirror-class (B-56): a hit on a generated registry mirror that is
    byte-identical to the scan base -- the registry's own voice, advisory
    and non-blocking. Anything else on a mirror path (divergent or
    unverifiable content) arrives here as claim-class and can refuse.
    """
    claims, self_hits, mentions, mirror_hits = [], [], [], []
    for h in raw_hits:
        pre = h.get("pre_class", "claim")
        if pre in ("mention", "mirror"):
            hit = {"surface": h["surface"],
                   "class": "mirror" if pre == "mirror" else "mention",
                   "snippet": " ".join(
                       (h.get("text", "") or h.get("where", "")).split())[:200]}
            for k in ("comment_id", "pr", "sha", "path", "author",
                      "created_at", "where"):
                if h.get(k) is not None:
                    hit[k] = h[k]
            (mirror_hits if pre == "mirror" else mentions).append(hit)
            continue
        self_hit = is_self(names, h.get("sig_text", "")) or (
            requester_ib and h.get("owner_ib") == requester_ib)
        klass = "self" if self_hit else "claim"
        hit = {"surface": h["surface"], "class": klass}
        for k in ("comment_id", "pr", "sha", "path", "author",
                  "created_at", "where", "owner_ib"):
            if h.get(k) is not None:
                hit[k] = h[k]
        num = h.get("_num")
        hit["snippet"] = snippet(h.get("text", "") or h.get("where", ""),
                                 num if num else 0)[:200]
        (self_hits if self_hit else claims).append(hit)
    return claims, self_hits, mentions, mirror_hits


def scan_all(repo=DEFAULT_ROOT, fixtures=None):
    """Run all four collectors once. Returns (maps, unreadable)."""
    maps, unreadable = {}, []
    try:
        maps["board_comments"] = collect_board(fixtures)
    except RuntimeError as e:
        unreadable.append("board_comments")
        maps["board_comments"] = {"_error": str(e)}
    try:
        maps["pr_heads"] = collect_prs(fixtures, repo=repo)
    except RuntimeError as e:
        unreadable.append("pr_heads")
        maps["pr_heads"] = {"_error": str(e)}
    try:
        maps["commit_graph"] = collect_graph(repo)
    except RuntimeError as e:
        unreadable.append("commit_graph")
        maps["commit_graph"] = {"_error": str(e)}
    try:
        maps["date_partitions"] = collect_partitions(repo)
    except RuntimeError as e:
        unreadable.append("date_partitions")
        maps["date_partitions"] = {"_error": str(e)}
    return maps, unreadable


def verdict_for(num, label, maps, unreadable, requester_ib, names, owned):
    raw = []
    for surface, by_num in maps.items():
        for h in by_num.get(num, []):
            h = dict(h)
            h["_num"] = num
            raw.append(h)
    claims, self_hits, mentions, mirror_hits = classify(
        raw, names, requester_ib)
    if unreadable:
        verdict = "SURFACE_ERROR"
    elif claims and not owned:
        verdict = "COLLISION"
    else:
        verdict = "CLEAR"
    return {
        "sn": label,
        "verdict": verdict,
        "already_owned_by_requester": owned,
        "unreadable_surfaces": unreadable,
        "foreign_claims": claims if not owned else [],
        "self_hits": self_hits,
        "mentions": mentions,
        "mirror_hits": mirror_hits,
        "warnings": claims if owned else [],
        "surfaces": {k: {"status": "unreadable" if k in unreadable else "scanned",
                         "hit_count": sum(len(v) for kk, v in m.items()
                                          if kk != "_error")}
                      for k, m in maps.items()},
    }


def check_sn(sn, requester_ib=None, requester_names=(), repo=DEFAULT_ROOT,
             fixtures=None):
    """Run the four-surface scan for candidate `sn`. Returns verdict dict."""
    num, label = norm_sn(sn)
    names = [n for n in requester_names if n]
    if requester_ib:
        names = [requester_ib] + names
    registry = load_registry(repo)
    owned = False
    if registry and requester_ib:
        for e in registry.get("entries", []):
            if sn_num(e.get("smart_note_id")) == num \
                    and e.get("intelligent_block_id") == requester_ib:
                owned = True
                break
    maps, unreadable = scan_all(repo=repo, fixtures=fixtures)
    return verdict_for(num, label, maps, unreadable, requester_ib, names, owned)


def audit(repo=DEFAULT_ROOT, fixtures=None, limit=None):
    """Registry-wide four-surface audit: every known SN scanned, one pass.

    Truth conditions (must hold on a clean tip):
    - Every structural hit on an ib-bearing surface (date partitions,
      commit-graph note files) resolves by front matter to the registry
      owner ib; otherwise it is a competing claim.
    - Board mentions of a REGISTERED id are announcements, not drift:
      they are advisory here. (The allocation-time check_sn keeps the
      strict rule -- a fresh candidate with any board mention refuses.)
    - Board claim-verb mentions of a registered id by 2+ DISTINCT authors
      flag as competing claims (the SN-0181 class: two seats announcing
      the same id).
    - Any structural hit for an id ABSENT from the registry flags: a claim
      with no registry backing is the drift signal, fail closed.
    """
    registry = load_registry(repo)
    ids = []  # (num, label, owner_ib)
    if registry:
        for e in registry.get("entries", []):
            n = sn_num(e.get("smart_note_id"))
            if n is not None:
                ids.append((n, norm_sn(e["smart_note_id"])[1],
                            e.get("intelligent_block_id")))
    maps, unreadable = scan_all(repo=repo, fixtures=fixtures)
    tree_nums = set()
    for by_num in maps.values():
        tree_nums |= {k for k in by_num if isinstance(k, int)}
    reg_nums = {n for n, _, _ in ids}
    for n in sorted(tree_nums - reg_nums):
        ids.append((n, norm_sn(f"SN-{n}")[1], None))
    if limit:
        ids = ids[:limit]
    results, bad = [], []
    for n, label, ib in ids:
        known = n in reg_nums
        names = [ib] if ib else []
        if known:
            # Announcement venue: a registered id's board mention is
            # expected (its owner announced it there), not drift.
            for h in maps.get("board_comments", {}).get(n, []):
                h["pre_class"] = "mention"
        v = verdict_for(n, label, maps, unreadable, ib, names, False)
        if known and v["verdict"] == "CLEAR" and not unreadable:
            claimants = {
                h.get("author")
                for h in maps.get("board_comments", {}).get(n, [])
                if h.get("author")
                and near_claim_verb(h.get("text", ""), n)
            }
            if len(claimants) > 1:
                v["verdict"] = "COLLISION"
                v["foreign_claims"] = [{
                    "surface": "board_comments", "class": "claim",
                    "reason": "competing-claims",
                    "authors": sorted(claimants),
                    "snippet": f"{len(claimants)} distinct authors claim "
                               f"{label} on the board",
                }]
        results.append(v)
        if v["verdict"] != "CLEAR":
            bad.append({"sn": v["sn"], "verdict": v["verdict"],
                        "foreign_claims": v["foreign_claims"],
                        "unreadable_surfaces": v["unreadable_surfaces"]})
    return {"scanned": len(results), "clear": len(results) - len(bad),
            "flagged": bad}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--sn", help="candidate Smart Note id, e.g. SN-0798")
    ap.add_argument("--requester-ib", default=None,
                    help="requesting intelligent block id (ownership/self attribution)")
    ap.add_argument("--requester-name", action="append", default=[],
                    help="seat/venue name token for self attribution (repeatable)")
    ap.add_argument("--repo", default=str(DEFAULT_ROOT),
                    help="repo root for commit-graph + date-partition surfaces")
    ap.add_argument("--fixtures", default=None,
                    help="JSON file overriding board + PR surfaces "
                         '{"comments":[...],"prs":[...]} (tests/synthetic runs)')
    ap.add_argument("--audit", action="store_true",
                    help="scan every registry + tree SN across all four surfaces")
    ap.add_argument("--limit", type=int, default=None,
                    help="audit: scan at most N ids (sampling)")
    args = ap.parse_args(argv)

    fixtures = None
    if args.fixtures:
        fixtures = json.loads(Path(args.fixtures).read_text(encoding="utf-8"))

    if args.audit:
        out = audit(repo=args.repo, fixtures=fixtures, limit=args.limit)
        print(json.dumps(out, indent=2))
        return 1 if out["flagged"] else 0

    if not args.sn:
        ap.error("--sn is required (or --audit)")
    verdict = check_sn(args.sn, requester_ib=args.requester_ib,
                       requester_names=args.requester_name,
                       repo=args.repo, fixtures=fixtures)
    print(json.dumps(verdict, indent=2))
    return {"CLEAR": 0, "COLLISION": 1, "SURFACE_ERROR": 2}[verdict["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
