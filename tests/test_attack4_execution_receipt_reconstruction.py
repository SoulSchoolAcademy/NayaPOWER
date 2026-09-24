from pathlib import Path

SOURCE = Path('supabase/functions/nayanet-compound-intelligence/index.ts')
RPC = Path('supabase/migrations/20260920030000_repair_cognition_event_receipt_lineage.sql')
AUTH_MIG = Path('supabase/migrations/20260918170000_authority_grant_runtime_v1.sql')


def body():
    text = SOURCE.read_text(encoding='utf-8')
    start = text.index('async function commitIntelligence')
    end = text.index('\nasync function health', start)
    return text[start:end]


def test_commit_requires_execution_authorization_lineage():
    b = body()
    assert 'execution_authorization' in b
    for field in ('decision_id', 'action_id', 'binding_hash', 'governance_state'):
        assert f'executionAuthorization.{field}' in b, f'missing ExecutionAuthorization field: {field}'
    assert 'EXECUTION_AUTHORIZATION_REQUIRED' in b


def test_commit_binds_execution_lineage_before_persistence():
    b = body()
    auth_pos = b.index('const executionAuthorization')
    persist_pos = b.index('captureReceipt=await record')
    validation_pos = b.index('nayanet_validate_authority_grant')
    assert validation_pos < persist_pos
    assert auth_pos < persist_pos
    for field in ('decision_id','action_id','binding_hash','governance_state'):
        assert f'{field}:executionAuthorization.{field}' in b, f'commit does not bind execution {field}'


def test_receipt_schema_has_reconstructable_execution_lineage():
    r = Path('supabase/migrations/20260924090000_bind_execution_lineage_into_cognition_receipts.sql').read_text(encoding='utf-8')
    assert "'execution_lineage'" in r
    assert "p_event->'metadata'->'execution_lineage'" in r
    b = body()
    for field in ('decision_id','action_id','binding_hash','governance_state'):
        assert f'{field}:executionAuthorization.{field}' in b
    assert 'authority_grant_id' in r
    assert 'authority_scope' in r
    assert 'authority_actions' in r
