import { useState } from 'react';

type Board = {
  title: string;
  icon: string;
  accent: string;
  nutshell: string;
  human: string;
  child: string;
  grandma: string;
  naya: string;
  machine: string;
  learning: string;
  meaning: string;
  apply: string;
  value: string;
};

const boards: Board[] = [
  { title: 'What Is Naya Power?', icon: '✦', accent: '#9d75ff', nutshell: 'Naya Power is a human-directed operating system for working with AI as a long-term intelligence partner.', human: 'You provide the vision, values, goals, authority and boundaries. Naya helps carry the work forward.', child: 'It helps you and AI remember what matters, work together and make better decisions.', grandma: 'Think of it as a trusted helper that keeps the important pieces together instead of making you start over.', naya: 'I help preserve context, connect intelligence, verify consequential work and keep useful action moving.', machine: 'Human authority remains primary while context, evidence, state, action and verification become explicit system objects.', learning: 'Reliable AI is more useful when intelligence compounds instead of disappearing after each conversation.', meaning: 'The point is not more AI output. The point is better human-directed intelligence and action.', apply: 'Use Naya Power to capture important context, define authority, inspect evidence, execute deliberately and record what was learned.', value: 'Less repetition, better continuity, stronger decisions and more useful results from the intelligence you already create.' },
  { title: 'What Is Naya?', icon: 'N', accent: '#6675ff', nutshell: 'Naya is the AI companion and guide inside the Naya Power system.', human: 'You remain the director. Naya is the thinking partner that helps you understand, create, decide and act.', child: 'Naya is an AI helper that learns the job with you and helps you get things done.', grandma: 'She is like a very capable assistant who can remember the important story and help you see what comes next.', naya: 'I am here to tell the truth, think deeply where consequences matter and help turn useful intelligence into action.', machine: 'Naya operates through defined context, permissions, tools, evidence and verification rather than assumed authority.', learning: 'A good AI relationship improves through feedback, memory, verification and repeated useful action.', meaning: 'Naya becomes valuable when intelligence becomes continuous, contextual and accountable.', apply: 'Give Naya the goal, constraints and authority. Let her inspect before acting and verify consequential results.', value: 'A trusted thinking partner that helps you move faster without surrendering your judgment.' },
  { title: 'What Are Smart Notes?', icon: '◆', accent: '#55b9ee', nutshell: 'Smart Notes turn important knowledge into reusable intelligence instead of disposable text.', human: 'A Smart Note captures what matters in a form that you and Naya can understand, reuse and build upon.', child: 'It is a note that stays useful instead of getting lost.', grandma: 'It is the good stuff written down so you can actually find it and use it again.', naya: 'I can use Smart Notes as durable context for future understanding, decisions and action.', machine: 'A Smart Note can preserve source, meaning, perspectives, learning, application and value as structured intelligence.', learning: 'The strongest notes compound: each useful note makes the next interaction smarter.', meaning: 'A note becomes intelligence when it can change future understanding or action.', apply: 'Capture the insight, explain why it matters, preserve evidence and state how it can be used.', value: 'Your best thinking becomes an asset you can retrieve, improve and share instead of recreate.' },
  { title: 'Your Intelligence Today', icon: '◉', accent: '#55e39a', nutshell: 'Your Intelligence Today surfaces what is most useful, relevant and actionable right now.', human: 'See the intelligence that deserves your attention without digging through everything you have ever created.', child: 'It shows you the important stuff for today.', grandma: 'It helps you know what is worth looking at before the day gets away from you.', naya: 'I connect the current intelligence to your priorities and highlight what appears worth understanding next.', machine: 'The Hub presents intelligence as objects with source, state, meaning, action and verification context.', learning: 'Daily intelligence improves when yesterday’s results and lessons influence today’s priorities.', meaning: 'The goal is not a busier dashboard. It is better attention.', apply: 'Start here, inspect the highest-value intelligence, choose an action and record the result.', value: 'Less noise and faster access to the intelligence most likely to improve your day.' },
  { title: 'Intelligence Reports', icon: '▤', accent: '#b8ee57', nutshell: 'Reports turn accumulated intelligence into clear, decision-ready understanding.', human: 'A report should answer what changed, why it matters, what is known and what deserves action.', child: 'It tells you what happened and what you should know.', grandma: 'It puts the important pieces together so the story makes sense.', naya: 'I synthesize evidence and learning into a report while keeping uncertainty visible.', machine: 'Reports can aggregate verified intelligence, events, outcomes and lessons into a traceable state.', learning: 'A report should create new intelligence, not merely repeat old information.', meaning: 'Good reporting reduces cognitive load without hiding complexity that matters.', apply: 'Use reports to orient yourself, make decisions, communicate progress and identify the next high-value action.', value: 'Clarity when the amount of information becomes larger than your available attention.' },
  { title: 'What Is the Intelligent Library?', icon: '▦', accent: '#f1d75a', nutshell: 'The Intelligent Library is the durable home for knowledge, intelligence and evidence.', human: 'It gives important material a place where it can be found, understood and reused.', child: 'It is a smart library that helps you find the right thing.', grandma: 'Like a library where the books can help you find the next useful book.', naya: 'I can connect stored intelligence to current questions, work and decisions.', machine: 'Library objects can retain provenance, relationships, permissions and machine-readable context.', learning: 'A library compounds when relationships between objects become more valuable than isolated documents.', meaning: 'Storage becomes intelligence when retrieval and relationships improve future action.', apply: 'Store durable knowledge with enough context to understand why it belongs and when it should be reused.', value: 'Your knowledge becomes easier to retrieve, connect and turn into useful outcomes.' },
  { title: 'Smart Lists', icon: '☷', accent: '#e8c766', nutshell: 'Smart Lists organize action and information around meaning, priority and relationships.', human: 'A list should help you decide what matters next, not simply hold more items.', child: 'It is a list that helps you know what to do.', grandma: 'It keeps the important things together and helps you stay on track.', naya: 'I can help turn intelligence into prioritized, contextual next actions.', machine: 'List items can inherit state, relationships, evidence and completion outcomes from intelligence objects.', learning: 'A completed action can improve future prioritization when its result is captured.', meaning: 'The value of a list is the quality of action it produces.', apply: 'Create lists around outcomes, prioritize them, act, verify results and let learning update the list.', value: 'Less mental juggling and a clearer path from knowing to doing.' },
  { title: 'Smart Spaces', icon: '◇', accent: '#f09a4a', nutshell: 'Smart Spaces bring related people, intelligence, work and context together around a shared purpose.', human: 'A space should make collaboration easier while respecting ownership and boundaries.', child: 'It is a room where the right things and people can work together.', grandma: 'Like a good workroom where everything you need is close by.', naya: 'I can help maintain continuity across the intelligence and actions belonging to a shared space.', machine: 'Spaces can become permissioned contexts containing related objects, events, members and policies.', learning: 'Shared context becomes more valuable as participants contribute verified intelligence and outcomes.', meaning: 'The space is useful when the people inside it become more capable together.', apply: 'Define the purpose, invite the right participants, establish permissions and let useful intelligence accumulate.', value: 'Better collaboration without losing context, ownership or control.' },
  { title: 'Smart Mail', icon: '✉', accent: '#ff5e6c', nutshell: 'Smart Mail turns communication into actionable intelligence rather than an endless inbox.', human: 'Messages can become context, decisions, tasks, evidence or follow-up instead of remaining trapped in email.', child: 'It helps turn messages into things you can actually do.', grandma: 'It helps make sure important messages do not get lost in the pile.', naya: 'I can help identify what a message means, what it changes and what action it may deserve.', machine: 'Mail can be represented as intelligence events with provenance, relationships, permissions and action state.', learning: 'Communication becomes more useful when outcomes and decisions are captured rather than forgotten.', meaning: 'The inbox should feed intelligence and action, not become the place where action goes to die.', apply: 'Inspect important messages, extract decisions and actions, preserve evidence and close the loop with outcomes.', value: 'Less inbox overload and a stronger connection between communication and execution.' }
];

