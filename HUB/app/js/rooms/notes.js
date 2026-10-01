/* NOTES — Smart Notes. Capture is REAL here (local drafts),
   and honest about the pipeline it feeds. */

function NotesRoom() {
  const { el, Icons, Board, StatePanel, toast } = window.NayaUI;
  const R = window.NayaRuntime;
  const wrap = el('div');
  const ACC = 'var(--accent-notes)';

  /* ——— Capture board — real, working ——— */
  const cap = Board({
    accent: ACC, icon: 'note',
    title: 'Capture anything',
    sub: 'Distill → classify → connect → retrieve. The pipeline is real; until the runtime lands, drafts are kept safely on this device.',
    lift: false,
  });
  cap.body.innerHTML = `
    <textarea id="note-input" rows="3" placeholder="Smart-note this…"
      style="width:100%;background:#ffffff08;border:1px solid var(--line);border-radius:var(--radius-md);
             color:var(--ink);padding:14px 16px;font-size:14px;resize:vertical;outline:none"></textarea>
    <div style="display:flex;gap:10px;margin-top:12px;align-items:center;flex-wrap:wrap">
      <button class="btn" id="note-keep" style="--btn-accent:${ACC}">${Icons.icon('plus')}<span>Keep it</span></button>
      <span style="color:var(--muted);font-size:14px;letter-spacing:.08em">LOCAL DRAFT · FLOWS TO THE GOVERNED PIPELINE WHEN IT CONNECTS</span>
    </div>`;
  wrap.appendChild(cap);

  /* ——— Drafts — real, from this device ——— */
  const draftsBoard = Board({ accent: ACC, icon: 'lists', title: 'Your drafts', sub: 'Kept on this device', lift: false });
  const listEl = el('div');
  draftsBoard.body.appendChild(listEl);
  wrap.appendChild(el('div', '', '<hr class="hr">'));
  wrap.appendChild(draftsBoard);

  function renderDrafts() {
    const notes = R.draftNotes();
    listEl.innerHTML = '';
    if (!notes.length) {
      listEl.appendChild(StatePanel({
        accent: ACC, icon: 'note',
        title: 'Nothing captured yet',
        body: 'Your first note will appear here the moment you keep it — and one day, the whole collective intelligence will remember it with you.',
        actions: [],
      }));
      return;
    }
    notes.forEach(n => {
      const item = el('div');
      item.style.cssText = 'padding:13px 4px;border-bottom:1px solid var(--line-soft)';
      const d = new Date(n.at);
      item.innerHTML = `
        <div style="font-size:15px;margin-bottom:5px">${escapeHtml(n.text)}</div>
        <div style="display:flex;gap:10px;align-items:center">
          <span class="pill soon"><span class="dot"></span>LOCAL DRAFT</span>
          <span style="color:var(--muted);font-size:14px">${d.toLocaleString()}</span>
        </div>`;
      listEl.appendChild(item);
    });
  }
  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  }

  cap.body.querySelector('#note-keep').addEventListener('click', () => {
    const input = cap.body.querySelector('#note-input');
    const res = R.captureNote(input.value);
    toast(res.message, ACC);
    if (res.ok) { input.value = ''; renderDrafts(); }
  });

  renderDrafts();
  return wrap;

  /* ——— Below the working capture, the honest state for the pipeline ——— */
}

window.NayaRooms = window.NayaRooms || {};
window.NayaRooms.notes = NotesRoom;
