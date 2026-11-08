#!/usr/bin/env python3
"""test-distill-machine.py — self-test for the distill machine.

Runs distill-machine.py in DRY-RUN mode on the 10-note proof batch and
asserts the properties that the dry runs caught by hand. Every check
below is a bug this machine actually had and a human had to spot by
reading output; the test exists so the next change is caught by the
machine, not by a seat's eye.

Checks:
  1. Exit 0 (the machine ran).
  2. SN == (max SN filed today, from the git/trees API) + 1, and != 1
     (the hyphen/slash date bug filed SN-1 if it had run with --file).
  3. Title is "Every Brief Carries the Standard" (the lesson's lead,
     not a bystander).
  4. All 7 filing gates PASS, none FAIL.
  5. Dest path matches the real filed format: slashed folder
     (2026/11/08) and compact filename (IB-SMART-NOTE-20261108-...).
  6. All 9 canonical sections are non-empty in the composed note
     (the prose "Why it matters" was empty in dry run 4 while the
     gate still passed).
  7. The quote is not double-wrapped (no > ""...").
  8. The lesson JSON names the 10 source SNs and the lesson lead.

Usage: python3 test-distill-machine.py [--out-dir DIR]
Exit 0 = all checks PASS. Exit 1 = any check FAIL.
"""
import json
import os
import re
import subprocess
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
MACHINE = os.path.join(HERE, "distill-machine.py")
NOTES_DIR = os.path.expanduser("~/workspace/team-nitro/smart-notes")
PROOF = [2252, 2254, 2255, 2256, 2257, 2258, 2259, 2260, 2261, 2262]
DATE = "2026-11-08"
SECTIONS = ["Hook", "Nutshell", "Human", "Child", "Grandma", "Naya",
            "What it means", "Why it matters", "What changes now"]

fails = []


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name,
                         (" — " + detail) if detail else ""))
    if not ok:
        fails.append(name)


def max_sn_today():
    url = ("https://api.github.com/repos/SoulSchoolAcademy/NayaPOWER"
           "/git/trees/main?recursive=1")
    req = urllib.request.Request(url, headers={"User-Agent": "muse-distill-test/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        tree = json.load(resp)["tree"]
    pat = re.compile(r"SMART-NOTES/2026/11/08/[^/]+/SN-(\d+)/")
    return max(int(m.group(1)) for e in tree
               for m in [pat.search(e.get("path", ""))] if m)


def main():
    out_dir = sys.argv[sys.argv.index("--out-dir") + 1] \
        if "--out-dir" in sys.argv else "/tmp/distill-test"
    os.makedirs(out_dir, exist_ok=True)
    inputs = [os.path.join(NOTES_DIR, f)
              for f in sorted(os.listdir(NOTES_DIR))
              if re.match(r"SN-(%s)-" % "|".join(map(str, PROOF)),
                          os.path.basename(f))]
    if len(inputs) != 10:
        print("TEST SETUP FAIL: expected 10 proof inputs, found %d"
              % len(inputs))
        return 1
    proc = subprocess.run(
        [sys.executable, MACHINE, "--inputs"] + inputs +
        ["--out-dir", out_dir, "--receipt", out_dir],
        capture_output=True, text=True, timeout=300)
    print(proc.stdout)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)
    check("exit 0", proc.returncode == 0, "exit %d" % proc.returncode)

    m = re.search(r"SN number: (\d+)", proc.stdout)
    sn = int(m.group(1)) if m else -1
    expected = max_sn_today() + 1
    check("SN is max+1, not 1", sn == expected and sn != 1,
          "got %d, expected %d" % (sn, expected))

    check("title is the lesson's lead",
          "Title: Every Brief Carries the Standard" in proc.stdout)

    passes = proc.stdout.count("[PASS]")
    check("all 7 gates PASS", passes == 7 and "[FAIL]" not in proc.stdout,
          "%d PASS lines" % passes)

    lesson_path = os.path.join(out_dir, "lesson-sn%d.json" % sn)
    lesson = json.load(open(lesson_path)) if os.path.isfile(lesson_path) \
        else {}
    dest = lesson.get("dest", "")
    check("dest folder is slashed date",
          "/2026/11/08/" in dest, dest)
    check("dest filename is compact date",
          ("IB-SMART-NOTE-20261108-sn%d-" % sn) in dest, dest)

    note_path = lesson.get("local_path", "")
    text = open(note_path).read() if os.path.isfile(note_path) else ""
    for sec in SECTIONS:
        m2 = re.search(r"## " + re.escape(sec) + r"\n\n(.*?)(?=\n## |\Z)",
                       text, re.S)
        body = (m2.group(1).strip() if m2 else "")
        check("section non-empty: %s" % sec, bool(body))
    check("quote not double-wrapped", '> ""' not in text)

    check("lesson JSON names the 10 sources",
          lesson.get("sources") == PROOF, str(lesson.get("sources")))
    check("lesson lead present",
          lesson.get("lesson_lead") == "Every brief carries the standard.")

    print("---")
    if fails:
        print("TEST FAILED: %d check(s): %s" % (len(fails), ", ".join(fails)))
        return 1
    print("TEST PASSED: all checks green.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
