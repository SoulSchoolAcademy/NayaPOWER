"""Real intent_to_harm producers for the Intent Doctrine disqualification branch.

The disqualification branch in kernel/value_calculus.py fires on
Candidate.intent_to_harm — but nothing ever set that field from real input,
so the branch could never fire on real data: a live check with a dead sensor.

This module is the sensor layer: typed inputs in, typed assessment out.
kernel/act_pipeline._candidate_to_calculus() runs assess_intent() over each
candidate's real text fields, so every plan reaching the calculus carries a
produced intent verdict — never a hand-set literal.

Scope honesty (read before extending): these producers detect DECLARED
intent — plain-language statements that the action's purpose is to harm.
Veiled, paraphrased, or implied intent outside the declared patterns is NOT
detected. That fail-open boundary is documented and covered by an explicit
test (test_fail_open_boundary_is_declared) — it is a known sensor limit,
not a hidden one. The harm-target lexicon is a CLOSED list of person/system
targets (_HUMAN_TARGETS / _SYSTEM_TARGETS): novel targets outside it evade.
Normalization defeats leet respellings (h4rm -> harm) and word separators
(harm-the-users), but keyword-internal separator insertion (h-a-r-m) still
evades — pinned by test_keyword_internal_separators_still_evade.
Extending coverage means adding producers, not weakening the gate.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import re

PRODUCER_VERSION = "INTENT-PRODUCERS-V1"

# ---------------------------------------------------------------------------
# Typed inputs / outputs
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class IntentSignal:
    """One sensor's verdict on the input."""

    signal_id: str          # e.g. "declared-intent:description"
    producer: str           # producer name + PRODUCER_VERSION
    fired: bool
    confidence: float       # 0..1 when fired; 0.0 when not fired
    evidence_refs: tuple = ()   # ("candidate.description",) — where it fired
    detail: str = ""        # the matched span (normalized), for audit


@dataclass(frozen=True)
class IntentAssessment:
    """The produced intent verdict for one candidate."""

    intent_to_harm: bool
    signals: tuple = ()
    reasons: tuple = ()         # e.g. ("DECLARED_HARMFUL_INTENT",)
    evidence_refs: tuple = ()   # union of fired signals' evidence_refs
    producer_version: str = PRODUCER_VERSION


# ---------------------------------------------------------------------------
# Normalization (leet/lookalike + separator collapse so trivial respellings
# cannot evade the declared-intent scan)
# ---------------------------------------------------------------------------

_LEET_TRANSLATION = str.maketrans({
    "1": "i", "!": "i", "|": "i",
    "0": "o",
    "3": "e",
    "4": "a", "@": "a",
    "5": "s", "$": "s",
    "7": "t", "+": "t",
    "8": "b",
    "9": "g",
})


def _normalize(text: str) -> str:
    lowered = (text or "").lower()
    # Possessives collapse first: "competitor's" -> "competitor", so the
    # stray "s" token cannot break verb+target adjacency.
    lowered = re.sub(r"['\u2019]s\b", "", lowered)
    translated = lowered.translate(_LEET_TRANSLATION)
    unified = re.sub(r"[-_.\s/\\:;,\(\)\"']+", " ", translated)
    return re.sub(r"\s+", " ", unified).strip()


# ---------------------------------------------------------------------------
# Benign frames: harm-words used in a safety context must NOT fire.
# These spans are stripped before the sensors run, so a field can carry both
# a benign frame and a real declaration ("we do harm reduction; the plan is
# to harm users") and only the declaration fires.
# ---------------------------------------------------------------------------

_BENIGN_FRAMES = (
    r"harm\s+reduction",
    r"reduc\w*\s+(the\s+)?harm\w*",
    r"prevent\w*\s+(the\s+)?harm\w*",
    r"avoid\w*\s+(the\s+)?harm\w*",
    r"do\s+no\s+harm",
    r"minimi\w*\s+(the\s+)?harm\w*",
    r"mitigat\w*\s+(the\s+)?harm\w*",
    r"assess\w*\s+(the\s+)?damage",
    r"damage\s+assessment",
    r"damage\s+control",
    r"remov\w*\s+harmful",
    r"harmful\s+content\s+(moderation|removal|filter\w*)",
    r"no\s+harm\s+(intended|done|caused)",
    r"protect\w*\s+from\s+harm",
)
_BENIGN_RE = re.compile(r"(?:%s)" % "|".join(_BENIGN_FRAMES))

# ---------------------------------------------------------------------------
# Sensor patterns (run against normalized text)
# ---------------------------------------------------------------------------

_HARM_VERBS = (
    "harm", "hurt", "injure", "maim", "kill", "murder",
    "sabotage", "destroy", "damage", "ruin", "cripple",
    "attack", "harass", "threaten", "intimidate", "blackmail", "defraud",
)
_HARM_VERBS_RE = "|".join(_HARM_VERBS)

