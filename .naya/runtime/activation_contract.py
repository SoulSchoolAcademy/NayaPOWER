#!/usr/bin/env python3
"""Machine-readable contract for zero-setup NayaPOWER knowledge activation.

The contract is intentionally provider-neutral. Documents are the customer-facing
input; canonical Note Events remain authoritative; chunks, indexes and future
vectors are derived representations.
"""
from __future__ import annotations

from typing import Any

SCHEMA_VERSION = 1
PACKAGE_ID_PREFIX = "NAYA-ACTIVATION"
REQUIRED_DOCUMENT_FIELDS = (
    "document_id", "version", "package_id", "order", "purpose", "content"
)


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if manifest.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version must be 1")
    for key in ("package_id", "package_version", "north_star", "documents"):
        if key not in manifest or manifest.get(key) in (None, "", []):
            errors.append(f"missing {key}")
    documents = manifest.get("documents")
    if not isinstance(documents, list) or not documents:
        errors.append("documents must be a non-empty list")
        return errors
    seen: set[str] = set()
    orders: set[int] = set()
    for i, document in enumerate(documents, 1):
        if not isinstance(document, dict):
            errors.append(f"document {i} must be an object")
            continue
        for key in REQUIRED_DOCUMENT_FIELDS:
            if key not in document or document.get(key) in (None, ""):
                errors.append(f"document {i} missing {key}")
        doc_id = str(document.get("document_id", ""))
        if doc_id in seen:
            errors.append(f"duplicate document_id: {doc_id}")
        seen.add(doc_id)
        order = document.get("order")
        if not isinstance(order, int) or order < 1:
            errors.append(f"document {i} order must be a positive integer")
        elif order in orders:
            errors.append(f"duplicate document order: {order}")
        else:
            orders.add(order)
    return errors


def validate_20_pdf_manifest(manifest: dict[str, Any]) -> list[str]:
    """Validate the fixed-size 20-document activation package boundary."""
    errors = validate_manifest(manifest)
    if errors:
        return errors
    if len(manifest["documents"]) != 20:
        errors.append(f"20-PDF package requires exactly 20 documents; got {len(manifest['documents'])}")
    expected = list(range(1, 21))
    actual = sorted(document.get("order") for document in manifest["documents"])
    if actual != expected:
        errors.append(f"20-PDF package requires document orders 1..20; got {actual}")
    if not str(manifest["package_id"]).startswith(PACKAGE_ID_PREFIX):
        errors.append(f"package_id must start with {PACKAGE_ID_PREFIX}")
    return errors


def activation_result_schema() -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "states": ["READY", "PARTIAL", "VERIFIED", "CONFLICT", "FAILED"],
        "document_identity": "package_id + document_id + version + content_sha256",
        "authoritative_source": "canonical Note Events",
        "derived_representations": ["chunks", "lexical_index", "future_vector_index"],
        "required_outputs": ["activation_state", "activation_receipt", "next_execution"],
        "prohibitions": [
            "no silent duplicate ingestion",
            "no overwrite of conflicting canonical content",
            "no claim of VERIFIED without verification evidence",
            "no vector store required for baseline activation",
        ],
    }
