from pathlib import Path

SOURCE = Path('supabase/functions/nayanet-compound-intelligence/index.ts')

def commit_body():
    text = SOURCE.read_text(encoding='utf-8')
    start = text.index('async function commitIntelligence(')
    end = text.index('\nasync function health(', start)
    return text[start:end]

def test_intelligence_commit_requires_authority_before_any_persistence():
    body = commit_body()
    assert 'authority_grant_id' in body, 'intelligence_commit must bind a real authority grant'
    assert 'nayanet_validate_authority_grant' in body, 'intelligence_commit must validate authority at its boundary'
    validate = body.index('nayanet_validate_authority_grant')
    first_persistence = min(i for i in [body.find('await record('), body.find('.insert(')] if i >= 0)
    assert validate < first_persistence, 'authority must be validated before any consequential persistence'

def test_intelligence_commit_cannot_claim_authorized_block_without_authority_lineage():
    body = commit_body()
    auth = body.index('nayanet_validate_authority_grant')
    block = body.index('authority:{state:"AUTHORIZED"')
    assert auth < block, 'authorized intelligent block must be downstream of authority validation'
    assert 'authority_grant_id' in body[auth:block], 'authorized block must carry grant lineage'
