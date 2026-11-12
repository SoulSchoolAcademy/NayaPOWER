#!/usr/bin/env python3
"""Regression test for D4 owner_scope doctrine (PR #2678).

D4: owner_scope=PRIVATE rows never enter public emitter output.
The D4 commit on emit_hub_feeds.py adds ``WHERE owner_scope != 'PRIVATE'``
to emit_lists() (emit_smart_feed() already had it). This test proves the
filter end-to-end against the *actual query text* emitted by emit_lists():
it routes that SQL through a stdlib-only SQLite stand-in, seeded with one
PUBLIC row and one PRIVATE row, and asserts the PRIVATE row is excluded
from emit_lists() output while the PUBLIC row is included.

Stdlib only: unittest, sqlite3, json. No network, no sb-api helper, no
credentials. The Postgres ``content->>'topic'`` operator is translated to
SQLite ``json_extract`` in the shim — the WHERE predicate under test is
executed verbatim.
"""
import json
import os
import sqlite3
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "HUB", "FEEDS"))

import emit_hub_feeds  # noqa: E402


def seed_db():
    """Temp SQLite stand-in for nayanet_intelligent_blocks."""
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE nayanet_intelligent_blocks ("
        "  intelligent_block_id TEXT,"
        "  title TEXT,"
        "  content TEXT,"
        "  updated_at TEXT,"
        "  owner_scope TEXT)"
    )
    conn.executemany(
        "INSERT INTO nayanet_intelligent_blocks "
        "(intelligent_block_id, title, content, updated_at, owner_scope) "
        "VALUES (?,?,?,?,?)",
        [
            # (id, title, content, updated_at, owner_scope)
            ("public-block-1", "Public note", json.dumps({"topic": "D4-TEST"}),
             "2026-10-16T00:00:00Z", "PUBLIC"),
            ("private-block-9", "Private note", json.dumps({"topic": "D4-TEST"}),
             "2026-10-16T00:01:00Z", "PRIVATE"),
            # NULL scope = unknown; D4 doctrine is fail-closed: excluded.
            ("nullscope-block-7", "Unknown-scope note", json.dumps({"topic": "D4-TEST"}),
             "2026-10-16T00:02:00Z", None),
        ],
    )
    conn.commit()
    return conn


def sqlite_q_shim(conn):
    """Translate emit_hub_feeds' Postgres dialect to SQLite and run it.

    The WHERE predicate (owner_scope != 'PRIVATE') passes through verbatim;
    only the Postgres-only ``->>`` JSON operator is translated.
    """
    def q(sql):
        sql = sql.replace(
            "content->>'topic'", "json_extract(content, '$.topic')")
        cur = conn.execute(sql)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]
    return q


class TestD4OwnerScopeFilter(unittest.TestCase):
    def setUp(self):
        self.conn = seed_db()
        self._real_q = emit_hub_feeds.q
        emit_hub_feeds.q = sqlite_q_shim(self.conn)

    def tearDown(self):
        emit_hub_feeds.q = self._real_q
        self.conn.close()

    def test_private_row_excluded_public_row_included(self):
        items, count = emit_hub_feeds.emit_lists()
        members = [m for it in items for m in it["members"]]
        titles = [it["title"] for it in items]
        self.assertIn("public-block-1", members,
                      f"PUBLIC row missing from emit_lists() output: {titles}")
        self.assertNotIn("private-block-9", members,
                         "D4 VIOLATION: PRIVATE row leaked into emit_lists() output")
        self.assertNotIn("nullscope-block-7", members,
                         "D4 VIOLATION: NULL-scope row leaked into emit_lists() output "
                         "(fail-closed: unknown scope must be excluded)")
        self.assertEqual(count, 1, f"expected exactly the PUBLIC row counted, got {count}")


if __name__ == "__main__":
    unittest.main()
