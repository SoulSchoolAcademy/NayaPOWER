import { useEffect, useRef, useState } from 'react';
import { createRoot, type Root } from 'react-dom/client';
import source from './hub-baseline.html?raw';
import { SmartMailSurface } from '../app/SmartMailSurface';
import '../styles/naya-mail-baseline.css';

const bridge = `
<script>
(() => {
  const signal = (name) => window.parent.postMessage({ type: 'NAYANET_HUB_ACTION', action: name }, '*');
  document.addEventListener('click', (event) => {
    const el = event.target.closest('[data-page="mail"]');
    if (el) {
      event.preventDefault();
      event.stopImmediatePropagation();
      signal('mail');
    }
  }, true);
})();
</script>`;

export function HubBaselineApp() {
  const frame = useRef<HTMLIFrameElement>(null);
  const mailRoot = useRef<Root | null>(null);
  const [mailOpen, setMailOpen] = useState(() => new URLSearchParams(location.search).get('surface') === 'mail');

  useEffect(() => {
    const onMessage = (event: MessageEvent) => {
      if (event.source !== frame.current?.contentWindow) return;
      if (event.data?.type === 'NAYANET_HUB_ACTION' && event.data.action === 'mail') {
        setMailOpen(true);
        history.replaceState(null, '', '?surface=mail');
      }
    };
    window.addEventListener('message', onMessage);
    return () => window.removeEventListener('message', onMessage);
  }, []);

  useEffect(() => {
    if (!mailOpen) return;
    const mount = document.getElementById('naya-mail-react-root');
    if (!mount) return;
    if (!mailRoot.current) mailRoot.current = createRoot(mount);
    mailRoot.current.render(<SmartMailSurface />);
  }, [mailOpen]);

  useEffect(() => () => {
    mailRoot.current?.unmount();
    mailRoot.current = null;
  }, []);

  if (mailOpen) {
    return (
      <div style={{ minHeight: '100vh', background: '#050507' }}>
        <div id="naya-mail-react-root" />
      </div>
    );
  }

  return (
    <iframe
      ref={frame}
      title="NayaNET Intelligent Hub"
      srcDoc={source.replace('</body>', bridge + '</body>')}
      style={{ width: '100%', minHeight: '100vh', height: '100vh', border: 0, display: 'block', background: '#050507' }}
      allow="clipboard-read; clipboard-write"
    />
  );
}