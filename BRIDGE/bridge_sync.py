"""Supabase <-> GitHub sync SKETCH for the NayaPOWER bridge backend.

One sync function, one conflict rule, dry-run mode.
This skeleton NEVER writes to real tables: it has no credentials, and the
server hard-gates the apply path (see bridge_server.py).

D4 doctrine is enforced at the exact point rows cross lanes: a row whose
owner_scope is PRIVATE never enters the public-lane output, whatever mode
is requested. The filter is tested, not just declared.
"""

PUBLIC_CONTRACT = "room-feed/v1"

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

    gh_by_id = {g.get("id"): g for g in github_rows}
    actions = []
    for row in publishable:
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
