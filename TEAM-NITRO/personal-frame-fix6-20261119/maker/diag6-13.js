const { fetchBase } = require('./fetchBase6.js');
const s = fetchBase();
const lines = s.split('\n');
console.log('--- popstate listeners ---');
lines.forEach((l, n) => { if (l.includes('popstate')) console.log((n+1) + ': ' + l.trim().slice(0, 300)); });
console.log('--- showView callers (short lines) ---');
lines.forEach((l, n) => { if (l.includes('showView(') && l.length < 300) console.log((n+1) + ': ' + l.trim().slice(0, 280)); });
console.log('--- osShowView callers (short lines) ---');
lines.forEach((l, n) => { if (l.includes('osShowView(') && l.length < 300) console.log((n+1) + ': ' + l.trim().slice(0, 280)); });
