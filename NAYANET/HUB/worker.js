export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const versionId = env.CF_VERSION_METADATA?.id || 'dev';
    const versionedAsset = (pathname) => {
      const assetUrl = new URL(pathname, url);
      assetUrl.search = '';
      assetUrl.searchParams.set('naya_asset_version', versionId);
      return new Request(assetUrl, request);
    };

    // Canonical Hub root: serve an extensionless byte-identical copy of the built React entry.
    // The Worker-version query prevents a prior edge asset cache from masking a new deployment.
    const assetRequest = (url.pathname === '/' || url.pathname === '/index.html')
      ? versionedAsset('/__nayanet-canonical-hub')
      : url.pathname === '/assistant-runtime.js'
        ? versionedAsset('/assistant-runtime.js')
        : request;
    const response = await env.ASSETS.fetch(assetRequest);

    if (url.pathname === '/' || url.pathname === '/index.html') {
      const headers = new Headers(response.headers);
      headers.set('Content-Type', 'text/html; charset=UTF-8');
      headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0');
      headers.set('Pragma', 'no-cache');
      headers.set('X-Naya-Canonical-Asset', 'index.html');
      headers.set('X-Naya-Asset-Version', versionId);
      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers
      });
    }

    if (url.pathname === '/assistant-runtime.js') {
      const headers = new Headers(response.headers);
      headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0');
      headers.set('Pragma', 'no-cache');
      headers.set('X-Naya-Runtime-Asset', 'live');
      headers.set('X-Naya-Asset-Version', versionId);
      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers
      });
    }

    return response;
  }
};
