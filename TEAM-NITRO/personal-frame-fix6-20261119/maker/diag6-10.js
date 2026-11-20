const { fetchBase } = require('./fetchBase6.js');
const s = fetchBase();
const lines = s.split('\n');
console.log('--- "Ask Naya" text occurrences (short lines only) ---');
lines.forEach((l, n) => { if (l.includes('Ask Naya') && l.length < 500) console.log((n+1) + ': ' + l.trim().slice(0, 400)); });
console.log('--- askBtn / aria-label Ask ---');
lines.forEach((l, n) => { if (/askBtn|aria-label=.Ask Naya/.test(l) && l.length < 500) console.log((n+1) + ': ' + l.trim().slice(0, 400)); });
console.log('--- HubView ask room: search "ask" in room render switch ---');
lines.forEach((l, n) => { if ((/roomId\s*===|activeRoom\s*===|case\s+'ask'/.test(l)) && l.length < 400) console.log((n+1) + ': ' + l.trim().slice(0, 350)); });
