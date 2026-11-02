#!/usr/bin/env python3
"""
Static parity checker: SQL twin (migration) vs Python source of truth.

B5 (2026-10-25). This checker is STATIC only — it parses both sources
as text/AST and asserts the shared contract surface agrees. It is NOT
an execution proof: execution equivalence between Postgres and Python
is UNPROVEN until a Postgres execution diff runs (production gate G5).

Shared contract surface asserted here:
  * function set — the 11 SQL functions (public.sm_* + public.smart_match)
    and their documented Python counterparts (SQL_TO_PYTHON below);
  * weights — topics .40 / goals .25 / offers_needs .20 / wants .15,
    extracted from both sources and compared channel by channel;
  * stopwords — the actual sets are extracted from both sources
    (Python STOPWORDS set literal; SQL sm_stopwords() array literal)
    and compared for count AND set equality (79 at the v1.5 head);
  * field set — topics / goals / offers / needs / wants, extracted from
    Python FIELDS and from the jsonb keys the SQL reads (a->'...',
    b->'...').

Python-only surface with no SQL counterpart (by design — orchestration
over the pair scorer, not pair scoring): rank_matches,
rank_matches_indexed, build_index, compute_idf. The checker asserts
those exist in Python so the documented surface cannot silently shrink.

Exit code: 0 = parity, 1 = drift (FAIL lines printed). Used by
test_sql_parity.py and runnable directly:
    python sql_parity.py [sql_file] [python_file]
"""
import ast
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
DEFAULT_PY = HERE / "smart_match.py"

EXPECTED_FIELDS = ("topics", "goals", "offers", "needs", "wants")
EXPECTED_WEIGHTS = {"topics": 0.40, "goals": 0.25,
                    "offers_needs": 0.20, "wants": 0.15}

# The documented function mapping (HARDENING-ELITE-V2-2026-10-24 §7 and
# the twin's own design). sm_stopwords maps to a constant, not a def;
# sm_sig_words is the length->3 signature-word tier inside cross_score.
SQL_TO_PYTHON = {
    "sm_stopwords": "STOPWORDS",
    "sm_terms": "_terms",
    "sm_stem": "stem",
    "sm_words": "_words",
    "sm_sig_words": "cross_score",
    "sm_terms_content": "_content_phrases",
    "sm_concepts": "concepts_of",
    "sm_coeff": "_coeff",
    "sm_family": "family_score",
    "sm_cross": "cross_score",
    "smart_match": "score",
}
PYTHON_ONLY_SURFACE = ("rank_matches", "rank_matches_indexed",
                       "build_index", "compute_idf")


def default_sql_path():
    """The B5 migration if present, else the original twin file."""
    migrations = sorted((REPO_ROOT / "supabase" / "migrations").glob(
        "*_smart_match_v1_4.sql"))
    if migrations:
        return migrations[-1]
    return REPO_ROOT / "tools" / "smart-match" / "smart_match_v1_4.sql"


# ---------------------------------------------------------------- SQL

def extract_sql(sql_text):
    functions = set(re.findall(
        r"create\s+or\s+replace\s+function\s+public\.(\w+)", sql_text, re.I))

    stopwords = set()
    m = re.search(r"function\s+public\.sm_stopwords\(\).*?array\[(.*?)\]",
                  sql_text, re.I | re.S)
    if m:
        stopwords = set(re.findall(r"'([^']*)'", m.group(1)))

    # Weighted relevance sum: first "<number>*<channel>" per channel.
    weights = {}
    for num, channel in re.findall(
            r"(\d+\.\d+)\s*\*\s*(topics|goals|offers_needs|wants)\b",
            sql_text):
        weights.setdefault(channel, float(num))

    fields = set(re.findall(r"(?:a|b)->'(\w+)'", sql_text))
    return {"functions": functions, "stopwords": stopwords,
            "weights": weights, "fields": fields}


# ------------------------------------------------------------- Python

