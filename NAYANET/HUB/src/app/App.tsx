import { IdentityProvider } from '../identity/session';
import { AppShell } from './AppShell';
import { HubRouter } from './HubRouter';

export default function App() {
  return (
    <IdentityProvider>
      <AppShell>
        {(path) => <HubRouter path={path} />}
      </AppShell>
    </IdentityProvider>
  );
}
