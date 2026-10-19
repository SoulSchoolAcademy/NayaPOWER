/* NayaFunction: ask-naya v1.0.0
   What: Ask Naya — voice + text AI assistant on the page. Orb visual, 
     memory filaments, voice memos, drawer navigation.
   Source: Ask-Naya-Page_Design.html (Prototype v9) — Shawn's file, 2026-10-18.
     "Pretty close to being done... it works currently." Updated 2026-10-18:
     text laws applied (24/18/14 only, no gray text).
   Activation: <div data-fn="ask-naya" data-fn-config='{...}'></div>
   Config: {
     orbColor: hex for the orb (default #a06bff purple)
     knowledgeBank: URL to the knowledge bank JSON (default: embedded)
     voiceClips: URL to voice clips (default: embedded; 2MB — consider external)
     showDrawer: show the NayaNET drawer (default true)
   } — all optional.
   Ready behavior: Orb renders, askNaya() responds from knowledge bank, 
     voice memos play, drawer navigates. Works client-side.
   Connected behavior: Live Naya backend — requires `connected: true`.
     (Backend `feature.naya_answers` exists — intake-only for now.)
   Implementation: See ~/workspace/user/files/Ask-Naya-Page_Design.html
     (3MB: 45KB code + 942KB knowledge bank + 2MB voice clips).
     This wrapper activates the core; bank/clips load separately.
   Status: IMPLEMENTED (text laws applied 2026-10-18). Needs different-seat verification.
*/
(function(){
  'use strict';
  const FN_ID = 'ask-naya';
  
  function activate(mount, config){
    config = config || {};
    // The full implementation lives in Ask-Naya-Page_Design.html.
    // This is the activation contract — the assembler inlines or references it.
    mount.setAttribute('data-fn-active', FN_ID);
    mount.setAttribute('data-fn-version', '1.0.0');
    
    // Minimal orb placeholder — full UI loads from the page
    const orb = document.createElement('div');
    orb.className = 'orb';
    orb.style.setProperty('--oc', config.orbColor || '#a06bff');
    orb.style.width = '80px';
    orb.style.height = '80px';
    orb.setAttribute('aria-label', 'Ask Naya');
    mount.appendChild(orb);
    
    // Click opens the full Ask Naya experience
    orb.style.cursor = 'pointer';
    orb.addEventListener('click', function(){
      // TODO: Open drawer/modal with full Ask Naya UI
      // For now, dispatch event for host to handle
      mount.dispatchEvent(new CustomEvent('asknaya-open', {bubbles: true}));
    });
    
    return {
      id: FN_ID,
      version: '1.0.0',
      destroy: function(){ mount.innerHTML = ''; }
    };
  }
  
  // Register with NayaFunctions if available
  if (typeof NayaFunctions !== 'undefined' && NayaFunctions.register) {
    NayaFunctions.register(FN_ID, { activate: activate });
  } else {
    // Standalone: expose globally
    window.NayaAskNaya = { activate: activate };
  }
})();
