#!/usr/bin/env python3
"""SETTINGS-FIX — apply the HAND-REVIEWED es/fr/de for the 37 new keys into
dict-final.json (167 -> 204 keys/language). The machine draft
(dict-settings-fix-draft.json) was reviewed string by string by the maker:
it dropped sentences, read 'feed' as food, read 'Sign in' as a road sign,
read 'Auto-refresh' as a soft drink / a fridge, used Sie/vous-plural where
the page's voice is du/tu/vous, and invented 'App-Gateway'. Every value
below is the maker's correction. Voice: es tu, fr vous, de du — the voice
the existing dictionary already uses. Proper names stay: NayaNET, Home,
About, Dashboard, Smart Mail."""
import json
W = '/home/hatch/workspace/team-nitro/auto-translate-20261113/'
NEW = {
"Your Preferences": ("Tus preferencias", "Vos préférences", "Deine Präferenzen"),
"Deep black": ("Negro profundo", "Noir profond", "Tiefschwarz"),
"This app\u2019s deep-black theme.": ("El tema negro profundo de esta app.", "Le thème noir profond de cette application.", "Das tiefschwarze Thema dieser App."),
"Notifications": ("Notificaciones", "Notifications", "Benachrichtigungen"),
"Kept on this device \u2014 nothing is sent yet.": ("Se guarda en este dispositivo \u2014 todavía no se envía nada.", "Conservé sur cet appareil \u2014 rien n\u2019est encore envoyé.", "Bleibt auf diesem Gerät \u2014 es wird noch nichts gesendet."),
"App behaviour": ("Comportamiento de la app", "Comportement de l\u2019app", "Verhalten der App"),
"Smart Tabs drift": ("Deriva de las pestañas inteligentes", "Dérive des onglets intelligents", "Gleiten der intelligenten Tabs"),
"The tab ribbon glides slowly, one way \u2014 the NayaNET standard.": ("La cinta de pestañas se desliza despacio, en un solo sentido \u2014 el estándar de NayaNET.", "Le ruban d\u2019onglets glisse lentement, dans un seul sens \u2014 la norme NayaNET.", "Die Tab-Leiste gleitet langsam, in eine Richtung \u2014 der NayaNET-Standard."),
"Motion & glow": ("Movimiento y brillo", "Mouvement et lueur", "Bewegung und Glanz"),
"Breathing light and living motion across the app.": ("Luz que respira y movimiento vivo en toda la app.", "Une lumière qui respire et un mouvement vivant dans toute l\u2019app.", "Licht, das atmet, und lebendige Bewegung in der ganzen App."),
"Auto-refresh": ("Actualización automática", "Actualisation automatique", "Automatische Aktualisierung"),
"Quietly re-reads whichever board is open \u2014 feed, today, inbox, reports or dashboard \u2014 every minute.": ("Vuelve a leer en silencio el panel que esté abierto \u2014 feed, hoy, bandeja de entrada, informes o Dashboard \u2014 cada minuto.", "Relit en silence le panneau ouvert \u2014 fil, aujourd\u2019hui, boîte de réception, rapports ou Dashboard \u2014 chaque minute.", "Liest leise neu, welches Panel gerade offen ist \u2014 Feed, Heute, Posteingang, Berichte oder Dashboard \u2014 jede Minute."),
"Identity": ("Identidad", "Identité", "Identität"),
"Owner:": ("Dueño:", "Propriétaire :", "Eigentümer:"),
"The name, face and story visitors see are this app\u2019s own data. Tap your picture on Home to change it \u2014 the story is edited in About.": ("El nombre, la foto y la historia que ven los visitantes son datos propios de esta app. Toca tu foto en Home para cambiarla \u2014 la historia se edita en About.", "Le nom, la photo et l\u2019histoire que voient les visiteurs sont les données propres de cette app. Touchez votre photo sur Home pour la changer \u2014 l\u2019histoire se modifie dans About.", "Der Name, das Foto und die Geschichte, die Besucher sehen, sind die eigenen Daten dieser App. Tippe auf dein Bild auf Home, um es zu ändern \u2014 die Geschichte wird in About bearbeitet."),
"This identity is what every app\u2019s gate checks \u2014 change it here and it changes everywhere.": ("Esta identidad es lo que comprueba la puerta de cada app \u2014 cámbiala aquí y cambia en todas partes.", "Cette identité est ce que vérifie la porte de chaque app \u2014 changez-la ici et elle change partout.", "Diese Identität ist es, was die Tür jeder App prüft \u2014 ändere sie hier und sie ändert sich überall."),
"Public profile": ("Perfil público", "Profil public", "Öffentliches Profil"),
"On \u2014 visitors can see your profile, make a post on your feed and message you. Off \u2014 this app is private.": ("Activado \u2014 los visitantes pueden ver tu perfil, publicar en tu feed y enviarte mensajes. Desactivado \u2014 esta app es privada.", "Activé \u2014 les visiteurs peuvent voir votre profil, publier sur votre fil et vous envoyer des messages. Désactivé \u2014 cette app est privée.", "An \u2014 Besucher können dein Profil sehen, einen Beitrag in deinem Feed schreiben und dir Nachrichten schicken. Aus \u2014 diese App ist privat."),
"Your story": ("Tu historia", "Votre histoire", "Deine Geschichte"),
"Your feed": ("Tu feed", "Votre fil", "Dein Feed"),
"Everything on this page": ("Todo en esta página", "Tout sur cette page", "Alles auf dieser Seite"),
"Every room on this page, in one place \u2014 and the doors to your other worlds.": ("Cada sala de esta página, en un solo lugar \u2014 y las puertas a tus otros mundos.", "Chaque salle de cette page, au même endroit \u2014 et les portes vers vos autres mondes.", "Jeder Raum auf dieser Seite, an einem Ort \u2014 und die Türen zu deinen anderen Welten."),
"Your other worlds:": ("Tus otros mundos:", "Vos autres mondes :", "Deine anderen Welten:"),
"Today": ("Hoy", "Aujourd\u2019hui", "Heute"),
"Notes": ("Notas", "Notes", "Notizen"),
"Inbox": ("Bandeja de entrada", "Boîte de réception", "Posteingang"),
"Lists": ("Listas", "Listes", "Listen"),
"Scheduler": ("Agenda", "Agenda", "Planer"),
"Reports": ("Informes", "Rapports", "Berichte"),
"Memberships": ("Membresías", "Adhésions", "Mitgliedschaften"),
"This app is installed on this device \u2014 one tap and you are home. It will not nag you again.": ("Esta app está instalada en este dispositivo \u2014 un toque y ya estás en casa. No volverá a molestarte.", "Cette app est installée sur cet appareil \u2014 une touche et vous êtes chez vous. Elle ne vous dérangera plus.", "Diese App ist auf diesem Gerät installiert \u2014 ein Tippen und du bist zu Hause. Sie wird dich nicht mehr nerven."),
"Ready to install.": ("Listo para instalar.", "Prêt à installer.", "Bereit zum Installieren."),
"Not installed yet. When your browser offers install, the button below lights up; on iPhone/iPad use Share \u2192 Add to Home Screen.": ("Todavía no está instalada. Cuando tu navegador ofrezca instalarla, se ilumina el botón de abajo; en iPhone/iPad usa Compartir \u2192 Añadir a la pantalla de inicio.", "Pas encore installée. Quand votre navigateur propose l\u2019installation, le bouton ci-dessous s\u2019allume ; sur iPhone/iPad utilisez Partager \u2192 Ajouter à l\u2019écran d\u2019accueil.", "Noch nicht installiert. Wenn dein Browser die Installation anbietet, leuchtet der Button unten auf; auf iPhone/iPad verwende Teilen \u2192 Zum Home-Bildschirm."),
"Your browser has not offered an install prompt yet \u2014 open the browser menu and choose \u201cAdd to Home Screen\u201d / \u201cInstall app\u201d. The button fires the real browser prompt when one exists.": ("Tu navegador todavía no ha ofrecido instalarla \u2014 abre el menú del navegador y elige \u201cAñadir a la pantalla de inicio\u201d / \u201cInstalar app\u201d. El botón lanza el aviso real del navegador cuando lo hay.", "Votre navigateur n\u2019a pas encore proposé d\u2019installer \u2014 ouvrez le menu du navigateur et choisissez \u201cAjouter à l\u2019écran d\u2019accueil\u201d / \u201cInstaller l\u2019appli\u201d. Le bouton déclenche le vrai message du navigateur quand il existe.", "Dein Browser hat noch keine Installation angeboten \u2014 öffne das Browser-Menü und wähle \u201eZum Home-Bildschirm\u201c / \u201eApp installieren\u201c. Der Button löst den echten Browser-Hinweis aus, sobald es einen gibt."),
"Account": ("Cuenta", "Compte", "Konto"),
"Sign in so NayaNET knows it\u2019s you \u2014 your apps, your mail and your data, synced on every device.": ("Inicia sesión para que NayaNET sepa que eres tú \u2014 tus apps, tu correo y tus datos, sincronizados en cada dispositivo.", "Connectez-vous pour que NayaNET sache que c\u2019est vous \u2014 vos apps, vos mails et vos données, synchronisés sur chaque appareil.", "Melde dich an, damit NayaNET weiß, dass du es bist \u2014 deine Apps, deine Mails und deine Daten, auf jedem Gerät synchronisiert."),
"Sign in": ("Iniciar sesión", "Se connecter", "Anmelden"),
}
d = json.load(open(W + 'dict-final.json', encoding='utf-8'))
assert len(NEW) == 37, len(NEW)
for k in NEW:
    assert k not in d['es'], 'key already present: %r' % k
