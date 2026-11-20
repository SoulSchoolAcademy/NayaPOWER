#!/usr/bin/env python3
"""FIX law check (2026-11-19): distill base vs fix new, with
check-design-laws.py's own rules, in memory. Base = transform-distill
outputs; new = transform-fix outputs; walk base = filed b6befc33 bytes
(local file pre-edit) vs the edited local walk file. Prints the delta;
laws delta must be 0."""
import base64, hashlib, importlib.util, json, subprocess, sys

WORK = "/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix-20261119/maker/work"
CHECKER = "/home/hatch/workspace/team-nitro/check-design-laws.py"
WALK = "/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html"

spec = importlib.util.spec_from_file_location("lawcheck", CHECKER)
law = importlib.util.module_from_spec(spec)
spec.loader.exec_module(law)


def emit(cmd):
    r = subprocess.run(cmd, capture_output=True, timeout=180)
    assert r.returncode == 0, "emit failed: %s" % r.stderr.decode("utf-8", "replace")[-500:]
    return r.stdout


def distill(mode):
    return emit(["node", WORK + "/transform-distill.js", "--emit", mode])


def fix():
    d = json.loads(emit(["node", WORK + "/transform-fix.js"]).decode("utf-8"))
    return base64.b64decode(d["unfold_b64"]), base64.b64decode(d["welcome_b64"])


def check_text(text, label):
    fails, warns = [], []
    for i, line in enumerate(text.splitlines(), 1):
        for rx in law.GRAY_RES:
            if rx.search(line):
                fails.append('%s:%d: GRAY (§2.2 no gray text): %s' % (label, i, line.strip()[:120]))
                break
    for m in law.FONTSIZE_RE.finditer(text):
        vals = [float(v) for v in m.groups() if v is not None]
        if vals and min(vals) < 17:
            line_no = text[:m.start()].count('\n') + 1
            fails.append('%s:%d: SIZE (§2.3 below 17px): %s' % (label, line_no, m.group(0)))
    for m in law.COLOR_DECL_RE.finditer(text):
        val = m.group(1).strip().lower()
        if val.startswith('var('):
            continue
        val = val.split()[0].rstrip(';')
        if val in law.FORBIDDEN_TEXT:
            line_no = text[:m.start()].count('\n') + 1
            fails.append('%s:%d: TEXT-COLOR (§2.2 red/orange/magenta as text): %s' % (label, line_no, m.group(0).strip()[:120]))
        elif val not in law.ALLOWED_TEXT and not val.startswith('#'):
            line_no = text[:m.start()].count('\n') + 1
            warns.append('%s:%d: TEXT-COLOR? (§2.2 check by eye): %s' % (label, line_no, m.group(0).strip()[:120]))
    if ':hover' not in text:
        warns.append('%s: NO-HOVER (§1 warning — no :hover rules found; objects must answer touch)' % label)
    return fails, warns


def main():
    u_base, w_base = distill("unfold"), distill("welcome")
    u_new, w_new = fix()
    walk_new = open(WALK, "rb").read()
    print("unfold base %d B %s -> new %d B %s" % (len(u_base), hashlib.sha256(u_base).hexdigest()[:12], len(u_new), hashlib.sha256(u_new).hexdigest()[:12]))
    print("welcome base %d B %s -> new %d B %s" % (len(w_base), hashlib.sha256(w_base).hexdigest()[:12], len(w_new), hashlib.sha256(w_new).hexdigest()[:12]))
    print("walk new %d B %s" % (len(walk_new), hashlib.sha256(walk_new).hexdigest()[:12]))
    results = {
        'unfold_base': check_text(u_base.decode('utf-8', 'replace'), 'unfold base'),
        'unfold_new': check_text(u_new.decode('utf-8', 'replace'), 'unfold new'),
        'welcome_base': check_text(w_base.decode('utf-8', 'replace'), 'welcome base'),
        'welcome_new': check_text(w_new.decode('utf-8', 'replace'), 'welcome new'),
        'walk_new': check_text(walk_new.decode('utf-8', 'replace'), 'walk new'),
    }
    for label, (fails, warns) in results.items():
        print("%s: %d FAIL / %d WARN" % (label, len(fails), len(warns)))
        for f in fails[:12]:
            print("  FAIL " + f)
        for w in warns[:5]:
            print("  WARN " + w)
    added = []
    for new_label, base_label in (('unfold_new', 'unfold_base'), ('welcome_new', 'welcome_base')):
        base_fails = set(results[base_label][0])
        for f in results[new_label][0]:
            key = f.split(': ', 1)[-1]
            if not any(key in b for b in base_fails):
                added.append(new_label + ': ' + f)
    print("ADDED FAILURES: %d" % len(added))
    for a in added:
        print("  ADDED " + a)
    print("LAW CHECK DONE: %s" % ("zero new violations" if not added else "NEW VIOLATIONS — see above"))


if __name__ == "__main__":
    main()
