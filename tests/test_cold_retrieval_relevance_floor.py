"""Cold lesson retrieval must not depend on knowing the exact wording of the lesson.

Observed on live `main` at dbe06f9e (2026-10-12), cold seat, no conversation memory.

The canonical cold-retrieval CLI is `tools/smart_note_v2.py retrieve`. Measured against
the live 631-entry registry, content scoring alone clears the relevance floor for 1 of 4
queries with known-correct answers. The floor is therefore being cleared almost entirely
by RETRIEVAL_PHRASE_BONUS, whose value (40.0) is exactly equal to the floor (40.0).
Net effect: retrieval behaves as literal substring matching against title/nutshell, and
the IDF field-weighting machinery is close to inert.

    'corroboration'                     content 26.90  -> MISSED
    'repetition is not corroboration'   content 36.01  -> MISSED   (top-1, then filtered)
    'a gate that cannot fail'           content 39.50  -> MISSED   (0.50 under the floor)
    'shared evidence convergence'       content 44.27  -> HIT

SN-0515 ("Shared-Evidence Convergence Is Agreement, Not Corroboration") is ACTIVE and
CANDIDATE in the registry, and is the note this repo's own anti-citogenesis doctrine
depends on. A cold Naya that thinks in concepts cannot retrieve it; a cold Naya that
already knows the exact title can.

Per PROTOCOL step 14 this is a continuity defect, not a cosmetic one: stored is not
learned, and a lesson a cold successor cannot retrieve has not been transferred.

These tests pin the defect. They are expected to FAIL on current main. They must not be
made to pass by widening the assertion; see the second test for the genuine trap.
"""

from __future__ import annotations

import re

import pytest

from tools import smart_note_v2 as S

# Queries paired with the note a reader would say is unambiguously correct.
# Sourced from live registry state, not from the note's own filename.
LABELLED = [
    ("corroboration", "SN-0515"),
    ("repetition is not corroboration", "SN-0515"),
    ("shared evidence convergence", "SN-0515"),
    ("a gate that cannot fail", "SN-0514"),
]


def _content_ranked(query: str):
    """Rank entries on content score only, with the phrase bonus removed.

    Isolates the IDF/field-weight machinery from the substring bonus so the two
    can be measured separately. Mirrors _ranked_candidates without editing it.
    """
    registry = S.load_json(S.REGISTRY)
    entries = [
        e
        for e in registry.get("entries", [])
        if str(e.get("lifecycle_state", "ACTIVE")).upper()
        not in {"SUPERSEDED", "ARCHIVED", "REVOKED"}
    ]

    scored = []
    for e in entries:
        fields = {
            "title": S._field_words(e.get("title", "")),
            "nutshell": S._field_words(S._nutshell_text(e.get("projection_path", ""))),
            "keywords": S._field_words(" ".join(e.get("keywords", []))),
            "taxonomy": S._field_words(
                " ".join([e.get("category", ""), e.get("topic", ""), e.get("subtopic", "")])
            ),
        }
        scored.append((e, fields))

    idf = S._retrieval_idf([f for _, f in scored])
    avg_len = sum(sum(len(w) for w in f.values()) for _, f in scored) / max(1, len(scored))

    terms = set(S._stem(w) for w in re.findall(r"[a-z0-9]+", query.lower()))
    ranked = []
    for e, fields in scored:
        score = 0.0
        for fname, fweight in S.RETRIEVAL_FIELD_WEIGHTS:
            for w in terms & fields[fname]:
                score += fweight * idf[w]
        doc_len = sum(len(w) for w in fields.values())
        if avg_len > 0:
            score /= 1.0 + S.RETRIEVAL_LENGTH_NORM_PIVOT * (doc_len / avg_len - 1.0)
        if score > 0:
            ranked.append((score, e))
    ranked.sort(key=lambda z: -z[0])
    return ranked


def test_content_scoring_can_clear_the_floor_on_its_own():
    """The relevance floor must be reachable without a literal phrase match.

    Today every labelled query except one is filtered out on content alone, so the
    phrase bonus is silently carrying retrieval. If this still fails after a fix, the
    floor is still mis-set against the corpus it is scored on.
    """
    cleared = []
    for query, expected in LABELLED:
        ranked = _content_ranked(query)
        if not ranked:
            continue
        top_score, top_entry = ranked[0]
        if top_score >= S.RETRIEVAL_RELEVANCE_FLOOR and top_entry.get("smart_note_id") == expected:
            cleared.append(query)
    assert len(cleared) == len(LABELLED), (
        f"Content scoring cleared the floor with the correct note for only "
        f"{len(cleared)}/{len(LABELLED)} labelled queries. The relevance floor is not "
        f"reachable from content alone, so retrieval depends on the query appearing "
        f"verbatim in title or nutshell. cleared={cleared}"
    )


