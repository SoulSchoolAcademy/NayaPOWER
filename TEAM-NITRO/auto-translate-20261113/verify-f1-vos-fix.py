#!/usr/bin/env python3
"""F1 VOS-FIX verification (maker, 2026-11-13).
Local bytes only (no disk writes except stdout): proves the one-value fix
and that nothing else moved. Staged re-verification runs separately after
filing, on the live staged bytes.
Prints a JSON report to stdout."""
import json, re, subprocess, hashlib, difflib

WORK = '/home/hatch/workspace/team-nitro/auto-translate-20261113/'
PAGE = '/home/hatch/workspace/personal-complete-wt/TEAM-NITRO/personal-page-complete-20261113/personal-complete.html'
DICTF = WORK + 'dict-final.json'
BASE_URL = ("https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/"
            "personal-page-complete-20261113/personal-complete.html"
            "&ref=personal/auto-translate-card-labels-fix-20261113"
            "&cb=2e348bb19e89ce6d4b1a3bc20130c00159d252e0")
R = {}

raw = open(PAGE, 'rb').read()
page = raw.decode('utf-8')
R['local_bytes'] = len(raw)
R['local_sha256'] = hashlib.sha256(raw).hexdigest()
R['base_sha256'] = '93f4302a5866a007b290ac3b144bda62c373ee16a7bfe63222e485ffc29a7b3b'
R['base_bytes'] = 1652796
R['tes_mots_in_page'] = page.count('TES MOTS')
R['vos_mots_formatted_in_page'] = page.count('VOS MOTS \u2014 MIS EN FORME AVEC SOIN PAR NAYA')
R['tus_palabras_in_page'] = page.count('TUS PALABRAS')
R['deine_worte_in_page'] = page.count('DEINE WORTE')
R['markers'] = {'data-mw-tr': page.count('data-mw-tr'),
                'data-mw-ph': page.count('data-mw-ph'),
                'data-mw-aria': page.count('data-mw-aria')}
R['fidelity_render_site'] = ('<span class="ib-naya-fidelity" data-mw-tr="set" '
                             'data-mw-en="YOUR WORDS \u2014 FORMATTED BEAUTIFULLY BY NAYA">' in page)

d = json.load(open(DICTF, encoding='utf-8'))
R['dict_keys_per_lang'] = {k: len(v) for k, v in d.items()}
R['dict_all_values_strings'] = all(isinstance(v, str) for lang in d for v in d[lang].values())
R['dict_fr_fidelity'] = d['fr'].get('YOUR WORDS \u2014 FORMATTED BEAUTIFULLY BY NAYA')
R['dict_es_fidelity'] = d['es'].get('YOUR WORDS \u2014 FORMATTED BEAUTIFULLY BY NAYA')
R['dict_de_fidelity'] = d['de'].get('YOUR WORDS \u2014 FORMATTED BEAUTIFULLY BY NAYA')
R['dict_tes_mots'] = sum(v.count('TES MOTS') for lang in d for v in d[lang].values())

NEW56 = ['IN A NUTSHELL', '\uff0b CREATE SPACE', '\u2605 FAVORITE',
         'ADD TO THE INTELLIGENCE', 'ADD INTEL',
         'ONE INTELLIGENCE \u00b7 MANY VIEWS \u00b7 ONE IDENTITY',
         'TRUST: SOURCE / INTERPRETATION SEPARATED', 'SAVE',
         '\u2764\ufe0f LOVE', '\U0001f44d LIKE', '\uff0b SHARE INTEL',
         'FILE UNDER A CATEGORY', 'Be the first to add intel...',
         'Add an observation, question, correction, or contribution...',
         'Add to the intelligence',
         'Create a smart space from this intelligence', 'Mark as favorite',
         'Save this intelligence', 'Share this intelligence',
         'Add your contribution',
         'Rate this intelligence from one to five stars',
         'Presented by Naya', 'Smart Note', 'from your Smart Feed',
         'Official NayaNET Guide', 'from the Intelligent Library', 'Note',
         'SMART NOTE', 'NAYA NOTE', 'NOTE', 'OWNER', 'PINNED',
         'YOUR WORDS, WORD FOR WORD',
         'DISTILLED FROM THE AUTHOR\u2019S WORDS \u2014 REVIEWED BEFORE POSTING',
         'YOUR WORDS \u2014 FORMATTED BEAUTIFULLY BY NAYA', 'Save to list',
         'Pin', 'Unpin', 'Space from this', 'Business from this',
         'Add a comment\u2026', 'Comment', 'Detail', 'IN:', 'In:',
         'In A Nutshell', 'Human Note', 'Child Note', 'Grandma Note',
         'Naya Note', 'Themes', 'Save', 'Saved \u2713', 'List', 'All notes',
         '+ List']
