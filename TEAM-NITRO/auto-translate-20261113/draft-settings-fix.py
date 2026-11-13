#!/usr/bin/env python3
"""SETTINGS-FIX — draft es/fr/de for the 37 new Settings-panel keys via the
round's own Workers AI staging worker (same path as draft-translations.py).
Writes dict-settings-fix-draft.json; the maker reviews every string by hand
before it lands in dict-final.json. Fault-tolerant: each batch retries up to
5 times; failures are reported, never silently skipped."""
import json, urllib.request, time
from concurrent.futures import ThreadPoolExecutor, as_completed
URL='https://naya-auto-translate-staging.nayapower.workers.dev/translate'
UA={'Content-Type':'application/json','User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0'}
KEYS=[
"Your Preferences","Deep black","This app\u2019s deep-black theme.","Notifications",
"Kept on this device \u2014 nothing is sent yet.","App behaviour","Smart Tabs drift",
"The tab ribbon glides slowly, one way \u2014 the NayaNET standard.","Motion & glow",
"Breathing light and living motion across the app.","Auto-refresh",
"Quietly re-reads whichever board is open \u2014 feed, today, inbox, reports or dashboard \u2014 every minute.",
"Identity","Owner:",
"The name, face and story visitors see are this app\u2019s own data. Tap your picture on Home to change it \u2014 the story is edited in About.",
"This identity is what every app\u2019s gate checks \u2014 change it here and it changes everywhere.",
"Public profile",
"On \u2014 visitors can see your profile, make a post on your feed and message you. Off \u2014 this app is private.",
"Your story","Your feed","Everything on this page",
"Every room on this page, in one place \u2014 and the doors to your other worlds.",
"Your other worlds:","Today","Notes","Inbox","Lists","Scheduler","Reports","Memberships",
"This app is installed on this device \u2014 one tap and you are home. It will not nag you again.",
"Ready to install.",
"Not installed yet. When your browser offers install, the button below lights up; on iPhone/iPad use Share \u2192 Add to Home Screen.",
"Your browser has not offered an install prompt yet \u2014 open the browser menu and choose \u201cAdd to Home Screen\u201d / \u201cInstall app\u201d. The button fires the real browser prompt when one exists.",
"Account",
"Sign in so NayaNET knows it\u2019s you \u2014 your apps, your mail and your data, synced on every device.",
"Sign in"]
def one(job):
    tgt,batch=job
    body=json.dumps({'segments':batch,'source_lang':'en','target_lang':tgt}).encode()
    last=None
    for attempt in range(5):
        try:
            req=urllib.request.Request(URL,data=body,headers=UA,method='POST')
            with urllib.request.urlopen(req,timeout=120) as r:
                d=json.load(r)
            if not d.get('ok'): raise RuntimeError(str(d)[:200])
            segs=d['segments']
            assert len(segs)==len(batch), 'segment count %d != %d' % (len(segs), len(batch))
            return tgt,dict(zip(batch,segs))
        except Exception as e:
            last=e; time.sleep(3*(attempt+1))
    raise RuntimeError('batch failed %s %s: %s'%(tgt,batch[0][:40],last))
jobs=[]
for tgt in ['es','fr','de']:
    for i in range(0,len(KEYS),6):
        jobs.append((tgt,KEYS[i:i+6]))
print('jobs:',len(jobs), flush=True)
out={'es':{},'fr':{},'de':{}}
failed=[]
with ThreadPoolExecutor(max_workers=3) as ex:
    futs={ex.submit(one,j):j for j in jobs}
    for f in as_completed(futs):
        try:
            tgt,res=f.result(); out[tgt].update(res)
            print('done', sum(len(v) for v in out.values()), '/', len(KEYS)*3, tgt, flush=True)
        except Exception as e:
            failed.append((futs[f],str(e))); print('FAILED', futs[f][0], futs[f][1][0][:40], e, flush=True)
json.dump(out, open('dict-settings-fix-draft.json','w'), ensure_ascii=False, indent=1)
print('saved dict-settings-fix-draft.json', {k:len(v) for k,v in out.items()}, 'failed:', len(failed))
for j,e in failed: print('  FAIL', j, e)
