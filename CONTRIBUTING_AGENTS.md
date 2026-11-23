# Contributing & Wave-Ordered Worktree Merge Runbook (v4 · `F-07`)

`Task 001`–`Task 004` freeze the canonical v4 contracts (`schema/pipeline.sql` v4, `providers.yaml`, `craft_rubric.yaml`, `MOTIF_REGISTRY_V1`, `packages/shared_contracts/`). After Day-1 freeze, **Developer A (Part 1)** and **Developer B (Part 2)** implement in isolated Git worktrees using **strictly offline zero-spend transport mocks (`F-01`)**, merging in **dependency-ordered waves** rather than a risky big-bang merge (`F-07`).

## 1. Zero-Spend Offline Guarantee In All Worktrees (`F-01`)
- Every worktree test invocation (`verify-harmony.mjs --task NNN`, `pytest`, `vitest`) strips `GEMINI_API_KEY`, `DEEPSEEK_API_KEY`, `ELEVENLABS_API_KEY`, enables socket-blocking (`--disable-socket` / custom test fixture blocking outbound DNS/TCP except `127.0.0.1`), and binds SQLite reservations to `purpose = 'OFFLINE_TEST'` (`trg_offline_test_zero_spend_guard` aborts on `> $0`).

## 2. Branch Hierarchy & Pinned Base Rules (`F-07`)
- **`main`** — Always releasable; receives commits ONLY via signed integration waves after Gate pass.
- **`integration/m0-frozen`** — Tagged base commit after `Task 004`; EVERY Part 1 / Part 2 wave branches from the latest green track integration tag.
- **`integration/part1` (Owner: Developer A)** & **`integration/part2` (Owner: Developer B)** — Track-level integration branches merged in dependency-ordered waves.
- **`task/NNN-<slug>`** in `../tc-wt/task-NNN-<slug>` — Single-task worktree branch (`Owned Write Scope` strictly enforced).

## 3. Dependency-Ordered Merge Waves & Stop/Go Gates

### Part 1 Waves (`integration/part1`, Developer A Lead)
| Wave | Task Batch | Shared-Contract Check & Stop/Go Gate |
|---|---|---|
| **W1-A · Storage & Budget** | `005–014` | `pytest packages/db` + `node schema/schema-test.js` (`12/12`) + offline zero-spend guard green. Tag `p1-w1`. |
| **W2-A · Scout & Quotas** | `015–032` | `pytest packages/agent1_scout` (mocked YT API + 30d full purge + zero third-party `captions.download`). Tag `p1-w2`. |
| **W3-A · Evidence, Disposition & Early 2K** | `033–044` | `pytest packages/agent2_evidence` (`INSERT+UPDATE` quarantine + `DRAFT->LOCKED` anchors + `is_illustrative_reconstruction=1`). Tag `p1-w3`. |
| **W4-A · Rights, PII & Voice/WhisperX** | `045–072` | `pytest packages/agent3_gatekeeper packages/voice_sync` (17 USC §105 narrowed + WhisperX word sync + <=90s/4MiB cloud ASR bounds). Tag `p1-w4`. |
| **W5-A · Director, `ScenePlan` & Stub Orchestrator** | `073–100` | `pytest packages/agent4_director packages/orchestrator` (`ScenePlan` `PLAN_APPROVED` gate + `max_hero_clips=10` + `PART1_CERT_REPORT.md`). Tag `p1-cert`. |

### Part 2 Waves (`integration/part2`, Developer B Lead)
| Wave | Task Batch | Shared-Contract Check & Stop/Go Gate |
|---|---|---|
| **W1-B · Core 4-Motif MVP & Motion Helpers** | `101–115, 117–118, 122, 130–142` | `pnpm --filter @tc/render_catalog test -- --mvp-4-motifs` (`MOTIF_REGISTRY_V1`) + monochrome Flow PNG tests (`0` crimson). Tag `p2-w1`. |
| **W2-B · Remaining 8 Vector Motifs & 2K Engine** | `116, 119–121, 123–129, 143–152` | Full 12-motif test + `crime_scene_2k` edge-clamp/watermark tests (`ILLUSTRATIVE RECONSTRUCTION`) + reproducible local perf bench. Tag `p2-w2`. |
| **W3-B · Omni Backend & Agent 6 Mastering** | `153–176` | `pytest packages/flow_adapter packages/agent6_mastering` (mocked Omni Interactions T2V/1F/2F + `UNKNOWN_RECONCILE` + `$135/mo` cap + `-14 LUFS`). Tag `p2-w3`. |
| **W4-B · Loopback UI, 5-Gate Sign-Off & Analytics** | `177–192` | Loopback `127.0.0.1` + auth token tests + Playwright E2E + `PART2_CERT_REPORT.md`. Tag `p2-cert`. |

## 4. Cross-Track Merge, Schema Conflict Protocol & Rollback
1. **Shared-File Ownership Rule:** `schema/**`, `providers.yaml`, `craft_rubric.yaml`, and `packages/shared_contracts/**` are **jointly owned (`M0`)**. If either developer needs a schema/contract amendment mid-wave, they open a standalone **Contract Bump PR** against `main`, rebase `integration/part1` and `integration/part2` cleanly, and bump `schema_version` or `CONTRACT_VERSION`—never silently patching contracts inside a feature worktree!
2. **Migration Conflict Resolution:** Only ONE sequential migration file (`migrations/000N_*.sql`) may hold sequence `N`; conflicts resolve cleanly during Contract Bump PR before re-running `node schema/schema-test.js`.
3. **Executable Merge & Rollback Commands:**
   ```powershell
   # Promote validated wave -> track branch with --no-ff preserving wave boundary:
   git checkout integration/part1
   git merge --no-ff task/042-agent2-early-2k-anchor-lock
   node scripts/verify-harmony.mjs --wave W3-A   # runs unit tests, contract parity, zero-spend socket guard

   # Rollback a bad wave cleanly without rewriting shared history:
   git revert -m 1 <wave_merge_commit_sha>
   git tag rollback/W3-A-<timestamp>
   ```
4. **Joint Cross-Track Gate (`Tasks 193–200`):** Merge `integration/part1` + `integration/part2` into `integration/v1-rc`, run the **complete offline cross-track matrix** (`Tasks 193–199`), and ONLY when 100% green invoke the **final deferred bounded live connectivity check (`<= $2.00`)** in `Task 200` before tagging `v1.0.0`.
