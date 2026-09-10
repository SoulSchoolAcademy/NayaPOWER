import { useEffect, useState } from 'react';
import type { ReactNode } from 'react';
import { useIdentity } from '../identity/session';
import { routes } from './routes';

type ShellProps = { children: (path: string) => ReactNode };

const nav: [string, string, string][] = [
  ['Home', routes.home, '⌂'],
  ['Smart Feed', routes.feed, '✦'],
  ['Smart Notes', routes.notes, '◈'],
  ['Today', routes.today, '◷'],
  ['Reports', routes.reports, '▤'],
  ['Library', routes.library, '▦'],
  ['Collective', routes.collective, '◎'],
  ['Evidence', routes.evidence, '◉'],
  ['Connections', routes.connections, '↔'],
  ['Smart Mail', routes.mail, '✉'],
  ['Smart Space', routes.space, '◌'],
];

function normalize(path: string) {
  if (path.length > 1 && path.endsWith('/')) return path.slice(0, -1);
  return path || '/';
}

export function AppShell({ children }: ShellProps) {
  const id = useIdentity();
  const [path, setPath] = useState(() => normalize(window.location.pathname));
  const [query, setQuery] = useState('');

  useEffect(() => {
    const onPop = () => setPath(normalize(window.location.pathname));
    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
  }, []);

  const go = (next: string) => {
    if (next === path) return;
    window.history.pushState({}, '', next);
    setPath(next);
  };

  const submitQuery = () => {
    if (!query.trim()) return;
    go(routes.feed);
    window.dispatchEvent(new CustomEvent('nayanet:search', { detail: { query: query.trim() } }));
  };

  const current = nav.find(([, route]) => route === path);
  const label = current?.[0] || 'NayaNET';

  return (
    <div className="app" data-shell-owner="AppShell" data-route={path} data-runtime-marker="NAYANET-HUB-REACT-CANONICAL">
      <aside className="sidebar">
        <button className="brand" onClick={() => go(routes.home)} aria-label="Go to NayaNET home">
          <span className="logo"><span>N</span></span>
          <span className="brand-copy"><b>NayaNET</b><small>INTELLIGENT HUB</small></span>
        </button>

        <div className="navlabel">YOUR INTELLIGENCE</div>
        <nav className="nav" aria-label="NayaNET navigation">
          {nav.map(([name, route, icon]) => (
            <button key={route} className={path === route ? 'active' : ''} onClick={() => go(route)} aria-current={path === route ? 'page' : undefined}>
              <span className="ico" aria-hidden="true">{icon}</span>
              <span>{name}</span>
            </button>
          ))}
        </nav>

        <button className="settings-link" onClick={() => go(routes.settings)} aria-current={path === routes.settings ? 'page' : undefined}>
          <span className="ico" aria-hidden="true">⚙</span><span>Settings</span>
        </button>

        <div className="sidefoot">
          <span className="privacy-dot" />
          <div><b>PRIVATE BY DEFAULT</b><small>Shared by choice · Collective by consent</small></div>
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <div className="top-context">
            <span className="top-eyebrow">NAYANET</span>
            <span className="top-divider" />
            <strong>{label}</strong>
          </div>

          <div className="universal-search">
            <span className="search-icon" aria-hidden="true">⌕</span>
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              onKeyDown={(event) => { if (event.key === 'Enter') submitQuery(); }}
              aria-label="Search or talk to Naya"
              placeholder="Search or talk to Naya…"
            />
            <kbd>⌘ K</kbd>
            <button className="talk-button" onClick={submitQuery}>TALK TO NAYA</button>
          </div>

          <button className="identity-chip" onClick={() => go(routes.settings)} aria-label="Open account settings">
            <span className="identity-avatar">{(id.smart_name || 'N').slice(0, 1).toUpperCase()}</span>
            <span><b>{id.smart_name}</b><small>@{id.smart_alias}</small></span>
          </button>
        </header>

        <section className="home">{children(path)}</section>
      </main>
    </div>
  );
}
