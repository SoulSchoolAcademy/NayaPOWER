const { fetchBase } = require('./fetchBase6.js');
const s = fetchBase();
const lines = s.split('\n');
for (let n = 23540; n <= 23640; n++) { const l = lines[n-1]; if (l.length < 400) console.log(n + ': ' + l); else console.log(n + ': [LONG ' + l.length + 'B] ' + l.slice(0, 250)); }
