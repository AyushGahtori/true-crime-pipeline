# Task 001 Handoff

- Task: 001 Bootstrap Hybrid Monorepo
- Branch: `task/001-monorepo-bootstrap`
- Worktree: `../tc-wt/task-001-monorepo-bootstrap`
- Track: Shared Foundation
- Status: committed on the task branch only

## What landed

- Python `>=3.12` uv workspace (`pyproject.toml`) and pnpm workspace (`package.json`, `pnpm-workspace.yaml`, `pnpm-lock.yaml`, `tsconfig.base.json`)
- `providers.yaml` is the only model-id and price registry. Primary video is `gemini-omni-1.2-flash` on the Gemini Interactions API at a conservative `$0.10/sec` (720p), `max_hero_clips: 10`, `max_hero_duration_sec: 80`, `$10.40/ep`, and `$135/mo` across all providers. DeepSeek carries both a `0%` cache projection and a best-effort cached projection. Word timing is local `whisperx-local` at `$0`. `VERTEX_VEO_ENTERPRISE` and `HUMAN_BATCH_DESK` are separate adapters (`interchangeable_with_primary: false`). Veo 3.1 on the Gemini Developer API is `shut_down` and `selectable_as_default: false`.
- `craft_rubric.yaml` is 77 lines. "interactive" means high-engagement visual curiosity hooks and pacing. It is not research and not a ScenePlan.
- `.gitignore` blocks `.env*`, `*.db*`, `node_modules/`, `.venv/`, `ready_to_upload/`, and `artifacts/`.
- `.gitattributes` sets `text=auto eol=lf` and marks media/font/archive files binary.
- `scripts/agent-worktree.mjs` implements `create`, `check`, `commit`, `wave-merge`, and `wave-rollback`. Create uses sibling `../tc-wt/task-NNN-<slug>` and branch `task/NNN-<slug>`. Task `000` is refused.
- `scripts/verify-harmony.mjs` checks owned paths from `IMPLEMENTATION_TASKS.md`, Part 1 (`005-100`) vs Part 2 (`101-192`) fences, secrets, hardcoded model ids under `packages/*/src` and `apps/*/src`, v4 schema text, diagram drift, and `node schema/schema-test.js`.
- Pytest blocks outbound sockets and scrubs `GEMINI_API_KEY`, `DEEPSEEK_API_KEY`, and `ELEVENLABS_API_KEY` unless both `--live-sandbox` and `ALLOW_PAID_SANDBOX=1` are set. Vitest blocks outbound `fetch` the same way. That pair is not enabled.
- Empty shells only: 13 Python packages and 4 pnpm packages (`@tc/shared-contracts-ts`, `@tc/render_catalog`, `@tc/batch_desk_ui`, `@tc/e2e`). No business logic.

The Gemini Image checkpoint is not pinned in the v4 blueprint. `providers.yaml` registers the role id `gemini-image` with `sku_pinned_in_blueprint: false`. Replace that id only in `providers.yaml`.

Root `package.json` is not `"type": "module"`. `schema/schema-test.js` and `tools/merge-diagrams.js` are CommonJS. Workspace packages that need ESM set `"type": "module"` themselves. Script entrypoints are `.mjs`.

## Windows long paths

Git config was not modified. This task did not set `core.longpaths` or `core.autocrlf`.

On Windows, the machine owner (not an agent) should enable long paths before deep worktrees:

```
git config --system core.longpaths true
```

Worktrees stay siblings of the primary clone at `../tc-wt/task-NNN-<slug>` so paths stay shorter than nesting them inside the repo. `.gitattributes` already forces `eol=lf` for source text. A machine-level `core.autocrlf=false` is appropriate and was not set here.

## Tools

- `uv` is not on PATH. `uv.lock` was not generated. The workspace manifest is ready for a later `uv sync`.
- pnpm 10.34.9 installed the workspace and wrote `pnpm-lock.yaml`.
- Node v24.16.0, Python 3.12.10, pytest 9.2.0.

## Verification

- `node scripts/agent-worktree.mjs create 000 smoke` exits 2 and does not create `task/000-*`.
- `wave-merge --wave W1-A --branch main` exits 2.
- `wave-rollback --wave W3-A --sha HEAD --dry-run` exits 2 because HEAD is not a merge. No revert ran.
- `node schema/schema-test.js`: 12/12 passed.
- `python -m pytest -q`: 8 passed (socket block, DNS block, key scrub, one-sided sandbox flags still blocked, scope/secret/model probes, Part 1 fence, missing wave tag).
- `node scripts/verify-harmony.mjs --task 001`: passed.
- `pnpm typecheck`: passed for the four TypeScript shells.
- `pnpm test` (vitest): 2 passed with provider keys set in the environment. Outbound `fetch` was blocked and the keys were scrubbed.

## Incomplete

- No `uv.lock` until `uv` is installed.
- pnpm warned that the `esbuild` install script was ignored. Vitest 3.2.7 still ran this test file.
- Paid sandbox was not enabled.
- Shells have no runtime behavior. Downstream tasks declare new dependencies in their own handoff.

## Notes for the next agent

Commit only on `task/NNN-<slug>`. Do not merge, push, or change git config. Model ids and prices stay in `providers.yaml`.
