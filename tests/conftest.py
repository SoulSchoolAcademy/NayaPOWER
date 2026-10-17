"""Shared fixtures for the readiness-instrument test suite.

The instrument carries module-level API-economy state (_LOCAL_ONLY,
_MAX_API_CALLS, _api_call_count). Every test starts from a known,
effectively-unbounded budget so unit tests (which monkeypatch gh_get with
fakes) can never trip the production budget cap, and no test leaks flag
state into another.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import production_readiness_checklist as prc  # noqa: E402


@pytest.fixture(autouse=True)
def _reset_api_economy():
    prc._LOCAL_ONLY = False
    prc._MAX_API_CALLS = 10 ** 9
    prc._api_call_count = 0
    yield
    prc._LOCAL_ONLY = False
    prc._MAX_API_CALLS = 10  # the module default / per-run REST budget
    prc._api_call_count = 0
