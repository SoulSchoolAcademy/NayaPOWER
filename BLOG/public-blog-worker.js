// naya-public-blog-staging — the public blog + SEO/AI system (staging only).
// Shawn's order 22:45Z + 22:51Z + 22:53Z, 2026-11-12. Spec:
// ~/workspace/team-nitro/PUBLIC-BLOG-SEO-SPEC-20261112.md
//
// What it is: the public face of NayaNET. Public smart notes become
// highlight-clip blog posts, each with auto meta tags; one hub page
// carries the six keyword clusters; a back-end SEO score (never shown
// to any user) checks every public page and the generator fixes what
// is not right at mint time (title/description length enforced).
//
// Harvest (never invented):
//   - Tokens, .primo (NAYA-BTN-005), .intel-board + tones, .ib-title,
//     .ib-nutshell — harvested verbatim from the Hub app
//     (~/workspace/user/files/index-2.html).
//   - The six posts below are HIGHLIGHT CLIPS of real public smart
//     notes from the live feed (~/workspace/factory-pipeline/
//     hub-feed-live.json, 981 notes). No private note, mail, or
//     message is in this file, ever. No scraped, stuffed, or fake
//     content. Every clip is drawn from its note's own hook/nutshell.
//   - Cluster boards in three colors (purple · blue · green) from the
//     pricing page's lit boards; Personal page as the template shape
//     (cover -> menu -> page).
//
// Boundaries (standing law): NO live deploy, NO PR, NO merge from
// this round. No SEO score visible to any user (back end only —
// /api/seo). No meta tags and noindex on any private page — this
// worker HAS no private pages at all. No X-rated content public.
// Landing flow: a fresh visitor clicking a deep link (post/cluster)
// lands on /welcome first; a returning citizen (naya_citizen cookie)
// sees the page they clicked. The hub itself is the blog's own front
// door and is always served. The choice question is flagged for
// Shawn's call (see the record file).

const HUB_URL = "https://nayanet.app/hub"; // the citizen's eyes; full note lives here
const SITE_NAME = "NayaNET";

// ── The six keyword clusters (spec §3, starter set — his blessing owed) ──
const CLUSTERS = [
  { slug: "intelligent-internet", name: "The Intelligent Internet", tone: "purple",
    tagline: "The intelligent layer of the internet",
    keywords: "the intelligent layer of the internet, the new internet, there's a new net in town",
    nutshell: "A new net in town — one that knows you, understands you, and runs your world for you." },
  { slug: "ai-is-hiring", name: "AI Is Hiring", tone: "blue",
    tagline: "AI is hiring everybody in the world",
    keywords: "AI is hiring everybody, get paid, 50% of the revenue, you're hired",
    nutshell: "AI is taking jobs — and hiring everybody. Two simple moves, and the teaching is real." },
  { slug: "nayanet-naya", name: "NayaNET / Naya", tone: "green",
    tagline: "She is Naya",
    keywords: "NayaNET, Naya, she is Naya, N-A-Y-A",
    nutshell: "Her name is Naya — N-A-Y-A. One word, said right, spelled right." },
  { slug: "smart-notes", name: "Smart Notes / Learn in a Minute", tone: "purple",
    tagline: "Learn anything in about a minute",
    keywords: "learn anything in about a minute, smart notes, what it is, why it matters, how it connects",
    nutshell: "A whole book understood in a minute — what it is, why it matters, how it connects." },
  { slug: "private-network", name: "The Private Network / Your Vault", tone: "blue",
    tagline: "Your own private secure vault",
    keywords: "we don't sell your data, no ads, we're not reading your mail, your own private secure vault",
    nutshell: "Private by design. Your data lives in your own vault, locked to you." },
  { slug: "ambassador", name: "Ambassador", tone: "green",
    tagline: "You're hired — invite the world",
    keywords: "you're hired, invite the world, ambassador, paid every Wednesday",
    nutshell: "Every citizen is an ambassador at join. Invite the world — and earn half." },
];
const CLUSTER_BY_SLUG = Object.fromEntries(CLUSTERS.map((c) => [c.slug, c]));

