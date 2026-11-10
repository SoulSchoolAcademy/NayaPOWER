#!/usr/bin/env python3
"""Welcome series scheduler — Smart Mail + daily send, operated by the LIVE
sync engine (nayanet-sync-engine, Cloudflare cron every minute).

What it does:
  enroll <alias> [--day1-in-minutes N]  enroll a new member: Day 0 goes out
      at once (fire_at=now, the worker fires it on the next minute tick),
      Days 1-10 follow one a day.
  tick                                   step every active enrollment whose
      next day is due: read that day's mail file FRESH, render it, and
      schedule it through sched_create. Idempotent — a day is scheduled
      once; re-running tick never doubles it.
  status                                 show enrollments + next fires.
  cancel <alias>                         stop a series (cancels any row
      still waiting to fire, then marks the enrollment cancelled).

How the words stay fresh: every mail file is read from disk at the moment
its row is created — never cached. A voice revision that lands before a
day is scheduled flows straight into that day's mail.

How a mail becomes a send: the scheduler creates a scheduled_messages row
(kind='mail', owner_alias='naya-power', recipients={"thread_aliases":[alias]},
fire_at, recur once) via the gated sched_create RPC, using a short-lived
owner session minted for this run only (token lives in memory, session row
deleted at the end of the run). The live worker claims the row on its next
minute tick and delivers it into Smart Mail (smart_mail_threads +
smart_mail_messages) — the same tables the one-off send helper writes.
No doubles by construction: the worker claims atomically (FOR UPDATE SKIP
LOCKED) and the scheduler's state ledger records every row it creates.

Bodies are sent as plain text (Smart Mail shows bodies as text): the mail
file's Markdown is rendered down — bold/heading markers stripped, links
spelled out as `text: url`. Every word is the file's word; only the
formatting is flattened and file-reference links are resolved through
welcome-series-links.json. Day 0 also gains the member's page links
(Business / Space / Dashboard) in its "Where to go from here" footer —
the standard app links, which open the signed-in member's own pages.

The service_role key comes --from-mgmt (Supabase Management API, memory
only), exactly as fire-test-sync-engine.py does. Nothing secret is printed,
logged, or stored. State lives in welcome-series-state.json beside this
script (written atomically, same directory).

Usage:
  python3 welcome-series-scheduler.py enroll <alias> [--day1-in-minutes N]
  python3 welcome-series-scheduler.py tick
  python3 welcome-series-scheduler.py status
  python3 welcome-series-scheduler.py cancel <alias>
"""
import hashlib
import json
import os
import re
import secrets as pysecrets
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")

HERE = os.path.dirname(os.path.abspath(__file__))
FILES_DIR = os.path.join(HERE, "files")
LINKS_PATH = os.path.join(HERE, "welcome-series-links.json")
STATE_PATH = os.path.join(HERE, "welcome-series-state.json")
SB_BASE = "https://dahisasgpfvziswqvmvm.supabase.co"
OWNER_ALIAS = "naya-power"
DAY1_DEFAULT_MINUTES = 24 * 60

MAIL_FILES = {
    0: "welcome-mail-00-welcome.md",
    1: "welcome-mail-01-profile-story.md",
    2: "welcome-mail-02-smart-notes.md",
    3: "welcome-mail-03-smart-feed.md",
    4: "welcome-mail-04-smart-links.md",
    5: "welcome-mail-05-smart-mail.md",
    6: "welcome-mail-06-auto-match.md",
    7: "welcome-mail-07-smart-lists.md",
    8: "welcome-mail-08-smart-box.md",
    9: "welcome-mail-09-dashboard.md",
    10: "welcome-mail-10-memberships.md",
}
PAGE_LINKS = [
    ("Your Business page", "https://nayanet.app/business"),
    ("Your Space", "https://nayanet.app/space"),
    ("Your Dashboard", "https://nayanet.app/dashboard"),
]


class SchedulerError(RuntimeError):
    pass


def utcnow():
    return datetime.now(timezone.utc)


def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


# ---------- Supabase (service key from mgmt API, memory only) ----------

def get_service_key():
    from dynamic_credentials import add_surrogate_to_request as asr
    req = urllib.request.Request(
        "https://api.supabase.com/v1/projects/dahisasgpfvziswqvmvm/api-keys",
        method="GET")
    asr(req, "custom.supabase-mgmt", allowed_hosts=["api.supabase.com"])
    with urllib.request.urlopen(req, timeout=30) as resp:
        keys = json.loads(resp.read().decode())
    for k in keys:
        if k.get("name") == "service_role" and k.get("api_key"):
            return k["api_key"]
    raise SchedulerError("service_role key not found via mgmt API")


