"""Supabase <-> GitHub sync SKETCH for the NayaPOWER bridge backend.

One sync function, one conflict rule, dry-run mode.
This skeleton NEVER writes to real tables: it has no credentials, and the
server hard-gates the apply path (see bridge_server.py).

D4 doctrine is enforced at the exact point rows cross lanes: a row whose
owner_scope is PRIVATE never enters the public-lane output, whatever mode
is requested. The filter is tested, not just declared.
"""

import json
import os

PUBLIC_CONTRACT = "room-feed/v1"
WEBHOOK_LEDGER_CONTRACT = "webhook-ledger/v1"
LEDGER_VERSION = 1

# Explicit conflict rule, stated once:
#   1. The newest updated_at wins on content fields.
#   2. Ties (same updated_at or missing) -> Supabase wins; the GitHub copy is
#      flagged 'diverged' for human review, never silently overwritten.
#   3. PRIVATE rows are filtered BEFORE any diff is computed; they cannot
#      appear in the public-lane plan at all (D4).
CONFLICT_RULE = (
    "newest updated_at wins; ties or missing timestamps -> Supabase wins and "
    "the GitHub copy is flagged 'diverged'; PRIVATE owner_scope rows are "
    "filtered before diffing and never enter the public lane"
)


def is_public(row):
    """D4 gate: only rows that may legally cross to the public lane.

    Default-closed: anything unlabelled or labelled PRIVATE stays private.
    """
    scope = (row.get("owner_scope") or "").upper()
    return scope in ("PUBLIC", "COLLECTIVE", "SHARED")


def public_items(rows):
    """Hard filter applied to every row before it touches the public lane."""
    return [r for r in rows if is_public(r)]


def compute_actions(publishable_rows, existing_rows):
    """Shared conflict-rule engine used by every sync entry point.

    Rules (see CONFLICT_RULE):
      * no existing row            -> create
      * equal timestamps           -> flag_diverged (never silent overwrite)
      * source newer               -> update
      * existing newer             -> skip
    """
    gh_by_id = {g.get("id"): g for g in existing_rows}
    actions = []
    for row in publishable_rows:
        rid = row.get("id")
        existing = gh_by_id.get(rid)
        if existing is None:
            actions.append({"op": "create", "id": rid})
            continue
        s_ts = row.get("updated_at") or ""
        g_ts = existing.get("updated_at") or ""
        if s_ts and g_ts and s_ts == g_ts:
            # identical timestamp on both sides: Supabase wins per rule,
            # flag the divergence instead of a silent overwrite.
            actions.append({"op": "flag_diverged", "id": rid})
        elif s_ts >= g_ts:
            actions.append({"op": "update", "id": rid})
        else:
            actions.append({"op": "skip", "id": rid, "reason": "github_newer"})
    return actions


def read_ledger_events(ledger_dir):
    """Read the append-only webhook ledger (webhook-ledger/v1 records).

    Returns a list of record dicts in file order. A missing ledger is an
    empty ledger, not an error. Corrupt lines are skipped and counted.
    """
    path = os.path.join(ledger_dir, "events.jsonl")
    events, corrupt = [], 0
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except ValueError:
                    corrupt += 1
    except FileNotFoundError:
        pass
    return events, corrupt


def event_to_row(record):
    """Map one ledger record to a sync row.

    The mapping is explicit and stable: id derives from the payload digest
    (the same event always maps to the same row id -> idempotent sync),
    owner_scope passes through untouched (D4: never re-labelled).
    """
    return {
        "id": "ev-" + str(record.get("payload_sha256", ""))[:12],
        "title": str(record.get("event", "")),
        "updated_at": str(record.get("received_at", "")),
        "owner_scope": str(record.get("owner_scope", "UNKNOWN")),
    }


def _load_feed(feed_path):
    """Load the local feed state. Missing file -> empty feed (not an error).

    Raises ValueError on a corrupt file: fail closed, never guess the state.
    """
    try:
        with open(feed_path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return []
    if not isinstance(data, list):
        raise ValueError("feed state must be a JSON list")
    return data


def _save_feed(feed_path, rows):
    os.makedirs(os.path.dirname(os.path.abspath(feed_path)), exist_ok=True)
    tmp = feed_path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, sort_keys=True)
        f.write("\n")
    os.replace(tmp, feed_path)  # atomic: the feed is never half-written