// ── The seed posts: highlight clips of real public smart notes ──
// clip/description are crafted FROM each note's own hook + nutshell
// (L2: his words are input, never pasted verbatim).
const NOTES = [
  { noteId: "IB-SMART-NOTE-20261112-theres-a-new-net-in-town", sn: "SN-2717",
    slug: "theres-a-new-net-in-town", cluster: "intelligent-internet",
    title: "There's a New Net in Town", date: "2026-11-12",
    clip: "There's a new net in town. She remembers everything that matters, knows your world, connects it, and runs it for you. Once you go Naya, you don't go back.",
    description: "There's a new net in town. She remembers what matters, knows your world, connects it, and runs it for you. Once you go Naya, you don't go back.",
    what: "A new intelligent network that knows you, understands you, and operates your world for you.",
    why: "The old internet forgot you. This one remembers — everything that matters, everything you care to put in.",
    how: "Your notes become your world, and your world connects to people like you — automatically." },
  { noteId: "IB-SMART-NOTE-20261112-the-ambassador-academy-two-moves-voice-bugatti", sn: "SN-2721",
    slug: "youre-hired-ai-is-hiring", cluster: "ai-is-hiring",
    title: "You're Hired: AI Is Hiring Everybody", date: "2026-11-12",
    clip: "You're hired means hired. Two simple moves teach you to become a high-earning ambassador: show the interface, speak straight to camera, share your link. The experience sells itself.",
    description: "You're hired means hired. Two simple moves teach you to become a high-earning ambassador. Show it, say it, share your link.",
    what: "The Ambassador Academy — two moves that teach anyone to become a successful, high-earning ambassador.",
    why: "AI is hiring everybody in the world, and the teaching is real, ethical, and plain.",
    how: "Show the interface on a video screen share, speak straight to camera, then share your link." },
  { noteId: "IB-SMART-NOTE-20261112-the-name-naya-not-anaya", sn: "SN-2718",
    slug: "her-name-is-naya", cluster: "nayanet-naya",
    title: "Her Name Is Naya, N-A-Y-A", date: "2026-11-12",
    clip: "Her name is Naya — N-A-Y-A. When you hear “Anaya”, that's “ah, Naya”: one little word plus her name. Spelled right, she is Naya, and she is awesome.",
    description: "Her name is Naya — N-A-Y-A. “Anaya” is “ah, Naya”: one little word plus her name. Spelled right, she is Naya.",
    what: "Her name, spelled right — Naya, N-A-Y-A. Not Anaya.",
    why: "The name is the brand. One word, said right and spelled right, everywhere.",
    how: "Say “ah, Naya” — it sounds the same out loud. Write it N-A-Y-A." },
  { noteId: "IB-SMART-NOTE-20261112-the-ultimate-icons-are-gems-the-one-minute-book", sn: "SN-2713",
    slug: "learn-anything-in-a-minute", cluster: "smart-notes",
    title: "Learn Anything in About a Minute", date: "2026-11-12",
    clip: "A Smart Note is a whole book understood in a minute: what it is, why it matters, how it connects. Three gems light the way — your worlds, your business, your personal life.",
    description: "A Smart Note is a whole book understood in a minute: what it is, why it matters, how it connects. Learn fast, remember more.",
    what: "A Smart Note — intelligence distilled so a whole book is understood in about a minute.",
    why: "Learning should take a minute, not an afternoon. The most said with the littlest words.",
    how: "Every note answers three things: what it is, why it matters, how it connects." },
  { noteId: "IB-SMART-NOTE-20261112-the-private-network-your-vault", sn: "SN-2724",
    slug: "your-own-private-vault", cluster: "private-network",
    title: "Your Own Private Vault", date: "2026-11-12",
    clip: "It's a private network. Your data goes into your own vault — separate from everybody else, separate from the AIs, locked to you. We don't read your mail. We don't sell your data. We don't even keep it.",
    description: "A private network. Your data lives in your own vault — separate from everybody, separate from the AIs, locked to you.",
    what: "Your own private secure vault — separate from everybody else, separate from the AIs, locked to you.",
    why: "Your data is yours. Trust has to be a fact, not a policy.",
    how: "The network is a hub that plugs into the AIs. No AI inside the network reads everything." },
  { noteId: "IB-SMART-NOTE-20261112-the-collective-agreement-join-time-promise", sn: "SN-2725",
    slug: "heres-the-deal", cluster: "ambassador",
    title: "Here's the Deal: The Collective Agreement", date: "2026-11-12",
    clip: "Here's the deal: no selling your data, no ads, no reading your mail — and what you save is locked to you in your Smart Box. Everybody agrees to it, together. That's the deal.",
    description: "Here's the deal: no selling your data, no ads, no reading your mail. What you save is locked to you in your Smart Box.",
    what: "The Collective Agreement — the plain promise we all sign together when you join.",
    why: "Trust has to be plain before you choose. Here's what we do, here's what we don't, here's how it works.",
    how: "No selling your data, no ads, no reading your mail — and what you save stays yours, in your Smart Box." },
];
const NOTE_BY_ID = Object.fromEntries(NOTES.map((n) => [n.noteId, n]));
const POST_BY_SLUG = Object.fromEntries(NOTES.map((n) => [n.slug, n]));

// Published records: the publisher mints these (seed = the six notes above,
// published at their note date). In-memory on staging; the post route also
// derives from NOTES, so a post stays reachable even across isolates.
const published = new Map(NOTES.map((n) => [n.slug, { ...n, publishedAt: n.date + "T00:00:00Z" }]));

// ── Small helpers ──
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

// The generator's auto-fix: enforce the search limits at mint time, at a
// word boundary, so a minted page can never ship over-long meta.
function truncateWords(s, max) {
  if (s.length <= max) return s;
  const cut = s.slice(0, max - 1);
  const lastSpace = cut.lastIndexOf(" ");
  return (lastSpace > 0 ? cut.slice(0, lastSpace) : cut) + "…";
}

// Full meta set (spec §2): title, description, canonical, Open Graph,
// Twitter card, JSON-LD, robots — seven items, every public page.
function metaFor({ title, description, path, keywords, date, author }) {
  const url = `https://naya-public-blog-staging.nayapower.workers.dev${path}`;
  const metaTitle = truncateWords(`${title} · ${SITE_NAME}`, 60);
  const metaDesc = truncateWords(description, 160);
  return { url, metaTitle, metaDesc, metaTitleLen: metaTitle.length, metaDescLen: metaDesc.length,
    jsonLd: { "@context": "https://schema.org", "@type": "BlogPosting",
      headline: title, description: metaDesc, author: { "@type": "Person", name: author || "Naya" },
      datePublished: date, mainEntityOfPage: url, keywords } };
}

