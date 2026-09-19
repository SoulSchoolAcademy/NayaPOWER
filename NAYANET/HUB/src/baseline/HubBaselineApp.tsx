import source from './hub-baseline.html?raw';

export function HubBaselineApp() {
  return (
    <iframe
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
  );
}