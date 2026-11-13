#!/usr/bin/env python3
"""Repair the card-labels dict growth (2026-11-13).
apply-card-labels-dict.py inserted each new key as the whole per-key
{es, fr, de} object under EVERY language, so MW_I18N.es['IN A NUTSHELL']
was a dict and mwTr() returned it -> textContent '[object Object]'.
Fix (mechanical, touches only broken entries): any value that is a dict
is replaced by its own language's string.
Asserts after: every value a string; no DE-leak chars into es/fr;
spot-checks on the captain's known set.
"""
import json, sys
P = '/home/hatch/workspace/team-nitro/auto-translate-20261113/dict-final.json'
d = json.load(open(P))
fixed = []
for lang in ('es', 'fr', 'de'):
    for k, v in list(d[lang].items()):
        if isinstance(v, dict):
            assert lang in v, (lang, k)
            assert isinstance(v[lang], str), (lang, k)
            d[lang][k] = v[lang]
            fixed.append((lang, k))
print('fixed %d object values' % len(fixed))
assert fixed, 'nothing to fix — dict already clean?'
assert len(fixed) == 56 * 3, 'expected 168 object values (56 keys x 3 langs), got %d' % len(fixed)
for lang in ('es', 'fr', 'de'):
    bad = [k for k, v in d[lang].items() if not isinstance(v, str)]
    assert not bad, (lang, bad[:5])
    print(lang, 'keys:', len(d[lang]), 'all strings OK')
# DE-leak check: no ä/ö/ü/ß in es/fr values
for lang in ('es', 'fr'):
    leak = [k for k, v in d[lang].items() if any(c in v for c in 'äöüßÄÖÜ')]
    assert not leak, (lang, leak[:5])
    print(lang, 'no DE leak OK')
for k, want in [('IN A NUTSHELL', {'es': 'EN POCAS PALABRAS', 'fr': 'EN RÉSUMÉ', 'de': 'KURZ GESAGT'}),
                ('ADD INTEL', {'es': 'AÑADIR INTEL', 'fr': 'AJOUTER INTEL', 'de': 'INTEL HINZUFÜGEN'}),
                ('SAVE', {'es': 'GUARDAR', 'fr': 'ENREGISTRER', 'de': 'SPEICHERN'})]:
    for lang, w in want.items():
        assert d[lang][k] == w, (lang, k, d[lang][k])
    print('spot-check OK:', k)
json.dump(d, open(P, 'w'), indent=1, ensure_ascii=False)
print('dict-final.json rewritten clean')
