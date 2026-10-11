"""
observation_window.py — T-07: delayed-harm observation windows with stop conditions.

Per Naya 1's Law 11 enforcement intel ("Do-No-Harm: Intelligent Risk Under
Uncertainty"): harm comes in four types requiring different safeguards —
uncertain, asymmetric, DELAYED, difficult-to-measure. For delayed harm, the
safeguard is:

    "Observation windows + stop conditions established BEFORE execution.
     Monitoring failure = pause rollout. Contradictory later evidence
     reopens outcomes."

This module is the machine form of that safeguard. It does not duplicate
Law 11's typed-action gate (typed_action.py) or the value calculus: it
extends them with a time dimension — what must be watched AFTER a
consequential action executes, and what stops the rollout when the
watching fails or the evidence turns.

GOVERNING SENTENCE (Naya 1): "When harm is delayed, continue observing."

SEAM CONTRACTS (neighboring lanes — do not duplicate):
  - T-05 (harm profile, 5 dimensions S/P/I/T/U/E per group): feeds the
    `harm_type` label and the indicator bands. This module takes the label
    as a plain string; the structured profile is T-05's lane.
  - T-06 (neutrality trap, six-state findings): indicator readings are
    never collapsed to "neutral" here — an unread indicator is UNMEASURED,
    not zero, and missing reports PAUSE rather than pass.
  - Law 12 (proofs expire): a REOPEN verdict from review() is the input
    Law 12's revalidation consumes. This module emits REOPEN; Law 12's
    lane decides the revalidation consequence.

RULES ENFORCED:
  1. The window is declared BEFORE execution. A window whose declared_at
     postdates the plan is invalid — observation cannot be invented
     retroactively. (Fail closed: missing window -> execution refused.)
  2. Every window names its indicators, review dates, and stop triggers
     upfront. A window missing any of the three is invalid at plan time.
  3. Monitoring failure = pause. If a review date passes with no
     observation report, the window PAUSES and execution/continuation is
     refused until observations resume.
  4. Stop triggers are machine-checkable. A fired trigger STOPS the
     window (terminal); nothing resumes it.
  5. Contradictory later evidence reopens the outcome. Readings outside
     the expected band — but below any stop trigger — return REOPEN: the
     status stays ACTIVE, but the verdict demands revalidation.
  6. Evidence never creates authority (Naya 1's ninth framework): a clean
     observation record does not grant new permissions; it only clears
     the observation door.
"""
from __future__ import annotations

from dataclasses import dataclass, field


# --- Harm types (Naya 1's four-type taxonomy). Plain labels here; the
# structured per-group profile is T-05's lane. -------------------------------
HARM_UNCERTAIN = "uncertain"
HARM_ASYMMETRIC = "asymmetric"
HARM_DELAYED = "delayed"
HARM_DIFFICULT_TO_MEASURE = "difficult_to_measure"
HARM_TYPES = frozenset({
    HARM_UNCERTAIN, HARM_ASYMMETRIC, HARM_DELAYED,
    HARM_DIFFICULT_TO_MEASURE,
})

# --- Window statuses ----------------------------------------------------------
STATUS_ACTIVE = "ACTIVE"
STATUS_PAUSED = "PAUSED"      # monitoring failure — rollout paused
STATUS_STOPPED = "STOPPED"    # stop trigger fired — terminal
STATUS_COMPLETED = "COMPLETED"  # window_end reached with clean record

# --- Review verdicts ----------------------------------------------------------
VERDICT_CONTINUE = "CONTINUE"
VERDICT_PAUSE = "PAUSE"
VERDICT_STOP = "STOP"
VERDICT_REOPEN = "REOPEN"     # contradictory evidence — revalidate
VERDICT_COMPLETE = "COMPLETE"

