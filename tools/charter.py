"""The NayaPOWER Charter — in code.

This module is the machine embodiment of the system charter. The canonical
machine source is MANIFESTO.machine.json at the repo root; this module loads
it once and exposes the motto, the manifesto, the twelve laws, and the mission
question as importable law — so any code in the system operates on the same
thesis the humans read.

    from tools.charter import MOTTO, TWELVE_LAWS, mission_check

Status: PROPOSED — the charter becomes law only on the Human Director's
ratification. Until then this module is the proposed machine form, never
quoted as authority.
"""

import json
from pathlib import Path

_CHARTER_PATH = Path(__file__).resolve().parents[1] / "MANIFESTO.machine.json"


def _load():
    with open(_CHARTER_PATH, encoding="utf-8") as f:
        return json.load(f)


_CHARTER = _load()

SCHEMA = _CHARTER["schema"]
VERSION = _CHARTER["version"]
STATUS = _CHARTER["status"]

MOTTO = _CHARTER["motto"]
MANIFESTO_STATEMENT = _CHARTER["manifesto_statement"]
MANIFESTO_FULL = _CHARTER["manifesto_full"]
PURPOSE = _CHARTER["purpose"]
MISSION_QUESTION = _CHARTER["mission_question"]
PRIVACY_LINE = _CHARTER["privacy_line"]
PRECEDENCE_CHAIN = _CHARTER["precedence_chain"]
FIVE_QUESTIONS = _CHARTER["five_questions"]
TWELVE_LAWS = _CHARTER["twelve_laws"]  # list of {id, title, statement}
LAW_BY_ID = {law["id"]: law for law in TWELVE_LAWS}


def law(law_id):
    """Return the law dict for a canonical law id, e.g. law('FAIL_CLOSED')."""
    return LAW_BY_ID[law_id]


def mission_check(description):
    """Frame any proposed work against the mission question.

    Returns the question the proposer must answer — the machine does not
    answer it for them.
    """
    return (
        f"{MISSION_QUESTION} "
        f"Proposed work: {description}. "
        "If the answer is not a measurable yes at the least necessary "
        "complexity, it does not ship."
    )


def recite():
    """The charter in its shortest complete spoken form."""
    laws = "; ".join(f"{i+1}. {l['title']}" for i, l in enumerate(TWELVE_LAWS))
    return f"{MOTTO} {MANIFESTO_STATEMENT} The twelve laws: {laws}."