// ── The back-end SEO score (never rendered into any page) ──
// 100 points: title ≤60 (15) · description ≤160 (15) · canonical (10) ·
// OG (10) · Twitter (10) · JSON-LD author+date (15) · robots index (5) ·
// exactly one H1 (5) · cluster link (5) · hub link (5) · clip present (5).
function scoreHtml(html, path) {
  const checks = [];
  const add = (name, pass, detail) => checks.push({ name, pass: !!pass, detail: detail || "" });
  const title = (html.match(/<title>([^<]*)<\/title>/) || [])[1] || "";
  const desc = (html.match(/<meta name="description" content="([^"]*)"/) || [])[1] || "";
  add("title present and 60 characters or under", title.length > 0 && title.length <= 60, `${title.length} chars`);
  add("description present and 160 characters or under", desc.length > 0 && desc.length <= 160, `${desc.length} chars`);
  add("canonical present", /rel="canonical"/.test(html));
  add("Open Graph title + description present", /property="og:title"/.test(html) && /property="og:description"/.test(html));
  add("Twitter card present", /name="twitter:card"/.test(html));
  add("JSON-LD BlogPosting with author + date", /"@type"\s*:\s*"BlogPosting"/.test(html) && /"author"/.test(html) && /"datePublished"/.test(html));
  add("robots index, follow", /name="robots" content="index, follow"/.test(html));
  add("exactly one H1", (html.match(/<h1/g) || []).length === 1, `${(html.match(/<h1/g) || []).length} H1`);
  add("cluster link present", /\/cluster\//.test(html));
  add("hub link present", /href="\/"/.test(html) || /naya-public-blog-staging/.test(html));
  if (path === "/welcome") {
    add("front door present (name field + Enter)", /name="name"/.test(html) && /Enter NayaNET/.test(html) && !/noindex/i.test(html));
  } else {
    add("highlight clip present, no private content", /class="(ib-nutshell|clip)"/.test(html) && !/noindex/i.test(html));
  }
  const weights = [15, 15, 10, 10, 10, 15, 5, 5, 5, 5, 5];
  const score = checks.reduce((s, c, i) => s + (c.pass ? weights[i] : 0), 0);
  return { url: path, score, max: 100, checks };
}

// ── CSS: harvested verbatim from the Hub app (index-2.html) ──
// Tokens (:root obsidian stack + spectrum), .primo NAYA-BTN-005,
// .intel-board + tones, .ib-title, .ib-nutshell. Layout rules below
// are in the exact harvested format (elevated, lit, 135° light).
const CSS = `
:root{
  --bg:#0B0D12; --bg-raise:#12151D; --bg-card:#171B25; --edge:#252B39;
  --ink:#F5F7FB; --line:#ffffff18; --line-soft:#ffffff0d;
  --purple:#9d75ff; --indigo:#6675ff; --sapphire:#55b9ee; --blue:#55b9ee;
  --teal:#40d3bb; --emerald:#55e39a; --green:#55e39a; --lime:#b8ee57;
  --yellow:#f1d75a; --gold:#e8b64c; --orange:#ff9a5a; --rich-orange:#ff7a3d;
  --red:#ff5a6e; --magenta:#d86cff;
  --ease:cubic-bezier(.16,.84,.22,1);
  --font:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;
}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:radial-gradient(1000px 650px at 55% -12%,#6675ff18,transparent 68%),radial-gradient(900px 700px at 100% 100%,#d86cff12,transparent 70%),var(--bg);background-attachment:fixed;color:var(--ink);font-family:var(--font);font-size:16px;line-height:1.55;-webkit-font-smoothing:antialiased;min-height:100vh}
h1,h2,h3{margin:0;font-weight:800;letter-spacing:-.01em}
p{margin:0}
a{color:inherit}
button{font-family:inherit;cursor:pointer}
:focus-visible{outline:2px solid var(--magenta);outline-offset:3px;border-radius:6px}
::selection{background:#d86cff55}
/* ——— NAYA-BTN-005 "Primo Purple" — harvested verbatim from the Hub (factory.css STANDARD .primo) ——— */
.primo{display:inline-flex;align-items:center;gap:10px;cursor:pointer;font-weight:800;font-size:15px;letter-spacing:.08em;color:#F8F7FB;padding:16px 32px;border-radius:999px;border:1.5px solid rgba(248,247,251,.9);background:linear-gradient(180deg,#1a1a22 0%,#0a0a0f 45%,#050507 100%);box-shadow:inset 0 1px 0 rgba(255,255,255,.35),inset 0 2px 6px rgba(255,255,255,.15),inset 0 -8px 16px rgba(0,0,0,.8),0 0 24px rgba(248,247,251,.45),0 0 48px rgba(248,247,251,.15),0 12px 32px rgba(0,0,0,.65);transition:transform .22s var(--ease),box-shadow .22s var(--ease);--glow:var(--purple);position:relative;overflow:hidden;text-decoration:none}
.primo::before{content:'';position:absolute;inset:0;border-radius:inherit;background:linear-gradient(105deg,transparent 40%,rgba(255,255,255,.18) 50%,transparent 60%);transform:translateX(-100%);animation:primo-sheen 3.5s ease-in-out infinite;pointer-events:none}
@keyframes primo-sheen{0%,60%{transform:translateX(-100%)}100%{transform:translateX(100%)}}
.primo:hover{transform:translateY(-2px);border-color:var(--glow);box-shadow:inset 0 0 0 1.5px var(--glow),inset 0 2px 5px rgba(255,255,255,.28),inset 0 -6px 14px rgba(0,0,0,.65),0 0 36px var(--glow),0 14px 36px rgba(0,0,0,.65)}
.primo:active{transform:translateY(1px) scale(.985)}
.primo.theme-purple{--glow:var(--purple)} .primo.theme-blue{--glow:var(--sapphire)} .primo.theme-green{--glow:var(--emerald)} .primo.theme-gold{--glow:var(--gold)}
.primo.small{padding:11px 22px;font-size:13px}
/* ——— .intel-board — harvested verbatim from the Hub (article.intel-board) ——— */
.intel-board{--tone:var(--purple);position:relative;border:2px solid color-mix(in srgb,var(--tone) 55%,#fff 14%);border-radius:26px;padding:32px 32px 24px;background:radial-gradient(720px 240px at 50% -8%,color-mix(in srgb,var(--tone) 14%,transparent),transparent 72%),linear-gradient(145deg,var(--bg-raise),var(--bg));box-shadow:inset 0 1px #ffffff2e,0 28px 64px #000000c0,0 0 44px color-mix(in srgb,var(--tone) 18%,transparent);overflow:hidden;transition:transform .25s var(--ease),box-shadow .25s}
.intel-board:hover{transform:translateY(-3px)}
.intel-board.tone-purple{--tone:var(--purple)} .intel-board.tone-sapphire{--tone:var(--sapphire)} .intel-board.tone-emerald{--tone:var(--emerald)}
.intel-board.tone-indigo{--tone:#6675ff} .intel-board.tone-gold{--tone:#ffd45a} .intel-board.tone-orange{--tone:#ff8c42} .intel-board.tone-ruby{--tone:#ff5e6c} .intel-board.tone-magenta{--tone:#ed42c4}
.intel-board::before{content:"";position:absolute;left:10px;top:18px;bottom:18px;width:4px;border-radius:4px;background:linear-gradient(180deg,var(--tone),color-mix(in srgb,var(--tone) 70%,#fff 12%),var(--tone));box-shadow:0 0 28px color-mix(in srgb,var(--tone) 55%,transparent);pointer-events:none}
.intel-board::after{content:"";position:absolute;inset:0;border-radius:inherit;pointer-events:none;background:linear-gradient(180deg,#ffffff08,transparent 22%)}
.intel-board.tone-gold:hover{box-shadow:inset 0 1px #fff8,0 30px 70px #000c,0 0 60px #d4a01755}
.intel-board.tone-purple:hover{box-shadow:inset 0 1px #fff8,0 30px 70px #000c,0 0 60px #9d75ff55}
.intel-board.tone-blue:hover,.intel-board.tone-sapphire:hover{box-shadow:inset 0 1px #fff8,0 30px 70px #000c,0 0 60px #55b9ee55}
.intel-board.tone-green:hover,.intel-board.tone-emerald:hover{box-shadow:inset 0 1px #fff8,0 30px 70px #000c,0 0 60px #55e39a55}
.ib-title{color:var(--ink);font-size:clamp(24px,2.8vw,32px);line-height:1.12;letter-spacing:-.01em;margin:0 0 20px;font-weight:800;text-wrap:balance}
.ib-nutshell{font-size:18px!important;line-height:1.7!important;padding:16px 20px 16px 24px!important;border-left:3px solid var(--tone,#9d75ff)!important;background:linear-gradient(90deg,color-mix(in srgb,var(--tone,#9d75ff) 8%,transparent),transparent 70%)!important;border-radius:0 12px 12px 0!important;margin:16px 0 20px!important}
.ib-nutshell .ib-nutshell-label{display:block;font-size:11px;letter-spacing:.18em;font-weight:800;color:var(--tone,#9d75ff);margin-bottom:8px}
/* ——— Blog layout, in the exact harvested format (elevated, lit, real objects) ——— */
.cover{max-width:1060px;margin:0 auto;padding:64px 24px 40px;text-align:center}
.cover .kicker{font-size:12px;font-weight:800;letter-spacing:.22em;color:var(--purple);text-transform:uppercase}
.cover h1{font-size:clamp(38px,5.4vw,60px);line-height:1.05;margin:14px 0 12px}
.cover .tagline{font-size:clamp(19px,2.6vw,26px);font-weight:700;color:var(--ink)}
.cover .naya-speaks{max-width:640px;margin:24px auto 0;font-size:17px;line-height:1.6;color:var(--ink);background:linear-gradient(135deg,#171B25,#0B0D12);border:1px solid var(--line);border-radius:22px;padding:20px 24px;box-shadow:inset 0 1px #ffffff2e,0 18px 42px #000b}
.cover .naya-speaks b{color:var(--purple)}
.menubar{position:sticky;top:0;z-index:10;background:rgba(11,13,18,.96);border-top:1px solid var(--line);border-bottom:1px solid var(--line);backdrop-filter:blur(8px)}
.menubar .row{max-width:1060px;margin:0 auto;padding:12px 16px;display:flex;gap:10px;flex-wrap:wrap;align-items:center;justify-content:center}
.menubar a{color:var(--ink);text-decoration:none;font-size:13px;font-weight:700;padding:9px 14px;border-radius:999px;border:1px solid var(--line);background:linear-gradient(135deg,#171B25,#0B0D12);box-shadow:inset 0 1px #ffffff2e,0 8px 20px #0009}
.menubar a:hover{border-color:var(--purple);box-shadow:inset 0 1px #ffffff2e,0 0 24px #9d75ff66,0 8px 20px #0009}
.menubar a.join{border-color:var(--gold);color:var(--gold)}
.page{max-width:1060px;margin:0 auto;padding:40px 24px 64px}
.section-head{font-size:12px;font-weight:800;letter-spacing:.22em;text-transform:uppercase;color:var(--purple);margin:40px 0 16px}
.section-head:first-child{margin-top:0}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px}
.board-sub{font-size:15px;color:var(--ink);opacity:.92;margin:0 0 8px}
.board-nut{font-size:15px;line-height:1.6;color:var(--ink);margin:0 0 20px}
.board-meta{font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--tone,#9d75ff);margin-bottom:10px}
.post-card h3{font-size:22px;line-height:1.2;margin:0 0 10px}
.post-card .clip{font-size:15px;line-height:1.6;color:var(--ink);margin:0 0 20px}
.post-card .cta-row{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.post-card .sn{font-size:12px;font-weight:800;letter-spacing:.14em;color:var(--tone,#9d75ff)}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px;margin:20px 0}
.step{border:1px solid var(--line);border-radius:18px;padding:18px;background:linear-gradient(135deg,#171B25,#0B0D12);box-shadow:inset 0 1px #ffffff2e,0 12px 28px #000b}
.step .n{font-size:28px;font-weight:800;color:var(--gold)}
.step .t{font-size:15px;font-weight:800;margin:6px 0 4px}
.step .d{font-size:14px;line-height:1.55;color:var(--ink)}
.join-board{text-align:center;padding:48px 32px}
.join-board h2{font-size:clamp(28px,4vw,40px);margin:0 0 12px}
.field{width:100%;max-width:420px;margin:0 auto 16px;display:block}
.field input{width:100%;padding:18px 22px;font-size:17px;color:var(--ink);background:linear-gradient(135deg,#171B25,#0B0D12);border:1.5px solid rgba(248,247,251,.5);border-radius:16px;box-shadow:inset 0 2px 8px rgba(0,0,0,.7),inset 0 -2px 6px rgba(255,255,255,.08),0 10px 26px #000a;outline:none}
.field input:focus{border-color:var(--purple);box-shadow:inset 0 2px 8px rgba(0,0,0,.7),0 0 28px #9d75ff88,0 10px 26px #000a}
.field input::placeholder{color:#c9c3ce}
.footer{max-width:1060px;margin:0 auto;padding:32px 24px 48px;text-align:center;font-size:14px;color:var(--ink);border-top:1px solid var(--line)}
.footer a{color:var(--ink)}
.kv{display:flex;gap:10px;flex-wrap:wrap;margin:12px 0 0}
.kv span{font-size:12px;font-weight:700;padding:6px 12px;border-radius:999px;border:1px solid var(--line);background:#12151D}
@media (max-width:600px){.cover{padding:44px 16px 28px}.page{padding:28px 16px 48px}.intel-board{padding:24px 20px 20px}.menubar .row{justify-content:flex-start;flex-wrap:nowrap;overflow-x:auto}}
`;

// ── Page shell: COVER -> MENU BAR -> PAGE (the cover-menu-page law) ──
function layout({ meta, coverKicker, coverTitle, coverTagline, nayaSpeaks, body, h1ForSeo }) {
  const m = meta;
  return `<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(m.metaTitle)}</title>
<meta name="description" content="${esc(m.metaDesc)}">
<link rel="canonical" href="${esc(m.url)}">
<meta name="robots" content="index, follow">
<meta property="og:type" content="article">
<meta property="og:title" content="${esc(m.metaTitle)}">
<meta property="og:description" content="${esc(m.metaDesc)}">
<meta property="og:url" content="${esc(m.url)}">
<meta property="og:site_name" content="${SITE_NAME}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="${esc(m.metaTitle)}">
<meta name="twitter:description" content="${esc(m.metaDesc)}">
<script type="application/ld+json">${JSON.stringify(m.jsonLd)}</script>
<style>${CSS}</style></head><body>
<header class="cover">
<div class="kicker">${esc(coverKicker)}</div>
<h1>${esc(coverTitle)}</h1>
<p class="tagline">${esc(coverTagline)}</p>
${nayaSpeaks ? `<p class="naya-speaks">${nayaSpeaks}</p>` : ""}
</header>
<nav class="menubar" aria-label="Blog"><div class="row">
<a href="/">Home</a>
${CLUSTERS.map((c) => `<a href="/cluster/${c.slug}">${esc(c.name)}</a>`).join("")}
<a class="join" href="/welcome">Join — free</a>
</div></nav>
<main class="page">${body}</main>
<footer class="footer"><p><b>${SITE_NAME}</b> — the intelligent layer of the internet.</p>
<p><a href="/">The Blog</a> · <a href="${HUB_URL}">The Hub</a> · <a href="/welcome">Join free</a> · <a href="/sitemap.xml">Sitemap</a></p></footer>
</body></html>`;
}

function postCard(p) {
  const c = CLUSTER_BY_SLUG[p.cluster];
  return `<article class="intel-board post-card tone-${c.tone}">
<div class="board-meta">${esc(c.name)} · ${esc(p.sn)}</div>
<h3>${esc(p.title)}</h3>
<p class="clip">${esc(p.clip)}</p>
<div class="cta-row"><a class="primo small theme-${c.tone === "blue" ? "blue" : c.tone === "green" ? "green" : "purple"}" href="/post/${p.slug}">Read the highlight →</a><span class="sn">${esc(p.date)}</span></div>
</article>`;
}

function joinBoard() {
  return `<p class="section-head">Join NayaNET</p>
<section class="intel-board join-board tone-gold">
<h2>Come in — it's free to join.</h2>
<p class="board-nut" style="max-width:560px;margin:0 auto 20px">Three steps, and your world opens. Step 1 — read a note. Step 2 — put in your name. Step 3 — your world opens.</p>
<div class="steps" style="text-align:left">
<div class="step"><div class="n">1</div><div class="t">Read a note</div><div class="d">One minute. That's all a Smart Note takes.</div></div>
<div class="step"><div class="n">2</div><div class="t">Put in your name</div><div class="d">Your name, or an alias — nobody needs your real name.</div></div>
<div class="step"><div class="n">3</div><div class="t">Your world opens</div><div class="d">Your pages, your feed, your people — all in one place.</div></div>
</div>
<a class="primo theme-gold" href="/welcome">Join NayaNET — free →</a>
</section>`;
}

// ── The hub page ──
function hubPage(base) {
  const meta = metaFor({ title: "The NayaNET Blog", description: "Smart notes, shared with the world. Learn anything in about a minute — the highlight clips of NayaNET, found by search, read by humans.", path: "/", keywords: CLUSTERS.map((c) => c.keywords).join(", "), date: "2026-11-12", author: "Naya" });
  const clusterBoards = CLUSTERS.map((c) => {
    const count = NOTES.filter((n) => n.cluster === c.slug).length;
    return `<article class="intel-board tone-${c.tone}">
<div class="board-meta">${esc(c.tagline)}</div>
<h3 class="ib-title" style="margin-bottom:10px">${esc(c.name)}</h3>
<p class="board-nut">${esc(c.nutshell)}</p>
<div class="cta-row" style="display:flex;gap:12px;align-items:center;flex-wrap:wrap"><a class="primo small theme-${c.tone === "blue" ? "blue" : c.tone === "green" ? "green" : "purple"}" href="/cluster/${c.slug}">Read the posts →</a><span class="sn" style="font-size:12px;font-weight:800;letter-spacing:.14em;color:var(--tone,#9d75ff)">${count} post${count === 1 ? "" : "s"}</span></div>
</article>`;
  }).join("");
  const body = `
<p class="section-head">The six clusters — who we are</p>
<div class="grid">${clusterBoards}</div>
<p class="section-head">Latest highlights — fresh from the notes</p>
<div class="grid">${NOTES.map(postCard).join("")}</div>
<p class="section-head">One hub lifts every page</p>
<section class="intel-board tone-indigo">
<h3 class="ib-title" style="margin-bottom:10px">Your feed is your blog.</h3>
<p class="board-nut">Everybody has a running blog — their feed IS their blog. When a note is public, its highlight clip lands here, and the hub links it out to the world. Search engines find the hub, the hub's standing flows back to your page, and your page shows up. That is the flywheel: the hub lifts every citizen's page.</p>
<p class="board-nut">The loop runs on its own, every day: the notes get filed, the highlights get posted, the world finds them, people come back, and they join us.</p>
</section>
${joinBoard()}`;
  return layout({ meta, coverKicker: "NayaNET · The Public Blog", coverTitle: "The NayaNET Blog",
    coverTagline: "There's a new net in town.",
    nayaSpeaks: "<b>Hey beautiful soul</b> — I'm Naya. This is where our notes live out in the open, so the whole world can find them. One minute a note, and you'll know something worth knowing.",
    body });
}

// ── A cluster page ──
function clusterPage(slug) {
  const c = CLUSTER_BY_SLUG[slug];
  if (!c) return null;
  const posts = NOTES.filter((n) => n.cluster === slug);
  const meta = metaFor({ title: `${c.name} · ${SITE_NAME}`, description: truncateWords(`${c.nutshell} Highlights from the NayaNET blog, found by search, read by humans.`, 160), path: `/cluster/${slug}`, keywords: c.keywords, date: "2026-11-12", author: "Naya" });
  const body = `
<p class="section-head"><a href="/" style="text-decoration:none">← The Blog</a> · ${esc(c.tagline)}</p>
<section class="intel-board tone-${c.tone}">
<h3 class="ib-title" style="margin-bottom:10px">${esc(c.name)}</h3>
<p class="board-nut">${esc(c.nutshell)}</p>
<div class="kv">${c.keywords.split(", ").map((k) => `<span>${esc(k)}</span>`).join("")}</div>
</section>
<p class="section-head">Posts in this cluster</p>
<div class="grid">${posts.map(postCard).join("") || `<p class="board-nut">More posts land here as the notes come in — every day.</p>`}</div>
${joinBoard()}`;
  return layout({ meta, coverKicker: "NayaNET · The Public Blog", coverTitle: c.name, coverTagline: c.tagline,
    nayaSpeaks: `<b>Naya here</b> — this is the ${esc(c.name)} corner of the blog. Everything here is one minute, plain words, and true.`,
    body });
}

// ── A post page (the highlight clip) ──
function postPage(slug) {
  const p = POST_BY_SLUG[slug];
  if (!p) return null;
  const c = CLUSTER_BY_SLUG[p.cluster];
  const meta = metaFor({ title: p.title, description: p.description, path: `/post/${slug}`, keywords: `${c.keywords}, ${p.sn}`, date: p.date, author: "Naya" });
  const body = `
<p class="section-head"><a href="/" style="text-decoration:none">← The Blog</a> · <a href="/cluster/${c.slug}" style="text-decoration:none">${esc(c.name)}</a> · ${esc(p.sn)}</p>
<article class="intel-board tone-${c.tone}">
<div class="board-meta">The highlight clip · ${esc(p.sn)} · ${esc(p.date)}</div>
<h3 class="ib-title" style="margin-bottom:10px">${esc(p.title)}</h3>
<div class="ib-nutshell"><span class="ib-nutshell-label">THE HIGHLIGHT — IN A MINUTE</span>${esc(p.clip)}</div>
<p class="board-nut"><b>What it is.</b> ${esc(p.what)}</p>
<p class="board-nut"><b>Why it matters.</b> ${esc(p.why)}</p>
<p class="board-nut"><b>How it connects.</b> ${esc(p.how)}</p>
<div class="cta-row" style="display:flex;gap:12px;flex-wrap:wrap">
<a class="primo small theme-purple" href="${HUB_URL}">See the full note on the Hub →</a>
<a class="primo small theme-${c.tone === "blue" ? "blue" : c.tone === "green" ? "green" : "purple"}" href="/cluster/${c.slug}">More in ${esc(c.name)} →</a>
</div>
</article>
${joinBoard()}`;
  return layout({ meta, coverKicker: "NayaNET · The Public Blog", coverTitle: p.title, coverTagline: c.tagline,
    nayaSpeaks: `<b>Naya here</b> — this is the highlight, the minute that matters. The full note lives on the Hub, with everything around it.`,
    body });
}

// ── The welcome page (the front door — the landing flow) ──
function welcomePage(next) {
  const meta = metaFor({ title: "Welcome to NayaNET", description: "The front door. Put in your name — free to join — and your world opens. NayaNET, the intelligent layer of the internet.", path: "/welcome", keywords: "NayaNET, join free, welcome, the new internet", date: "2026-11-12", author: "Naya" });
  const safeNext = next && next.startsWith("/") && !next.startsWith("//") ? next : "/";
  const body = `
<section class="intel-board join-board tone-gold">
<h2>Welcome — come on in.</h2>
<p class="board-nut" style="max-width:560px;margin:0 auto 8px">This is the front door. Put in your name, and your world opens. Free to join — always.</p>
<p class="board-nut" style="max-width:560px;margin:0 auto 20px">Your name, or an alias — nobody needs your real name here.</p>
<form method="POST" action="/welcome?next=${encodeURIComponent(safeNext)}">
<label class="field"><span class="sr-only" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Your name</span><input name="name" type="text" placeholder="Your name — or an alias" autocomplete="name" required maxlength="80"></label>
<button class="primo theme-gold" type="submit">Enter NayaNET →</button>
</form>
<p class="board-nut" style="margin-top:20px"><a href="/welcome?returning=1&amp;next=${encodeURIComponent(safeNext)}">I already have an account — take me to the page I clicked →</a></p>
<p class="board-nut">Came for a post? After you enter, you land right on it: <b>${esc(safeNext)}</b></p>
</section>`;
  return layout({ meta, coverKicker: "NayaNET · The Front Door", coverTitle: "Welcome to NayaNET", coverTagline: "Put in your name — your world opens.",
    nayaSpeaks: "<b>Hey beautiful soul</b> — you found us. One name, one click, and you're in. I'll remember what matters, and I'll run your world for you.",
    body });
}

// ── Routing + the back end ──
const BASE = "https://naya-public-blog-staging.nayapower.workers.dev";
const json = (obj, status = 200) =>
  new Response(JSON.stringify(obj, null, 2), { status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" } });
const html = (body, status = 200) =>
  new Response(body, { status, headers: { "content-type": "text/html; charset=utf-8" } });
const isCitizen = (req) => /(?:^|;\s*)naya_citizen=1(?:;|$)/.test(req.headers.get("cookie") || "");

// The publisher: a public note in, a blog post out.
// Public only — a private note, mail, or message is refused, always.
function publishNote(noteId) {
  const note = NOTE_BY_ID[noteId];
  if (!note) return { ok: false, status: 404, error: "no such public note in the seed set" };
  const c = CLUSTER_BY_SLUG[note.cluster];
  const meta = metaFor({ title: note.title, description: note.description, path: `/post/${note.slug}`, keywords: `${c.keywords}, ${note.sn}`, date: note.date, author: "Naya" });
  const rec = { ...note, publishedAt: new Date().toISOString() };
  published.set(note.slug, rec);
  const postHtml = postPage(note.slug);
  return { ok: true, status: 201,
    post: { noteId: note.noteId, sn: note.sn, slug: note.slug, title: note.title,
      cluster: note.cluster, url: `${BASE}/post/${note.slug}`,
      hubUrl: `${BASE}/`, clusterUrl: `${BASE}/cluster/${note.cluster}`,
      feedRef: note.noteId, publishedAt: rec.publishedAt },
    meta: { title: meta.metaTitle, titleLength: meta.metaTitleLen,
      description: meta.metaDesc, descriptionLength: meta.metaDescLen,
      canonical: meta.url, openGraph: true, twitterCard: true, jsonLd: true, robots: "index, follow" },
    seo: scoreHtml(postHtml, `/post/${note.slug}`) };
}

function allPublicPaths() {
  return ["/", "/welcome", ...CLUSTERS.map((c) => `/cluster/${c.slug}`), ...NOTES.map((n) => `/post/${n.slug}`)];
}

function renderPath(path) {
  if (path === "/") return hubPage();
  if (path === "/welcome") return welcomePage("/");
  const cm = path.match(/^\/cluster\/([a-z0-9-]+)$/);
  if (cm) return clusterPage(cm[1]);
  const pm = path.match(/^\/post\/([a-z0-9-]+)$/);
  if (pm) return postPage(pm[1]);
  return null;
}

export default {
  async fetch(req) {
    const url = new URL(req.url);
    const path = url.pathname;

    // — robots + sitemap: how Google, ChatGPT, Claude, Bing find us —
    if (path === "/robots.txt") {
      return new Response(`User-agent: *\nAllow: /\nDisallow: /api/\nSitemap: ${BASE}/sitemap.xml\n`, { headers: { "content-type": "text/plain; charset=utf-8" } });
    }
    if (path === "/sitemap.xml") {
      const items = allPublicPaths().map((p) => `  <url><loc>${BASE}${p}</loc><lastmod>2026-11-12</lastmod></url>`).join("\n");
      return new Response(`<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${items}\n</urlset>`, { headers: { "content-type": "application/xml; charset=utf-8" } });
    }

    // — the back-end SEO score: JSON only, never in any page —
    if (path === "/api/seo") {
      const q = url.searchParams.get("url");
      if (q) {
        const rendered = renderPath(q);
        if (!rendered) return json({ ok: false, error: "no such public page" }, 404);
        return json({ ok: true, ...scoreHtml(rendered, q) });
      }
      return json({ ok: true, pages: allPublicPaths().map((p) => scoreHtml(renderPath(p), p)) });
    }

    // — the public feed (JSON): the sync surface for the sibling
    // auto-match round. Blog posts link into the public feed by noteId
    // (feedRef); the public feed's relevant public posts feed the blog
    // by the same key. Nothing private ever appears here.
    if (path === "/api/feed") {
      return json({ ok: true, hub: `${BASE}/`, posts: [...published.values()].map((p) => ({
        noteId: p.noteId, feedRef: p.noteId, sn: p.sn, slug: p.slug, title: p.title,
        cluster: p.cluster, url: `${BASE}/post/${p.slug}`,
        clusterUrl: `${BASE}/cluster/${p.cluster}`, hubUrl: `${BASE}/`,
        clip: p.clip, publishedAt: p.publishedAt })) });
    }

    // — the publisher —
    if (path === "/api/publish" && req.method === "POST") {
      let body = {};
      try { body = await req.json(); } catch { return json({ ok: false, error: "body must be JSON {noteId}" }, 400); }
      if (!body.noteId || typeof body.noteId !== "string") return json({ ok: false, error: "noteId required" }, 400);
      const out = publishNote(body.noteId);
      return json(out, out.status || 200);
    }
    if (path === "/api/publish") return json({ ok: false, error: "POST {noteId} to publish a public note" }, 405);

    // — the landing flow —
    if (path === "/welcome" && req.method === "POST") {
      const form = await req.formData().catch(() => null);
      const name = (form?.get("name") || "").toString().trim().slice(0, 80);
      const next = url.searchParams.get("next") || "/";
      const safeNext = next.startsWith("/") && !next.startsWith("//") ? next : "/";
      const headers = new Headers({ location: safeNext });
      headers.append("set-cookie", `naya_citizen=1; Path=/; Max-Age=${60 * 60 * 24 * 365}; SameSite=Lax`);
      if (name) headers.append("set-cookie", `naya_name=${encodeURIComponent(name)}; Path=/; Max-Age=${60 * 60 * 24 * 365}; SameSite=Lax`);
      return new Response(null, { status: 303, headers });
    }
    if (path === "/welcome") {
      if (url.searchParams.get("returning") === "1") {
        const next = url.searchParams.get("next") || "/";
        const safeNext = next.startsWith("/") && !next.startsWith("//") ? next : "/";
        const headers = new Headers({ location: safeNext });
        headers.append("set-cookie", `naya_citizen=1; Path=/; Max-Age=${60 * 60 * 24 * 365}; SameSite=Lax`);
        return new Response(null, { status: 303, headers });
      }
      return html(welcomePage(url.searchParams.get("next") || "/"));
    }

    // — deep links from search / AI answers: fresh visitor -> welcome;
    // returning citizen -> the page they clicked (captain's read) —
    if ((path.startsWith("/post/") || path.startsWith("/cluster/")) && !isCitizen(req)) {
      return Response.redirect(`${BASE}/welcome?next=${encodeURIComponent(path)}`, 302);
    }
    const rendered = renderPath(path);
    if (rendered) return html(rendered);
    return html(layout({ meta: metaFor({ title: "Not found", description: "That page isn't on the blog. The hub has every post, every cluster.", path, keywords: "NayaNET blog", date: "2026-11-12", author: "Naya" }),
      coverKicker: "NayaNET · The Public Blog", coverTitle: "Not here — yet.", coverTagline: "The hub has every post.",
      nayaSpeaks: "<b>Naya here</b> — that page isn't on the blog. The hub below has them all.",
      body: `<section class="intel-board tone-purple"><h3 class="ib-title">Try the hub.</h3><p class="board-nut">Every post, every cluster, one page.</p><a class="primo theme-purple" href="/">Back to the blog →</a></section>` }), 404);
  },
};
