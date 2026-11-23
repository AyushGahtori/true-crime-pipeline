#!/usr/bin/env node
/**
 * Task worktree CLI.
 *
 *   node scripts/agent-worktree.mjs create <NNN> <slug>
 *   node scripts/agent-worktree.mjs check <NNN>
 *   node scripts/agent-worktree.mjs commit <NNN> --message "<text>"
 *   node scripts/agent-worktree.mjs wave-merge --wave <id> --branch task/NNN-slug [--dry-run]
 *   node scripts/agent-worktree.mjs wave-rollback --wave <id> --sha <merge> [--dry-run]
 *
 * Worktrees are siblings of the primary clone: ../tc-wt/task-NNN-<slug>
 * Branches: task/NNN-<slug>
 * This script does not read or write git config.
 */

import { execFileSync, spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const waves = JSON.parse(fs.readFileSync(path.join(repoRoot, 'scripts', 'waves.json'), 'utf8'));

function git(args, cwd = repoRoot) {
  return execFileSync('git', args, {
    cwd,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  });
}

function fail(message, code = 2) {
  console.error(message);
  process.exit(code);
}

function primaryRoot() {
  const common = git(['rev-parse', '--git-common-dir']).trim();
  return path.dirname(path.resolve(repoRoot, common));
}

function normalizeTask(raw) {
  const text = String(raw ?? '').trim();
  if (!/^\d{1,3}$/.test(text)) {
    fail(`invalid task id '${raw}'. Expected 001-200.`);
  }
  const task = text.padStart(3, '0');
  const n = Number(task);
  if (n === 0) {
    fail('refusing task 000 smoke: scratch branch task/000-* is not created. Valid tasks are 001-200.');
  }
  if (n < 1 || n > 200) {
    fail(`refusing task ${task}: valid tasks are 001-200.`);
  }
  return task;
}

function validateSlug(slug) {
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug ?? '')) {
    fail(`invalid slug '${slug}'. Use lowercase words separated by hyphens.`);
  }
}

function branchName(task, slug) {
  return `task/${task}-${slug}`;
}

function worktreeDir(task, slug) {
  return path.resolve(primaryRoot(), '..', 'tc-wt', `task-${task}-${slug}`);
}

function branchExists(name) {
  const result = spawnSync('git', ['show-ref', '--verify', '--quiet', `refs/heads/${name}`], {
    cwd: repoRoot,
  });
  return result.status === 0;
}

function findWorktree(task) {
  const porcelain = git(['worktree', 'list', '--porcelain']);
  const prefix = `refs/heads/task/${task}-`;
  let current = {};
  const found = [];
  for (const line of porcelain.split(/\r?\n/)) {
    if (!line.trim()) {
      if (current.worktree && current.branch) found.push(current);
      current = {};
      continue;
    }
    if (line.startsWith('worktree ')) current.worktree = line.slice('worktree '.length);
    if (line.startsWith('branch ')) current.branch = line.slice('branch '.length);
  }
  if (current.worktree && current.branch) found.push(current);
  return found.find((entry) => entry.branch.startsWith(prefix)) ?? null;
}

function trackFor(task) {
  const n = Number(task);
  if (n <= 4) return 'Shared Foundation';
  if (n <= 100) return 'Part 1';
  if (n <= 192) return 'Part 2';
  return 'Joint';
}

function ensureTrailers(message, task) {
  const lines = String(message ?? '').replace(/\r\n/g, '\n').trim();
  if (!lines) fail('commit requires --message');
  const trailers = [];
  if (!/^TC-Task-ID:/m.test(lines)) trailers.push(`TC-Task-ID: ${task}`);
  if (!/^TC-Track:/m.test(lines)) trailers.push(`TC-Track: ${trackFor(task)}`);
  if (!/^TC-Never-Merge:/m.test(lines)) trailers.push('TC-Never-Merge: true');
  if (trailers.length === 0) return `${lines}\n`;
  return `${lines}\n\n${trailers.join('\n')}\n`;
}

function parseArgs(argv) {
  const flags = { dryRun: false };
  const positionals = [];
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (token === '--dry-run') {
      flags.dryRun = true;
      continue;
    }
    if (token === '--wave' || token === '--branch' || token === '--sha' || token === '--message' || token === '-m') {
      const key = token === '-m' ? 'message' : token.slice(2);
      const value = argv[i + 1];
      if (!value || value.startsWith('--')) fail(`${token} needs a value`);
      flags[key] = value;
      i += 1;
      continue;
    }
    if (token.startsWith('--')) fail(`unknown flag ${token}`);
    positionals.push(token);
  }
  return { flags, positionals };
}

function cmdCreate(taskRaw, slug) {
  const task = normalizeTask(taskRaw);
  validateSlug(slug);
  const branch = branchName(task, slug);
  const dest = worktreeDir(task, slug);
  if (branchExists(branch)) fail(`branch ${branch} already exists`);
  if (fs.existsSync(dest)) fail(`worktree path already exists: ${dest}`);
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  execFileSync('git', ['worktree', 'add', '-b', branch, dest, 'HEAD'], {
    cwd: repoRoot,
    stdio: 'inherit',
  });
  console.log(`created ${branch}`);
  console.log(`worktree ${dest}`);
}

