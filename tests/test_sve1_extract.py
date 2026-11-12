"""Tests for sve1.py extract — the SVE-1 mechanical extraction step.

tools/human_value/sve1.py — covers the exact extraction rule from the SVE-1
spec (hidden_files/areas/mu-value-instrument-1-20261012T2145.md §7):

  - colon-attribution quotes -> reported (authorship=inferred, seat source)
  - same-line attribution-clause quotes -> verbatim
  - seat restatements without quote marks -> side ledger (paraphrase, never units)
  - unattributed quote spans -> side ledger (uncertain)
  - dedupe by content hash across lines
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SVE1 = Path(__file__).resolve().parent.parent / "tools" / "human_value" / "sve1.py"
SYS = sys.executable


def extract(text):
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as fh:
        fh.write(text)
        path = fh.name
    out = subprocess.run(
        [SYS, str(SVE1), "extract", path], capture_output=True, text=True
    )
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def test_colon_attribution_is_reported_not_verbatim():
    d = extract('Notes: Shawn: "Keep up giving me the updates. I love that."\n')
    assert d["counts"]["candidates"] == 1
    c = d["candidates"][0]
    assert c["class"] == "reported"
    assert c["attribution"] == "colon"
    assert c["span"] == "Keep up giving me the updates. I love that."


def test_clause_attribution_is_verbatim():
    d = extract('Shawn said the format worked, "keep them coming".\n')
    assert d["counts"]["candidates"] == 1
    assert d["candidates"][0]["class"] == "verbatim"
    assert d["candidates"][0]["span"] == "keep them coming"


def test_paraphrase_never_counted():
    d = extract("He liked the new format and he loved the color scheme.\n")
    assert d["counts"]["candidates"] == 0
    assert any(c["class"] == "paraphrase" for c in d["side_ledger"])


def test_unattributed_quote_is_uncertain():
    d = extract('Random seat note: "the hold that stood all day is drained".\n')
    assert d["counts"]["candidates"] == 0
    assert any(c["class"] == "uncertain" for c in d["side_ledger"])


def test_dedupe_across_lines():
    d = extract(
        'Shawn: "Take the reins, this is your baby."\n'
        'Recount: Shawn: "Take the reins, this is your baby."\n'
    )
    assert d["counts"]["candidates"] == 1


def test_empty_window_is_clean_exit_not_error():
    d = extract("Nothing here. Just a normal log line.\n")
    assert d["counts"]["candidates"] == 0
    assert d["counts"]["side_ledger"] == 0
