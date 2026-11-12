// nayanet.app — thin worker, all content served as static assets.
// The 5.4MB app lives in ./public and does NOT count against the 1MB script limit.
export default {
  async fetch(request, env) {
    // Static assets handle everything; this is the fallback.
    return env.ASSETS.fetch(request);
  },
};
