import assert from 'node:assert/strict';
import { test } from 'vitest';

test('ordinary vitest runs scrub provider keys', () => {
  assert.equal(process.env.GEMINI_API_KEY, undefined);
  assert.equal(process.env.DEEPSEEK_API_KEY, undefined);
  assert.equal(process.env.ELEVENLABS_API_KEY, undefined);
});

test('ordinary vitest runs block outbound fetch', async () => {
  await assert.rejects(() => fetch('https://example.com/'), /ZERO_SPEND_GUARD/);
});
