// Launch Chromium so it can actually reach the internet from a Claude Code
// remote session. Import launch() instead of calling chromium.launch() directly.
//
// Two faults, both diagnosed from Chrome's own net-log. Fixing either one alone
// still fails:
//
//   1. Chromium ignores HTTPS_PROXY and resolves every request as DIRECT
//      ("proxy_info": "DIRECT" in the net-log). Direct egress is blocked, so
//      everything fails with ERR_CONNECTION_RESET. The explicit --proxy-server
//      flag is required; the env var alone does nothing, and neither does
//      Playwright's own proxy: option.
//
//   2. With the proxy set, CONNECT succeeds ("200 Connection Established" for
//      every host) and the TLS 1.3 handshake inside the tunnel is then reset.
//      --ssl-version-max=tls1.2 fixes it.
//
// The TLS cap is not a weakening. openssl s_client -proxy returns the genuine
// upstream chains, so the proxy is a plain CONNECT tunnel and nothing is
// re-signed. Certificate verification stays fully on; never reach for
// --ignore-certificate-errors.
//
// Ruled out by testing, do not retry: Encrypted ClientHello, post-quantum key
// share, DNS-over-HTTPS, the network sandbox, --proxy-bypass-list, and
// importing the proxy CA into ~/.pki/nssdb.

import { chromium } from 'playwright';
import { existsSync, readdirSync } from 'node:fs';

/** Find the installed Chromium. Never hard-code the build number; it changes. */
export function chromePath() {
  if (process.env.CHROME_PATH && existsSync(process.env.CHROME_PATH)) return process.env.CHROME_PATH;
  const root = process.env.PLAYWRIGHT_BROWSERS_PATH || '/opt/pw-browsers';
  const candidates = [];
  if (existsSync(root)) {
    for (const d of readdirSync(root)) {
      if (!d.startsWith('chromium')) continue;
      for (const sub of ['chrome-linux/chrome', 'chrome-linux/headless_shell',
                         'chrome-linux64/chrome']) {
        const p = `${root}/${d}/${sub}`;
        if (existsSync(p)) candidates.push(p);
      }
    }
  }
  // prefer full chrome over headless_shell, and the highest build number
  candidates.sort((a, b) =>
    (b.includes('/chrome') - a.includes('/chrome')) || b.localeCompare(a, undefined, {numeric: true}));
  if (candidates.length) return candidates[0];
  return undefined; // let Playwright try its own default
}

export function browserArgs({ proxy = process.env.HTTPS_PROXY, extra = [] } = {}) {
  const args = ['--no-sandbox', '--disable-dev-shm-usage', '--ssl-version-max=tls1.2'];
  if (proxy) args.push(`--proxy-server=${proxy}`);
  return args.concat(extra);
}

/** Drop-in for chromium.launch(). Pass {offline:true} to block all egress. */
export async function launch({ offline = false, extra = [], ...opts } = {}) {
  const executablePath = chromePath();
  return chromium.launch({
    ...(executablePath ? { executablePath } : {}),
    args: browserArgs({ proxy: offline ? null : process.env.HTTPS_PROXY, extra }),
    ...opts,
  });
}

/** Context that only loads local files. Use for rendering our own mockups. */
export async function localContext(browser, viewport) {
  const ctx = await browser.newContext({ viewport });
  await ctx.route('**://**', r =>
    r.request().url().startsWith('file:') ? r.continue() : r.abort());
  return ctx;
}