R['new56_count'] = len(NEW56)
R['new56_present_all_langs'] = all(k in d[lang] for k in NEW56 for lang in ('es', 'fr', 'de'))
R['new56_all_strings'] = all(isinstance(d[lang][k], str) for k in NEW56 for lang in ('es', 'fr', 'de'))
# tu-form scan, checker's exact regex + a wider net, over the 56 new fr values
pat_checker = re.compile(r"\b(tu|tes|ton|ta|tes mots)\b", re.I)
pat_wide = re.compile(r"\b(tu|tes|ton|ta|toi|t['\u2019]es|t['\u2019]as|te|vous|vos|votre|tes)\b", re.I)
hits_checker = [k for k in NEW56 if pat_checker.search(d['fr'][k])]
hits_wide_tu = [k for k in NEW56 if re.search(r"\b(tu|tes|ton|ta|toi|t['\u2019]es|t['\u2019]as)\b", d['fr'][k], re.I)]
R['tu_scan_new56_checker_regex'] = hits_checker
R['tu_scan_new56_wide'] = hits_wide_tu
# full-fr scan for context (pre-existing base-210 tu-forms, not charged here)
R['tu_scan_all_fr_checker_regex'] = [k for k, v in d['fr'].items() if pat_checker.search(v)]

# embedded MW_I18N parse + equality with dict-final.json
m = re.search(r'MW_I18N\s*=\s*\{', page)
R['mw_i18n_found'] = bool(m)
if m:
    i = m.end() - 1
    depth = 0; j = i; instr = False; esc = False
    while j < len(page):
        ch = page[j]
        if instr:
            if esc: esc = False
            elif ch == '\\': esc = True
            elif ch == '"': instr = False
        else:
            if ch == '"': instr = True
            elif ch == '{': depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0: break
        j += 1
    emb = json.loads(page[i:j + 1])
    R['embedded_counts'] = {k: len(v) for k, v in emb.items()}
    R['embedded_equals_dict_final'] = all(emb[lang] == d[lang] for lang in ('es', 'fr', 'de'))
    R['embedded_fr_fidelity'] = emb['fr'].get('YOUR WORDS \u2014 FORMATTED BEAUTIFULLY BY NAYA')
    R['embedded_tes_mots'] = sum(v.count('TES MOTS') for lang in emb for v in emb[lang].values())
    R['embedded_tu_scan_new56'] = [k for k in NEW56 if pat_checker.search(emb['fr'][k])]

# diff vs card-labels staged bytes (live fetch, in-memory)
r = subprocess.run(['curl', '-sS', '-A', 'Mozilla/5.0', '--max-time', '90', BASE_URL],
                   capture_output=True)
R['staged_base_fetch_bytes'] = len(r.stdout)
R['staged_base_fetch_sha256'] = hashlib.sha256(r.stdout).hexdigest()
base = r.stdout.decode('utf-8', errors='replace')
bl = base.splitlines(); fl = page.splitlines()
sm = difflib.SequenceMatcher(None, bl, fl, autojunk=False)
ops = [(t, i1, i2, j1, j2) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != 'equal']
R['diff_changed_lines'] = sum((i2 - i1) + (j2 - j1) for _, i1, i2, j1, j2 in ops)
R['diff_hunks'] = len(ops)
R['diff_hunk_summary'] = []
for tag, i1, i2, j1, j2 in ops:
    R['diff_hunk_summary'].append({
        'op': tag, 'base_lines': [i1, i2], 'fix_lines': [j1, j2],
        'base_sample': [bl[x][:120] for x in range(i1, min(i2, i1 + 1))],
        'fix_sample': [fl[x][:120] for x in range(j1, min(j2, j1 + 1))]})
# the one changed line must be the MW_I18N line, and only TES->VOS inside it
R['diff_only_mw_i18n_line'] = (len(ops) == 1 and ops[0][0] == 'replace'
                               and 'MW_I18N' in fl[ops[0][3]])
if len(ops) == 1:
    bline = bl[ops[0][1]]; fline = fl[ops[0][3]]
    R['changed_line_tes_to_vos_only'] = (
        bline.replace('TES MOTS', 'VOS MOTS') == fline
        and bline.count('TES MOTS') == 1
        and bline.count('VOS MOTS') == 1  # sibling key VOS MOTS, MOT POUR MOT
        and fline.count('VOS MOTS') == 2)  # sibling + this fix

print(json.dumps(R, ensure_ascii=False, indent=1))
