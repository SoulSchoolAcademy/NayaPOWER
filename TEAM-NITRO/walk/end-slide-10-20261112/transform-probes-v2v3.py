#!/usr/bin/env python3
"""Transform the v1 probe scripts into the v2/v3 re-runs (fresh aliases,
fresh profiles) — the /tmp profiles and the v1 aliases were consumed by the
previous maker's runs and the restart wiped /tmp. No logic changes except:
- bug-verify-v3: fresh aliases/profiles; leg 0 is rewritten by hand after
  this script (self-poisoned heal, see the muse.edit on the leg-0 block).
- end-probe-v2: fresh aliases; console listeners now record (url, text)
  so the checks assert zero STAGED-origin errors, and the 1440 leg gains a
  live-dashboard direct-load adjudication for the v1 1-fail (unpkg
  supabase-js MIME error on the LIVE dashboard page).
"""
import pathlib

ROUND = pathlib.Path("/home/hatch/workspace/team-nitro/walk/end-slide-10-20261112")

# ---------------- bug-verify-v3 ----------------
p = ROUND / "bug-verify-v3.py"
s = p.read_text()
reps = [
    ('OUT = "/home/hatch/workspace/team-nitro/walk-s2-box-pages-20261112/"',
     'OUT = "/home/hatch/workspace/team-nitro/walk/end-slide-10-20261112/"'),
    ('PROFILE_OLD = "/tmp/bug-profile-bugowner7"', 'PROFILE_OLD = "/tmp/bug3-profile-poison"'),
    ('PROFILE_NEW = "/tmp/bug-profile-bugowner8"', 'PROFILE_NEW = "/tmp/bug3-profile-main"'),
    ("bugowner7", "healwalk1"),
    ("bugowner8", "bugowner9"),
    ("mike7", "mike8"),
    ("bugfresh1", "bugfresh2"),
]
for a, b in reps:
    assert a in s, f"bug-verify-v3: pattern not found: {a!r}"
    s = s.replace(a, b)
p.write_text(s)
print("bug-verify-v3 transformed")

# ---------------- end-probe-v2 ----------------
p = ROUND / "end-probe-v2.py"
s = p.read_text()
reps = [
    ('OUT = "/home/hatch/workspace/team-nitro/walk-s2-box-pages-20261112/"',
     'OUT = "/home/hatch/workspace/team-nitro/walk/end-slide-10-20261112/"'),
    ("endwalk3", "endwalk5"),
    ("endwalk4", "endwalk6"),
    ("End Walk Three", "End Walk Five"),
    ("End Walk Four", "End Walk Six"),
    ('open(OUT + "end-results.json", "w")', 'open(OUT + "end-results-v2.json", "w")'),
    ('pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)',
     'pg.on("console", lambda m: errs.append((pg.url, m.text)) if m.type == "error" else None)'),
    ('p2.on("console", lambda m: errs2.append(m.text) if m.type == "error" else None)',
     'p2.on("console", lambda m: errs2.append((p2.url, m.text)) if m.type == "error" else None)'),
    ('p3.on("console", lambda m: errs3.append(m.text) if m.type == "error" else None)',
     'p3.on("console", lambda m: errs3.append((p3.url, m.text)) if m.type == "error" else None)'),
]
for a, b in reps:
    assert a in s, f"end-probe-v2: pattern not found: {a!r}"
    s = s.replace(a, b)

# 1440: adjudication after door_clicks, staged-only console check
old1440 = '''        door_clicks(pg, "endwalk5", "1440")
        check("1440 console errors", len(errs) == 0, f"{len(errs)}: {errs[:3]}")'''
new1440 = '''        door_clicks(pg, "endwalk5", "1440")
        # Live-dashboard adjudication: the Dashboard door lands on the LIVE
        # dashboard; any console error there is that page's own, not the
        # walk's. Load it directly in a fresh page: reproducing the same
        # signature proves pre-existing (out of scope); a clean direct load
        # would prove the door caused it (a real fail to investigate).
        _live = [e for (u, e) in errs if "nayanet.app" in u and "naya-walk-beginning-staging" not in u]
        _adj = br.new_context(viewport={"width": 1440, "height": 900}).new_page()
        _adj_errs = []
        _adj.on("console", lambda m: _adj_errs.append(m.text) if m.type == "error" else None)
        _adj.goto("https://nayanet.app/dashboard?name=End%20Walk%20Five&alias=endwalk5", wait_until="networkidle")
        _adj.wait_for_timeout(4000)
        check("1440 live dashboard direct load reproduces the door's live errors (pre-existing, out of scope)",
              all(any(e == d or e[:80] == d[:80] for d in _adj_errs) for e in _live),
              f"door-live={_live[:2]} direct={_adj_errs[:2]}")
        _adj.context.close()
        _staged = [e for (u, e) in errs if "naya-walk-beginning-staging" in u]
        check("1440 console errors (staged origins)", len(_staged) == 0, f"{len(_staged)}: {_staged[:3]}")
        check("1440 live-origin console errors (named boundary, see adjudication)", True, f"live={_live[:2]}")'''
assert old1440 in s, "end-probe-v2: 1440 console anchor not found"
s = s.replace(old1440, new1440)

old390 = '''        check("390 console errors", len(errs2) == 0, f"{len(errs2)}: {errs2[:3]}")'''
new390 = '''        _staged2 = [e for (u, e) in errs2 if "naya-walk-beginning-staging" in u]
        check("390 console errors (staged origins)", len(_staged2) == 0, f"{len(_staged2)}: {_staged2[:3]}")'''
assert old390 in s, "end-probe-v2: 390 console anchor not found"
s = s.replace(old390, new390)

old360 = '''    check("360 console errors", len(errs3) == 0, f"{len(errs3)}: {errs3[:3]}")'''
new360 = '''    _staged3 = [e for (u, e) in errs3 if "naya-walk-beginning-staging" in u]
    check("360 console errors (staged origins)", len(_staged3) == 0, f"{len(_staged3)}: {_staged3[:3]}")'''
assert old360 in s, "end-probe-v2: 360 console anchor not found"
s = s.replace(old360, new360)

p.write_text(s)
print("end-probe-v2 transformed")
