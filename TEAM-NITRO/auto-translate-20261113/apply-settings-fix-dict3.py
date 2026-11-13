#!/usr/bin/env python3
"""SETTINGS-FIX (third pass) — the eye check of the Spanish screenshot caught
two more English labels the text dump could not see: the cover-slot input
PLACEHOLDERS (attributes, not textContent). Four new keys (dict 206 -> 210),
hand-written by the maker in the page's voice (es tu, fr vous, de du).
de 'Name' == 'Name' is legitimately identical."""
import json
W = '/home/hatch/workspace/team-nitro/auto-translate-20261113/'
NEW = {
"Button name \u2014 e.g. Naya Academy": (
"Nombre del botón \u2014 p. ej., Naya Academy",
"Nom du bouton \u2014 p. ex. Naya Academy",
"Button-Name \u2014 z. B. Naya Academy"),
"URL \u2014 enter it and the button wakes up": (
"URL \u2014 escríbela y el botón se activa",
"URL \u2014 saisissez-la et le bouton s\u2019active",
"URL \u2014 gib sie ein und der Button wacht auf"),
"Cover button": ("Botón de portada", "Bouton de couverture", "Cover-Button"),
"Name": ("Nombre", "Nom", "Name"),
}
d = json.load(open(W + 'dict-final.json', encoding='utf-8'))
assert all(len(v) == 206 for v in d.values()), {k: len(v) for k, v in d.items()}
for k in NEW:
    assert k not in d['es'], 'key already present: %r' % k
for lang, i in (('es', 0), ('fr', 1), ('de', 2)):
    for k, vals in NEW.items():
        d[lang][k] = vals[i]
for lang in ('es', 'fr', 'de'):
    assert len(d[lang]) == 210, (lang, len(d[lang]))
for k in NEW:
    for lang in ('es', 'fr', 'de'):
        if (k, lang) == ('Name', 'de'):
            continue
        assert d[lang][k] != k, 'fallback: %s %r' % (lang, k)
    assert d['es'][k] != d['de'][k] and d['fr'][k] != d['de'][k], 'DE leak: %r' % k
json.dump(d, open(W + 'dict-final.json', 'w'), ensure_ascii=False, indent=1)
print('dict grown 206 -> 210 keys/language; new keys:', len(NEW))
