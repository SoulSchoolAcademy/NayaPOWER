#!/usr/bin/env python3
"""CARD-LABELS-FIX dictionary growth (Area #41, 2026-11-13).
Adds the note cards' fixed Intelligent Block labels to MW_I18N in es/fr/de:
210 -> 266 keys/language. Every value below is hand-written by the maker
(no machine draft — the last round's draft had errors a human had to
correct: "tu alimentación", "señales en", "Auto-refresco").
Voice: es tú / fr vous / de du — the voice the existing dictionary uses.
Assertions: every new key absent from dict-final.json (Share/Send are
REUSED existing keys, not added); no English fallback except the three
legitimately identical words (fr 'Note', de 'Detail', de 'IN:'); no DE
value (ä/ö/ü/ß) leaking into es/fr; 'NayaNET' preserved inside every
value that carries it in English.
Usage: apply-card-labels-dict.py  (edits dict-final.json in place)"""
import json

WORK = '/home/hatch/workspace/team-nitro/auto-translate-20261113/'
NEW = {
    # --- the captain's seven (CAPTAIN-VERDICT-AUTO-TRANSLATE-SETTINGS-FIX) ---
    'IN A NUTSHELL': {
        'es': 'EN POCAS PALABRAS', 'fr': 'EN RÉSUMÉ', 'de': 'KURZ GESAGT'},
    '\uff0b CREATE SPACE': {
        'es': '\uff0b CREAR ESPACIO', 'fr': '\uff0b CRÉER UN ESPACE',
        'de': '\uff0b RAUM ERSTELLEN'},
    '\u2605 FAVORITE': {
        'es': '\u2605 FAVORITO', 'fr': '\u2605 FAVORI', 'de': '\u2605 FAVORIT'},
    'ADD TO THE INTELLIGENCE': {
        'es': 'AÑADIR A LA INTELIGENCIA',
        'fr': 'AJOUTER À L’INTELLIGENCE',
        'de': 'ZUR INTELLIGENZ HINZUFÜGEN'},
    'ADD INTEL': {
        'es': 'AÑADIR INTEL', 'fr': 'AJOUTER INTEL', 'de': 'INTEL HINZUFÜGEN'},
    'ONE INTELLIGENCE · MANY VIEWS · ONE IDENTITY': {
        'es': 'UNA INTELIGENCIA · MUCHAS VISTAS · UNA IDENTIDAD',
        'fr': 'UNE INTELLIGENCE · PLUSIEURS VUES · UNE IDENTITÉ',
        'de': 'EINE INTELLIGENZ · VIELE ANSICHTEN · EINE IDENTITÄT'},
    'TRUST: SOURCE / INTERPRETATION SEPARATED': {
        'es': 'CONFIANZA: FUENTE / INTERPRETACIÓN SEPARADAS',
        'fr': 'CONFIANCE : SOURCE / INTERPRÉTATION SÉPARÉES',
        'de': 'VERTRAUEN: QUELLE / INTERPRETATION GETRENNT'},
    # --- BoardActions top/bottom actions (visible labels) ---
    'SAVE': {'es': 'GUARDAR', 'fr': 'ENREGISTRER', 'de': 'SPEICHERN'},
    '\u2764\ufe0f LOVE': {
        'es': '\u2764\ufe0f ME ENCANTA', 'fr': '\u2764\ufe0f J’ADORE',
        'de': '\u2764\ufe0f LIEBEN'},
    '\U0001f44d LIKE': {
        'es': '\U0001f44d ME GUSTA', 'fr': '\U0001f44d J’AIME',
        'de': '\U0001f44d GEFÄLLT MIR'},
    '\uff0b SHARE INTEL': {
        'es': '\uff0b COMPARTIR INTEL', 'fr': '\uff0b PARTAGER L’INTEL',
        'de': '\uff0b INTEL TEILEN'},
    'FILE UNDER A CATEGORY': {
        'es': 'ARCHIVAR EN UNA CATEGORÍA',
        'fr': 'CLASSER DANS UNE CATÉGORIE',
        'de': 'IN EINER KATEGORIE ABLEGEN'},
    # --- addIntel block ---
    'Be the first to add intel...': {
        'es': 'Sé el primero en añadir intel...',
        'fr': 'Soyez le premier à ajouter de l’intel...',
        'de': 'Füge als Erster Intel hinzu...'},
    'Add an observation, question, correction, or contribution...': {
        'es': 'Añade una observación, pregunta, corrección o aportación...',
        'fr': 'Ajoutez une observation, une question, une correction ou une contribution...',
        'de': 'Füge eine Beobachtung, Frage, Korrektur oder einen Beitrag hinzu...'},
    # --- aria-labels (routed at creation + re-synced by the [data-mw-aria] pass) ---
    'Add to the intelligence': {
        'es': 'Añadir a la inteligencia', 'fr': 'Ajouter à l’intelligence',
        'de': 'Zur Intelligenz hinzufügen'},
    'Create a smart space from this intelligence': {
        'es': 'Crear un espacio inteligente a partir de esta inteligencia',
        'fr': 'Créer un espace intelligent à partir de cette intelligence',
        'de': 'Aus dieser Intelligenz einen Smart Space erstellen'},
    'Mark as favorite': {
        'es': 'Marcar como favorito', 'fr': 'Marquer comme favori',
        'de': 'Als Favorit markieren'},
    'Save this intelligence': {
        'es': 'Guardar esta inteligencia',
        'fr': 'Enregistrer cette intelligence',
        'de': 'Diese Intelligenz speichern'},
    'Share this intelligence': {
        'es': 'Compartir esta inteligencia',
        'fr': 'Partager cette intelligence',
        'de': 'Diese Intelligenz teilen'},
    'Add your contribution': {
        'es': 'Añade tu aportación', 'fr': 'Ajoutez votre contribution',
        'de': 'Füge deinen Beitrag hinzu'},
    'Rate this intelligence from one to five stars': {
        'es': 'Valora esta inteligencia de una a cinco estrellas',
        'fr': 'Notez cette intelligence de une à cinq étoiles',
        'de': 'Bewerte diese Intelligenz mit einem bis fünf Sternen'},
    # --- intelBoard foot / presenter / meta ---
    'Presented by Naya': {
        'es': 'Presentado por Naya', 'fr': 'Présenté par Naya',
        'de': 'Präsentiert von Naya'},
    'Smart Note': {
        'es': 'Nota inteligente', 'fr': 'Note intelligente',
        'de': 'Intelligente Notiz'},
    'from your Smart Feed': {
        'es': 'de tu feed inteligente', 'fr': 'de votre feed intelligent',
        'de': 'aus deinem intelligenten Feed'},
    'Official NayaNET Guide': {
        'es': 'Guía oficial de NayaNET', 'fr': 'Guide officiel NayaNET',
        'de': 'Offizieller NayaNET-Leitfaden'},
    'from the Intelligent Library': {
        'es': 'de la Biblioteca Inteligente',
        'fr': 'de la Bibliothèque Intelligente',
        'de': 'aus der intelligenten Bibliothek'},
    'Note': {'es': 'Nota', 'fr': 'Note', 'de': 'Notiz'},
    # --- ibFeedCard kinds / badges / microcopy ---
    'SMART NOTE': {
        'es': 'NOTA INTELIGENTE', 'fr': 'NOTE INTELLIGENTE',
        'de': 'INTELLIGENTE NOTIZ'},
    'NAYA NOTE': {'es': 'NOTA NAYA', 'fr': 'NOTE NAYA', 'de': 'NAYA-NOTIZ'},
    'NOTE': {'es': 'NOTA', 'fr': 'NOTE', 'de': 'NOTIZ'},
    'OWNER': {'es': 'DUEÑO', 'fr': 'PROPRIÉTAIRE', 'de': 'EIGENTÜMER'},
    'PINNED': {'es': 'FIJADO', 'fr': 'ÉPINGLÉ', 'de': 'ANGEPINNT'},
    'YOUR WORDS, WORD FOR WORD': {
        'es': 'TUS PALABRAS, PALABRA POR PALABRA',
        'fr': 'TES MOTS, MOT POUR MOT',
        'de': 'DEINE WORTE, WORT FÜR WORT'},
    'DISTILLED FROM THE AUTHOR’S WORDS — REVIEWED BEFORE POSTING': {
        'es': 'DESTILADO DE LAS PALABRAS DEL AUTOR — REVISADO ANTES DE PUBLICAR',
        'fr': 'DISTILLÉ DES MOTS DE L’AUTEUR — VÉRIFIÉ AVANT PUBLICATION',
        'de': 'DESTILLIERT AUS DEN WORTEN DES AUTORS — VOR DEM POSTEN GEPRÜFT'},
    'YOUR WORDS — FORMATTED BEAUTIFULLY BY NAYA': {
        'es': 'TUS PALABRAS — CON FORMATO PRECIOSO POR NAYA',
        'fr': 'TES MOTS — MIS EN FORME AVEC SOIN PAR NAYA',
        'de': 'DEINE WORTE — WUNDERSCHÖN FORMATIERT VON NAYA'},
    'Save to list': {
        'es': 'Guardar en lista', 'fr': 'Enregistrer dans une liste',
        'de': 'In Liste speichern'},
    'Pin': {'es': 'Fijar', 'fr': 'Épingler', 'de': 'Anpinnen'},
    'Unpin': {'es': 'Quitar fijación', 'fr': 'Désépingler',
              'de': 'Fixierung lösen'},
    'Space from this': {
        'es': 'Espacio a partir de esto', 'fr': 'Espace à partir de ceci',
        'de': 'Space daraus erstellen'},
    'Business from this': {
        'es': 'Negocio a partir de esto', 'fr': 'Entreprise à partir de ceci',
        'de': 'Business daraus erstellen'},
    'Add a comment…': {
        'es': 'Añade un comentario…', 'fr': 'Ajoutez un commentaire…',
        'de': 'Füge einen Kommentar hinzu…'},
    'Comment': {'es': 'Comentar', 'fr': 'Commenter', 'de': 'Kommentieren'},
    'Detail': {'es': 'Detalle', 'fr': 'Détail', 'de': 'Detail'},
    'IN:': {'es': 'EN:', 'fr': 'DANS :', 'de': 'IN:'},
    'In:': {'es': 'En:', 'fr': 'Dans :', 'de': 'In:'},
    # --- layer heads (title case as stored in note data; unknown heads fall
    # back to English at render — citizen-defined heads are never forced) ---
    'In A Nutshell': {
        'es': 'En pocas palabras', 'fr': 'En résumé', 'de': 'Kurz gesagt'},
    'Human Note': {
        'es': 'Nota humana', 'fr': 'Note humaine', 'de': 'Menschliche Notiz'},
    'Child Note': {
        'es': 'Nota infantil', 'fr': 'Note d’enfant', 'de': 'Kindernotiz'},
    'Grandma Note': {
        'es': 'Nota de abuela', 'fr': 'Note de grand-mère',
        'de': 'Oma-Notiz'},
    'Naya Note': {'es': 'Nota Naya', 'fr': 'Note Naya', 'de': 'Naya-Notiz'},
    'Themes': {'es': 'Temas', 'fr': 'Thèmes', 'de': 'Themen'},
    # --- noteCard (Notes view) ---
    'Save': {'es': 'Guardar', 'fr': 'Enregistrer', 'de': 'Speichern'},
    'Saved ✓': {
        'es': 'Guardado ✓', 'fr': 'Enregistré ✓', 'de': 'Gespeichert ✓'},
    'List': {'es': 'Lista', 'fr': 'Liste', 'de': 'Liste'},
    # --- category bar (ibCatBarHTML, exported beside ibFeedCard) ---
    'All notes': {
        'es': 'Todas las notas', 'fr': 'Toutes les notes',
        'de': 'Alle Notizen'},
    '+ List': {'es': '+ Lista', 'fr': '+ Liste', 'de': '+ Liste'},
}

