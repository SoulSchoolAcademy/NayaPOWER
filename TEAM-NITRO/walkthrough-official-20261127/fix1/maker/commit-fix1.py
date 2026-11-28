# File FIX1 (small files + rebuild inputs) to branch walkthrough-official-20261127.
# Blobs via gh-app-api ONLY, base64 piped (no multi-MB JSON staged to disk).
# portal.html (47 MB) + worker-consolidated.js (47 MB) are NOT filed: the blobs
# API 422s them ("input too large") — proven this round. They are REBUILDABLE:
# portal-v1.html + build scripts + phone parts + the 14 pictures ARE filed here,
# and the rebuild was proven byte-identical twice locally (portal eb6a2f7e...,
# worker c9560a0e...). Parent = current branch head 512a3bbf....
import json, subprocess, sys
GH = '/home/hatch/workspace/custom-connectors/custom.legacy-github/bin/gh-app-api'
REPO = 'SoulSchoolAcademy/NayaPOWER'
BRANCH = 'walkthrough-official-20261127'
DIR = 'TEAM-NITRO/walkthrough-official-20261127/fix1/maker/'
LANE = '/home/hatch/workspace/team-nitro/walkthrough-official-20261127/fix1/maker/'
def api(method, path, body=None):
    args = [GH, method, path]
    if body is not None:
        args.append('@' + body)
    out = subprocess.run(args, capture_output=True, text=True, timeout=300)
    if out.returncode != 0:
        print('API FAIL', method, path, out.stdout[:500], out.stderr[:500]); sys.exit(1)
    return json.loads(out.stdout)
def blob_for(local):
    # pipe: base64 -> jq -> gh-app-api, no disk staging
    cmd = ("base64 -w0 %s | jq -Rs '{content: ., encoding: \"base64\"}' | %s POST /repos/%s/git/blobs @/dev/stdin" % (local, GH, REPO))
    out = subprocess.run(['bash', '-c', cmd], capture_output=True, text=True, timeout=300)
    if out.returncode != 0:
        print('BLOB FAIL', local, out.stdout[:500], out.stderr[:500]); sys.exit(1)
    return json.loads(out.stdout)['sha']
FILES = ['identity.html', 'identity-consolidated.html', 'worker-meta.json', 'sw.js',
 'build-official.mjs', 'build-worker-official.mjs', 'fix-cert.mjs', 'fix1-cert.mjs', 'commit-fix1.py',
 'phone-section3.html', 'phone-style3.html', 'phone-script3.html', 'steps.js', 'engine.js',
 'media/1_THE_VAULT.jpg', 'media/2_HOW_WE_SNYC.jpg', 'media/3_NANOVERSE.jpg',
 'media/4_HOW_IT_WORKS.jpg', 'media/5_SMART_VAULT.jpg', 'media/6_AUTO_MATCH.jpg',
 'media/7_AUTO_ORGINIZED.jpg', 'media/a3/a3903dafe3e9ee81ac66c6bb14104fdffcd7483550bd521a141f1c1ea6e538c4.png',
 'media/c0/c017eea7acbc2527b07efa2e61e9233bd0fb61f793b45882c7a867c562a0a8b7.png',
 'media/77/7702f98780b5dec46e146997451f61a4172de44cd93dee9fe6ccf1da37a882da.png',
 'media/f0/f0e21717d412807e5ad25bc58ded1b38be42a1b5f872ae27688c5c7daf1dfcef.png',
 'media/b6/b6cfaacab406f5213c1893c6f305b1f910dc1428a78dcb413004e335b7db4bb2.png',
 'media/42/4248188b4ea181ac848b727c30c7671c5243006cda8f62935241fcf2c2a5dae7.png',
 'media/fa/fa45cb8958e4aa3832c2622936988e8955e620a4c40264a0cd5fc5d940f86cfb.png',
 'evidence/probe-fix1.py', 'evidence/probe-fix1.log',
 'evidence/fix1-390-cert.png', 'evidence/fix1-390-g1.png', 'evidence/fix1-390-end.png',
 'evidence/fix1-1440-g1.png', 'evidence/fix1-1440-end.png']
