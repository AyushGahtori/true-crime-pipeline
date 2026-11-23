# Contributing & Multi-Agent Parallel Workflow (Part 1 & Part 2)

`Task 001`–`Task 004` freeze the repository skeleton, SQLite schemas, and `packages/shared_contracts/`. Every subsequent task (`Task 005`–`Task 192`) is executed inside an isolated Git worktree by either **Developer A (Part 1)** or **Developer B (Part 2)** with zero overlapping file writes.

## Six-Step Task Execution Protocol

1. **Create an isolated worktree from `integration/main` (or track integration branch `integration/part1` / `integration/part2`):**
   ```text
   node scripts/agent-worktree.mjs create 045 agent3-provenance-whitelist
   ```
   Creates branch `task/045-agent3-provenance-whitelist` at `../tc-wt/task-045-agent3-provenance-whitelist`.
2. **Read every file listed in the task's `Mandatory Reference Files`** plus the frozen types in `packages/shared_contracts/`.
3. **Respect Disjoint Write Ownership:** Edit ONLY paths listed in the task's `Owned Write Scope` plus `.agent-handoffs/task-NNN.md`. Never edit shared lockfiles, `schema/*.sql`, or the other developer's packages unless the task explicitly owns them.
4. **Record Cross-Cutting Needs in `.agent-handoffs/task-NNN.md`:** New package dependencies, barrel exports, or contract change requests go in the structured handoff manifest—never directly into root config files.
5. **Run the Scope & Verification Gate:**
   ```text
   node scripts/verify-harmony.mjs --task 045
   ```
   Verifies disjoint subtree ownership, zero leaked API keys/secrets, clean lint/typecheck/tests, and valid handoff YAML.
6. **Commit on Your Task Branch Only (Never Merge Directly):**
   ```text
   node scripts/agent-worktree.mjs commit 045 "implement deterministic provenance whitelist"
   ```
   Commits carry `TC-Task-ID`, `TC-Track` (`part1` | `part2` | `shared`), and `TC-Never-Merge: true`.

## Track Ownership Summary

| Track | Developer | Owned Directories | Standalone Test Mechanism |
|---|---|---|---|
| **Foundation** | Shared (`001`–`004`) | `packages/shared_contracts/**`, `schema/**`, `fixtures/**`, `scripts/**`, `tools/**` | `schema-test.js`, contract parity checks |
| **Part 1** | Developer A (`005`–`100`) | `packages/db/**`, `packages/agent1_scout/**`, `packages/agent2_evidence/**`, `packages/agent3_gatekeeper/**`, `packages/voice_sync/**`, `packages/agent4_director/**`, `packages/orchestrator/**` | `RenderBackendStub` + recorded YouTube/CourtListener/TTS/DeepSeek fixtures |
| **Part 2** | Developer B (`101`–`192`) | `packages/render_catalog/**`, `packages/python_motion/**`, `packages/crime_scene_2k/**`, `packages/flow_adapter/**`, `packages/agent6_mastering/**`, `apps/batch_desk_ui/**` | `fixtures/golden_manifests/**` + synthetic WAV/MP4 inputs producing real 1080p MP4s |
| **Integration** | Both (`193`–`200`) | `tests/e2e/**`, `benchmarks/**`, root wiring | Live Part 1 -> Part 2 end-to-end 1,200s build |