def extract_python(py_text):
    tree = ast.parse(py_text)
    functions, assigns = set(), {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            functions.add(node.name)
        elif isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name):
            assigns[node.targets[0].id] = node.value

    stopwords = set()
    if "STOPWORDS" in assigns and isinstance(assigns["STOPWORDS"], ast.Set):
        stopwords = {e.value for e in assigns["STOPWORDS"].elts
                     if isinstance(e, ast.Constant)}

    weights = {}
    if "WEIGHTS" in assigns and isinstance(assigns["WEIGHTS"], ast.Dict):
        weights = {k.value: float(v.value)
                   for k, v in zip(assigns["WEIGHTS"].keys,
                                   assigns["WEIGHTS"].values)
                   if isinstance(k, ast.Constant)
                   and isinstance(v, ast.Constant)}

    fields = ()
    if "FIELDS" in assigns and isinstance(assigns["FIELDS"], ast.Tuple):
        fields = tuple(e.value for e in assigns["FIELDS"].elts
                       if isinstance(e, ast.Constant))

    names = functions | set(assigns)
    return {"functions": functions, "names": names, "stopwords": stopwords,
            "weights": weights, "fields": fields}


# ------------------------------------------------------------ compare

def compare(sql, py):
    """Return a list of FAIL lines; empty list means parity."""
    fails = []

    # Function set: SQL side exactly the documented 11.
    if sql["functions"] != set(SQL_TO_PYTHON):
        fails.append(
            f"FAIL functions: SQL set {sorted(sql['functions'])} != "
            f"documented set {sorted(SQL_TO_PYTHON)}")
    # Every SQL function has its documented Python counterpart present.
    for sql_fn, py_name in sorted(SQL_TO_PYTHON.items()):
        if sql_fn in sql["functions"] and py_name not in py["names"]:
            fails.append(
                f"FAIL functions: SQL {sql_fn} counterpart {py_name} "
                f"missing from Python source")
    # Documented Python-only surface still exists.
    for name in PYTHON_ONLY_SURFACE + ("score",):
        if name not in py["functions"]:
            fails.append(f"FAIL functions: Python surface {name} missing")

    # Weights: both sources equal each other AND the published values.
    if py["weights"] != EXPECTED_WEIGHTS:
        fails.append(f"FAIL weights: Python {py['weights']} != "
                     f"published {EXPECTED_WEIGHTS}")
    if sql["weights"] != EXPECTED_WEIGHTS:
        fails.append(f"FAIL weights: SQL {sql['weights']} != "
                     f"published {EXPECTED_WEIGHTS}")
    if sql["weights"] != py["weights"]:
        fails.append(f"FAIL weights: SQL {sql['weights']} != "
                     f"Python {py['weights']}")

    # Stopwords: extracted sets — count and equality, never assumed.
    if len(py["stopwords"]) != 79:
        fails.append(f"FAIL stopwords: Python count "
                     f"{len(py['stopwords'])} != 79")
    if len(sql["stopwords"]) != 79:
        fails.append(f"FAIL stopwords: SQL count "
                     f"{len(sql['stopwords'])} != 79")
    if sql["stopwords"] != py["stopwords"]:
        only_sql = sorted(sql["stopwords"] - py["stopwords"])
        only_py = sorted(py["stopwords"] - sql["stopwords"])
        fails.append(f"FAIL stopwords: sets differ; "
                     f"SQL-only={only_sql} Python-only={only_py}")

    # Fields: Python FIELDS vs the jsonb keys SQL reads.
    if tuple(py["fields"]) != EXPECTED_FIELDS:
        fails.append(f"FAIL fields: Python FIELDS {py['fields']} != "
                     f"{EXPECTED_FIELDS}")
    if sql["fields"] != set(EXPECTED_FIELDS):
        fails.append(f"FAIL fields: SQL jsonb keys "
                     f"{sorted(sql['fields'])} != "
                     f"{sorted(EXPECTED_FIELDS)}")

    return fails


def check_texts(sql_text, py_text):
    return compare(extract_sql(sql_text), extract_python(py_text))


def check_files(sql_path=None, py_path=None):
    sql_path = Path(sql_path) if sql_path else default_sql_path()
    py_path = Path(py_path) if py_path else DEFAULT_PY
    fails = check_texts(sql_path.read_text(), py_path.read_text())
    return fails, sql_path, py_path


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    sql_path = argv[0] if len(argv) > 0 else None
    py_path = argv[1] if len(argv) > 1 else None
    fails, used_sql, used_py = check_files(sql_path, py_path)
    print(f"sql_parity: SQL={used_sql}")
    print(f"sql_parity: Python={used_py}")
    if fails:
        for line in fails:
            print(line)
        print(f"FAIL: {len(fails)} parity check(s) failed")
        return 1
    print("PASS: function set, weights (.40/.25/.20/.15), stopwords "
          "(79, set-equal), fields (topics/goals/offers/needs/wants) "
          "all agree")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
