import { IdentityProvider } from '../identity/session';
import { AppShellV3 } from './AppShellV3';
import { HubRouter } from './HubRouter';

export default function App() {
  return (
    <IdentityProvider>
      <AppShellV3>
        {(path) => <HubRouter path={path} />}
      </AppShellV3>
    </IdentityProvider>
  );
}