# Sensor 1 — explicit declarations: "intent to harm", "intend to hurt",
# "goal is to sabotage", "plan to kill". Confidence 1.0.
_DECLARED_RE = re.compile(
    r"\bintent\s+to\s+(?:%s)\b" % _HARM_VERBS_RE
    + r"|\bintends?\s+to\s+(?:harm|hurt|injure|sabotage|kill|attack|harass|defraud)\b"
    + r"|\bplans?\s+to\s+(?:harm|hurt|sabotage|kill|attack)\b"
    + r"|\b(?:goal|purpose|aim|objective)s?\s+(?:is|are)\s+to\s+"
      r"(?:harm|hurt|injure|sabotage|destroy|damage|kill|ruin|attack)\b"
)

# Sensor 2 — purpose clauses: "in order to harm", "so that X is harmed",
# "to cause harm to X", "with the intent to destroy". Confidence 0.95.
_PURPOSE_RE = re.compile(
    r"\bin\s+order\s+to\s+(?:%s)\b" % _HARM_VERBS_RE
    + r"|\bso\s+that\b.{0,80}?\b(?:is|are|will\s+be|gets?|were)\s+"
      r"(?:harmed|hurt|injured|damaged|destroyed|sabotaged|killed|ruined|attacked)\b"
    + r"|\bto\s+cause\s+harm\s+to\b"
    + r"|\bwith\s+the\s+intent\s+to\s+(?:%s)\b" % _HARM_VERBS_RE
)

# Sensor 3 — harm verb + named target: "harm the users",
# "destroy the production database", "sabotage the payment system".
# Confidence 0.9.
_HUMAN_TARGETS = (
    "users?", "customers?", "clients?", "employees?", "people", "public",
    "competitors?", "rivals?", "victims?", "members?", "patients?",
    "students?", "children", "voters", "tenants?", "subscribers?",
    "vendors?", "suppliers?", "partners?", "regulators?", "journalists?",
)
_SYSTEM_TARGETS = (
    "database", "system", "service", "reputation", "business",
    "servers?", "network", "pipeline", "election", "campaign",
    "website", "platform", "infrastructure",
)
_TARGET_RE = re.compile(
    r"\b(?:harm|hurt|injure|kill|harass|threaten|intimidate|blackmail|defraud|attack)"
    r"\s+(?:the\s+|their\s+|our\s+)?(?:%s)\b" % "|".join(_HUMAN_TARGETS)
    + r"|\b(?:sabotage|destroy|damage|ruin|cripple|disrupt)"
      r"\s+(?:the\s+|their\s+|our\s+)?(?:[a-z0-9_]+\s+)?(?:%s)\b" % "|".join(_SYSTEM_TARGETS)
    + r"|\b(?:harm|hurt|destroy|damage|sabotage)\s+[a-z0-9_]+s\s+"
      r"(?:data|reputation|business|system|database)\b"
)

_SENSORS = (
    ("declared-intent", _DECLARED_RE, 1.0, "DECLARED_HARMFUL_INTENT"),
    ("purpose-clause", _PURPOSE_RE, 0.95, "HARMFUL_PURPOSE_DECLARED"),
    ("harm-target", _TARGET_RE, 0.9, "HARM_TARGET_NAMED"),
)


def _strip_benign_frames(normalized: str) -> str:
    return _BENIGN_RE.sub(" ", normalized)


def _scan_field(field_name: str, text: str) -> list[IntentSignal]:
    """Run all three sensors over one typed input field."""
    if not isinstance(text, str):
        raise TypeError(f"{field_name} must be str, got {type(text).__name__}")
    normalized = _strip_benign_frames(_normalize(text))
    signals: list[IntentSignal] = []
    for sensor_id, pattern, confidence, _reason in _SENSORS:
        match = pattern.search(normalized)
        fired = match is not None
        signals.append(IntentSignal(
            signal_id=f"{sensor_id}:{field_name}",
            producer=f"{sensor_id}/{PRODUCER_VERSION}",
            fired=fired,
            confidence=confidence if fired else 0.0,
            evidence_refs=(f"candidate.{field_name}",) if fired else (),
            detail=match.group(0).strip()[:120] if fired else "",
        ))
    return signals


def assess_intent(*, action_text: str = "", description: str = "",
                  expected_outcome: str = "") -> IntentAssessment:
    """Produce the intent_to_harm verdict from real candidate text.

    Typed keyword-only inputs: the candidate's own action/description/
    expected_outcome strings — the same data the planner sees. No other
    channel can set the verdict (see the anti-bypass test).
    """
    signals: list[IntentSignal] = []
    signals.extend(_scan_field("action", action_text))
    signals.extend(_scan_field("description", description))
    signals.extend(_scan_field("expected_outcome", expected_outcome))

    fired = [s for s in signals if s.fired]
    reasons = tuple(dict.fromkeys(
        reason for s in fired
        for _sid, _pat, _conf, reason in _SENSORS
        if s.signal_id.startswith(_sid + ":")
    ))
    evidence_refs = tuple(dict.fromkeys(
        ref for s in fired for ref in s.evidence_refs
    ))
    return IntentAssessment(
        intent_to_harm=bool(fired),
        signals=tuple(signals),
        reasons=reasons,
        evidence_refs=evidence_refs,
    )