def sb(key, method, path, body=None, query=""):
    url = SB_BASE + path + (("?" + query) if query else "")
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={"apikey": key, "Authorization": "Bearer " + key,
                 "Content-Type": "application/json",
                 "Prefer": "return=representation"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        raise SchedulerError(f"{method} {path} -> HTTP {e.code}: "
                             f"{e.read().decode()[:300]}")


def mint_session(key):
    """Short-lived owner session for this run only. Returns (token, hash)."""
    token = pysecrets.token_hex(32)
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    expires = iso(utcnow() + timedelta(hours=2))
    sb(key, "POST", "/rest/v1/member_sessions",
       {"kind": "owner", "alias": OWNER_ALIAS,
        "token_hash": token_hash, "expires_at": expires})
    return token, token_hash


def drop_session(key, token_hash):
    try:
        sb(key, "DELETE", "/rest/v1/member_sessions",
           query=f"token_hash=eq.{token_hash}")
    except SchedulerError:
        pass  # best effort; a 2h session expires on its own


# ---------- state ----------

def load_state():
    if not os.path.exists(STATE_PATH):
        return {"enrollments": {}}
    with open(STATE_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    tmp = STATE_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, sort_keys=True)
        f.write("\n")
    os.replace(tmp, STATE_PATH)


# ---------- mail files: read fresh, render to plain text ----------

def load_links():
    with open(LINKS_PATH, encoding="utf-8") as f:
        return json.load(f)


def resolve_link(filename, links):
    exact = links.get("exact", {})
    if filename in exact:
        return exact[filename]
    fb = links.get("fallbacks", {})
    if filename.startswith("welcome-sn-"):
        return fb.get("smart-note", "")
    if filename.startswith("welcome-nn-"):
        return fb.get("naya-note", "")
    if filename == "welcome-fast-action-plan.md":
        return fb.get("fast-action-plan", "")
    if filename.startswith("welcome-mail-"):
        return fb.get("next-mail", "")
    return ""


def md_to_plain(text):
    """Markdown -> plain text. Words untouched; formatting flattened;
    links spelled out as `text: url`."""
    def link_repl(m):
        label, url = m.group(1), m.group(2)
        return f"{label}: {url}" if url else label
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_repl, text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"(^|\W)\*([^\*\n]+)\*", r"\1\2", text)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.M)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = [ln.rstrip() for ln in text.split("\n")]
    # collapse doubled lead-ins: "- The Smart Note: The Smart Note: url"
    # -> "- The Smart Note: url" (the bullet already names the link)
    fixed = []
    for ln in lines:
        m = re.match(r"^(\s*-\s*)([^:]+): \2: (.*)$", ln)
        if m:
            ln = f"{m.group(1)}{m.group(2)}: {m.group(3)}"
        fixed.append(ln)
    return "\n".join(fixed).strip() + "\n"


def human_label(filename):
    """The mail files link by filename; the member reads a human label."""
    if filename.startswith("welcome-sn-"):
        return "The Smart Note"
    if filename.startswith("welcome-nn-"):
        return "The Naya Note"
    if filename == "welcome-fast-action-plan.md":
        return "Your Fast Action Plan"
    if filename.startswith("welcome-mail-"):
        return "The mail"
    return filename


def read_mail(day, links):
    """Read the day's mail file FRESH. Returns (subject, body_plain)."""
    path = os.path.join(FILES_DIR, MAIL_FILES[day])
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    subject = None
    nutshell = None
    for ln in raw.split("\n"):
        if ln.startswith("**Subject:**"):
            subject = ln[len("**Subject:**"):].strip()
        if ln.startswith("**In a nutshell:**"):
            nutshell = ln[len("**In a nutshell:**"):].strip()
    if not subject:
        raise SchedulerError(f"day {day}: no **Subject:** line in {MAIL_FILES[day]}")
    # body = everything after the first '---' rule (the letter + footer)
    parts = raw.split("\n---\n", 1)
    body_md = parts[1] if len(parts) == 2 else raw
    # resolve file-reference links through the link table
    def href_repl(m):
        label, href = m.group(1), m.group(2)
        if href.startswith("welcome-") and href.endswith(".md"):
            if label.endswith(".md"):
                label = human_label(href)
            return f"[{label}]({resolve_link(href, links)})"
        return m.group(0)
    body_md = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", href_repl, body_md)
    # Day 0: add the member's page links to "Where to go from here"
    if day == 0:
        extra = "".join(
            f"- **{label}:** {url}\n" for label, url in PAGE_LINKS)
        lines = body_md.split("\n")
        out = []
        inserted = False
        for ln in lines:
            out.append(ln)
            if not inserted and "On the site:" in ln:
                out.append(extra.rstrip("\n"))
                inserted = True
        body_md = "\n".join(out)
    body = ""
    if nutshell:
        body += f"In a nutshell: {nutshell}\n\n"
    body += md_to_plain(body_md)
    return subject, body


# ---------- scheduling ----------

def schedule_row(key, token, day, subject, body, alias, fire_at):
    row_id = sb(key, "POST", "/rest/v1/rpc/sched_create",
                {"p_token": token, "p_kind": "mail",
                 "p_subject": subject, "p_body": body,
                 "p_recipients": {"thread_aliases": [alias]},
                 "p_fire_at": iso(fire_at),
                 "p_recur": {"freq": "once"}})
    if isinstance(row_id, list):
        row_id = row_id[0] if row_id else None
    if not row_id:
        raise SchedulerError(f"day {day}: sched_create returned no id")
    return row_id


