// Ambient stubs so a normal tsc can type-check Deno edge-function sources.
// These exist ONLY for the CI type-check gate (see tools/edge-typecheck/README.md).
// They are not shipped and not used by Deno, which resolves the real specifiers.
//
// Scope discipline: these declare SHAPES only. `any` return types are deliberate --
// the goal is catching undefined identifiers, wrong arity, and unreachable
// conditions, which are the defects that surface in production as opaque HTTP 400s.
// Asserting real library types would make the gate a Deno emulator, which is a
// different (and much larger) project.

declare module "https://*" {
  export const createRemoteJWKSet: (...args: any[]) => any;
  export const jwtVerify: (...args: any[]) => Promise<any>;
  export const decodeJwt: (...args: any[]) => any;
  export const createClient: (...args: any[]) => any;
  export const importPKCS8: (...args: any[]) => Promise<any>;
  export const compactDecrypt: (...args: any[]) => Promise<any>;
  export const importSPKI: (...args: any[]) => Promise<any>;
  export const compactVerify: (...args: any[]) => Promise<any>;
  export const assertEquals: (a: any, b: any, msg?: any) => void;
  export const assert: (cond: any, msg?: any) => void;
  export const SignJWT: any;
  export const exportJWK: (...args: any[]) => Promise<any>;
  export const generateKeyPair: (...args: any[]) => Promise<any>;
  export const importX509: (...args: any[]) => Promise<any>;
  export const decodeProtectedHeader: (...args: any[]) => any;
  const _default: any;
  export default _default;
}

declare module "npm:*" {
  export const createClient: (...args: any[]) => any;
  // jose (imported as npm:jose@* by nayanet-github-dispatch for GitHub App
  // JWT minting). Mirrors the https://* stub's shape declarations -- shapes
  // only, per this file's scope discipline.
  export const SignJWT: any;
  export const importPKCS8: (...args: any[]) => Promise<any>;
  const _default: any;
  export default _default;
}

declare module "jsr:*" {
  const _default: any;
  export default _default;
}

declare namespace Deno {
  const env: { get(key: string): string | undefined };
  const version: { deno: string };
  const args: string[];
  function serve(handler: (req: Request) => Response | Promise<Response>, options?: any): any;
  function readFile(path: string): Promise<Uint8Array>;
  function writeTextFile(path: string, data: string): Promise<void>;
  function mkdir(path: string, options?: any): Promise<void>;
  function remove(path: string, options?: any): Promise<void>;
  function readDir(path: string): AsyncIterable<{ name: string; isFile: boolean; isDirectory: boolean }>;
  function test(name: string, fn: (t: any) => any): void;
  function exit(code?: number): never;
  function cwd(): string;
}
