import { defineLumenElements } from '@santi020k/lumen-elements/define';
import '@santi020k/lumen-elements/styles.css';
defineLumenElements();
const status=document.querySelector('#status'),log=document.querySelector('#eventLog');
document.addEventListener('focusin',e=>{const item=e.target.closest('.candidate [data-page]');if(!item)return;status.textContent=`FOCUSED · ${item.dataset.page.toUpperCase()}`;log.textContent=`Focused: ${item.textContent.trim()} · page=${item.dataset.page}`;});
document.addEventListener('keydown',e=>{const item=e.target.closest('.candidate [data-page]');if(!item)return;const keys=['ArrowRight','ArrowLeft','ArrowDown','ArrowUp','Home','End'];if(!keys.includes(e.key))return;requestAnimationFrame(()=>{const active=document.activeElement;status.textContent=`KEY · ${e.key} → ${active?.textContent?.trim()||'unknown'}`;log.textContent=`Lumen navigation test: ${e.key} → ${active?.textContent?.trim()||'unknown'}`;});});
document.querySelectorAll('.candidate [data-page]').forEach(button=>button.addEventListener('click',()=>{document.querySelectorAll('.candidate [data-page]').forEach(x=>x.classList.remove('active'));button.classList.add('active');status.textContent=`SELECTED · ${button.dataset.page.toUpperCase()}`;log.textContent=`Preserved hook: data-page="${button.dataset.page}"`;}));