# --- Execution-door codes (mirrored into act_pipeline's code vocabulary) ------
OBSERVATION_WINDOW_REQUIRED = "OBSERVATION_WINDOW_REQUIRED"
OBSERVATION_WINDOW_INVALID = "OBSERVATION_WINDOW_INVALID"
OBSERVATION_WINDOW_MISSING = "OBSERVATION_WINDOW_MISSING"
OBSERVATION_REGISTRY_UNAVAILABLE = "OBSERVATION_REGISTRY_UNAVAILABLE"
OBSERVATION_PAUSED = "OBSERVATION_PAUSED"
OBSERVATION_STOPPED = "OBSERVATION_STOPPED"

DIRECTION_ABOVE = "above"
DIRECTION_BELOW = "below"


@dataclass(frozen=True)
class ObservationIndicator:
    """One thing to watch, with its expected band.

    name: machine key, e.g. "error_rate_5xx".
    low/high: the expected band. A reading outside the band is
      contradictory evidence (REOPEN) unless a stop trigger fires first.
      The band is set BEFORE execution — never tuned post-hoc to fit data.
    unit: human label, e.g. "errors/min". Informational only.
    """
    name: str
    low: float
    high: float
    unit: str = ""


@dataclass(frozen=True)
class StopTrigger:
    """A machine-checkable stop condition.

    name: human label, e.g. "error spike".
    indicator: key into the window's indicators.
    threshold: the trip value.
    direction: "above" (reading > threshold fires) or "below".
    When fired the window STOPS and the rollout halts. Terminal.
    """
    name: str
    indicator: str
    threshold: float
    direction: str = DIRECTION_ABOVE


@dataclass(frozen=True)
class ObservationWindow:
    """The upfront declaration for a consequential rollout.

    Declared at plan time, enforced at execution time and at every review
    date. All three pillars — indicators, review dates, stop triggers —
    are named here, before execution. None may be added later to excuse
    what already happened.
    """
    window_id: str
    action: str               # the action this window observes
    actor_id: str
    declared_at: float        # epoch seconds; must be <= plan time
    window_end: float         # epoch seconds; must be > declared_at
    review_dates: tuple[float, ...]  # scheduled review points, ascending
    indicators: tuple[ObservationIndicator, ...]
    stop_triggers: tuple[StopTrigger, ...]
    harm_type: str = HARM_DELAYED
    status: str = STATUS_ACTIVE
    notes: str = ""


@dataclass(frozen=True)
class ObservationReport:
    """One observation round: readings for (some of) the indicators.

    readings: indicator name -> measured value. A missing indicator is
      UNMEASURED, never zero — the neutrality trap (T-06) applies: an
      unmeasured indicator cannot clear a review date.
    """
    readings: dict = field(default_factory=dict)
    notes: str = ""


@dataclass(frozen=True)
class ReviewVerdict:
    """Outcome of reviewing a window at one point in time."""
    verdict: str
    window_id: str
    status: str               # resulting status after this review
    reasons: tuple[str, ...] = ()
    review_dates_due: tuple[float, ...] = ()


