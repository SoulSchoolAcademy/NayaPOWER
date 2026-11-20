// Fix-5 checker local servers: base (fix-4 tip bytes) on 18095, fix-5 bytes on 18096.
// Routes map to the four filed files; everything else 302s to staging (assets unchanged).
const http = require('http');
const fs = require('fs');
const F4 = '/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix4-20261119/checker/work/';
const F5 = '/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix5-20261119/checker/work/';
const STAGE = 'https://naya-walk-beginning-staging.nayapower.workers.dev';
function serve(dir, prefix, port) {
  const routes = {
    '/': dir + prefix + '-welcome-staged.html',
    '/identity.html': dir + prefix + '-identity-fixed.html',
    '/welcome': dir + prefix + '-walk-beginning-fixed.html',
    '/agreement': dir + prefix + '-agreement-unfold-fixed.html',
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
serve(F4, 'fix4', 18095);
serve(F5, 'fix5', 18096);
