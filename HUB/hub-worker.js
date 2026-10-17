// NayaPOWER Hub worker — serves the Hub static assets from HUB/app/.
// Deployments run ONLY through .github/workflows/deploy-hub-cloudflare.yml
// This file is the thinnest possible shell: all content is static assets.
export default {
  async fetch(request, env) {
    return env.ASSETS.fetch(request);
  },
};
