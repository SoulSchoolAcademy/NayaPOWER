/* Smart Block JS: lists/sp-about-rows
 * Source: Smart Spaces Page Design.html (extracted byte-true, never rewritten)
 * Adapted from renderAboutTab (source ~line 1924): sp-about-row with sp-about-k/sp-about-v,
 * plus the optional sp-about-desc. Only data plumbing changed; class strings and DOM
 * structure are source-faithful.
 */

/* ============ helpers (from source ~line 724) ============ */
function el(tag, cls, text){
  var e = document.createElement(tag);
  if(cls) e.className = cls;
  if(text !== undefined && text !== null) e.textContent = text;
  return e;
}

/* ============ builders ============ */

/**
 * Key/value about rows inside an .sp-about card.
 *   rows — array of [key, value] pairs
 *   desc — optional description string appended as .sp-about-desc (source-faithful)
 *
 * Source note: the source's about tab derived rows from space data
 * (topic, privacy, member count via spaceMembers(), post count via spacePosts(),
 * created date). The builder takes the resolved [key, value] pairs instead —
 * callers pass already-computed strings.
 */
function spAboutRows(rows, desc){
  var about = el('div','sp-about');
  (rows || []).forEach(function(r){
    var row = el('div','sp-about-row');
    row.appendChild(el('span','sp-about-k', r[0]));
    row.appendChild(el('span','sp-about-v', r[1]));
    about.appendChild(row);
  });
  if(desc){
    about.appendChild(el('div','sp-about-desc', desc));
  }
  return about;
}

// Demo:
// document.body.appendChild(spAboutRows(
//   [['Topic','Creativity'], ['Privacy','🌐 Public'], ['Members','128'], ['Posts','342']],
//   'World-class interface craft. The bar is 10 stars or it never ships.'
// ));
