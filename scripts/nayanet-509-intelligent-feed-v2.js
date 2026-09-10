/* NayaNET Intelligent Feed V2 — RETIRED COMPATIBILITY SHIM
 *
 * The former V2 materializer could replace the authoritative Hub feed with
 * oversized replacement boards. That behavior is retired.
 *
 * Canonical Hub feed presentation now lives in the authoritative Hub artifact
 * itself and preserves the existing Intelligent Block architecture.
 * This file intentionally performs no DOM replacement, no feed mounting, and
 * no synthetic board rendering.
 */
(()=>{'use strict';
  if(typeof window!=='undefined'){
    window.NayaNET509Renderer={
      status:'retired',
      authority:'authoritative Hub artifact',
      replacesFeed:false,
      rendersSyntheticBoards:false
    };
  }
})();