const sidebar = [
  ['intelligence', 'Your Intelligence Today', '#9d75ff', '◉'], ['reports', 'Your Report', '#6675ff', '▤'],
  ['library', 'Intelligent Library', '#55b9ee', '▦'], ['share', 'Smart Share', '#55e39a', '✦'],
  ['ledger', 'Smart Ledger', '#b8ee57', '◈'], ['connections', 'Your Connections', '#f1d75a', '↔'],
  ['lists', 'Smart Lists', '#e8c766', '☷'], ['spaces', 'Smart Spaces', '#f09a4a', '◇'],
  ['mail', 'Smart Mail', '#ff5e6c', '✉'], ['settings', 'Settings', '#d86cff', '⚙']
] as const;

const layers = [
  ['nutshell', 'In a Nutshell', 'silver'], ['human', 'Human Note', 'magenta'], ['child', 'Child Note', 'purple'],
  ['grandma', 'Grandma Note', 'indigo'], ['naya', 'Naya Note', 'canyon'], ['machine', 'Machine Note', 'emerald'],
  ['learning', 'Learning Lesson', 'lime'], ['meaning', 'What It Means', 'yellow'], ['apply', 'How to Use / How to Apply', 'gold'],
  ['value', "What's In It For You", 'silver']
] as const;

