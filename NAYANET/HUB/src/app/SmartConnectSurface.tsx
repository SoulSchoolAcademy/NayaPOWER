import { useIdentity } from '../identity/session';

const DOORS = [
  ['GITHUB APP','Connect NayaNET to a governed GitHub installation.'],
  ['MCP','Connect an MCP-capable intelligence or tool environment.'],
  ['REST / OPENAPI','Connect an external service through a governed API contract.'],
  ['WEBHOOKS','Let an authorized system send events into NayaNET.'],
  ['SDK','Embed NayaNET capabilities through the supported SDK boundary.'],
  ['A2A','Connect another agent through the agent-to-agent boundary.'],
  ['MCP APPS','Connect an MCP App / interactive capability to the Hub.'],
] as const;

export function SmartConnectSurface() {
  const identity = useIdentity();
  return (
    <section className="feature-surface" data-surface="smart-connect">
      <div className="feature-hero">
        <div>
          <div className="eyebrow">NAYANET · SMART CONNECT · SEVEN DOORS</div>
          <h1>Smart Connect</h1>
          <p>Open one governed door to connect a Naya, human, app, agent, or external system to NayaNET.</p>
        </div>
        <div className="feature-state">{identity.is_authenticated ? 'AUTHENTICATED' : 'AUTHENTICATION REQUIRED'}</div>
      </div>
      <div className="share-consent">
        <b>THE CONNECTION AGREEMENT</b>
        <span>
          When you Smart Connect, you agree to participate in NayaNET: share your wisdom by default,
          keep your personal intelligence and activity private, and keep your identity private by default.
          Useful wisdom may be distilled into collective intelligence through governed quality, privacy,
          safety, deduplication, and verification filters. Public identity or publication is never implied.
        </span>
      </div>
      <div className="connection-room-grid">
        {DOORS.map(([name, description], index) => (
          <article className="connection-room-card" key={name}>
            <div>
              <span className="feature-card-kicker">DOOR {String(index + 1).padStart(2, '0')}</span>
              <h2>{name}</h2>
              <p>{description}</p>
            </div>
            <div className="connection-room-meta">
              <span>PARTICIPATION · WISDOM SHARING ENABLED BY CONNECTION</span>
              <span>IDENTITY · PRIVATE BY DEFAULT</span>
            </div>
            <button type="button" disabled={!identity.is_authenticated}>
              {identity.is_authenticated ? 'CONNECT' : 'AUTHENTICATE TO CONNECT'}
            </button>
          </article>
        ))}
      </div>
      <div className="feature-foot">
        <span>SMART CONNECT</span>
        <b>CONNECT · SHARE WISDOM · PROTECT IDENTITY</b>
        <span>•</span>
        <span>CAPABILITY ≠ AUTHORITY</span>
      </div>
    </section>
  );
}
