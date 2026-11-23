#!/usr/bin/env node
/**
 * Disjoint-scope, secret, and zero-spend harmony check.
 *
 *   node scripts/verify-harmony.mjs --task NNN [--wave <id>]
 *   node scripts/verify-harmony.mjs --wave <id>
 *   node scripts/verify-harmony.mjs --lint-model-ids
 *
 * Foundation tasks 001-004 may touch only their own parsed scopes.
 * Part 1 (005-100) and Part 2 (101-192) cannot write each other's trees.
 */

import { execFileSync, spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const waves = JSON.parse(fs.readFileSync(path.join(repoRoot, 'scripts', 'waves.json'), 'utf8'));

const PART1_PREFIXES = [
  'packages/db/',
  'packages/agent1_scout/',
  'packages/agent2_evidence/',
  'packages/agent3_gatekeeper/',
  'packages/voice_sync/',
  'packages/agent4_director/',
  'packages/orchestrator/',
];

const PART2_PREFIXES = [
  'packages/render_catalog/',
  'packages/python_motion/',
  'packages/crime_scene_2k/',
  'packages/flow_adapter/',
  'packages/agent6_mastering/',
  'packages/analytics_feedback/',
  'apps/batch_desk_ui/',
  'apps/e2e/',
];

const TASK_001_OVERLAY = [
  'scripts/',
  '.agent-handoffs/',
  'pnpm-lock.yaml',
  'uv.lock',
  'vitest.config.mjs',
];

const SECRET_PATTERNS = [
  { name: 'gemini-key', re: /GEMINI_API_KEY\s*=\s*['"]?[A-Za-z0-9_\-]{8,}/ },
  { name: 'deepseek-key', re: /DEEPSEEK_API_KEY\s*=\s*['"]?[A-Za-z0-9_\-]{8,}/ },
  { name: 'elevenlabs-key', re: /ELEVENLABS_API_KEY\s*=\s*['"]?[A-Za-z0-9_\-]{8,}/ },
  { name: 'aws-access-key', re: /AKIA[0-9A-Z]{16}/ },
  { name: 'private-key', re: /-----BEGIN [A-Z ]*PRIVATE KEY-----/ },
  { name: 'google-api-key', re: /AIza[0-9A-Za-z\-_]{35}/ },
];

const MODEL_LITERAL = /gemini-omni|deepseek|veo/i;
const SRC_EXT = new Set(['.py', '.ts', '.tsx', '.js', '.mjs', '.cjs']);
const SKIP_DIRS = new Set(['node_modules', '.venv', 'venv', '.git', 'dist', 'artifacts', 'ready_to_upload', '.pytest_cache']);

const failures = [];

function fail(message) {
  failures.push(message);
}

function git(args) {
  return execFileSync('git', args, {
    cwd: repoRoot,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  });
}

function parseArgs(argv) {
  const out = { lintOnly: false };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (token === '--lint-model-ids') out.lintOnly = true;
    else if (token === '--task' || token === '--wave') {
      const value = argv[i + 1];
      if (!value || value.startsWith('--')) {
        fail(`${token} needs a value`);
        return out;
      }
      out[token.slice(2)] = value;
      i += 1;
    } else {
      fail(`unknown argument ${token}`);
    }
  }
  return out;
}

function normalizeTask(raw) {
  if (!/^\d{1,3}$/.test(String(raw).trim())) return null;
  return String(raw).trim().padStart(3, '0');
}

function readScopeMap() {
  const markdown = fs.readFileSync(path.join(repoRoot, 'IMPLEMENTATION_TASKS.md'), 'utf8');
  const map = new Map();
  let current = null;
  for (const line of markdown.split(/\r?\n/)) {
    const heading = line.match(/^### Task (\d{3})\b/);
    if (heading) {
      current = heading[1];
      continue;
    }
    if (!current) continue;
    if (!line.includes('**Owned Write Scope:**') && !line.includes('**Files:**')) continue;
    const paths = [...line.matchAll(/`([^`]+)`/g)]
      .map((match) => match[1].trim())
      .filter((token) => token.includes('/') || token.includes('.') || token.startsWith('.'))
      .filter((token) => !token.includes(' '));
    const existing = map.get(current) ?? [];
    map.set(current, existing.concat(paths));
  }
  return map;
}

function matchesPattern(file, pattern) {
  const normalized = file.replaceAll('\\', '/');
  let token = pattern.replaceAll('\\', '/').replace(/^\.\//, '');
  if (token.endsWith('/**')) {
    const prefix = token.slice(0, -3).replace(/\/$/, '');
    return normalized === prefix || normalized.startsWith(`${prefix}/`);
  }
  if (token.endsWith('/*')) {
    const prefix = token.slice(0, -2).replace(/\/$/, '');
    return normalized === prefix || normalized.startsWith(`${prefix}/`);
  }
  if (token.endsWith('/')) {
    const prefix = token.replace(/\/$/, '');
    return normalized === prefix || normalized.startsWith(`${prefix}/`);
  }
  return normalized === token || normalized.startsWith(`${token}/`);
}

function allowedPatterns(task, scopeMap) {
  const parsed = scopeMap.get(task) ?? [];
  if (task === '001') return parsed.concat(TASK_001_OVERLAY);
  return parsed;
}

function changedFiles() {
  const candidates = ['main', 'origin/main', 'master'];
  let baseRef = null;
  for (const ref of candidates) {
    const probe = spawnSync('git', ['rev-parse', '--verify', '--quiet', ref], { cwd: repoRoot });
    if (probe.status === 0) {
      baseRef = ref;
      break;
    }
  }
  if (!baseRef) {
    fail('no main/master ref to diff against');
    return [];
  }
  const base = git(['merge-base', 'HEAD', baseRef]).trim();
  const names = new Set();
  for (const args of [
    ['diff', '--name-only', '-z', `${base}...HEAD`],
    ['diff', '--name-only', '-z'],
    ['diff', '--name-only', '-z', '--cached'],
    ['ls-files', '--others', '--exclude-standard', '-z'],
  ]) {
    const output = execFileSync('git', args, { cwd: repoRoot });
    for (const name of output.toString('utf8').split('\0')) {
      if (name) names.add(name.replaceAll('\\', '/'));
    }
  }
  return [...names].sort();
}

function partViolation(task, file) {
  const n = Number(task);
  if (n >= 1 && n <= 4) return null;
  if (n >= 5 && n <= 100 && PART2_PREFIXES.some((prefix) => file.startsWith(prefix))) {
    return `Part 1 task ${task} cannot write Part 2 path ${file}`;
  }
  if (n >= 101 && n <= 192 && PART1_PREFIXES.some((prefix) => file.startsWith(prefix))) {
    return `Part 2 task ${task} cannot write Part 1 path ${file}`;
  }
  return null;
}

function checkScope(task, files, scopeMap) {
  const patterns = allowedPatterns(task, scopeMap);
  if (patterns.length === 0) {
    console.log(`scope: task ${task} has no owned-write map; enforcing the part fence only`);
  }
  for (const file of files) {
    const crossed = partViolation(task, file);
    if (crossed) fail(crossed);
    if (patterns.length > 0 && !patterns.some((pattern) => matchesPattern(file, pattern))) {
      fail(`out of scope for task ${task}: ${file}`);
    }
  }
  if (patterns.length > 0) {
    console.log(`scope: task ${task} checked ${files.length} path(s) against ${patterns.length} pattern(s)`);
  }
}

function checkWave(task, waveId) {
  const wave = waves[waveId];
  if (!wave) {
    fail(`unknown wave ${waveId}`);
    return;
  }
  if (wave.track === 'main' || wave.track === 'master') {
    fail(`wave ${waveId} refuses target ${wave.track}`);
  }
  if (task && !wave.tasks.includes(Number(task))) {
    fail(`task ${task} is not in wave ${waveId}`);
  }
  if (wave.requiresTag) {
    const tag = spawnSync('git', ['rev-parse', '--verify', '--quiet', `refs/tags/${wave.requiresTag}`], {
      cwd: repoRoot,
    });
    if (tag.status !== 0) {
      fail(`wave ${waveId} is blocked until tag ${wave.requiresTag} exists`);
    }
  }
  console.log(`wave: ${waveId} -> ${wave.track} (produces ${wave.producesTag})`);
}

function looksBinary(file) {
  const ext = path.extname(file).toLowerCase();
  return ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.wav', '.mp3', '.mp4', '.pdf', '.zip', '.gz'].includes(ext);
}

function checkSecrets(files) {
  const trackedEnv = git(['ls-files', '-z'])
    .split('\0')
    .filter((name) => /(^|\/)\.env($|\.)/.test(name.replaceAll('\\', '/')));
  for (const name of trackedEnv) fail(`tracked env file: ${name}`);

  for (const file of files) {
    const normalized = file.replaceAll('\\', '/');
    if (/(^|\/)\.env($|\.)/.test(normalized)) fail(`env file in change set: ${file}`);
    if (looksBinary(file)) continue;
    const absolute = path.join(repoRoot, file);
    if (!fs.existsSync(absolute) || !fs.statSync(absolute).isFile()) continue;
    if (fs.statSync(absolute).size > 1_000_000) continue;
    const text = fs.readFileSync(absolute, 'utf8');
    for (const pattern of SECRET_PATTERNS) {
      if (pattern.re.test(text)) fail(`secret scan (${pattern.name}) hit ${file}`);
    }
  }
  console.log(`secrets: scanned ${files.length} changed path(s)`);
}

function walk(dir, visit) {
  if (!fs.existsSync(dir)) return;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (SKIP_DIRS.has(entry.name)) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, visit);
    else if (entry.isFile()) visit(full);
  }
}

function lintModelIds() {
  const roots = [path.join(repoRoot, 'packages'), path.join(repoRoot, 'apps')];
  let files = 0;
  for (const root of roots) {
    walk(root, (full) => {
      const rel = path.relative(repoRoot, full).replaceAll('\\', '/');
      if (!rel.includes('/src/')) return;
      if (!SRC_EXT.has(path.extname(full).toLowerCase())) return;
      files += 1;
      const lines = fs.readFileSync(full, 'utf8').split(/\r?\n/);
      lines.forEach((line, index) => {
        if (!MODEL_LITERAL.test(line)) return;
        if (line.includes('providers.yaml')) return;
        fail(`hardcoded model id in ${rel}:${index + 1}`);
      });
    });
  }
  console.log(`model-ids: scanned ${files} source file(s) under packages/*/src and apps/*/src`);
  return files;
}

function assertTextIncludes(rel, needles) {
  const absolute = path.join(repoRoot, rel);
  if (!fs.existsSync(absolute)) {
    fail(`missing ${rel}`);
    return;
  }
  const text = fs.readFileSync(absolute, 'utf8');
  for (const needle of needles) {
    if (!text.includes(needle)) fail(`${rel} is missing ${JSON.stringify(needle)}`);
  }
}

function checkContracts() {
  assertTextIncludes('schema/pipeline.sql', ["('schema_version', '4')"]);
  assertTextIncludes('schema/telemetry.sql', ['schema version 3']);
  assertTextIncludes('providers.yaml', [
    'model_id: gemini-omni-1.2-flash',
    'api: gemini_interactions',
    'usd_per_sec: 0.10',
    'max_hero_clips: 10',
    'max_hero_duration_sec: 80',
    'episode_cap_usd: 10.40',
    'all_providers_monthly_cap_usd: 135.00',
    'VERTEX_VEO_ENTERPRISE',
    'HUMAN_BATCH_DESK',
    'interchangeable_with_primary: false',
    'whisperx-local',
    'cache_hit_rate_0',
    'cached_best_effort',
    'selectable_as_default: false',
    'status: shut_down',
    'usd_per_episode: 0.00',
  ]);
  const rubricPath = path.join(repoRoot, 'craft_rubric.yaml');
  if (!fs.existsSync(rubricPath)) {
    fail('missing craft_rubric.yaml');
  } else {
    const rubric = fs.readFileSync(rubricPath, 'utf8');
    const lineCount = rubric.split(/\r?\n/).length;
    if (lineCount > 150) fail(`craft_rubric.yaml is ${lineCount} lines (max 150)`);
    if (!/high-engagement visual curiosity hooks/i.test(rubric)) {
      fail('craft_rubric.yaml does not define interactive as visual curiosity hooks');
    }
    console.log(`craft_rubric.yaml: ${lineCount} lines`);
  }
  assertTextIncludes('.gitignore', ['.env*', '*.db*', 'node_modules/', '.venv/', 'ready_to_upload/', 'artifacts/']);
  assertTextIncludes('.gitattributes', ['text=auto eol=lf', 'binary']);
}

function runNode(args, label) {
  const result = spawnSync(process.execPath, args, {
    cwd: repoRoot,
    encoding: 'utf8',
  });
  if ((result.status ?? 1) !== 0) {
    const tail = `${result.stdout ?? ''}\n${result.stderr ?? ''}`.trim().split(/\r?\n/).slice(-20).join('\n');
    fail(`${label} failed\n${tail}`);
    return;
  }
  console.log(`${label}: ok`);
}

function checkDiagrams() {
  const output = path.join(repoRoot, 'pipeline-complete.mmd');
  const before = fs.existsSync(output) ? fs.readFileSync(output) : null;
  const result = spawnSync(process.execPath, ['tools/merge-diagrams.js'], {
    cwd: repoRoot,
    encoding: 'utf8',
  });
  const after = fs.existsSync(output) ? fs.readFileSync(output) : null;
  if (before) fs.writeFileSync(output, before);
  else if (after) fs.rmSync(output);
  if ((result.status ?? 1) !== 0) {
    fail(`node tools/merge-diagrams.js failed\n${result.stderr ?? ''}`);
    return;
  }
  const normalize = (buf) => buf.toString('utf8').replace(/\r\n/g, '\n');
  if (before && after && normalize(before) !== normalize(after)) {
    fail('pipeline-complete.mmd drifted from tools/merge-diagrams.js');
    return;
  }
  console.log('diagrams: pipeline-complete.mmd matches tools/merge-diagrams.js');
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.lintOnly && !args.task && !args.wave) {
    lintModelIds();
    if (failures.length) {
      for (const message of failures) console.error(`FAIL ${message}`);
      process.exit(1);
    }
    console.log('model-id lint passed');
    return;
  }
  if (!args.task && !args.wave) {
    console.error('pass --task NNN, --wave <id>, or --lint-model-ids');
    process.exit(2);
  }

  const task = args.task ? normalizeTask(args.task) : null;
  if (args.task && !task) fail(`invalid task id ${args.task}`);
  if (task === '000') fail('refusing task 000');

  const files = changedFiles();
  if (task) checkScope(task, files, readScopeMap());
  if (args.wave) {
    checkWave(task, args.wave);
    const wave = waves[args.wave];
    if (wave && !task) {
      const scopeMap = readScopeMap();
      const patterns = wave.tasks.flatMap((id) => allowedPatterns(String(id).padStart(3, '0'), scopeMap));
      for (const file of files) {
        if (patterns.length > 0 && !patterns.some((pattern) => matchesPattern(file, pattern))) {
          fail(`out of scope for wave ${args.wave}: ${file}`);
        }
      }
    }
  }
  checkSecrets(files);
  lintModelIds();
  checkContracts();
  checkDiagrams();
  runNode(['schema/schema-test.js'], 'node schema/schema-test.js');

  if (failures.length) {
    for (const message of failures) console.error(`FAIL ${message}`);
    process.exit(1);
  }
  console.log('verify-harmony: passed');
}

main();
