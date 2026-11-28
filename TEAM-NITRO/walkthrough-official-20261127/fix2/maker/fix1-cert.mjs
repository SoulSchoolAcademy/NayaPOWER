// FIX1 certificate edits (D1, D3, D4) — applied to identity-consolidated.html.
// Node only. Every replacement asserted exactly-once; a miss fails loudly.
import {readFileSync, writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const sha = b => createHash('sha256').update(b).digest('hex');
const F = './identity-consolidated.html';
let s = readFileSync(F, 'utf8');
console.log('base', s.length, 'B sha', sha(Buffer.from(s)));
const once = (name, from, to) => {
  const n = s.split(from).length - 1;
  if (n !== 1) throw new Error('PATCH ' + name + ': expected 1, found ' + n);
  s = s.replace(from, to);
  console.log('patched', name);
};

// ---- D1: kill the install veil on the certificate, entirely. ----
// (a) Guard openModal: the veil can never open on this page. The corner
//     button was already removed; the timer below is deleted too. Two
//     locks, so ENTER can never land on the veil again.
once('D1-openModal-guard',
`      function openModal() {
        var logo = document.getElementById('installLogo');`,
`      function openModal() {
        /* FIX1 D1 — the install veil is DEAD on the certificate: it
           auto-popped ~5s after load and blocked ENTER (checker D1).
           No auto-invite, no manual open, no veil over the certificate,
           ever. The corner button is already gone; this guard is the
           second lock. */
        return;
        var logo = document.getElementById('installLogo');`);
// (b) Delete the auto-show timer branch entirely.
once('D1-auto-show-removed',
`      if (done && cornerBtn) {
        cornerBtn.style.display = 'none';
      } else if (!hide && !done && shows < 3) {
        setTimeout(function () {
          var h = null, d = null, n = 0;
          try {
            h = localStorage.getItem(LS_HIDE);
            d = localStorage.getItem(LS_DONE) || localStorage.getItem(LS_INSTALLED);
            n = parseInt(localStorage.getItem(LS_SHOWS) || '0', 10) || 0;
          } catch (e) {}
          if (!h && !d && n < 3) {
            try { localStorage.setItem(LS_SHOWS, String(n + 1)); } catch (e) {}
            openModal();
          }
        }, 5000);
      }`,
`      if (done && cornerBtn) {
        cornerBtn.style.display = 'none';
      }
      /* FIX1 D1 — the auto-show branch that lived here (5s setTimeout
         -> openModal, capped at 3 shows) is DELETED, not gated: the
         install veil must never auto-pop over the certificate. */`);

// ---- D3: date/time digit tiles on the already-claimed restore path. ----
// (a) paintCertDatetime takes an optional fixed certification moment
//     (the registry row's stored created_at): the DATE shown is that
//     certified day, the TIME ticks live every second. The weekday word
//     leads, coloured by the laws' weekday identity (§3.3) — Friday ruby.
once('D3-paint-weekday-fixed',
`    var DT_COLORS = {'0':'#ffffff','1':'#c62828','2':'#c2410c','3':'#d4a017','4':'#07925f','5':'#0e7490','6':'#3f51b5','7':'#8e24aa','8':'#6d28d9','9':'#a21caf'};
    window.paintCertDatetime = function() {
      var el = document.getElementById('certDatetime');
      if (!el) return;
      var now = new Date();
      var months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'];`,
`    var DT_COLORS = {'0':'#ffffff','1':'#c62828','2':'#c2410c','3':'#d4a017','4':'#07925f','5':'#0e7490','6':'#3f51b5','7':'#8e24aa','8':'#6d28d9','9':'#a21caf'};
    /* FIX1 D3 — weekday identity (laws §3.3): the day's word wears its
       own colour — Friday is ruby red #c62828. */
    var DT_WEEKDAYS = ['SUNDAY','MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY'];
    var DT_WEEKDAY_COLORS = {'SUNDAY':'#8e24aa','MONDAY':'#c2410c','TUESDAY':'#d4a017','WEDNESDAY':'#0f52ba','THURSDAY':'#07925f','FRIDAY':'#c62828','SATURDAY':'#3f51b5'};
    window.paintCertDatetime = function(fixedIso) {
      var el = document.getElementById('certDatetime');
      if (!el) return;
      /* A fixed certification moment pins the DATE (the day the name
         was certified, read from the registry row's stored created_at);
         the TIME stays live and ticks every second. No fixed moment
         means a fresh claim / own restore: date and time both live. */
      if (fixedIso) { try { window.__certDtFixed = fixedIso; } catch(e){} }
      var dayObj = window.__certDtFixed ? new Date(window.__certDtFixed) : new Date();
      var now = new Date();
      var months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'];`);
once('D3-paint-html',
`      el.innerHTML = tiles(pad(now.getDate())) + '<span class="cert-dt-word">' + months[now.getMonth()] + '</span>' + tiles(String(now.getFullYear())) + '<span class="cert-dt-sep">&nbsp;&middot;&nbsp;</span>' + tiles(pad(now.getHours()) + ':' + pad(now.getMinutes()) + ':' + pad(now.getSeconds()));`,
`      var wd = DT_WEEKDAYS[dayObj.getDay()];
      el.innerHTML = '<span class="cert-dt-word" style="color:' + DT_WEEKDAY_COLORS[wd] + '">' + wd + '</span>' + tiles(pad(dayObj.getDate())) + '<span class="cert-dt-word">' + months[dayObj.getMonth()] + '</span>' + tiles(String(dayObj.getFullYear())) + '<span class="cert-dt-sep">&nbsp;&middot;&nbsp;</span>' + tiles(pad(now.getHours()) + ':' + pad(now.getMinutes()) + ':' + pad(now.getSeconds()));`);
// (b) The alias check: when the row exists under ANOTHER device's key,
//     keep the read-only regalia (created_at, cert_no) and paint the
//     date/time from it — a returning citizen sees their certificate's
//     date/time without any claim language and without any write.
once('D3-restore-paint',
`          if (rows && rows.length) {
            var own = null; try { own = localStorage.getItem('nayanet_vault_key'); } catch(e){}
            if (own && rows[0].device_key === own) { certRegalia = { createdAt: rows[0].created_at || null, certNo: (rows[0].cert_no != null ? rows[0].cert_no : null), alias: rows[0].alias || alias, name: rows[0].name || null }; setAliasState('own', alias); }
            else { certRegalia = null; setAliasState(silent ? 'neutral' : 'taken', alias); }
          } else { certRegalia = null; setAliasState(silent ? 'neutral' : 'available', alias); }`,
`          if (rows && rows.length) {
            var own = null; try { own = localStorage.getItem('nayanet_vault_key'); } catch(e){}
            if (own && rows[0].device_key === own) { certRegalia = { createdAt: rows[0].created_at || null, certNo: (rows[0].cert_no != null ? rows[0].cert_no : null), alias: rows[0].alias || alias, name: rows[0].name || null }; setAliasState('own', alias); }
            else { /* FIX1 D3 — already claimed under another key: keep the
                      row's own facts READ-ONLY (no write, no claim words)
                      and paint the certificate date/time from its stored
                      created_at, so the returning citizen sees it. */
              certRegalia = { createdAt: rows[0].created_at || null, certNo: (rows[0].cert_no != null ? rows[0].cert_no : null), alias: rows[0].alias || alias, name: rows[0].name || null };
              if (certRegalia.createdAt && window.paintCertDatetime) paintCertDatetime(certRegalia.createdAt);
              setAliasState(silent ? 'neutral' : 'taken', alias); }
          } else { certRegalia = null; setAliasState(silent ? 'neutral' : 'available', alias); }`);
// (c) The ENTER claim's 409 read-back: carry created_at through as
//     'taken' (it was discarded as null) and paint from it.
once('D3-409-createdAt',
`                if (rows[0].device_key !== deviceKey) return { status: 'taken', createdAt: null };`,
`                if (rows[0].device_key !== deviceKey) return { status: 'taken', createdAt: rows[0].created_at || null };`);
once('D3-taken-paint',
`        if (status === 'taken') {
          lastTakenAlias = finalAlias; setAliasState('taken', finalAlias);`,
`        if (status === 'taken') {
          /* FIX1 D3 — the already-claimed state IS a reachable state:
             paint the certificate date/time from the row's stored
             created_at (read-only), ticking live. */
          if (result && result.createdAt && window.paintCertDatetime) paintCertDatetime(result.createdAt);
          lastTakenAlias = finalAlias; setAliasState('taken', finalAlias);`);

// ---- D4: "already claimed" message clear of the frame corners. ----
once('D4-note-margins',
`#hubNote.fp-taken-green{color:#2fe89e !important;font-size:19px !important;font-weight:800;text-align:center}`,
`#hubNote.fp-taken-green{color:#2fe89e !important;font-size:19px !important;font-weight:800;text-align:center;margin:14px 24px 0 !important;padding:0 8px;box-sizing:border-box;overflow-wrap:break-word}
/* FIX1 D4 — the already-claimed note ran edge-to-edge and touched the
   bottom frame corner jewels; it now sits 24px clear on both sides. */`);

writeFileSync(F, s, 'utf8');
console.log('wrote', F, s.length, 'B sha', sha(Buffer.from(s)));
