from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FUNCTION = ROOT / "supabase/functions/nayanet-compound-intelligence/index.ts"

source = FUNCTION.read_text(encoding="utf-8")

def test_document_distill_adapter_requires_source_and_distillation_contract():
    required = [
        'action === "document_distill"',
        'DOCUMENT_ID_REQUIRED',
        'DOCUMENT_SOURCE_REF_REQUIRED',
        'DOCUMENT_SOURCE_CONTENT_REQUIRED',
        'DOCUMENT_ESSENCE_REQUIRED',
        'DOCUMENT_DOMAIN_REQUIRED',
        'DOCUMENT_TYPE_REQUIRED',
        'AUTHORITY_GRANT_ID_REQUIRED',
        'NAYANET_DOCUMENT_DISTILL_V1',
    ]
    for marker in required:
        assert marker in source, f"missing document-distill contract marker: {marker}"

def test_document_distill_binds_source_hash_and_classification_to_commit():
    required = [
        'const sourceHash = await sha256Hex(sourceContent);',
        'source_type: "document"',
        'document_id: documentId',
        'source_ref: sourceRef',
        'source_hash: sourceHash',
        'distillation: { essence, title, domain, type }',
        'content: essence',
        'category: domain',
        'topic: type',
    ]
    for marker in required:
        assert marker in source, f"missing provenance/classification binding: {marker}"

print("DOCUMENT_DISTILL_CONTRACT: PASS")


def test_retrieve_exposes_canonical_library_projections():
    compound = (ROOT / "supabase/functions/nayanet-compound-intelligence/index.ts").read_text(encoding="utf-8")
    for marker in [
        'library: {',
        'indexes: indexResult.data ?? []',
        'intelligent_blocks: blockResult.data ?? []',
        'nayanet_intelligence_index',
        'nayanet_intelligent_blocks',
    ]:
        assert marker in compound, f"missing retrieval/library marker: {marker}"
