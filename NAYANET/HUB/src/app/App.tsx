import { IdentityProvider, useIdentity } from '../identity/session';
import { AuthPanel } from '../identity/AuthPanel';
import { AppShell } from './AppShell';
import { HubRouter } from './HubRouter';

function AuthenticatedHub() {
  const identity = useIdentity();

  if (!identity.is_authenticated) {
    return (
      <main className="auth-gate" data-runtime-marker="NAYANET-HUB-AUTH-GATE">
        <AuthPanel />
      </main>
    );
  }

  return (
    <AppShell>
      {(path) => <HubRouter path={path} />}
    </AppShell>
  );
}

export default function App() {
  return (
    <IdentityProvider>
      <AuthenticatedHub />
    </IdentityProvider>
  );
}
