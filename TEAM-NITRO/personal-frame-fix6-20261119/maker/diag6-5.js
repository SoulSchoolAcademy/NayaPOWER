const { fetchBase, count } = require('./fetchBase6.js');
const s = fetchBase();
const lines = s.split('\n');
console.log('--- hashchange listeners ---');
lines.forEach((l, n) => { if (l.includes('hashchange')) console.log((n + 1) + ': ' + l.trim().slice(0, 300)); });
console.log('--- ask occurrences (hub/ask, room ask, ask room) ---');
lines.forEach((l, n) => { if (/['"]ask['"]|room:\s*'ask'|hub\/ask|AskRoom|ask-room|naya-ask-room/.test(l)) console.log((n + 1) + ': ' + l.trim().slice(0, 300)); });
console.log('--- HubView room dispatch: search "room ===" / "room ===" ---');
lines.forEach((l, n) => { if (/room\s*===|room\s*!==|params\.room/.test(l)) console.log((n + 1) + ': ' + l.trim().slice(0, 300)); });
