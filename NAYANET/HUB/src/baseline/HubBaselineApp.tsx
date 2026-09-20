import { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import source from './hub-baseline.html?raw';
import mailCss from '../styles/naya-mail-baseline.css?raw';
import { SmartMailSurface } from '../app/SmartMailSurface';

export function HubBaselineApp() {
  const frameRef = useRef<HTMLIFrameElement>(null);
  const [mailRoot, setMailRoot] = useState<HTMLElement | null>(null);

  useEffect(() => {
    const frame = frameRef.current;
    if (!frame) return;

    const boot = () => {
      const doc = frame.contentDocument;
      if (!doc) return;

      if (!doc.getElementById('naya-react-mail-style')) {
        const style = doc.createElement('style');
        style.id = 'naya-react-mail-style';
        style.textContent = mailCss + `
          body.naya-react-mail-open .main > :not(.top):not(#naya-react-mail-root),
          body.naya-react-mail-open .mission,
          body.naya-react-mail-open .features { display: none !important; }
          #naya-react-mail-root { min-height: calc(100vh - 82px); }
        `;
        doc.head.appendChild(style);
      }

      let root = doc.getElementById('naya-react-mail-root');
      if (!root) {
        root = doc.createElement('div');
        root.id = 'naya-react-mail-root';
        const main = doc.querySelector('.main');
        const top = main?.querySelector('.top');
        if (!main) return;
        if (top?.nextSibling) main.insertBefore(root, top.nextSibling);
        else main.appendChild(root);
      }

      const setMailMode = (open: boolean) => {
        doc.body.classList.toggle('naya-react-mail-open', open);
        setMailRoot(open ? root : null);
      };

      const buttons = [...doc.querySelectorAll<HTMLElement>('[data-page]')];
      const handlers = buttons.map((button) => {
        const handler = (event: Event) => {
          const page = button.getAttribute('data-page');
          if (page !== 'mail') {
            setMailMode(false);
            return;
          }
          event.preventDefault();
          event.stopPropagation();
          setMailMode(true);
        };
        button.addEventListener('click', handler, true);
        return [button, handler] as const;
      });

      if (new URLSearchParams(window.location.search).get('surface') === 'mail') {
        setMailMode(true);
      }

      return () => {
        handlers.forEach(([button, handler]) => button.removeEventListener('click', handler, true));
        doc.body.classList.remove('naya-react-mail-open');
      };
    };

    frame.addEventListener('load', boot);
    if (frame.contentDocument?.readyState === 'complete') boot();

    return () => frame.removeEventListener('load', boot);
  }, []);

  return (
    <>
      <iframe
        ref={frameRef}
        title="NayaNET Intelligent Hub"
        srcDoc={source}
        style={{
          width: '100%',
          minHeight: '100vh',
          height: '100vh',
          border: 0,
          display: 'block',
          background: '#050507',
        }}
        allow="clipboard-read; clipboard-write"
      />
      {mailRoot ? createPortal(<SmartMailSurface />, mailRoot) : null}
    </>
  );
}
