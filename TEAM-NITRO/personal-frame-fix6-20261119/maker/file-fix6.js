// File the Personal Frame FIX-6 bytes to NEW branch personal/frame-round-fix6-20261119.
// Bytes built in memory via edit-fix6.js transform() on the API-fetched base
// blob -- no local 10MB write (EPERM flake). Verifies three ways.
const { execFileSync } = require('child_process');
const crypto = require('crypto');
const os = require('os');
const { transform, fetchBase } = require('./edit-fix6.js');

const APP_ID = process.env.GITHUB_APP_ID || '5198315';
const INSTALLATION_ID = process.env.GITHUB_APP_INSTALLATION_ID || '168168354';
const PEM_PATH = (process.env.GITHUB_APP_PEM || '~/.config/nayapower/github-app.pem').replace(/^~/, os.homedir());
const BASE = 'https://api.github.com';
const REPO = 'SoulSchoolAcademy/NayaPOWER';
const FILE_PATH = 'TEAM-NITRO/personal-page-complete-20261113/personal-complete.html';
const BASE_TIP = '04715a7f8fc7dbd885b05401c1fb6b1839aa7811';
const BASE_BLOB = 'dedf0b19057b4396572d8b1963352f0744c32439';
const NEW_BRANCH = 'personal/frame-round-fix6-20261119';

function b64url(buf) { return Buffer.from(buf).toString('base64url'); }
function mintJwt() {
  const now = Math.floor(Date.now() / 1000);
  const header = b64url(JSON.stringify({ alg: 'RS256', typ: 'JWT' }));
  const payload = b64url(JSON.stringify({ iat: now - 60, exp: now + 600, iss: APP_ID }));
  const input = `${header}.${payload}`;
  const sig = execFileSync('openssl', ['dgst', '-sha256', '-sign', PEM_PATH], { input });
  return `${input}.${b64url(sig)}`;
}
async function gh(method, path, token, body) {
  const res = await fetch(BASE + path, {
    method,
    headers: {
      Accept: 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28',
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
      'User-Agent': 'muse-github-skill/1.0',
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  return { status: res.status, text };
}

async function main() {
  const base = fetchBase();
  const out = transform(base);
  const raw = Buffer.from(out, 'latin1');
  const sha256 = crypto.createHash('sha256').update(raw).digest('hex');
  const gitSha = crypto.createHash('sha1').update(`blob ${raw.length}\0`).update(raw).digest('hex');
  console.log(JSON.stringify({ newSize: raw.length, newSha256: sha256, newGitBlobSha1: gitSha }));

  const jwt = mintJwt();
  const tok = await gh('POST', `/app/installations/${INSTALLATION_ID}/access_tokens`, jwt, {});
  if (tok.status !== 201) { console.error('token exchange failed', tok.status, tok.text.slice(0, 300)); process.exit(1); }
  const token = JSON.parse(tok.text).token;

  const pre = await gh('GET', `/repos/${REPO}/git/refs/heads/${NEW_BRANCH}`, token);
  console.log(JSON.stringify({ branchPrecheckStatus: pre.status }));
  if (pre.status === 200) { console.error('BRANCH ALREADY EXISTS -- refusing to reuse', pre.text.slice(0, 300)); process.exit(1); }

  const ref = await gh('POST', `/repos/${REPO}/git/refs`, token, { ref: `refs/heads/${NEW_BRANCH}`, sha: BASE_TIP });
  if (ref.status !== 201) { console.error('branch create failed', ref.status, ref.text.slice(0, 500)); process.exit(1); }
  console.log(JSON.stringify({ branchCreated: true, sha: JSON.parse(ref.text).object.sha }));

  const put = await gh('PUT', `/repos/${REPO}/contents/${FILE_PATH}`, token, {
    message: 'Personal Frame Fix-6 Round (2026-11-19): Ask Naya button opens the room — popstate handler no longer routes Hub-room hashes through showView(home) F3 yield',
    content: raw.toString('base64'),
    branch: NEW_BRANCH,
    sha: BASE_BLOB,
  });
  if (put.status !== 200 && put.status !== 201) {
    console.error('contents PUT failed', put.status, put.text.slice(0, 800)); process.exit(1);
  }
  const putJson = JSON.parse(put.text);
  console.log(JSON.stringify({
    filed: true,
    commitSha: putJson.commit.sha,
    contentSha: putJson.content.sha,
    contentSize: putJson.content.size,
    contentPath: putJson.content.path,
  }));

  const branch = await gh('GET', `/repos/${REPO}/branches/${NEW_BRANCH}`, token);
  const branchJson = JSON.parse(branch.text);
  console.log(JSON.stringify({ verifyBranchTip: branchJson.commit.sha, tipIsFiledCommit: branchJson.commit.sha === putJson.commit.sha }));
  const blob = await gh('GET', `/repos/${REPO}/git/blobs/${putJson.content.sha}`, token);
  const blobJson = JSON.parse(blob.text);
  const blobRaw = Buffer.from(blobJson.content.replace(/\s/g, ''), 'base64');
  console.log(JSON.stringify({
    verifyBlobSha: blobJson.sha,
    verifyBlobSize: blobRaw.length,
    verifyBlobSha256: crypto.createHash('sha256').update(blobRaw).digest('hex'),
    sizeMatchesLocal: blobRaw.length === raw.length,
    sha256MatchesLocal: crypto.createHash('sha256').update(blobRaw).digest('hex') === sha256,
    bytesIdentical: blobRaw.equals(raw),
  }));
  const commit = await gh('GET', `/repos/${REPO}/git/commits/${putJson.commit.sha}`, token);
  const commitJson = JSON.parse(commit.text);
  console.log(JSON.stringify({ commitParents: (commitJson.parents || []).map((p) => p.sha), parentIsBaseTip: (commitJson.parents || []).length === 1 && commitJson.parents[0].sha === BASE_TIP }));
}
main().catch((e) => { console.error('FATAL', e.message); process.exit(1); });