def validate_window(window: ObservationWindow, *, action: str,
                    now: float) -> tuple[bool, tuple[str, ...]]:
    """Validate a window declaration at plan time. Fail closed.

    Checks (all must hold):
      - window.action matches the planned action (bound to this rollout)
      - declared_at <= now (declared before/already at plan time — never future)
      - window_end > now (the window lies ahead, not behind)
      - harm_type is a known label
      - review_dates non-empty, ascending, each > declared_at and <= window_end
      - indicators non-empty, unique names, low <= high
      - stop_triggers non-empty, unique names, each references a known
        indicator, direction in {above, below}
    """
    problems: list[str] = []
    if window.action != action:
        problems.append(f"ACTION_MISMATCH:{window.action!r}!={action!r}")
    if window.declared_at > now:
        problems.append("DECLARED_IN_FUTURE")
    if window.window_end <= now:
        problems.append("WINDOW_END_NOT_IN_FUTURE")
    if window.harm_type not in HARM_TYPES:
        problems.append(f"UNKNOWN_HARM_TYPE:{window.harm_type!r}")
    if not window.review_dates:
        problems.append("NO_REVIEW_DATES")
    else:
        prev = None
        for d in window.review_dates:
            if prev is not None and d <= prev:
                problems.append("REVIEW_DATES_NOT_ASCENDING")
                break
            prev = d
            if d <= window.declared_at:
                problems.append(f"REVIEW_DATE_NOT_AFTER_DECLARATION:{d}")
            if d > window.window_end:
                problems.append(f"REVIEW_DATE_AFTER_WINDOW_END:{d}")
    if not window.indicators:
        problems.append("NO_INDICATORS")
    else:
        names = [i.name for i in window.indicators]
        if len(set(names)) != len(names):
            problems.append("DUPLICATE_INDICATOR_NAMES")
        for i in window.indicators:
            if not i.name:
                problems.append("EMPTY_INDICATOR_NAME")
            if i.low > i.high:
                problems.append(f"INVERTED_INDICATOR_BAND:{i.name}")
    if not window.stop_triggers:
        problems.append("NO_STOP_TRIGGERS")
    else:
        tnames = [t.name for t in window.stop_triggers]
        if len(set(tnames)) != len(tnames):
            problems.append("DUPLICATE_TRIGGER_NAMES")
        known = {i.name for i in window.indicators}
        for t in window.stop_triggers:
            if t.indicator not in known:
                problems.append(f"TRIGGER_UNKNOWN_INDICATOR:{t.name}->{t.indicator}")
            if t.direction not in (DIRECTION_ABOVE, DIRECTION_BELOW):
                problems.append(f"TRIGGER_BAD_DIRECTION:{t.name}")
    return (not problems, tuple(problems))


