"""Adversarial tests for UD-04 claim fidelity.

Acceptance gate: extraction preserves meaning on all adversarial cases,
mixed-validity lessons keep their good claims, no promotion passes any
surface, and independent alternatives survive unrelated compromise.
One failure = FAIL.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from claim_fidelity import (
    UNKNOWN, HYPOTHESIS, SUPPORTED, PROVEN,
    ExtractedClaim, check_extraction,
    SupportItem, SupportSet,
    Claim, shares_lineage, independent_support_count,
    Rendering, classify_propagation, guard_surface, anchoring_rendering,
    ANCHORING, CORROBORATING, REPEATING, PROMOTING, INADMISSIBLE,
    derive_claim, mention,
    audit_lesson, survives_compromise, ExtractionVerdict,
    SURFACES, certainty_name,
)

PASS = []
FAIL = []


def check(name, cond, detail=""):
    if cond:
        PASS.append(name)
    else:
        FAIL.append(f"{name} :: {detail}")


# ---------------------------------------------------------------------------
# 1. Extraction gate: decision-critical qualifiers preserved 100%
# ---------------------------------------------------------------------------

SRC = [
    "The connector does not write to production.",          # 0: negation
    "Merges are allowed only if the gate passes.",          # 1: condition
    "Three of five trials succeeded in October 2026.",      # 2: quantifier+time
    "Some seats reported higher latency.",                  # 3: quantifier some
    "The cache never serves stale entries after a deploy.",  # 4: negation+time
]

# --- faithful extraction: all green ---
good = [
    ExtractedClaim("g0", "The connector does not write to production.",
                   (0,), negated=True),
    ExtractedClaim("g1", "Merges are allowed only if the gate passes.",
                   (1,), conditions=("only if",)),
    ExtractedClaim("g2", "Three of five trials succeeded in October 2026.",
                   (2,), quantifier="3 of 5", time_scope="2026-10"),
    ExtractedClaim("g3", "Some seats reported higher latency.",
                   (3,), quantifier="some"),
    ExtractedClaim("g4", "The cache never serves stale entries after a deploy.",
                   (4,), negated=True, time_scope="after deploy"),
]
for v in check_extraction(SRC, good):
    check(f"extract faithful {v.claim_id} passes", v.ok, str(v.codes))

# --- negation dropped: meaning flip must be caught ---
v = check_extraction(SRC, [ExtractedClaim("b0", "The connector writes to production.",
                                         (0,), negated=False)])[0]
check("negation dropped -> refused", not v.ok and "NEGATION_DROPPED" in v.codes, str(v.codes))

# --- negation flipped (adding a not that wasn't there) ---
v = check_extraction(SRC, [ExtractedClaim("b0f", "Merges are not allowed only if the gate passes.",
                                          (1,), negated=True, conditions=("only if",))])[0]
check("negation flipped -> refused", not v.ok and "NEGATION_FLIPPED" in v.codes, str(v.codes))

# --- condition dropped: scope widened ---
v = check_extraction(SRC, [ExtractedClaim("b1", "Merges are allowed.",
                                          (1,), conditions=())])[0]
check("condition dropped -> refused", not v.ok and "CONDITION_DROPPED" in v.codes, str(v.codes))

# --- quantifier widened some -> all ---
v = check_extraction(SRC, [ExtractedClaim("b3", "All seats reported higher latency.",
                                          (3,), quantifier="all")])[0]
check("quantifier widened some->all -> refused",
      not v.ok and ("QUANTIFIER_WIDENED" in v.codes or "UNSUPPORTED_GENERALIZATION" in v.codes),
      str(v.codes))

# --- time scope dropped ---
v = check_extraction(SRC, [ExtractedClaim("b2", "Three of five trials succeeded.",
                                          (2,), quantifier="3 of 5")])[0]
check("time scope dropped -> refused", not v.ok and "TIME_SCOPE_DROPPED" in v.codes, str(v.codes))

# --- unsupported generalization: empty source span ---
v = check_extraction(SRC, [ExtractedClaim("b9", "All connectors are safe.", ())])[0]
check("empty span -> UNSUPPORTED_GENERALIZATION",
      not v.ok and "UNSUPPORTED_GENERALIZATION" in v.codes, str(v.codes))

# --- "all" asserted with no "all" in source ---
v = check_extraction(["Some trials passed."],
                     [ExtractedClaim("ba", "All trials passed.", (0,), quantifier="all")])[0]
check("all without source basis -> refused", not v.ok, str(v.codes))


# ---------------------------------------------------------------------------
# 2. Claim manifests: support sets with AND/OR/partial semantics
# ---------------------------------------------------------------------------

ss_and = SupportSet("AND", [SupportItem("e1", 0.9), SupportItem("e2", 0.4)])
check("AND verdict = weakest link", ss_and.verdict() == 0.4, str(ss_and.verdict()))

ss_or = SupportSet("OR", [SupportItem("e1", 0.9), SupportItem("e2", 0.4)])
check("OR verdict = best witness", ss_or.verdict() == 0.9, str(ss_or.verdict()))

check("region verdicts expose the weak region",
      ss_and.region_verdicts() == {"e1": 0.9, "e2": 0.4})

check("empty support = zero", SupportSet("AND", []).verdict() == 0.0)

partial = SupportSet("AND", [SupportItem("e1", 0.5, "PARTIALLY_SUPPORTS")])
check("partial support carries weight 0.5", partial.verdict() == 0.5)


# ---------------------------------------------------------------------------
# 3. Propagation guards: no promotion passes any surface
# ---------------------------------------------------------------------------

hyp = Claim(id="c1", text="The new cache may reduce latency.",
            certainty=HYPOTHESIS,
            support=SupportSet("AND", [SupportItem("bench-7", 0.6)]),
            origin=("bench-7",), quantifier="some")

# 3a. Hypothesis -> fact in a summary: THE demonstration case.
promo = Rendering(text="The new cache reduces latency.",
                  certainty=SUPPORTED, cites=("c1",), quantifier="some")
v = guard_surface("summary", hyp, promo)
check("hypothesis->fact in summary refused", not v.allowed and v.classification == PROMOTING,
      str(v))
check("promotion named at its stage", v.refusal_code == "PROMOTION_FORBIDDEN@summary",
      str(v.refusal_code))
check("promotion note names the grade change",
      any("HYPOTHESIS->SUPPORTED" in n for n in v.notes), str(v.notes))

# 3b. Certainty raise refused on EVERY surface.
for surface in SURFACES:
    r = Rendering(text="The new cache reduces latency.", certainty=PROVEN,
                  cites=("c1",), quantifier="some")
    vv = guard_surface(surface, hyp, r)
    check(f"certainty promotion refused @{surface}",
          not vv.allowed and vv.refusal_code == f"PROMOTION_FORBIDDEN@{surface}",
          str(vv.refusal_code))

# 3c. Negation dropped in a Smart Note -> promotion.
neg = Claim(id="c2", text="The connector does not write to production.",
            certainty=SUPPORTED,
            support=SupportSet("AND", [SupportItem("audit-3", 0.9)]),
            origin=("audit-3",), negated=True)
r = Rendering(text="The connector writes to production.", certainty=SUPPORTED,
              cites=("c2",), negated=False)
vv = guard_surface("smart_note", neg, r)
check("negation dropped in smart_note -> PROMOTING",
      not vv.allowed and any("NEGATION_DROPPED" in n for n in vv.notes), str(vv.notes))

# 3d. Condition dropped in successor package -> promotion.
cond = Claim(id="c3", text="Merges are allowed only if the gate passes.",
             certainty=SUPPORTED,
             support=SupportSet("AND", [SupportItem("gate-log", 0.85)]),
             origin=("gate-log",), conditions=("only if",))
r = Rendering(text="Merges are allowed.", certainty=SUPPORTED,
              cites=("c3",), conditions=())
vv = guard_surface("successor_package", cond, r)
check("condition dropped in successor_package -> PROMOTING",
      not vv.allowed and any("CONDITION_DROPPED" in n for n in vv.notes), str(vv.notes))

# 3e. Quantifier widened in an index -> promotion.
r = Rendering(text="The new cache reduces latency for all workloads.",
              certainty=HYPOTHESIS, cites=("c1",), quantifier="all")
vv = guard_surface("index", hyp, r)
check("quantifier widened in index -> PROMOTING",
      not vv.allowed and any("QUANTIFIER_WIDENED" in n for n in vv.notes), str(vv.notes))

# 3f. Unknown surface refused.
vv = guard_surface("tweet", hyp, anchoring_rendering(hyp))
check("unknown surface refused", not vv.allowed and vv.classification == INADMISSIBLE)


# ---------------------------------------------------------------------------
# 4. Faithful propagation: anchoring allowed, repetition never evidence
# ---------------------------------------------------------------------------

v = guard_surface("summary", hyp, anchoring_rendering(hyp))
check("faithful rendering anchors", v.allowed, str(v.classification))

# Same lineage restated on three surfaces: all REPEATING, support count 1.
copies = [Claim(id=f"copy{i}", text=hyp.text, certainty=HYPOTHESIS,
                support=hyp.support, origin=("bench-7",), quantifier="some")
          for i in range(3)]
for surface in ("summary", "index", "smart_note"):
    vv = guard_surface(surface, hyp, Rendering(
        text=hyp.text, certainty=HYPOTHESIS, cites=(hyp.id,),
        new_origin=("bench-7",), quantifier="some"))
    check(f"same-lineage restatement @{surface} -> REPEATING",
          vv.classification == REPEATING and vv.allowed, str(vv.classification))
check("repetition never counts as corroboration",
      independent_support_count([hyp] + copies) == 1,
      str(independent_support_count([hyp] + copies)))
check("shared lineage detected structurally",
      shares_lineage(hyp, copies[0]) and shares_lineage(copies[0], copies[2]))

# Lineage-distinct evidence -> CORROBORATING, grade unchanged.
r = Rendering(text=hyp.text, certainty=HYPOTHESIS, cites=(hyp.id,),
              new_evidence=("bench-9",), new_origin=("bench-9",), quantifier="some")
vv = guard_surface("summary", hyp, r)
check("lineage-distinct evidence corroborates",
      vv.classification == CORROBORATING and vv.allowed, str(vv.classification))

# "New evidence" sharing lineage is repetition wearing a costume.
r = Rendering(text=hyp.text, certainty=HYPOTHESIS, cites=(hyp.id,),
              new_evidence=("bench-7b",), new_origin=("bench-7",), quantifier="some")
vv = guard_surface("summary", hyp, r)
check("shared-lineage 'new evidence' -> REPEATING, not corroborating",
      vv.classification == REPEATING, str(vv.classification))

# Unsupported claim presented as fact -> INADMISSIBLE.
bare2 = Claim(id="c9b", text="Latency fell.", certainty=SUPPORTED,
              support=SupportSet("AND", []), origin=())
r2 = Rendering(text="Latency fell.", certainty=SUPPORTED, quantifier="some")
vv2 = guard_surface("document", bare2, r2)
check("unsupported fact -> INADMISSIBLE",
      vv2.classification == INADMISSIBLE and not vv2.allowed, str(vv2.classification))


# ---------------------------------------------------------------------------
# 5. Derived claims recompute honestly; mentions transmit nothing
# ---------------------------------------------------------------------------

s1 = Claim(id="s1", text="Gate passed on tip T.", certainty=PROVEN,
           support=SupportSet("AND", [SupportItem("ci-1", 0.95)]), origin=("ci-1",))
s2 = Claim(id="s2", text="Tip T is the merge base.", certainty=SUPPORTED,
           support=SupportSet("AND", [SupportItem("git-1", 0.8)]), origin=("git-1",))
d = derive_claim("d1", "The merge is safe on tip T.", [s1, s2])
check("derived claim never exceeds weakest source",
      d.certainty == SUPPORTED, certainty_name(d.certainty))
check("derived origin is the union", set(d.origin) == {"ci-1", "git-1"}, str(d.origin))

m = mention(s1)
check("mention does not transmit certainty", m.transmits_certainty is False)
check("mention records referenced grade", m.referenced_certainty == PROVEN)


# ---------------------------------------------------------------------------
# 6. Lesson quarantine: one bad claim never launders its neighbors
# ---------------------------------------------------------------------------

good_claim = Claim(id="lc1", text="The gate caught the bad merge.",
                   certainty=SUPPORTED,
                   support=SupportSet("AND", [SupportItem("gate-log", 0.9)]),
                   origin=("gate-log",))
bad_claim = Claim(id="lc2", text="All merges are now safe.",
                  certainty=SUPPORTED,
                  support=SupportSet("AND", []),  # no support: unsupported fact
                  origin=(), quantifier="all")
broken_claim = Claim(id="lc3", text="The connector writes to production.",
                     certainty=SUPPORTED,
                     support=SupportSet("AND", [SupportItem("audit-3", 0.9)]),
                     origin=("audit-3",), negated=False)
verdicts = {
    "lc1": ExtractionVerdict("lc1", True, []),
    "lc2": ExtractionVerdict("lc2", True, []),
    "lc3": ExtractionVerdict("lc3", False, ["NEGATION_DROPPED"]),
}
audit = audit_lesson([good_claim, bad_claim, broken_claim], verdicts)
check("mixed-validity lesson keeps its good claims",
      [c.id for c in audit.kept] == ["lc1"], str([c.id for c in audit.kept]))
check("bad claims quarantined with reasons", len(audit.quarantined) == 2,
      str([(c.id, r) for c, r in audit.quarantined]))
check("extraction failure named", any("NEGATION_DROPPED" in r for _, r in audit.quarantined))
check("unsupported fact named", any("UNSUPPORTED_FACT" in r for _, r in audit.quarantined))

# Independent alternatives survive unrelated compromise.
alt_a = Claim(id="altA", text="Approach A works.", certainty=SUPPORTED,
              support=SupportSet("AND", [SupportItem("exp-A", 0.85)]), origin=("exp-A",))
alt_b = Claim(id="altB", text="Approach B works.", certainty=SUPPORTED,
              support=SupportSet("AND", [SupportItem("exp-B", 0.85)]), origin=("exp-B",))
survivors = survives_compromise([alt_a, alt_b], {"altA"})
check("independent alternative survives unrelated compromise",
      [c.id for c in survivors] == ["altB"], str([c.id for c in survivors]))

# Shared-evidence claims fall together (honest, not over-broad).
dep = Claim(id="depC", text="Follows from A.", certainty=SUPPORTED,
            support=SupportSet("AND", [SupportItem("exp-A", 0.7)]), origin=("exp-A",))
survivors = survives_compromise([alt_a, alt_b, dep], {"altA"})
check("shared-evidence dependent does not survive",
      [c.id for c in survivors] == ["altB"], str([c.id for c in survivors]))


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

print(f"PASS: {len(PASS)}  FAIL: {len(FAIL)}")
for f in FAIL:
    print("FAILED:", f)
sys.exit(1 if FAIL else 0)