for lang, i in (('es', 0), ('fr', 1), ('de', 2)):
    for k, vals in NEW.items():
        d[lang][k] = vals[i]
for lang in ('es', 'fr', 'de'):
    assert len(d[lang]) == 204, (lang, len(d[lang]))
# no English fallbacks among the new keys (fr 'Notes' == 'Notes' and fr
# 'Notifications' == 'Notifications' are legitimately identical words)
for k in NEW:
    for lang in ('es', 'fr', 'de'):
        if (k, lang) in (('Notes', 'fr'), ('Notifications', 'fr')):
            continue
        assert d[lang][k] != k, 'fallback: %s %r' % (lang, k)
# no DE leak into es/fr (the first maker's preserve-step lesson)
for k in NEW:
    assert d['es'][k] != d['de'][k], 'es==de: %r' % k
    assert d['fr'][k] != d['de'][k], 'fr==de: %r' % k
# proper names stay inside the sentences
for k in NEW:
    for lang in ('es', 'fr', 'de'):
        if 'NayaNET' in k:
            assert 'NayaNET' in d[lang][k], 'NayaNET lost: %s %r' % (lang, k)
json.dump(d, open(W + 'dict-final.json', 'w'), ensure_ascii=False, indent=1)
print('dict grown 167 -> 204 keys/language; new keys:', len(NEW))
