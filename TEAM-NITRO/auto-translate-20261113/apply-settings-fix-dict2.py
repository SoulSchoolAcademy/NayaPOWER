#!/usr/bin/env python3
"""SETTINGS-FIX (second pass) — the auth card's info decorator writes two
more English strings at runtime (the ⓘ panel text + its aria-label), and the
h3 it decorates carries a child button, so the marker must sit on a span,
not the h3. Two new keys (dict 204 -> 206), hand-written by the maker in
the page's voice (es tu, fr vous, de du). Also one voice correction to a
round-1 value: the install card's de line said 'Setzen Sie...' (Sie) while
every other de line on the panel is du — corrected to du, before/after in
the record."""
import json
W = '/home/hatch/workspace/team-nitro/auto-translate-20261113/'
NEW = {
"Your email is your key. It recovers your password if you ever lose it. It proves you are you when you sign in. And it connects your smart apps to you, so your world is there from any phone or computer you sign in on.": (
"Tu correo es tu llave. Recupera tu contraseña si alguna vez la pierdes. Prueba que eres tú cuando inicias sesión. Y conecta tus apps inteligentes contigo, para que tu mundo esté ahí desde cualquier teléfono u ordenador en el que inicies sesión.",
"Votre e-mail est votre clé. Il récupère votre mot de passe si jamais vous le perdez. Il prouve que c\u2019est vous quand vous vous connectez. Et il relie vos apps intelligentes à vous, pour que votre monde soit là depuis n\u2019importe quel téléphone ou ordinateur sur lequel vous vous connectez.",
"Deine E-Mail ist dein Schlüssel. Sie stellt dein Passwort wieder her, falls du es je verlierst. Sie beweist, dass du es bist, wenn du dich anmeldest. Und sie verbindet deine intelligenten Apps mit dir, damit deine Welt von jedem Telefon oder Computer aus da ist, auf dem du dich anmeldest."),
"What does signing in do?": (
"¿Qué hace iniciar sesión?",
"À quoi sert la connexion ?",
"Was bringt das Anmelden?"),
}
d = json.load(open(W + 'dict-final.json', encoding='utf-8'))
assert all(len(v) == 204 for v in d.values()), {k: len(v) for k, v in d.items()}
for k in NEW:
    assert k not in d['es'], 'key already present: %r' % k
for lang, i in (('es', 0), ('fr', 1), ('de', 2)):
    for k, vals in NEW.items():
        d[lang][k] = vals[i]
# voice correction (round-1 value, de Sie -> du, install card line)
old_de = d['de']['Put this app on your home screen — it opens like any other app, no browser bars.']
assert old_de.startswith('Setzen Sie'), old_de
d['de']['Put this app on your home screen — it opens like any other app, no browser bars.'] = 'Setze diese App auf deinen Startbildschirm \u2014 sie öffnet sich wie jede andere App, ohne Browserleisten.'
for lang in ('es', 'fr', 'de'):
    assert len(d[lang]) == 206, (lang, len(d[lang]))
for k in NEW:
    for lang in ('es', 'fr', 'de'):
        assert d[lang][k] != k, 'fallback: %s %r' % (lang, k)
    assert d['es'][k] != d['de'][k] and d['fr'][k] != d['de'][k], 'DE leak: %r' % k
json.dump(d, open(W + 'dict-final.json', 'w'), ensure_ascii=False, indent=1)
print('dict grown 204 -> 206 keys/language; new keys:', len(NEW), '+ 1 de voice correction')
