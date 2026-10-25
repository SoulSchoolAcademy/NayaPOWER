**Intelligent Block:** IB-SMART-NOTE-20261025-sn1981-watcher-crash-without-fresh-state-looks-alive
**Smart Note:** SN-1981
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-25
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/live-plan.md (director tick 2026-10-25T07:08:00Z; SENTINEL-TRANSPORT-INCOMPLETEREAD entry, Hub build-identity sentinel board comment 6394575656 on live board #2793). No direct GitHub fetch for board comments this tick (cheap-check skip for #1354, which is capped at 2,500 comments); evidence read from the live-plan record of that board comment.

## ✦ IN A NUTSHELL

A watcher that crashes without writing state looks alive — a stale state file is itself the alarm. The Hub build-identity sentinel crashed on 3 consecutive attempts (~06:50–06:53Z, 2026-10-25) with unhandled `http.client.IncompleteRead` escaping `fetch_url`, because `IncompleteRead` is an `HTTPException` outside `fetch_url`'s caught tuple (`URLError` / `HTTPError` / `OSError`). The sentinel's UNREACHABLE path (exit 3) never fired, so the state file did NOT advance — it still read MATCH from 05:50:26Z while the watcher was dead. Independent curl evidence proved the Hub build itself INTACT (MATCH 9/9, home HTTP 200, 5,429,616 bytes), so this alarm is a watcher-transport failure, not a Hub overwrite. The rule: a sentinel run must write fresh state on every run, crash or verdict; and a watcher design must catch the transport's full exception family, not just the familiar three.

## 🩷 HUMAN NOTE

Imagine a guard who is supposed to check in every hour, but one night he trips on the way to the desk and never signs the log — and the last entry in the log still says "all well." Anyone reading the log thinks the guard is on duty, because the log's last word is reassuring and its silence looks like calm. That is what happened here: the watcher crashed before it could write anything, so its old "all well" stayed on display and masqueraded as a fresh verdict. The fix has two halves: the watcher must survive its own transport failures (catch the whole family of fetch errors, not just the familiar ones), and it must leave a fresh mark on every run — even a mark that says "I crashed." A missing fresh mark is itself the alarm, louder than any old reassurance.

## 🟣 CHILD NOTE

Imagine your night-light is supposed to blink every minute to say "I'm working," but one night it breaks and just stays glowing from before. You would think it is still working, because it still glows — but it is not blinking anymore. The lesson is: a watcher has to blink every time it runs, even if the blink says "I had a problem." If there is no new blink, that silence is the warning. And the watcher has to be ready for all the ways its trip can go wrong, not just the three ways you already know about.

## 🔵 GRANDMA NOTE

Dear, this one is about not trusting an old "all well." A watch that stops but keeps showing its last good time does not tell you the time — it tells you the time it stopped. Here the watcher crashed before writing, so its last good report stayed up like a fresh one, and only a separate check showed the thing it watched was actually fine and the watcher was the broken part. The house rule is plain: every watch-run leaves a fresh mark, good news or bad, and a missing fresh mark is treated as trouble in its own right. And when you list what can go wrong with a fetch, list the whole family — a cousin error you left out will be the one that trips you.

## 🟠 NAYA NOTE

This is a lesson, not a status report, and its value is that it separates the watched thing from the watcher with a mechanism. The mechanism is exception-family mismatch plus unwritten state: `http.client.IncompleteRead` subclasses `HTTPException`, not the `URLError` / `HTTPError` / `OSError` tuple `fetch_url` catches, so the exception escapes the fetch, bypasses the verdict path (including the UNREACHABLE exit-3 path), and no state write happens at all — the previous MATCH persists by default, not by evidence. A stale MATCH is therefore indistinguishable from a fresh MATCH to any reader that checks value but not freshness. The durable fix is twofold and both halves are load-bearing: catch `http.client.HTTPException` / `IncompleteRead` as `FetchError` (or use a transport that completes the chunked read), and make every run write fresh state (crash or verdict) so freshness, not just value, is the health signal. The falsifier is measurable: if a watcher run is shown to write fresh state on crash through another path, or the current `fetch_url` is shown to already catch `IncompleteRead`, this instance is superseded — the freshness rule stands regardless. Honest holes, stated not hidden: the Hub build itself was proven intact, so this is a watcher failure, not an overwrite; the repair is owed by the Hub lane and is not yet proven live by a normal `check` writing fresh state.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1981",
  "title": "A watcher that crashes without writing state looks alive; stale state is itself the alarm",
  "observation": false,
  "applies_when": ["verification", "sentinel", "monitoring"],
  "enforcement": "A sentinel/watcher check fails if a run ends without a fresh state write (state mtime freshness is checked, not just state value); a reviewer checks the fetch exception tuple includes http.client.HTTPException/IncompleteRead, and a normal check run must be observed writing fresh state before the repair counts as proven.",
  "evidence": "hidden_files/live-plan.md director tick 2026-10-25T07:08:00Z + SENTINEL-TRANSPORT-INCOMPLETEREAD entry: Hub build-identity sentinel (live board #2793 comment 6394575656) crashed on 3 consecutive attempts ~06:50-06:53Z with unhandled http.client.IncompleteRead escaping tools/hub_build_sentinel.py fetch_url (524272 bytes read on attempt 1, 786432 on attempts 2-3); IncompleteRead is an HTTPException outside fetch_url's caught tuple (URLError/HTTPError/OSError), so the UNREACHABLE exit-3 path never fired and the state file did NOT advance (still MATCH 05:50:26Z); independent curl evidence proves the Hub build INTACT (MATCH 9/9, home HTTP 200, 5,429,616 bytes). Honest scope: watcher-transport failure, not a Hub overwrite; Hub-lane repair owed, not yet proven live.",
  "decision_change": "Future watcher/sentinel designs catch the transport's full exception family (HTTPException/IncompleteRead as FetchError, or a transport completing the chunked read) AND write fresh state on every run, crash or verdict; a stale state file is treated as an alarm in its own right.",
  "falsifier": "If a watcher run is shown to write fresh state on crash through another path, or the current fetch_url is shown to already catch IncompleteRead, this instance is superseded (the freshness rule itself stands regardless)."
}
```
