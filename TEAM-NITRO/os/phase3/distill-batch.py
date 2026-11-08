#!/usr/bin/env python3
"""distill-batch.py — batch mode for the distill machine.

A day's raw notes are more than 10. This wrapper chunks them into
groups of 10 (in SN order) and runs distill-machine.py once per group,
sequentially — so each group files before the next group's SN is
computed (the SN is max+1 at its turn, never hardcoded).

Usage:
  python3 distill-batch.py --inputs NOTE1.md NOTE2.md ... [NOTE30.md]
      [--out-dir DIR] [--receipt DIR] [--date YYYY-MM-DD] [--file]
  python3 distill-batch.py --dir ~/workspace/team-nitro/smart-notes
      [--pattern 'SN-22*.md'] [--out-dir DIR] [--receipt DIR] [--file]
  --file: file each distilled note (else dry-run only).
  In dry-run mode each group writes to its own out-dir (g1, g2, ...)
  because the SN repeats when nothing is filed; in --file mode the
  SN increments per group, so groups share the out-dir.
  The last group may be partial (< 10 notes) — it still distills;
  the 10:1 ratio holds per full group.
Exit 0 = every group distilled (+ filed and verified if --file).
Exit 1 = any group failed.
"""
import argparse
import glob
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MACHINE = os.path.join(HERE, "distill-machine.py")
GROUP = 10


def sn_of(path):
    m = re.search(r"SN-(\d+)-", os.path.basename(path))
    return int(m.group(1)) if m else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", nargs="+", default=None)
    parser.add_argument("--dir", default=None,
                        help="Directory of note .md files")
    parser.add_argument("--pattern", default="SN-*.md")
    parser.add_argument("--out-dir", default="/tmp/distill-batch")
    parser.add_argument("--receipt", default=None)
    parser.add_argument("--date", default=None)
    parser.add_argument("--file", action="store_true")
    args = parser.parse_args()

    if args.inputs:
        inputs = sorted(args.inputs, key=sn_of)
    elif args.dir:
        inputs = sorted(
            glob.glob(os.path.join(os.path.expanduser(args.dir),
                                   args.pattern)), key=sn_of)
    else:
        print("BATCH: need --inputs or --dir", file=sys.stderr)
        return 1
    if not inputs:
        print("BATCH: no input notes found", file=sys.stderr)
        return 1

    receipt_dir = os.path.expanduser(args.receipt) if args.receipt else HERE
    os.makedirs(receipt_dir, exist_ok=True)
    groups = [inputs[i:i + GROUP] for i in range(0, len(inputs), GROUP)]
    print("BATCH: %d notes in %d group(s) of up to %d"
          % (len(inputs), len(groups), GROUP))
    failed = []
    for gi, group in enumerate(groups, 1):
        if args.file:
            out_dir = os.path.expanduser(args.out_dir)
        else:
            out_dir = os.path.join(os.path.expanduser(args.out_dir),
                                   "g%d" % gi)
        os.makedirs(out_dir, exist_ok=True)
        lesson_out = os.path.join(receipt_dir,
                                  "lesson-batch-g%d.json" % gi)
        cmd = [sys.executable, MACHINE, "--inputs"] + group + \
            ["--out-dir", out_dir, "--receipt", receipt_dir,
             "--lesson-out", lesson_out]
        if args.date:
            cmd += ["--date", args.date]
        if args.file:
            cmd.append("--file")
        print("--- group %d/%d: SN %s..%s (%d notes) ---"
              % (gi, len(groups), sn_of(group[0]), sn_of(group[-1]),
                 len(group)))
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              timeout=600)
        print(proc.stdout)
        if proc.stderr:
            print(proc.stderr, file=sys.stderr)
        if proc.returncode != 0:
            failed.append(gi)
            print("BATCH: group %d FAILED (exit %d) — stopping"
                  % (gi, proc.returncode))
            break
    if failed:
        print("BATCH FAILED: group(s) %s" % failed)
        return 1
    print("BATCH DONE: %d group(s), %d notes distilled."
          % (len(groups), len(inputs)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
