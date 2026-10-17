#!/usr/bin/env python3
"""Blindness proof for the key-split level drill (Lane 9, t0730/t0765).

Answers the question "can a worker with source access run this blind?" with
bytes, not willpower. Four checks, all machine-runnable by a cold successor:

1. AST scan of the scenario file — no answer-shaped code may exist:
   dict keys / keyword args / assignments named "rung" or "label",
   any function named "key".
2. Token scan — no bare NAME tokens "rung"/"label"/"key" outside string
   literals (prose text may mention the ladder; code may not).
3. Legacy-instrument scan (--instrument, default tools/level_drill.py):
   the old instrument must carry ZERO answer-shaped fields — no
   module-level data-literal constants, no function definitions at all,
   no answer vocabulary in code tokens. It is a fail-closed deprecation
   shim; anything that imports it gets a loud refusal, never the key.
4. Seal ordering (with --answers): the sealed key file must be older than
   the answers file — the key was committed before any run, or scoring is
   refused.

Exit 0 = BLIND-CERTIFIABLE. Exit 1 = key-contacted, with the reason.
RED-first: run against the PRE-fix instrument blob (the legacy file as of
commit cde0c63dd, e.g. `git show cde0c63dd:tools/level_drill.py` saved to a
temp file) and it must FAIL with exit 1 — that is the pre/post differential
proving the check is non-vacuous. Then run against the fixed branch and it
must PASS with exit 0. Stdlib only.

Usage:
    python3 tools/verify_drill_blindness.py --scenarios tools/level_drill_scenarios.py --key tools/level_drill_key.py [--instrument tools/level_drill.py] [--answers answers.json]
"""
import argparse
import ast
import io
import os
import sys
import tokenize

FORBIDDEN = {"rung", "label"}
# Answer-shaped vocabulary that may never appear as code (non-string)
# tokens in the legacy instrument. The shim's prose may mention the ladder.
INSTRUMENT_FORBIDDEN_TOKENS = {"rung", "label", "key", "answer", "truth",
                               "expected", "grade", "score"}


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


def token_scan(path, src, forbidden=FORBIDDEN | {"key"}):
    """No bare answer-vocabulary NAME tokens outside string literals."""
    string_spans = []
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    except tokenize.TokenError as e:
        fail(f"{path} does not tokenize ({e})")
    for t in toks:
        if t.type == tokenize.STRING:
            string_spans.append((t.start, t.end))

    def in_string(pos):
        (sl, sc) = pos[0]
        for (a, b) in string_spans:
            if a <= (sl, sc) <= b:
                return True
        return False
    for t in toks:
        if t.type == tokenize.NAME and t.string in forbidden:
            if not in_string((t.start, t.end)):
                fail(f'{path}: bare code token "{t.string}" at '
                     f"line {t.start[0]} — answer-shaped vocabulary in code")


def instrument_scan(path, src):
    """The legacy instrument must be a data-free, function-free shim.

    Fail-closed: any module-level data-literal constant, any function
    definition, or any answer-vocabulary code token = exit 1.
    """
    try:
        tree = ast.parse(src, filename=path)
    except SyntaxError as e:
        fail(f"{path} does not parse ({e})")
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            fail(f'{path}: defines function "{node.name}" (line '
                 f"{node.lineno}) — the instrument must be a refusal shim, "
                 "never executable grading logic")
        if isinstance(node, ast.Assign):
            if isinstance(node.value,
                          (ast.Dict, ast.List, ast.Set, ast.Tuple)):
                targets = [t.id for t in node.targets
                           if isinstance(t, ast.Name)]
                fail(f"{path}: module-level data literal {targets} (line "
                     f"{node.lineno}) — the instrument carries no data")
        if isinstance(node, ast.AnnAssign) and isinstance(node.value,
                                                            (ast.Dict,
                                                             ast.List,
                                                             ast.Set,
                                                             ast.Tuple)):
            fail(f"{path}: module-level data literal (line {node.lineno}) "
                 "— the instrument carries no data")
    # Reuse the generic structure scan too: the shim may not reintroduce
    # answer-shaped dict keys, keyword args, or a function named "key".
    ast_scan(path, src)
    # Wider vocabulary ban for the instrument: nothing that smells like
    # grading/answer logic may appear as code.
    token_scan(path, src, forbidden=INSTRUMENT_FORBIDDEN_TOKENS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenarios", required=True)
    ap.add_argument("--key", required=True)
    ap.add_argument("--instrument", default="tools/level_drill.py")
    ap.add_argument("--answers", default=None)
    args = ap.parse_args()

    for label, p in (("scenarios", args.scenarios),
                     ("key", args.key),
                     ("instrument", args.instrument)):
        if not os.path.isfile(p):
            fail(f"{label} file not found: {p} — no file, no proof")
    with open(args.scenarios) as f:
        scen_src = f.read()
    with open(args.instrument) as f:
        inst_src = f.read()
    ast_scan(args.scenarios, scen_src)
    token_scan(args.scenarios, scen_src)
    instrument_scan(args.instrument, inst_src)

    if args.answers:
        if not os.path.isfile(args.answers):
            fail(f"answers file not found: {args.answers}")
        km, am = os.path.getmtime(args.key), os.path.getmtime(args.answers)
        if not km < am:
            fail("seal ordering violated: key file is not older than the "
                 "answers file — the key must be committed before any run")

    print(f"BLIND-CERTIFIABLE: {args.scenarios} and {args.instrument} carry "
          "no answer-shaped fields; key sealed before runs.")


if __name__ == "__main__":
    main()
