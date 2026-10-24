// Dashboard ambassador embed — renders from the SAME ambassador_links row the Welcome end slide renders from.
// One wire: no second issuance call. Share text appends the citizen's own link. Ask Naya writes the post when they don't know what to say.
function ambassadorLink(alias) {
  return "https://nayanet.live/joinus?ref=" + encodeURIComponent(alias);
}
function sharePayload(alias, channel) {
  const link = ambassadorLink(alias);
  const text = "I got hired by the future. Your own Smart App, your own AI, your own dashboard — set up ready to go. " + link;
  return { link, channel, text };
}
function askNayaPostPrompt(alias) {
  return "Write me a short, warm post inviting friends to join NayaNET with my ambassador link, " + ambassadorLink(alias) + ". Keep it simple, honest, and beautiful — no hype, no promises about earnings.";
}
function dashboardStats(events) {
  let clicks = 0, signups = 0, sales = 0, net = 0;
  for (const e of events) {
    if (e.kind === "click") clicks++;
    else if (e.kind === "signup") signups++;
    else if (e.kind === "sale") { sales++; net += Number(e.net || 0); }
  }
  return { clicks, signups, sales, share: Math.max(0, net * 0.5) };
}
function nextWednesday(from) {
  const d = new Date(from || Date.now());
  const add = (3 - d.getDay() + 7) % 7 || 7;
  d.setDate(d.getDate() + add);
  return d.toISOString().slice(0, 10);
}
