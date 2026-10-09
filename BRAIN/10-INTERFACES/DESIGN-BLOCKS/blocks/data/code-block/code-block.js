/* Smart Block: code-block — byte-true from Naya Epic Elements - Lego pieces N5.html */
/* Copy buttons */
function copyCode(id) {
  const el = document.getElementById(id);
  const text = el.innerText;
  navigator.clipboard.writeText(text).then(() => {
    const btn = event.target; const old = btn.textContent;
    btn.textContent = 'Copied ✓'; setTimeout(() => btn.textContent = old, 1600);
  });
}
