import http from 'node:http';
import https from 'node:https';

const SCRUBBED = ['GEMINI_API_KEY', 'DEEPSEEK_API_KEY', 'ELEVENLABS_API_KEY'];

function paidSandboxEnabled() {
  return process.argv.includes('--live-sandbox') && process.env.ALLOW_PAID_SANDBOX === '1';
}

function isLoopback(hostname) {
  const host = String(hostname ?? '').replace(/^\[|\]$/g, '').toLowerCase();
  return host === '127.0.0.1' || host === 'localhost' || host === '::1';
}

function blocked(target) {
  const error = new Error(`ZERO_SPEND_GUARD: blocked outbound fetch to ${target}`);
  error.code = 'ZERO_SPEND_GUARD';
  return error;
}

if (!paidSandboxEnabled()) {
  for (const key of SCRUBBED) delete process.env[key];

  const originalFetch = globalThis.fetch?.bind(globalThis);
  globalThis.fetch = async (input, init) => {
    const raw = typeof input === 'string' ? input : input instanceof URL ? input.href : input.url;
    const url = new URL(raw);
    if (!isLoopback(url.hostname)) throw blocked(url.host);
    if (!originalFetch) throw blocked(url.host);
    return originalFetch(input, init);
  };

  function guardRequest(original) {
    return function guarded(input, options, callback) {
      const host = typeof input === 'string'
        ? new URL(input).hostname
        : input?.hostname || input?.host;
      if (!isLoopback(host)) throw blocked(host ?? input);
      return original.call(this, input, options, callback);
    };
  }

  http.request = guardRequest(http.request);
  http.get = guardRequest(http.get);
  https.request = guardRequest(https.request);
  https.get = guardRequest(https.get);
}
