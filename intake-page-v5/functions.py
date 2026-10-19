"""Step 2 function rows — every icon from the approved library, nothing invented."""
FUNCS = [
 ("Smart Mail","#3fb8ff","Your email, turned into an intelligent inbox.",
  '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>'),
 ("Smart Lists","#ffbf3d","Living collections that organize what matters.",
  '<path d="M4 19v-8m5 8V5m5 14V9m5 10V3"/>'),
 ("Smart Space","#a06bff","A home base for a project, topic, or part of your life.",
  '<rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/>'),
 ("Connect + communicate","#2fe89e","Message and share with people, right from the app.",
  '<circle cx="9" cy="8" r="3"/><path d="M3 20v-2c0-6 12-6 12 0v2M17 5a3 3 0 0 1 0 6m1 4c2 0 3 2 3 4v1"/>'),
 ("Intelligence Today","#e84fff","Your daily briefing — what matters, every morning.",
  '<path d="M12 3l2.2 6.6L21 12l-6.8 2.4L12 21l-2.2-6.6L3 12l6.8-2.4z"/>'),
 ("Personal social feed","#ff9a5a","Your own feed — post once, it goes everywhere you allow.",
  '<circle cx="12" cy="12" r="8"/><path d="M12 4v16M4 12h16"/>'),
 ("Smart Tabs","#6675ff","Contextual windows — the right view for the moment you're in.",
  '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/>'),
 ("Share","#a06bff","Send anything, anywhere.",
  '<circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="M8.2 10.8l7.6-3.6M8.2 13.2l7.6 3.6"/>'),
]
EXTRAS = [
 ("Ask Naya","#40d3bb","Ask anything — answers from your own intelligence.",
  '<circle cx="11" cy="11" r="7"/><path d="M16.5 16.5L21 21"/>'),
 ("Reports","#6675ff","Daily, weekly, monthly — your numbers, explained.",
  '<path d="M5 19v-6m5 6V5m5 14v-9m4 9H3"/>'),
 ("Booking doors","#2fe89e","Let people book time with you.",
  '<rect x="5" y="3" width="14" height="18" rx="1"/><circle cx="15" cy="12" r="1.2"/>'),
 ("Guard","#ff5e6c","You decide who sees what. Always.",
  '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/>'),
 ("Saved","#40d3bb","Everything you keep, in one place.",
  '<path d="M6 3h12v18l-6-4-6 4z"/>'),
 ("Calendar","#ffbf3d","Your schedule, intelligent.",
  '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>'),
]
def frow(name, color, sub, path, on):
    return ('<div class="frow elev-1"><span class="fic" style="--fc:' + color + '">'
      '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--fc)" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">' + path + '</svg></span>'
      '<span style="flex:1"><b>' + name + '</b><span class="fsub">' + sub + '</span></span>'
      '<span class="tog' + (' on' if on else '') + '"><span class="knob"></span></span></div>')

FUNCS_HTML = ('<div class="frow-head">STANDARD — ON, UNCHECK TO REMOVE</div>'
  + "\n".join(frow(n, c, s, p, True) for n, c, s, p in FUNCS)
  + '<details class="xdrop elev-1"><summary>EXTRA FEATURES — TAP TO BROWSE</summary>'
  + "\n".join(frow(n, c, s, p, False) for n, c, s, p in EXTRAS)
  + '</details>')