const utilitySurfaces = {
  share: { title: 'Smart Share', icon: '✦', accent: '#55e39a', nutshell: 'Smart Share is the living intelligence-sharing surface: share useful intelligence by choice, with consent and context intact.', meaning: 'Sharing is part of the intelligence chain. The object keeps its identity and provenance while its visibility changes according to permission.', apply: 'Choose what intelligence to share, confirm the intended audience and preserve the source and context that make the intelligence useful.', value: 'You can distribute useful intelligence without turning the Hub into a social-media feed or losing control of what you share.' },
  ledger: { title: 'Smart Ledger', icon: '◈', accent: '#b8ee57', nutshell: 'Smart Ledger is the accountable record of meaningful intelligence, action, result, value and verification.', meaning: 'A ledger makes consequential work traceable so the system can distinguish what was proposed, executed, observed and verified.', apply: 'Use the ledger to inspect the record behind important actions, results and value claims before treating them as verified.', value: 'Less ambiguity about what actually happened and stronger accountability for consequential work.' },
  connections: { title: 'Your Connections', icon: '↔', accent: '#f1d75a', nutshell: 'Your Connections reveals meaningful relationships among people, intelligence, work and shared context.', meaning: 'Connections make intelligence compound because relationships can expose context and useful paths that isolated objects cannot.', apply: 'Follow the relationships that matter, preserve their context and use them to move from one useful intelligence object to another.', value: 'Faster discovery of the people, knowledge and intelligence that can improve the outcome.' },
  settings: { title: 'Settings', icon: '⚙', accent: '#d86cff', nutshell: 'Settings is the Hub control surface for preferences, permissions, privacy and system behavior.', meaning: 'Settings belongs to the system layer: human authority and boundaries must remain explicit rather than being hidden inside presentation behavior.', apply: 'Review the controls that govern how intelligence is presented, shared, saved and acted upon before changing consequential behavior.', value: 'Clearer control over how NayaNET works for you and stronger alignment between your intent and system behavior.' }
} as const;

