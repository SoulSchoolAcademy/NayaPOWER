# Hub Build Sentinel — Runbook

**What it is.** `tools/hub_build_sentinel.py` is the first watcher for the
public Hub (nayanet.live). It fetches the home page and one room page over
HTTPS and verifies **build identity** — that the served pages are the true
canonical build — instead of mere liveness (HTTP 200). It observes only;
it never touches publishing or deploy machinery.

**Why it exists.** On 2026-10-22 the GitHub auto-deploy shipped the
repo's stale `HUB/app` monolith over the live Hub on PR #2961's merge.
Every deploy step reported success (the health check asserted only
HTTP 200), the site served an October-2-era shell for ~25 minutes, and
the director found it by eye. The watcher that used to re-assert the true
build had died silently days earlier. This sentinel exists so neither
half of that failure can recur silently: a wrong build alarms as
DIVERGED, and a dead sentinel alarms through its own stale state file.

## Commands

```bash
# One identity check (also writes the state file):
python3 tools/hub_build_sentinel.py check

# Offline evaluation of captured pages (incident replay, tests):
python3 tools/hub_build_sentinel.py check --home-file home.html --room-file room.html

# Liveness of the sentinel itself (for a supervisor / second watcher):
python3 tools/hub_build_sentinel.py check-state            # --max-age 600 default
```

Exit codes — `check`: **0** MATCH · **1** DIVERGED · **2** usage/config
error · **3** UNREACHABLE (fetch failed; a site that cannot be reached is
a different alarm from a site serving the wrong build).
`check-state`: **0** fresh · **1** stale/missing/unreadable state.

## Verdicts

- **MATCH** — every identity marker in `hub_build_expectations.json`
  passed on both pages. Nothing to do.
- **DIVERGED** — at least one marker failed. The output names each failed
  marker and the suspected build: the *stale repo monolith* when the
  served home page carries the snapshot block instead of the note wall, a
  *monolith-derived/hybrid* build when stale signature elements are
  present, otherwise *unknown build*. **On DIVERGED: do not redeploy
  anything yourself.** Post the sentinel output to the live board
  (#2793) as an alarm and route to the Hub lane / Nitro, who own the
  build and the two-paths reconciliation. The sentinel's job ends at a
  loud, precise alarm.
- **UNREACHABLE** — a page could not be fetched at all. Route as a site
  availability incident, not a build incident.

## The state file (liveness by construction)

Every `check` run — MATCH, DIVERGED, or UNREACHABLE — writes its verdict
and timestamp to the state file:

- default: `~/.local/state/nayapower/hub-build-sentinel.state.json`
  (i.e. `$XDG_STATE_HOME/nayapower/…` when `XDG_STATE_HOME` is set)
- override: `--state PATH` or the `HUB_SENTINEL_STATE` environment
  variable. **The scheduler wiring and the `check-state` supervisor must
  point at the same path.**

**A state file older than the max age is itself an alarm**: it means the
sentinel stopped running — the exact dead-watcher failure that let the
2026-10-22 overwrite stick. Whatever supervises the sentinel (the main
seat's cadence, a second cron, a human glancing at a dashboard) should
run `check-state` on its own interval and treat exit 1 as an incident
with the same seriousness as DIVERGED.

## Recommended wiring (main seat's step — not enabled by the sentinel PR)

- **Interval: every 5 minutes.** The 2026-10-22 overwrite lived ~25
  minutes and was found by a human; a 5-minute sentinel bounds the same
  event to ~5 minutes and finds it first.
- Command: `python3 tools/hub_build_sentinel.py check` from a checkout of
  this repo at main, with the state path pinned (`--state` or env) to the
  same path the `check-state` supervisor reads.
- On exit 1 (DIVERGED) or 3 (UNREACHABLE): post the full sentinel output
  to the live board (#2793) as the alarm receipt and notify the Hub lane.
  On exit 0: stay silent — a watcher that narrates its passes becomes
  noise the team learns to ignore.
- The supervisor's own `check-state` run should be at most 10 minutes
  behind the check cadence (default `--max-age 600` = 2 missed runs).

## Expectations file — who updates it, and when

`tools/hub_build_expectations.json` describes the TRUE build's identity:
required markers (Smart Factory room registry entry, the current design
token, the Smart Note wall counted as baked note records and as unique
note ids, the shell's size class), forbidden markers (monolith-only
wiring), the room-page identity, and the stale-signature needles used to
name a diverged build. All values in the first version were measured
against the restored build and the stale monolith on 2026-10-22.

When the canonical build legitimately changes, **the Hub lane updates the
affected markers in the same change** and notes the date in the file. A
DIVERGED alarm caused by a legitimate build change is the sentinel
working, and the cure is updating the expectations — never deleting
markers wholesale or silencing the check. The unit suite
(`tools/test_hub_build_sentinel.py`) pins the expectations' minimum
strictness so the file cannot be quietly weakened into theater.
