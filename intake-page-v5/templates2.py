"""Template cards v2 — branded names, nutshells, real jewel sockets, VIEW."""

SPARK = '<path d="M12 3l2.2 6.6L21 12l-6.8 2.4L12 21l-2.2-6.6L3 12l6.8-2.4z"/>'
SUN = '<circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M19.1 4.9L17 7M7 17l-2.1 2.1"/>'
LIST = '<path d="M8 6h13M8 12h13M8 18h13"/><circle cx="4" cy="6" r="1.2"/><circle cx="4" cy="12" r="1.2"/><circle cx="4" cy="18" r="1.2"/>'
SHOP = '<path d="M4 9l1-4h14l1 4M4 9v10h16V9M4 9h16M9 19v-6h6v6"/>'
CAL = '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>'
TAG = '<path d="M3 3h7l11 11-7 7L3 10z"/><circle cx="8" cy="8" r="1.5"/>'
TICKET = '<path d="M3 8a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v2a2 2 0 0 0 0 4v2a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-2a2 2 0 0 0 0-4z"/><path d="M13 6v2M13 11v2M13 16v2"/>'
PEOPLE = '<circle cx="9" cy="8" r="3"/><path d="M3 20v-2c0-6 12-6 12 0v2M17 5a3 3 0 0 1 0 6m1 4c2 0 3 2 3 4v1"/>'
IMAGE = '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="M3 17l5-4 4 3 4-4 5 5"/>'
MENU = '<path d="M4 7h16M4 12h16M4 17h16"/>'
DOOR = '<path d="M14 3h7v18h-7M10 8l4 4-4 4M14 12H3"/>'
CHART = '<path d="M5 19v-6m5 6V5m5 14v-9m4 9H3"/>'

# key, color, rgb, shape, glyph, brand name, nutshell, detail
TEMPLATES2 = [
 ("Personal", "#a06bff", "160,107,255", "diamond", SPARK, "Your Personal Smart App",
  "Your home on NayaNET.",
  "Profile, feed, spaces — the one everything orbits. The flagship."),
 ("Today", "#40d3bb", "64,211,187", "circle", SUN, "Your Intelligence Today Smart App",
  "Your daily briefing.",
  "What matters, every morning, in your voice."),
 ("Smart List", "#ffbf3d", "255,191,61", "square", LIST, "Your Smart List App",
  "Lists that stay useful.",
  "Living collections that organize what matters."),
 ("Business", "#3fb8ff", "63,184,255", "square", SHOP, "Your Smart Business App",
  "Your front door.",
  "Services, booking, contact — the page that sells."),
 ("Booking", "#2fe89e", "47,232,158", "circle", CAL, "Your Smart Booking App",
  "Appointments, handled.",
  "A calendar that books itself."),
 ("Product", "#e84fff", "232,79,255", "square", TAG, "Your Smart Product App",
  "Sell one thing beautifully.",
  "Page, price, buy."),
 ("Event", "#ff9a5a", "255,154,90", "circle", TICKET, "Your Smart Event App",
  "Gather people.",
  "Invites, RSVP, day-of — all handled."),
 ("Community", "#ff5e6c", "255,94,108", "circle", PEOPLE, "Your Smart Community App",
  "Your people's home.",
  "Feed, spaces, belonging."),
 ("Portfolio", "#6675ff", "102,117,255", "square", IMAGE, "Your Smart Portfolio App",
  "Show your work.",
  "The gallery that sells for you."),
 ("Menu", "#b8ee57", "184,238,87", "square", MENU, "Your Smart Menu App",
  "Taste, priced.",
  "Your menu, your prices — order-ready."),
 ("Signup", "#40d3bb", "64,211,187", "square", DOOR, "Your Smart Signup App",
  "One page that converts.",
  "Join, subscribe, start."),
 ("Dashboard", "#a06bff", "160,107,255", "diamond", CHART, "Your Smart Dashboard App",
  "Your numbers, live.",
  "Track everything that matters."),
]

def tcard2(key, color, rgb, shape, glyph, brand, nut, detail):
    gem = ('<span class="mini-gem ' + shape + '" style="--tone:' + color + '">'
        '<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.8" '
        'stroke-linecap="round" stroke-linejoin="round" style="width:28px;height:28px">' + glyph + '</svg></span>')
    return ('<div class="tcard2" data-t="' + key + '" style="--tc:' + color + '">'
        + gem
        + '<div style="flex:1;min-width:0"><b class="tbrand">' + brand + '</b><span class="tnut">' + nut + '</span>'
        + '<div class="tdetail">' + detail + '<br><br><b>Ships with the standard eight functions on.</b> Your cart pieces land on top.</div></div>'
        + '<button class="tview" type="button">VIEW</button></div>')

TMPLS2 = "\n".join(tcard2(*t) for t in TEMPLATES2)