head = api('GET', '/repos/%s/git/refs/heads/%s' % (REPO, BRANCH))
parent = head['object']['sha']
print('branch head:', parent)
base_commit = api('GET', '/repos/%s/git/commits/%s' % (REPO, parent))
base_tree = base_commit['tree']['sha']
print('base tree:', base_tree)
entries = []
# portal-v1.html blob already created + verified this round; reuse it.
entries.append({'path': DIR + 'portal-v1.html', 'mode': '100644', 'type': 'blob',
                'sha': 'a780799aa7a21b42891f0c081445d6a517431c81'})
print('blob portal-v1.html (reused, verified) -> a780799a...')
import os
for f in FILES:
    p = LANE + f
    print('blob', f, os.path.getsize(p), 'B...', flush=True)
    sha = blob_for(p)
    print('  ->', sha)
    entries.append({'path': DIR + f, 'mode': '100644', 'type': 'blob', 'sha': sha})
open('/tmp/fix1-tree.json', 'w').write(json.dumps({'base_tree': base_tree, 'tree': entries}))
tree = api('POST', '/repos/%s/git/trees' % REPO, '/tmp/fix1-tree.json')
print('tree:', tree['sha'])
msg = ("Official walkthrough FIX1 2026-11-27 (staged only, nothing live)\n\n"
 "Fixes the checker's six defects (GOES BACK 8.0/10 -> this round):\n"
 "D1 MAJOR: install veil killed on the certificate — auto-show timer deleted\n and openModal guarded, so the veil can never pop over ENTER again.\n"
 "D2 MAJOR: 1440 trio phones were 211px (a broken CSS comment in\n phone-style3.html swallowed the #fpWalk{max-width:1320px} rule, leaving\n the v1 720px cap in force) — comment repaired, phones now 360px, nothing\n clips at 1440x900 in any of the 8 groups.\n"
 "D3: certificate date/time digit tiles now paint on the already-claimed\n restore path (ENTER 409 + silent restore), from the row's stored\n created_at, read-only, no new row written: certified date in tiles with\n the weekday word in its laws §3.3 colour (Tue 20 Oct 2026 = gold), live\n time ticking every second.\n"
 "D4: already-claimed note gets 24px margins clear of the frame corners.\n"
 "D5: slide header on every walk step + end phone: emblem (/naya-emblem-cut.png)\n top-left, Naya (/agmt-b06.png) top-right, harvested from the portal.\n"
 "D6: portal.html + worker-consolidated.js (47 MB each) STILL not filed — the\n blobs API 422s them ('input too large', proven this round, piped base64).\n No Git LFS in the repo (.gitattributes has no filter=lfs). INSTEAD the\n rebuild inputs ARE filed here: portal-v1.html (blob a780799a, verified by\n read-back) + build scripts + phone parts + all 14 source pictures, and the\n rebuild was proven byte-identical twice locally: portal 47,431,829 B sha\n eb6a2f7e..., worker 47,776,425 B sha c9560a0e... (build-official.mjs +\n build-worker-official.mjs; pictures read from workspace/user/media_library\n — copy media/ there first).\n\n"
 "Staged: https://official-walkthrough-staging.nayapower.workers.dev/ — portal\n 47,431,829 B sha eb6a2f7e..., cert 317,666 B sha 86536d53..., worker\n deployment on official-walkthrough-staging (HTTP 200), staged bytes ==\n local bytes for / and /identity.html. Probe: 0 FAILs at 390x844 + 1440x900\n (probe-fix1.py in this lane; 44 answer keys, end whole both widths, video\n ball play/pause, vision reveal, 0 unexplained errors — 503s are transient\n agmt-*.jpg, direct curl 200; 409s are the honest already-claimed answer).")
open('/tmp/fix1-commit.json', 'w').write(json.dumps({'message': msg, 'tree': tree['sha'], 'parents': [parent]}))
commit = api('POST', '/repos/%s/git/commits' % REPO, '/tmp/fix1-commit.json')
print('commit:', commit['sha'])
open('/tmp/fix1-ref.json', 'w').write(json.dumps({'sha': commit['sha'], 'force': False}))
ref = api('PATCH', '/repos/%s/git/refs/heads/%s' % (REPO, BRANCH), '/tmp/fix1-ref.json')
print('ref now:', ref['object']['sha'])
print('COMMIT DONE', commit['sha'])
