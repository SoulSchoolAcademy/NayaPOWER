from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
RECEIVER=ROOT/'supabase/functions/v7-smart-note-canonical/index.ts'
DISPATCH=ROOT/'supabase/functions/nayanet-github-dispatch/index.ts'
WORKFLOW=ROOT/'.github/workflows/project-canonical-smart-note.yml'
RUNTIME=ROOT/'NAYANET/HUB/public/assistant-runtime.js'

def test_receiver_automatically_authorizes_and_dispatches_canonical_projection():
    s=RECEIVER.read_text(encoding='utf-8')
    required=[
      'nayanet_issue_authority_grant',
      'smart_note_github_projection',
      'nayanet-github-dispatch',
      'operation:"project_smart_note"',
      'authority_grant_id',
      'EXPLICIT_APPROVAL_GRANTED',
    ]
    missing=[x for x in required if x not in s]
    assert not missing, 'receiver is not wired to automatic canonical GitHub projection: '+', '.join(missing)

def test_receiver_does_not_report_smart_link_until_projection_is_verified():
    s=RECEIVER.read_text(encoding='utf-8')
    assert 'PROJECTION_VERIFIED' in s
    assert 'smart_link:null' not in s
    assert 'SMART_NOTE_GITHUB_PROJECTION_FAILED' in s

def test_dispatch_waits_for_exact_transaction_workflow_and_returns_verified_link():
    s=DISPATCH.read_text(encoding='utf-8')
    required=['display_title', 'waitForProjectionWorkflow', 'PROJECTION_VERIFIED', 'transaction_id', 'smart_link']
    missing=[x for x in required if x not in s]
    assert not missing, 'GitHub dispatch bridge is fire-and-forget: '+', '.join(missing)

def test_projection_workflow_run_name_binds_transaction():
    s=WORKFLOW.read_text(encoding='utf-8')
    assert 'run-name:' in s
    assert '${{ inputs.transaction_id }}' in s

def test_client_requires_verified_smart_link_from_receiver():
    s=RUNTIME.read_text(encoding='utf-8')
    assert "data?.smart_link" in s
    assert 'SMART_LINK_VERIFICATION_FAILED' in s
    assert 'github.com/SoulSchoolAcademy/NayaPOWER/blob/main/.naya/memory/smart-notes/' in s
