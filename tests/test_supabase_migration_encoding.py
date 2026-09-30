from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"


def test_supabase_sql_migrations_do_not_start_with_utf8_bom():
    offenders = [
        str(path.relative_to(ROOT))
        for path in sorted(MIGRATIONS.glob("*.sql"))
        if path.read_bytes().startswith(b"\xef\xbb\xbf")
    ]
    assert offenders == [], f"Supabase SQL migrations must be UTF-8 without BOM: {offenders}"
