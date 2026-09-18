(()=>{'use strict';
const OUTER=['What Is Naya Power?','What Is Naya?','What Are Smart Notes?','Your Intelligence Today','Intelligence Reports','What Is the Intelligent Library?','Smart Lists','Smart Spaces','Smart Mail'];
function lock(){const bs=[...document.querySelectorAll('.block[data-real-smart-note]')];if(bs.length!==9)return false;bs.forEach((b,i)=>{const h=b.querySelector('h3');if(h)h.textContent=OUTER[i];b.style.width='100%';b.style.minWidth='100%';b.style.maxWidth='none';});return true}
lock();[100,500,1000,2000].forEach(t=>setTimeout(lock,t));
window.NAYA509_SMART_BOARD_V24='outer-title-canonical-lock';
})();