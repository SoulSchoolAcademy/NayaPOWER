import base64, hashlib, importlib.util, json, os, urllib.request
spec = importlib.util.spec_from_file_location('ghdirect', os.path.expanduser('~/workspace/team-nitro/gh-direct.py'))
ghd = importlib.util.module_from_spec(spec); spec.loader.exec_module(ghd)
token = ghd.get_token()
BASE='https://api.github.com/repos/SoulSchoolAcademy/NayaPOWER'
H={'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28','Authorization':f'Bearer {token}','User-Agent':'muse-github-skill/1.0'}
OUT=os.path.expanduser('~/workspace/team-nitro/dashboard/defectfix-v7/pass6on7')
jobs={
 'pass5':'4b4084e1aad4e3fbd64d1052abc2f48cdc56ac23',
 'pass6':'9fb49a377de6e0f00c2e550bdf7859477b12d551',
 'pass7':'9227167d2e20b29ebbfb8299e5a5864e24ef854d',
}
expect={'pass5':(1778959,'0e4ef2fef4ccf54c178155f86d14176a56418d1d7590732ce39321b583b4a388'),
 'pass6':(1783285,'034f9f813911245828b4a727e8af8f9080966ed0a76d5d9899f65fd3a12a367e'),
 'pass7':(1781461,'7613bc46e781078ea6c8f55ce5381701a4c7289863969f364d853a22f847f013')}
for name,sha in jobs.items():
    req=urllib.request.Request(BASE+'/git/blobs/'+sha, headers=H)
    with urllib.request.urlopen(req) as r: blob=json.load(r)
    raw=base64.b64decode(blob['content'])
    open(f'{OUT}/dashboard-{name}-blob.html','wb').write(raw)
    h=hashlib.sha256(raw).hexdigest()
    print(name, 'blob', blob['sha'], 'size', blob.get('size'), 'decoded', len(raw), 'sha256', h, 'EXPECT', expect[name], 'MATCH', (len(raw),h)==expect[name])
