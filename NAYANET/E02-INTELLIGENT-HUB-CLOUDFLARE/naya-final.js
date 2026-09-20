"use strict";
(() => {
  const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
  const open=kind=>window.NayaRuntimeOpen?.(kind) || window.dispatchEvent(new CustomEvent("naya:open",{detail:{kind}}));
  $$('[data-preview]').forEach(b=>b.onclick=e=>{e.preventDefault();e.stopPropagation();const x=b.dataset.preview;if(x==="player"){document.querySelector("#coreArt")?.click();return}if(x==="brain")return open("naya");if(x==="identity")return open("identity");if(x==="network")return open("network");if(x==="maxess")return location.href="https://aiscore.nayanet.app/";});
  $$('[data-quick]').forEach(b=>b.onclick=e=>{e.preventDefault();e.stopPropagation();if(b.dataset.quick==="player")document.querySelector("#openPlayer")?.click();else if(b.dataset.quick==="maxess")location.href="https://aiscore.nayanet.app/"});
  document.addEventListener("click",e=>{const b=e.target.closest?.("#worldPrimary");if(!b)return;e.preventDefault();e.stopImmediatePropagation();const tag=$("#worldTag")?.textContent||"";if(/MAXESS/.test(tag))return location.href="https://aiscore.nayanet.app/";if(/5-DAY/.test(tag))return open("challenge");if(/INTELLIGENT SPACES/.test(tag))return open("space");if(/YOUR NETWORK/.test(tag))return open("network");if(/SMART NOTES|INTELLIGENCE/.test(tag))return open("notes");return open("naya")},true);
})();
