#!/usr/bin/env python3
"""Grow the auto-translate dictionary for the REPAIR fix round (2026-11-13).

Closes the checker's F1-F10: 16 NEW keys (791 -> 807 keys/language).
Source of truth for the base: the embedded MW_I18N span of the third-surface
tip (791 keys/language, verified) — dict-final.json on disk is 0 bytes
(EPERM flake damage) and is NOT the source. Per-language assignment
(d[lang][k] = vals[lang]) — NEVER dict.update(NEW): the card-labels round
proved update() with {es,fr,de} objects corrupts every language.
Assertions before write:
  * start 791 keys/language; no collision on any new key
  * every value a non-empty string
  * no DE-leak chars (a o u ss) into es/fr values
  * NayaNET / Naya preserved where the English key carries them
  * a value identical to its English key only where allowlisted
Voice: es tu / fr vous / de du. Proper names never translate.
Fragment keys where word order holds in es/fr/de; {n} templates where not.
"""
import json, sys

P = "dict-final.json"
START = 791

# (key, es, fr, de)
NEW = [
# ---- F4: Dashboard week-bars Busiest: / quiet-stretch sites ----
("Posts, messages and invites together.", "Publicaciones, mensajes e invitaciones juntos.", "Publications, messages et invitations ensemble.", "Beiträge, Nachrichten und Einladungen zusammen."),
("A quiet stretch — the next post, message or invite lights the first bar.", "Un tramo tranquilo — la próxima publicación, mensaje o invitación enciende la primera barra.", "Une période calme — la prochaine publication, le prochain message ou la prochaine invitation allume la première barre.", "Eine ruhige Phase — der nächste Beitrag, die nächste Nachricht oder Einladung lässt den ersten Balken leuchten."),
("A quiet stretch — the next post, message or invite lights the first circle.", "Un tramo tranquilo — la próxima publicación, mensaje o invitación enciende el primer círculo.", "Une période calme — la prochaine publication, le prochain message ou la prochaine invitation allume le premier cercle.", "Eine ruhige Phase — der nächste Beitrag, die nächste Nachricht oder Einladung lässt den ersten Kreis leuchten."),
("A quiet stretch so far — the chart is waiting.", "Un tramo tranquilo por ahora — el gráfico está esperando.", "Une période calme pour l’instant — le graphique attend.", "Bislang eine ruhige Phase — das Diagramm wartet."),
("The next post, note, message or invite lights the first circle.", "La próxima publicación, nota, mensaje o invitación enciende el primer círculo.", "La prochaine publication, note, message ou invitation allume le premier cercle.", "Der nächste Beitrag, die nächste Notiz, Nachricht oder Einladung lässt den ersten Kreis leuchten."),
("The circles show the story week by week; the totals cover the whole story.", "Los círculos muestran la historia semana a semana; los totales cubren toda la historia.", "Les cercles montrent l’histoire semaine après semaine ; les totaux couvrent toute l’histoire.", "Die Kreise zeigen die Geschichte Woche für Woche; die Summen decken die ganze Geschichte ab."),
("The circles show the last 7 days; the totals cover the full period.", "Los círculos muestran los últimos 7 días; los totales cubren todo el período.", "Les cercles montrent les 7 derniers jours ; les totaux couvrent toute la période.", "Die Kreise zeigen die letzten 7 Tage; die Summen decken den gesamten Zeitraum ab."),
# ---- F5: Dashboard invite-journey funnel (renderFunnel, the bare copy) ----
("No invites yet — record the first one above.", "Todavía no hay invitaciones — registra la primera arriba.", "Pas encore d’invitations — enregistrez la première ci-dessus.", "Noch keine Einladungen — erfasse die erste oben."),
(" walked the whole invite journey.", " recorrió todo el viaje de invitaciones.", " a parcouru tout le parcours d’invitation.", " die ganze Einladungsreise zurückgelegt."),
# ---- F6: the old + menu (#plusmenu) ----
("Send a message", "Enviar un mensaje", "Envoyer un message", "Nachricht senden"),
("Add a Smart Link", "Añadir un Smart Link", "Ajouter un Smart Link", "Smart Link hinzufügen"),
("Add to a list", "Añadir a una lista", "Ajouter à une liste", "Zu einer Liste hinzufügen"),
("Add something", "Añadir algo", "Ajouter quelque chose", "Etwas hinzufügen"),
# ---- F7: avatar camera button (#avedit) ----
("Change picture", "Cambiar foto", "Changer de photo", "Bild ändern"),
("Edit photo", "Editar foto", "Modifier la photo", "Foto bearbeiten"),
# ---- F10: Hide breakdown toggle ----
("Hide breakdown", "Ocultar desglose", "Masquer le détail", "Aufschlüsselung ausblenden"),
]

FIXES = []

IDENTICAL_OK = set()

DE_LEAK = set("äöüßÄÖÜ")


def grow(d):
    """Apply NEW to an already-loaded dict (791 keys/language); return it."""
    assert {k: len(v) for k, v in d.items()} == {"es": START, "fr": START, "de": START}, \
        f"unexpected start counts: {{{k: len(v) for k, v in d.items()}}}"
    seen = set()
    for k, es, fr, de in NEW:
        assert k not in seen, f"duplicate new key: {k!r}"
        seen.add(k)
        for lang in ("es", "fr", "de"):
            assert k not in d[lang], f"COLLISION: {k!r} already in {lang}"
        for lang, v in (("es", es), ("fr", fr), ("de", de)):
            assert isinstance(v, str) and v, f"empty/non-string value for {k!r} in {lang}"
            if lang in ("es", "fr"):
                bad = [c for c in v if c in DE_LEAK]
                assert not bad, f"DE-leak in {lang} value for {k!r}: {bad}"
            if "NayaNET" in k:
                assert "NayaNET" in v, f"NayaNET lost in {lang} value for {k!r}"
            if "Naya" in k:
                assert "Naya" in v, f"Naya lost in {lang} value for {k!r}"
            if v == k and (k, lang) not in IDENTICAL_OK:
                raise AssertionError(f"identical value not allowlisted: {k!r} in {lang}")
        d["es"][k] = es
        d["fr"][k] = fr
        d["de"][k] = de
    for lang, k, old, new in FIXES:
        assert d[lang].get(k) == old, f"FIX precondition failed: {lang}[{k!r}]"
        d[lang][k] = new
    assert {k: len(v) for k, v in d.items()} == {"es": START + len(NEW), "fr": START + len(NEW), "de": START + len(NEW)}
    return d


def main():
    with open(P, encoding="utf-8") as f:
        d = json.load(f)
    grow(d)
    sys.stdout.write(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) + "\n")
    sys.stdout.flush()
    print(f"OK: {len(NEW)} new keys; {START} -> {START + len(NEW)} per language", file=sys.stderr)


if __name__ == "__main__":
    main()
