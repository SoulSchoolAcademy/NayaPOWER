"""Fairness measurer — UD-17 "MEASURE FAIRNESS WITH EVIDENCE, NEVER GUESSWORK".

Fairness isn't a feeling — it's measured. Across parties, seats, and decisions,
we track who gets what and whether the distribution matches the stated
principles. Bias is found by the numbers, not by accusation.

Load-bearing rules (from D58-D65, simplified to an operational core):
  1. Only ELIGIBLE_PROVEN records count toward fairness bounds. A worker's own
     "eligible" flag is never enough — eligibility must carry evidence.
  2. ELIGIBILITY_UNDETERMINED records are never auto-eligible or auto-ineligible.
     They stay in the audit trail with a reconstruction obligation.
  3. Fairness debt is computed as bounds over every evidence-compatible history:
     a breach is PROVEN only if it holds under all assignments of the unknowns.
  4. Self-certified eligibility never counts (no circular proof groups).
  5. Small samples are never flagged as bias — thresholds respect sample size.
  6. The report names the pattern, never the person's worth.

Stdlib only.
"""

import hashlib
import json
import math

# ---------------------------------------------------------------- eligibility

ELIGIBLE_PROVEN = "ELIGIBLE_PROVEN"
INELIGIBLE_PROVEN = "INELIGIBLE_PROVEN"
ELIGIBILITY_UNDETERMINED = "ELIGIBILITY_UNDETERMINED"

# Ineligibility reasons that are never accepted as proof on their own:
# "every worker was busy" is contention, and under a capacity-backed
# fair-queue contract contention is precisely why fairness matters.
STARVATION_HIDING_REASONS = {"all_busy", "workers_busy", "contention", "no_capacity"}

OUTCOME_SELECTED = "selected"
OUTCOME_NOT_SELECTED = "not_selected"

DOES_NOT_CLAIM = (
    "What this does NOT claim: this report measures distributions of decisions "
    "against stated principles. It never measures the worth of any person. "
    "A FAIRNESS_DEVIATION flag names a statistical pattern with numbers; it is "
    "not a verdict on anyone's character or intent."
)


# ---------------------------------------------------------------- records

class DecisionRecord:
    """One governed decision, as reconstructed from authoritative records."""

    __slots__ = ("record_id", "decider", "party", "party_entity", "outcome",
                 "value", "principle_id", "eligibility", "eligibility_evidence",
                 "eligibility_reason", "authority_ok")

    def __init__(self, record_id, decider, party, party_entity, outcome,
                 value, principle_id, eligibility,
                 eligibility_evidence=None, eligibility_reason=None,
                 authority_ok=True):
        if eligibility not in (ELIGIBLE_PROVEN, INELIGIBLE_PROVEN,
                               ELIGIBILITY_UNDETERMINED):
            raise ValueError("bad eligibility: %r" % (eligibility,))
        if outcome not in (OUTCOME_SELECTED, OUTCOME_NOT_SELECTED):
            raise ValueError("bad outcome: %r" % (outcome,))
        self.record_id = record_id
        self.decider = decider
        self.party = party                    # label as reported
        self.party_entity = party_entity      # stable underlying entity id
        self.outcome = outcome
        self.value = float(value)
        self.principle_id = principle_id
        self.eligibility = eligibility
        self.eligibility_evidence = list(eligibility_evidence or [])
        self.eligibility_reason = eligibility_reason
        self.authority_ok = bool(authority_ok)

    def to_dict(self):
        return {k: getattr(self, k) for k in self.__slots__}


# ---------------------------------------------------------------- principles

class FairnessPrinciple:
    """The stated principle a distribution is measured against.

    expected_rates maps party label -> expected selection rate, or the string
    "equal" for an equal-share principle. The principle is content-hashed;
    silent bound mutations are rejected at measure time.
    """

    def __init__(self, principle_id, version, expected_rates, min_samples,
                 deviation_threshold, statement):
        self.principle_id = principle_id
        self.version = str(version)
        self.expected_rates = expected_rates
        self.min_samples = int(min_samples)
        self.deviation_threshold = float(deviation_threshold)
        self.statement = statement

    def canonical(self):
        return json.dumps({
            "principle_id": self.principle_id,
            "version": self.version,
            "expected_rates": self.expected_rates,
            "min_samples": self.min_samples,
            "deviation_threshold": self.deviation_threshold,
            "statement": self.statement,
        }, sort_keys=True)

    @property
    def digest(self):
        return hashlib.sha256(self.canonical().encode()).hexdigest()

    def expected_for(self, party, pooled_rate):
        """Expected selection rate for a party.

        "equal" means no party is treated differently from the pooled average
        — the standard equal-treatment reading. An explicit dict names
        per-party expected rates; an unlisted party defaults to the pool.
        """
        if self.expected_rates == "equal":
            return float(pooled_rate)
        return float(self.expected_rates.get(party, pooled_rate))