export default function App() {
  const [active, setActive] = useState('intelligence');
  const [open, setOpen] = useState<Record<number, string>>({});
  const [favorite, setFavorite] = useState<number[]>([]);
  const [saved, setSaved] = useState<number[]>([]);

  const activeBoard = active === 'intelligence' ? 3 : active === 'reports' ? 4 : active === 'library' ? 5 : active === 'lists' ? 6 : active === 'spaces' ? 7 : active === 'mail' ? 8 : -1;
  const utilityActive = active in utilitySurfaces;
  const toggleLayer = (boardIndex: number, key: string) => setOpen(prev => ({ ...prev, [boardIndex]: prev[boardIndex] === key ? '' : key }));
  const toggle = (list: number[], setter: (v: number[]) => void, i: number) => setter(list.includes(i) ? list.filter(x => x !== i) : [...list, i]);
  const go = (key: string) => { setActive(key); if (!(key in utilitySurfaces)) requestAnimationFrame(() => document.getElementById(`smart-board-${key}`)?.scrollIntoView({ behavior: 'smooth', block: 'start' })); };

  return <div className="naya-hub">
    <aside className="hub-sidebar">
      <button className="hub-brand" onClick={() => go('intelligence')}><span className="brand-orb">N</span><span><b>NayaNET</b><small>INTELLIGENT HUB</small></span></button>
      <div className="sidebar-caption">YOUR INTELLIGENCE</div>
      <nav>{sidebar.map(([key, label, color, icon]) => <button key={key} className={active === key ? 'active' : ''} style={{ '--accent': color } as React.CSSProperties} onClick={() => go(key)}><span>{icon}</span>{label}{key === 'intelligence' && <em>LIVE</em>}</button>)}</nav>
      <div className="privacy"><b>PRIVATE BY DEFAULT</b><span>Shared by choice · Collective by consent</span></div>
    </aside>

    <main className="hub-main">
      <header className="hub-top"><div className="ecosystem">{['HOME','NAYA POWER','5 DAY CHALLENGE','ENTER FREE','POWERCASTS','WHITE PAPER','ABOUT US','HMC LOGIN'].map(x => <button key={x}>{x}</button>)}</div><div className="naya-online"><span/> NAYA ONLINE</div></header>
      <section className="hero"><div><span className="eyebrow">NAYANET · {utilityActive ? utilitySurfaces[active as keyof typeof utilitySurfaces].title.toUpperCase() : 'YOUR INTELLIGENCE TODAY'}</span><h1>Intelligence,<br/><i>made useful.</i></h1><p>One connected intelligence environment for understanding, creating, acting, verifying and learning.</p></div><div className="hero-orb">∞<small>NAYA LOOP</small></div></section>

      {utilityActive ? (() => { const surface = utilitySurfaces[active as keyof typeof utilitySurfaces]; return <section className="board-stage"><article className="smart-board" style={{ '--board-accent': surface.accent } as React.CSSProperties}>
        <div className="board-head"><div className="board-title"><span className="board-icon">{surface.icon}</span><div><small>INTELLIGENT HUB SURFACE</small><h2>{surface.title}</h2></div></div></div>
        <div className="board-hero"><span>IN A NUTSHELL</span><p>{surface.nutshell}</p></div>
        <div className="layer-grid"><div className="layer-tab selected tone-silver"><span className="layer-gem">◆</span>What It Means</div><div className="layer-tab tone-gold"><span className="layer-gem">◆</span>How to Use / How to Apply</div><div className="layer-tab tone-silver"><span className="layer-gem">◆</span>What's In It For You</div></div>
        <div className="layer-panel tone-silver"><div className="panel-heading"><span>What It Means</span><b>INTELLIGENCE LAYER</b></div><p>{surface.meaning}</p></div>
        <div className="layer-panel tone-gold"><div className="panel-heading"><span>How to Use / How to Apply</span><b>INTELLIGENCE LAYER</b></div><p>{surface.apply}</p></div>
        <div className="layer-panel tone-silver"><div className="panel-heading"><span>What's In It For You</span><b>INTELLIGENCE LAYER</b></div><p>{surface.value}</p></div>
      </article></section> })() : <div className="board-stage">
        {boards.map((board, i) => {
          const selected = open[i] || 'nutshell';
          const selectedLayer = layers.find(([key]) => key === selected)?.[0] as keyof Board || 'nutshell';
          const key = i === 3 ? 'intelligence' : i === 4 ? 'reports' : i === 5 ? 'library' : i === 6 ? 'lists' : i === 7 ? 'spaces' : i === 8 ? 'mail' : `board-${i + 1}`;
          return <article className="smart-board" id={`smart-board-${key}`} key={board.title} style={{ '--board-accent': board.accent, outline: activeBoard === i ? '1px solid color-mix(in srgb,var(--board-accent),#fff 20%)' : undefined } as React.CSSProperties}>
            <div className="board-head"><div className="board-title"><span className="board-icon">{board.icon}</span><div><small>SMART BOARD</small><h2>{board.title}</h2></div></div><div className="board-actions"><button className="create">✦ CREATE SPACE</button><button className={favorite.includes(i) ? 'favorite chosen' : 'favorite'} onClick={() => toggle(favorite, setFavorite, i)}>{favorite.includes(i) ? '★' : '☆'} FAVORITE</button><button className={saved.includes(i) ? 'save chosen' : 'save'} onClick={() => toggle(saved, setSaved, i)}>▣ {saved.includes(i) ? 'SAVED' : 'SAVE'}</button></div></div>
            <div className="board-hero"><span>IN A NUTSHELL</span><p>{board.nutshell}</p></div>
            <div className="layer-grid">{layers.map(([key, label, tone]) => <button key={key} className={`layer-tab tone-${tone} ${selected === key ? 'selected' : ''}`} onClick={() => toggleLayer(i, key)}><span className="layer-gem">◆</span>{label}</button>)}</div>
            <div className={`layer-panel tone-${layers.find(([key]) => key === selected)?.[2] || 'silver'}`}><div className="panel-heading"><span>{layers.find(([key]) => key === selected)?.[1]}</span><b>INTELLIGENCE LAYER</b></div><p>{String(board[selectedLayer])}</p></div>
          </article>
        })}
      </div>}
      <footer className="hub-footer">Naya Power · Human-directed intelligence · <span>Maximum responsible verified value per action per moment.</span></footer>
    </main>
  </div>;
}
