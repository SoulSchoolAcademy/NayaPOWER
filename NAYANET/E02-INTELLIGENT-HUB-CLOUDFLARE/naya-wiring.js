"use strict";
(() => {
  const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
  const panel=kind=>window.NayaRuntimeOpen?.(kind);
  const openRuntime=kind=>{if(typeof window.__nayaOpen==="function")window.__nayaOpen(kind);};
  // naya-runtime exposes its private open function through this small bridge.
  if(typeof window.__nayaOpen!=="function"){
    // The runtime is loaded immediately before this file; its DOM panel is enough to reuse by click delegation.
    document.addEventListener("click",e=>{
      const b=e.target.closest?.("[data-runtime-open]"); if(!b)return; e.preventDefault();e.stopPropagation();
      const p=$("#nayaRuntimePanel"); if(p)p.classList.add("open");
    },true);
  }
  const runtimePanel=$("#nayaRuntimePanel");
  if(!runtimePanel)return;
  function open(kind){
    const content=$("#runtimeContent");
    // Re-dispatch a semantic event consumed by the runtime's existing controls.
    const evt=new CustomEvent("naya:open",{detail:{kind}});window.dispatchEvent(evt);
  }
  // Replace the two ambiguous legacy actions with useful, direct destinations.
  const ask=$("#askNaya"); if(ask)ask.onclick=e=>{e.preventDefault();window.dispatchEvent(new CustomEvent("naya:open",{detail:{kind:"naya"}}));};
  $$('[data-preview]').forEach(b=>b.onclick=e=>{e.preventDefault();const x=b.dataset.preview;const kind=x==="brain"?"naya":x==="identity"?"identity":x==="network"?"network":x;window.dispatchEvent(new CustomEvent("naya:open",{detail:{kind}}));});
  // Direct world actions are intentionally kept real: MAXESS remains the live assessment, while local capabilities open their real runtime.
  $$('[data-quick]').forEach(b=>b.onclick=e=>{e.preventDefault();if(b.dataset.quick==="maxess")location.href="https://aiscore.nayanet.app/";});
  window.addEventListener("naya:open",e=>{
    const kind=e.detail?.kind;
    if(!kind)return;
    // Recreate the useful panel by clicking a hidden semantic launcher when available.
    let launcher=$("#runtimeLauncher");
    if(!launcher){launcher=document.createElement("button");launcher.id="runtimeLauncher";launcher.hidden=true;document.body.appendChild(launcher);}
    launcher.dataset.kind=kind;
    // The runtime's own open function is not global; use the same event path by temporarily setting a command.
    const target=$("#nayaRuntimePanel");
    if(target){target.classList.add("open");target.dataset.requestedKind=kind;}
    // If the runtime panel is already present, invoke its forms through a lightweight reconstruction event.
    window.dispatchEvent(new CustomEvent("naya:render",{detail:{kind}}));
  });
})();
