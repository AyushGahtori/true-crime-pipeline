// Merges every source diagram (*.mmd in repository root) into one flowchart:
//   pipeline-complete.mmd
// Each source becomes a subgraph inside its chapter with unique prefixes so node IDs never collide.
// Run from repo root: node tools/merge-diagrams.js

const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const OUTPUT = 'pipeline-complete.mmd';

const chapters = [
  ['1 · Overview: End-to-End Hybrid Pipeline', [
    ['pipeline-architecture.mmd', 'pa'],
  ]],
  ['2 · Parallel Two-Developer Split (Part 1 & Part 2)', [
    ['parallel-part1-part2-architecture.mmd', 'pp'],
  ]],
  ['3 · Part 1 Upstream Intelligence (Agents 1–3)', [
    ['scout-and-saturation.mmd', 'sc'],
    ['evidence-and-fact-ledger.mmd', 'ev'],
    ['legal-copyright-and-adsense.mmd', 'lg'],
  ]],
  ['4 · Part 1 Voice-First, Director 13 Laws & Economics', [
    ['voice-first-and-asr-sync.mmd', 'vs'],
    ['director-and-13-laws.mmd', 'dl'],
    ['economics-and-credit-math.mmd', 'ec'],
  ]],
  ['5 · Part 2 Visual Synthesis (Remotion Catalog & 2K Grid)', [
    ['code-animation-catalog.mmd', 'ca'],
    ['crime-scene-2k-grid-engine.mmd', 'g2'],
  ]],
  ['6 · Part 2 Batch Desk Operations & Agent 6 Mastering', [
    ['flow-hybrid-and-batch-desk.mmd', 'bd'],
    ['mastering-loudness-and-qa.mmd', 'mq'],
  ]],
  ['7 · SQLite State, Escrow & Conveyor Storage', [
    ['database-and-state-design.mmd', 'db'],
  ]],
];

const KEYWORDS = new Set([
  'subgraph', 'end', 'direction', 'classDef', 'class', 'style', 'linkStyle', 'click',
  'flowchart', 'graph', 'TB', 'TD', 'BT', 'LR', 'RL',
]);

function renameCode(code, p) {
  let out = '';
  let i = 0;
  while (i < code.length) {
    const ch = code[i];
    if (ch === '#') {
      let j = i + 1;
      while (j < code.length && /[0-9A-Za-z_-]/.test(code[j])) j++;
      out += code.slice(i, j);
      i = j;
      continue;
    }
    if (ch === '"') {
      const end = code.indexOf('"', i + 1);
      const stop = end === -1 ? code.length : end + 1;
      out += code.slice(i, stop);
      i = stop;
      continue;
    }
    if (ch === '|') {
      const end = code.indexOf('|', i + 1);
      if (end !== -1 && !code.slice(i + 1, end).includes('\n')) {
        out += code.slice(i, end + 1);
        i = end + 1;
        continue;
      }
    }
    if (/[A-Za-z_]/.test(ch)) {
      let j = i + 1;
      while (j < code.length && /[A-Za-z0-9_-]/.test(code[j])) j++;
      const word = code.slice(i, j);
      const prev = out.slice(-1);
      const next = code[j];
      if (KEYWORDS.has(word) || prev === '#' || prev === '.' || prev === ':' || next === ':') {
        out += word;
      } else {
        out += `${p}_${word}`;
      }
      i = j;
      continue;
    }
    out += ch;
    i++;
  }
  return out;
}

function stripFrontmatter(src) {
  const lines = src.replace(/\r\n/g, '\n').split('\n');
  let start = 0;
  let title = '';
  if (lines[0] && lines[0].trim() === '---') {
    for (let k = 1; k < lines.length; k++) {
      if (lines[k].trim().startsWith('title:')) {
        title = lines[k].trim().slice(6).trim();
      }
      if (lines[k].trim() === '---') {
        start = k + 1;
        break;
      }
    }
  }
  while (start < lines.length && !lines[start].trim()) start++;
  let dir = 'TB';
  if (lines[start] && /^(flowchart|graph)\s+(TB|TD|BT|LR|RL)/.test(lines[start].trim())) {
    dir = lines[start].trim().split(/\s+/)[1];
    start++;
  }
  return { title, dir, body: lines.slice(start).join('\n') };
}

const sections = [
  '---',
  'title: Automated True-Crime Documentary Pipeline — Complete Architecture Atlas',
  '---',
  'flowchart TB',
];

for (let cIdx = 0; cIdx < chapters.length; cIdx++) {
  const [chapterTitle, items] = chapters[cIdx];
  const chId = `CH_${cIdx + 1}`;
  sections.push(`  subgraph ${chId}["${chapterTitle}"]`);
  sections.push('    direction TB');
  for (const [file, prefix] of items) {
    const fullPath = path.join(root, file);
    if (!fs.existsSync(fullPath)) {
      throw new Error(`Missing diagram file: ${file}`);
    }
    const raw = fs.readFileSync(fullPath, 'utf8');
    const { title, dir, body } = stripFrontmatter(raw);
    const label = title || file.replace(/\.mmd$/, '');
    sections.push(`    subgraph ${prefix}_ROOT["${label}"]`);
    sections.push(`      direction ${dir}`);
    const renamed = renameCode(body, prefix)
      .split('\n')
      .map((l) => (l.trim() ? `      ${l}` : ''))
      .join('\n');
    sections.push(renamed);
    sections.push('    end');
  }
  sections.push('  end');
}

fs.writeFileSync(path.join(root, OUTPUT), sections.join('\n') + '\n', 'utf8');
console.log(`Merged ${chapters.reduce((n, [, items]) => n + items.length, 0)} diagrams into ${OUTPUT}`);