IDENTICAL = {('fr', 'Note'), ('de', 'Detail'), ('de', 'IN:')}

d = json.load(open(WORK + 'dict-final.json', encoding='utf-8'))
assert all(len(v) == 210 for v in d.values()), 'dict must start at 210 keys/language'
assert len(NEW) == 56, 'expected 56 new keys, got %d' % len(NEW)
for k, vals in NEW.items():
    assert set(vals) == {'es', 'fr', 'de'}, 'key %r missing a language' % k
    for lang in ('es', 'fr', 'de'):
        assert k not in d[lang], 'key %r already in dict[%s] (collision)' % (k, lang)
        v = vals[lang]
        assert v.strip(), 'empty value for %r[%s]' % (k, lang)
        if v != k:
            assert (lang, k) not in IDENTICAL, 'identical value not allowlisted: %r[%s]' % (k, lang)
        if 'NayaNET' in k:
            assert 'NayaNET' in v, 'NayaNET lost in %r[%s]' % (k, lang)
        if lang in ('es', 'fr'):
            assert not any(c in v for c in 'äöüß'), 'DE leak into %s: %r -> %r' % (lang, k, v)
        if lang == 'de' and k in ('IN A NUTSHELL', 'ADD INTEL', 'SAVE'):
            assert v, 'missing de for %r' % k
for lang in ('es', 'fr', 'de'):
    d[lang].update(NEW)
assert all(len(v) == 266 for v in d.values()), 'dict must end at 266 keys/language, got %s' % {k: len(v) for k, v in d.items()}
json.dump(d, open(WORK + 'dict-final.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=2)
print('dict grown: 210 -> 266 keys/language (56 new, 0 collisions)')
