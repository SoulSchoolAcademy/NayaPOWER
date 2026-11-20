const { fetchBase, count } = require('./fetchBase6.js');
const s = fetchBase();
const lines = s.split('\n');
// Find NayaRouter definition
let idx = [];
let from = 0;
while (true) { const i = s.indexOf('NayaRouter', from); if (i < 0) break; idx.push({ line: s.slice(0, i).split('\n').length, text: s.slice(i, i + 120).replace(/\n/g, ' ') }); from = i + 1; if (idx.length > 80) break; }
console.log('NayaRouter occurrences:', idx.length);
idx.forEach(o => console.log(o.line, o.text));
// Router.on definitions
console.log('--- Router.on lines ---');
lines.forEach((l, n) => { if (l.includes("Router.on(")) console.log((n + 1) + ': ' + l.trim().slice(0, 220)); });
console.log('--- navigate defs ---');
lines.forEach((l, n) => { if (/navigate\s*[:=]|function navigate/.test(l)) console.log((n + 1) + ': ' + l.trim().slice(0, 220)); });
console.log('counts: hub/ask', count(s, '/hub/ask'), 'hub/:room', count(s, 'hub/:room'), "Router.on('*'", count(s, "Router.on('*'"));