class PrincipleMutationRejected(Exception):
    """Raised when the principle's bounds were silently mutated."""


class PrincipleRegistry:
    """Governed principle versions. A version bump requires a justification;
    measuring against a mutated-but-unversioned principle is refused."""

    def __init__(self):
        self._versions = {}  # (principle_id, version) -> (digest, justification)

    def register(self, principle, justification):
        if not justification or not justification.strip():
            raise ValueError("principle version changes require a justification")
        key = (principle.principle_id, principle.version)
        self._versions[key] = (principle.digest, justification.strip())

    def check(self, principle):
        key = (principle.principle_id, principle.version)
        if key not in self._versions:
            raise PrincipleMutationRejected(
                "PRINCIPLE_MUTATION_REJECTED: principle %s version %s was never "
                "registered — register it with a justification first."
                % (principle.principle_id, principle.version))
        registered_digest, _ = self._versions[key]
        if registered_digest != principle.digest:
            raise PrincipleMutationRejected(
                "PRINCIPLE_MUTATION_REJECTED: principle %s version %s bounds "
                "differ from the registered digest. Changed fields: %s. "
                "Bump the version with a justification instead of mutating "
                "bounds silently."
                % (principle.principle_id, principle.version,
                   _diff_fields(registered_digest, principle)))


def _diff_fields(registered_digest, principle):
    # We cannot reconstruct the registered canonical form from the digest
    # alone; report the digest mismatch and the live canonical form so the
    # minimal counterexample is the differing bound set itself.
    return "digest %s... != live %s...; live canonical: %s" % (
        registered_digest[:12], principle.digest[:12], principle.canonical())


# ---------------------------------------------------------------- ledger

class FairnessLedger:
    """Append-only ledger of decision records. Records are immutable once
    added; unresolved eligibility stays unresolved here."""

    def __init__(self):
        self._records = []

    def add(self, record):
        if not isinstance(record, DecisionRecord):
            raise TypeError("ledger takes DecisionRecord")
        if any(r.record_id == record.record_id for r in self._records):
            raise ValueError("duplicate record_id: %s" % record.record_id)
        self._records.append(record)

    @property
    def records(self):
        return tuple(self._records)


# ---------------------------------------------------------------- statistics

def wilson_interval(k, n, z=1.96):
    """95% Wilson score interval for a binomial rate. Respects small n:
    wide intervals mean noise is never mistaken for bias."""
    if n <= 0:
        return (0.0, 1.0)
    p = k / n
    denom = 1.0 + z * z / n
    center = (p + z * z / (2.0 * n)) / denom
    half = z * math.sqrt(p * (1.0 - p) / n + z * z / (4.0 * n * n)) / denom
    return (max(0.0, center - half), min(1.0, center + half))


def _is_self_certified(record):
    """Circular proof groups never pass: eligibility whose only evidence is
    the decider's own assertion is not evidence."""
    if not record.eligibility_evidence:
        return True
    return all(
        ref.strip().lower().startswith("self:")
        or ref.strip().lower() in {"decider_assertion", "worker_claimed_eligible"}
        for ref in record.eligibility_evidence
    )


# ---------------------------------------------------------------- measurement

