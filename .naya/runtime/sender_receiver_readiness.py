#!/usr/bin/env python3
"""Sender/receiver readiness acceptance over existing governed action primitives."""
from __future__ import annotations

REQUIRED={"capability","authority","consent","scope","revocation","idempotency","receipt","persistence","retrieval"}

def evaluate(contract: dict) -> dict:
    missing=sorted(REQUIRED-set(contract))
    failures=[]
    if contract.get("capability") is not True: failures.append("CAPABILITY_NOT_PROVEN")
    if contract.get("authority") is not True: failures.append("AUTHORITY_NOT_PROVEN")
    if contract.get("consent") is not True: failures.append("CONSENT_NOT_PROVEN")
    if not contract.get("scope"): failures.append("SCOPE_NOT_DECLARED")
    if contract.get("revocation") is not True: failures.append("REVOCATION_NOT_PROVEN")
    if contract.get("idempotency") is not True: failures.append("IDEMPOTENCY_NOT_PROVEN")
    if contract.get("receipt") is not True: failures.append("RECEIPT_NOT_PROVEN")
    if contract.get("persistence") is not True: failures.append("PERSISTENCE_NOT_PROVEN")
    if contract.get("retrieval") is not True: failures.append("RETRIEVAL_NOT_PROVEN")
    return {"status":"READY" if not missing and not failures else "NOT_READY","missing":missing,"failures":failures}