class ObservationRegistry:
    """The live record of observation windows.

    The registry is the authority on window state: status transitions
    happen ONLY through review(). There is no setter for status — a
    paused window cannot be forged back to ACTIVE by writing a field.
    """

    def __init__(self) -> None:
        self._windows: dict[str, ObservationWindow] = {}
        # window_id -> {review_date: ObservationReport} — the observation record
        self._reports: dict[str, dict[float, ObservationReport]] = {}

    def declare(self, window: ObservationWindow) -> None:
        """Register a window. Raises ValueError on duplicate window_id.

        Declaration does NOT validate the window's contents — validation
        is the plan gate's job (validate_window). The registry records
        what was declared, when.
        """
        if window.window_id in self._windows:
            raise ValueError(f"duplicate window_id: {window.window_id!r}")
        self._windows[window.window_id] = window
        self._reports[window.window_id] = {}

    def get(self, window_id: str) -> ObservationWindow | None:
        return self._windows.get(window_id)

    def due_review_dates(self, window_id: str, now: float) -> tuple[float, ...]:
        """Review dates at or before now with no report yet."""
        window = self._windows.get(window_id)
        if window is None:
            return ()
        reported = self._reports[window_id]
        return tuple(d for d in window.review_dates
                     if d <= now and d not in reported)

    def _transition(self, window: ObservationWindow,
                    status: str) -> ObservationWindow:
        updated = ObservationWindow(
            window_id=window.window_id, action=window.action,
            actor_id=window.actor_id, declared_at=window.declared_at,
            window_end=window.window_end, review_dates=window.review_dates,
            indicators=window.indicators, stop_triggers=window.stop_triggers,
            harm_type=window.harm_type, status=status, notes=window.notes,
        )
        self._windows[window.window_id] = updated
        return updated

    def _evaluate_report(self, window: ObservationWindow,
                         report: ObservationReport
                         ) -> tuple[str, tuple[str, ...]]:
        """Evaluate one report: STOP > REOPEN > CONTINUE.

        Stop triggers are checked first (terminal). Readings outside the
        expected band — without a fired trigger — are contradictory
        evidence (REOPEN). Unmeasured indicators (missing from readings)
        are UNMEASURED, never zero, and never clear anything.
        """
        stop_reasons: list[str] = []
        reopen_reasons: list[str] = []
        bands = {i.name: i for i in window.indicators}
        for trigger in window.stop_triggers:
            if trigger.indicator not in report.readings:
                continue  # unmeasured: cannot fire, cannot clear (T-06)
            reading = report.readings[trigger.indicator]
            fired = (reading > trigger.threshold
                     if trigger.direction == DIRECTION_ABOVE
                     else reading < trigger.threshold)
            if fired:
                stop_reasons.append(
                    f"STOP_TRIGGER_FIRED:{trigger.name} "
                    f"({trigger.indicator}={reading} "
                    f"{trigger.direction} {trigger.threshold})"
                )
        if stop_reasons:
            return VERDICT_STOP, tuple(stop_reasons)
        for name, reading in report.readings.items():
            band = bands.get(name)
            if band is None:
                continue  # unknown indicator: recorded, not judged
            if reading < band.low or reading > band.high:
                reopen_reasons.append(
                    f"CONTRADICTORY_EVIDENCE:{name}={reading} "
                    f"outside expected [{band.low}, {band.high}]"
                )
        if reopen_reasons:
            return VERDICT_REOPEN, tuple(reopen_reasons)
        return VERDICT_CONTINUE, ()

    def review(self, window_id: str, now: float,
               report: ObservationReport | None = None
               ) -> ReviewVerdict:
        """Review a window at `now`, optionally filing an observation report.

        Semantics (fail closed throughout):
          - Unknown window -> PAUSE verdict (cannot verify: refuse to continue).
          - STOPPED window -> STOP verdict (terminal; nothing resumes it).
          - Review date due and no report filed -> PAUSE
            ("monitoring failure = pause rollout").
          - Report filed -> triggers evaluated: fired -> STOP (terminal);
            contradictory readings -> REOPEN (status stays ACTIVE);
            clean -> CONTINUE.
          - now >= window_end with status ACTIVE and no due dates -> COMPLETE.
          - A PAUSED window resumes (ACTIVE) only via a filed report that
            evaluates CONTINUE/REOPEN — never by writing status directly.

        The filed report is recorded against the earliest due review date
        (or the latest passed review date when called between dates).
        """
        window = self._windows.get(window_id)
        if window is None:
            return ReviewVerdict(
                verdict=VERDICT_PAUSE, window_id=window_id,
                status=STATUS_PAUSED,
                reasons=(OBSERVATION_WINDOW_MISSING,),
            )
        if window.status == STATUS_STOPPED:
            return ReviewVerdict(
                verdict=VERDICT_STOP, window_id=window_id,
                status=STATUS_STOPPED,
                reasons=("WINDOW_ALREADY_STOPPED",),
            )
        if window.status == STATUS_COMPLETED:
            return ReviewVerdict(
                verdict=VERDICT_COMPLETE, window_id=window_id,
                status=STATUS_COMPLETED,
                reasons=("WINDOW_ALREADY_COMPLETED",),
            )

        due = self.due_review_dates(window_id, now)

        if report is not None:
            # A report with zero readings for known indicators is a
            # monitoring failure, not an observation (T-06: unmeasured is
            # never zero, and an empty report never clears a review date).
            known_names = {i.name for i in window.indicators}
            known_readings = {k: v for k, v in report.readings.items()
                              if k in known_names}
            if not known_readings:
                if due:
                    updated = (window if window.status == STATUS_PAUSED
                               else self._transition(window, STATUS_PAUSED))
                    return ReviewVerdict(
                        verdict=VERDICT_PAUSE, window_id=window_id,
                        status=updated.status,
                        reasons=tuple(
                            "MONITORING_FAILURE:no usable indicator readings "
                            f"for review date {d}" for d in due),
                        review_dates_due=due,
                    )
                # Off-schedule note observing nothing known: nothing to
                # judge, nothing filed.
                return ReviewVerdict(verdict=VERDICT_CONTINUE,
                                     window_id=window_id,
                                     status=window.status, reasons=(),
                                     review_dates_due=due)
            # File the report against the earliest due date, else the
            # latest passed review date (an off-schedule observation).
            target = due[0] if due else max(
                (d for d in window.review_dates if d <= now), default=None)
            if target is not None:
                self._reports[window_id][target] = report
                due = self.due_review_dates(window_id, now)
            verdict, reasons = self._evaluate_report(window, report)
            if verdict == VERDICT_STOP:
                updated = self._transition(window, STATUS_STOPPED)
                return ReviewVerdict(verdict=VERDICT_STOP,
                                     window_id=window_id,
                                     status=updated.status, reasons=reasons,
                                     review_dates_due=due)
            if verdict == VERDICT_REOPEN:
                # Contradictory evidence reopens the outcome; the window
                # stays ACTIVE so observation continues under the flag.
                return ReviewVerdict(verdict=VERDICT_REOPEN,
                                     window_id=window_id,
                                     status=window.status, reasons=reasons,
                                     review_dates_due=due)
            # CONTINUE: a paused window resumes; an active one continues.
            updated = (self._transition(window, STATUS_ACTIVE)
                       if window.status == STATUS_PAUSED else window)
            if now >= window.window_end and not due:
                updated = self._transition(updated, STATUS_COMPLETED)
                return ReviewVerdict(verdict=VERDICT_COMPLETE,
                                     window_id=window_id,
                                     status=updated.status,
                                     reasons=("WINDOW_END_REACHED_CLEAN",),
                                     review_dates_due=due)
            return ReviewVerdict(verdict=VERDICT_CONTINUE,
                                 window_id=window_id,
                                 status=updated.status,
                                 reasons=reasons, review_dates_due=due)

        # No report filed.
        if due:
            # Monitoring failure = pause rollout. Never silently continue.
            updated = (window if window.status == STATUS_PAUSED
                       else self._transition(window, STATUS_PAUSED))
            return ReviewVerdict(
                verdict=VERDICT_PAUSE, window_id=window_id,
                status=updated.status,
                reasons=tuple(f"MONITORING_FAILURE:no report for review date {d}"
                              for d in due),
                review_dates_due=due,
            )
        if now >= window.window_end and window.status == STATUS_ACTIVE:
            updated = self._transition(window, STATUS_COMPLETED)
            return ReviewVerdict(verdict=VERDICT_COMPLETE,
                                 window_id=window_id,
                                 status=updated.status,
                                 reasons=("WINDOW_END_REACHED_CLEAN",))
        return ReviewVerdict(verdict=VERDICT_CONTINUE, window_id=window_id,
                             status=window.status, reasons=(),
                             review_dates_due=due)

    def execution_permitted(self, window_id: str, action: str,
                            now: float) -> tuple[bool, str]:
        """The execution door for observation-bound actions.

        Returns (permitted, code). Code is "" when permitted. Fail closed:
          - unknown window -> (False, OBSERVATION_WINDOW_MISSING)
          - window bound to a different action -> (False, OBSERVATION_WINDOW_INVALID)
          - PAUSED -> (False, OBSERVATION_PAUSED)
          - STOPPED -> (False, OBSERVATION_STOPPED)
          - ACTIVE or COMPLETED -> (True, "")
        """
        window = self._windows.get(window_id)
        if window is None:
            return False, OBSERVATION_WINDOW_MISSING
        if window.action != action:
            return False, OBSERVATION_WINDOW_INVALID
        if window.status == STATUS_PAUSED:
            return False, OBSERVATION_PAUSED
        if window.status == STATUS_STOPPED:
            return False, OBSERVATION_STOPPED
        return True, ""
