export async function fetchJson(url) {
  const res = await fetch(url);
  const text = await res.text();
  if (!res.ok) throw new Error(`HTTP ${res.status} Bad Request\n${text}`);
  return JSON.parse(text);
}
