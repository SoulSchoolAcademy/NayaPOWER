# AUTO-TRANSLATE — chrome inventory (counted at round start, 2026-11-13)
# Base: personal-complete.html sha 4872414a1d428a940a4e12ac31c419f999843a2fde072a9ac91d09b42051c666
# Method: every label was read first-hand from the base file (static markup +
# the JS that renders chrome). Proper names never translate (Naya, NayaNET, a
# citizen's alias, page names Dashboard/Personal/Business/Space/Contacts/About,
# membership names, Smart Mail/Smart Bar/Smart Notes as product names where they
# are names). Icons never translate (R20).
#
# SCOPE (the brief's Exact element): row buttons, feed tabs, bottom bar, + menu,
# Settings rows, composer, side rail, feed cards, language picker — plus the
# home chrome the citizen cannot avoid (cover buttons, drawers, Live Feed strip,
# search, My World). OUT of this inventory (named, not silent — see RECORD §5):
#  - the inner ROOMS (Mail, Connections, Scheduler, Lists, Reports, About, ...):
#    whole app surfaces, each a round of its own; the mechanism reaches them next.
#  - the Smart Access course pane + PowerCast player (content surface).
#  - the wall meta line (a composed sentence with counts + relative time — needs
#    plural templates, a follow-on).
#  - the chat send-status lines (transient server messages).
#  - the owner's tagline (the owner's own words — content, like a note).
#  - the hidden old plus menu (#pluswrap, display:none) — unreachable chrome.
# GAPS FOUND FIRST-HAND (brief vs page):
#  - "12 keys": the dictionary holds 18 entries / 17 distinct keys per language
#    ('My World' is duplicated with the same value). The brief undercounted.
#  - "the eight row buttons": the visible row is 8 (Message, About, My World,
#    Skills, Connections, Invite, Share, Join NayaNET); the byId map names 11
#    because it also carries statsbtn + intelbtn, which do not exist in the
#    markup (dead entries), and settingsbtn, which is the gear (icon only, R20).
#  - "the guide steps": NO numbered guide-steps block exists on this page
#    (grep 'Step 1/2/3', '1-2-3', 'easy as' = 0 hits). Nothing to twin; the
#    no-words flow's ENTER step is the cover + row buttons. No guide block is
#    invented in this round.
#  - the bottom bar is ALREADY icon-only (5 round segs, svg + count); its only
#    words are aria-label/title. Part 3's work there is nil — recorded, not claimed.
#  - the drawers' opener buttons (#os-rooms-plus, #os-eco-plus) are display:none
#    (Personal round override), so the drawer labels are unreachable today; they
#    are still translated (cheap, future-proof) but get no new icon twins.
# COUNTS: distinct English keys in the inventory below. The build script asserts
# the grown dictionary covers every one of them in es/fr/de.
