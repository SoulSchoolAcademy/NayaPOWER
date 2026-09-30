import json
import os
from pathlib import Path
import re
from textwrap import dedent
from unittest.mock import patch

import pytest

@pytest.fixture(autouse=True)
def isolated_output(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

ROOT=Path(__file__).resolve().parents[1]
SHA='a'*40

def ci_program():
    text=(ROOT/'.github/workflows/governed-supabase-production-deploy.yml').read_text()
    snippets=re.findall(r"          python - <<'PY'\n(.*?)\n          PY",text,re.S)
    return dedent(next(s for s in snippets if 'for attempt in range(90)' in s))

def run_ci(**overrides):
    def api(args,**kwargs):
        endpoint=args[-1]
        if '/check-runs' in endpoint:
            return json.dumps({'check_runs':[{'name':'test','status':'completed','conclusion':'success'}]})
        workflow='kernel-tests.yml' if 'kernel-tests.yml' in endpoint else 'collective-chain-readiness-gate.yml'
        record=dict(id=1,head_sha=SHA,head_branch='main',event='push',status='completed',conclusion='success',
                    path='.github/workflows/'+workflow,run_attempt=1)
        record.update(overrides)
        return json.dumps({'workflow_runs':[record]})
    with patch('subprocess.check_output',api),patch('time.sleep',lambda _:None),patch.dict(os.environ,REPO='SoulSchoolAcademy/NayaPOWER',GITHUB_SHA=SHA):
        exec(compile(ci_program(),'governed-workflow-ci','exec'),{})

def test_real_workflow_uses_exact_workflow_runs_instead_of_job_check_names():
    run_ci()

@pytest.mark.parametrize('overrides', [dict(head_sha='b'*40),dict(event='pull_request'),dict(head_branch='other'),
                                       dict(status='in_progress'),dict(conclusion='failure'),dict(conclusion='skipped')])
def test_real_workflow_never_accepts_wrong_or_unfinished_ci_evidence(overrides):
    with pytest.raises(SystemExit):
        run_ci(**overrides)


def delta_program():
    source = (ROOT/'.github/workflows/governed-supabase-production-deploy.yml').read_text()
    return dedent(re.search(r"          python - <<'PYCODE'\n(.*?)\n          PYCODE", source, re.S).group(1))


def test_full_undeployed_delta_includes_protected_changes_from_earlier_pushes():
    base = 'b'*40
    Path('production-runtime-source.ts').write_text('const DEPLOYED_SOURCE_REVISION = "'+base+'";')
    with patch('subprocess.run') as ancestry, patch('subprocess.check_output', return_value='supabase/migrations/security.sql\nsupabase/functions/example/index.ts\n') as diff, patch.dict(os.environ, GITHUB_SHA=SHA):
        exec(compile(delta_program(), 'governed-workflow-delta', 'exec'), {})
    ancestry.assert_called_once_with(['git','merge-base','--is-ancestor',base,SHA], check=True)
    diff.assert_called_once_with(['git','diff','--name-only',base,SHA],text=True)
    assert json.loads(Path('standing-changed-paths.json').read_text())[0] == 'supabase/migrations/security.sql'


@pytest.mark.parametrize('source', ['const DEPLOYED_SOURCE_REVISION = "UNSTAMPED";', ''])
def test_missing_production_provenance_refuses_before_diff(source):
    Path('production-runtime-source.ts').write_text(source)
    with patch('subprocess.check_output') as diff, pytest.raises(SystemExit, match='provenance missing'):
        exec(compile(delta_program(), 'governed-workflow-delta', 'exec'), {})
    diff.assert_not_called()
