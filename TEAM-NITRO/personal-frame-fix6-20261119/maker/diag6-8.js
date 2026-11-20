const { fetchBase } = require('./fetchBase6.js');
const s = fetchBase();
const lines = s.split('\n');
const show = (n) => { const l = lines[n-1]; console.log(n + ': ' + l.slice(0, 600)); };
[10283,10284,10285,10524,10525,10526,15228,15229,15230,15231,15232,15233,15234,15235,23570,23571,23572,23573,23574,23575,23576,23577,23578,23579,23580,23581,23582,23583].forEach(show);
console.log('--- location.hash = #/hub occurrences ---');
lines.forEach((l, n) => { if (l.includes("location.hash") && l.includes("#/hub")) console.log((n+1) + ': ' + l.trim().slice(0, 400)); });
console.log('--- navigate(/hub/feed) occurrences ---');
lines.forEach((l, n) => { if (l.includes("navigate('/hub/feed')") || l.includes('navigate("/hub/feed")')) console.log((n+1) + ': ' + l.trim().slice(0, 250)); });
