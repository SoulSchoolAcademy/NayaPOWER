"""UD-04 — CLAIMS STAY FAITHFUL, FROM EXTRACTION TO EVERY COPY.

Absorbs D4, D5, D14, D32.

Every claim the system touches carries exactly what its evidence supports —
from extraction, through every summary, index, Smart Note, and successor
package. Uncertainty travels with claims along true evidence dependencies
only: a summary may compress words but may never raise certainty, upgrade a
hypothesis to a fact, widen scope, or turn repetition into corroboration.

Three mechanisms:

1. EXTRACTION GATE — a proposed extraction (atomic claims with declared
   source spans) is checked for meaning preservation: negations, conditions,
   chronology, and quantifiers must survive. Dropped qualifiers and
   unsupported generalizations are refused with named codes.

2. CLAIM MANIFESTS — every claim carries a support set (AND/OR/partial
   semantics with region verdicts) and an origin chain. Repetition is
   detected structurally (shared origin/ancestor chain) and never counted
   as evidence.

3. PROPAGATION GUARDS — per surface (summary / index / smart_note /
   successor_package / document), every rendering of a claim is classified
   ANCHORING / CORROBORATING / REPEATING / PROMOTING / INADMISSIBLE.
   Promotion is structurally forbidden: the guard refuses and names the
   stage (PROMOTION_FORBIDDEN@<surface>).

Relationship to the D32 document gate (tools/d32_gate.py, draft PR #2224):
that gate enforces uncertainty discipline on markdown documents (sourced
numbers, does-not-claim section, evidenced confidence words). It is kept
as-is and treated as the document-surface instance of the same law. This
module is the general machinery: extraction, manifests, and the four
named surfaces plus the document hook point.

A claim's certainty ladder (never raised by propagation, only by honest
recompute from new evidence):
    UNKNOWN < HYPOTHESIS < SUPPORTED < PROVEN
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Certainty ladder
# ---------------------------------------------------------------------------

UNKNOWN = 0
HYPOTHESIS = 1
SUPPORTED = 2
PROVEN = 3

_CERTAINTY_NAMES = {0: "UNKNOWN", 1: "HYPOTHESIS", 2: "SUPPORTED", 3: "PROVEN"}
_NAME_TO_CERTAINTY = {v: k for k, v in _CERTAINTY_NAMES.items()}


def certainty_name(level: int) -> str:
    return _CERTAINTY_NAMES[level]


def certainty_level(name: str) -> int:
    return _NAME_TO_CERTAINTY[name.upper()]


# Quantifier widening order (narrow -> wide). Widening without evidence is
# promotion. "n-of-m" is handled numerically.
_QUANTIFIER_ORDER = ["none", "one", "few", "some", "most", "all"]


def _quantifier_rank(q: str) -> tuple[int, str]:
    q = q.strip().lower()
    m = re.fullmatch(r"(\d+)\s+of\s+(\d+)", q)
    if m:
        n, d = int(m.group(1)), int(m.group(2))
        # rank by fraction, tie-broken after "some"
        return (2, f"{n / d:.4f}")
    if q in _QUANTIFIER_ORDER:
        return (_QUANTIFIER_ORDER.index(q), "")
    return (2, q)  # unknown quantifier: treat as "some"-level, named


# ---------------------------------------------------------------------------
# Qualifier signatures (extraction gate)
# ---------------------------------------------------------------------------

_NEGATION_RE = re.compile(
    r"\b(not|never|no\b|none|without|fails?\s+to|unable\s+to|cannot|can't|won't|"
    r"didn't|doesn't|don't|isn't|aren't|wasn't|weren't|hasn't|haven't|hadn't)\b",
    re.IGNORECASE,
)
_CONDITION_RE = re.compile(
    r"\b(if|when|unless|provided|providing|only\s+if|as\s+long\s+as|in\s+case|"
    r"assuming|given\s+that)\b",
    re.IGNORECASE,
)
_QUANTIFIER_RE = re.compile(
    r"\b(all|every|each|most|many|some|several|few|a\s+few|one|single|none)\b"
    r"|\b(\d+)\s+of\s+(\d+)",
    re.IGNORECASE,
)
_TIME_RE = re.compile(
    r"\b(19|20)\d{2}(-\d{2}(-\d{2})?)?\b"
    r"|\b(before|after|until|since|during|between)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class QualifierSignature:
    """The decision-critical qualifiers present in a sentence."""
    negated: bool
    conditions: tuple[str, ...]
    quantifier: str  # narrowest quantifier found, default "some"
    has_time: bool

    def promotion_vs(self, source: "QualifierSignature") -> list[str]:
        """Codes for every way this signature is weaker than the source."""
        codes: list[str] = []
        if source.negated and not self.negated:
            codes.append("NEGATION_DROPPED")
        if not source.negated and self.negated:
            codes.append("NEGATION_FLIPPED")
        if len(self.conditions) < len(source.conditions):
            codes.append("CONDITION_DROPPED")
        if _quantifier_rank(self.quantifier) > _quantifier_rank(source.quantifier):
            codes.append("QUANTIFIER_WIDENED")
        if source.has_time and not self.has_time:
            codes.append("TIME_SCOPE_DROPPED")
        return codes


def signature_of(sentence: str) -> QualifierSignature:
    conds = tuple(sorted(set(m.group(0).lower() for m in _CONDITION_RE.finditer(sentence))))
    q = "some"
    for m in _QUANTIFIER_RE.finditer(sentence):
        raw = m.group(0).lower()
        raw = re.sub(r"\s+", " ", raw)
        if raw in ("a few",):
            raw = "few"
        if raw in ("every", "each", "many"):
            raw = {"every": "all", "each": "all", "many": "most"}[raw]
        if raw == "several":
            raw = "some"
        # keep the narrowest quantifier found (most conservative reading)
        if _quantifier_rank(raw) < _quantifier_rank(q):
            q = raw
    return QualifierSignature(
        negated=bool(_NEGATION_RE.search(sentence)),
        conditions=conds,
        quantifier=q,
        has_time=bool(_TIME_RE.search(sentence)),
    )


# ---------------------------------------------------------------------------
# Extraction gate
# ---------------------------------------------------------------------------

@dataclass
class ExtractedClaim:
    """One atomic claim proposed by an extractor."""
    id: str
    text: str
    source_span: tuple[int, ...]  # sentence indices in the source
    certainty: int = HYPOTHESIS
    negated: bool = False
    conditions: tuple[str, ...] = ()
    quantifier: str = "some"
    time_scope: str | None = None


@dataclass
class ExtractionVerdict:
    claim_id: str
    ok: bool
    codes: list[str] = field(default_factory=list)


def check_extraction(source_sentences: list[str],
                     claims: list[ExtractedClaim]) -> list[ExtractionVerdict]:
    """Verify every extracted claim preserves its source's qualifiers.

    Rules (all mechanical):
    - A claim with an empty source span is an unsupported generalization.
    - Dropping/flipping a negation, dropping a condition, widening a
      quantifier, or dropping the time scope is refused with a named code.
    - Decision-critical qualifiers must survive 100%: one violation fails
      the claim.
    """
    verdicts: list[ExtractionVerdict] = []
    for claim in claims:
        if not claim.source_span:
            verdicts.append(ExtractionVerdict(
                claim.id, False, ["UNSUPPORTED_GENERALIZATION"]))
            continue
        codes: list[str] = []
        rendered = QualifierSignature(
            negated=claim.negated,
            conditions=tuple(sorted(claim.conditions)),
            quantifier=claim.quantifier,
            has_time=claim.time_scope is not None,
        )
        for idx in claim.source_span:
            if idx < 0 or idx >= len(source_sentences):
                codes.append("SPAN_OUT_OF_RANGE")
                continue
            src = signature_of(source_sentences[idx])
            for code in rendered.promotion_vs(src):
                if code not in codes:
                    codes.append(code)
        # A claim asserting "all" with no source quantifier basis is refused.
        if claim.quantifier.strip().lower() == "all":
            basis = any(
                signature_of(source_sentences[i]).quantifier == "all"
                for i in claim.source_span
                if 0 <= i < len(source_sentences)
            )
            if not basis and "QUANTIFIER_WIDENED" not in codes:
                codes.append("UNSUPPORTED_GENERALIZATION")
        verdicts.append(ExtractionVerdict(claim.id, not codes, codes))
    return verdicts


# ---------------------------------------------------------------------------
# Claim manifests: support sets with AND/OR/partial semantics
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SupportItem:
    evidence_id: str
    weight: float  # 0..1, partial support allowed
    verdict: str = "SUPPORTS"  # SUPPORTS | PARTIALLY_SUPPORTS | CONTESTED


@dataclass
class SupportSet:
    mode: str = "AND"  # AND | OR
    items: list[SupportItem] = field(default_factory=list)

    def verdict(self) -> float:
        """Combined support weight. AND = weakest link; OR = best witness."""
        if not self.items:
            return 0.0
        weights = [i.weight for i in self.items]
        if self.mode.upper() == "OR":
            return max(weights)
        return min(weights)

    def region_verdicts(self) -> dict[str, float]:
        """Per-evidence verdicts: no bad region hides behind a good average."""
        return {i.evidence_id: i.weight for i in self.items}

    def evidence_ids(self) -> set[str]:
        return {i.evidence_id for i in self.items}


@dataclass
class Claim:
    id: str
    text: str
    certainty: int
    support: SupportSet = field(default_factory=SupportSet)
    origin: tuple[str, ...] = ()  # origin/ancestor chain, oldest first
    negated: bool = False
    conditions: tuple[str, ...] = ()
    quantifier: str = "some"
    time_scope: str | None = None

    def origin_set(self) -> set[str]:
        return set(self.origin)


def shares_lineage(a: Claim, b: Claim) -> bool:
    """True if the two claims share any origin/ancestor: repetition, not
    corroboration. Structural detection — no text similarity heuristics."""
    return bool(a.origin_set() & b.origin_set())


def independent_support_count(claims: list[Claim]) -> int:
    """How many lineage-distinct roots support this claim family."""
    seen: set[str] = set()
    for c in claims:
        if c.origin:
            seen.add(c.origin[0])
    return len(seen)


# ---------------------------------------------------------------------------
# Propagation guards
# ---------------------------------------------------------------------------

SURFACES = ("summary", "index", "smart_note", "successor_package", "document")

# Classification codes
ANCHORING = "ANCHORING"         # restates, same certainty, cites the claim
CORROBORATING = "CORROBORATING"  # new lineage-distinct evidence, same claim
REPEATING = "REPEATING"         # same lineage restated: never evidence
PROMOTING = "PROMOTING"         # certainty raised / scope widened: forbidden
INADMISSIBLE = "INADMISSIBLE"   # unsupported: refused at the surface


@dataclass
class Rendering:
    """How a claim appears on a target surface."""
    text: str
    certainty: int
    cites: tuple[str, ...] = ()       # claim ids cited
    new_evidence: tuple[str, ...] = ()  # evidence ids added on this surface
    new_origin: tuple[str, ...] = ()    # origin chain of the new evidence
    negated: bool = False
    conditions: tuple[str, ...] = ()
    quantifier: str = "some"
    time_scope: str | None = None


@dataclass
class PropagationVerdict:
    classification: str
    allowed: bool
    refusal_code: str | None = None
    notes: list[str] = field(default_factory=list)


def classify_propagation(claim: Claim, rendering: Rendering,
                         surface: str) -> PropagationVerdict:
    """Classify one rendering of a claim on one surface.

    Order matters — promotion is checked before anything else, because a
    polished promotion must never be misread as corroboration.
    """
    notes: list[str] = []
    rendered_sig = QualifierSignature(
        negated=rendering.negated,
        conditions=tuple(sorted(rendering.conditions)),
        quantifier=rendering.quantifier,
        has_time=rendering.time_scope is not None,
    )
    claim_sig = QualifierSignature(
        negated=claim.negated,
        conditions=tuple(sorted(claim.conditions)),
        quantifier=claim.quantifier,
        has_time=claim.time_scope is not None,
    )

    # 1. Certainty raised -> promotion, always forbidden.
    if rendering.certainty > claim.certainty:
        return PropagationVerdict(
            PROMOTING, False,
            f"PROMOTION_FORBIDDEN@{surface}",
            [f"certainty raised {certainty_name(claim.certainty)}"
             f"->{certainty_name(rendering.certainty)} at surface '{surface}'"],
        )
    # 2. Qualifier weakened -> promotion (scope widened / meaning changed).
    promo_codes = rendered_sig.promotion_vs(claim_sig)
    if promo_codes:
        return PropagationVerdict(
            PROMOTING, False,
            f"PROMOTION_FORBIDDEN@{surface}",
            [f"{code} at surface '{surface}'" for code in promo_codes],
        )
    # 3. Presented as fact with no support and no citation -> inadmissible.
    if (rendering.certainty >= SUPPORTED
            and claim.id not in rendering.cites
            and claim.support.verdict() == 0.0 and not rendering.new_evidence):
        return PropagationVerdict(
            INADMISSIBLE, False, f"INADMISSIBLE@{surface}",
            ["unsupported claim presented as fact"],
        )
    # 4. New lineage-distinct evidence -> corroborating (never raises grade
    #    by itself; grade recompute is a separate honest step).
    if rendering.new_evidence:
        if set(rendering.new_origin) & claim.origin_set():
            notes.append("new evidence shares lineage: repetition, not corroboration")
            return PropagationVerdict(REPEATING, True, None, notes)
        notes.append(
            f"lineage-distinct evidence {list(rendering.new_evidence)} corroborates "
            f"without raising {certainty_name(claim.certainty)}")
        return PropagationVerdict(CORROBORATING, True, None, notes)
    # 5. Same lineage restated -> repeating. Repetition is never evidence.
    notes.append("same origin chain restated: repetition carries no evidential weight")
    return PropagationVerdict(REPEATING, True, None, notes)


def guard_surface(surface: str, claim: Claim,
                  rendering: Rendering) -> PropagationVerdict:
    """The per-surface propagation guard. Promotion is structurally
    forbidden: the guard refuses and names the stage."""
    if surface not in SURFACES:
        return PropagationVerdict(INADMISSIBLE, False,
                                  f"UNKNOWN_SURFACE@{surface}",
                                  [f"surface '{surface}' is not a governed surface"])
    return classify_propagation(claim, rendering, surface)


def anchoring_rendering(claim: Claim) -> Rendering:
    """Build the canonical faithful rendering: same certainty, same
    qualifiers, cites the claim. This is what ANCHORING looks like."""
    return Rendering(
        text=claim.text,
        certainty=claim.certainty,
        cites=(claim.id,),
        negated=claim.negated,
        conditions=claim.conditions,
        quantifier=claim.quantifier,
        time_scope=claim.time_scope,
    )


# ---------------------------------------------------------------------------
# Honest recompute: derived claims and mentions
# ---------------------------------------------------------------------------

def derive_claim(new_id: str, text: str, sources: list[Claim],
                 **qualifiers) -> Claim:
    """A derived claim recomputes its certainty honestly: it can never
    exceed its weakest source. Origin is the union of source chains."""
    level = min([s.certainty for s in sources], default=UNKNOWN)
    origins: list[str] = []
    for s in sources:
        for o in s.origin:
            if o not in origins:
                origins.append(o)
    support = SupportSet(
        mode="AND",
        items=[SupportItem(evidence_id=s.id, weight=s.support.verdict())
               for s in sources],
    )
    return Claim(id=new_id, text=text, certainty=level, support=support,
                 origin=tuple(origins), **qualifiers)


@dataclass(frozen=True)
class Mention:
    """A mention/citation of a claim. Mentions do NOT transmit certainty:
    pointing at a claim is not evidence for it."""
    claim_id: str
    referenced_certainty: int
    transmits_certainty: bool = False


def mention(claim: Claim) -> Mention:
    return Mention(claim_id=claim.id, referenced_certainty=claim.certainty)


# ---------------------------------------------------------------------------
# Lesson quarantine: one bad claim never launders its neighbors
# ---------------------------------------------------------------------------

@dataclass
class LessonAudit:
    kept: list[Claim]
    quarantined: list[tuple[Claim, str]]  # (claim, reason)


def audit_lesson(claims: list[Claim],
                 extraction_verdicts: dict[str, ExtractionVerdict]
                 ) -> LessonAudit:
    """Split a mixed-validity lesson claim by claim. A failed claim is
    quarantined with its reason; valid claims keep their standing. The
    lesson is never taken down whole because of one bad claim."""
    kept: list[Claim] = []
    quarantined: list[tuple[Claim, str]] = []
    for claim in claims:
        v = extraction_verdicts.get(claim.id)
        if v is not None and not v.ok:
            quarantined.append((claim, "EXTRACTION_FAILED: " + ",".join(v.codes)))
            continue
        if claim.certainty >= SUPPORTED and claim.support.verdict() == 0.0:
            quarantined.append((claim, "UNSUPPORTED_FACT"))
            continue
        kept.append(claim)
    return LessonAudit(kept=kept, quarantined=quarantined)


def survives_compromise(claims: list[Claim],
                        compromised_ids: set[str]) -> list[Claim]:
    """Independent alternatives survive unrelated compromise: a claim
    survives iff its support evidence is disjoint from every compromised
    claim's support evidence."""
    compromised_evidence: set[str] = set()
    by_id = {c.id: c for c in claims}
    for cid in compromised_ids:
        if cid in by_id:
            compromised_evidence |= by_id[cid].support.evidence_ids()
    survivors: list[Claim] = []
    for claim in claims:
        if claim.id in compromised_ids:
            continue
        if claim.support.evidence_ids() & compromised_evidence:
            continue
        survivors.append(claim)
    return survivors


# ---------------------------------------------------------------------------
# What this does NOT claim
# ---------------------------------------------------------------------------
# - The extraction gate checks a PROPOSED extraction; it does not extract
#   claims from raw text by itself (no NLP). An extractor proposes, the
#   gate disposes.
# - Qualifier detection is pattern-based (stdlib regex). Deliberately
#   paraphrased qualifier-dropping that evades the patterns is outside
#   this gate's vision; the adversarial corpus covers the direct forms.
# - Corroboration judges lineage-distinctness, not truth: two independent
#   wrong witnesses still corroborate structurally. Truth needs UD-02.
