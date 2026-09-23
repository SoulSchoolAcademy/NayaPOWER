import { IdentityProvider } from '../identity/session';
import { AppShellV3 } from './shell/AppShell';
import { HubRouter } from './routing/HubRouter';

export default function App() {
  return (
    <IdentityProvider>
      <AppShellV3>
        {(path) => <HubRouter path={path} />}
      </AppShellV3>
    </IdentityProvider>
  );
}
