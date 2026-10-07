/* Smart Block JS: data/li-day
 * Source: "Ledger Page Design.html" — adapted from the day-divider builder
 * (~lines 1000-1006). el() copied verbatim from ~line 324. The source
 * applied styling inline via cssText and computed the label itself from the
 * day key (TODAY / YESTERDAY / formatted date); here the label arrives as a
 * plain string and styling comes from block.css. DOM structure kept
 * byte-true: <p class="li-day">.
 */
function el(tag,cls,text){const e=document.createElement(tag);if(cls)e.className=cls;if(text!==undefined&&text!==null)e.textContent=text;return e;}

/* liDay(label) -> <p class="li-day">
 * label — e.g. 'TODAY', 'YESTERDAY', or a formatted date string such as
 *         'THURSDAY, OCT 8' (source: d.toLocaleDateString(undefined,
 *         {weekday:'long',month:'short',day:'numeric'}).toUpperCase())
 */
function liDay(label){
  var divider = el('p','li-day','');
  divider.textContent = label;
  return divider;
}

// Demo:
// document.querySelector('.li-stage').appendChild(liDay('TODAY'));
