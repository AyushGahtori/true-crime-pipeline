import { defineConfig } from 'vitest/config';

const paidSandbox =
  process.argv.includes('--live-sandbox') && process.env.ALLOW_PAID_SANDBOX === '1';

if (!paidSandbox) {
  delete process.env.GEMINI_API_KEY;
  delete process.env.DEEPSEEK_API_KEY;
  delete process.env.ELEVENLABS_API_KEY;
}

export default defineConfig({
  test: {
    environment: 'node',
    setupFiles: ['./scripts/vitest.setup.mjs'],
    include: ['scripts/**/*.test.mjs', 'packages/**/*.test.ts', 'apps/**/*.test.ts'],
  },
});
