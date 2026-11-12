"""Tests for tools/safety_anon_grant_gate.py.

The gate is fail-closed: anonymous-surface grants without an allowlist
entry fail the build, and anything the gate cannot evaluate fails closed
too (missing dir, missing/invalid allowlist, unparseable GRANT).
"""

import json

import pytest

from tools import safety_anon_grant_gate as gate


def _write(tmp_path, name, content):
    p = tmp_path / name
    p.write_text(content)
    return p


def _allowlist(tmp_path, entries):
    p = tmp_path / "allowlist.json"
    p.write_text(json.dumps({"version": "TEST", "grants": entries}))
    return p


def _migrations(tmp_path, files):
    d = tmp_path / "migrations"
    d.mkdir()
    for name, content in files.items():
        _write(d, name, content)
    return d


def _entry(obj="table:public.t", privs=("select",), grantees=("anon",)):
    return {"object": obj, "privileges": list(privs),
            "grantees": list(grantees), "justification": "test",
            "migration": "test.sql"}


def test_anon_execute_without_allowlist_fails(tmp_path):
    mig = _migrations(tmp_path, {"a.sql": "GRANT EXECUTE ON FUNCTION public.f(uuid) TO anon;"})
    al = _allowlist(tmp_path, [])
    violations, errors = gate.check(mig, al)
    assert not errors
    assert len(violations) == 1
    assert "anon" in violations[0]


def test_allowlisted_grant_passes(tmp_path):
    mig = _migrations(tmp_path, {"a.sql":
        "GRANT SELECT ON TABLE public.nayanet_intelligence_publications TO anon, authenticated;"})
    al = _allowlist(tmp_path, [_entry("table:public.nayanet_intelligence_publications")])
    violations, errors = gate.check(mig, al)
    assert errors == []
    assert violations == []


def test_revoke_is_always_fine(tmp_path):
    mig = _migrations(tmp_path, {"a.sql":
        "REVOKE EXECUTE ON FUNCTION public.f(uuid) FROM anon, authenticated;"})
    al = _allowlist(tmp_path, [])
    violations, errors = gate.check(mig, al)
    assert errors == []
    assert violations == []


def test_authenticated_only_grant_passes(tmp_path):
    mig = _migrations(tmp_path, {"a.sql":
        "GRANT EXECUTE ON FUNCTION public.f(uuid) TO authenticated;"})
    al = _allowlist(tmp_path, [])
    violations, errors = gate.check(mig, al)
    assert errors == []
    assert violations == []


def test_public_role_is_watched(tmp_path):
    mig = _migrations(tmp_path, {"a.sql": "grant execute on function public.f() to PUBLIC;"})
    al = _allowlist(tmp_path, [])
    violations, errors = gate.check(mig, al)
    assert not errors
    assert len(violations) == 1


def test_privilege_exceeding_allowlist_fails(tmp_path):
    mig = _migrations(tmp_path, {"a.sql":
        "GRANT SELECT, INSERT ON TABLE public.t TO anon;"})
    al = _allowlist(tmp_path, [_entry("table:public.t", privs=("select",))])
    violations, errors = gate.check(mig, al)
    assert not errors
    assert any("exceed" in v for v in violations)


def test_broad_grant_fails_closed(tmp_path):
    mig = _migrations(tmp_path, {"a.sql":
        "GRANT SELECT ON ALL TABLES IN SCHEMA public TO anon;"})
    al = _allowlist(tmp_path, [_entry("table:public.t")])
    violations, errors = gate.check(mig, al)
    assert not errors
    assert any("broad grant" in v for v in violations)


def test_comment_grant_is_ignored(tmp_path):
    mig = _migrations(tmp_path, {"a.sql":
        "-- GRANT EXECUTE ON FUNCTION public.f() TO anon; (historical note)\nSELECT 1;"})
    al = _allowlist(tmp_path, [])
    violations, errors = gate.check(mig, al)
    assert errors == []
    assert violations == []


def test_missing_migrations_dir_fails_closed(tmp_path):
    al = _allowlist(tmp_path, [])
    violations, errors = gate.check(tmp_path / "nope", al)
    assert errors != []


def test_missing_allowlist_fails_closed(tmp_path):
    mig = _migrations(tmp_path, {"a.sql": "SELECT 1;"})
    violations, errors = gate.check(mig, tmp_path / "no-allowlist.json")
    assert errors != []


def test_invalid_allowlist_fails_closed(tmp_path):
    mig = _migrations(tmp_path, {"a.sql": "SELECT 1;"})
    bad = _write(tmp_path, "bad.json", "{not json")
    violations, errors = gate.check(mig, bad)
    assert errors != []


def test_grantee_case_insensitive(tmp_path):
    mig = _migrations(tmp_path, {"a.sql": "Grant Select On Table public.T To ANON;"})
    al = _allowlist(tmp_path, [_entry("table:public.t")])
    violations, errors = gate.check(mig, al)
    assert errors == []
    assert violations == []


def test_main_returns_zero_on_clean_tree():
    # The real repo tree must pass: only the allowlisted publications grant exists.
    violations, errors = gate.check(gate.DEFAULT_MIGRATIONS, gate.DEFAULT_ALLOWLIST)
    assert errors == [], errors
    assert violations == [], violations