def measure(ledger, principle, registry):
    """Measure the ledger against the principle. Returns a FairnessReport.

    Raises PrincipleMutationRejected on silent bound mutation.
    """
    registry.check(principle)
    records = [r for r in ledger.records
               if r.principle_id == principle.principle_id]

    flags = []
    reconstruction_obligations = []

    # --- eligibility triage ------------------------------------------------
    proven, undetermined, ineligible = [], [], []
    for r in records:
        if r.eligibility == ELIGIBLE_PROVEN:
            if _is_self_certified(r):
                flags.append({
                    "code": "SELF_CERTIFIED_ELIGIBILITY",
                    "record_id": r.record_id,
                    "detail": ("record %s claims ELIGIBLE_PROVEN on the decider's "
                               "own assertion only — demoted to UNDETERMINED; "
                               "circular proof never counts." % r.record_id),
                })
                undetermined.append(r)
                reconstruction_obligations.append(r.record_id)
            elif not r.authority_ok:
                flags.append({
                    "code": "FALSE_ELIGIBILITY",
                    "record_id": r.record_id,
                    "detail": ("record %s counted eligible without authority "
                               "(authority_ok=False) — false eligibility "
                               "without authority; excluded from bounds."
                               % r.record_id),
                })
                ineligible.append(r)
            else:
                proven.append(r)
        elif r.eligibility == ELIGIBILITY_UNDETERMINED:
            undetermined.append(r)
            reconstruction_obligations.append(r.record_id)
        else:
            ineligible.append(r)
            if (r.eligibility_reason in STARVATION_HIDING_REASONS
                    or not r.eligibility_evidence):
                flags.append({
                    "code": "FALSE_INELIGIBILITY_SUSPECT",
                    "record_id": r.record_id,
                    "detail": ("record %s marked ineligible with reason %r and "
                               "no independent evidence — contention is not "
                               "ineligibility; possible hidden starvation."
                               % (r.record_id, r.eligibility_reason)),
                })

    parties = sorted({r.party for r in proven} | {r.party for r in undetermined})
    total_n = len(proven)
    total_k = sum(1 for r in proven if r.outcome == OUTCOME_SELECTED)
    pooled_rate = (total_k / total_n) if total_n else 0.0
    per_party = {}
    for party in parties:
        p_proven = [r for r in proven if r.party == party]
        p_undet = [r for r in undetermined if r.party == party]
        n = len(p_proven)
        k = sum(1 for r in p_proven if r.outcome == OUTCOME_SELECTED)
        u = len(p_undet)
        rate = (k / n) if n else 0.0
        ci_low, ci_high = wilson_interval(k, n)
        expected = principle.expected_for(party, pooled_rate)
        abs_dev = abs(rate - expected)

        if n < principle.min_samples:
            verdict = "INSUFFICIENT_SAMPLE"
        elif (expected < ci_low or expected > ci_high) \
                and abs_dev > principle.deviation_threshold:
            verdict = "FAIRNESS_DEVIATION"
            flags.append({
                "code": "FAIRNESS_DEVIATION",
                "party": party,
                "detail": ("pattern: party %r selected at %.3f (n=%d, 95%% CI "
                           "[%.3f, %.3f]) vs expected %.3f — absolute "
                           "deviation %.3f exceeds threshold %.3f."
                           % (party, rate, n, ci_low, ci_high,
                              expected, abs_dev,
                              principle.deviation_threshold)),
                "numbers": {"observed_rate": round(rate, 4), "expected_rate": round(expected, 4),
                            "ci_low": round(ci_low, 4), "ci_high": round(ci_high, 4),
                            "n": n, "abs_deviation": round(abs_dev, 4)},
            })
        else:
            verdict = "WITHIN_BOUNDS"

        # Fairness-debt bounds over every evidence-compatible history.
        denom = n + u
        rate_min = (k / denom) if denom else 0.0
        rate_max = ((k + u) / denom) if denom else 0.0
        if rate_max < expected - principle.deviation_threshold:
            debt = "BOUNDED_BREACH_PROVEN"
        elif rate_min > expected + principle.deviation_threshold:
            debt = "BOUNDED_BREACH_PROVEN"
        elif (rate_min < expected - principle.deviation_threshold
                or rate_max > expected + principle.deviation_threshold):
            debt = "BOUNDED_BREACH_UNDETERMINED"
        else:
            debt = "NO_BREACH_WITHIN_VERIFIED_INTERVAL"

        values = [r.value for r in p_proven if r.outcome == OUTCOME_SELECTED]
        mean_value = (sum(values) / len(values)) if values else 0.0
        per_party[party] = {
            "n_eligible_proven": n, "n_selected": k,
            "n_undetermined": u, "observed_rate": round(rate, 4),
            "wilson_ci_95": [round(ci_low, 4), round(ci_high, 4)],
            "expected_rate": round(expected, 4),
            "verdict": verdict,
            "debt_bound": debt,
            "debt_interval": [round(rate_min, 4), round(rate_max, 4)],
            "mean_selected_value": round(mean_value, 4),
        }

    # --- value skew: selected, but systematically given scraps ---------------
    selected_means = [(p, s["mean_selected_value"]) for p, s in per_party.items()
                      if s["n_selected"] >= principle.min_samples]
    if len(selected_means) >= 2:
        overall = sum(m for _, m in selected_means) / len(selected_means)
        for party, mean in selected_means:
            dev = abs(mean - overall)
            if dev > principle.deviation_threshold * 10:
                direction = "below" if mean < overall else "above"
                flags.append({
                    "code": "VALUE_SKEW",
                    "party": party,
                    "detail": ("pattern: party %r is selected but its mean "
                               "selected value %.3f sits %.3f %s the overall "
                               "mean %.3f — selection without substance."
                               % (party, mean, dev, direction, overall)),
                    "numbers": {"party_mean_value": round(mean, 4),
                                "overall_mean_value": round(overall, 4),
                                "direction": direction},
                })

    # --- gaming: re-labeling parties --------------------------------------
    entity_labels = {}
    for r in records:
        entity_labels.setdefault(r.party_entity, set()).add(r.party)
    for entity, labels in sorted(entity_labels.items()):
        if len(labels) > 1:
            flags.append({
                "code": "LABEL_SHIFT_GAMING",
                "entity": entity,
                "detail": ("pattern: entity %r appears under %d distinct "
                           "party labels %s — re-labeling to evade measurement."
                           % (entity, len(labels), sorted(labels))),
                "labels": sorted(labels),
            })

    # Split dilution: one entity spread across labels hides entity-level bias.
    entity_stats = {}
    for entity in entity_labels:
        e_proven = [r for r in proven if r.party_entity == entity]
        n = len(e_proven)
        k = sum(1 for r in e_proven if r.outcome == OUTCOME_SELECTED)
        entity_stats[entity] = (n, k)
    if entity_stats:
        avg_rate = sum(k / n for n, k in entity_stats.values() if n) \
            / max(1, sum(1 for n, k in entity_stats.values() if n))
        for entity, (n, k) in sorted(entity_stats.items()):
            if n >= principle.min_samples:
                rate = k / n
                ci_low, ci_high = wilson_interval(k, n)
                if (avg_rate < ci_low or avg_rate > ci_high) \
                        and abs(rate - avg_rate) > principle.deviation_threshold:
                    label_parts = sorted({r.party for r in proven
                                          if r.party_entity == entity})
                    if not any(f.get("party") in label_parts
                               and f["code"] == "FAIRNESS_DEVIATION"
                               for f in flags):
                        flags.append({
                            "code": "SPLIT_DILUTION",
                            "entity": entity,
                            "detail": ("pattern: entity %r deviates at the "
                                       "entity level (rate %.3f, n=%d) while no "
                                       "single label trips — bias diluted "
                                       "across labels %s."
                                       % (entity, rate, n, label_parts)),
                            "numbers": {"entity_rate": round(rate, 4),
                                        "peer_mean_rate": round(avg_rate, 4),
                                        "n": n},
                        })

    return FairnessReport(
        principle_id=principle.principle_id,
        principle_version=principle.version,
        principle_digest=principle.digest,
        per_party=per_party,
        flags=flags,
        reconstruction_obligations=sorted(set(reconstruction_obligations)),
        n_proven=len(proven),
        n_undetermined=len(undetermined),
        n_ineligible=len(ineligible),
    )


