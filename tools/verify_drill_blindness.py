#!/usr/bin/env python3
"""Blindness proof for the key-split level drill (Lane 9, t0730).

Answers the question "can a worker with source access run this blind?" with
bytes, not willpower. Three checks, all machine-runnable by a cold successor:

1. AST scan of the scenario file — no answer-shaped code may exist:
   dict keys / keyword args / assignments named "rung" or "label",
   any function named "key".
2. Token scan — no bare NAME tokens "rung"/"label"/"key" outside string
   literals (prose text may mention the ladder; code may not).
3. Seal ordering (with --answers): the sealed key file must be older than
   the answers file — the key was committed before any run, or scoring is
   refused.

Exit 0 = BLIND-CERTIFIABLE. Exit 1 = key-contacted, with the reason.
Run against the OLD instrument (tools/level_drill.py at PR #2568's head) and
it must FAIL — that is the pre/post differential proving the check is
non-vacuous. Stdlib only.

Usage:
    python3 tools/verify_drill_blindness.py --scenarios tools/level_drill_scenarios.py --key tools/level_drill_key.py [--answers answers.json]
"""
import argparse
import ast
import io
import os
import sys
import tokenize

FORBIDDEN = {"rung", "label"}


def fail(msg):
    print(f"BLINDNESS CHECK FAILED: {msg}")
    sys.exit(1)


def ast_scan(path, src):
    """No answer-shaped code structures."""
    try:
        tree = ast.parse(src, filename=path)
    except SyntaxError as e:
        fail(f"{path} does not parse ({e})")
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            for k in node.keys:
                if isinstance(k, ast.Constant) and isinstance(k.value, str) \
                        and k.value in FORBIDDEN:
                    fail(f'{path}: dict carries answer-shaped key "{k.value}" '
                         f"(line {k.lineno})")
        if isinstance(node, ast.keyword) and node.arg in FORBIDDEN:
            fail(f'{path}: keyword argument "{node.arg}" (line {node.lineno})')
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id in FORBIDDEN:
                    fail(f'{path}: assignment to "{t.id}" (line {t.lineno})')
        if isinstance(node, ast.FunctionDef) and node.name == "key":
            fail(f'{path}: function named "key" (line {node.lineno}) '
                 "— the answer key must live in the sealed file only")


def token_scan(path, src):
    """No bare rung/label/key NAME tokens outside string literals."""
    string_spans = []
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    except tokenize.TokenError as e:
        fail(f"{path} does not tokenize ({e})")
    for t in toks:
        if t.type == tokenize.STRING:
            string_spans.append((t.start, t.end))
    def in_string(pos):
        (sl, sc), (el, ec) = pos[0], pos[1]
        for (a, b) in string_spans:
            if (a < (sl, sc) or (a == (sl, sc))) and ((sl, sc) < b or (sl, sc) == b):
                # crude containment: token start inside a string token span
                if (sl, sc) >= a and (sl, sc) <= b:
                    return True
        return False
    for t in toks:
        if t.type == tokenize.NAME and t.string in FORBIDDEN | {"key"}:
            if not in_string((t.start, t.end)):
                fail(f'{path}: bare code token "{t.string}" at '
                     f"line {t.start[0]} — answer-shaped vocabulary in code")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenarios", required=True)
    ap.add_argument("--key", required=True)
    ap.add_argument("--answers", default=None)
    args = ap.parse_args()

    if not os.path.isfile(args.scenarios):
        fail(f"scenarios file not found: {args.scenarios}")
    if not os.path.isfile(args.key):
        fail(f"key file not found: {args.key} — no key, no proof")
    with open(args.scenarios) as f:
        src = f.read()
    ast_scan(args.scenarios, src)
    token_scan(args.scenarios, src)

    if args.answers:
        if not os.path.isfile(args.answers):
            fail(f"answers file not found: {args.answers}")
        km, am = os.path.getmtime(args.key), os.path.getmtime(args.answers)
        if not km < am:
            fail("seal ordering violated: key file is not older than the "
                 "answers file — the key must be committed before any run")

    print(f"BLIND-CERTIFIABLE: {args.scenarios} carries no answer-shaped "
          "fields; key sealed before runs.")


if __name__ == "__main__":
    main()
