import { execSync } from 'node:child_process';
import fs from 'node:fs';

const expected = process.env.EXPECTED_SHA || process.env.GITHUB_SHA || '';
const actual = execSync('git rev-parse HEAD', { encoding: 'utf8' }).trim();
const branch = execSync('git branch --show-current', { encoding: 'utf8' }).trim();
const deployed = process.env.DEPLOYED_SOURCE_SHA || '';
const live = process.env.LIVE_ARTIFACT_SHA || '';

const proof = {
  schema_version: 'NAYANET_CURRENT_SOURCE_IDENTITY_PROOF_V1',
  expected_sha: expected,
  checked_out_sha: actual,
  checked_out_branch: branch,
  deployed_source_sha: deployed || null,
  live_artifact_sha: live || null,
  source_match: expected === actual,
  deployment_source_match: !deployed || deployed === actual,
  status: expected && expected === actual && (!deployed || deployed === actual) ? 'VERIFIED' : 'FAILED'
};

fs.writeFileSync('current-source-identity-proof.json', JSON.stringify(proof, null, 2) + '\\n');
console.log(JSON.stringify(proof));
if (proof.status !== 'VERIFIED') process.exit(1);