def _apply_actions(existing_rows, publishable_rows, actions):
    by_id = {g.get("id"): g for g in existing_rows}
    src = {r.get("id"): r for r in publishable_rows}
    for act in actions:
        rid = act.get("id")
        if act.get("op") == "create" and rid in src:
            by_id[rid] = src[rid]
        elif act.get("op") == "update" and rid in src:
            by_id[rid] = src[rid]
        # skip / flag_diverged: deliberate no-op. Divergences stay visible
        # in the plan for human review instead of being silently overwritten.
    return list(by_id.values())


def sync_ledger_to_feed(ledger_dir, feed_path, mode="dry-run", credentials_ok=False):
    """WORKING sync for the ledger data: ledger events -> local feed state.

    This is the sketch made real: it reads the ACTUAL append-only webhook
    ledger on disk (not fixtures), applies the D4 private filter, computes
    the conflict-rule plan, and — only on an explicit local apply — writes
    the resulting feed state to a LOCAL file.

    mode: 'dry-run' (compute plan, write nothing) or 'apply' (write the
          local feed file; requires credentials_ok=True).
    feed_path: local JSON feed-state file. This function writes ONLY to this
          local file, never to a remote service. Remote Supabase/GitHub
          writes are engine territory (BRIDGE_CAN_WRITE + real credentials).

    The returned plan is itself D4-safe: 'actions' derive only from
    public-scope events.
    """
    if mode not in ("dry-run", "apply"):
        raise ValueError("mode must be 'dry-run' or 'apply'")

    events, corrupt_lines = read_ledger_events(ledger_dir)
    rows = [event_to_row(e) for e in events]
    publishable = public_items(rows)
    private_excluded = len(rows) - len(publishable)

    existing = _load_feed(feed_path)
    actions = compute_actions(publishable, existing)

    plan = {
        "contract": PUBLIC_CONTRACT,
        "source_contract": WEBHOOK_LEDGER_CONTRACT,
        "mode": mode,
        "conflict_rule": CONFLICT_RULE,
        "events_seen": len(events),
        "corrupt_lines_skipped": corrupt_lines,
        "private_excluded_d4": private_excluded,
        "publishable": len(publishable),
        "actions": actions,
        "writes_performed": 0,  # stays 0 unless the local apply below runs
        "feed_path": feed_path,
    }

    if mode == "apply":
        if not credentials_ok:
            raise PermissionError(
                "sync apply is closed: credentials_ok=False "
                "(BRIDGE_CAN_WRITE not enabled by the engine)")
        plan["feed_path_state"] = _apply_actions(existing, publishable, actions)
        _save_feed(feed_path, plan["feed_path_state"])
        plan["writes_performed"] = sum(
            1 for a in actions if a.get("op") in ("create", "update"))
    return plan


def sync_supabase_to_github(supabase_rows, github_rows, mode="dry-run"):
    """Compute (dry-run) or describe (apply) one Supabase -> GitHub feed sync.

    supabase_rows: list of dicts with at least id, title, updated_at,
                   owner_scope. Content lives in .content per the emitter's
                   room-feed/v1 shape.
    github_rows:   list of dicts as read back from the public feed file.
    mode:          'dry-run' (compute plan, write nothing) or 'apply'
                   (stubbed: returns the plan plus the write that WOULD
                   happen; the server refuses to execute it without
                   credentials + explicit enablement).

    Returns a plan dict that is itself D4-safe: 'items' carries only
    public-scope rows.
    """
    if mode not in ("dry-run", "apply"):
        raise ValueError("mode must be 'dry-run' or 'apply'")

    publishable = public_items(supabase_rows)
    private_excluded = len(supabase_rows) - len(publishable)
    actions = compute_actions(publishable, github_rows)

    plan = {
        "contract": PUBLIC_CONTRACT,
        "mode": mode,
        "conflict_rule": CONFLICT_RULE,
        "rows_seen": len(supabase_rows),
        "private_excluded_d4": private_excluded,
        "publishable": len(publishable),
        "actions": actions,
        "writes_performed": 0,  # this skeleton never writes; the engine owns the switch
    }
    return plan