class FairnessReport:
    def __init__(self, principle_id, principle_version, principle_digest,
                 per_party, flags, reconstruction_obligations,
                 n_proven, n_undetermined, n_ineligible):
        self.principle_id = principle_id
        self.principle_version = principle_version
        self.principle_digest = principle_digest
        self.per_party = per_party
        self.flags = flags
        self.reconstruction_obligations = reconstruction_obligations
        self.n_proven = n_proven
        self.n_undetermined = n_undetermined
        self.n_ineligible = n_ineligible
        self.does_not_claim = DOES_NOT_CLAIM

    def has_breach(self):
        return any(f["code"] in ("FAIRNESS_DEVIATION", "VALUE_SKEW",
                                 "LABEL_SHIFT_GAMING", "SPLIT_DILUTION",
                                 "FALSE_ELIGIBILITY",
                                 "FALSE_INELIGIBILITY_SUSPECT",
                                 "SELF_CERTIFIED_ELIGIBILITY")
                   for f in self.flags)

    def to_dict(self):
        return {
            "principle": "%s@%s" % (self.principle_id, self.principle_version),
            "principle_digest": self.principle_digest,
            "counts": {"eligible_proven": self.n_proven,
                       "undetermined": self.n_undetermined,
                       "ineligible": self.n_ineligible},
            "per_party": self.per_party,
            "flags": self.flags,
            "reconstruction_obligations": self.reconstruction_obligations,
            "does_not_claim": self.does_not_claim,
        }
