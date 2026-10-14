"""Learn-clock — the measurement instrument for near-instant learning.

Spec: learn-clock-spec.md. Eight timestamps, all UTC:
  T0 EVENT → T1 CAPTURED → T2 TRIAGED → T3 DISTILLED → T4 INJECTED →
  T5 APPLIED → T6 VERIFIED → T7 COMPOUNDED.

Learning latency = T6 − T0. Target: a live failure becomes a verified
cold-successor behavior change within 60 minutes.

The clock is append-only evidence, not a framework. Stages must arrive in
order; anything else raises loudly. Missing stages are reported, never
silently skipped.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

STAGES = ["T0_EVENT", "T1_CAPTURED", "T2_TRIAGED", "T3_DISTILLED",
          "T4_INJECTED", "T5_APPLIED", "T6_VERIFIED", "T7_COMPOUNDED"]
N_STAGES = len(STAGES)

DEFAULT_LOG = Path.home() / "workspace" / "_scratch" / "learn-clock" / "learn-clock.jsonl"


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _parse_iso(s):
    return datetime.fromisoformat(s)


class OutOfOrderError(ValueError):
    """A stage arrived out of sequence, or its timestamp regressed."""


class LearnClock:
    def __init__(self, path=DEFAULT_LOG):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _events(self, lesson_id):
        """All events for a lesson, in stage order."""
        if not self.path.exists():
            return []
        evs = []
        with open(self.path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                e = json.loads(line)
                if e["lesson_id"] == lesson_id:
                    evs.append(e)
        evs.sort(key=lambda e: e["stage"])
        return evs

    def emit(self, lesson_id, stage, ts=None):
        """Stamp a stage for a lesson. `stage` is 0-7 (T0..T7).

        `ts` is an ISO UTC string for retroactive reconstruction (the spec's
        bootstrap step); defaults to now. Stages must arrive in order and
        timestamps must not regress — violations raise OutOfOrderError.
        """
        if not isinstance(stage, int) or not 0 <= stage < N_STAGES:
            raise ValueError(f"stage must be 0-{N_STAGES - 1}, got {stage!r}")
        ts = ts or _now_iso()
        prior = self._events(lesson_id)
        expected = prior[-1]["stage"] + 1 if prior else 0
        if stage != expected:
            raise OutOfOrderError(
                f"lesson {lesson_id}: expected {STAGES[expected]} next, "
                f"got {STAGES[stage]}")
        if prior and _parse_iso(ts) < _parse_iso(prior[-1]["ts"]):
            raise OutOfOrderError(
                f"lesson {lesson_id}: timestamp regressed at {STAGES[stage]}")
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps({"lesson_id": lesson_id, "stage": stage,
                                "stage_name": STAGES[stage], "ts": ts}) + "\n")
        return {"lesson_id": lesson_id, "stage": stage,
                "stage_name": STAGES[stage], "ts": ts}

    def status(self, lesson_id):
        """Which stages are hit / missing for a lesson."""
        hit = [e["stage"] for e in self._events(lesson_id)]
        missing = [s for s in range(N_STAGES) if s not in hit]
        return {"lesson_id": lesson_id,
                "hit": [STAGES[s] for s in hit],
                "missing": [STAGES[s] for s in missing],
                "complete_through": STAGES[hit[-1]] if hit else None}

    def _ts(self, lesson_id, stage):
        for e in self._events(lesson_id):
            if e["stage"] == stage:
                return _parse_iso(e["ts"])
        return None

    def _delta_min(self, lesson_id, a, b):
        ta, tb = self._ts(lesson_id, a), self._ts(lesson_id, b)
        if ta is None or tb is None:
            return None
        return (tb - ta).total_seconds() / 60

    def latency(self, lesson_id):
        """Learning latency = T6 − T0 in minutes. None until T6 exists."""
        return self._delta_min(lesson_id, 0, 6)

    def lags(self, lesson_id):
        """The spec's secondary metrics, in minutes (None when unmeasurable)."""
        return {"capture_lag": self._delta_min(lesson_id, 0, 1),
                "injection_lag": self._delta_min(lesson_id, 3, 4),
                "verification_lag": self._delta_min(lesson_id, 5, 6)}

    def meets_target(self, lesson_id, minutes=60):
        """True only when a measured latency is within target. Fail-closed:
        no T6, no claim."""
        lat = self.latency(lesson_id)
        return lat is not None and lat <= minutes


_default = LearnClock()


def emit(lesson_id, stage, ts=None):
    return _default.emit(lesson_id, stage, ts=ts)


def status(lesson_id):
    return _default.status(lesson_id)


def latency(lesson_id):
    return _default.latency(lesson_id)


def lags(lesson_id):
    return _default.lags(lesson_id)


def meets_target(lesson_id, minutes=60):
    return _default.meets_target(lesson_id, minutes=minutes)