function cmdCheck(taskRaw) {
  const task = normalizeTask(taskRaw);
  const located = findWorktree(task);
  const cwd = located ? located.worktree : repoRoot;
  const branch = git(['rev-parse', '--abbrev-ref', 'HEAD'], cwd).trim();
  if (!branch.startsWith(`task/${task}-`)) {
    fail(`no worktree on task/${task}-* (current ${cwd} is ${branch})`);
  }
  const script = path.join(cwd, 'scripts', 'verify-harmony.mjs');
  if (!fs.existsSync(script)) fail(`missing ${script}`);
  const result = spawnSync(process.execPath, [script, '--task', task], {
    cwd,
    stdio: 'inherit',
  });
  process.exit(result.status ?? 1);
}

function cmdCommit(taskRaw, message) {
  const task = normalizeTask(taskRaw);
  const located = findWorktree(task);
  const cwd = located ? located.worktree : repoRoot;
  const branch = git(['rev-parse', '--abbrev-ref', 'HEAD'], cwd).trim();
  if (branch === 'main' || branch === 'master' || branch.startsWith('integration/')) {
    fail(`refusing commit on shared branch ${branch}`);
  }
  if (!branch.startsWith(`task/${task}-`)) {
    fail(`refusing commit: ${cwd} is on ${branch}, expected task/${task}-*`);
  }
  const full = ensureTrailers(message, task);
  execFileSync('git', ['add', '-A'], { cwd, stdio: 'inherit' });
  execFileSync('git', ['commit', '-m', full], { cwd, stdio: 'inherit' });
}

function cmdWaveMerge(flags) {
  const wave = waves[flags.wave];
  if (!wave) fail(`unknown wave '${flags.wave ?? ''}'`);
  if (wave.track === 'main' || wave.track === 'master') {
    fail('refusing to merge into main');
  }
  if (!flags.branch || !flags.branch.startsWith('task/')) {
    fail('wave-merge requires --branch task/NNN-slug');
  }
  const task = flags.branch.split('/')[1]?.slice(0, 3);
  if (!/^\d{3}$/.test(task ?? '')) fail(`cannot read task id from ${flags.branch}`);
  const harmony = spawnSync(
    process.execPath,
    [path.join(repoRoot, 'scripts', 'verify-harmony.mjs'), '--wave', flags.wave, '--task', task],
    { cwd: repoRoot, stdio: 'inherit' },
  );
  if ((harmony.status ?? 1) !== 0) {
    fail('wave-merge aborted: verify-harmony failed', harmony.status ?? 1);
  }
  if (flags.dryRun) {
    console.log(`dry-run: git checkout ${wave.track}`);
    console.log(`dry-run: git merge --no-ff ${flags.branch}`);
    console.log(`dry-run: tag after the gate passes: ${wave.producesTag}`);
    return;
  }
  const primary = primaryRoot();
  const dirty = git(['status', '--porcelain'], primary).trim();
  if (dirty) fail(`primary worktree is dirty; refusing checkout of ${wave.track}`);
  execFileSync('git', ['checkout', wave.track], { cwd: primary, stdio: 'inherit' });
  execFileSync(
    'git',
    ['merge', '--no-ff', flags.branch, '-m', `Merge ${flags.branch} into ${wave.track} (${flags.wave})`],
    { cwd: primary, stdio: 'inherit' },
  );
  console.log(`merged ${flags.branch} into ${wave.track}. Tag when the gate is green: ${wave.producesTag}`);
}

function cmdWaveRollback(flags) {
  const wave = waves[flags.wave];
  if (!wave) fail(`unknown wave '${flags.wave ?? ''}'`);
  if (!flags.sha) fail('wave-rollback requires --sha <merge-commit>');
  const parents = git(['rev-list', '--parents', '-n', '1', flags.sha]).trim().split(/\s+/);
  if (parents.length < 3) {
    fail(`refusing rollback: ${flags.sha} is not a merge commit`);
  }
  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  const tag = `rollback/${flags.wave}-${stamp}`;
  if (flags.dryRun) {
    console.log(`dry-run: git revert -m 1 ${flags.sha}`);
    console.log(`dry-run: git tag ${tag}`);
    return;
  }
  execFileSync('git', ['revert', '-m', '1', '--no-edit', flags.sha], {
    cwd: repoRoot,
    stdio: 'inherit',
  });
  execFileSync('git', ['tag', tag], { cwd: repoRoot, stdio: 'inherit' });
  console.log(`reverted merge ${flags.sha} and tagged ${tag}`);
}

function usage() {
  console.log(`Usage:
  node scripts/agent-worktree.mjs create <NNN> <slug>
  node scripts/agent-worktree.mjs check <NNN>
  node scripts/agent-worktree.mjs commit <NNN> --message "<text>"
  node scripts/agent-worktree.mjs wave-merge --wave <id> --branch task/NNN-slug [--dry-run]
  node scripts/agent-worktree.mjs wave-rollback --wave <id> --sha <merge> [--dry-run]`);
}

const { flags, positionals } = parseArgs(process.argv.slice(2));
const [command, ...rest] = positionals;

if (command === 'create') cmdCreate(rest[0], rest[1]);
else if (command === 'check') cmdCheck(rest[0]);
else if (command === 'commit') cmdCommit(rest[0], flags.message);
else if (command === 'wave-merge') cmdWaveMerge(flags);
else if (command === 'wave-rollback') cmdWaveRollback(flags);
else {
  usage();
  process.exit(command ? 2 : 0);
}
