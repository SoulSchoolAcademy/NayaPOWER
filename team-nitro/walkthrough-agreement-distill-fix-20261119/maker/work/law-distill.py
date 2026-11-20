#!/usr/bin/env python3
"""DISTILL law check (2026-11-19): base-vs-new with check-design-laws.py's own
rules. Base blobs are the v5 filed blobs (welcome f2da72cc / identity
7920438e / walk 7b8fe1bf / unfold ac0d1c84), fetched via the git blob API
and checked IN MEMORY — no disk writes (EPERM flake live). The new unfold
+ new welcome come from their FILED distill blobs (argv). Identity / walk
are unchanged; checked anyway so the delta is proven, not assumed. Usage:
python3 law-distill.py <unfold_blob> <welcome_blob>"""
import base64, hashlib, importlib.util, json, subprocess, sys

REPO = "SoulSchoolAcademy/NayaPOWER"
GH = "/home/hatch/workspace/team-nitro/gh-direct.py"
CHECKER = "/home/hatch/workspace/team-nitro/check-design-laws.py"
BASES = {
    "welcome": "f2da72cc16635cf6db9f39e225ab635a3a510a81",
    "identity": "7920438ed488869f29d520fd8dcd590061cb6586",
    "walk": "7b8fe1bfbfe7d821c6e268890c682080421ff920",
    "unfold": "ac0d1c84d231334f2c49aa7b7ab723074f64db11",
}
UNFOLD_BLOB = sys.argv[1]
WELCOME_BLOB = sys.argv[2]

spec = importlib.util.spec_from_file_location("lawcheck", CHECKER)
law = importlib.util.module_from_spec(spec)
spec.loader.exec_module(law)


def gh_blob(sha):
    r = subprocess.run([sys.executable, GH, "GET",
                        "/repos/%s/git/blobs/%s" % (REPO, sha)],
                       capture_output=True, timeout=180)
    out = r.stdout.decode("utf-8", "replace")
    payload = out.split("\n", 1)[1]
    d = json.loads(payload)
    raw = base64.b64decode("".join(d["content"].split()))
    print("blob %s: %d B sha %s" % (sha[:8], len(raw), hashlib.sha256(raw).hexdigest()[:12]), flush=True)
    return raw


def check_text(text, label):
    """Faithful copy of check-design-laws.py check() body, text-instead-of-file.
    Same FAIL/WARN sets as the CLI; only the input differs."""
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
    results = {}
    for label, blob in BASES.items():
        raw = gh_blob(blob)
        results[label + '_base'] = check_text(raw.decode('utf-8', 'replace'), label + ' base')
    new_unfold = gh_blob(UNFOLD_BLOB)
    new_welcome = gh_blob(WELCOME_BLOB)
    results['unfold_new'] = check_text(new_unfold.decode('utf-8', 'replace'), 'unfold new')
    results['welcome_new'] = check_text(new_welcome.decode('utf-8', 'replace'), 'welcome new')
    for label, (fails, warns) in results.items():
        print("%s: %d FAIL / %d WARN" % (label, len(fails), len(warns)), flush=True)
        for f in fails[:10]:
            print("  FAIL " + f, flush=True)
        for w in warns[:5]:
            print("  WARN " + w, flush=True)
    # Delta: only the ADDED failures in the two changed files count.
    added = []
    for new_label, base_label in (('unfold_new', 'unfold_base'), ('welcome_new', 'welcome_base')):
        base_fails = set(results[base_label][0])
        for f in results[new_label][0]:
            key = f.split(': ', 1)[-1]
            if not any(key in b for b in base_fails):
                added.append(new_label + ': ' + f)
    print("ADDED FAILURES: %d" % len(added), flush=True)
    for a in added:
        print("  ADDED " + a, flush=True)
    print("LAW CHECK DONE: %s" % ("zero new violations" if not added else "NEW VIOLATIONS — see above"), flush=True)


if __name__ == "__main__":
    main()
