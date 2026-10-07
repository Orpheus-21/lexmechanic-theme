// A small Chrome DevTools Protocol client for a temporary Obsidian window.
//
// Usage: node scripts/cdp.mjs SCRIPT.mjs [PORT]
//
// SCRIPT.mjs must export a default async function. It gets { ev, shot, sleep, send }:
//   ev(expression)      run JavaScript in the page and return the value (it can use `app`)
//   shot(file)          save a PNG screenshot of the page
//   sleep(ms)           wait
//   send(method, args)  send any DevTools Protocol command
// Start Obsidian with a separate profile and --remote-debugging-port=PORT first. The default
// port is 9333. docs/testing.md has the commands and the safety rules.
// The script needs Node 22 or newer, which has a global WebSocket and fetch.
import fs from 'node:fs';

const port = process.argv[3] || '9333';
const list = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
const page = list.find(t => t.type === 'page');
if (!page) throw new Error('No page found on port ' + port);
const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise(r => ws.addEventListener('open', r));
let id = 0;
const pending = new Map();
ws.addEventListener('message', m => {
  const d = JSON.parse(m.data);
  if (d.id && pending.has(d.id)) { pending.get(d.id)(d); pending.delete(d.id); }
});
const send = (method, params = {}) => new Promise(res => {
  const i = ++id;
  pending.set(i, res);
  ws.send(JSON.stringify({ id: i, method, params }));
});
const sleep = ms => new Promise(r => setTimeout(r, ms));
const ev = async expression => {
  const r = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
  if (r.result.exceptionDetails) return { error: r.result.exceptionDetails.exception?.description || r.result.exceptionDetails.text };
  return r.result.result.value;
};
const shot = async file => {
  const r = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(file, Buffer.from(r.result.data, 'base64'));
};
const mod = await import(new URL(process.argv[2], 'file://' + process.cwd() + '/').href);
try { await mod.default({ ev, shot, sleep, send }); } finally { ws.close(); }