def test_phrase_bonus_is_not_load_bearing_for_admission():
    """The bonus and the floor are both 40.0, so the bonus alone decides admission.

    These should not be equal. When bonus == floor, any query containing one literal
    substring is admitted regardless of content relevance, and any query that does not
    is rejected regardless of how well it matches on meaning.
    """
    assert S.RETRIEVAL_PHRASE_BONUS != S.RETRIEVAL_RELEVANCE_FLOOR, (
        f"RETRIEVAL_PHRASE_BONUS ({S.RETRIEVAL_PHRASE_BONUS}) equals "
        f"RETRIEVAL_RELEVANCE_FLOOR ({S.RETRIEVAL_RELEVANCE_FLOOR}), so substring "
        f"matching alone decides admission and content scoring is decorative."
    )


def test_governing_vocabulary_exists_in_the_corpus():
    """THE TRAP: a floor fix does NOT close this.

    'anti-citogenesis' is the governing term of the newest law on main (#2469,
    merged dbe06f9e). It scores exactly 0.00 against every entry, because the term
    appears in no note's title, nutshell, keywords or taxonomy. Lowering the floor
    changes nothing for this query.

    A repair that reports "retrieval fixed" after only moving the floor has fixed the
    scoring and left the vocabulary gap untouched. This test is what distinguishes the
    two, and it is the reason a floor-only repair must not be called complete.
    """
    assert "citogenesi" not in _corpus_haystack(), (
        "The term 'anti-citogenesis' is absent from every Smart Note's "
        "title/nutshell/keywords/taxonomy. The law can be cited by an agent that has "
        "read AGENTS.md, but it cannot be retrieved by one that has not."
    )


def test_retrieval_does_not_depend_on_where_the_repo_was_cloned():
    """THE SECOND, INDEPENDENT DEFECT: silent retrieval blindness past MAX_PATH.

    Measured on live main at dbe06f9e, same commit, same registry, two checkout
    depths on the same machine:

        checkout path length 57  ->  4  projection paths unreadable, SN-0515 readable
        checkout path length 63  -> 15  projection paths unreadable, SN-0515 UNREADABLE

    `_nutshell_text()` reads each note's distilled lesson. When the open fails, the
    lesson body returns empty and the note is scored on its title alone. Nothing
    raises, nothing is logged, and the retrieval result silently changes.

    The consequence is that what a cold Naya is able to learn depends on the absolute
    path of the directory it happens to be standing in, rather than on the intelligence
    the repository actually stores. SN-0515 -- the note this project's own
    anti-citogenesis doctrine rests on -- is legible at one checkout depth and
    invisible at another.

    A floor recalibration cannot fix this. This is a filesystem-access defect.
    """
    unreadable = []
    for e in S.load_json(S.REGISTRY).get("entries", []):
        path = e.get("projection_path")
        if not path:
            continue
        try:
            with open(path, encoding="utf-8") as fh:
                fh.read()
        except OSError:
            unreadable.append(e.get("smart_note_id"))

    assert not unreadable, (
        f"{len(unreadable)} Smart Note projection paths cannot be read from this "
        f"checkout, so their lessons are invisible to retrieval while still appearing "
        f"in the registry as ACTIVE. Counts change with checkout depth, which means "
        f"retrieval results are a function of where the repo was cloned. "
        f"unreadable={unreadable}"
    )


def _corpus_haystack() -> set[str]:
    registry = S.load_json(S.REGISTRY)
    words: set[str] = set()
    for e in registry.get("entries", []):
        if str(e.get("lifecycle_state", "ACTIVE")).upper() in {"SUPERSEDED", "ARCHIVED", "REVOKED"}:
            continue
        words |= S._field_words(e.get("title", ""))
        words |= S._field_words(S._nutshell_text(e.get("projection_path", "")))
        words |= S._field_words(" ".join(e.get("keywords", [])))
        words |= S._field_words(
            " ".join([e.get("category", ""), e.get("topic", ""), e.get("subtopic", "")])
        )
    return words


@pytest.mark.parametrize("query,expected", LABELLED)
def test_cold_cli_retrieval_returns_expected_note(query, expected, monkeypatch):
    """End-to-end through the shipped CLI, at the shipped floor.

    Guards against a fix that adjusts the scorer but not the public entry point.
    """
    monkeypatch.setenv("PYTHONIOENCODING", "utf-8")
    ranked = S._ranked_candidates(query)
    assert ranked, f"cold retrieval returned nothing for {query!r}"
    assert ranked[0][2].get("smart_note_id") == expected, (
        f"cold retrieval for {query!r} returned {ranked[0][2].get('smart_note_id')}, "
        f"expected {expected}"
    )
