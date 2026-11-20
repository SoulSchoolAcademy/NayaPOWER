// Fix-5 maker local servers: base bytes on 18093, fix5 bytes on 18094.
// Page routes map to the four files; everything else 302-redirects to staging
// (images / api / assets are unchanged between base and fix5).
const http = require('http');
const fs = require('fs');
const W = '/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/';
const STAGE = 'https://naya-walk-beginning-staging.nayapower.workers.dev';
function serve(prefix, port) {
  const routes = {
    '/': W + prefix + '-welcome-staged.html',
    '/identity.html': W + prefix + '-identity-fixed.html',
    '/welcome': W + prefix + '-walk-beginning-fixed.html',
    '/agreement': W + prefix + '-agreement-unfold-fixed.html',
  };
  const srv = http.createServer((req, res) => {
    const u = new URL(req.url, 'http://x');
    const f = routes[u.pathname];
    if (f && fs.existsSync(f)) {
      const buf = fs.readFileSync(f);
      res.writeHead(200, { 'Content-Type': 'text/html;charset=utf-8', 'Cache-Control': 'no-store' });
      res.end(buf);
      return;
    }
    res.writeHead(302, { Location: STAGE + req.url });
    res.end();
  });
  srv.listen(port, '127.0.0.1', () => console.log(prefix, 'on', port));
}
serve('base', 18093);
serve('fix5', 18094);
