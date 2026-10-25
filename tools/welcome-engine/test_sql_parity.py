#!/usr/bin/env python3
"""
Parity tests: SQL twin (B5 migration) vs Python source of truth.

Static checks only — no database is touched. Drift in weights,
stopwords, fields or the function surface turns these red in CI.
Sabotage tests mutate a temp copy and require the checker to flag it,
so a checker that always passes cannot pass this suite.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import sql_parity  # noqa: E402

SQL_PATH = sql_parity.default_sql_path()
PY_PATH = sql_parity.DEFAULT_PY
SQL_TEXT = SQL_PATH.read_text()
PY_TEXT = PY_PATH.read_text()


def test_current_pair_has_parity():
    fails = sql_parity.check_texts(SQL_TEXT, PY_TEXT)
    assert fails == [], "\n".join(fails)


def test_sql_source_is_the_b5_migration():
    # The checker must be guarding the deployable migration, and the
    # migration must sort after the previous latest migration.
    assert SQL_PATH.parent.name == "migrations"
    assert SQL_PATH.name == "20261025040000_smart_match_v1_4.sql"
    assert SQL_PATH.name > "20261024194500_smart_mail_participant_" \
                           "completion_and_intake_scope_v1.sql"


def test_function_set_matches_documented_mapping():
    sql = sql_parity.extract_sql(SQL_TEXT)
    assert sql["functions"] == set(sql_parity.SQL_TO_PYTHON)
    assert len(sql["functions"]) == 11


def test_weights_extracted_equal():
    sql = sql_parity.extract_sql(SQL_TEXT)
    py = sql_parity.extract_python(PY_TEXT)
    assert py["weights"] == {"topics": 0.40, "goals": 0.25,
                             "offers_needs": 0.20, "wants": 0.15}
    assert sql["weights"] == py["weights"]


def test_stopwords_extracted_count_and_set_equal():
    sql = sql_parity.extract_sql(SQL_TEXT)
    py = sql_parity.extract_python(PY_TEXT)
    assert len(py["stopwords"]) == 79
    assert len(sql["stopwords"]) == 79
    assert sql["stopwords"] == py["stopwords"]


def test_field_set_equal():
    sql = sql_parity.extract_sql(SQL_TEXT)
    py = sql_parity.extract_python(PY_TEXT)
    assert tuple(py["fields"]) == sql_parity.EXPECTED_FIELDS
    assert sql["fields"] == set(sql_parity.EXPECTED_FIELDS)


def test_migration_body_matches_original_twin():
    # Repackaging, not a rewrite: every function body of the original
    # twin survives verbatim in the migration.
    twin = (sql_parity.REPO_ROOT / "tools" / "smart-match"
            / "smart_match_v1_4.sql").read_text()
    body = twin[twin.index("create or replace function"):]
    assert body.strip() in SQL_TEXT


def test_migration_header_names_all_four_divergences():
    header = SQL_TEXT.split("\ncreate or replace function")[0]
    assert "bare numeric" in header and "verified-value record" in header
    assert "half-away" in header and "banker's" in header
    assert "no reasons" in header
    assert "Non-array jsonb errors" in header and \
        "graceful degradation" in header
    assert "UNPROVEN" in header and "G5" in header


# ------------------------------------------------------------- sabotage

def test_sabotage_sql_weight_drift_is_flagged():
    mutated = SQL_TEXT.replace("0.40*topics", "0.45*topics", 1)
    assert mutated != SQL_TEXT
    fails = sql_parity.check_texts(mutated, PY_TEXT)
    assert any("weights" in f for f in fails), fails


def test_sabotage_python_weight_drift_is_flagged():
    mutated = PY_TEXT.replace('"topics": 0.40', '"topics": 0.41', 1)
    assert mutated != PY_TEXT
    fails = sql_parity.check_texts(SQL_TEXT, mutated)
    assert any("weights" in f for f in fails), fails


def test_sabotage_stopword_removed_is_flagged():
    mutated = SQL_TEXT.replace("'the',", "", 1)
    assert mutated != SQL_TEXT
    fails = sql_parity.check_texts(mutated, PY_TEXT)
    assert any("stopwords" in f for f in fails), fails


def test_sabotage_stopword_added_in_python_is_flagged():
    mutated = PY_TEXT.replace('"help", "want",', '"help", "zebra", "want",', 1)
    assert mutated != PY_TEXT
    fails = sql_parity.check_texts(SQL_TEXT, mutated)
    assert any("stopwords" in f for f in fails), fails


def test_sabotage_field_renamed_is_flagged():
    mutated = SQL_TEXT.replace("a->'wants'", "a->'desires'")
    assert mutated != SQL_TEXT
    fails = sql_parity.check_texts(mutated, PY_TEXT)
    assert any("fields" in f for f in fails), fails


def test_sabotage_function_dropped_is_flagged(tmp_path):
    mutated = SQL_TEXT.replace(
        "create or replace function public.sm_coeff",
        "create or replace function public.sm_coeff_dropped", 1)
    assert mutated != SQL_TEXT
    fails = sql_parity.check_texts(mutated, PY_TEXT)
    assert any("functions" in f for f in fails), fails
