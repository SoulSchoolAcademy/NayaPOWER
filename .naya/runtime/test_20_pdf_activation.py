#!/usr/bin/env python3
"""Acceptance tests for the 20-PDF zero-setup activation path."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location("activation_engine", Path(__file__).with_name("activation_engine.py"))
activation = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = activation
assert spec.loader is not None
spec.loader.exec_module(activation)
contract = __import__("activation_contract")

PACKAGE = "NAYA-ACTIVATION-20PDF-TEST"


def manifest(count: int = 20):
    return {
        "schema_version": 1,
        "package_id": PACKAGE,
        "package_version": "1.0.0",
        "north_star": "Turn a 20-document knowledge package into deterministic, recoverable canonical memory with zero external vector infrastructure.",
        "documents": [
            {
                "document_id": f"PDF-{i:02d}",
                "version": "1.0.0",
                "package_id": PACKAGE,
                "order": i,
                "purpose": f"Knowledge source {i}",
                "content": f"Extracted text for PDF {i}. This fixture represents text produced by the PDF extraction boundary."
            }
            for i in range(1, count + 1)
        ],
    }


def test_exactly_twenty_documents_are_ready():
    data = manifest(20)
    assert contract.validate_20_pdf_manifest(data) == []
    result = activation.inspect_package(data)
    assert result["status"] == "READY"
    assert result["document_count"] == 20
    assert len(result["documents"]) == 20
    assert all(item["chunk_count"] >= 1 for item in result["documents"])


def test_nineteen_documents_are_rejected_by_20_pdf_boundary():
    assert contract.validate_20_pdf_manifest(manifest(19))


def test_twenty_one_documents_are_rejected_by_20_pdf_boundary():
    assert contract.validate_20_pdf_manifest(manifest(21))


def test_duplicate_content_identity_is_rejected():
    data = manifest(20)
    data["documents"][1]["content"] = data["documents"][0]["content"]
    result = activation.inspect_package(data)
    assert result["status"] == "CONFLICT"


def test_missing_document_order_is_rejected_by_20_pdf_boundary():
    data = manifest(20)
    data["documents"][10]["order"] = 21
    assert contract.validate_20_pdf_manifest(data)


def test_identity_changes_when_content_changes():
    first = activation.prepare_document(manifest(20)["documents"][0])[0]
    changed = manifest(20)["documents"][0]
    changed["content"] += " changed"
    second = activation.prepare_document(changed)[0]
    assert first.identity != second.identity


def test_baseline_activation_requires_no_vector_store():
    schema = contract.activation_result_schema()
    assert "future_vector_index" in schema["derived_representations"]
    assert "no vector store required for baseline activation" in schema["prohibitions"]


if __name__ == "__main__":
    tests = [value for name, value in globals().items() if name.startswith("test_")]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS {len(tests)} 20-PDF activation tests")
