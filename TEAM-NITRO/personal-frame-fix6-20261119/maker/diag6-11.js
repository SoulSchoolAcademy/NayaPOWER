const { fetchBase } = require('./fetchBase6.js');
const s = fetchBase();
const lines = s.split('\n');
for (let n = 12600; n <= 12750; n++) { const l = lines[n-1]; if (l.length < 400) console.log(n + ': ' + l); else console.log(n + ': [LONG ' + l.length + 'B] ' + l.slice(0, 200)); }