def cmd_enroll(alias, day1_minutes):
    state = load_state()
    enr = state["enrollments"].get(alias)
    if enr and enr.get("status") == "active":
        print(f"already enrolled: {alias} (next day {enr['next_day']})")
        return 0
    key = get_service_key()
    token, token_hash = mint_session(key)
    try:
        links = load_links()
        subject, body = read_mail(0, links)
        now = utcnow()
        row_id = schedule_row(key, token, 0, subject, body, alias, now)
        state["enrollments"][alias] = {
            "joined_at": iso(now),
            "next_day": 1,
            "next_fire_at": iso(now + timedelta(minutes=day1_minutes)),
            "rows": {"0": row_id},
            "status": "active",
        }
        save_state(state)
        print(f"enrolled {alias}: day 0 scheduled row={row_id} "
              f"(fires on the next worker tick); day 1 due "
              f"{iso(now + timedelta(minutes=day1_minutes))}")
        return 0
    finally:
        drop_session(key, token_hash)


def cmd_tick():
    state = load_state()
    now = utcnow()
    due = [(a, e) for a, e in state["enrollments"].items()
           if e.get("status") == "active" and e.get("next_day", 99) <= 10
           and parse_iso(e["next_fire_at"]) <= now]
    if not due:
        print("tick: nothing due")
        return 0
    key = get_service_key()
    token, token_hash = mint_session(key)
    try:
        links = load_links()
        for alias, enr in due:
            day = enr["next_day"]
            try:
                subject, body = read_mail(day, links)
                fire_at = max(parse_iso(enr["next_fire_at"]), now)
                row_id = schedule_row(key, token, day, subject, body,
                                      alias, fire_at)
            except SchedulerError as e:
                print(f"tick: {alias} day {day} FAILED: {e} "
                      f"(left for the next tick)")
                continue
            enr["rows"][str(day)] = row_id
            enr["next_day"] = day + 1
            enr["next_fire_at"] = iso(
                parse_iso(enr["next_fire_at"]) + timedelta(hours=24))
            if enr["next_day"] > 10:
                enr["status"] = "done"
            save_state(state)
            print(f"tick: {alias} day {day} scheduled row={row_id} "
                  f"fire_at={iso(fire_at)}")
        return 0
    finally:
        drop_session(key, token_hash)


def cmd_status():
    state = load_state()
    if not state["enrollments"]:
        print("no enrollments")
        return 0
    for alias, enr in sorted(state["enrollments"].items()):
        print(f"{alias}: status={enr.get('status')} "
              f"joined={enr.get('joined_at')} next_day={enr.get('next_day')} "
              f"next_fire_at={enr.get('next_fire_at')} "
              f"rows={len(enr.get('rows', {}))}")
    return 0


def cmd_cancel(alias):
    state = load_state()
    enr = state["enrollments"].get(alias)
    if not enr:
        print(f"no enrollment for {alias}")
        return 1
    if enr.get("status") != "active":
        print(f"{alias} already {enr.get('status')}")
        return 0
    key = get_service_key()
    token, token_hash = mint_session(key)
    try:
        for day, row_id in list(enr.get("rows", {}).items()):
            try:
                rows = sb(key, "GET", "/rest/v1/scheduled_messages",
                          query=f"id=eq.{row_id}&select=status")
                if rows and rows[0].get("status") == "scheduled":
                    sb(key, "POST", "/rest/v1/rpc/sched_cancel",
                       {"p_token": token, "p_id": row_id})
                    print(f"cancelled pending row day {day} {row_id}")
            except SchedulerError as e:
                print(f"cancel row day {day}: {e}")
    finally:
        drop_session(key, token_hash)
    enr["status"] = "cancelled"
    save_state(state)
    print(f"cancelled {alias}")
    return 0


def main():
    if len(sys.argv) < 2:
        print(__doc__.strip().split("\n")[0], file=sys.stderr)
        print("usage: enroll <alias> [--day1-in-minutes N] | tick | "
              "status | cancel <alias>", file=sys.stderr)
        return 2
    cmd = sys.argv[1]
    if cmd == "enroll":
        if len(sys.argv) < 3:
            print("usage: enroll <alias> [--day1-in-minutes N]",
                  file=sys.stderr)
            return 2
        minutes = DAY1_DEFAULT_MINUTES
        if "--day1-in-minutes" in sys.argv:
            i = sys.argv.index("--day1-in-minutes")
            minutes = int(sys.argv[i + 1])
        return cmd_enroll(sys.argv[2], minutes)
    if cmd == "tick":
        return cmd_tick()
    if cmd == "status":
        return cmd_status()
    if cmd == "cancel":
        if len(sys.argv) < 3:
            print("usage: cancel <alias>", file=sys.stderr)
            return 2
        return cmd_cancel(sys.argv[2])
    print(f"unknown command: {cmd}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
