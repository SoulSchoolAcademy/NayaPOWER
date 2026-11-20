// Minimal static server for the local fix-6 file (localhost only).
const http = require('http');
const fs = require('fs');
const p = '/home/hatch/workspace/team-nitro/personal-frame-fix6-20261119/maker/personal-complete-fix6.html';
const buf = fs.readFileSync(p);
http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' });
  res.end(buf);
}).listen(18091, '127.0.0.1', () => console.log('SERVING fix6 on 127.0.0.1:18091'));
