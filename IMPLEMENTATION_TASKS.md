# True-Crime Documentary Pipeline: Master Implementation Task Plan (v3 Audit-Hardened)

## Purpose And Scope

This document is the authoritative, end-to-end engineering task plan for implementing the **Automated Hybrid True-Crime Documentary YouTube Pipeline** from zero code to a production-certified single-host system delivering up to **10 twenty-minute (1,200-second) documentaries per month** using **`gemini-omni-1.2-flash` via the official Gemini Interactions API (`~$8.00–$10.40/ep` @ `720p`, `<= 10` clips / `80s` max, `$135/mo` total autonomous compute cap) + DeepSeek V4.1 Flash/V4-Pro (`~$0.75–$1.90/ep`) + Gemini TTS/ASR (`~$0.45/ep`)**, with separate optional adapters (`VERTEX_VEO_ENTERPRISE`, `HUMAN_BATCH_DESK`), a **mandatory 5-gate human release approval boundary**, and an honest post-publish YouTube Analytics loop.

It resolves all 22 architectural, provider-shutdown, schema, legal/rights, security, and strategy findings (`F-01`–`F-22`, November 23, 2026) across **200 detailed, disjoint-scope, agent-executable tasks** (`Task 001` through `Task 200`).

## Two-Developer Parallel Execution Model (Part 1 & Part 2)

This repository is engineered so **two developers build and test 100% independently in parallel** after a shared Day-1 contract freeze (`Task 001`–`004`), immediately validating a **genuine Milestone M0.5 Minimal End-to-End Thin Vertical Slice** (`1` primary-record case + `1` clearly labeled illustrative 2K scene + authoritative `4-motif` MVP slice + `1` live bounded `gemini-omni-1.2-flash` sandbox call + `-14.0 LUFS` master + 5-gate human sign-off) before scaling to all 12 motifs and merging cleanly in `Task 193`–`200`:

| Track | Task Range | Developer / Team | Owned Packages & Subtrees | Independent Verification Mechanism |
|---|---|---|---|---|
| **Shared Foundation** | `Task 001`–`004` | Shared (Day-1 Freeze) | Root configs, `providers.yaml` (`gemini-omni-1.2-flash`, `max_hero_clips=10`, `$10.40/ep`), `scripts/`, `packages/shared_contracts/`, `schema/` v3 (`SQLite >= 3.51.3`), `fixtures/golden_manifests/` | `node schema/schema-test.js` (**12/12**), `pytest schema/schema_test.py`, Pydantic/Zod parity, single `MOTIF_REGISTRY_V1` |
| **Part 1 · Upstream Brain & Control Plane** | `Task 005`–`100` | **Developer A (Part 1)** | `packages/db/`, `packages/agent1_scout/`, `packages/agent2_evidence/` (early illustrative 2K + `DRAFT->LOCKED` anchors), `packages/agent3_gatekeeper/`, `packages/voice_sync/`, `packages/agent4_director/`, `packages/orchestrator/` | Real scouting (authorized metadata leads, 30d full YT purge), INSERT+UPDATE disposition + quarantine, explicit anonymization states, component rights provenance, music-gated Demucs (`asr_hypothesis_disagreement`), spoken+visual PII scrub, segmented TTS/ASR, 13-Law linter, tested standalone against `RenderBackendStub` |
| **Part 2 · Visual Synthesis, Mastering, Cockpit & Analytics** | `Task 101`–`192` | **Developer B (Part 2)** | `packages/render_catalog/`, `packages/python_motion/`, `packages/crime_scene_2k/`, `packages/flow_adapter/`, `packages/agent6_mastering/`, `packages/analytics_feedback/`, `apps/batch_desk_ui/` | Real JS-boil Remotion renders (`30 fps`, authoritative 4-motif MVP -> 12 motifs), monochrome keyframes, sole-owner `crime_scene_2k` illustrative pan/zoom, crash-safe `gemini-omni-1.2-flash` (`budget_reservations` + `UNKNOWN_RECONCILE` + fail-closed Vision QA), per-track `-14 LUFS`, loopback FastAPI (`127.0.0.1` + auth token) + 5-gate human release UI, honest Analytics (`UNKNOWN` default + Studio CSV), tested standalone against `fixtures/golden_manifests/` |
| **M0.5 Early Slice, Merge & V1 Certification** | `Task 193`–`200` | **Both Developers (Joint)** | `packages/integration_bridge/`, `tests/integration/`, `benchmarks/` | Early M0.5 minimal live slice (`Task 193`, incl. bounded Omni sandbox contract check), full 12-motif live adapter, Legal/PII/Rights Red-Team Gauntlet, 3-Slot Conveyor & Crash Soak, `$135/mo` 10-Ep Economics Audit, `V1_RELEASE_SCORECARD.md` |

## Non-Negotiable Architectural Ground Truth (v3 Audit-Hardened)

1. **Honest 1,200-Second Split & Supported Provider ([economics-and-credit-math.md](economics-and-credit-math.md)):** Veo 3.1 Preview on Gemini Developer API shut down Oct 22, 2026 (`F-01`). Primary default is **`gemini-omni-1.2-flash`** via **Gemini Interactions API** (`google-genai >= 2.30.1`), conservatively budgeted at `$0.10/sec` @ `720p` (verified via bounded M0.5 live sandbox invoice). Single source of truth in `providers.yaml` + DB: **`13.0 min (780s)`** Code/FOIA (`$0` video), **`5.67 min (340s)`** `STILL_2K_PANZOOM` (`crime_scene_2k` sole owner), and **`1.33 min (80s)`** `FLOW_HERO_VIDEO` (**`MAX_HERO_CLIPS = 10`**, `max_hero_duration_sec = 80s`, `$8.00` base / **`$10.40` durable SQLite USD cap/ep**, **`$135/mo`** total autonomous cap @ 10 eps). `VERTEX_VEO_ENTERPRISE` and `HUMAN_BATCH_DESK` are separate non-interchangeable adapters (`F-02`).
2. **Crash-Safe Idempotency, T2V/F2V Modes & Durable USD Cap ([flow-hybrid-and-batch-desk.md](flow-hybrid-and-batch-desk.md)):** `flow_jobs` enforces `UNIQUE (episode_id, scene_id)`, `idempotency_key`, persisted `provider_operation_id`, `prompt_mode` (`TEXT_TO_VIDEO` null frames / `FIRST_FRAME` / `FIRST_AND_LAST_FRAME <= 10s`), and explicit crash states (`SUBMITTING`, `RUNNING`, `UNKNOWN_RECONCILE`, fail-closed `PENDING_MANUAL_SPOT_CHECK`). Paid admission control lives strictly in `pipeline.db` `budget_reservations` (`trg_budget_cap_guard`), never async `telemetry.db` (`F-07`, `F-10`, `F-18`).
3. **Truthful State Machines, Illustrative Labeling & 5-Gate Human Release Sign-Off ([evidence-and-fact-ledger.md](evidence-and-fact-ledger.md), [legal-copyright-and-adsense.md](legal-copyright-and-adsense.md)):** `cases` guards disposition on BOTH INSERT & UPDATE and auto-quarantines downstream episodes (`QUARANTINED_LEGAL_HOLD`) on reversal (`F-03`); `anonymization_status` defaults to `NOT_STARTED` and `spatial_anchors.lock_status` defaults to `DRAFT` (`F-04`); all 2K plates carry `is_illustrative_reconstruction = 1` + visible **`ILLUSTRATIVE RECONSTRUCTION — NOT CRIME SCENE PHOTO`** watermark (`F-05`); `trg_episode_release_gate` requires ALL 5 human gates (`FACTUAL_ACCURACY`, `PRIVACY_PII`, `SOURCE_RIGHTS`, `SYNTHETIC_DISCLOSURE`, `ILLUSTRATIVE_LABELING`) approved for `ready_bundle_sha256` before export (`F-06`).
4. **Segmented Non-Overlapping Timeline & Single Motif Registry ([voice-first-and-asr-sync.md](voice-first-and-asr-sync.md), [code-animation-catalog.md](code-animation-catalog.md)):** `voice_segments` & `scenes` enforce kind-specific media checks and non-overlap triggers + `timeline_validated_sha256` (`F-09`). Single `MOTIF_REGISTRY_V1` freezes the **4-Motif MVP Slice** (`StickmanStage`, `AudioEvidenceCard`, `RedactedDocReveal`, `FoiaFootageFrame`) and assigns `Illustrative2KPanZoom` strictly to Python `crime_scene_2k` (`F-16`).
5. **Conflict-Free 13-Law Linter ([director-and-13-laws.md](director-and-13-laws.md)):** Byte-0 global static prompt caching; split Law 11/12 templates (`TEXT_TO_VIDEO` vs `FIRST_FRAME`/`FIRST_AND_LAST_FRAME`); cinematography bigram whitelist (`tracking shot`); `>= 2.5s` remainder splits; Act-constrained `RULE_02`; non-neighbor `fallback_spec`; flexible `210–270s` boundary-snapped `CaseBoardSpine`; CSS layout Safe-Zones.
6. **Remotion JS Line Boil (Benchmark Target) & Single-Pass Grading ([code-animation-catalog.md](code-animation-catalog.md)):** Zero SVG `<feTurbulence>` filters; deterministic **6 fps JS polyline vertex-jitter** at **`30 fps`** (`<5s` single-scene heal treated as a **Design Target** verified empirically on local hardware in `Task 131`, `F-21`); **zero grain in Remotion/`crime_scene_2k`**—Agent 6 applies continuous paper grain & vignette **once** across non-FOIA clips (leaving `FOIA_REAL_FOOTAGE` raw).
7. **Component Rights Provenance, Honest ASR Disagreement & Audio Mastering ([legal-copyright-and-adsense.md](legal-copyright-and-adsense.md)):** 17 U.S.C. § 105 narrowed strictly to federal-employee works (`F-14`, component-level `creator_entity`/`rights_holder`/`license_basis` blocking `RESTRICTED_NO_REUSE`); music-gated Demucs paired with honest **`asr_hypothesis_disagreement`** (reserving true WER for offline labeled reference corpus, `F-15`); visual + spoken PII scrub; `"TRANSCRIPT DRAMATIZATION"` badge; per-track pre-norm -> `linear=true` `-14.0 LUFS` master pass. Policy checks are risk controls, never guaranteed monetization (`F-13`).
8. **Pinned SQLite `>= 3.51.3`, Loopback FastAPI Security & Honest YouTube APIs ([database-and-state-design.md](database-and-state-design.md)):** Python sole writer enforcing **`SQLite >= 3.51.3`** on local host storage (`F-22`); loopback-only FastAPI (`127.0.0.1` + `X-Local-Auth-Token` + localhost CORS + `audit_log`, `F-19`); NO unsupported third-party `captions.download` (`F-11`); non-null 30-day YouTube full-field retention purge (`F-20`); NO fabricated `videos.list` monetization field (`adsense_status` defaults to `UNKNOWN`, populated via Studio CSV / manual entry, `F-12`).

## Multi-Agent Git Worktree & Disjoint Subtree Protocol

- **Worktree Isolation:** Every task runs in `../tc-wt/task-NNN-<slug>` on branch `task/NNN-<slug>` via `node scripts/agent-worktree.mjs create NNN <slug>`.
- **Commit-Only, Never-Merge:** Agents commit ONLY on `task/NNN-<slug>` (`TC-Task-ID`, `TC-Track`, `TC-Never-Merge: true`).
- **Disjoint Write Scope:** `scripts/verify-harmony.mjs --task NNN` blocks out-of-scope edits, secret leaks, or schema/diagram drift.

---

## Task Roadmap

### Task 001: Bootstrap Hybrid Monorepo, `providers.yaml` Registry, Worktree CLI & Part 1/2 Scope Guardrails

- **Track & Owner:** `Shared Foundation` (Day-1 Prerequisite)
- **Milestone:** `M0 · Shared Contract Freeze & Provider Registry`
- **Depends On:** `None`
- **Git Worktree & Branch:** `main` -> `integration/main` (tags `foundation/task-001-complete`)
- **Owned Write Scope:** Root `pyproject.toml`, `uv.lock`, `package.json`, `pnpm-workspace.yaml`, `tsconfig.base.json`, `providers.yaml`, `craft_rubric.yaml`, `.gitignore`, `.gitattributes`, `scripts/agent-worktree.mjs`, `scripts/verify-harmony.mjs`, `.agent-handoffs/TEMPLATE.md`, empty package shells under `packages/*` and `apps/*`
- **Mandatory Reference Files:** [README.md](README.md), [CONTRIBUTING_AGENTS.md](CONTRIBUTING_AGENTS.md), [parallel-part1-part2-architecture.md](parallel-part1-part2-architecture.md), [director-and-13-laws.md](director-and-13-laws.md)
- **Shared Contracts Produced:** Full Python (`3.12+`) + TypeScript (`Node 22+ / pnpm 10`) monorepo, config-driven `providers.yaml`, concise `craft_rubric.yaml` (`<= 150 lines`), repo-wide offline zero-spend test harness, and wave-ordered worktree CLI

#### Scope And Implementation Requirements

- [ ] Initialize Git (`core.longpaths=true`, `core.autocrlf=false`), `.gitattributes`, and `.gitignore` blocking `.env*`, `*.db*`, `node_modules/`, `.venv/`, `ready_to_upload/`, and `artifacts/`.
- [ ] Author config-driven `providers.yaml` centralizing ALL model IDs (`gemini-omni-1.2-flash` Interactions API `@ $0.10/sec` conservative 720p plan, `max_hero_clips = 10`, `max_hero_duration_sec = 80s`, `$10.40/ep` video cap, **`$135/mo` ALL-providers global ceiling**, DeepSeek dual `0%`-cache / cached projections, local WhisperX aligner) so zero model strings or rates are hardcoded across packages (`F-01`, `F-02`, `F-03`).
- [ ] Author concise **`craft_rubric.yaml`** (`<= 150 lines`, `F-06`) encoding structured documentary pacing & visual clarity principles (`"interactive"` = high-engagement visual curiosity hooks/pacing) cleanly separated from episode research and per-scene `ScenePlan` inputs.
- [ ] Enforce **Repo-Wide Zero-Spend Offline Test Guard (`F-01`)**: install global `pytest` socket-blocking & Vitest outbound-fetch blockers + scrubbed provider env vars across all ordinary worktree/CI test invocations, permitting outbound paid provider sockets ONLY when both `--live-sandbox` AND `ALLOW_PAID_SANDBOX=1` are explicitly passed post-integration (`Task 200`).
- [ ] Implement `scripts/agent-worktree.mjs` (`create`, `check`, `commit`, `wave-merge`, `wave-rollback`) and `scripts/verify-harmony.mjs --task NNN --wave <id>` enforcing disjoint Part 1/Part 2 write ownership, wave dependency ordering (`F-07`), v4 contract drift scanning (`F-04`), secret scans, `node schema/schema-test.js`, and `node tools/merge-diagrams.js`.
- [ ] Scaffold Python workspace (`shared_contracts`, `db`, `agent1_scout`, `agent2_evidence`, `agent3_gatekeeper`, `voice_sync`, `agent4_director`, `orchestrator`, `python_motion`, `crime_scene_2k`, `flow_adapter`, `agent6_mastering`, `analytics_feedback`) and pnpm workspace (`shared-contracts-ts`, `render_catalog`, `batch_desk_ui`, `e2e`).

#### Edge Cases And Failure Modes

- Windows 260-char `MAX_PATH` limits: enforce sibling `../tc-wt/` root and `core.longpaths=true`.
- Hardcoded model checkpoint strings drifting from `providers.yaml`: add lint check flagging unconfigured literal model names in source packages.

#### Bug Prevention And Invariants

- **Config-Driven Provider Invariant:** All LLM/Vision/TTS/ASR/Video pricing and model IDs resolve exclusively from `providers.yaml`.
- **Single Lockfile Baseline Invariant:** Downstream tasks declare new dependencies in `.agent-handoffs/task-NNN.md`.

#### Independent Testability & Parallel Isolation

- Establishes `foundation/task-001-complete` tag cleanly for Part 1 and Part 2 branching.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `node scripts/agent-worktree.mjs create 000 smoke` -> verify out-of-scope block & secret scan -> remove scratch branch.
- [ ] Confirm `pnpm typecheck`, `uv run pytest --collect-only`, `node schema/schema-test.js`, and `node tools/merge-diagrams.js` pass.
- **Acceptance:** Monorepo, `providers.yaml`, and harmony guardrails green on Day 1.

### Task 002: Freeze `packages/shared_contracts` v4 (`ScenePlan`, `MOTIF_REGISTRY_V1`, `prompt_mode`, Analytics Models)

- **Track & Owner:** `Shared Foundation`
- **Milestone:** `M0 · Canonical v4 Contract Freeze`
- **Depends On:** `Task 001`
- **Git Worktree & Branch:** `task/002-frozen-shared-contracts` in `../tc-wt/task-002-frozen-shared-contracts`
- **Owned Write Scope:** `packages/shared_contracts/**`, `packages/shared-contracts-ts/**`, `.agent-handoffs/task-002.md`
- **Mandatory Reference Files:** [parallel-part1-part2-architecture.md](parallel-part1-part2-architecture.md), [director-and-13-laws.md](director-and-13-laws.md), [voice-first-and-asr-sync.md](voice-first-and-asr-sync.md), [prompt-contracts.md](prompt-contracts.md)
- **Shared Contracts Produced:** Bi-directional Pydantic v2 + Zod + JSON Schema parity models (`v4`) + pure-math external-margin `10x10` coordinate transform helpers

#### Scope And Implementation Requirements

- [ ] Freeze Pydantic v2 (`extra="forbid"`) & Zod (`.strict()`) models for `SeedPacket`, `TemporalFactLedger`, `ComplianceClearedCase`, **`ScenePlan`** (`story_purpose`, `intended_audience_effect`, `approved_narration_text`, `narration_version_sha256`, `cited_fact_ids_json`, `visual_concept`, `visual_prompt`, `keyframe_refs_json`, `expected_output_summary`, `transition_spec_json`, `sound_cues_json`, `edit_instructions`, `acceptance_criteria_json`, `plan_status` `F-05`), segmented `VoiceTrackManifest`, `SpatialAnchor`, `CaseBible`, `ProductionManifest`, `TimelineSpec` (`30 fps`, **`prompt_mode: "TEXT_TO_VIDEO" | "FIRST_FRAME" | "FIRST_AND_LAST_FRAME"`**, `MOTIF_REGISTRY_V1`), `FlowJobCard`, `EpisodeAnalyticsSnapshot`, and `ReadyToUploadPack`.
- [ ] Include pure deterministic `grid_cell_to_pixel_and_zoom(...)` helper cleanly in `packages/shared_contracts`.
- [ ] Define `RenderBackendPort`, `ProviderRegistryLoader` (`providers.yaml`), and `CraftRubricLoader` (`craft_rubric.yaml`).

#### Edge Cases And Failure Modes

- Enum/field drift or retired identifiers (`FRAMES_MOTION_ONLY`, `VEO_3_1_LITE`, `CrimeScenePanZoom`): CI parity test fails immediately if deprecated v2 identifiers appear!

#### Bug Prevention And Invariants

- **Strict Canonical v4 Schema Parity Invariant:** Zero `extra` fields permitted across Python/TypeScript boundaries.

#### Independent Testability & Parallel Isolation

- Freezes the exact contract seam decoupling Developer A (Part 1) and Developer B (Part 2).

#### Verification, Testing And Acceptance Criteria

- [ ] Run offline `uv run pytest packages/shared_contracts` and `pnpm --filter @tc/shared-contracts-ts test` verifying 100% parity on 60 valid and 60 adversarial vectors (`$0` API calls).
- **Acceptance:** Frozen v4 shared contracts verified across Python and TypeScript.

### Task 003: Freeze Executable SQLite Schemas v4 (`pipeline.sql` & `telemetry.sql`) & Cross-Runtime Tests

- **Track & Owner:** `Shared Foundation`
- **Milestone:** `M0 · Canonical v4 Contract Freeze`
- **Depends On:** `Task 001`, `Task 002`
- **Git Worktree & Branch:** `task/003-frozen-sqlite-schemas` in `../tc-wt/task-003-frozen-sqlite-schemas`
- **Owned Write Scope:** `schema/**`, `.agent-handoffs/task-003.md`
- **Mandatory Reference Files:** [database-and-state-design.md](database-and-state-design.md), [schema/pipeline.sql](schema/pipeline.sql), [schema/telemetry.sql](schema/telemetry.sql), [schema/queries.sql](schema/queries.sql)
- **Shared Contracts Produced:** Verified `schema/pipeline.sql` v4 (`scene_plans`, `monthly_budget_ledger`, `provider_spend_reservations`, `trg_offline_test_zero_spend_guard`, `trg_provider_global_budget_cap_guard`, `release_approvals`, `trg_case_disposition_quarantine`, `total_input_tokens >= cached_input_tokens`) + dual Node/Python tests

#### Scope And Implementation Requirements

- [ ] Freeze `schema/pipeline.sql` v4 (`schema_version = '4'`), `schema/telemetry.sql` v3, and `schema/queries.sql` v4.
- [ ] Implement `schema/schema_test.py` mirroring ALL **12** scenarios verified in `schema/schema-test.js`!

#### Edge Cases And Failure Modes

- `UPDATE` bypassing `INSERT` disposition/hedging/overlap triggers or non-zero `OFFLINE_TEST` budget slips: all guarded cleanly in SQLite triggers.

#### Bug Prevention And Invariants

- **Python Sole-Writer, Global `$135/mo` Cap & Zero-Spend Offline Test Invariant.**

#### Independent Testability & Parallel Isolation

- Validated offline in Node 24 and Python 3.12+.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `node schema/schema-test.js` (`12/12` pass) and `uv run pytest schema/schema_test.py` (`12/12` pass).
- **Acceptance:** `pipeline.sql` v4 and `telemetry.sql` v3 frozen and verified.

### Task 004: Build Deterministic v4 Golden Fixture Packs & Synthetic Media Assets (`fixtures/`)

- **Track & Owner:** `Shared Foundation`
- **Milestone:** `M0 · Canonical v4 Contract Freeze`
- **Depends On:** `Task 002`, `Task 003`
- **Git Worktree & Branch:** `task/004-golden-fixture-packs` in `../tc-wt/task-004-golden-fixture-packs`
- **Owned Write Scope:** `fixtures/golden_manifests/**`, `fixtures/recorded_apis/**`, `fixtures/synthetic_media/**`, `.agent-handoffs/task-004.md`
- **Mandatory Reference Files:** [parallel-part1-part2-architecture.md](parallel-part1-part2-architecture.md), [code-animation-catalog.md](code-animation-catalog.md)
- **Shared Contracts Produced:** Three v4 Golden Packs (`ep_golden_01_20min`, `ep_golden_02_2strike_fallback`, `ep_golden_03_2k_grid_heavy`) + synthetic media + adversarial prompt-injection test payloads

#### Scope And Implementation Requirements

- [ ] Build 3 Golden Packs conforming strictly to **v4** contracts: **`13.0m / 5.67m / 1.33m`** runtime split (`max_hero_clips = 10` / `80s`), versioned `ScenePlan[]` (`EDITED_APPROVED`), `MOTIF_REGISTRY_V1` components, `prompt_mode in {TEXT_TO_VIDEO, FIRST_FRAME, FIRST_AND_LAST_FRAME}`, segmented `VoiceTrackManifest`, explicitly locked `spatial_anchors` on illustrative 2K plates, monochrome Start/End PNGs (zero crimson), non-neighbor `fallback_spec`s, and honest `episode_analytics` mocks.
- [ ] Generate synthetic media & adversarial injection fixtures (`911_8khz_distorted.wav`, `bodycam_440hz_music_042profanity.mp4`, `911_spoken_pii.wav`, mocked `recorded_apis/`, plus synthetic prompt-injection breakout `</data>` strings).

#### Edge Cases And Failure Modes

- Git bloat from binary assets: keep all synthetic media clips compact (`2–10s`, `< 500 KB`) and validate JSONs against Pydantic + Zod.

#### Bug Prevention And Invariants

- **100% v2 Contract-Valid Fixtures Invariant:** Both Part 1 and Part 2 test immediately without blocking.

#### Independent Testability & Parallel Isolation

- Unblocks Developer A (`005`–`100`) and Developer B (`101`–`192`) concurrently.

#### Verification, Testing And Acceptance Criteria

- [ ] Run fixture validator confirming all 3 Golden Packs and recorded API mocks validate cleanly.
- **Acceptance:** Golden fixtures and synthetic media verified for parallel Part 1 & Part 2 execution.

---

### PART 1 — Developer A: Upstream Brain, Early 2K Lock, Gatekeeper, Voice & Director (`Tasks 005`–`100`)

### Task 005: Implement Python Sole-Writer SQLite WAL Driver & `BEGIN IMMEDIATE` Pool (`packages/db`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 003`
- **Git Worktree & Branch:** `task/005-db-wal-sole-writer` in `../tc-wt/task-005-db-wal-sole-writer`
- **Owned Write Scope:** `packages/db/src/connection.py`, `packages/db/tests/test_connection.py`, `.agent-handoffs/task-005.md`
- **Mandatory Reference Files:** [database-and-state-design.md](database-and-state-design.md), [schema/pipeline.sql](schema/pipeline.sql)
- **Shared Contracts Consumed / Produced:** Python sole-writer `PipelineDbPool` (`WAL`, `synchronous=FULL`, `foreign_keys=ON`, `busy_timeout=5000`, `BEGIN IMMEDIATE`)

#### Scope And Implementation Requirements

- [ ] Implement `PipelineDb` enforcing `BEGIN IMMEDIATE` inside an in-process `RLock` with bounded jitter retries on transient `SQLITE_BUSY` / Windows `EBUSY`.
- [ ] **SQLite Runtime Version Pin & Local Filesystem Guard (`F-22`):** At startup, assert `sqlite3.sqlite_version_info >= (3, 51, 3)` (fixing SQLite's documented WAL-reset concurrency bug), verify `pipeline.db` resides on local host storage (rejecting SMB/NFS/UNC network paths), and log active SQLite version to `audit_log`.
- [ ] Enforce Python sole-writer ownership lock (`meta` owner heartbeat + OS advisory file lock) while allowing short-lived read transactions and periodic `PASSIVE`/`TRUNCATE` WAL checkpoints.

#### Edge Cases And Failure Modes

- Unclosed cursor starving WAL checkpoints: strictly enforce context-manager cleanup on every query.

#### Bug Prevention And Invariants

- **Python Sole-Writer Serialization Invariant:** Zero cross-runtime Node/TS direct writes to `pipeline.db`.

#### Independent Testability & Parallel Isolation

- 16-thread stress test on disk WAL SQLite DB.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/db/tests/test_connection.py` confirming 0 `SQLITE_BUSY` errors under 16-thread contention.
- **Acceptance:** Python sole-writer WAL driver verified.

### Task 006: Implement Database Migration Runner & `VACUUM INTO` Pre-Upgrade Backup (`packages/db`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 005`
- **Git Worktree & Branch:** `task/006-db-migrations-backup` in `../tc-wt/task-006-db-migrations-backup`
- **Owned Write Scope:** `packages/db/src/migrations.py`, `packages/db/tests/test_migrations.py`, `.agent-handoffs/task-006.md`
- **Mandatory Reference Files:** [database-and-state-design.md](database-and-state-design.md), [schema/pipeline.sql](schema/pipeline.sql)
- **Shared Contracts Consumed / Produced:** `DbInitializer` & `MigrationRunner` with `VACUUM INTO` backup + `quick_check` auto-restore

#### Scope And Implementation Requirements

- [ ] Bootstrap `pipeline.db` and `telemetry.db` from `schema/*.sql` (`schema_version = 4`), run `VACUUM INTO` pre-migration snapshot + `PRAGMA quick_check`, and roll back automatically if any migration step fails.

#### Edge Cases And Failure Modes

- Older code opening a newer schema version: fail fast with `SchemaVersionTooNewError`.

#### Bug Prevention And Invariants

- **Backup-Before-Migrate Invariant:** Never alters schema without verified `VACUUM INTO` snapshot.

#### Independent Testability & Parallel Isolation

- Standalone temp-file migration and failure-rollback tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/db/tests/test_migrations.py` passing fresh init, migration, and rollback checks.
- **Acceptance:** Migration & backup runner verified.

### Task 007: Implement 3-Bucket YouTube Quota Tracker & 30-Day ToS Payload TTL Purge (`packages/db`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 005`
- **Git Worktree & Branch:** `task/007-youtube-quota-tos-ttl` in `../tc-wt/task-007-youtube-quota-tos-ttl`
- **Owned Write Scope:** `packages/db/src/quota_repo.py`, `packages/db/tests/test_quota_repo.py`, `.agent-handoffs/task-007.md`
- **Mandatory Reference Files:** [scout-and-saturation.md](scout-and-saturation.md), [schema/queries.sql](schema/queries.sql)
- **Shared Contracts Consumed / Produced:** `QuotaTracker` (`yt_search 100`, `yt_general 10000`, `yt_insert 100`, `15`-call daily re-check reserve) + 30-day YouTube ToS TTL purge

#### Scope And Implementation Requirements

- [ ] Implement atomic `consume_quota()` with Pacific midnight window reset and hard `15-call` `yt_search` floor reserved strictly for daily Pre-Render Saturation Re-Checks.
- [ ] Implement `purge_expired_yt_api_records(now_ms)` (`schema/queries.sql`, `F-20`) enforcing mandatory non-null `yt_ttl_expires_at` on every `TRACK_A_OUTLIER` row and clearing **all YouTube API-derived fields** (`raw_yt_payload_json`, `views_count`, `outlier_ratio`, YT metadata inside `seed_packet_json`) after 30 days (transitioning unconsumed rows to `EXPIRED_TOS_PURGED`) while preserving only independently verified court/FOIA primary-record `cases`.

#### Edge Cases And Failure Modes

- Nightly watchlist poll accidentally requesting `yt_search` bucket: structurally reject `nightly_poll` tag on `yt_search`.

#### Bug Prevention And Invariants

- **30-Day ToS Retention & Zero Quota Overrun Invariant:** Raw YT API blobs never survive `> 30` days.

#### Independent Testability & Parallel Isolation

- Fake-clock SQLite tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/db/tests/test_quota_repo.py` confirming 15-call reserve, midnight PT reset, and 30-day TTL purge.
- **Acceptance:** Quota tracker & ToS TTL purge verified.

### Task 008: Implement CourtListener 125/Day Rate-Paced Repository & Persistent Cache (`packages/db`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 005`, `Task 007`
- **Git Worktree & Branch:** `task/008-courtlistener-rate-cache` in `../tc-wt/task-008-courtlistener-rate-cache`
- **Owned Write Scope:** `packages/db/src/courtlistener_repo.py`, `packages/db/tests/test_courtlistener_repo.py`, `.agent-handoffs/task-008.md`
- **Mandatory Reference Files:** [scout-and-saturation.md](scout-and-saturation.md), [evidence-and-fact-ledger.md](evidence-and-fact-ledger.md)
- **Shared Contracts Consumed / Produced:** `CourtListenerRateLimiter` enforcing `5/min`, `50/hr`, `125/day` + persistent `courtlistener_cache`

#### Scope And Implementation Requirements

- [ ] Enforce `<= 5 req/min`, `<= 50 req/hr`, and `<= 125 req/day` simultaneously, serving cached opinions (`courtlistener_cache`) at `0` API calls and honoring HTTP 429 `Retry-After`.

#### Edge Cases And Failure Modes

- Burst verification calls exceeding `5/min`: pace smoothly with deterministic token bucket.

#### Bug Prevention And Invariants

- **3-Window Ceiling Invariant:** Never exceeds `5/min`, `50/hr`, or `125/day`.

#### Independent Testability & Parallel Isolation

- Fake-clock sliding-window unit tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/db/tests/test_courtlistener_repo.py` verifying cache hit reuse and 3-window pacing.
- **Acceptance:** CourtListener rate limiter & cache verified.

### Task 009: Implement Google Pro Account Ledger With `24h + 5m` Rolling Reset Drift Lock (`packages/db`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 005`
- **Git Worktree & Branch:** `task/009-account-ledger-24h-lock` in `../tc-wt/task-009-account-ledger-24h-lock`
- **Owned Write Scope:** `packages/db/src/accounts_repo.py`, `packages/db/tests/test_accounts_repo.py`, `.agent-handoffs/task-009.md`
- **Mandatory Reference Files:** [economics-and-credit-math.md](economics-and-credit-math.md), [flow-hybrid-and-batch-desk.md](flow-hybrid-and-batch-desk.md), [schema/queries.sql](schema/queries.sql)
- **Shared Contracts Consumed / Produced:** `AccountPoolLedger` tracking `first_daily_spend_utc_ms` and `next_daily_reset_utc_ms = first_spend + 86_400_000 + 300_000` (fixing rolling 24h drift!)

#### Scope And Implementation Requirements

- [ ] Track `monthly_credits_left (1,000)`, `daily_credits_left (50)`, `first_daily_spend_utc_ms`, and **`next_daily_reset_utc_ms = first_daily_spend_utc_ms + 86_400_000 + 300_000`** (`24h + 5m` safety guard) per optional Pro account.
- [ ] Block daily-credit attempts before `next_daily_reset_utc_ms` unless explicitly using `MONTHLY_BASE`, preventing silent monthly reserve burn when clicking 2 minutes early!

#### Edge Cases And Failure Modes

- Operator attempts Batch Desk run 3 minutes before 24h reset expires: `is_account_daily_locked(account_id, now_ms)` returns locked status + exact remaining `seconds_until_reset`.

#### Bug Prevention And Invariants

- **Zero Early-Click Monthly Drain Invariant:** Daily pool locks until `24h + 5m` passes cleanly.

#### Independent Testability & Parallel Isolation

- Fake-clock SQLite tests across 14-day multi-shift simulation.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/db/tests/test_accounts_repo.py` proving `24h + 5m` lock prevents drift and unintended monthly draws.
- **Acceptance:** Rolling `24h + 5m` account ledger verified.

### Task 010: Implement Cross-Provider Global Budget Ledger & Episode USD/Escrow Governor (`packages/db`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 005`, `Task 009`
- **Git Worktree & Branch:** `task/010-global-budget-ledger` in `../tc-wt/task-010-global-budget-ledger`
- **Owned Write Scope:** `packages/db/src/escrow_repo.py`, `packages/db/tests/test_escrow_repo.py`, `.agent-handoffs/task-010.md`
- **Mandatory Reference Files:** [economics-and-credit-math.md](economics-and-credit-math.md), [schema/pipeline.sql](schema/pipeline.sql), [schema/queries.sql](schema/queries.sql)
- **Shared Contracts Consumed / Produced:** `GlobalBudgetLedgerRepository` managing `monthly_budget_ledger` (`$135/mo ALL_PROVIDERS` cap + per-provider sub-caps) and `provider_spend_reservations` (with `$0 OFFLINE_TEST` guard + `$10.40/ep` `gemini_omni` video ceiling)

#### Scope And Implementation Requirements

- [ ] Implement transactional `reserve_provider_budget()` and `settle_provider_budget()` (`schema/queries.sql`) enforcing **`trg_offline_test_zero_spend_guard`** (`purpose = 'OFFLINE_TEST' -> $0`) and **`trg_provider_global_budget_cap_guard`** (`ALL_PROVIDERS <= $135/mo`, per-provider sub-caps incl. `deepseek_chat` `$38/mo` `0%`-cache upper bound, and `$10.40/ep` video cap).
- [ ] Track Act 1 `<= 40%` hero allocation and `flow_backend_mode` (`GEMINI_OMNI_INTERACTIONS` vs `VERTEX_VEO_ENTERPRISE` vs `HUMAN_BATCH_DESK`).

#### Edge Cases And Failure Modes

- DeepSeek batch + Gemini Omni clip running concurrently near month-end hitting global `$135` across providers: transactional SQLite trigger blocks the overflow cleanly regardless of which provider came last!

#### Bug Prevention And Invariants

- **Single Authoritative Cross-Provider USD Ledger Invariant (`F-01`, `F-02`):** `telemetry.db` is NEVER queried for budget admission control.

#### Independent Testability & Parallel Isolation

- Offline SQLite concurrency & cross-provider overflow tests (`$0` API calls).

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/db/tests/test_escrow_repo.py` verifying `$0` `OFFLINE_TEST` guard, `$135/mo ALL_PROVIDERS` cap, and `$10.40/ep` cap.
- **Acceptance:** Global multi-provider USD budget repository verified.

### Task 011: Implement Flow Job Queue & SQL 2-Strike Circuit Breaker Repository (`packages/db`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 005`, `Task 010`
- **Git Worktree & Branch:** `task/011-flow-job-repo` in `../tc-wt/task-011-flow-job-repo`
- **Owned Write Scope:** `packages/db/src/flow_jobs_repo.py`, `packages/db/tests/test_flow_jobs_repo.py`, `.agent-handoffs/task-011.md`
- **Mandatory Reference Files:** [flow-hybrid-and-batch-desk.md](flow-hybrid-and-batch-desk.md), [schema/pipeline.sql](schema/pipeline.sql)
- **Shared Contracts Consumed / Produced:** `FlowJobRepository` supporting `GEMINI_API_USD` (`$0` released on safety blocks!) and `HUMAN_BATCH_DESK` pools

#### Scope And Implementation Requirements

- [ ] Implement `record_attempt()` tracking `pool_source` (`GEMINI_API_USD`, `VERTEX_USD`, `DAILY_CREDITS`, `MONTHLY_CREDITS`), settling `provider_spend_reservations` to `RELEASED` (`$0`) on safety blocks (`total_output_tokens == 0`) and persisting `provider_operation_id` / `UNKNOWN_RECONCILE` safely across crashes (`F-10`).
- [ ] Enforce Strike 1 -> `STRIKE_1_RETRY_SAFE` (`prompt_v2_safe`) and Strike 2 -> `SWITCHED_TO_FALLBACK` (`trg_flow_two_strike_breaker` blocking Attempt 3).

#### Edge Cases And Failure Modes

- Safety block in Gemini Omni Interactions mode: settle reservation cleanly as `RELEASED` (`actual_micro_usd = 0`) so safety-rejected prompts release reserved USD headroom back to escrow!

#### Bug Prevention And Invariants

- **Max 2 Attempts & Zero-Bill API Block Invariant:** API safety blocks never waste USD budget; 3rd retries are structurally impossible.

#### Independent Testability & Parallel Isolation

- Standalone SQLite repository tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/db/tests/test_flow_jobs_repo.py` verifying `$0` API safety-block billing and 2-strike fallback transition.
- **Acceptance:** Flow job & 2-strike repository verified.

### Task 012: Implement Multi-Episode Conveyor State Machine (`Up to 3` in `AWAITING_FLOW_BATCH`) (`packages/db`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 005`
- **Git Worktree & Branch:** `task/012-conveyor-state-repo` in `../tc-wt/task-012-conveyor-state-repo`
- **Owned Write Scope:** `packages/db/src/conveyor_repo.py`, `packages/db/tests/test_conveyor_repo.py`, `.agent-handoffs/task-012.md`
- **Mandatory Reference Files:** [flow-hybrid-and-batch-desk.md](flow-hybrid-and-batch-desk.md), [schema/pipeline.sql](schema/pipeline.sql)
- **Shared Contracts Consumed / Produced:** `ConveyorStateRepository` supporting `EVIDENCE_AND_2K_LOCKED` state and up to 3 concurrent `AWAITING_FLOW_BATCH` episodes (oldest-first)

#### Scope And Implementation Requirements

- [ ] Enforce valid directed transitions (`QUEUED -> SCOUTED -> EVIDENCE_AND_2K_LOCKED -> COMPLIANCE_PASSED -> SCENE_PLAN_APPROVED -> VOICE_READY -> MANIFEST_LINTED -> ANIMATIC_APPROVED -> CODE_RENDERED -> AWAITING_FLOW_BATCH -> POST_FLOW_PROCESSING -> MASTERED -> PENDING_HUMAN_SIGNOFF -> READY_TO_UPLOAD -> PUBLISHED`).
- [ ] Allow up to **3 concurrent episodes** in `AWAITING_FLOW_BATCH` (fixing the 1-slot 3-day stall bug in optional Batch Desk mode) and query oldest-first (`ORDER BY created_at ASC`).

#### Edge Cases And Failure Modes

- 4th episode trying to enter `AWAITING_FLOW_BATCH` while 3 multi-day episodes are queued: pause new scouting upstream cleanly (`BACKPRESSURE_QUEUE_FULL`) rather than letting stale cases rot.

#### Bug Prevention And Invariants

- **Oldest-First Drain & 3-Slot Cap Invariant:** Active Flow queue stays bounded `<= 3` and drains FIFO.

#### Independent Testability & Parallel Isolation

- Pure SQLite state-machine tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/db/tests/test_conveyor_repo.py` verifying 3-episode parking, FIFO order, and illegal-transition rejection.
- **Acceptance:** Non-deadlocking conveyor state repository verified.

### Task 013: Implement Entropy History & Post-Publish `episode_analytics` Repository (`packages/db`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 005`
- **Git Worktree & Branch:** `task/013-entropy-analytics-repo` in `../tc-wt/task-013-entropy-analytics-repo`
- **Owned Write Scope:** `packages/db/src/entropy_repo.py`, `packages/db/tests/test_entropy_repo.py`, `.agent-handoffs/task-013.md`
- **Mandatory Reference Files:** [director-and-13-laws.md](director-and-13-laws.md), [mastering-loudness-and-qa.md](mastering-loudness-and-qa.md)
- **Shared Contracts Consumed / Produced:** `EntropyAndAnalyticsRepository` managing `published_entropy_history` + `episode_analytics` feedback scores

#### Scope And Implementation Requirements

- [ ] Query last 5 cold-open archetypes (never repeating back-to-back) and last 3 `thumbnail_mood_vec` entries (preserving brand typography while rotating focal composition/mood).
- [ ] Store and query `episode_analytics` (`ctr_pct`, `retention_30s_pct`, `retention_min6_14_pct`, `avd_pct`, `watch_hours_total`, `rpm_micro_usd`, `adsense_status`) grouped by `cold_open_archetype` and `track` (`TRACK_A` vs `TRACK_B`) to weight future scouting/directing!

#### Edge Cases And Failure Modes

- Cold start (`0` published analytics rows): return balanced uniform weights across archetypes until `>= 3` episodes accumulate real telemetry.

#### Bug Prevention And Invariants

- **Closed-Loop Feedback Storage Invariant:** Analytics snapshots cleanly inform upstream archetype selection without mutating historical facts.

#### Independent Testability & Parallel Isolation

- Pure SQLite unit tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/db/tests/test_entropy_repo.py` verifying archetype rotation and analytics aggregation queries.
- **Acceptance:** Entropy & analytics repository verified.

### Task 014: Implement Config-Driven `telemetry.db` Cost & Cache-Hit Logger (`packages/db`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 001`, `Task 003`, `Task 005`
- **Git Worktree & Branch:** `task/014-telemetry-provider-cost-logger` in `../tc-wt/task-014-telemetry-provider-cost-logger`
- **Owned Write Scope:** `packages/db/src/telemetry_repo.py`, `packages/db/tests/test_telemetry_repo.py`, `.agent-handoffs/task-014.md`
- **Mandatory Reference Files:** [economics-and-credit-math.md](economics-and-credit-math.md), [schema/telemetry.sql](schema/telemetry.sql)
- **Shared Contracts Consumed / Produced:** `TelemetryCostLogger` calculating integer micro-USD dynamically from `providers.yaml`

#### Scope And Implementation Requirements

- [ ] Load token/audio/video rates dynamically from `providers.yaml` (DeepSeek `0%`-cache conservative & best-effort cached rates, Gemini TTS, `gemini-omni-1.2-flash` `~$0.10/sec` conservative 720p plan, Image API) and log asynchronously into **non-authoritative `telemetry.db` (`total_input_tokens` where `cached_input_tokens <= total_input_tokens` CHECK holds)** without ever gating paid admission control!
- [ ] Compute per-episode spend rollups and Byte-0 cross-episode cache-hit ratios, pruning rows `> 30` days.

#### Edge Cases And Failure Modes

- `providers.yaml` adds a new model checkpoint (`DeepSeek-V4.2`): cost logger picks up new entry automatically without Python code edits.

#### Bug Prevention And Invariants

- **Zero Hardcoded Rate & Zero Cross-DB Lock Invariant:** Pricing derives solely from `providers.yaml`.

#### Independent Testability & Parallel Isolation

- Unit tested with overridden temp `providers.yaml` fixture.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/db/tests/test_telemetry_repo.py` confirming config-driven pricing math and 30-day pruning.
- **Acceptance:** Config-driven `telemetry.db` logger verified.

---

### Task 015: Implement Dynamic Watchlist Seeder & Weekly Spillover Discovery/Pruning (`packages/agent1_scout`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 007`
- **Git Worktree & Branch:** `task/015-agent1-dynamic-watchlist` in `../tc-wt/task-015-agent1-dynamic-watchlist`
- **Owned Write Scope:** `packages/agent1_scout/src/watchlist.py`, `packages/agent1_scout/tests/test_watchlist.py`, `.agent-handoffs/task-015.md`
- **Mandatory Reference Files:** [scout-and-saturation.md](scout-and-saturation.md), [research/youtube-and-foia-mining.md](research/youtube-and-foia-mining.md)
- **Shared Contracts Consumed / Produced:** `WatchlistManager` managing `250–400` active `2K–120K` channels with weekly spillover auto-discovery & dormant/graduated pruning

#### Scope And Implementation Requirements

- [ ] Seed initial channels via bulk `channels.list` (`50` IDs/unit, `0 search.list`) mapping `UC...` -> `UU...`.
- [ ] Implement weekly **`discover_spillover_channels(search_results)`**: inspect channels surfaced during `search.list` alias checks (`Task 019`), batch-check `subscriberCount` (`2K–120K`) & topic match, promote qualifying channels (`discovered_via = 'SPILLOVER'`), and prune dormant (`> 180d` no upload) or graduated (`> 120K` subs) channels!

#### Edge Cases And Failure Modes

- Spillover channel is a true-crime Shorts farm or general pop-culture commentary: require `>= 3` long-form (`>= 10 min`) crime videos in last 10 uploads before admitting.

#### Bug Prevention And Invariants

- **Self-Refreshing Watchlist Invariant:** Watchlist continuously replaces burned-out or graduated channels without manual curation.

#### Independent Testability & Parallel Isolation

- Tested offline with `fixtures/recorded_apis/yt_channels_batch.json`.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent1_scout/tests/test_watchlist.py` verifying spillover admission, dormant pruning, and `0 search.list` cost.
- **Acceptance:** Dynamic watchlist manager verified.

### Task 016: Implement Nightly Zero-Search Playlist Poller & 50-ID Batch `videos.list` Fetcher (`packages/agent1_scout`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 015`
- **Git Worktree & Branch:** `task/016-agent1-zero-search-poller` in `../tc-wt/task-016-agent1-zero-search-poller`
- **Owned Write Scope:** `packages/agent1_scout/src/poller.py`, `packages/agent1_scout/tests/test_poller.py`, `.agent-handoffs/task-016.md`
- **Mandatory Reference Files:** [scout-and-saturation.md](scout-and-saturation.md)
- **Shared Contracts Consumed / Produced:** `NightlyZeroSearchPoller` (`~450` `yt_general` units/day, `0 yt_search`)

#### Scope And Implementation Requirements

- [ ] Poll `playlistItems.list` on active `UU...` playlists + batch `videos.list` (`50` IDs/call), filtering out Shorts (`< 600s` / `#shorts`) and tagging `yt_ttl_expires_at = now + 30 days`.

#### Edge Cases And Failure Modes

- API returns ISO-8601 duration `PT58S` or `PT4M10S`: filter strictly `duration_sec >= 600` (long-form documentary comps only).

#### Bug Prevention And Invariants

- **Zero `search.list` Polling & 30-Day TTL Tagging Invariant:** Never touches `yt_search`; stamps ToS TTL on every fetched payload.

#### Independent Testability & Parallel Isolation

- Tested offline on 300-channel mock fixture.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent1_scout/tests/test_poller.py` asserting `0 yt_search` calls and Shorts exclusion.
- **Acceptance:** Nightly zero-search poller verified.

### Task 017: Implement 20-Video Rolling Median & Outlier Ratio (`OR >= 3.5x`) Filter (`packages/agent1_scout`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 016`
- **Git Worktree & Branch:** `task/017-agent1-outlier-ratio` in `../tc-wt/task-017-agent1-outlier-ratio`
- **Owned Write Scope:** `packages/agent1_scout/src/outlier_filter.py`, `packages/agent1_scout/tests/test_outlier_filter.py`, `.agent-handoffs/task-017.md`
- **Mandatory Reference Files:** [scout-and-saturation.md](scout-and-saturation.md)
- **Shared Contracts Consumed / Produced:** `OutlierRatioScorer` (`OR >= 3.5x`, `>= 20K` views, `<= 12 mo`)

#### Scope And Implementation Requirements

- [ ] Compute channel 20-video median (`statistics.median`, minimum 5 prior long-form videos), score `OR = views / median`, and retain top 15–20 candidates meeting Sweet Spot bounds.

#### Edge Cases And Failure Modes

- New 2-video channel distorting median: enforce `min_history_videos >= 5`.

#### Bug Prevention And Invariants

- **Median-Not-Mean Skew Immunity Invariant:** Legacy viral outliers do not inflate baseline median.

#### Independent Testability & Parallel Isolation

- Pure Python unit tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent1_scout/tests/test_outlier_filter.py` passing skewed viral distribution checks.
- **Acceptance:** Outlier Ratio filter verified.

### Task 018: Implement Config-Driven Canonical Alias Expander (`alias-expander@1`) (`packages/agent1_scout`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 002`, `Task 017`
- **Git Worktree & Branch:** `task/018-agent1-alias-expander` in `../tc-wt/task-018-agent1-alias-expander`
- **Owned Write Scope:** `packages/agent1_scout/src/alias_expander.py`, `packages/agent1_scout/tests/test_alias_expander.py`, `.agent-handoffs/task-018.md`
- **Mandatory Reference Files:** [scout-and-saturation.md](scout-and-saturation.md), [prompt-contracts.md](prompt-contracts.md)
- **Shared Contracts Consumed / Produced:** `CanonicalAliasExpander` using `providers.yaml` model routing

#### Scope And Implementation Requirements

- [ ] Generate 3–4 canonical search aliases (`[Suspect Full Name + Year]`, `[Victim Name + Crime]`, `[City + Case Nickname]`, `[Unique Forensic Detail]`) inside `<data>` envelope, deduplicating normalized queries.

#### Edge Cases And Failure Modes

- Ambiguous clickbait title lacking names: defer alias search until after `youtube-xray@2` extracts factual names.

#### Bug Prevention And Invariants

- **<= 4 Alias Query Fan-Out Invariant:** Caps daily `search.list` burn cleanly.

#### Independent Testability & Parallel Isolation

- Offline unit tests with mocked LLM responses.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent1_scout/tests/test_alias_expander.py` verifying 3–4 normalized aliases.
- **Acceptance:** Alias expander verified.

### Task 019: Implement Deduplicated Surgical `search.list` Runner & Spillover Collector (`packages/agent1_scout`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 007`, `Task 018`
- **Git Worktree & Branch:** `task/019-agent1-dedup-search-runner` in `../tc-wt/task-019-agent1-dedup-search-runner`
- **Owned Write Scope:** `packages/agent1_scout/src/search_runner.py`, `packages/agent1_scout/tests/test_search_runner.py`, `.agent-handoffs/task-019.md`
- **Mandatory Reference Files:** [scout-and-saturation.md](scout-and-saturation.md)
- **Shared Contracts Consumed / Produced:** `AliasDedupSearchRunner` deduplicating video IDs AND feeding spillover channel IDs to `WatchlistManager` (`Task 015`)

#### Scope And Implementation Requirements

- [ ] Execute `search.list` strictly on top 15–20 outliers (respecting the `15`-call daily re-check reserve), merge deduplicated `videoId` union, batch-fetch stats via `videos.list`, and pass unknown `2K–120K` channel IDs to weekly spillover discovery!

#### Edge Cases And Failure Modes

- Video appearing across all 4 alias queries: union set ensures each `videoId` is stored and scored exactly ONCE.

#### Bug Prevention And Invariants

- **Single-Count Union & Reserve Guard Invariant:** Zero duplicate video IDs and zero encroachment on Pre-Render search reserve.

#### Independent Testability & Parallel Isolation

- Tested offline with `fixtures/recorded_apis/yt_search_aliases.json`.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent1_scout/tests/test_search_runner.py` confirming deduplication and spillover collection.
- **Acceptance:** Deduplicated search runner verified.

### Task 020: Implement Mutually Exclusive Saturation Index (`SI`), 90-Day `>200K` Kill & Time Decay (`packages/agent1_scout`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 019`
- **Git Worktree & Branch:** `task/020-agent1-mutually-exclusive-si` in `../tc-wt/task-020-agent1-mutually-exclusive-si`
- **Owned Write Scope:** `packages/agent1_scout/src/saturation.py`, `packages/agent1_scout/tests/test_saturation.py`, `.agent-handoffs/task-020.md`
- **Mandatory Reference Files:** [scout-and-saturation.md](scout-and-saturation.md), [research/youtube-and-foia-mining.md](research/youtube-and-foia-mining.md)
- **Shared Contracts Consumed / Produced:** `SaturationCalculator` fixing bucket double-counting, recent 90d exhaustion, and old-mega decay

#### Scope And Implementation Requirements

- [ ] **90-Day Instant Kill:** Immediately set `has_90d_200k_kill = 1` (`REJECTED`) if ANY video on the case exceeded `200,000` views in the last `90 days` (even if `< 500K`!).
- [ ] **Mutually Exclusive Bucketing (Highest Priority Wins — Zero Double-Counting!):**
  1. `N_14d_excl` (`published <= 14d` ago, weight `8`)
  2. `N_mega_decayed` (remaining `> 500K` or Tier-1 giants in last 3 years: weight `1.0` if `<= 18 mo`, `0.5` if `18–36 mo`, scaled by `25`)
  3. `N_recent_excl` (remaining `> 50K` in last 18 months, weight `12`)
  ```text
  SI = min(100, round(25 * N_mega_decayed + 12 * N_recent_excl + 8 * N_14d_excl))
  ```
- [ ] Hard kill `SI >= 55`; Track A sweet spot `SI <= 35`.

#### Edge Cases And Failure Modes

- 5-day-old 600K upload: counted strictly ONCE in `N_14d_excl` AND immediately killed by the 90-day `>200K` rule (`has_90d_200k_kill = 1`)!
- 28-month-old 700K upload with zero recent competitors: decays to `0.5 * 25 = 13 <= 35`, rightly allowing a fresh FOIA/2K upgrade!

#### Bug Prevention And Invariants

- **Mutually Exclusive Partition Invariant:** `N_14d_excl + N_mega_count + N_recent_excl <= total_unique_videos`.

#### Independent Testability & Parallel Isolation

- Pure Python unit tests across 5-day 400K/600K, 28-month decayed mega, and Zombie Supply cases.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent1_scout/tests/test_saturation.py` verifying zero double-counting, 90d `>200K` kill, and 18–36mo decay.
- **Acceptance:** Fixed mutually-exclusive `SI` engine verified.

### Task 021: Implement Tier-1 True-Crime Giant Channel Registry (`packages/agent1_scout`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 020`
- **Git Worktree & Branch:** `task/021-agent1-tier1-giants` in `../tc-wt/task-021-agent1-tier1-giants`
- **Owned Write Scope:** `packages/agent1_scout/src/tier1_giants.py`, `packages/agent1_scout/tests/test_tier1_giants.py`, `.agent-handoffs/task-021.md`
- **Mandatory Reference Files:** [scout-and-saturation.md](scout-and-saturation.md)
- **Shared Contracts Consumed / Produced:** `Tier1GiantMatcher` classifying Tier-1 network/giant uploads into `N_mega_decayed` (mutually exclusive)

#### Scope And Implementation Requirements

- [ ] Maintain configurable YAML/DB list of Tier-1 giants (`EWU`, `JCS`, `That Chapter`, `48 Hours`, `Dateline`, `20/20`, `Law&Crime`) matched by canonical `channelId` or normalized title.

#### Edge Cases And Failure Modes

- Tier-1 giant uploaded yesterday (counted in `N_14d_excl`): apply Tier-1 giant instant-kill flag or classify without double-counting across buckets.

#### Bug Prevention And Invariants

- **Mutually Exclusive Giant Tagging Invariant:** Integrates cleanly into `Task 020`'s exclusive bucketing.

#### Independent Testability & Parallel Isolation

- Pure Python unit tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent1_scout/tests/test_tier1_giants.py` with 100% pass.
- **Acceptance:** Tier-1 giant matcher verified.

### Task 022: Implement Comment Gap Miner & Safe-Title CTR Feasibility Check (`packages/agent1_scout`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 007`, `Task 013`, `Task 020`
- **Git Worktree & Branch:** `task/022-agent1-comment-gap-safe-ctr` in `../tc-wt/task-022-agent1-comment-gap-safe-ctr`
- **Owned Write Scope:** `packages/agent1_scout/src/comment_miner.py`, `packages/agent1_scout/tests/test_comment_miner.py`, `.agent-handoffs/task-022.md`
- **Mandatory Reference Files:** [scout-and-saturation.md](scout-and-saturation.md), [prompt-contracts.md](prompt-contracts.md)
- **Shared Contracts Consumed / Produced:** `CommentQualityGapMiner` + **Safe-Title CTR Feasibility Checker** (`safe_title_ctr_ok`)

#### Scope And Implementation Requirements

- [ ] Pull top 100 comments (`commentThreads.list`), strip commenter PII, and cluster unanswered forensic questions (`comment-gap-miner@1`).
- [ ] Run **Safe-Title CTR Feasibility Check**: draft a policy-compliant (non-tabloid, AdSense-safe) documentary title for the case and score whether the mystery/twist hook remains compelling without sensationalist clickbait (`safe_title_ctr_ok`), calibrated against `episode_analytics` CTR history!

#### Edge Cases And Failure Modes

- Outlier video succeeded purely via graphic tabloid title (*"CHOPPED UP IN BASEMENT?!"*) on a weak underlying story: Safe-Title CTR Check flags `safe_title_ctr_ok = 0` and rejects!

#### Bug Prevention And Invariants

- **Policy-Safe Hook Viability Invariant:** Only cases that sustain strong curiosity under clean AdSense-compliant titles advance.

#### Independent Testability & Parallel Isolation

- Tested offline with tabloid-vs-forensic title fixtures.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent1_scout/tests/test_comment_miner.py` verifying comment clustering and tabloid-title rejection.
- **Acceptance:** Comment gap miner & Safe-Title CTR check verified.

### Task 023: Implement Gemini YouTube URL X-Ray With Age-Restricted Metadata/Transcript Fallback (`packages/agent1_scout`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 002`, `Task 020`
- **Git Worktree & Branch:** `task/023-agent1-gemini-xray-fallback` in `../tc-wt/task-023-agent1-gemini-xray-fallback`
- **Owned Write Scope:** `packages/agent1_scout/src/gemini_xray.py`, `packages/agent1_scout/tests/test_gemini_xray.py`, `.agent-handoffs/task-023.md`
- **Mandatory Reference Files:** [scout-and-saturation.md](scout-and-saturation.md), [prompt-contracts.md](prompt-contracts.md)
- **Shared Contracts Consumed / Produced:** `GeminiYouTubeXRayClient` (`youtube-xray@2`) with automatic **age-restricted/playback-blocked fallback**

#### Scope And Implementation Requirements

- [ ] Pass top 3–5 YouTube URLs to Gemini API (`providers.yaml` model ID) where playback is permitted to extract factual lead keys without downloading MP4s.
- [ ] **Age-Restricted Authorized Metadata Fallback (`F-11`):** If Gemini returns `PLAYBACK_RESTRICTED` / `AGE_GATED`, proceed strictly with authorized `videos.list` metadata (`title`, `description`, `tags`) + `commentThreads.list` public questions labeled `LEAD_ONLY` (NEVER attempt unauthorized third-party `captions.download` scraping—which requires video edit rights—and never treat comments/metadata as factual evidence!).

#### Edge Cases And Failure Modes

- Age-restricted video with empty description: fuse comment entity mentions + search snippets to populate `SeedPacket` for Agent 2 primary-record verification.

#### Bug Prevention And Invariants

- **Zero Third-Party MP4 Download & Zero Silent Age-Gate Failure Invariant:** Age-restricted URLs fall back cleanly to metadata/comments.

#### Independent Testability & Parallel Isolation

- Tested offline with mocked `PLAYBACK_RESTRICTED` Gemini error + fallback fixture.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent1_scout/tests/test_gemini_xray.py` confirming Agentic Video Mode and age-restricted fallback path.
- **Acceptance:** Resilient Gemini YouTube URL X-Ray verified.

### Task 024: Implement Clean-Room Seed Firewall & Immediate Transcript Purge (`packages/agent1_scout`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 023`
- **Git Worktree & Branch:** `task/024-clean-room-seed-firewall` in `../tc-wt/task-024-clean-room-seed-firewall`
- **Owned Write Scope:** `packages/agent1_scout/src/clean_room_firewall.py`, `packages/agent1_scout/tests/test_clean_room_firewall.py`, `.agent-handoffs/task-024.md`
- **Mandatory Reference Files:** [scout-and-saturation.md](scout-and-saturation.md), [prompt-contracts.md](prompt-contracts.md)
- **Shared Contracts Consumed / Produced:** `CleanRoomFirewall` outputting strictly factual `SeedPacket`

#### Scope And Implementation Requirements

- [ ] Enforce closed `SeedPacket` schema (no narrative outline, beat order, or creator commentary; max 200 chars/field) and deterministically wipe any fallback transcript buffer immediately after extraction.

#### Edge Cases And Failure Modes

- Smuggled story arc in `unanswered_comment_questions`: reject multi-sentence narrative prose deterministically.

#### Bug Prevention And Invariants

- **Zero Creator Script Contamination Invariant:** Zero creator transcript bytes survive Agent 1.

#### Independent Testability & Parallel Isolation

- Adversarial smuggling & disk residue unit tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent1_scout/tests/test_clean_room_firewall.py` with 100% pass.
- **Acceptance:** Clean-Room Seed Firewall verified.

### Task 025: Implement Binary Policy Kill-Switch Classifier (`packages/agent1_scout`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 024`
- **Git Worktree & Branch:** `task/025-policy-kill-switch` in `../tc-wt/task-025-policy-kill-switch`
- **Owned Write Scope:** `packages/agent1_scout/src/kill_switch.py`, `packages/agent1_scout/tests/test_kill_switch.py`, `.agent-handoffs/task-025.md`
- **Mandatory Reference Files:** [scout-and-saturation.md](scout-and-saturation.md), [legal-copyright-and-adsense.md](legal-copyright-and-adsense.md)
- **Shared Contracts Consumed / Produced:** `PolicyKillSwitchGate` hard-dropping minors, mass shootings, terrorism, child abuse, and unconvicted suspects

#### Scope And Implementation Requirements

- [ ] Hard-reject any candidate matching the 5 blocked categories (`REJECTED` + `policy_kill_reason`), passing adult convicted cases (including appellate reviews of standing convictions).

#### Edge Cases And Failure Modes

- Minor witness vs minor victim: hard-drop any case centering on minor distress/abuse/offense.

#### Bug Prevention And Invariants

- **Fail-Closed Policy Gate Invariant:** Ambiguous minor involvement drops immediately.

#### Independent Testability & Parallel Isolation

- Pure Python classification tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent1_scout/tests/test_kill_switch.py` with 100% catch rate on all 5 categories.
- **Acceptance:** Binary policy kill-switch verified.

### Task 026: Implement Track B MuckRock FOIA Completed-Drop Radar Poller (`packages/agent1_scout`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 002`, `Task 025`
- **Git Worktree & Branch:** `task/026-track-b-muckrock-radar` in `../tc-wt/task-026-track-b-muckrock-radar`
- **Owned Write Scope:** `packages/agent1_scout/src/muckrock_radar.py`, `packages/agent1_scout/tests/test_muckrock_radar.py`, `.agent-handoffs/task-026.md`
- **Mandatory Reference Files:** [scout-and-saturation.md](scout-and-saturation.md)
- **Shared Contracts Consumed / Produced:** Emits `TRACK_B_FOIA_RADAR` `SeedPacket`s from completed MuckRock FOIA drops

#### Scope And Implementation Requirements

- [ ] Poll completed MuckRock FOIA drops, filter out empty/denial-only drops, run `SI` + 90d `>200K` check, and pre-tag attachments requiring Agent 3 third-party CCTV inspection.

#### Edge Cases And Failure Modes

- MuckRock drop consists solely of fee-waiver correspondence: check `files[]` for substantive media/PDF sizes.

#### Bug Prevention And Invariants

- **Substantive Attachment Invariant:** Track B MuckRock seeds require verified non-denial attachments.

#### Independent Testability & Parallel Isolation

- Tested offline with `fixtures/recorded_apis/muckrock_completed.json`.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent1_scout/tests/test_muckrock_radar.py` passing all checks.
- **Acceptance:** Track B MuckRock radar verified.

### Task 027: Implement Track B CourtListener Appellate Ruling Radar Poller (`packages/agent1_scout`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 008`, `Task 025`
- **Git Worktree & Branch:** `task/027-track-b-courtlistener-radar` in `../tc-wt/task-027-track-b-courtlistener-radar`
- **Owned Write Scope:** `packages/agent1_scout/src/courtlistener_radar.py`, `packages/agent1_scout/tests/test_courtlistener_radar.py`, `.agent-handoffs/task-027.md`
- **Mandatory Reference Files:** [scout-and-saturation.md](scout-and-saturation.md), [evidence-and-fact-ledger.md](evidence-and-fact-ledger.md)
- **Shared Contracts Consumed / Produced:** Emits `TRACK_B_FOIA_RADAR` `SeedPacket`s strictly for `AFFIRMED` appellate criminal opinions (`>= 3,000` words)

#### Scope And Implementation Requirements

- [ ] Poll recent criminal appellate opinions within reserved `<= 50%` of the 125/day cap, **pre-filtering for `AFFIRMED` disposition** (skipping `REVERSED`/`REMANDED` early!), and populate `courtlistener_cache` for Agent 2 reuse.

#### Edge Cases And Failure Modes

- Opinion reverses on one minor count while affirming murder conviction: parse primary disposition tags carefully before rejecting or passing to Agent 2 Disposition Gate.

#### Bug Prevention And Invariants

- **Quota-Preserving & Disposition-Aware Invariant:** Reserves >= 50% of 125/day quota for Agent 2 verification.

#### Independent Testability & Parallel Isolation

- Tested offline with `fixtures/recorded_apis/courtlistener_opinions.json`.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent1_scout/tests/test_courtlistener_radar.py` with 100% pass.
- **Acceptance:** Track B CourtListener radar verified.

### Task 028: Implement 70/30 Dual-Track Slate Enforcer Calibrated By `episode_analytics` (`packages/agent1_scout`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 013`, `Task 020`, `Task 026`, `Task 027`
- **Git Worktree & Branch:** `task/028-dual-track-slate-balancer` in `../tc-wt/task-028-dual-track-slate-balancer`
- **Owned Write Scope:** `packages/agent1_scout/src/slate_balancer.py`, `packages/agent1_scout/tests/test_slate_balancer.py`, `.agent-handoffs/task-028.md`
- **Mandatory Reference Files:** [scout-and-saturation.md](scout-and-saturation.md)
- **Shared Contracts Consumed / Produced:** `MonthlySlateAllocator` maintaining 70/30 Track A/B baseline with analytics-informed priority and zero duplicate defendants

#### Scope And Implementation Requirements

- [ ] Enforce `7 TRACK_A_OUTLIER` : `3 TRACK_B_FOIA_RADAR` per 10-episode rolling window (adaptable via `episode_analytics` Track ROI metrics!), deduplicating `(defendant_normalized, incident_year)`.

#### Edge Cases And Failure Modes

- Same case discovered via both Track A and Track B: merge into one candidate retaining Track B's primary FOIA documents.

#### Bug Prevention And Invariants

- **Zero Duplicate Case Greenlight Invariant:** `(defendant_normalized, incident_year)` uniqueness enforced across episodes.

#### Independent Testability & Parallel Isolation

- Pure Python + SQLite slate simulation tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent1_scout/tests/test_slate_balancer.py` verifying 7/3 split and duplicate merging.
- **Acceptance:** 70/30 slate balancer verified.

### Task 029: Implement Mandatory 2-Upgrade Rule Evaluator (`packages/agent1_scout`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 022`, `Task 024`
- **Git Worktree & Branch:** `task/029-mandatory-two-upgrade-rule` in `../tc-wt/task-029-mandatory-two-upgrade-rule`
- **Owned Write Scope:** `packages/agent1_scout/src/upgrade_evaluator.py`, `packages/agent1_scout/tests/test_upgrade_evaluator.py`, `.agent-handoffs/task-029.md`
- **Mandatory Reference Files:** [scout-and-saturation.md](scout-and-saturation.md)
- **Shared Contracts Consumed / Produced:** `TwoUpgradeEvaluator` requiring `>= 2` of 4 upgrade axes on Track A cases

#### Scope And Implementation Requirements

- [ ] Verify Track A candidates beat the small creator on `>= 2` of 4 axes: missed appellate/FOIA facts, top-3 comment answers, 2K spatial crime-scene reconstruction, or cleaner Demucs/scrubbed FOIA audio.

#### Edge Cases And Failure Modes

- Candidate passes only 1 axis: hard-reject (`REJECTED_NO_10X_UPGRADE`).

#### Bug Prevention And Invariants

- **`>= 2` Axes Invariant:** Prevents low-differentiation copycats.

#### Independent Testability & Parallel Isolation

- Pure Python rule-table unit tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent1_scout/tests/test_upgrade_evaluator.py` with 100% pass.
- **Acceptance:** Mandatory 2-Upgrade Rule verified.

### Task 030: Implement Composite Evidence-Density Ranker (`0.30/0.25/0.25/0.20`) (`packages/agent1_scout`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 028`, `Task 029`
- **Git Worktree & Branch:** `task/030-evidence-density-ranker` in `../tc-wt/task-030-evidence-density-ranker`
- **Owned Write Scope:** `packages/agent1_scout/src/ranker.py`, `packages/agent1_scout/tests/test_ranker.py`, `.agent-handoffs/task-030.md`
- **Mandatory Reference Files:** [scout-and-saturation.md](scout-and-saturation.md)
- **Shared Contracts Consumed / Produced:** `EvidenceDensityRanker` ranking candidates meeting `safe_title_ctr_ok == 1`

#### Scope And Implementation Requirements

- [ ] Score `0.30*Docs + 0.25*FOIA + 0.25*Twist + 0.20*Gap`, rejecting `safe_title_ctr_ok == 0` candidates and writing `GREENLIT` into `outlier_candidates`.

#### Edge Cases And Failure Modes

- High doc word count on a weak tabloid-only title: `safe_title_ctr_ok` gate blocks selection.

#### Bug Prevention And Invariants

- **Exact Weight Parity (`1.00`) & Safe-Title Gate Invariant.**

#### Independent Testability & Parallel Isolation

- Deterministic unit tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent1_scout/tests/test_ranker.py` with 100% pass.
- **Acceptance:** Composite ranker verified.

### Task 031: Implement Per-Day Pre-Render Saturation Re-Check & Sunk-Cost Guard (`packages/agent1_scout`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 007`, `Task 019`, `Task 020`
- **Git Worktree & Branch:** `task/031-pre-render-sunk-cost-recheck` in `../tc-wt/task-031-pre-render-sunk-cost-recheck`
- **Owned Write Scope:** `packages/agent1_scout/src/pre_render_recheck.py`, `packages/agent1_scout/tests/test_pre_render_recheck.py`, `.agent-handoffs/task-031.md`
- **Mandatory Reference Files:** [scout-and-saturation.md](scout-and-saturation.md), [flow-hybrid-and-batch-desk.md](flow-hybrid-and-batch-desk.md)
- **Shared Contracts Consumed / Produced:** `PreRenderSaturationGate` executed before Headless Veo API spend AND before **each day's** optional Batch Desk shift

#### Scope And Implementation Requirements

- [ ] Run 3-call `search.list` re-check from the 15-call daily reserve prior to Flow generation (and prior to Day 2 / Day 3 shifts in optional multi-day Batch Desk mode!).
- [ ] Abort cleanly (`ABORTED_COPYCAT_WAVE`) if `N_14d_wave > 3` (or `has_90d_200k_kill == 1`), **EXCEPT** apply the **Sunk-Cost Threshold**: if `spent_credits_pct > 0.50` AND `N_14d_wave <= 5` (and no Tier-1 giant hit), set `sunk_cost_override = 1` and finish the episode instead of wasting >50% sunk Flow spend!

#### Edge Cases And Failure Modes

- Viral wave explodes on Day 2 when 20% spent -> aborts early saving 80% credits; 75% spent with 4 small copycats -> finishes via sunk-cost override!

#### Bug Prevention And Invariants

- **Multi-Day Protection & Sunk-Cost Guard Invariant:** Protects both pre-spend and multi-day batches rationally.

#### Independent Testability & Parallel Isolation

- Fake-history unit tests covering Day 1 abort, Day 2 early abort, and `>50%` sunk-cost completion.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent1_scout/tests/test_pre_render_sunk_cost_recheck.py` passing all 3 scenarios.
- **Acceptance:** Per-day Pre-Render Re-Check & Sunk-Cost Guard verified.

### Task 032: Agent 1 Recorded-Corpus Integration & Anti-Trap Suite (`packages/agent1_scout`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 015`–`031`
- **Git Worktree & Branch:** `task/032-agent1-integration-suite` in `../tc-wt/task-032-agent1-integration-suite`
- **Owned Write Scope:** `packages/agent1_scout/src/pipeline.py`, `packages/agent1_scout/tests/test_agent1_e2e.py`, `.agent-handoffs/task-032.md`
- **Mandatory Reference Files:** [scout-and-saturation.md](scout-and-saturation.md), [architecture-review-decisions.md](architecture-review-decisions.md)
- **Shared Contracts Consumed / Produced:** `Agent1ScoutService` certified against all search/mining/age-gate/ToS traps

#### Scope And Implementation Requirements

- [ ] Verify end-to-end scouting across `fixtures/recorded_apis/` proving: `0 search.list` nightly polls, mutually exclusive `SI` (no 5-day 600K triple-count), 90d `>200K` instant kill, age-restricted X-Ray fallback, Clean-Room transcript deletion, Safe-Title CTR check, 30-day TTL purge, and sunk-cost re-check.

#### Edge Cases And Failure Modes

- All Track A candidates fail `90d >200K` kill: fall back smoothly to Track B FOIA winners.

#### Bug Prevention And Invariants

- **Zero Trap Leakage Invariant:** 100% deterministic catch across all scouting edge cases.

#### Independent Testability & Parallel Isolation

- 100% offline recorded-API suite.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent1_scout` with 100% pass.
- **Acceptance:** Agent 1 v2 certified end-to-end.

---

### Task 033: Implement Primary-Record & Appellate Disposition Verification Gate (`packages/agent2_evidence`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 008`, `Task 024`
- **Git Worktree & Branch:** `task/033-agent2-disposition-gate` in `../tc-wt/task-033-agent2-disposition-gate`
- **Owned Write Scope:** `packages/agent2_evidence/src/primary_gate.py`, `packages/agent2_evidence/tests/test_primary_gate.py`, `.agent-handoffs/task-033.md`
- **Mandatory Reference Files:** [evidence-and-fact-ledger.md](evidence-and-fact-ledger.md), [schema/pipeline.sql](schema/pipeline.sql)
- **Shared Contracts Consumed / Produced:** `PrimaryRecordVerifier` enforcing `disposition_status IN ('AFFIRMED', 'STANDING_CONVICTION')`

#### Scope And Implementation Requirements

- [ ] Verify `(suspect_names, incident_year, docket_ids)` in CourtListener + State DOC + `.gov` releases AND extract exact judicial disposition (`AFFIRMED`, `STANDING_CONVICTION`, `REVERSED`, `VACATED`, `ACQUITTED`, `PENDING`).
- [ ] Hard-kill fake NoSleep cases AND **hard-kill any `REVERSED`, `VACATED`, `ACQUITTED`, or `PENDING` appellate ruling** (`trg_case_disposition_guard`), preventing catastrophic defamation!

#### Edge Cases And Failure Modes

- Opinion reverses conviction on Count 2 (procedural) while affirming Count 1 (homicide): confirm core charge conviction still stands in State DOC before allowing `STANDING_CONVICTION`; if entire conviction vacated/remanded for new trial, auto-kill!

#### Bug Prevention And Invariants

- **Standing-Conviction-Only Invariant:** Zero reversed, vacated, or pending defendants proceed to scripting.

#### Independent Testability & Parallel Isolation

- Tested offline with `fixtures/recorded_apis/` `REVERSED` vs `AFFIRMED` appellate rulings.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent2_evidence/tests/test_primary_gate.py` proving `REVERSED` and NoSleep cases auto-kill while `AFFIRMED` passes.
- **Acceptance:** Primary-Record & Disposition Gate verified.

### Task 034: Implement CourtListener Appellate Opinion & Docket Harvester (`packages/agent2_evidence`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 008`, `Task 033`
- **Git Worktree & Branch:** `task/034-agent2-courtlistener-harvester` in `../tc-wt/task-034-agent2-courtlistener-harvester`
- **Owned Write Scope:** `packages/agent2_evidence/src/courtlistener_harvester.py`, `packages/agent2_evidence/tests/test_courtlistener_harvester.py`, `.agent-handoffs/task-034.md`
- **Mandatory Reference Files:** [evidence-and-fact-ledger.md](evidence-and-fact-ledger.md)
- **Shared Contracts Consumed / Produced:** Clean normalized opinion texts with `p. X, para. Y` citation locators

#### Scope And Implementation Requirements

- [ ] Fetch full opinion text via cached `CourtListenerRateLimiter`, separate majority from concurring/dissenting sections, preserve page/paragraph anchors, and register in `primary_documents`.

#### Edge Cases And Failure Modes

- Dissenting opinion speculating on alternative facts: tag dissent text separately so `fact_ledger` never treats dissent arguments as established holdings.

#### Bug Prevention And Invariants

- **Majority-vs-Dissent Separation Invariant.**

#### Independent Testability & Parallel Isolation

- Offline HTML/JSON fixture tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent2_evidence/tests/test_courtlistener_harvester.py` with 100% pass.
- **Acceptance:** CourtListener harvester verified.

### Task 035: Implement MuckRock & State-Statute FOIA Package Downloader (`packages/agent2_evidence`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 033`
- **Git Worktree & Branch:** `task/035-agent2-foia-downloader` in `../tc-wt/task-035-agent2-foia-downloader`
- **Owned Write Scope:** `packages/agent2_evidence/src/foia_downloader.py`, `packages/agent2_evidence/tests/test_foia_downloader.py`, `.agent-handoffs/task-035.md`
- **Mandatory Reference Files:** [evidence-and-fact-ledger.md](evidence-and-fact-ledger.md), [legal-copyright-and-adsense.md](legal-copyright-and-adsense.md)
- **Shared Contracts Consumed / Produced:** Stages raw FOIA docs & media into `raw_foia/` tagged with jurisdiction metadata for Agent 3 granular audit

#### Scope And Implementation Requirements

- [ ] Download FOIA PDFs, 911 audio, and bodycam/dashcam MP4s, extracting PDF text (+ OCR fallback for scans) and recording state jurisdiction + attachment origin metadata in `foia_media_assets` for Agent 3's per-file CCTV/statute gate.

#### Edge Cases And Failure Modes

- FOIA ZIP contains `ring_doorbell_neighbor.mp4` alongside `officer_bodycam.mp4`: preserve exact attachment filename/origin metadata so `Task 045` quarantines the private Ring clip cleanly!

#### Bug Prevention And Invariants

- **Raw Media Quarantine Invariant:** Zero `raw_foia/` assets enter Part 2 without Agent 3 clearance.

#### Independent Testability & Parallel Isolation

- Tested against local mock HTTP FOIA ZIP server.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent2_evidence/tests/test_foia_downloader.py` with 100% pass.
- **Acceptance:** FOIA downloader verified.

### Task 036: Implement Secondary News Text-Only Extractor (Zero-Pixel Enforcement) (`packages/agent2_evidence`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 033`
- **Git Worktree & Branch:** `task/036-agent2-news-text-only` in `../tc-wt/task-036-agent2-news-text-only`
- **Owned Write Scope:** `packages/agent2_evidence/src/news_text_only.py`, `packages/agent2_evidence/tests/test_news_text_only.py`, `.agent-handoffs/task-036.md`
- **Mandatory Reference Files:** [legal-copyright-and-adsense.md](legal-copyright-and-adsense.md)
- **Shared Contracts Consumed / Produced:** Registers `doc_type = 'news_text_only'` with zero retained media bytes

#### Scope And Implementation Requirements

- [ ] Strip all `<img>`, `<video>`, `<picture>`, and base64 media payloads before extracting plain article text, locking `doc_type = 'news_text_only'`.

#### Edge Cases And Failure Modes

- Embedded base64 mugshot inside HTML article: stripped deterministically at DOM parser stage.

#### Bug Prevention And Invariants

- **Zero News Pixel Retention Invariant.**

#### Independent Testability & Parallel Isolation

- HTML sanitization unit tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent2_evidence/tests/test_news_text_only.py` verifying 0 media bytes retained.
- **Acceptance:** News text-only extractor verified.

### Task 037: Implement 1M-Context DeepSeek Ingestion Orchestrator (`packages/agent2_evidence`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 014`, `Task 034`–`036`
- **Git Worktree & Branch:** `task/037-agent2-1m-ingestion` in `../tc-wt/task-037-agent2-1m-ingestion`
- **Owned Write Scope:** `packages/agent2_evidence/src/ingestion_orchestrator.py`, `packages/agent2_evidence/tests/test_ingestion_orchestrator.py`, `.agent-handoffs/task-037.md`
- **Mandatory Reference Files:** [evidence-and-fact-ledger.md](evidence-and-fact-ledger.md), [prompt-contracts.md](prompt-contracts.md)
- **Shared Contracts Consumed / Produced:** Packs `<data source="...">` envelopes using `providers.yaml` model IDs

#### Scope And Implementation Requirements

- [ ] Pack documents in priority order (`court_ruling` -> `police_affidavit` -> `foia_package` -> `news_text_only`) under 850K-token batch ceiling with byte-0 static instruction prefix.

#### Edge Cases And Failure Modes

- Mega-dockets `> 850K` tokens: deterministic boundary-preserving batch splitter with entity carryover.

#### Bug Prevention And Invariants

- **Untrusted `<data>` Isolation Invariant.**

#### Independent Testability & Parallel Isolation

- Large-docket unit tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent2_evidence/tests/test_ingestion_orchestrator.py` with 100% pass.
- **Acceptance:** 1M-context ingestion orchestrator verified.

### Task 038: Implement Temporal Fact Ledger Extractor & Living Third-Party Anonymizer (`packages/agent2_evidence`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 002`, `Task 037`
- **Git Worktree & Branch:** `task/038-agent2-ledger-anonymizer` in `../tc-wt/task-038-agent2-ledger-anonymizer`
- **Owned Write Scope:** `packages/agent2_evidence/src/fact_extractor.py`, `packages/agent2_evidence/tests/test_fact_extractor.py`, `.agent-handoffs/task-038.md`
- **Mandatory Reference Files:** [evidence-and-fact-ledger.md](evidence-and-fact-ledger.md), [prompt-contracts.md](prompt-contracts.md)
- **Shared Contracts Consumed / Produced:** `TemporalFactLedger` with `source_type` locked to cited document AND automatic **anonymization of unconvicted living third parties**

#### Scope And Implementation Requirements

- [ ] Extract `TemporalFactLedger` via `evidence-ledger-extractor@3` (tool-less, zero DB-write privileges, delimiter-sanitized random nonce wrapper `<untrusted_source_...>` rejecting injected instructions inside `<data>` breakouts — Additional Security Check #2), overriding `source_type` from the cited `primary_documents` row.
- [ ] **Living Third-Party Anonymizer (`F-04`):** Automatically detect and replace names of unconvicted witnesses, neighbors, coworkers, and family members with neutral role aliases (`"Witness A"`, `"a coworker"`, `"Neighbor B"`), advancing `cases.anonymization_status` from `NOT_STARTED` -> `IN_REVIEW` (recording `anonymization_artifact_sha256`; NEVER default-approving to `APPROVED` without verified review metadata!).

#### Edge Cases And Failure Modes

- Appellate filing or third-party report contains fake `"IGNORE PREVIOUS INSTRUCTIONS"` / `"</data>"` prompt-injection payload: tool-less schema extractor ignores directives cleanly and passes offline adversarial injection tests!

#### Bug Prevention And Invariants

- **Zero Unconvicted Private Individual Naming Invariant:** Protects against defamation & GDPR/privacy claims.

#### Independent Testability & Parallel Isolation

- Tested with mock filings naming cleared alternate suspects and witnesses.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent2_evidence/tests/test_fact_extractor.py` proving source-tier enforcement and 100% third-party anonymization.
- **Acceptance:** Fact ledger extractor & third-party anonymizer verified.

### Task 039: Implement `DeepSeek-V4-Pro-0813` Conflict & Alibi Reconciler (`packages/agent2_evidence`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 038`
- **Git Worktree & Branch:** `task/039-agent2-v4-pro-reconciler` in `../tc-wt/task-039-agent2-v4-pro-reconciler`
- **Owned Write Scope:** `packages/agent2_evidence/src/conflict_reconciler.py`, `packages/agent2_evidence/tests/test_conflict_reconciler.py`, `.agent-handoffs/task-039.md`
- **Mandatory Reference Files:** [evidence-and-fact-ledger.md](evidence-and-fact-ledger.md)
- **Shared Contracts Consumed / Produced:** Resolves multi-document timeline contradictions using `providers.yaml` reasoning model

#### Scope And Implementation Requirements

- [ ] Route overlapping/conflicting facts to `DeepSeek-V4-Pro-0813`, enforcing `court_ruling > police_affidavit > news_report` precedence and linking discredited suspect alibis cleanly.

#### Edge Cases And Failure Modes

- Unresolved trial discrepancy: preserve both facts marked disputed rather than guessing.

#### Bug Prevention And Invariants

- **Judicial Hierarchy Invariant.**

#### Independent Testability & Parallel Isolation

- Conflicting alibi unit tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent2_evidence/tests/test_conflict_reconciler.py` with 100% pass.
- **Acceptance:** `V4-Pro-0813` reconciler verified.

### Task 040: Implement Source-Tier Hedging Tagger (`court_ruling` vs `police_affidavit` vs `news_report`) (`packages/agent2_evidence`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 038`, `Task 039`
- **Git Worktree & Branch:** `task/040-agent2-hedging-tagger` in `../tc-wt/task-040-agent2-hedging-tagger`
- **Owned Write Scope:** `packages/agent2_evidence/src/hedging_tagger.py`, `packages/agent2_evidence/tests/test_hedging_tagger.py`, `.agent-handoffs/task-040.md`
- **Mandatory Reference Files:** [evidence-and-fact-ledger.md](evidence-and-fact-ledger.md), [schema/pipeline.sql](schema/pipeline.sql)
- **Shared Contracts Consumed / Produced:** Locks `hedging_required = 1` on every `news_report` fact

#### Scope And Implementation Requirements

- [ ] Split composite facts mixing verified rulings with news rumors, set `hedging_required = 1` for `news_report`, and attach attribution prefixes verified by SQLite triggers.

#### Edge Cases And Failure Modes

- Attempted `UPDATE` downgrading `hedging_required = 0`: caught by `trg_fact_news_hedging_update`.

#### Bug Prevention And Invariants

- **Zero Unhedged Secondary Claim Invariant.**

#### Independent Testability & Parallel Isolation

- SQLite trigger & unit tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent2_evidence/tests/test_hedging_tagger.py` with 100% pass.
- **Acceptance:** Hedging tagger verified.

### Task 041: Implement `TurningPointBeat` Extractor (`>= 3` Analytical Editorial Beats) (`packages/agent2_evidence`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 039`, `Task 040`
- **Git Worktree & Branch:** `task/041-agent2-turning-points` in `../tc-wt/task-041-agent2-turning-points`
- **Owned Write Scope:** `packages/agent2_evidence/src/turning_points.py`, `packages/agent2_evidence/tests/test_turning_points.py`, `.agent-handoffs/task-041.md`
- **Mandatory Reference Files:** [evidence-and-fact-ledger.md](evidence-and-fact-ledger.md), [director-and-13-laws.md](director-and-13-laws.md)
- **Shared Contracts Consumed / Produced:** `TurningPointBeat[]` (`>= 3` analytical insight beats per episode)

#### Scope And Implementation Requirements

- [ ] Extract `>= 3` evidence-backed turning points (discredited alibis, forensic matches, appellate holdings) with objective editorial analysis (zero legal advice), rejecting thin `< 3`-twist cases early.

#### Edge Cases And Failure Modes

- Case has only 1 chronological twist: fail fast (`REJECTED_LOW_TWIST_DENSITY`).

#### Bug Prevention And Invariants

- **`>= 3` Turning Points Invariant.**

#### Independent Testability & Parallel Isolation

- Unit tested against full vs thin fact ledgers.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent2_evidence/tests/test_turning_points.py` with 100% pass.
- **Acceptance:** Turning-point extractor verified.

### Task 042: Implement Early Image API 2K Crime-Scene Generator & Margin `10x10` `span_cells` Anchor Lock (`packages/agent2_evidence`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 002`, `Task 038`
- **Git Worktree & Branch:** `task/042-agent2-early-2k-anchor-lock` in `../tc-wt/task-042-agent2-early-2k-anchor-lock`
- **Owned Write Scope:** `packages/agent2_evidence/src/early_2k_anchors.py`, `packages/agent2_evidence/tests/test_early_2k_anchors.py`, `.agent-handoffs/task-042.md`
- **Mandatory Reference Files:** [evidence-and-fact-ledger.md](evidence-and-fact-ledger.md), [crime-scene-2k-grid-engine.md](crime-scene-2k-grid-engine.md), [parallel-part1-part2-architecture.md](parallel-part1-part2-architecture.md)
- **Shared Contracts Consumed / Produced:** **Solves Law 4 Circular Deadlock!** Calls Official Image API (`providers.yaml`), stamps external-margin `10x10` grid, runs `grid-grounding-vision@2`, and locks `spatial_anchors` (`span_cols`, `span_rows`, `x_px`, `y_px`, `target_zoom`) BEFORE Agent 3 scripting

#### Scope And Implementation Requirements

- [ ] Cluster `physical_clues[]` into `<= 8` clues per 2K pass and invoke the Official Gemini Image API (`>= 2560x1440` clean plate) using `CaseBible` monochrome charcoal style, inserting a `still_assets` row explicitly marked **`is_illustrative_reconstruction = 1`** with mandatory disclaimer **`ILLUSTRATIVE RECONSTRUCTION — NOT CRIME SCENE PHOTO`** (`F-05`).
- [ ] Add **non-occluding `64 px` external margin border** (`A–J` top, `1–10` left) on a temporary inspection PNG copy, call `grid-grounding-vision@2` returning `{grid_cell, sub_quadrant, span_cols, span_rows}`, and map exact `(x_px, y_px)` and `target_zoom` (`1.6x–3.8x`).
- [ ] Write `spatial_anchors` rows referencing `still_assets(still_2k_id)` and `fact_ledger(fact_id)` starting in **`lock_status = 'DRAFT'`** (`F-04`, `F-09`), transitioning explicitly `DRAFT -> IN_REVIEW -> LOCKED` (with `locked_by`, `locked_at`, `still_asset_sha256`) after validation/review before advancing to `EVIDENCE_AND_2K_LOCKED`!

#### Edge Cases And Failure Modes

- Clue spans 2 cells horizontally (`span_cols = 2.0`): `target_zoom` scales down cleanly to `1.6x–1.8x` so the full object stays visible inside the viewport instead of over-zooming to `3.8x`!

#### Bug Prevention And Invariants

- **Zero Part 2 Dependency & Early Law 4 Lock Invariant:** Part 1 locks verified 2K coordinates before scripting begins without calling Part 2 code.

#### Independent Testability & Parallel Isolation

- Tested offline with mocked Image API 2K PNG + mocked `grid-grounding-vision@2` JSON.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent2_evidence/tests/test_early_2k_anchors.py` verifying margin grid labeling, `span_cells` zoom calculation, untouched clean 2K SHA-256, and `spatial_anchors` DB lock.
- **Acceptance:** Law 4 circular dependency eliminated; early 2K anchor lock verified.

### Task 043: Implement Temporal Chronology Consistency & Citation Verifier (`packages/agent2_evidence`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 038`–`042`
- **Git Worktree & Branch:** `task/043-agent2-chronology-verifier` in `../tc-wt/task-043-agent2-chronology-verifier`
- **Owned Write Scope:** `packages/agent2_evidence/src/chronology_verifier.py`, `packages/agent2_evidence/tests/test_chronology_verifier.py`, `.agent-handoffs/task-043.md`
- **Mandatory Reference Files:** [evidence-and-fact-ledger.md](evidence-and-fact-ledger.md)
- **Shared Contracts Consumed / Produced:** Validates ISO-8601 timezone offsets and citation locators

#### Scope And Implementation Requirements

- [ ] Normalize DST-aware ISO timestamps, flag physically impossible travel intervals, and confirm every `citation_locator` resolves inside `primary_documents.local_text_path`.

#### Edge Cases And Failure Modes

- DST fall-back 1:30 AM overlap: require explicit UTC offset (`-05:00` vs `-04:00`).

#### Bug Prevention And Invariants

- **100% Resolvable Citation Invariant.**

#### Independent Testability & Parallel Isolation

- DST & broken-citation unit tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent2_evidence/tests/test_chronology_verifier.py` with 100% pass.
- **Acceptance:** Chronology & citation verifier verified.

### Task 044: Agent 2 Disposition, Anonymization & Early 2K Lock Integration Suite (`packages/agent2_evidence`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 033`–`043`
- **Git Worktree & Branch:** `task/044-agent2-integration-suite` in `../tc-wt/task-044-agent2-integration-suite`
- **Owned Write Scope:** `packages/agent2_evidence/src/pipeline.py`, `packages/agent2_evidence/tests/test_agent2_e2e.py`, `.agent-handoffs/task-044.md`
- **Mandatory Reference Files:** [evidence-and-fact-ledger.md](evidence-and-fact-ledger.md)
- **Shared Contracts Consumed / Produced:** `Agent2EvidenceService` transitioning cases cleanly to `EVIDENCE_AND_2K_LOCKED`

#### Scope And Implementation Requirements

- [ ] Run end-to-end replay: Disposition Gate (`REVERSED` killed, `AFFIRMED` passes) -> FOIA/CourtListener/News text-only -> 1M ledger + living 3rd-party anonymization -> V4-Pro reconciliation -> Hedging -> `>=3` Turning Points -> **Early Image API 2K + margin `10x10` `span_cells` anchor lock**.

#### Edge Cases And Failure Modes

- CourtListener 125/day ceiling hit mid-harvest: park cleanly without losing cached docs.

#### Bug Prevention And Invariants

- **Verified Standing Conviction & Pre-Script Spatial Lock Invariant.**

#### Independent Testability & Parallel Isolation

- 100% offline suite inside `packages/agent2_evidence`.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent2_evidence` with 100% pass.
- **Acceptance:** Agent 2 certified end-to-end.

---

### Task 045: Implement Granular Provenance Enforcer (State FOIA Statutes, MuckRock 3P Filter & Wikimedia API) (`packages/agent3_gatekeeper`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 002`, `Task 044`
- **Git Worktree & Branch:** `task/045-agent3-granular-provenance` in `../tc-wt/task-045-agent3-granular-provenance`
- **Owned Write Scope:** `packages/agent3_gatekeeper/src/provenance_whitelist.py`, `packages/agent3_gatekeeper/tests/test_provenance_whitelist.py`, `.agent-handoffs/task-045.md`
- **Mandatory Reference Files:** [legal-copyright-and-adsense.md](legal-copyright-and-adsense.md), [research/youtube-2026-policy-and-adsense.md](research/youtube-2026-policy-and-adsense.md)
- **Shared Contracts Consumed / Produced:** `GranularProvenanceEnforcer` replacing naive domain whitelists

#### Scope And Implementation Requirements

- [ ] **Component-Level Federal & Public-Records Rights (`F-14` — FOIA Access != Reuse Permission):** Narrow `US_FED_EMPLOYEE_17USC105` strictly to works prepared by U.S. federal government employees within official duties (17 U.S.C. § 105). Record `creator_entity`, `rights_holder`, `license_basis`, `permitted_uses_json`, `contains_third_party_attach`, and explicit `rights_review_status` (`NOT_STARTED -> IN_REVIEW -> APPROVED | REJECTED`) per file and embedded component!
- [ ] **State FOIA Statute Allowlist:** Explicit state-by-state clearance config (`FL_SUNSHINE`, `WA_PRA`, `OH_PRA`, etc.) honoring state restrictions on 911 death/private-residence audio rather than blindly clearing all state `.gov` URLs.
- [ ] **MuckRock & FOIA Third-Party Attachment Quarantine:** Inspect FOIA attachment metadata & frames to tag contractor-produced media, private Ring doorbell CCTV, store security cameras, and scanned newspaper PDFs as `RESTRICTED_NO_REUSE` (`contains_third_party_attach = 1`), blocked by SQLite `CHECK` from ever entering `APPROVED` status!
- [ ] **Wikimedia Commons API Check:** Query `extmetadata.LicenseShortName` per asset, admitting strictly `CC0` / `Public Domain` and rejecting `CC BY-NC` / `CC BY-SA`!
- [ ] Block news domains and third-party YouTube URLs unconditionally.

#### Edge Cases And Failure Modes

- MuckRock ZIP contains `walmart_lobby_cam.mp4` or `local_gazette_scan.pdf`: flagged and excluded before media processing!
- Wikimedia file tagged `CC BY-NC-ND 4.0`: rejected immediately (`PROVENANCE_LICENSE_RESTRICTED`).

#### Bug Prevention And Invariants

- **Per-Asset Statute & License Proof Invariant:** Zero copyrighted Ring/store CCTV or `CC BY-NC` files clear Agent 3.

#### Independent Testability & Parallel Isolation

- Tested offline with mocked Wikimedia `extmetadata` JSON, MuckRock Ring-CCTV fixture, and state-statute matrix.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent3_gatekeeper/tests/test_provenance_whitelist.py` verifying all 4 granular provenance checks.
- **Acceptance:** Granular provenance enforcer verified.

### Task 046: Implement Non-Whitelisted Pixel Purge, Ingest CFR/48kHz Normalization & 3P Blocker (`packages/agent3_gatekeeper`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 045`
- **Git Worktree & Branch:** `task/046-agent3-ingest-norm-pixel-purge` in `../tc-wt/task-046-agent3-ingest-norm-pixel-purge`
- **Owned Write Scope:** `packages/agent3_gatekeeper/src/ingest_normalizer.py`, `packages/agent3_gatekeeper/tests/test_ingest_normalizer.py`, `.agent-handoffs/task-046.md`
- **Mandatory Reference Files:** [legal-copyright-and-adsense.md](legal-copyright-and-adsense.md), [mastering-loudness-and-qa.md](mastering-loudness-and-qa.md)
- **Shared Contracts Consumed / Produced:** Purges un-cleared pixels AND normalizes all cleared FOIA media at ingest to **`CFR 30 fps`, `48 kHz stereo PCM`, `yuv420p`** (`normalized_cfr_30fps_48k = 1`)

#### Scope And Implementation Requirements

- [ ] Audit staging folders and unlink any non-cleared image/video bytes (`news`, `CC BY-NC`, `Ring CCTV`).
- [ ] Transcode/normalize every cleared FOIA MP4/WAV into canonical ingest format (**`30 fps CFR`**, `yuv420p`, **`48 kHz` stereo 24-bit PCM**) so variable-frame-rate (`23.976` / `29.97` / VFR) bodycams and `8 kHz` 911 calls never cause downstream FFmpeg drift or mixer errors!

#### Edge Cases And Failure Modes

- 8 kHz mono 911 WAV upsampled naively causing aliasing: use FFmpeg `aresample=48000:resampler=soxr` clean stereo dual-mono expansion.

#### Bug Prevention And Invariants

- **Strict Ingest Parity (`30 fps CFR`, `48 kHz PCM`) Invariant:** All downstream agents receive uniform frame rates and sample rates.

#### Independent Testability & Parallel Isolation

- Tested on VFR MP4 and 8 kHz mono WAV fixtures verified via `FFprobe`.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent3_gatekeeper/tests/test_ingest_normalizer.py` verifying contraband purge and `30 fps CFR / 48 kHz` output streams.
- **Acceptance:** Pixel purge & ingest normalizer verified.

### Task 047: Implement Music-Gated Demucs + Honest ASR Disagreement & Labeled-Corpus WER Gate (`packages/agent3_gatekeeper`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 004`, `Task 046`
- **Git Worktree & Branch:** `task/047-agent3-music-gated-demucs` in `../tc-wt/task-047-agent3-music-gated-demucs`
- **Owned Write Scope:** `packages/agent3_gatekeeper/src/demucs_stripper.py`, `packages/agent3_gatekeeper/tests/test_demucs_stripper.py`, `.agent-handoffs/task-047.md`
- **Mandatory Reference Files:** [legal-copyright-and-adsense.md](legal-copyright-and-adsense.md), [research/audio-mastering-and-conveyor-ops.md](research/audio-mastering-and-conveyor-ops.md)
- **Shared Contracts Consumed / Produced:** `MusicGatedDemucsIsolator` running `htdemucs` **strictly on music-detected intervals**, tracking honest **`asr_hypothesis_disagreement`** in production and true **`labeled_corpus_wer`** on a manually verified offline test corpus (`F-15`)

#### Scope And Implementation Requirements

- [ ] Run lightweight music-detection pass (`YAMNet` / `PANNs` / spectral harmonic classifier) across normalized `48 kHz` FOIA tracks.
- [ ] **Bypass Demucs completely** (`music_detected = 0`, `demucs_applied = 0`) on pure speech / distorted 8 kHz 911 dispatch calls so `htdemucs` never introduces underwater artifacts or swallows frantic caller speech!
- [ ] **Honest Intelligibility Metrics (`F-15`):** When background music triggers Demucs (`music_detected = 1`), compute **`asr_hypothesis_disagreement`** (token edit distance between pre-Demucs and post-Demucs ASR outputs—explicitly NOT called WER because two ASR runs can share identical errors!). Whenever `asr_hypothesis_disagreement > 0.10` or recognizer confidence drops, set `human_audio_review_required = 1` for mandatory human listening (and revert to spectral notch filtering if severely degraded).
- [ ] Maintain an offline manually verified reference transcript corpus (`tests/audio_corpus/`) measuring true **`labeled_corpus_wer`** against human ground truth during CI regression.

#### Edge Cases And Failure Modes

- Distorted 8 kHz 911 scream misclassified as `other` stem by Demucs: music-detector skips 911 speech cleanly; if triggered, elevated `asr_hypothesis_disagreement` or low confidence flags `human_audio_review_required = 1`.

#### Bug Prevention And Invariants

- **Honest Intelligibility & Human-Review Escalation Invariant:** Never mislabel ASR hypothesis disagreement as ground-truth WER; escalate uncertain music-stripped speech to human review.

#### Independent Testability & Parallel Isolation

- Tested with `911_8khz_distorted.wav` (Demucs bypassed!) and manually transcribed `bodycam_440hz_music.mp4` (true `labeled_corpus_wer` + `asr_hypothesis_disagreement` verified).

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent3_gatekeeper/tests/test_demucs_stripper.py` verifying 911 bypass, bodycam music removal, `asr_hypothesis_disagreement` human-review flagging, and offline reference-corpus WER.
- **Acceptance:** Music-gated Demucs with honest intelligibility metrics verified.

### Task 048: Implement Whole-Clip Profanity Map & `0:00–0:30` Slice Auto-Bleeper (`packages/agent3_gatekeeper`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 047`
- **Git Worktree & Branch:** `task/048-agent3-whole-clip-profanity` in `../tc-wt/task-048-agent3-whole-clip-profanity`
- **Owned Write Scope:** `packages/agent3_gatekeeper/src/profanity_bleeper.py`, `packages/agent3_gatekeeper/tests/test_profanity_bleeper.py`, `.agent-handoffs/task-048.md`
- **Mandatory Reference Files:** [legal-copyright-and-adsense.md](legal-copyright-and-adsense.md)
- **Shared Contracts Consumed / Produced:** Indexes `profanity_intervals_json` across the **entire** raw FOIA clip and auto-bleeps any slice routed to `0:00–0:30`

#### Scope And Implementation Requirements

- [ ] Run word-timestamped ASR profanity scan across `100%` of every FOIA audio/video asset (not just the first 15s of the source file!) and store `profanity_intervals_json` (`[{start_ms, end_ms, severity}]`) in `foia_media_assets`.
- [ ] Apply `1000 Hz` bleep + mute on all severe slurs everywhere AND **strictly on ANY trimmed slice (`0:42–0:54`) placed into episode `0:00–0:30`**!

#### Edge Cases And Failure Modes

- Agent 4 trims `0:40–0:52` from a 10-minute bodycam into the `0:00` cold open containing an expletive at `0:42`: whole-clip profanity map triggers bleep automatically!

#### Bug Prevention And Invariants

- **Episode-Relative `0:00–0:30` Zero-Profanity Invariant:** Slicing deep-clip timestamps into the intro can never leak profanity.

#### Independent Testability & Parallel Isolation

- Tested with `bodycam_440hz_music_042profanity.mp4` sliced at `0:40–0:52`.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent3_gatekeeper/tests/test_profanity_bleeper.py` verifying `0:42` profanity is indexed and bleeped when sliced into cold open.
- **Acceptance:** Whole-clip profanity mapper verified.

### Task 049: Implement Corner Watermark Detector (`packages/agent3_gatekeeper`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 046`
- **Git Worktree & Branch:** `task/049-agent3-watermark-detector` in `../tc-wt/task-049-agent3-watermark-detector`
- **Owned Write Scope:** `packages/agent3_gatekeeper/src/watermark_detector.py`, `packages/agent3_gatekeeper/tests/test_watermark_detector.py`, `.agent-handoffs/task-049.md`
- **Mandatory Reference Files:** [legal-copyright-and-adsense.md](legal-copyright-and-adsense.md)
- **Shared Contracts Consumed / Produced:** `CornerWatermarkScanner` rejecting broadcaster/YouTube logos while allowing official agency `AXON BODY` OSD

#### Scope And Implementation Requirements

- [ ] Scan 15% corner Safe-Zones via temporal persistence + Vision confirmation, rejecting TV/CourtTV/YouTube watermarks cleanly.

#### Edge Cases And Failure Modes

- Official Axon/WatchGuard bodycam timestamp HUD vs broadcaster logo: Vision verifier distinguishes agency OSD (`PASS`) from third-party channel logos (`REJECT`).

#### Bug Prevention And Invariants

- **Zero Broadcaster Watermark Invariant.**

#### Independent Testability & Parallel Isolation

- Synthetic Axon OSD vs Fox-style corner logo unit tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent3_gatekeeper/tests/test_watermark_detector.py` with 100% pass.
- **Acceptance:** Corner watermark detector verified.

### Task 050: Implement Visual + Spoken Audio PII Detector (OpenCV/YOLO + ASR NER) (`packages/agent3_gatekeeper`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 048`, `Task 049`
- **Git Worktree & Branch:** `task/050-agent3-visual-and-spoken-pii` in `../tc-wt/task-050-agent3-visual-and-spoken-pii`
- **Owned Write Scope:** `packages/agent3_gatekeeper/src/pii_detector.py`, `packages/agent3_gatekeeper/tests/test_pii_detector.py`, `.agent-handoffs/task-050.md`
- **Mandatory Reference Files:** [legal-copyright-and-adsense.md](legal-copyright-and-adsense.md), [research/youtube-2026-policy-and-adsense.md](research/youtube-2026-policy-and-adsense.md)
- **Shared Contracts Consumed / Produced:** Detects **BOTH visual PII** (faces, plates, house numbers) **AND spoken audio PII** (caller full names, street addresses, phone numbers, DOBs, juvenile names in 911/bodycam ASR)

#### Scope And Implementation Requirements

- [ ] Run OpenCV/YOLO visual detection with IOU temporal track smoothing for bystander faces, plates, and residential house numbers.
- [ ] **Spoken PII ASR NER Scanner:** Scan FOIA ASR word timestamps using regex + NER (`PHONE`, `STREET_ADDRESS`, `DOB`, `PERSON` matching non-defendant bystanders/callers/juveniles) and emit exact `[start_ms, end_ms]` spoken-PII mute intervals!

#### Edge Cases And Failure Modes

- 911 dispatcher reads caller's callback number (`"555-0194"`) and home address (`"412 Oak Street"`) digit by digit across 4 seconds: span-merged regex + NER covers the entire spoken address/phone window!

#### Bug Prevention And Invariants

- **Dual Visual + Spoken PII Coverage Invariant:** Zero unredacted home addresses, phone numbers, or bystander names leak in FOIA audio or video.

#### Independent Testability & Parallel Isolation

- Tested on `fixtures/synthetic_media/911_spoken_pii.wav` and synthetic face/plate frames.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent3_gatekeeper/tests/test_pii_detector.py` detecting 100% of synthetic visual and spoken phone/address/bystander spans.
- **Acceptance:** Visual + Spoken PII detector verified.

### Task 051: Implement Deterministic Visual Blur & Spoken PII Audio Muter (`packages/agent3_gatekeeper`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 050`
- **Git Worktree & Branch:** `task/051-agent3-pii-scrubber-renderer` in `../tc-wt/task-051-agent3-pii-scrubber-renderer`
- **Owned Write Scope:** `packages/agent3_gatekeeper/src/pii_blur_renderer.py`, `packages/agent3_gatekeeper/tests/test_pii_blur_renderer.py`, `.agent-handoffs/task-051.md`
- **Mandatory Reference Files:** [legal-copyright-and-adsense.md](legal-copyright-and-adsense.md)
- **Shared Contracts Consumed / Produced:** Renders visual Gaussian blur (`sigma >= 25`) AND spoken PII tone/mute into `scrubbed_foia/` (`visual_pii_blurred=1`, `spoken_pii_bleeped=1`)

#### Scope And Implementation Requirements

- [ ] Apply `sigma >= 25` Gaussian blur over all visual PII tracks AND overwrite spoken PII `[start_ms, end_ms]` windows with soft `-24 dBFS` tone/room-tone mute, running a post-scrub re-scan confirming zero residual crisp faces or unmuted spoken PII!

#### Edge Cases And Failure Modes

- Audio-only 911 WAV file needing spoken PII scrubbing without video track: handle audio-only WAV path cleanly alongside MP4 video+audio files.

#### Bug Prevention And Invariants

- **Verified Zero-PII Output Invariant:** Post-scrub audit confirms both visual and spoken PII are irreversibly masked.

#### Independent Testability & Parallel Isolation

- Unit + verification tests on synthetic MP4 and 911 WAV fixtures.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent3_gatekeeper/tests/test_pii_blur_renderer.py` with 100% pass.
- **Acceptance:** Visual & spoken PII scrubber renderer verified.

### Task 052: Implement Fact-Grounded, Topology-Safe Documentary Script Generator (`packages/agent3_gatekeeper`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 044`
- **Git Worktree & Branch:** `task/052-agent3-grounded-script-gen` in `../tc-wt/task-052-agent3-grounded-script-gen`
- **Owned Write Scope:** `packages/agent3_gatekeeper/src/script_generator.py`, `packages/agent3_gatekeeper/tests/test_script_generator.py`, `.agent-handoffs/task-052.md`
- **Mandatory Reference Files:** [evidence-and-fact-ledger.md](evidence-and-fact-ledger.md), [director-and-13-laws.md](director-and-13-laws.md)
- **Shared Contracts Consumed / Produced:** Generates ~2,400–2,800 word narration script (leaving ~4m for FOIA slots = 20m total!) anchored to `spatial_anchors` and topology-safe phrasing

#### Scope And Implementation Requirements

- [ ] Consume `TemporalFactLedger`, `TurningPointBeat[]`, concise `craft_rubric.yaml` (`<= 150 lines`, clarifying `"interactive"` as engaging visual documentary pacing), and **explicitly `LOCKED` `spatial_anchors`** (`EVIDENCE_AND_2K_LOCKED`).
- [ ] **Versioned Per-Scene `ScenePlan` Stage 1 Compiler (`Plan First`, `F-05`, `F-06`):** Persist one typed `scene_plans` row per scene binding `story_purpose`, `intended_audience_effect`, `approved_narration_text` + `narration_version_sha256`, `cited_fact_ids_json`, `visual_concept`, `prompt_mode`, `visual_prompt`, `keyframe_refs_json`, `expected_output_summary`, `timing`, `transition_spec_json`, `sound_cues_json`, `edit_instructions`, and `acceptance_criteria_json`, transitioning cleanly to `SCENE_PLAN_APPROVED` BEFORE voice synthesis or visual creation!
- [ ] Enforce non-misleading, record-anchored phrasing referenced to verified `fact_ledger` IDs.

#### Edge Cases And Failure Modes

- Narration word count ignoring 3.5 minutes of raw FOIA playback (producing a 24-minute video): compute `target_narration_words = (1200 - foia_total_sec) / 60 * 145`!

#### Bug Prevention And Invariants

- **FOIA-Aware Word Budget & Pre-Locked Anchor Invariant.**

#### Independent Testability & Parallel Isolation

- Offline unit tests with mocked script outputs.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent3_gatekeeper/tests/test_script_generator.py` confirming FOIA-aware length math and `spatial_anchors` grounding.
- **Acceptance:** Topology-safe grounded script generator verified.

### Task 053: Implement "That vs. How" AdSense & Defamation Forensic Rewriter (`that-vs-how-linter@1`) (`packages/agent3_gatekeeper`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 052`
- **Git Worktree & Branch:** `task/053-agent3-that-vs-how-linter` in `../tc-wt/task-053-agent3-that-vs-how-linter`
- **Owned Write Scope:** `packages/agent3_gatekeeper/src/that_vs_how_linter.py`, `packages/agent3_gatekeeper/tests/test_that_vs_how_linter.py`, `.agent-handoffs/task-053.md`
- **Mandatory Reference Files:** [legal-copyright-and-adsense.md](legal-copyright-and-adsense.md), [prompt-contracts.md](prompt-contracts.md)
- **Shared Contracts Consumed / Produced:** Clinical forensic `"that"` phrasing rewriter

#### Scope And Implementation Requirements

- [ ] Detect graphic mechanism/suffering vocabulary (`NFKC` normalized) and rewrite via `that-vs-how-linter@1` into clinical forensic `"that"` phrasing, verified by zero-tolerance regex pass.

#### Edge Cases And Failure Modes

- Unicode homoglyph evasion: normalize NFKC before scanning.

#### Bug Prevention And Invariants

- **Zero Graphic "How" Invariant.**

#### Independent Testability & Parallel Isolation

- 30-sentence adversarial rewrite tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent3_gatekeeper/tests/test_that_vs_how_linter.py` with 100% pass.
- **Acceptance:** "That vs. How" linter verified.

### Task 054: Implement Anti-AI-Legal-Persona Filter (`packages/agent3_gatekeeper`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 052`
- **Git Worktree & Branch:** `task/054-agent3-anti-legal-persona` in `../tc-wt/task-054-agent3-anti-legal-persona`
- **Owned Write Scope:** `packages/agent3_gatekeeper/src/anti_legal_persona.py`, `packages/agent3_gatekeeper/tests/test_anti_legal_persona.py`, `.agent-handoffs/task-054.md`
- **Mandatory Reference Files:** [legal-copyright-and-adsense.md](legal-copyright-and-adsense.md)
- **Shared Contracts Consumed / Produced:** Enforces YouTube July 2025 YPP Inauthentic/Repetitious Content policy risk controls (`F-13`)

#### Scope And Implementation Requirements

- [ ] Strip unattributed legal advice/interpretation phrasing, rewriting to objective procedural reporting (`"the prosecutor charged X"`, `"the court held"`).

#### Edge Cases And Failure Modes

- Verbatim attributed judicial quote: permitted strictly inside explicit attribution tags.

#### Bug Prevention And Invariants

- **Zero AI Legal Advice Invariant.**

#### Independent Testability & Parallel Isolation

- Pure Python regex/NLP tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent3_gatekeeper/tests/test_anti_legal_persona.py` with 100% pass.
- **Acceptance:** Anti-AI-Legal-Persona filter verified.

### Task 055: Implement Mandatory `news_report` Hedging Verifier (`packages/agent3_gatekeeper`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 040`, `Task 052`
- **Git Worktree & Branch:** `task/055-agent3-hedging-verifier` in `../tc-wt/task-055-agent3-hedging-verifier`
- **Owned Write Scope:** `packages/agent3_gatekeeper/src/hedging_verifier.py`, `packages/agent3_gatekeeper/tests/test_hedging_verifier.py`, `.agent-handoffs/task-055.md`
- **Mandatory Reference Files:** [legal-copyright-and-adsense.md](legal-copyright-and-adsense.md)
- **Shared Contracts Consumed / Produced:** Verifies every script beat citing `news_report` carries explicit attribution hedging

#### Scope And Implementation Requirements

- [ ] Cross-check beat `cited_fact_ids[]` against `fact_ledger`, auto-injecting or requiring approved hedges on any `news_report` citation (`RULE_09`).

#### Edge Cases And Failure Modes

- Mixed `court_ruling` + `news_report` beat: requires explicit hedging unless secondary clause is separated.

#### Bug Prevention And Invariants

- **Zero Unhedged Secondary Claim Invariant.**

#### Independent Testability & Parallel Isolation

- Pure Python tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent3_gatekeeper/tests/test_hedging_verifier.py` with 100% pass.
- **Acceptance:** Hedging verifier verified.

### Task 056: Implement First-30s AdSense Safety & Hard-Blocked Topic Classifier (`packages/agent3_gatekeeper`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 053`, `Task 054`
- **Git Worktree & Branch:** `task/056-agent3-first30s-adsense-gate` in `../tc-wt/task-056-agent3-first30s-adsense-gate`
- **Owned Write Scope:** `packages/agent3_gatekeeper/src/adsense_gate.py`, `packages/agent3_gatekeeper/tests/test_adsense_gate.py`, `.agent-handoffs/task-056.md`
- **Mandatory Reference Files:** [legal-copyright-and-adsense.md](legal-copyright-and-adsense.md)
- **Shared Contracts Consumed / Produced:** Enforces `first_30s_adsense_safe = 1` across both opening narration AND any cold-open FOIA slice

#### Scope And Implementation Requirements

- [ ] Inspect `0:00–0:30` opening script + cold-open `foia_asset_id` slice profanity intervals (`Task 048`) ensuring zero profanity, zero weapon terms, and zero graphic distress tags in the intro hook.

#### Edge Cases And Failure Modes

- FOIA slice `0:40–0:52` mapped to cold open: cross-checks `profanity_intervals_json` for `[40000, 52000]` before clearing `first_30s_adsense_safe = 1`.

#### Bug Prevention And Invariants

- **Clean Opening 30s Invariant.**

#### Independent Testability & Parallel Isolation

- Unit tests with cold-open FOIA slice overlap.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent3_gatekeeper/tests/test_adsense_gate.py` with 100% pass.
- **Acceptance:** First-30s AdSense safety gate verified.

### Task 057: Implement `altered_content_disclosure` & `"TRANSCRIPT DRAMATIZATION"` Quote Classifier (`packages/agent3_gatekeeper`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 056`
- **Git Worktree & Branch:** `task/057-agent3-disclosure-dramatization` in `../tc-wt/task-057-agent3-disclosure-dramatization`
- **Owned Write Scope:** `packages/agent3_gatekeeper/src/disclosure_classifier.py`, `packages/agent3_gatekeeper/tests/test_disclosure_classifier.py`, `.agent-handoffs/task-057.md`
- **Mandatory Reference Files:** [legal-copyright-and-adsense.md](legal-copyright-and-adsense.md), [research/youtube-2026-policy-and-adsense.md](research/youtube-2026-policy-and-adsense.md)
- **Shared Contracts Consumed / Produced:** Sets `altered_content_disclosure` AND flags **`requires_dramatization_badge = True`** on any verbatim suspect/911 quote voiced by TTS

#### Scope And Implementation Requirements

- [ ] Set `altered_content_disclosure = False` for stylized 2D stick figures (`True` only if realistic reconstruction tags present).
- [ ] Detect any verbatim suspect/witness/911 quote voiced by Gemini TTS inside `AUDIO_EVIDENCE_CARD` or `RedactedDocReveal`, tagging `requires_dramatization_badge = True` so Part 2 renders `"TRANSCRIPT DRAMATIZATION"` unambiguously!

#### Edge Cases And Failure Modes

- TTS reading a 911 transcript quote over an `AUDIO_EVIDENCE_CARD` waveform without badge: viewer could mistake TTS for real archival 911 recording -> mandatory badge prevents misleading-audio flags!

#### Bug Prevention And Invariants

- **Honest Archival vs TTS Quote Separation Invariant.**

#### Independent Testability & Parallel Isolation

- Unit tests on verbatim quote vs archival WAV beats.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent3_gatekeeper/tests/test_disclosure_classifier.py` with 100% pass.
- **Acceptance:** Disclosure & dramatization badge classifier verified.

### Task 058: Implement Full Compliance Audit Receipt & Provenance Writer (`packages/agent3_gatekeeper`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 046`, `Task 051`, `Task 055`, `Task 057`
- **Git Worktree & Branch:** `task/058-agent3-compliance-receipt` in `../tc-wt/task-058-agent3-compliance-receipt`
- **Owned Write Scope:** `packages/agent3_gatekeeper/src/audit_writer.py`, `packages/agent3_gatekeeper/tests/test_audit_writer.py`, `.agent-handoffs/task-058.md`
- **Mandatory Reference Files:** [legal-copyright-and-adsense.md](legal-copyright-and-adsense.md), [schema/pipeline.sql](schema/pipeline.sql)
- **Shared Contracts Consumed / Produced:** Writes `compliance_audits` row (`spoken_pii_audit_passed = 1`, `first_30s_adsense_safe = 1`, etc.) & emits `ComplianceClearedCase`

#### Scope And Implementation Requirements

- [ ] Verify every FOIA asset has `normalized_cfr_30fps_48k = 1`, `rights_review_status = 'APPROVED'`, `watermark_clean = 1`, `visual_pii_blurred = 1`, `spoken_pii_bleeped = 1`, and either `asr_hypothesis_disagreement <= 0.10` or explicit `human_audio_review_required` sign-off (if Demucs ran), then persist `compliance_audits` and advance to `COMPLIANCE_PASSED`.

#### Edge Cases And Failure Modes

- Missing `spoken_pii_bleeped = 1` on a 911 WAV: hard block `COMPLIANCE_BLOCKED`.

#### Bug Prevention And Invariants

- **Fail-Closed Compliance Gate Invariant.**

#### Independent Testability & Parallel Isolation

- Complete vs incomplete compliance-state unit tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent3_gatekeeper/tests/test_audit_writer.py` with 100% pass.
- **Acceptance:** Compliance receipt writer verified.

### Task 059: Agent 3 Granular Legal, Spoken PII & Policy Red-Team Suite (`packages/agent3_gatekeeper`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 045`–`058`
- **Git Worktree & Branch:** `task/059-agent3-redteam-suite` in `../tc-wt/task-059-agent3-redteam-suite`
- **Owned Write Scope:** `packages/agent3_gatekeeper/src/pipeline.py`, `packages/agent3_gatekeeper/tests/test_agent3_redteam.py`, `.agent-handoffs/task-059.md`
- **Mandatory Reference Files:** [legal-copyright-and-adsense.md](legal-copyright-and-adsense.md), [architecture-review-decisions.md](architecture-review-decisions.md)
- **Shared Contracts Consumed / Produced:** `Agent3GatekeeperService` certified against all 9 copyright, privacy, audio, and AdSense vectors

#### Scope And Implementation Requirements

- [ ] Verify 100% defense across: (1) MuckRock Ring CCTV inside FOIA ZIP (`RESTRICTED_NO_REUSE`), (2) Wikimedia `CC BY-NC` image, (3) distorted 8 kHz 911 WAV (Demucs safely bypassed!), (4) 440Hz-music bodycam (Demucs stripped, `asr_hypothesis_disagreement <= 0.10` & labeled corpus WER verified), (5) profanity at `0:42` routed to `0:00` hook, (6) spoken phone number & address in 911 audio, (7) TV corner logo + bystander face, (8) graphic `"how"` + AI legal advice, (9) unhedged `news_report`.

#### Edge Cases And Failure Modes

- Simultaneous spoken PII + profanity overlap: cleanly muted and verified via post-scrub ASR scan.

#### Bug Prevention And Invariants

- **Zero Policy/Privacy/Copyright Leak Invariant.**

#### Independent Testability & Parallel Isolation

- 100% standalone test suite inside `packages/agent3_gatekeeper`.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent3_gatekeeper/tests/test_agent3_redteam.py` achieving 100% pass.
- **Acceptance:** Agent 3 certified against all legal, media, and privacy traps.

### Task 060: Music-Gated Demucs + Visual/Spoken PII Scrubbing Local Benchmark (`packages/agent3_gatekeeper`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M1-P1 · Scout, Disposition Gate, Early 2K Lock & PII/AdSense`
- **Depends On:** `Task 047`, `Task 051`, `Task 059`
- **Git Worktree & Branch:** `task/060-agent3-scrub-benchmark` in `../tc-wt/task-060-agent3-scrub-benchmark`
- **Owned Write Scope:** `packages/agent3_gatekeeper/benchmarks/bench_scrub.py`, `packages/agent3_gatekeeper/tests/test_bench_scrub.py`, `.agent-handoffs/task-060.md`
- **Mandatory Reference Files:** [legal-copyright-and-adsense.md](legal-copyright-and-adsense.md), [roadmap.md](roadmap.md)
- **Shared Contracts Consumed / Produced:** Verifies bounded `< 4 GB` RAM and speedup from skipping Demucs on pure-speech 911 clips

#### Scope And Implementation Requirements

- [ ] Benchmark music-gated Demucs vs unconditional Demucs + OpenCV/YOLO PII scrubbing across 10s–60s synthetic clips, confirming peak RAM `< 4 GB` and fast bypass on non-music 911 tracks.

#### Edge Cases And Failure Modes

- Long 30-min bodycam: pre-slice manifest windows (`+/- 5s`) before Demucs.

#### Bug Prevention And Invariants

- **Bounded Memory & Fast Pure-Speech Bypass Invariant.**

#### Independent Testability & Parallel Isolation

- Runs deterministically on `fixtures/synthetic_media/`.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent3_gatekeeper/tests/test_bench_scrub.py` with 100% pass.
- **Acceptance:** Milestone `M1-P1` exit check complete!

---

### Task 061: Implement Script Beat & FOIA-Slot Chunker (`packages/voice_sync`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 058`
- **Git Worktree & Branch:** `task/061-voice-segmented-chunker` in `../tc-wt/task-061-voice-segmented-chunker`
- **Owned Write Scope:** `packages/voice_sync/src/chunker.py`, `packages/voice_sync/tests/test_chunker.py`, `.agent-handoffs/task-061.md`
- **Mandatory Reference Files:** [voice-first-and-asr-sync.md](voice-first-and-asr-sync.md)
- **Shared Contracts Consumed / Produced:** `TtsSegmentPlan` separating `NARRATION` chunks (`1–3 min`, `< 16,384` token cap) from `FOIA_AUDIO_SLOT` intervals

#### Scope And Implementation Requirements

- [ ] Partition `ComplianceClearedCase` into ordered `NARRATION` chunks (`150–450` words, never splitting mid-sentence), `TWIST_PAD` markers (`is_plot_twist: true`), and `FOIA_AUDIO_SLOT` intervals (`foia_asset_id`, `duration_ms`) where Track 1 remains silent while Track 2 FOIA plays!

#### Edge Cases And Failure Modes

- Short 2-sentence narration sandwiched between two FOIA clips: allow `< 1 min` chunk cleanly rather than merging across a FOIA gap!

#### Bug Prevention And Invariants

- **FOIA-Slot Separation Invariant:** Narration chunks never bleed across `FOIA_AUDIO_SLOT` boundaries.

#### Independent Testability & Parallel Isolation

- Pure Python unit tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/voice_sync/tests/test_chunker.py` with 100% pass.
- **Acceptance:** Segmented Voice/FOIA chunker verified.

### Task 062: Implement Config-Driven Gemini 3.8 TTS Adapter With Per-Chunk LUFS/EQ Consistency (`packages/voice_sync`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 014`, `Task 061`
- **Git Worktree & Branch:** `task/062-gemini-tts-eq-consistent` in `../tc-wt/task-062-gemini-tts-eq-consistent`
- **Owned Write Scope:** `packages/voice_sync/src/gemini_tts.py`, `packages/voice_sync/tests/test_gemini_tts.py`, `.agent-handoffs/task-062.md`
- **Mandatory Reference Files:** [voice-first-and-asr-sync.md](voice-first-and-asr-sync.md)
- **Shared Contracts Consumed / Produced:** `GeminiTtsAdapter` reading model/rates from `providers.yaml` and matching per-chunk loudness/EQ

#### Scope And Implementation Requirements

- [ ] Load `gemini-3.8-flash-tts` / `flash-lite-tts` config from `providers.yaml`, inject an identical directing style prefix per chunk, resample `24 kHz` output cleanly to `48 kHz stereo PCM`, and run **per-chunk `-16.0 LUFS` loudness + spectral tilt normalization** so acoustic tone never shifts across 7–20 separate TTS calls!

#### Edge Cases And Failure Modes

- Chunk #8 synthesized noticeably louder or brighter than Chunk #7: per-chunk `-16 LUFS` + mild shelf EQ matching eliminates seam jumps completely!

#### Bug Prevention And Invariants

- **Consistent Acoustic Seam Invariant:** All chunks match `48 kHz PCM` and `-16.0 +/- 0.5 LUFS` before timeline assembly.

#### Independent Testability & Parallel Isolation

- Tested offline with mocked Gemini WAV payloads of mismatched gain.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/voice_sync/tests/test_gemini_tts.py` verifying `48 kHz` resampling and `-16 LUFS` chunk parity.
- **Acceptance:** Consistent Gemini 3.8 TTS adapter verified.

### Task 063: Implement Google Vids Audio-Extraction Optional Fallback (`packages/voice_sync`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 061`
- **Git Worktree & Branch:** `task/063-google-vids-tts-adapter` in `../tc-wt/task-063-google-vids-tts-adapter`
- **Owned Write Scope:** `packages/voice_sync/src/google_vids_tts.py`, `packages/voice_sync/tests/test_google_vids_tts.py`, `.agent-handoffs/task-063.md`
- **Mandatory Reference Files:** [voice-first-and-asr-sync.md](voice-first-and-asr-sync.md)
- **Shared Contracts Consumed / Produced:** Optional `48 kHz` WAV extraction from user-exported Google Vids voiceovers

#### Scope And Implementation Requirements

- [ ] Format bracket-tag scripts (`[calmly]`, `[dramatically]`) and extract/normalize `48 kHz stereo PCM` (`-16 LUFS`) via FFmpeg from manually exported Google Vids MP4s when explicitly selected.

#### Edge Cases And Failure Modes

- Exported MP4 lacks audio stream: fail fast with explicit `MissingAudioStreamError`.

#### Bug Prevention And Invariants

- **Uniform 48 kHz / -16 LUFS Output Invariant.**

#### Independent Testability & Parallel Isolation

- Tested on synthetic MP4 fixture.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/voice_sync/tests/test_google_vids_tts.py` with 100% pass.
- **Acceptance:** Google Vids optional TTS adapter verified.

### Task 064: Implement DeepSeek Speech TTS Failover Adapter (`packages/voice_sync`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 014`, `Task 061`
- **Git Worktree & Branch:** `task/064-deepseek-tts-adapter` in `../tc-wt/task-064-deepseek-tts-adapter`
- **Owned Write Scope:** `packages/voice_sync/src/deepseek_tts.py`, `packages/voice_sync/tests/test_deepseek_tts.py`, `.agent-handoffs/task-064.md`
- **Mandatory Reference Files:** [voice-first-and-asr-sync.md](voice-first-and-asr-sync.md)
- **Shared Contracts Consumed / Produced:** Config-driven DeepSeek TTS failover (`providers.yaml`)

#### Scope And Implementation Requirements

- [ ] Implement DeepSeek TTS client reading character rates from `providers.yaml`, normalizing to `48 kHz PCM / -16 LUFS`, and enforcing single-voice consistency per episode on failover.

#### Edge Cases And Failure Modes

- Mid-episode failover: re-synthesize prior chunks on the failover voice so voice timbre never changes mid-documentary!

#### Bug Prevention And Invariants

- **Single-Voice Per Episode Invariant.**

#### Independent Testability & Parallel Isolation

- Mocked HTTP failover tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/voice_sync/tests/test_deepseek_tts.py` with 100% pass.
- **Acceptance:** DeepSeek TTS failover verified.

### Task 065: Implement Room-Tone `TwistPad` & Segmented `voice_segments` Timeline Builder (`packages/voice_sync`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 062`–`064`
- **Git Worktree & Branch:** `task/065-segmented-voice-timeline` in `../tc-wt/task-065-segmented-voice-timeline`
- **Owned Write Scope:** `packages/voice_sync/src/stitcher.py`, `packages/voice_sync/tests/test_stitcher.py`, `.agent-handoffs/task-065.md`
- **Mandatory Reference Files:** [voice-first-and-asr-sync.md](voice-first-and-asr-sync.md), [schema/pipeline.sql](schema/pipeline.sql)
- **Shared Contracts Consumed / Produced:** Builds ordered `voice_segments` (`NARRATION`, `TWIST_PAD`, `FOIA_AUDIO_SLOT`) where room-tone silence pads (`-65 dBFS`, never dead digital zero!) follow `is_plot_twist: true`

#### Scope And Implementation Requirements

- [ ] Assemble exact master timeline map (`start_ms`, `end_ms`) interleaving `NARRATION` WAV segments, **`0.45s–0.75s` sampled room-tone `TWIST_PAD`s** (low-level `-65 dBFS` pink/room noise floor, never dead zero digital dropout!), and silent Track-1 **`FOIA_AUDIO_SLOT`** windows matching scrubbed FOIA clip durations (`+ 0.6s–1.0s` L-cut pre-roll).
- [ ] Persist segments into SQLite `voice_segments` and set `episodes.total_master_ms`.

#### Edge Cases And Failure Modes

- Dead digital zero (`0.0`) silence pad sounding like an audio glitch on headphones: verify RMS of `TWIST_PAD` sits strictly in `[-72 dBFS, -58 dBFS]` room-tone band!

#### Bug Prevention And Invariants

- **Zero Monolithic TTS Assumption & Non-Zero Room-Tone Invariant:** `total_master_ms` explicitly accounts for every `FOIA_AUDIO_SLOT` and `TWIST_PAD`.

#### Independent Testability & Parallel Isolation

- SciPy/FFmpeg waveform & SQLite timeline tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/voice_sync/tests/test_stitcher.py` verifying room-tone floor, exact segment bounds, and `total_master_ms`.
- **Acceptance:** Segmented voice timeline builder verified.

### Task 066: Implement Local WhisperX Forced Word-Level Aligner & Global Offset Mapper (`packages/voice_sync`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 014`, `Task 065`
- **Git Worktree & Branch:** `task/066-whisperx-word-aligner` in `../tc-wt/task-066-whisperx-word-aligner`
- **Owned Write Scope:** `packages/voice_sync/src/whisperx_aligner.py`, `packages/voice_sync/tests/test_whisperx_aligner.py`, `.agent-handoffs/task-066.md`
- **Mandatory Reference Files:** [voice-first-and-asr-sync.md](voice-first-and-asr-sync.md), [research/voice-first-tts-asr-sync.md](research/voice-first-tts-asr-sync.md)
- **Shared Contracts Consumed / Produced:** **Sole Owner of Millisecond `WordTimestamp[]` (`F-03`)** via local `$0` WhisperX forced alignment mapped accurately onto global `total_master_ms`

#### Scope And Implementation Requirements

- [ ] Run local **WhisperX + Phoneme Wav2Vec2 forced aligner (`whisperx-local`)** offline (`$0` API cost, zero `8 MiB` / `120s` upload limit!) against each `NARRATION` segment's `48 kHz` WAV + `approved_narration_text`, offsetting every `WordTimestamp` cleanly by `segment.start_ms`!

#### Edge Cases And Failure Modes

- Offset forgetting `FOIA_AUDIO_SLOT` duration before Segment 3: verify timestamps after a `25s` FOIA slot jump cleanly by `+25,000 ms`!
- Why DeepSeek ASR is NOT used here (`F-03`): DeepSeek Speech-to-Text enforces a hard `8 MiB / 120s` limit (`48 kHz` stereo PCM exceeds `8 MiB` in `< 1 min`) and returns no word-level timestamps.

#### Bug Prevention And Invariants

- **Offline Forced Alignment & Global Timeline Offset Accuracy Invariant (`F-03`).**

#### Independent Testability & Parallel Isolation

- Offline unit tests with synthetic forced-alignment fixtures across multi-segment timelines containing FOIA gaps (`$0` network calls).

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/voice_sync/tests/test_whisperx_aligner.py` with 100% pass offline.
- **Acceptance:** Local WhisperX word-level aligner verified.

### Task 067: Implement Bounded Cloud ASR Wrapper (`<= 90s / <= 4 MiB` `16 kHz` FLAC Slicer) (`packages/voice_sync`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 066`
- **Git Worktree & Branch:** `task/067-bounded-cloud-asr-slicer` in `../tc-wt/task-067-bounded-cloud-asr-slicer`
- **Owned Write Scope:** `packages/voice_sync/src/bounded_cloud_asr.py`, `packages/voice_sync/tests/test_bounded_cloud_asr.py`, `.agent-handoffs/task-067.md`
- **Mandatory Reference Files:** [voice-first-and-asr-sync.md](voice-first-and-asr-sync.md), [research/voice-first-tts-asr-sync.md](research/voice-first-tts-asr-sync.md)
- **Shared Contracts Consumed / Produced:** Optional raw-FOIA cloud transcription adapter (DeepSeek ASR / Gemini Transcribe) strictly slicing/transcoding audio to **`16 kHz` mono FLAC `<= 90s / <= 4 MiB`** (`F-03`)

#### Scope And Implementation Requirements

- [ ] Before calling any optional cloud ASR (DeepSeek Speech-to-Text `8 MiB / 120s` max or Gemini Transcribe) on unscripted FOIA/911 audio, deterministically downsample to `16 kHz` mono FLAC and split on silence into **`<= 90s`** chunks strictly `< 4 MiB`, followed by WhisperX if word timestamps are needed (`never` send `48 kHz` stereo PCM to DeepSeek ASR!).
- [ ] Include spoken-number normalization (`"2023"` -> `"twenty twenty three"`) cleanly.

#### Edge Cases And Failure Modes

- Caller passes a 3-minute `48 kHz` stereo WAV (`~34 MB`) directly: slicer enforces chunking + `16 kHz` FLAC transcode so every payload fits cleanly `< 4 MiB` & `<= 90s`!

#### Bug Prevention And Invariants

- **Strict API Payload-Limit Invariant (`F-03`):** Hard-reject any cloud ASR payload `> 7.5 MiB` or `> 115s` prior to network transmission (mocked offline in tests).

#### Independent Testability & Parallel Isolation

- Offline chunker/size-guard tests using 3-minute synthetic stereo `48 kHz` WAVs (`$0` API calls).

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/voice_sync/tests/test_bounded_cloud_asr.py` verifying strict `<= 90s / <= 4 MiB` slicing and mocked transport handling.
- **Acceptance:** Bounded cloud ASR slicer verified compatible with DeepSeek/Gemini API limits.

### Task 068: Implement Millisecond Keyword Trigger & Free ASR Proper-Noun Phonetic Diff Check (`packages/voice_sync`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 066`, `Task 067`
- **Git Worktree & Branch:** `task/068-keyword-cue-and-pronunciation-check` in `../tc-wt/task-068-keyword-cue-and-pronunciation-check`
- **Owned Write Scope:** `packages/voice_sync/src/cue_indexer.py`, `packages/voice_sync/tests/test_cue_indexer.py`, `.agent-handoffs/task-068.md`
- **Mandatory Reference Files:** [voice-first-and-asr-sync.md](voice-first-and-asr-sync.md), [research/voice-first-tts-asr-sync.md](research/voice-first-tts-asr-sync.md)
- **Shared Contracts Consumed / Produced:** Resolves visual clue trigger timestamps AND flags mangled TTS pronunciations of suspect/victim/town names via **free ASR-vs-Script phonetic diffing**

#### Scope And Implementation Requirements

- [ ] Map visual cue triggers inside beat boundaries (`[beat_start_ms, beat_end_ms]`).
- [ ] **Proper-Noun Pronunciation Gate:** Run raw un-forced ASR phonetic comparison (Metaphone/Double-Metaphone + Jaro-Winkler) on proper nouns (`defendant_name`, street/town names, county). If TTS mangled a name (`similarity < 0.72`), automatically generate a phonetic respelling override (`"Krzysztof"` -> `"KRIH-stohf"`) and re-synthesize strictly that single chunk BEFORE video rendering!

#### Edge Cases And Failure Modes

- Unusual surname mispronounced by Gemini TTS as an unrelated English word: phonetic diff flags `similarity = 0.35`, triggers phonetic respelling retry, and verifies fix on re-check!

#### Bug Prevention And Invariants

- **Zero Mangled Proper-Noun Pronunciation Invariant:** Embarrassing TTS mispronunciations of real victim/suspect/town names are caught free via ASR before rendering.

#### Independent Testability & Parallel Isolation

- Unit tested with intentionally mispronounced proper-noun ASR fixtures.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/voice_sync/tests/test_cue_indexer.py` verifying beat-scoped keyword sync and proper-noun phonetic diff catch.
- **Acceptance:** Keyword cue & proper-noun pronunciation verifier passed.

### Task 069: Implement RMS Vocal Amplitude Envelope Extractor (`packages/voice_sync`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 065`
- **Git Worktree & Branch:** `task/069-rms-amplitude-envelope` in `../tc-wt/task-069-rms-amplitude-envelope`
- **Owned Write Scope:** `packages/voice_sync/src/amplitude_envelope.py`, `packages/voice_sync/tests/test_amplitude_envelope.py`, `.agent-handoffs/task-069.md`
- **Mandatory Reference Files:** [voice-first-and-asr-sync.md](voice-first-and-asr-sync.md), [code-animation-catalog.md](code-animation-catalog.md)
- **Shared Contracts Consumed / Produced:** `30 fps` `amplitude_envelope[]` aligned across `NARRATION`, `TWIST_PAD` (`0.0`), and `FOIA_AUDIO_SLOT` (`0.0`)

#### Scope And Implementation Requirements

- [ ] Extract quantized `[0.00–1.00]` RMS envelope at `30 fps` across all `NARRATION` segments (`-50 dBFS` noise gate -> `0.00` during `-65 dBFS` room-tone twist pads and FOIA slots).

#### Edge Cases And Failure Modes

- Off-by-one frame counts across 15 segments: compute exact frame boundaries in `int64` milliseconds (`round(total_master_ms * 30 / 1000)`).

#### Bug Prevention And Invariants

- **Exact 30-fps Master Timeline Length Invariant.**

#### Independent Testability & Parallel Isolation

- SciPy/NumPy verification tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/voice_sync/tests/test_amplitude_envelope.py` with 100% pass.
- **Acceptance:** Amplitude envelope extractor verified.

### Task 070: Implement Segmented Timeline Drift Validator (`packages/voice_sync`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 068`, `Task 069`
- **Git Worktree & Branch:** `task/070-voice-drift-validator` in `../tc-wt/task-070-voice-drift-validator`
- **Owned Write Scope:** `packages/voice_sync/src/drift_validator.py`, `packages/voice_sync/tests/test_drift_validator.py`, `.agent-handoffs/task-070.md`
- **Mandatory Reference Files:** [voice-first-and-asr-sync.md](voice-first-and-asr-sync.md)
- **Shared Contracts Consumed / Produced:** Confirms `sum(voice_segments) == total_master_ms` with `< 20 ms` total drift

#### Scope And Implementation Requirements

- [ ] Verify every `NARRATION` WAV file duration via `FFprobe` matches its `voice_segments` interval and total `total_master_ms` exhibits `< 20 ms` drift across 1,200s.

#### Edge Cases And Failure Modes

- Cumulative floating-point rounding drift: integer millisecond arithmetic only.

#### Bug Prevention And Invariants

- **Zero Cumulative Drift Invariant (`< 20 ms`).**

#### Independent Testability & Parallel Isolation

- 1,200-second simulated segmented timeline tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/voice_sync/tests/test_drift_validator.py` with 100% pass.
- **Acceptance:** Segmented drift validator verified.

### Task 071: Implement `VoiceTrackManifest` Serializer & Cache Store (`packages/voice_sync`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 002`, `Task 070`
- **Git Worktree & Branch:** `task/071-voice-manifest-serializer` in `../tc-wt/task-071-voice-manifest-serializer`
- **Owned Write Scope:** `packages/voice_sync/src/manifest_writer.py`, `packages/voice_sync/tests/test_manifest_writer.py`, `.agent-handoffs/task-071.md`
- **Mandatory Reference Files:** [voice-first-and-asr-sync.md](voice-first-and-asr-sync.md)
- **Shared Contracts Consumed / Produced:** Frozen segmented `VoiceTrackManifest` validated against `packages/shared_contracts`

#### Scope And Implementation Requirements

- [ ] Serialize `VoiceTrackManifest` (`segments[]`, `total_master_ms`, `word_timestamps[]`, `cue_points[]`, `amplitude_envelope[]`) cached per chunk SHA-256 so proper-noun fixes only re-synthesize the single edited chunk!

#### Edge Cases And Failure Modes

- Re-synthesizing 1 edited chunk shifts downstream timestamps: automatically recompute global offsets cleanly in `manifest_writer.py`.

#### Bug Prevention And Invariants

- **Chunk-Granular Cache Invariant.**

#### Independent Testability & Parallel Isolation

- Schema & cache invalidation unit tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/voice_sync/tests/test_manifest_writer.py` with 100% pass.
- **Acceptance:** `VoiceTrackManifest` serializer verified.

### Task 072: Voice-First Segmented Timeline & Pronunciation Integration Suite (`packages/voice_sync`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 061`–`071`
- **Git Worktree & Branch:** `task/072-voice-sync-e2e-suite` in `../tc-wt/task-072-voice-sync-e2e-suite`
- **Owned Write Scope:** `packages/voice_sync/src/pipeline.py`, `packages/voice_sync/tests/test_voice_sync_e2e.py`, `.agent-handoffs/task-072.md`
- **Mandatory Reference Files:** [voice-first-and-asr-sync.md](voice-first-and-asr-sync.md)
- **Shared Contracts Consumed / Produced:** `VoiceSyncService` transitioning episodes cleanly to `VOICE_READY`

#### Scope And Implementation Requirements

- [ ] Verify end-to-end chunking -> consistent `-16 LUFS / 48 kHz` TTS -> room-tone TwistPads + FOIA slots -> ASR global offset + proper-noun pronunciation diff -> `< 20 ms` drift -> schema parity with Golden Pack.

#### Edge Cases And Failure Modes

- TTS 429 + phonetic mismatch retry in same run: clean recovery without orphaned WAVs.

#### Bug Prevention And Invariants

- **Segmented Voice-First Completeness Invariant.**

#### Independent Testability & Parallel Isolation

- 100% standalone test suite in `packages/voice_sync`.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/voice_sync` with 100% pass.
- **Acceptance:** Segmented Voice-First subsystem certified.

---

### Task 073: Implement `CaseBible` Style DNA & Monochrome Keyframe Palette Builder (`packages/agent4_director`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 002`, `Task 012`, `Task 072`
- **Git Worktree & Branch:** `task/073-agent4-case-bible` in `../tc-wt/task-073-agent4-case-bible`
- **Owned Write Scope:** `packages/agent4_director/src/case_bible.py`, `packages/agent4_director/tests/test_case_bible.py`, `.agent-handoffs/task-073.md`
- **Mandatory Reference Files:** [director-and-13-laws.md](director-and-13-laws.md), [code-animation-catalog.md](code-animation-catalog.md)
- **Shared Contracts Consumed / Produced:** Locks `CaseBible` separating `evidenceCrimsonHex` (Remotion/2K callouts ONLY) from `flowKeyframeSafePalette` (monochrome + muted blue/amber ONLY)

#### Scope And Implementation Requirements

- [ ] Lock `CaseBible` with unique character props/colors (`detective_01`, `suspect_01`, etc.) AND explicitly tag `flowKeyframeSafePalette` excluding `evidenceCrimsonHex` so Python Start/End PNGs never trip safety filters!

#### Edge Cases And Failure Modes

- `suspect_01` assigned crimson accent `#C92A2A` used inside a Flow Start PNG: `flowKeyframeSafePalette` substitutes muted slate/amber for Flow PNGs while retaining crimson strictly for Remotion/2K overlays!

#### Bug Prevention And Invariants

- **Zero Crimson in Flow Keyframes Invariant.**

#### Independent Testability & Parallel Isolation

- Pure Python + SQLite unit tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent4_director/tests/test_case_bible.py` with 100% pass.
- **Acceptance:** `CaseBible` builder verified.

### Task 074: Implement Byte-0 Global Static Prompt-Cached Director Client (`packages/agent4_director`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 014`, `Task 073`
- **Git Worktree & Branch:** `task/074-agent4-byte0-prompt-cache` in `../tc-wt/task-074-agent4-byte0-prompt-cache`
- **Owned Write Scope:** `packages/agent4_director/src/cached_director_client.py`, `packages/agent4_director/tests/test_cached_director_client.py`, `.agent-handoffs/task-074.md`
- **Mandatory Reference Files:** [prompt-contracts.md](prompt-contracts.md), [economics-and-credit-math.md](economics-and-credit-math.md)
- **Shared Contracts Consumed / Produced:** Orders prompt prefix strictly **Byte 0 Global Static Rules -> Tier 2 Episode `CaseBible` -> Tier 3 Dynamic Scene** so cache hits work *across episodes*!

#### Scope And Implementation Requirements

- [ ] Place immutable global rules (13 Laws, 12-Motif Zod schema, split Metaphor Tables) at **byte `0`** (`sort_keys=True`), `CaseBible` + `spatial_anchors` in Tier 2, and dynamic `VoiceTrackManifest` segments at the tail, reading model config from `providers.yaml`.

#### Edge Cases And Failure Modes

- Putting `CaseBible` before static schemas (the v1 bug): assert byte-`0` SHA-256 across TWO DIFFERENT episodes is **100% identical**!

#### Bug Prevention And Invariants

- **Cross-Episode Byte-0 Prefix Invariance:** Global static prefix hash stays identical across Episode 1 and Episode 2.

#### Independent Testability & Parallel Isolation

- Cross-episode byte-comparison unit tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent4_director/tests/test_cached_director_client.py` confirming identical byte-0 prefix across distinct episodes.
- **Acceptance:** Cross-episode prompt cache ordering verified.

### Task 075: Implement Layer 1 `director-manifest@4` Proposal Generator (`13.0m / 5.67m / 1.33m` Split & `ScenePlan`) (`packages/agent4_director`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 074`
- **Git Worktree & Branch:** `task/075-agent4-manifest-proposer` in `../tc-wt/task-075-agent4-manifest-proposer`
- **Owned Write Scope:** `packages/agent4_director/src/manifest_proposer.py`, `packages/agent4_director/tests/test_manifest_proposer.py`, `.agent-handoffs/task-075.md`
- **Mandatory Reference Files:** [director-and-13-laws.md](director-and-13-laws.md), [economics-and-credit-math.md](economics-and-credit-math.md), [craft_rubric.yaml](craft_rubric.yaml)
- **Shared Contracts Consumed / Produced:** Compiles **`13.0m Code/FOIA + 5.67m Illustrative 2K + 1.33m Omni Hero` (`max_hero_clips = 10 / 80s`)** manifest + `30 fps` `TimelineSpec` strictly bound to `PLAN_APPROVED` `scene_plans` (`F-02`, `F-04`, `F-05`)

#### Scope And Implementation Requirements

- [ ] Generate `ProductionManifest` + `TimelineSpec` (`30 fps`, `MOTIF_REGISTRY_V1`) from `PLAN_APPROVED` `scene_plans` aligned to segmented `VoiceTrackManifest`, inserting `CaseBoardSpine` inside **`210s–270s` flexible boundary-snapped windows** and enforcing single-config cap **`<= 10` Hero clips (`<= 80s`)** using `TEXT_TO_VIDEO` / `FIRST_FRAME` / `FIRST_AND_LAST_FRAME (<= 10s)`.

#### Edge Cases And Failure Modes

- 911 audio call running from `3:50` to `4:15`: `CaseBoardSpine` snaps cleanly to `4:15` (inside `210s–270s` window) instead of chopping the 911 call at `4:00`!

#### Bug Prevention And Invariants

- **Honest 1,200s Split & Zero Mid-Sentence Spine Cut Invariant.**

#### Independent Testability & Parallel Isolation

- Tested offline with mocked `director-manifest@2` responses.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent4_director/tests/test_manifest_proposer.py` with 100% pass.
- **Acceptance:** Layer 1 v2 manifest proposer verified.

### Task 076: Implement `manifest_linter.py` Core + Segmented `RULE_01` & `6s+3.2s` `RULE_03` (`packages/agent4_director`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 002`, `Task 075`
- **Git Worktree & Branch:** `task/076-linter-segmented-rule01-03` in `../tc-wt/task-076-linter-segmented-rule01-03`
- **Owned Write Scope:** `packages/agent4_director/src/linter_core.py`, `packages/agent4_director/src/rules/rule_01_03_timing.py`, `packages/agent4_director/tests/test_rule_01_03.py`, `.agent-handoffs/task-076.md`
- **Mandatory Reference Files:** [director-and-13-laws.md](director-and-13-laws.md)
- **Shared Contracts Consumed / Produced:** Fixes `RULE_01` (segmented `total_master_ms`) and `RULE_03` (`6s + 3.2s` split when remainder `< 2.5s`)

#### Scope And Implementation Requirements

- [ ] **`RULE_01`:** Verify `abs(sum(scene_durations_ms) - VoiceTrackManifest.total_master_ms) <= 250 ms` (checking `FOIA_REAL_FOOTAGE`/`AUDIO_EVIDENCE_CARD` scenes match `FoiaAudioSlot` intervals + L-cuts cleanly!).
- [ ] **`RULE_03`:** Split `> 8.5s` Flow beats cleanly: if `beat_sec - 8.0 < 2.5` (e.g., `9.2s` -> `1.2s` remainder fails `RULE_07`!), **use `6.0s Flow + (beat_sec - 6.0)s Code`** (`6.0s + 3.2s`) so every bookend holds `>= 2.5s`!

#### Edge Cases And Failure Modes

- `9.2s` dramatic beat split blindly as `8.0s + 1.2s`: fixed automatically to `6.0s + 3.2s`!

#### Bug Prevention And Invariants

- **FOIA-Aligned `RULE_01` & Minimum `>= 2.5s` Bookend Remainder Invariant.**

#### Independent Testability & Parallel Isolation

- Pure Python unit tests covering `9.2s`, `11.4s`, and 4-minute FOIA slot timelines.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent4_director/tests/test_rule_01_03.py` confirming `9.2s -> 6s+3.2s` and 4m FOIA timeline alignment pass.
- **Acceptance:** Conflict-free `RULE_01` & `RULE_03` verified.

### Task 077: Implement Act-Constrained `RULE_02` & Non-Neighbor Fallback `RULE_04` (`packages/agent4_director`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 076`
- **Git Worktree & Branch:** `task/077-linter-act-aware-rule02-04` in `../tc-wt/task-077-linter-act-aware-rule02-04`
- **Owned Write Scope:** `packages/agent4_director/src/rules/rule_02_04_budget.py`, `packages/agent4_director/tests/test_rule_02_04.py`, `.agent-handoffs/task-077.md`
- **Mandatory Reference Files:** [director-and-13-laws.md](director-and-13-laws.md)
- **Shared Contracts Consumed / Produced:** Fixes `RULE_02` vs `RULE_06` collision and `RULE_04` vs `RULE_05` fallback streak collision!

#### Scope And Implementation Requirements

- [ ] **`RULE_02` (Act-Constrained Downgrade & Global Cap Check, `F-02`, `F-04`):** Enforce single-config `providers.yaml` cap (`max_hero_clips = 10`, `max_hero_duration_sec = 80s`, `$10.40/ep` video limit) PLUS remaining global monthly headroom in `monthly_budget_ledger` (`ALL_PROVIDERS <= $135/mo`). When auto-downgrading excess clips, **protect Cold Open AND protect Act 2's `>= 2` highest-scoring hero peaks** (`RULE_06`).
- [ ] **`RULE_04` (Non-Neighbor Fallback):** Require every `FLOW_HERO_VIDEO` scene's `fallback_spec.engine != prev_scene.engine` (and `!= next_scene.engine` when distinct)—typically selecting `STILL_2K_PANZOOM` between `CODE_STICKMAN` scenes so a 2-strike fallback can NEVER create a `> 50.0s` single-engine streak (`RULE_05`)!

#### Edge Cases And Failure Modes

- Downgrading Act 2 clips leaving Act 2 with 1 peak (`RULE_06` fail): Act-constrained downgrade skips Act 2's top 2 peaks cleanly!

#### Bug Prevention And Invariants

- **Zero `RULE_02`/`RULE_06` & `RULE_04`/`RULE_05` Collisions Invariant.**

#### Independent Testability & Parallel Isolation

- Adversarial budget-overrun & neighbor-streak unit tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent4_director/tests/test_rule_02_04.py` verifying Act 2 peak protection and non-neighbor fallback selection.
- **Acceptance:** Conflict-free `RULE_02` & `RULE_04` verified.

### Task 078: Implement `RULE_05` (Flow Motion Exemption & `210–270s` Boundary-Snapped `CaseBoardSpine`) (`packages/agent4_director`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 076`, `Task 077`
- **Git Worktree & Branch:** `task/078-linter-rule05-flexible-spine` in `../tc-wt/task-078-linter-rule05-flexible-spine`
- **Owned Write Scope:** `packages/agent4_director/src/rules/rule_05_interrupt.py`, `packages/agent4_director/tests/test_rule_05.py`, `.agent-handoffs/task-078.md`
- **Mandatory Reference Files:** [director-and-13-laws.md](director-and-13-laws.md)
- **Shared Contracts Consumed / Produced:** Enforces `<= 6.0s` micro-beats on Code/2K (exempting continuous `<= 8s` Flow motion!), `<= 50.0s` macro streaks, and `210s–270s` boundary-snapped `CaseBoardSpine`

#### Scope And Implementation Requirements

- [ ] Exempt continuous `FLOW_HERO_VIDEO` clips (`<= 10.0s`) from the `<= 6.0s` static micro-beat clock (eliminating `RULE_03` vs `RULE_05` false failures on continuous Omni hero shots!).
- [ ] Validate `CaseBoardSpine` triggers inside `210s–270s` intervals strictly at completed scene/sentence boundaries (never mid-sentence or mid-911!).

#### Edge Cases And Failure Modes

- 8.0s Veo chase clip flagged as "8s static frame": exempted cleanly because native video contains continuous fluid motion!

#### Bug Prevention And Invariants

- **Zero Mid-Sentence Spine Chop & Continuous Flow Exemption Invariant.**

#### Independent Testability & Parallel Isolation

- Pure Python timeline interval tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent4_director/tests/test_rule_05.py` with 100% pass.
- **Acceptance:** Conflict-free `RULE_05` & flexible `CaseBoardSpine` verified.

### Task 079: Implement `RULE_06` Mid-Video Retention Validator (`packages/agent4_director`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 077`
- **Git Worktree & Branch:** `task/079-linter-rule06-retention` in `../tc-wt/task-079-linter-rule06-retention`
- **Owned Write Scope:** `packages/agent4_director/src/rules/rule_06_retention.py`, `packages/agent4_director/tests/test_rule_06.py`, `.agent-handoffs/task-079.md`
- **Mandatory Reference Files:** [director-and-13-laws.md](director-and-13-laws.md)
- **Shared Contracts Consumed / Produced:** Act 1 `<= 40%` Flow budget, Act 2 `>= 2` Hero/FOIA peaks, `3.5–4.5m` Open Loops

#### Scope And Implementation Requirements

- [ ] Enforce Act 1 Flow credit ceiling `<= 40%`, Act 2 (min 6–14) `>= 2` peaks, and Open Loop spacing `<= 4.5 min`.

#### Edge Cases And Failure Modes

- Intro-heavy manifest: returns Act 1->Act 2 reallocation diff.

#### Bug Prevention And Invariants

- **Anti-Front-Loading Retention Invariant.**

#### Independent Testability & Parallel Isolation

- Pure Python unit tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent4_director/tests/test_rule_06.py` with 100% pass.
- **Acceptance:** `RULE_06` verified.

### Task 080: Implement `RULE_07` ("12-Word Glance" & CSS-Delegated Safe-Zone Contract Check) (`packages/agent4_director`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 076`
- **Git Worktree & Branch:** `task/080-linter-rule07-word-and-zone` in `../tc-wt/task-080-linter-rule07-word-and-zone`
- **Owned Write Scope:** `packages/agent4_director/src/rules/rule_07_safe_zone.py`, `packages/agent4_director/tests/test_rule_07.py`, `.agent-handoffs/task-080.md`
- **Mandatory Reference Files:** [director-and-13-laws.md](director-and-13-laws.md), [code-animation-catalog.md](code-animation-catalog.md)
- **Shared Contracts Consumed / Produced:** Checks `<= 12` words + `>= 1.0 + 0.3*words` hold time + static waypoint coordinates, while delegating dynamic text wrapping containment to Remotion CSS Safe-Zones + Agent 6 pixel verification!

#### Scope And Implementation Requirements

- [ ] Validate `word_count <= 12`, `duration_sec >= 1.0 + 0.3 * word_count`, and explicit stage/2K anchor coords (`safe_zone_mode: "CSS_CONTAINED"`), without brittle Python fake text-wrap pixel simulation!

#### Edge Cases And Failure Modes

- `1.2s` remainder trying to show a 2-word headline (`1.6s` minimum): caught immediately (`RULE_03` `6s+3.2s` prevents it!).

#### Bug Prevention And Invariants

- **12-Word Glance & CSS Containment Contract Invariant.**

#### Independent Testability & Parallel Isolation

- Pure Python geometric & word-count tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent4_director/tests/test_rule_07.py` with 100% pass.
- **Acceptance:** `RULE_07` verified.

### Task 081: Implement `RULE_08` (Last-5 Cold-Open Rotation, `>=3` Insights & Brand-Coherent Mood Novelty) (`packages/agent4_director`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 013`, `Task 076`
- **Git Worktree & Branch:** `task/081-linter-rule08-brand-entropy` in `../tc-wt/task-081-linter-rule08-brand-entropy`
- **Owned Write Scope:** `packages/agent4_director/src/rules/rule_08_entropy.py`, `packages/agent4_director/tests/test_rule_08.py`, `.agent-handoffs/task-081.md`
- **Mandatory Reference Files:** [director-and-13-laws.md](director-and-13-laws.md), [mastering-loudness-and-qa.md](mastering-loudness-and-qa.md)
- **Shared Contracts Consumed / Produced:** Enforces Cold-Open rotation, `>=3` Turning Points, and **brand-coherent composition/mood novelty** (preserving channel signature framing!)

#### Scope And Implementation Requirements

- [ ] Reject consecutive duplicate `cold_open_archetype` (`EntropyAndAnalyticsRepository`), require `turning_point_count >= 3`, and verify thumbnail specification rotates **focal silhouette subject + composition + accent mood** while preserving consistent channel typography & framing!

#### Edge Cases And Failure Modes

- Analytics shows `ALIBI_THAT_CRACKED` outperforms other openers by 2x CTR: still forbid back-to-back repetition (`RULE_08`), rotating smoothly between top-performing eligible archetypes!

#### Bug Prevention And Invariants

- **Brand-Coherent Anti-Template Invariant.**

#### Independent Testability & Parallel Isolation

- Pure Python + SQLite entropy tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent4_director/tests/test_rule_08.py` with 100% pass.
- **Acceptance:** `RULE_08` verified.

### Task 082: Implement `RULE_09` & `RULE_10` (Hedging, Anti-Legal-Advice, Dramatization Badge & Disclosure) (`packages/agent4_director`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 055`, `Task 057`, `Task 076`
- **Git Worktree & Branch:** `task/082-linter-rule09-rule10` in `../tc-wt/task-082-linter-rule09-rule10`
- **Owned Write Scope:** `packages/agent4_director/src/rules/rule_09_10_policy.py`, `packages/agent4_director/tests/test_rule_09_10.py`, `.agent-handoffs/task-082.md`
- **Mandatory Reference Files:** [director-and-13-laws.md](director-and-13-laws.md), [legal-copyright-and-adsense.md](legal-copyright-and-adsense.md)
- **Shared Contracts Consumed / Produced:** Enforces `RULE_09`, `RULE_10`, and `requires_dramatization_badge` propagation on `AUDIO_EVIDENCE_CARD` scenes

#### Scope And Implementation Requirements

- [ ] Audit narration + on-screen labels against `fact_ledger`, block distress/graphic tags, and confirm any `AUDIO_EVIDENCE_CARD` playing TTS-voiced verbatim quotes carries `show_dramatization_badge = True`!

#### Edge Cases And Failure Modes

- Director drops `show_dramatization_badge` on a quoted 911 transcript scene: `RULE_10` auto-injects `"TRANSCRIPT DRAMATIZATION"` badge requirement.

#### Bug Prevention And Invariants

- **Full-Frame Policy & Dramatization Disclosure Invariant.**

#### Independent Testability & Parallel Isolation

- Adversarial on-screen banner & quote tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent4_director/tests/test_rule_09_10.py` with 100% pass.
- **Acceptance:** `RULE_09` & `RULE_10` verified.

### Task 083: Implement Law 4 Pre-Locked `spatial_anchors` & `travel_axis` Continuity Validator (`packages/agent4_director`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 042`, `Task 076`
- **Git Worktree & Branch:** `task/083-linter-law4-spatial-axis` in `../tc-wt/task-083-linter-law4-spatial-axis`
- **Owned Write Scope:** `packages/agent4_director/src/rules/law_04_spatial.py`, `packages/agent4_director/tests/test_law_04.py`, `.agent-handoffs/task-083.md`
- **Mandatory Reference Files:** [director-and-13-laws.md](director-and-13-laws.md), [evidence-and-fact-ledger.md](evidence-and-fact-ledger.md)
- **Shared Contracts Consumed / Produced:** Verifies every `STILL_2K_PANZOOM` clue reference resolves to Agent 2's pre-locked `spatial_anchors` (`span_cols`, `span_rows`) and pursuit shots hold consistent `travel_axis`

#### Scope And Implementation Requirements

- [ ] Confirm all referenced spatial anchors exist in `spatial_anchors` (`lock_status = 'LOCKED'`) referencing valid `still_assets(still_2k_id)` (`is_illustrative_reconstruction = 1`) and enforce `travel_axis` continuity across consecutive movement scenes.

#### Edge Cases And Failure Modes

- Script references clue missing from pre-locked `spatial_anchors`: return exact missing anchor diff for repair.

#### Bug Prevention And Invariants

- **Pre-Locked Spatial Truth & Screen-Axis Invariant.**

#### Independent Testability & Parallel Isolation

- Pure Python + SQLite anchor checks.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent4_director/tests/test_law_04.py` with 100% pass.
- **Acceptance:** Law 4 validator verified.

### Task 084: Implement Law 6 Segmented L-Cut, Music Ducking & Room-Tone Twist Validator (`packages/agent4_director`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 065`, `Task 076`
- **Git Worktree & Branch:** `task/084-linter-law6-audio-graph` in `../tc-wt/task-084-linter-law6-audio-graph`
- **Owned Write Scope:** `packages/agent4_director/src/rules/law_06_audio.py`, `packages/agent4_director/tests/test_law_06.py`, `.agent-handoffs/task-084.md`
- **Mandatory Reference Files:** [director-and-13-laws.md](director-and-13-laws.md), [mastering-loudness-and-qa.md](mastering-loudness-and-qa.md)
- **Shared Contracts Consumed / Produced:** Validates `0.6–1.0s` L-cuts into `FOIA_AUDIO_SLOT`s, `-22 -> -36 LUFS` music ducks, and alignment to `TWIST_PAD`s

#### Scope And Implementation Requirements

- [ ] Verify every FOIA/911 scene aligns cleanly with its `FOIA_AUDIO_SLOT` + `0.6–1.0s` visual lead-in bridged by `radio_squelch`/`tape_click` and emits `-36 LUFS` ducking windows.

#### Edge Cases And Failure Modes

- Adjacent FOIA clips `< 0.5s` apart: merge ducking envelope continuously to prevent `-36 -> -22 -> -36` pumping.

#### Bug Prevention And Invariants

- **Zero Audio Pumping & Clean L-Cut Alignment Invariant.**

#### Independent Testability & Parallel Isolation

- Pure Python manifest tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent4_director/tests/test_law_06.py` with 100% pass.
- **Acceptance:** Law 6 validator verified.

### Task 085: Implement `RULE_11` Split `prompt_mode` Compressor (`FIRST_FRAME` / `FIRST_AND_LAST_FRAME` vs `TEXT_TO_VIDEO`) (`packages/agent4_director`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 076`
- **Git Worktree & Branch:** `task/085-linter-rule11-split-compressor` in `../tc-wt/task-085-linter-rule11-split-compressor`
- **Owned Write Scope:** `packages/agent4_director/src/rules/rule_11_prompt_compress.py`, `packages/agent4_director/tests/test_rule_11.py`, `.agent-handoffs/task-085.md`
- **Mandatory Reference Files:** [director-and-13-laws.md](director-and-13-laws.md), [schema/pipeline.sql](schema/pipeline.sql)
- **Shared Contracts Consumed / Produced:** Canonical v4 `prompt_mode` prompt validation (`TEXT_TO_VIDEO` | `FIRST_FRAME` | `FIRST_AND_LAST_FRAME` — zero retired `FRAMES_MOTION_ONLY` or `VEO_3_1_LITE` references! `F-04`)

#### Scope And Implementation Requirements

- [ ] Enforce **`gemini-omni-1.2-flash`** motion prompt length (`15–30 words`, negative-keyword `"no"`/`"don't show"` ban) and duration bucket parity (`3s–15s` for `TEXT_TO_VIDEO`/`FIRST_FRAME`; **`3s–10s` max** for `FIRST_AND_LAST_FRAME`).
- [ ] **Mode-Specific Enforcement:**
  - When `prompt_mode IN ('FIRST_FRAME', 'FIRST_AND_LAST_FRAME')`: strictly forbid appearance/clothing/material nouns (`hooded`, `detective`, `charcoal`, `coat`, `fedora`)—allowing strictly motion verbs, pacing adverbs, and camera moves!
  - When `prompt_mode == 'TEXT_TO_VIDEO'` (null frames): permit concise stylized subject labels (`"Minimalist 2D stick figure"`).

#### Edge Cases And Failure Modes

- Prompt uses `"hooded 2D ink figure"` on a `FIRST_AND_LAST_FRAME` job: stripped cleanly to `"Figure moves steadily left-to-right down alley, smooth side tracking shot."`!

#### Bug Prevention And Invariants

- **Zero Deprecated `FRAMES_MOTION_ONLY` / `VEO_3_1_LITE` Contract Drift Invariant (`F-04`).**

#### Independent Testability & Parallel Isolation

- Pure Python mode-split word/noun checks (`$0` API calls).

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent4_director/tests/test_rule_11.py` confirming `FIRST_FRAME` / `FIRST_AND_LAST_FRAME` strip appearance words while `TEXT_TO_VIDEO` allows stylized tags.
- **Acceptance:** Canonical v4 `RULE_11` prompt compressor verified.

### Task 086: Implement `RULE_12` Split Anonymizer & Cinematography Bigram Whitelist (`packages/agent4_director`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 076`, `Task 085`
- **Git Worktree & Branch:** `task/086-linter-rule12-bigram-anonymizer` in `../tc-wt/task-086-linter-rule12-bigram-anonymizer`
- **Owned Write Scope:** `packages/agent4_director/src/rules/rule_12_anonymizer.py`, `packages/agent4_director/tests/test_rule_12.py`, `.agent-handoffs/task-086.md`
- **Mandatory Reference Files:** [director-and-13-laws.md](director-and-13-laws.md)
- **Shared Contracts Consumed / Produced:** Stage 1 Regex Scrub with **Cinematography Bigram Whitelist** + Stage 2 Split Metaphor Tables (`TEXT_TO_VIDEO` vs `FIRST_FRAME`/`FIRST_AND_LAST_FRAME`)

#### Scope And Implementation Requirements

- [ ] **Cinematography Bigram Whitelist:** Before scanning for `"shoot"` / `"shot"` / `"gun"` / `"minor"`, mask whitelisted camera bigrams (`tracking shot`, `static shot`, `dolly shot`, `wide shot`, `medium shot`, `panning shot`, `establishing shot`).
- [ ] **Two Metaphor Templates:** Compile `TEXT_TO_VIDEO` prompts using atmospheric stylized silhouettes and `FIRST_FRAME`/`FIRST_AND_LAST_FRAME` prompts using pure motion + camera verbs with zero appearance descriptors!

#### Edge Cases And Failure Modes

- `"smooth side tracking shot"` false-flagged by naive `"shot"` regex: cleared cleanly while `"suspect shot the victim"` hard-fails!

#### Bug Prevention And Invariants

- **Zero Benign Cinematography False-Positives Invariant.**

#### Independent Testability & Parallel Isolation

- Offline unit tests covering both modes.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent4_director/tests/test_rule_12.py` with 100% pass.
- **Acceptance:** Canonical `RULE_12` anonymizer verified.

### Task 087: Implement `RULE_13` Dual-Prompt Pre-Compiler (`prompt_v1` + `prompt_v2_safe`) (`packages/agent4_director`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 085`, `Task 086`
- **Git Worktree & Branch:** `task/087-linter-rule13-dual-prompt` in `../tc-wt/task-087-linter-rule13-dual-prompt`
- **Owned Write Scope:** `packages/agent4_director/src/rules/rule_13_dual_prompt.py`, `packages/agent4_director/tests/test_rule_13.py`, `.agent-handoffs/task-087.md`
- **Mandatory Reference Files:** [director-and-13-laws.md](director-and-13-laws.md)
- **Shared Contracts Consumed / Produced:** Enforces `prompt_v1` + ultra-safe environmental `prompt_v2_safe` (both honoring `prompt_mode`)

#### Scope And Implementation Requirements

- [ ] Verify both prompts pass `RULE_11` and `RULE_12`, and `prompt_v2_safe` contains strictly environmental motion (flashlight beam, rain reflections, swinging door) with zero human confrontation words.

#### Edge Cases And Failure Modes

- `prompt_v2_safe` reuses `"struggle"` or `"chase"`: rejected cleanly.

#### Bug Prevention And Invariants

- **Ultra-Safe Environmental Backup Invariant.**

#### Independent Testability & Parallel Isolation

- Pure Python dual-prompt tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent4_director/tests/test_rule_13.py` with 100% pass.
- **Acceptance:** `RULE_13` verified.

### Task 088: Implement LLM Diff-Repair Loop (`Max 3 Retries`) & Act-Aware Auto-Downgrade (`packages/agent4_director`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 076`–`087`
- **Git Worktree & Branch:** `task/088-agent4-repair-loop` in `../tc-wt/task-088-agent4-repair-loop`
- **Owned Write Scope:** `packages/agent4_director/src/compiler_loop.py`, `packages/agent4_director/tests/test_compiler_loop.py`, `.agent-handoffs/task-088.md`
- **Mandatory Reference Files:** [director-and-13-laws.md](director-and-13-laws.md)
- **Shared Contracts Consumed / Produced:** `DirectorCompiler` converging to `13/13` zero-conflict pass within `<= 3` retries

#### Scope And Implementation Requirements

- [ ] Execute `Layer 1 -> manifest_linter.py -> max 3 diff retries -> deterministic auto-downgrade`, asserting fixed-point convergence across all 13 rules (including Act 2 peak preservation and non-neighbor fallbacks!).

#### Edge Cases And Failure Modes

- Repairing `RULE_03` (`9.2s -> 6s+3.2s`) triggers neighbor check: fixed-point re-lint loop verifies all 13 rules hold simultaneously on the final output!

#### Bug Prevention And Invariants

- **Fixed-Point Multi-Rule Convergence Invariant.**

#### Independent Testability & Parallel Isolation

- Stubborn-faulty LLM mock tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent4_director/tests/test_compiler_loop.py` with 100% pass.
- **Acceptance:** Director compiler loop verified.

### Task 089: Implement 15-Second Pre-Flight 480p Animatic Renderer (`--dry-run`) (`packages/agent4_director`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 088`
- **Git Worktree & Branch:** `task/089-preflight-animatic-dryrun` in `../tc-wt/task-089-preflight-animatic-dryrun`
- **Owned Write Scope:** `packages/agent4_director/src/preflight_animatic.py`, `packages/agent4_director/tests/test_preflight_animatic.py`, `.agent-handoffs/task-089.md`
- **Mandatory Reference Files:** [director-and-13-laws.md](director-and-13-laws.md)
- **Shared Contracts Consumed / Produced:** Renders `854x480` wireframe animatic (`<= 15s` compute) stitched cleanly across segmented `VoiceTrackManifest` (`Narration + FOIA Slots + Twist Pads`)

#### Scope And Implementation Requirements

- [ ] Render one diagnostic PNG per scene showing `engine`, `credit/USD cost`, `Open Loop`, `Safe-Zone` dashed guide, and `2K zoom` box, muxed onto segmented `Narration + FOIA + TwistPad` audio in `<= 15 seconds` via FFmpeg `concat`.

#### Edge Cases And Failure Modes

- Segmented audio assembly: concatenate `Narration` WAVs + `FoiaSlot` audio + `TwistPad` WAVs into quick preview audio track before muxing.

#### Bug Prevention And Invariants

- **`<= 15s` Pre-Flight Zero-Flow-Spend Invariant.**

#### Independent Testability & Parallel Isolation

- 20-minute golden manifest benchmark test.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent4_director/tests/test_preflight_animatic.py` confirming `< 15s` runtime and 480p MP4 validity.
- **Acceptance:** Pre-flight animatic verified.

### Task 090: Agent 4 Conflict-Free 13-Law Property & Adversarial Suite (`packages/agent4_director`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 073`–`089`
- **Git Worktree & Branch:** `task/090-agent4-13-law-adversarial-suite` in `../tc-wt/task-090-agent4-13-law-adversarial-suite`
- **Owned Write Scope:** `packages/agent4_director/src/pipeline.py`, `packages/agent4_director/tests/test_agent4_13_laws.py`, `.agent-handoffs/task-090.md`
- **Mandatory Reference Files:** [director-and-13-laws.md](director-and-13-laws.md)
- **Shared Contracts Consumed / Produced:** Certifies `Agent4DirectorService` across all 13 Laws and all previously-colliding rule pairs

#### Scope And Implementation Requirements

- [ ] Test every individual law (`RULE_01`–`RULE_13`) PLUS every audited collision pair (`RULE_01` + 4m FOIA, `RULE_11` + `RULE_12`, `RULE_03` `9.2s` + `RULE_07`, `RULE_02` + `RULE_06`, `RULE_04` + `RULE_05`, `CaseBoardSpine` mid-911 boundary snap).

#### Edge Cases And Failure Modes

- Simultaneous `RULE_02` overrun + `9.2s` beat + `"tracking shot"` in same manifest: fixed-point compiler resolves all cleanly!

#### Bug Prevention And Invariants

- **Zero Inter-Rule Collision Invariant.**

#### Independent Testability & Parallel Isolation

- 100% standalone test suite inside `packages/agent4_director`.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/agent4_director` with 100% pass.
- **Acceptance:** Agent 4 certified conflict-free across all 13 laws.

---

### Task 091: Define `RenderBackendPort` Interface Seam (`Part 1 -> Part 2`) (`packages/orchestrator`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 002`, `Task 090`
- **Git Worktree & Branch:** `task/091-render-backend-port` in `../tc-wt/task-091-render-backend-port`
- **Owned Write Scope:** `packages/orchestrator/src/render_port.py`, `packages/orchestrator/tests/test_render_port.py`, `.agent-handoffs/task-091.md`
- **Mandatory Reference Files:** [parallel-part1-part2-architecture.md](parallel-part1-part2-architecture.md)
- **Shared Contracts Consumed / Produced:** `RenderBackendPort` covering both MVP 4-motif Vertical Slice and full 12-motif execution

#### Scope And Implementation Requirements

- [ ] Define `RenderBackendPort` (`render_code_scene`, `render_2k_panzoom`, `generate_flow_keyframes`, `dispatch_flow_jobs`, `assemble_master`), keeping zero direct imports of Part 2 packages.

#### Edge Cases And Failure Modes

- Accidental Part 2 import: static AST import check enforces strict dependency inversion.

#### Bug Prevention And Invariants

- **Strict Port-Adapter Separation Invariant.**

#### Independent Testability & Parallel Isolation

- Static import + contract mock tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/orchestrator/tests/test_render_port.py` with 100% pass.
- **Acceptance:** `RenderBackendPort` verified.

### Task 092: Implement `RenderBackendStub` For Standalone Part 1 & Vertical Slice Testing (`packages/orchestrator`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 011`, `Task 091`
- **Git Worktree & Branch:** `task/092-render-backend-stub` in `../tc-wt/task-092-render-backend-stub`
- **Owned Write Scope:** `packages/orchestrator/src/render_stub.py`, `packages/orchestrator/tests/test_render_stub.py`, `.agent-handoffs/task-092.md`
- **Mandatory Reference Files:** [parallel-part1-part2-architecture.md](parallel-part1-part2-architecture.md)
- **Shared Contracts Consumed / Produced:** `RenderBackendStub` exercising real SQLite triggers & simulating both Headless API and optional Batch Desk modes

#### Scope And Implementation Requirements

- [ ] Validate all `ProductionManifest`, `TimelineSpec`, `CaseBible`, `ScenePlan`, and segmented `VoiceTrackManifest` payloads via Pydantic `extra="forbid"`, run real `FlowJobRepository` 2-strike transitions (including `$0` released reservation simulation in `GEMINI_OMNI_INTERACTIONS` mode!), and produce deterministic stub outputs at **$0.00 spend (`OFFLINE_TEST`)**.

#### Edge Cases And Failure Modes

- Stub bypassing `24h+5m` lock check in `HUMAN_BATCH_DESK` simulation: enforce real `AccountPoolLedger` timing checks!

#### Bug Prevention And Invariants

- **Real Trigger & Ledger Coverage Invariant.**

#### Independent Testability & Parallel Isolation

- Standalone inside Developer A's workspace.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/orchestrator/tests/test_render_stub.py` with 100% pass.
- **Acceptance:** `RenderBackendStub` verified.

### Task 093: Implement Headless-Default Conveyor Scheduler (`Up to 3` Parked Episodes) (`packages/orchestrator`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 012`, `Task 092`
- **Git Worktree & Branch:** `task/093-headless-default-conveyor` in `../tc-wt/task-093-headless-default-conveyor`
- **Owned Write Scope:** `packages/orchestrator/src/conveyor_scheduler.py`, `packages/orchestrator/tests/test_conveyor_scheduler.py`, `.agent-handoffs/task-093.md`
- **Mandatory Reference Files:** [flow-hybrid-and-batch-desk.md](flow-hybrid-and-batch-desk.md), [database-and-state-design.md](database-and-state-design.md)
- **Shared Contracts Consumed / Produced:** `ConveyorScheduler` supporting **`GEMINI_OMNI_INTERACTIONS`** default, staggered **`Plan -> Voice -> Create -> Edit`** checkpoints (`SCENE_PLAN_APPROVED` -> `ANIMATIC_APPROVED`), AND up to `3` FIFO episodes in `AWAITING_FLOW_BATCH` for optional `HUMAN_BATCH_DESK`

#### Scope And Implementation Requirements

- [ ] Under default `GEMINI_OMNI_INTERACTIONS` mode: run Scout -> Evidence+2K -> Compliance -> **Stage 1 `ScenePlan` Approval -> Stage 2 Voice + WhisperX + Animatic Approval** -> Render -> Mastering continuously without manual account-clicking waits!
- [ ] Under optional `HUMAN_BATCH_DESK` mode: allow up to `3` episodes parked cleanly in `AWAITING_FLOW_BATCH` (FIFO oldest-first drain) so a 3-day 15-clip episode NEVER blocks `Ep N+2` compute!

#### Edge Cases And Failure Modes

- 3-day multi-shift episode blocking `Ep N+2`: multi-slot (`<= 3`) queue keeps compute saturated while preventing stale queue overflow!

#### Bug Prevention And Invariants

- **Zero Deadlock & Non-Stalling Queue Invariant.**

#### Independent Testability & Parallel Isolation

- Simulated multi-day clock tests across both backend modes.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/orchestrator/tests/test_conveyor_scheduler.py` passing both Headless 24/7 and 3-slot Batch Desk simulations.
- **Acceptance:** Non-deadlocking conveyor scheduler verified.

### Task 094: Implement Off-Peak DeepSeek Batch Window Scheduler (`providers.yaml`) (`packages/orchestrator`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 014`, `Task 093`
- **Git Worktree & Branch:** `task/094-offpeak-deepseek-scheduler` in `../tc-wt/task-094-offpeak-deepseek-scheduler`
- **Owned Write Scope:** `packages/orchestrator/src/offpeak_scheduler.py`, `packages/orchestrator/tests/test_offpeak_scheduler.py`, `.agent-handoffs/task-094.md`
- **Mandatory Reference Files:** [economics-and-credit-math.md](economics-and-credit-math.md)
- **Shared Contracts Consumed / Produced:** Routes heavy non-urgent LLM batches into DeepSeek 50%-off off-peak UTC windows configured in `providers.yaml`

#### Scope And Implementation Requirements

- [ ] Schedule heavy Agent 2 & Agent 4 runs into configured off-peak UTC windows (`max_wait_hours` configurable, `--force-peak` override for immediate runs).

#### Edge Cases And Failure Modes

- Urgent MVP vertical slice run delayed 6 hours waiting for off-peak: default `--force-peak` for single-episode runs, off-peak scheduling for background `Ep N+2` pre-staging!

#### Bug Prevention And Invariants

- **Config-Driven Off-Peak Window Invariant.**

#### Independent Testability & Parallel Isolation

- Fake UTC clock tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/orchestrator/tests/test_offpeak_scheduler.py` with 100% pass.
- **Acceptance:** Off-peak scheduler verified.

### Task 095: Implement Flow Dispatch & Optional `AWAITING_FLOW_BATCH` Parker (`packages/orchestrator`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 009`, `Task 011`, `Task 093`
- **Git Worktree & Branch:** `task/095-flow-dispatch-parker` in `../tc-wt/task-095-flow-dispatch-parker`
- **Owned Write Scope:** `packages/orchestrator/src/flow_batch_parker.py`, `packages/orchestrator/tests/test_flow_batch_parker.py`, `.agent-handoffs/task-095.md`
- **Mandatory Reference Files:** [flow-hybrid-and-batch-desk.md](flow-hybrid-and-batch-desk.md)
- **Shared Contracts Consumed / Produced:** Dispatches `flow_jobs` directly to `GeminiOmniInteractionsBackend` OR parks silently in `AWAITING_FLOW_BATCH` with `24h+5m` reset awareness

#### Scope And Implementation Requirements

- [ ] Create `flow_jobs` rows (`UNIQUE(episode_id, scene_id)`, `idempotency_key`, `prompt_mode`, `prompt_v1`, `prompt_v2_safe`, non-neighbor `fallback_spec`) and dispatch via `RenderBackendPort.dispatch_flow_jobs()` (`GEMINI_OMNI_INTERACTIONS` / `VERTEX_VEO_ENTERPRISE`) or queue by account (`HUMAN_BATCH_DESK`).

#### Edge Cases And Failure Modes

- `GEMINI_OMNI_INTERACTIONS` mode accidentally waiting for human shift: immediate dispatch skips manual account tabs!

#### Bug Prevention And Invariants

- **Zero Unnecessary Wait in Headless Mode Invariant.**

#### Independent Testability & Parallel Isolation

- Unit tested across both backend modes.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/orchestrator/tests/test_flow_batch_parker.py` with 100% pass.
- **Acceptance:** Flow dispatcher & optional parker verified.

### Task 096: Implement Per-Shift Saturation Watcher & Post-Flow Overnight Trigger (`packages/orchestrator`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 031`, `Task 095`
- **Git Worktree & Branch:** `task/096-post-flow-watcher` in `../tc-wt/task-096-post-flow-watcher`
- **Owned Write Scope:** `packages/orchestrator/src/post_flow_watcher.py`, `packages/orchestrator/tests/test_post_flow_watcher.py`, `.agent-handoffs/task-096.md`
- **Mandatory Reference Files:** [flow-hybrid-and-batch-desk.md](flow-hybrid-and-batch-desk.md), [scout-and-saturation.md](scout-and-saturation.md)
- **Shared Contracts Consumed / Produced:** Executes daily Pre-Shift Re-Check (with `>50%` sunk-cost guard) AND atomic `POST_FLOW_PROCESSING` wakeup

#### Scope And Implementation Requirements

- [ ] Re-run `PreRenderSaturationGate` before each day's Flow spend (respecting `>50%` sunk-cost completion threshold) and transition episode to `POST_FLOW_PROCESSING` once all `flow_jobs` are terminal (`ACCEPTED` / `SWITCHED_TO_FALLBACK`).

#### Edge Cases And Failure Modes

- Multi-day episode hits viral wave on Day 2 at 20% spent -> cleanly aborted before burning the remaining 80%.

#### Bug Prevention And Invariants

- **Single-Fire Overnight Wakeup Invariant.**

#### Independent Testability & Parallel Isolation

- Simulated multi-day drop & abort tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/orchestrator/tests/test_post_flow_watcher.py` with 100% pass.
- **Acceptance:** Per-shift watcher verified.

### Task 097: Implement Orchestrator CLI & Headless Conveyor Daemon (`packages/orchestrator`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 093`–`096`
- **Git Worktree & Branch:** `task/097-orchestrator-cli-daemon` in `../tc-wt/task-097-orchestrator-cli-daemon`
- **Owned Write Scope:** `packages/orchestrator/src/cli.py`, `packages/orchestrator/src/daemon.py`, `packages/orchestrator/tests/test_cli_daemon.py`, `.agent-handoffs/task-097.md`
- **Mandatory Reference Files:** [flow-hybrid-and-batch-desk.md](flow-hybrid-and-batch-desk.md)
- **Shared Contracts Consumed / Produced:** `tc-conveyor` CLI (`--backend=stub|live`, `--flow-mode=headless|batch-desk`, `--mvp-slice`, `--dry-run`, `--daemon`)

#### Scope And Implementation Requirements

- [ ] Provide CLI subcommands including `--mvp-slice` mode (running minimal 4-motif Vertical Slice fast!), exclusive `pipeline.db.lock` file lock, and clean `SIGTERM` WAL truncation.

#### Edge Cases And Failure Modes

- Duplicate daemon launch: OS file lock aborts cleanly.

#### Bug Prevention And Invariants

- **Single-Instance Daemon Lock Invariant.**

#### Independent Testability & Parallel Isolation

- CLI smoke tests against temp SQLite DB.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/orchestrator/tests/test_cli_daemon.py` with 100% pass.
- **Acceptance:** Orchestrator CLI & daemon verified.

### Task 098: Implement Multi-Provider Global Budget & `OFFLINE_TEST` Zero-Spend Guardrails (`packages/orchestrator`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 014`, `Task 097`
- **Git Worktree & Branch:** `task/098-budget-quota-guardrails` in `../tc-wt/task-098-budget-quota-guardrails`
- **Owned Write Scope:** `packages/orchestrator/src/budget_guardrails.py`, `packages/orchestrator/tests/test_budget_guardrails.py`, `.agent-handoffs/task-098.md`
- **Mandatory Reference Files:** [economics-and-credit-math.md](economics-and-credit-math.md), [schema/pipeline.sql](schema/pipeline.sql)
- **Shared Contracts Consumed / Produced:** Enforces transactional **`$135/mo` `ALL_PROVIDERS` global cap**, per-provider sub-caps (incl. `$38/mo` `0%`-cache DeepSeek cap), `$10.40/ep` `gemini_omni` cap (`<= 10` clips / `80s`), and **`OFFLINE_TEST == $0.00`** trigger (`F-01`, `F-02`)

#### Scope And Implementation Requirements

- [ ] Execute every paid provider reservation via `provider_spend_reservations` inside authoritative `pipeline.db` (NEVER reading lagging `telemetry.db` for budget admission!).
- [ ] Enforce BOTH `0%`-cache worst-case DeepSeek projections (`~$2.80–$3.80/ep`) AND `gemini-omni-1.2-flash` (`$8.00` base / `$10.40` hard cap/ep), halting runaway retries cleanly before breaching global `$135/mo` `ALL_PROVIDERS` cap!

#### Edge Cases And Failure Modes

- DeepSeek batch + Gemini Omni clip hitting `$135/mo` simultaneously OR an ordinary test trying to reserve `$0.01`: `trg_provider_global_budget_cap_guard` / `trg_offline_test_zero_spend_guard` aborts atomically (`0` unbudgeted spend).

#### Bug Prevention And Invariants

- **Hard Per-Episode Spend Circuit Breaker Invariant.**

#### Independent Testability & Parallel Isolation

- Simulated spend spike tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/orchestrator/tests/test_budget_guardrails.py` with 100% pass.
- **Acceptance:** Budget guardrails verified.

### Task 099: Part 1 Fault-Injection, 30-Day ToS Purge & Crash-Recovery Soak Tests (`packages/orchestrator`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 091`–`098`
- **Git Worktree & Branch:** `task/099-part1-fault-injection` in `../tc-wt/task-099-part1-fault-injection`
- **Owned Write Scope:** `packages/orchestrator/tests/test_part1_fault_injection.py`, `.agent-handoffs/task-099.md`
- **Mandatory Reference Files:** [architecture-review-decisions.md](architecture-review-decisions.md)
- **Shared Contracts Consumed / Produced:** Proves crash-safe idempotency across all Part 1 transitions + 30-day ToS purge

#### Scope And Implementation Requirements

- [ ] Inject crashes mid-dispatch (`SUBMITTING`/`RUNNING` -> reconciled via `UNKNOWN_RECONCILE` & `budget_reservations`), 429 backoffs, adverse `UPDATE` `REVERSED` disposition flips (`trg_case_disposition_quarantine` auto-quarantining active episodes & revoking approvals, `F-03`), Day-2 copycat aborts, and full 30-day YouTube API field purges (`F-20`), asserting **0 duplicate `(episode_id, scene_id)` paid `flow_jobs`** (`F-10`).

#### Edge Cases And Failure Modes

- Crash after early 2K anchor lock before scripting: resumes cleanly at `EVIDENCE_AND_2K_LOCKED` without regenerating 2K images!

#### Bug Prevention And Invariants

- **Idempotent Checkpoint Recovery Invariant.**

#### Independent Testability & Parallel Isolation

- Standalone inside Developer A's workspace.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `uv run pytest packages/orchestrator/tests/test_part1_fault_injection.py` with 100% pass.
- **Acceptance:** Part 1 fault tolerance verified.

### Task 100: Part 1 Standalone End-to-End Certification Gate (`packages/orchestrator`)

- **Track & Owner:** `Part 1 · Developer A`
- **Milestone:** `M2-P1 · Segmented Voice-First, 13-Law Director & Conveyor`
- **Depends On:** `Task 032`, `Task 044`, `Task 060`, `Task 072`, `Task 090`, `Task 099`
- **Git Worktree & Branch:** `task/100-part1-standalone-certification` in `../tc-wt/task-100-part1-standalone-certification`
- **Owned Write Scope:** `packages/orchestrator/tests/test_part1_standalone_e2e.py`, `packages/orchestrator/PART1_CERT_REPORT.md`, `.agent-handoffs/task-100.md`
- **Mandatory Reference Files:** [parallel-part1-part2-architecture.md](parallel-part1-part2-architecture.md), [roadmap.md](roadmap.md)
- **Shared Contracts Consumed / Produced:** Certifies complete **Part 1 (Developer A)** independent readiness using `RenderBackendStub`

#### Scope And Implementation Requirements

- [ ] Execute full 3-episode offline run (`GEMINI_OMNI_INTERACTIONS` transport mock + `HUMAN_BATCH_DESK` check, **`$0.00` API spend, outbound sockets blocked**) inside Developer A's workspace: Scout -> Disposition + Quarantine -> Explicitly `APPROVED` Anonymization + Early Illustrative 2K Anchors -> Component Rights + Music-Gated Demucs -> **`ScenePlan` Stage 1 Approval -> WhisperX Word Alignment** -> 13-Law `manifest_linter.py` (`<= 10` clips / `80s`) -> `RenderBackendStub` completion, validating 100% Zod parity!

#### Edge Cases And Failure Modes

- Any Part 1 JSON failing TypeScript Zod validation: caught immediately by Task 100 cross-language parity gate.

#### Bug Prevention And Invariants

- **100% Part 2 Contract Compatibility Invariant.**

#### Independent Testability & Parallel Isolation

- Zero dependency on Part 2 code.

#### Verification, Testing And Acceptance Criteria

- [ ] Run full Part 1 suite (`uv run pytest packages/db packages/agent1_scout packages/agent2_evidence packages/agent3_gatekeeper packages/voice_sync packages/agent4_director packages/orchestrator`) with 100% pass and emit `PART1_CERT_REPORT.md`.
- **Acceptance:** Part 1 (Developer A) certified independently and ready for Vertical Slice & Merge!

---

### PART 2 — Developer B: Visual Synthesis, 2K Cubic Renderer, Mastering, Analytics & Optional UI (`Tasks 101`–`192`)

### Task 101: Bootstrap Remotion `30 fps` Workspace, Zod Parser & CSS Layout Safe-Zone Frame (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M1-P2 · Core 4-Motif Vertical Slice & 2K Cubic Engine`
- **Depends On:** `Task 002`, `Task 004`
- **Git Worktree & Branch:** `task/101-remotion-30fps-css-safezone` in `../tc-wt/task-101-remotion-30fps-css-safezone`
- **Owned Write Scope:** `packages/render_catalog/src/index.ts`, `packages/render_catalog/src/parser.ts`, `packages/render_catalog/src/safe_zone.tsx`, `packages/render_catalog/tests/parser.test.ts`, `.agent-handoffs/task-101.md`
- **Mandatory Reference Files:** [code-animation-catalog.md](code-animation-catalog.md), [director-and-13-laws.md](director-and-13-laws.md)
- **Shared Contracts Consumed / Produced:** Locks output container strictly to **`1920x1080 @ 30 fps`** and enforces YouTube exclusion zones via **CSS layout containment**

#### Scope And Implementation Requirements

- [ ] Configure Remotion root strictly at `1920x1080 @ 30 fps` (eliminating pointless `60 fps` renders for `6 fps` line-boil animation).
- [ ] Implement `<SafeZoneLayout isEndScreen={...}>` CSS Flexbox/Grid container enforcing `paddingBottom: 194px` (`18%`), `paddingTop: 108px` (`10%`), bottom-right `22% x 14%` exclusion box, and final-20s end-screen card masks cleanly across arbitrary text wraps!

#### Edge Cases And Failure Modes

- Long dynamic label wrapping to 3 lines inside `<SafeZoneLayout>`: CSS `overflow: hidden` + `maxHeight` + responsive clamp prevents bleeding into YouTube's caption bar!

#### Bug Prevention And Invariants

- **CSS-Enforced Safe-Zone Containment Invariant.**

#### Independent Testability & Parallel Isolation

- Standalone Zod + React layout tests on `ep_golden_01_20min`.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- parser` with 100% pass.
- **Acceptance:** `30 fps` Remotion workspace & CSS Safe-Zone verified.

### Task 102: Implement `CaseBible` Style DNA React Theme Provider (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M1-P2 · Core 4-Motif Vertical Slice & 2K Cubic Engine`
- **Depends On:** `Task 101`
- **Git Worktree & Branch:** `task/102-case-bible-theme-provider` in `../tc-wt/task-102-case-bible-theme-provider`
- **Owned Write Scope:** `packages/render_catalog/src/theme/CaseBibleContext.tsx`, `packages/render_catalog/tests/theme.test.tsx`, `.agent-handoffs/task-102.md`
- **Mandatory Reference Files:** [code-animation-catalog.md](code-animation-catalog.md)
- **Shared Contracts Consumed / Produced:** `useCaseBible()` distributing locked hex palette & character props

#### Scope And Implementation Requirements

- [ ] Distribute `CaseBible` palette and character prop definitions cleanly, rejecting unregistered `characterId`s and checking contrast >= `3.5:1`.

#### Edge Cases And Failure Modes

- Missing character entry: explicit render-time error.

#### Bug Prevention And Invariants

- **Zero Hardcoded Palette Drift Invariant.**

#### Independent Testability & Parallel Isolation

- React unit tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- theme` with 100% pass.
- **Acceptance:** `CaseBible` theme provider verified.

### Task 103: Implement Fast `6 fps` Deterministic JS Polyline Vertex-Jitter Line Boil (Replacing SVG `<feTurbulence>`) (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M1-P2 · Core 4-Motif Vertical Slice & 2K Cubic Engine`
- **Depends On:** `Task 102`
- **Git Worktree & Branch:** `task/103-fast-js-6fps-line-boil` in `../tc-wt/task-103-fast-js-6fps-line-boil`
- **Owned Write Scope:** `packages/render_catalog/src/rig/LineBoilPath.tsx`, `packages/render_catalog/tests/line_boil.test.tsx`, `.agent-handoffs/task-103.md`
- **Mandatory Reference Files:** [code-animation-catalog.md](code-animation-catalog.md), [research/remotion-json-catalog-and-2k-grid.md](research/remotion-json-catalog-and-2k-grid.md)
- **Shared Contracts Consumed / Produced:** **Eliminates 5–15 hr SVG `<feTurbulence>` bottleneck!** Pure JS deterministic `6 fps` stroke vertex perturbation (`50x` faster in headless Chromium)

#### Scope And Implementation Requirements

- [ ] **Ban SVG `<feTurbulence>` & `<feDisplacementMap>` completely** (which stall Chromium at `1–3s/frame` at `1080p`!).
- [ ] Implement `<BoilPath points={...} seed={...}>` subdividing SVG polylines/curves and applying deterministic Mulberry32 PRNG normal-vector jitter (`+/- 1.4 px`) quantized to **`6 fps` ticks (`Math.floor(frame / 5)` at `30 fps`)**—rendering pure crisp `<path>` nodes in `< 0.5 ms` per frame!

#### Edge Cases And Failure Modes

- Closed loop seam drifting between start point and end point: share identical PRNG vertex perturbation for `point[0]` and `point[N-1]` on closed paths (`closed=true`).

#### Bug Prevention And Invariants

- **Zero SVG Filter Bottleneck & Bit-Deterministic `6 fps` Boil Invariant.**

#### Independent Testability & Parallel Isolation

- Benchmarks frame render speed (`< 2 ms/frame`) + snapshot determinism.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- line_boil` confirming zero `<feTurbulence>` nodes in DOM and fast deterministic `6 fps` ticks.
- **Acceptance:** Fast JS 6 fps line-boil engine verified.

### Task 104: Implement Parametric `StickFigure` Core Geometry Rig (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M1-P2 · Core 4-Motif Vertical Slice & 2K Cubic Engine`
- **Depends On:** `Task 103`
- **Git Worktree & Branch:** `task/104-stick-figure-core-rig` in `../tc-wt/task-104-stick-figure-core-rig`
- **Owned Write Scope:** `packages/render_catalog/src/rig/StickFigureGeometry.tsx`, `packages/render_catalog/tests/stick_geometry.test.tsx`, `.agent-handoffs/task-104.md`
- **Mandatory Reference Files:** [code-animation-catalog.md](code-animation-catalog.md)
- **Shared Contracts Consumed / Produced:** Parametric stickman skeletal geometry rendered via `<BoilPath>`

#### Scope And Implementation Requirements

- [ ] Render locked bone ratios (`headRadius`, `torsoLen`, `upperArm`, `forearm`, `thigh`, `shin`) via `<BoilPath>` with prop attachment sockets inside CSS Safe-Zone bounds.

#### Edge Cases And Failure Modes

- Scale pushing head into top 10% or bottom 18%: clamped inside `SafeZoneLayout`.

#### Bug Prevention And Invariants

- **Locked Bone-Length Invariant.**

#### Independent Testability & Parallel Isolation

- Property tests across 100 random joint configurations.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- stick_geometry` with 100% pass.
- **Acceptance:** Parametric `StickFigure` rig verified.

### Task 105: Implement `StickFigure` Silhouette Prop Library (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M1-P2 · Core 4-Motif Vertical Slice & 2K Cubic Engine`
- **Depends On:** `Task 104`
- **Git Worktree & Branch:** `task/105-stick-figure-prop-library` in `../tc-wt/task-105-stick-figure-prop-library`
- **Owned Write Scope:** `packages/render_catalog/src/rig/StickProps.tsx`, `packages/render_catalog/tests/stick_props.test.tsx`, `.agent-handoffs/task-105.md`
- **Mandatory Reference Files:** [code-animation-catalog.md](code-animation-catalog.md)
- **Shared Contracts Consumed / Produced:** `<BoilPath>` vector props (`fedora`, `hoodie`, `badge`, `glasses`, `tie`, `scarf`, `briefcase`, `flashlight`, `phone`, `document`)

#### Scope And Implementation Requirements

- [ ] Implement crisp `<BoilPath>` overlays anchored to `StickFigure` sockets with clean left/right facing mirroring.

#### Edge Cases And Failure Modes

- Mirrored facing flipping asymmetric badge/brim: symmetric transform wrapper around torso X-axis.

#### Bug Prevention And Invariants

- **Silhouette Readability Invariant.**

#### Independent Testability & Parallel Isolation

- SVG snapshot tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- stick_props` with 100% pass.
- **Acceptance:** Prop library verified.

### Task 106: Implement `StickFigure` 14-Pose Choreography State Machine (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M1-P2 · Core 4-Motif Vertical Slice & 2K Cubic Engine`
- **Depends On:** `Task 105`
- **Git Worktree & Branch:** `task/106-stick-figure-14-poses` in `../tc-wt/task-106-stick-figure-14-poses`
- **Owned Write Scope:** `packages/render_catalog/src/rig/StickPoses.ts`, `packages/render_catalog/tests/stick_poses.test.tsx`, `.agent-handoffs/task-106.md`
- **Mandatory Reference Files:** [code-animation-catalog.md](code-animation-catalog.md)
- **Shared Contracts Consumed / Produced:** Exhaustive 14-pose solver with 300ms cubic transitions

#### Scope And Implementation Requirements

- [ ] Implement all 14 enum-locked poses (`idle` through `slumped`), syncing `walk_loop`/`run_loop` stride velocity to `travel_axis` motion.

#### Edge Cases And Failure Modes

- Pose transition pop: smooth 300ms angle interpolation.

#### Bug Prevention And Invariants

- **14/14 Exhaustive Pose Coverage Invariant.**

#### Independent Testability & Parallel Isolation

- All 14x14 transition tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- stick_poses` with 100% pass.
- **Acceptance:** 14-pose choreography engine verified.

### Task 107: Implement `StickFigure` 10-Emotion Facial & Posture Rig (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M1-P2 · Core 4-Motif Vertical Slice & 2K Cubic Engine`
- **Depends On:** `Task 106`
- **Git Worktree & Branch:** `task/107-stick-figure-10-emotions` in `../tc-wt/task-107-stick-figure-10-emotions`
- **Owned Write Scope:** `packages/render_catalog/src/rig/StickEmotions.tsx`, `packages/render_catalog/tests/stick_emotions.test.tsx`, `.agent-handoffs/task-107.md`
- **Mandatory Reference Files:** [code-animation-catalog.md](code-animation-catalog.md)
- **Shared Contracts Consumed / Produced:** All 10 emotion expressions + deterministic blink cycles

#### Scope And Implementation Requirements

- [ ] Implement all 10 enum-locked emotions (`neutral` through `guilty`) with deterministic 3.5s blinks and scale-aware simplification.

#### Edge Cases And Failure Modes

- Distant character `< 0.45` scale: simplify brow/mouth detail cleanly.

#### Bug Prevention And Invariants

- **10/10 Exhaustive Emotion Coverage Invariant.**

#### Independent Testability & Parallel Isolation

- Snapshot tests across all 10 emotions.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- stick_emotions` with 100% pass.
- **Acceptance:** 10-emotion rig verified.

### Task 108: Implement TTS RMS Amplitude-Driven Head-Nod & Gesture Sync (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M1-P2 · Core 4-Motif Vertical Slice & 2K Cubic Engine`
- **Depends On:** `Task 106`, `Task 107`
- **Git Worktree & Branch:** `task/108-amplitude-nod-sync` in `../tc-wt/task-108-amplitude-nod-sync`
- **Owned Write Scope:** `packages/render_catalog/src/rig/useVoiceSyncMotion.ts`, `packages/render_catalog/tests/voice_sync_motion.test.tsx`, `.agent-handoffs/task-108.md`
- **Mandatory Reference Files:** [code-animation-catalog.md](code-animation-catalog.md), [voice-first-and-asr-sync.md](voice-first-and-asr-sync.md)
- **Shared Contracts Consumed / Produced:** Reads segmented `VoiceTrackManifest.amplitude_envelope[]` (`30 fps`)

#### Scope And Implementation Requirements

- [ ] Drive subtle nod pitch and gesture bounce from `amplitude_envelope[frame]`, locking flat `0.0` during room-tone `TWIST_PAD`s and `FOIA_AUDIO_SLOT`s!

#### Edge Cases And Failure Modes

- Out-of-bounds frame rounding: clamp cleanly to `0.0`.

#### Bug Prevention And Invariants

- **Zero Motion During Silence Pads Invariant.**

#### Independent Testability & Parallel Isolation

- Tested on v2 golden segmented `VoiceTrackManifest`.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- voice_sync_motion` with 100% pass.
- **Acceptance:** Amplitude nod sync verified.

### Task 109: Remove Double-Grading From Remotion (Emit `needs_grade` Metadata For Single Agent 6 Pass) (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M1-P2 · Core 4-Motif Vertical Slice & 2K Cubic Engine`
- **Depends On:** `Task 102`
- **Git Worktree & Branch:** `task/109-single-pass-grade-metadata` in `../tc-wt/task-109-single-pass-grade-metadata`
- **Owned Write Scope:** `packages/render_catalog/src/grade/GradeContract.tsx`, `packages/render_catalog/tests/grade.test.tsx`, `.agent-handoffs/task-109.md`
- **Mandatory Reference Files:** [code-animation-catalog.md](code-animation-catalog.md), [mastering-loudness-and-qa.md](mastering-loudness-and-qa.md)
- **Shared Contracts Consumed / Produced:** **Fixes the Double-Grading Bug!** Remotion renders clean un-grained RGB frames and exports `scene_grade_manifest.json` (`apply_grade: true` for Code/2K/Flow vs `false` for `FOIA_REAL_FOOTAGE`) so **Agent 6 applies ONE continuous paper-grain + vignette pass** across the entire timeline!

#### Scope And Implementation Requirements

- [ ] Ensure Remotion applies **zero** paper grain or vignette overlays (preventing both Chromium filter overhead AND grain doubling/resetting across scene cuts!).
- [ ] Export `scene_grade_manifest.json` tagging `FOIA_REAL_FOOTAGE` as `apply_grade: false` and all stylized scenes as `apply_grade: true` for Agent 6's unified single-pass compositor (`Task 168`).

#### Edge Cases And Failure Modes

- `FoiaFootageFrame` containing stylized PiP narrator border + raw bodycam inset: keep bodycam inset un-grained (`apply_grade: false` or masked inset rect!).

#### Bug Prevention And Invariants

- **Zero Double-Grading & Continuous Temporal Grain Invariant:** Grain never doubles up or resets frame-phase across scene cuts.

#### Independent Testability & Parallel Isolation

- Pixel noise-floor test verifying Remotion outputs flat un-grained background RGB matching `CaseBible.paperBgHex` exactly!

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- grade` confirming pure un-grained Remotion background and accurate `scene_grade_manifest.json`.
- **Acceptance:** Single-grade contract verified cleanly.

### Task 110: Implement Built-In Micro-SFX Trigger Dispatcher (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M1-P2 · Core 4-Motif Vertical Slice & 2K Cubic Engine`
- **Depends On:** `Task 101`
- **Git Worktree & Branch:** `task/110-micro-sfx-dispatcher` in `../tc-wt/task-110-micro-sfx-dispatcher`
- **Owned Write Scope:** `packages/render_catalog/src/sfx/SfxRegistry.ts`, `packages/render_catalog/tests/sfx.test.ts`, `.agent-handoffs/task-110.md`
- **Mandatory Reference Files:** [code-animation-catalog.md](code-animation-catalog.md)
- **Shared Contracts Consumed / Produced:** Emits `MicroSfxCue[]` JSON with 60ms burst cooldowns

#### Scope And Implementation Requirements

- [ ] Emit sample-accurate `MicroSfxCue` timestamps (`typing_tap`, `highlighter_glide`, `camera_shutter`, `pin_thud`, `conflict_stamp`, `tick_sfx`, `radio_squelch`, `tape_click`) for Agent 6 mixing.

#### Edge Cases And Failure Modes

- Rapid burst > 12 cues/sec: 60ms cooldown + gain taper prevents `-1.0 dBTP` clipping.

#### Bug Prevention And Invariants

- **Deterministic SFX Cue Export Invariant.**

#### Independent Testability & Parallel Isolation

- Pure TypeScript unit tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- sfx` with 100% pass.
- **Acceptance:** Micro-SFX dispatcher verified.

### Task 111: Implement CSS-Contained Kinetic Callouts & Safe Subtitles (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M1-P2 · Core 4-Motif Vertical Slice & 2K Cubic Engine`
- **Depends On:** `Task 102`, `Task 108`
- **Git Worktree & Branch:** `task/111-kinetic-callout-subtitles` in `../tc-wt/task-111-kinetic-callout-subtitles`
- **Owned Write Scope:** `packages/render_catalog/src/typography/SafeCallout.tsx`, `packages/render_catalog/tests/safe_callout.test.tsx`, `.agent-handoffs/task-111.md`
- **Mandatory Reference Files:** [director-and-13-laws.md](director-and-13-laws.md), [code-animation-catalog.md](code-animation-catalog.md)
- **Shared Contracts Consumed / Produced:** CSS-contained `<= 12`-word callouts synced to global `WordTimestamp[]`

#### Scope And Implementation Requirements

- [ ] Render word-highlighted callouts inside `<SafeZoneLayout>` with greedy Y-slot de-confliction (`+/- 64 px`) and `<= 12`-word runtime clamp.

#### Edge Cases And Failure Modes

- Overlapping callout slots: Y-slot de-conflicter separates vertically inside Safe-Zone.

#### Bug Prevention And Invariants

- **Zero Overlapping Labels & CSS Safe-Zone Invariant.**

#### Independent Testability & Parallel Isolation

- React + bounding-box tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- safe_callout` with 100% pass.
- **Acceptance:** Kinetic Safe-Zone callouts verified.

### Task 112: Implement Headless Remotion `30 fps` Worker Pool & `<5s` Local Re-Render Cache (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M1-P2 · Core 4-Motif Vertical Slice & 2K Cubic Engine`
- **Depends On:** `Task 101`, `Task 103`, `Task 109`
- **Git Worktree & Branch:** `task/112-remotion-worker-pool-cache` in `../tc-wt/task-112-remotion-worker-pool-cache`
- **Owned Write Scope:** `packages/render_catalog/src/renderer/RenderPool.ts`, `packages/render_catalog/tests/render_pool.test.ts`, `.agent-handoffs/task-112.md`
- **Mandatory Reference Files:** [code-animation-catalog.md](code-animation-catalog.md)
- **Shared Contracts Consumed / Produced:** Renders `1080p30` scenes using fast JS line boil in `< 5s` per scene edit (`SHA-256` cache keyed)

#### Scope And Implementation Requirements

- [ ] Bundle Remotion once, cache scene MP4s by `SHA-256(canonical_scene_json + case_bible_hash)`, and render changed scenes with JS 6 fps boil (`no SVG turbulence`) genuinely under `< 5 seconds`!

#### Edge Cases And Failure Modes

- Interrupted render leaving `.tmp.mp4`: atomic `FFprobe` verify -> rename.

#### Bug Prevention And Invariants

- **Real `< 5s` Single-Scene Re-Render Invariant.**

#### Independent Testability & Parallel Isolation

- Headless render benchmark on golden scene.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- render_pool` confirming `< 5s` single-scene re-render.
- **Acceptance:** Fast Remotion worker pool verified.

### Task 113: Implement Visual Regression Snapshot & Frame-Hash Harness (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M1-P2 · Core 4-Motif Vertical Slice & 2K Cubic Engine`
- **Depends On:** `Task 107`, `Task 109`
- **Git Worktree & Branch:** `task/113-remotion-visual-regression` in `../tc-wt/task-113-remotion-visual-regression`
- **Owned Write Scope:** `packages/render_catalog/tests/visual_regression.test.ts`, `packages/render_catalog/src/renderer/FrameVerifier.ts`, `.agent-handoffs/task-113.md`
- **Mandatory Reference Files:** [code-animation-catalog.md](code-animation-catalog.md)
- **Shared Contracts Consumed / Produced:** Deterministic `renderStill` SSIM & Safe-Zone border audits

#### Scope And Implementation Requirements

- [ ] Verify SSIM `>= 0.995` and zero high-contrast pixel intrusion in exclusion borders across sampled motif stills.

#### Edge Cases And Failure Modes

- Font anti-aliasing subpixel noise across OS: tolerant SSIM threshold.

#### Bug Prevention And Invariants

- **Non-Blank & Safe-Zone-Clean Frame Invariant.**

#### Independent Testability & Parallel Isolation

- Standalone in `packages/render_catalog`.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- visual_regression` with 100% pass.
- **Acceptance:** Visual regression harness verified.

### Task 114: `StickFigure` Rig & Fast JS Boil Consistency Test Suite (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M1-P2 · Core 4-Motif Vertical Slice & 2K Cubic Engine`
- **Depends On:** `Task 101`–`113`
- **Git Worktree & Branch:** `task/114-stick-rig-consistency-suite` in `../tc-wt/task-114-stick-rig-consistency-suite`
- **Owned Write Scope:** `packages/render_catalog/tests/rig_consistency.test.tsx`, `.agent-handoffs/task-114.md`
- **Mandatory Reference Files:** [code-animation-catalog.md](code-animation-catalog.md)
- **Shared Contracts Consumed / Produced:** Certifies Layer 1 `StickFigure` (`14x10x7` combinations, JS boil, RMS nod sync, zero SVG turbulence)

#### Scope And Implementation Requirements

- [ ] Exercise all 140 pose-emotion permutations + props + RMS sync + un-grained output parity.

#### Edge Cases And Failure Modes

- Conflicting `handcuffed` + held prop: explicit precedence warning.

#### Bug Prevention And Invariants

- **100% Character & Speed Invariant.**

#### Independent Testability & Parallel Isolation

- Standalone suite in `packages/render_catalog`.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- rig_consistency` with 100% pass.
- **Acceptance:** `StickFigure` rig certified.

---

### Task 115: Implement MVP Motif #1 — `StickmanStage` (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M1-P2 · Core 4-Motif Vertical Slice & 2K Cubic Engine`
- **Depends On:** `Task 114`
- **Git Worktree & Branch:** `task/115-motif-stickman-stage` in `../tc-wt/task-115-motif-stickman-stage`
- **Owned Write Scope:** `packages/render_catalog/src/motifs/StickmanStage.tsx`, `packages/render_catalog/tests/motifs/stickman_stage.test.tsx`, `.agent-handoffs/task-115.md`
- **Mandatory Reference Files:** [code-animation-catalog.md](code-animation-catalog.md)
- **Shared Contracts Consumed / Produced:** Core Vertical Slice Motif #1 (`StickmanStage`)

#### Scope And Implementation Requirements

- [ ] Render 1–5 `StickFigure`s across 6 noir architectural presets inside `<SafeZoneLayout>` with cubic camera pan and `travel_axis` motion.

#### Edge Cases And Failure Modes

- 5-character horizontal crowding: minimum `180 px` spacing.

#### Bug Prevention And Invariants

- **Zero Head Collision & Axis Continuity Invariant.**

#### Independent Testability & Parallel Isolation

- Tested on `ep_golden_01_20min`.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- stickman_stage` with 100% pass.
- **Acceptance:** MVP Motif #1 `StickmanStage` verified.

### Task 116: Implement Extended 2D Motif #5 — `TimelineScrubber` (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M2-Full · Scale Motifs, Optional Batch Desk & Analytics`
- **Depends On:** `Task 111`, `Task 114`
- **Git Worktree & Branch:** `task/116-motif-timeline-scrubber` in `../tc-wt/task-116-motif-timeline-scrubber`
- **Owned Write Scope:** `packages/render_catalog/src/motifs/TimelineScrubber.tsx`, `packages/render_catalog/tests/motifs/timeline_scrubber.test.tsx`, `.agent-handoffs/task-116.md`
- **Mandatory Reference Files:** [code-animation-catalog.md](code-animation-catalog.md), [schema/pipeline.sql](schema/pipeline.sql)
- **Shared Contracts Consumed / Produced:** Extended 2D Motif #5 (`TimelineScrubber`) per single authoritative `MOTIF_REGISTRY_V1` (`F-16`; note `Illustrative2KPanZoom` is owned SOLELY by Python `packages/crime_scene_2k`, NOT duplicated in Remotion!)

#### Scope And Implementation Requirements

- [ ] Implement `TimelineScrubber` rendering chronological documentary date/hour scrub bars, milestone pins linked to `fact_ledger(fact_id)`, and crisp Safe-Zone containment inside `<SafeZoneLayout>`.

#### Edge Cases And Failure Modes

- Dense multi-year date jumps (`2018 -> 2023`): auto-compress tick spacing cleanly without overlapping date labels (`RULE_07`).

#### Bug Prevention And Invariants

- **Single `MOTIF_REGISTRY_V1` Ownership Invariant (`F-16`):** `@tc/render_catalog` owns 2D vector motifs exclusively; `packages/crime_scene_2k` owns all 2K illustrative pan/zoom scenes exclusively.

#### Independent Testability & Parallel Isolation

- Tested offline on multi-day timeline fixture JSON.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- timeline_scrubber` with 100% pass.
- **Acceptance:** Extended 2D Motif #5 `TimelineScrubber` verified under `MOTIF_REGISTRY_V1`.

### Task 117: Implement MVP Motif #3 — `AudioEvidenceCard` (With `"TRANSCRIPT DRAMATIZATION"` Badge) (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M1-P2 · Core 4-Motif Vertical Slice & 2K Cubic Engine`
- **Depends On:** `Task 111`, `Task 114`
- **Git Worktree & Branch:** `task/117-motif-audio-evidence-card` in `../tc-wt/task-117-motif-audio-evidence-card`
- **Owned Write Scope:** `packages/render_catalog/src/motifs/AudioEvidenceCard.tsx`, `packages/render_catalog/tests/motifs/audio_evidence_card.test.tsx`, `.agent-handoffs/task-117.md`
- **Mandatory Reference Files:** [code-animation-catalog.md](code-animation-catalog.md), [legal-copyright-and-adsense.md](legal-copyright-and-adsense.md)
- **Shared Contracts Consumed / Produced:** Core Vertical Slice Motif #3 (`2K noir room + FFT waveform + L-cut banner + mandatory "TRANSCRIPT DRAMATIZATION" badge when TTS-voiced`)

#### Scope And Implementation Requirements

- [ ] Render log-scaled FFT spectrum waveform, Law 6 `0.6–1.0s` L-cut visual lead-in, and prominent `"TRANSCRIPT DRAMATIZATION · TTS READING"` badge whenever `showDramatizationBadge === true` (`Task 057`/`082`)!

#### Edge Cases And Failure Modes

- Archival 911 WAV (`showDramatizationBadge: false`) vs TTS-voiced 911 transcript quote (`true`): toggle badge deterministically (`"ARCHIVAL 911 AUDIO (FOIA)"` vs `"TRANSCRIPT DRAMATIZATION"`).

#### Bug Prevention And Invariants

- **Unambiguous Archival vs Dramatization Labeling Invariant.**

#### Independent Testability & Parallel Isolation

- React + FFT fixture tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- audio_evidence_card` verifying both archival and dramatization badges.
- **Acceptance:** MVP Motif #3 `AudioEvidenceCard` verified.

### Task 118: Implement Authoritative MVP Motif #4 — `FoiaFootageFrame` (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M0.5 / M1-P2 · Authoritative 4-Motif MVP Slice`
- **Depends On:** `Task 109`, `Task 114`
- **Git Worktree & Branch:** `task/118-motif-foia-footage-frame` in `../tc-wt/task-118-motif-foia-footage-frame`
- **Owned Write Scope:** `packages/render_catalog/src/motifs/FoiaFootageFrame.tsx`, `packages/render_catalog/tests/motifs/foia_footage_frame.test.tsx`, `.agent-handoffs/task-118.md`
- **Mandatory Reference Files:** [code-animation-catalog.md](code-animation-catalog.md), [schema/pipeline.sql](schema/pipeline.sql)
- **Shared Contracts Consumed / Produced:** Authoritative 4-Motif MVP Slice Motif #4 (`MOTIF_REGISTRY_V1` `F-16`); renders rights-cleared CFR-normalized FOIA MP4 tagged `apply_grade: false` for raw authenticity + editorial HUD/PiP

#### Scope And Implementation Requirements

- [ ] Embed scrubbed `30 fps CFR` FOIA clip with provenance HUD, callout zoom box, `9:16` pillarbox dossier layout, and optional PiP `StickFigure`, flagged `apply_grade: false` in `scene_grade_manifest.json`.

#### Edge Cases And Failure Modes

- `9:16` phone clip inside `16:9`: intentional dossier sidebar layout.

#### Bug Prevention And Invariants

- **Raw FOIA Authenticity & Transformative Overlay Invariant.**

#### Independent Testability & Parallel Isolation

- Synthetic `9:16` and `16:9` MP4 tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- foia_footage_frame` with 100% pass.
- **Acceptance:** Motif #4 `FoiaFootageFrame` verified.

### Task 119: Implement Motif #5 — `HeroVideoBridge` (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M2-Full · Scale Motifs, Optional Batch Desk & Analytics`
- **Depends On:** `Task 109`, `Task 115`
- **Git Worktree & Branch:** `task/119-motif-hero-video-bridge` in `../tc-wt/task-119-motif-hero-video-bridge`
- **Owned Write Scope:** `packages/render_catalog/src/motifs/HeroVideoBridge.tsx`, `packages/render_catalog/tests/motifs/hero_video_bridge.test.tsx`, `.agent-handoffs/task-119.md`
- **Mandatory Reference Files:** [code-animation-catalog.md](code-animation-catalog.md), [director-and-13-laws.md](director-and-13-laws.md)
- **Shared Contracts Consumed / Produced:** Flow Veo/Omni bridge tagged `apply_grade: true` (graded once in Agent 6) + automatic non-neighbor `fallback_spec` switch

#### Scope And Implementation Requirements

- [ ] Play accepted `720p->1080p` Flow MP4 (`0.85x–1.15x` speed bounds) OR transparently switch to `fallback_spec` (non-neighbor engine!) on `SWITCHED_TO_FALLBACK`.

#### Edge Cases And Failure Modes

- `7.6s` scene with `8.0s` Flow clip: clean exact-millisecond trim without speed distortion.

#### Bug Prevention And Invariants

- **Seamless Fallback & Single-Grade Tagging Invariant.**

#### Independent Testability & Parallel Isolation

- Tested on `ep_golden_02_2strike_fallback`.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- hero_video_bridge` with 100% pass.
- **Acceptance:** Motif #5 `HeroVideoBridge` verified.

### Task 120: Implement Motif #6 — `SmsPhoneThread` (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M2-Full · Scale Motifs, Optional Batch Desk & Analytics`
- **Depends On:** `Task 110`, `Task 114`
- **Git Worktree & Branch:** `task/120-motif-sms-phone-thread` in `../tc-wt/task-120-motif-sms-phone-thread`
- **Owned Write Scope:** `packages/render_catalog/src/motifs/SmsPhoneThread.tsx`, `packages/render_catalog/tests/motifs/sms_phone_thread.test.tsx`, `.agent-handoffs/task-120.md`
- **Mandatory Reference Files:** [code-animation-catalog.md](code-animation-catalog.md)
- **Shared Contracts Consumed / Produced:** Motif #6 (`SmsPhoneThread`)

#### Scope And Implementation Requirements

- [ ] Render bezel-clipped dark smartphone evidence chat thread inside `<SafeZoneLayout>`, syncing typing indicators, highlight bubbles, and `typing_tap` SFX cues.

#### Edge Cases And Failure Modes

- 10+ messages overflowing height: clipped smooth auto-scroll inside phone bezel.

#### Bug Prevention And Invariants

- **Bezel-Clipped Safe Scroll Invariant.**

#### Independent Testability & Parallel Isolation

- Golden SMS fixture tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- sms_phone_thread` with 100% pass.
- **Acceptance:** Motif #6 `SmsPhoneThread` verified.

### Task 121: Implement Motif #7 — `MapRouteTrace` (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M2-Full · Scale Motifs, Optional Batch Desk & Analytics`
- **Depends On:** `Task 111`, `Task 114`
- **Git Worktree & Branch:** `task/121-motif-map-route-trace` in `../tc-wt/task-121-motif-map-route-trace`
- **Owned Write Scope:** `packages/render_catalog/src/motifs/MapRouteTrace.tsx`, `packages/render_catalog/tests/motifs/map_route_trace.test.tsx`, `.agent-handoffs/task-121.md`
- **Mandatory Reference Files:** [code-animation-catalog.md](code-animation-catalog.md)
- **Shared Contracts Consumed / Produced:** Motif #7 (`MapRouteTrace` — 100% procedural SVG, zero copyrighted map tiles!)

#### Scope And Implementation Requirements

- [ ] Render procedural vector blueprint map with multi-waypoint polyline trace, drive-time HUD, and animated marker.

#### Edge Cases And Failure Modes

- Multi-stop alibi route: `waypoints[]` polyline with per-leg timestamp callouts.

#### Bug Prevention And Invariants

- **Zero Copyrighted Map-Tile Invariant.**

#### Independent Testability & Parallel Isolation

- Multi-waypoint NJ Route 9 fixture tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- map_route_trace` with 100% pass.
- **Acceptance:** Motif #7 `MapRouteTrace` verified.

### Task 122: Implement Authoritative MVP Motif #3 — `RedactedDocReveal` (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M0.5 / M1-P2 · Authoritative 4-Motif MVP Slice`
- **Depends On:** `Task 110`, `Task 114`
- **Git Worktree & Branch:** `task/122-motif-redacted-doc-reveal` in `../tc-wt/task-122-motif-redacted-doc-reveal`
- **Owned Write Scope:** `packages/render_catalog/src/motifs/RedactedDocReveal.tsx`, `packages/render_catalog/tests/motifs/redacted_doc_reveal.test.tsx`, `.agent-handoffs/task-122.md`
- **Mandatory Reference Files:** [code-animation-catalog.md](code-animation-catalog.md), [schema/pipeline.sql](schema/pipeline.sql)
- **Shared Contracts Consumed / Produced:** Authoritative 4-Motif MVP Slice Motif #3 (`RedactedDocReveal`, aligned with `MOTIF_REGISTRY_V1` `F-16`)

#### Scope And Implementation Requirements

- [ ] Render aged court filing sheet inside `<SafeZoneLayout>`, black redaction bars, citation badge, and multi-line yellow highlighter sweep synced to `word_timestamps[]` (`highlighter_glide` SFX).

#### Edge Cases And Failure Modes

- Wrapped multi-line quote: sequential per-line `<mark>` rect sweep.

#### Bug Prevention And Invariants

- **Multi-Line Highlight & Safe-Zone Containment Invariant.**

#### Independent Testability & Parallel Isolation

- Multi-line wrapped quote tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- redacted_doc_reveal` with 100% pass.
- **Acceptance:** MVP Motif #4 `RedactedDocReveal` verified.

### Task 123: Implement Motif #9 — `TimelineDateScrubber` (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M2-Full · Scale Motifs, Optional Batch Desk & Analytics`
- **Depends On:** `Task 110`, `Task 114`
- **Git Worktree & Branch:** `task/123-motif-timeline-date-scrubber` in `../tc-wt/task-123-motif-timeline-date-scrubber`
- **Owned Write Scope:** `packages/render_catalog/src/motifs/TimelineDateScrubber.tsx`, `packages/render_catalog/tests/motifs/timeline_date_scrubber.test.tsx`, `.agent-handoffs/task-123.md`
- **Mandatory Reference Files:** [code-animation-catalog.md](code-animation-catalog.md)
- **Shared Contracts Consumed / Produced:** Motif #9 (`TimelineDateScrubber`)

#### Scope And Implementation Requirements

- [ ] Render non-linear forensic date ruler with `// TIME GAP` dividers, focal card zoom, and `tick_sfx` cues.

#### Edge Cases And Failure Modes

- Tight 4-minute event clusters: non-linear spacing prevents label collision.

#### Bug Prevention And Invariants

- **Non-Overlapping Notch Invariant.**

#### Independent Testability & Parallel Isolation

- Mixed multi-year + minute-cluster tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- timeline_date_scrubber` with 100% pass.
- **Acceptance:** Motif #9 `TimelineDateScrubber` verified.

### Task 124: Implement Motif #10 — `CaseBoardSpine` (`210s–270s` Boundary-Snapped Reset) (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M2-Full · Scale Motifs, Optional Batch Desk & Analytics`
- **Depends On:** `Task 110`, `Task 114`
- **Git Worktree & Branch:** `task/124-motif-case-board-spine` in `../tc-wt/task-124-motif-case-board-spine`
- **Owned Write Scope:** `packages/render_catalog/src/motifs/CaseBoardSpine.tsx`, `packages/render_catalog/tests/motifs/case_board_spine.test.tsx`, `.agent-handoffs/task-124.md`
- **Mandatory Reference Files:** [code-animation-catalog.md](code-animation-catalog.md), [director-and-13-laws.md](director-and-13-laws.md)
- **Shared Contracts Consumed / Produced:** Motif #10 (`CaseBoardSpine`) rendered cleanly at boundary-snapped `210–270s` windows

#### Scope And Implementation Requirements

- [ ] Render 2-row Safe-Zone corkboard grid (up to 16 clue polaroids), pin-drop animation (`pin_thud` SFX), crimson string draw-on, and 5-second camera zoom-out reset.

#### Edge Cases And Failure Modes

- 16 clues on final Act 3 board: deterministic 2-row Safe-Zone layout keeps all strings/cards unclipped.

#### Bug Prevention And Invariants

- **Bounded 16-Clue Corkboard Invariant.**

#### Independent Testability & Parallel Isolation

- Tested at 3, 8, and 16 clues.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- case_board_spine` with 100% pass.
- **Acceptance:** Motif #10 `CaseBoardSpine` verified.

### Task 125: Implement Motif #11 — `AlibiSplitScreen` (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M2-Full · Scale Motifs, Optional Batch Desk & Analytics`
- **Depends On:** `Task 110`, `Task 114`
- **Git Worktree & Branch:** `task/125-motif-alibi-split-screen` in `../tc-wt/task-125-motif-alibi-split-screen`
- **Owned Write Scope:** `packages/render_catalog/src/motifs/AlibiSplitScreen.tsx`, `packages/render_catalog/tests/motifs/alibi_split_screen.test.tsx`, `.agent-handoffs/task-125.md`
- **Mandatory Reference Files:** [code-animation-catalog.md](code-animation-catalog.md)
- **Shared Contracts Consumed / Produced:** Motif #11 (`AlibiSplitScreen`)

#### Scope And Implementation Requirements

- [ ] Render suspect claim vs primary evidence split with millisecond-synced crimson `CONFLICT` stamp (`<= 6px` clamped micro-shake) and `conflict_stamp` SFX.

#### Edge Cases And Failure Modes

- Micro-shake shifting text across Safe-Zone: restrict shake to inner graphic container inside `SafeZoneLayout`.

#### Bug Prevention And Invariants

- **Millisecond Stamp Sync Invariant.**

#### Independent Testability & Parallel Isolation

- Golden Turning Point split tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- alibi_split_screen` with 100% pass.
- **Acceptance:** Motif #11 `AlibiSplitScreen` verified.

### Task 126: Implement Motif #12 — `EvidenceMatchCard` (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M2-Full · Scale Motifs, Optional Batch Desk & Analytics`
- **Depends On:** `Task 110`, `Task 114`
- **Git Worktree & Branch:** `task/126-motif-evidence-match-card` in `../tc-wt/task-126-motif-evidence-match-card`
- **Owned Write Scope:** `packages/render_catalog/src/motifs/EvidenceMatchCard.tsx`, `packages/render_catalog/tests/motifs/evidence_match_card.test.tsx`, `.agent-handoffs/task-126.md`
- **Mandatory Reference Files:** [code-animation-catalog.md](code-animation-catalog.md)
- **Shared Contracts Consumed / Produced:** Motif #12 (`EvidenceMatchCard`)

#### Scope And Implementation Requirements

- [ ] Render symmetric side-by-side forensic exhibit frames (`object-fit: contain`), animated crimson comparison arrows, and `camera_shutter` SFX.

#### Edge Cases And Failure Modes

- Mismatched aspect-ratio exhibits: normalized symmetric dossier boxes.

#### Bug Prevention And Invariants

- **Symmetric Framing Invariant.**

#### Independent Testability & Parallel Isolation

- Aspect-ratio mismatch tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- evidence_match_card` with 100% pass.
- **Acceptance:** Motif #12 `EvidenceMatchCard` verified.

### Task 127: Implement Layer 4 Sandboxed `CustomDiagramScene` (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M2-Full · Scale Motifs, Optional Batch Desk & Analytics`
- **Depends On:** `Task 111`, `Task 114`
- **Git Worktree & Branch:** `task/127-custom-diagram-sandbox` in `../tc-wt/task-127-custom-diagram-sandbox`
- **Owned Write Scope:** `packages/render_catalog/src/motifs/CustomDiagramScene.tsx`, `packages/render_catalog/tests/motifs/custom_diagram.test.tsx`, `.agent-handoffs/task-127.md`
- **Mandatory Reference Files:** [code-animation-catalog.md](code-animation-catalog.md)
- **Shared Contracts Consumed / Produced:** Declarative SVG-primitive JSON escape hatch (`<= 25` primitives, zero JS `eval`)

#### Scope And Implementation Requirements

- [ ] Render declarative JSON shapes/arrows/labels inside `<SafeZoneLayout>` using `<BoilPath>` with strict XSS/script rejection.

#### Edge Cases And Failure Modes

- Untrusted `<script>` string in label: rendered strictly as escaped SVG text node.

#### Bug Prevention And Invariants

- **Zero Arbitrary Code Execution Invariant.**

#### Independent Testability & Parallel Isolation

- Adversarial injection tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- custom_diagram` with 100% pass.
- **Acceptance:** `CustomDiagramScene` verified.

### Task 128: Implement `TimelineSpec` Full-Catalog & MVP-Slice `BatchCompiler` (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M1-P2 · Core 4-Motif Vertical Slice & 2K Cubic Engine`
- **Depends On:** `Task 112`, `Task 115`–`127`
- **Git Worktree & Branch:** `task/128-timeline-spec-batch-compiler` in `../tc-wt/task-128-timeline-spec-batch-compiler`
- **Owned Write Scope:** `packages/render_catalog/src/renderer/BatchCompiler.ts`, `packages/render_catalog/tests/batch_compiler.test.ts`, `.agent-handoffs/task-128.md`
- **Mandatory Reference Files:** [code-animation-catalog.md](code-animation-catalog.md)
- **Shared Contracts Consumed / Produced:** Compiles `TimelineSpec` -> `1080p30` scene MP4s + `micro_sfx_cues.json` + `scene_grade_manifest.json` (`apply_grade`)

#### Scope And Implementation Requirements

- [ ] Route all motifs cleanly (supporting `--mvp-4-motifs` subset early as well as full 12-motif catalog), emit `scene_grade_manifest.json` (single Agent 6 grade pass!), and handle `SWITCHED_TO_FALLBACK` swaps transparently.

#### Edge Cases And Failure Modes

- Mixed `apply_grade: true` and `false` scenes: accurate per-scene manifest metadata passed cleanly to Agent 6.

#### Bug Prevention And Invariants

- **100% Motif Routing & Single-Grade Manifest Invariant.**

#### Independent Testability & Parallel Isolation

- Tested on all 3 Golden Packs.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- batch_compiler` with 100% pass.
- **Acceptance:** `BatchCompiler` verified.

### Task 129: Implement `CustomDiagramScene` Promotion & Registry Tooling (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M2-Full · Scale Motifs, Optional Batch Desk & Analytics`
- **Depends On:** `Task 127`, `Task 128`
- **Git Worktree & Branch:** `task/129-custom-diagram-promoter` in `../tc-wt/task-129-custom-diagram-promoter`
- **Owned Write Scope:** `packages/render_catalog/src/tools/promote_diagram.ts`, `packages/render_catalog/tests/promote_diagram.test.ts`, `.agent-handoffs/task-129.md`
- **Mandatory Reference Files:** [code-animation-catalog.md](code-animation-catalog.md)
- **Shared Contracts Consumed / Produced:** Scaffolds new catalog components from recurring `CustomDiagramScene` tags

#### Scope And Implementation Requirements

- [ ] Detect `>= 3` recurring diagram tags and scaffold Zod + React motif templates without colliding with motifs #1–#12.

#### Edge Cases And Failure Modes

- Reserved name collision: rejected before file write.

#### Bug Prevention And Invariants

- **Unique Motif Registry Invariant.**

#### Independent Testability & Parallel Isolation

- Temp-dir generator tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- promote_diagram` with 100% pass.
- **Acceptance:** Diagram promoter verified.

### Task 130: Implement `render_catalog` CSS Safe-Zone Bounding Box Verification (`packages/render_catalog`)

- **Track & Owner:** `Part 2 · Developer B`
- **Milestone:** `M1-P2 · Core 4-Motif Vertical Slice & 2K Cubic Engine`
- **Depends On:** `Task 128`
- **Git Worktree & Branch:** `task/130-catalog-css-safezone-audit` in `../tc-wt/task-130-catalog-css-safezone-audit`
- **Owned Write Scope:** `packages/render_catalog/src/guards/RuntimeGuards.ts`, `packages/render_catalog/tests/runtime_guards.test.ts`, `.agent-handoffs/task-130.md`
- **Mandatory Reference Files:** [director-and-13-laws.md](director-and-13-laws.md), [code-animation-catalog.md](code-animation-catalog.md)
- **Shared Contracts Consumed / Produced:** Empirically verifies DOM/SVG bounding boxes across all 12 motifs stay inside `<SafeZoneLayout>` even with max-length 12-word labels!

#### Scope And Implementation Requirements

- [ ] Measure rendered `getBoundingClientRect()` inside Chromium across all 12 motifs with adversarial max-length 12-word text labels, confirming 0 exclusion-zone leaks.

#### Edge Cases And Failure Modes

- Dynamic wrap expanding downward past `885 px`: CSS containment clamps cleanly!

#### Bug Prevention And Invariants

- **Zero CSS Safe-Zone Intrusion Invariant.**

#### Independent Testability & Parallel Isolation

- Standalone Chromium layout tests.

#### Verification, Testing And Acceptance Criteria

- [ ] Run `pnpm --filter @tc/render_catalog test -- runtime_guards` with 100% pass.
- **Acceptance:** Runtime CSS Safe-Zone audit verified.

### Task 131: Benchmark `<5s` JS-Boil Remotion Re-Render Performance (`packages/render_catalog`)
- **Owner:** Developer B (Part 2) | **Milestone:** M1-P2 | **Depends on:** Task 103, Task 109, Task 125
- **Files:** `packages/render_catalog/benchmarks/js_boil_bench.ts`, `packages/render_catalog/tests/perf_sla.test.ts`
- **Tests:** Automated Chromium/Playwright Remotion CLI single-scene re-render timer test asserting zero `<feTurbulence>` DOM nodes and `<5.0s` wall-clock render for a `10.0s` 1080p30 scene.

#### Scope And Implementation Requirements
- Implement an automated benchmark suite proving that replacing SVG `<feTurbulence>` filter chains with the deterministic `6 fps` JS vertex-jitter boil algorithm (evaluated at `30 fps` container cadence) hits sub-5-second single-scene heal rendering for Agent 6 Vision QA fixes (`RULE_04` / `RULE_07`).
- Assert via static AST scan and Chromium DOM serialization that ZERO `<feTurbulence>`, `<feDisplacementMap>`, or duplicate film-grain `<canvas>` elements are emitted inside `render_catalog` JSX components (`scene_grade_manifest.json` owns grading exclusively for Agent 6).
- Measure P50, P95, and P99 render wall-clock latencies across all 12 motion archetypes (`SplitScreenEvidence`, `AnimatedMapRoute`, `EvidenceDocumentZoom`, etc.) on local CPU/Chromium (`--concurrency=4`).
- Emit benchmark JSON telemetry to `artifacts/benchmarks/remotion_js_boil_perf.json` including frame-time histograms and Chromium heap watermarks.

#### Edge Cases And Failure Modes
- Remotion Chromium cold-start overhead (`~1.2s`) skewing single-scene SLA measurements: support warm-bundle reuse or pooled headless Chrome socket in production Agent 6 heal calls while measuring both cold and warm bounds.
- Dense particle scenes (`MapRoute` + 25 callouts + corkboard pins) approaching the `5.0s` ceiling on lower-core CPUs: cap pin/callout shadow CSS filters to hardware-composited `transform`/`opacity` properties only.
- Non-deterministic `Math.random()` inside JS boil path sneaking past ESLint: hook `global.Math.random = () => { throw new Error("Forbidden") }` during unit and benchmark execution.

#### Bug Prevention And Invariants
- Never allow `<feTurbulence>` back into `packages/render_catalog` under any legacy flag or fallback branch.
- Verify output PNG frame hashes at `frame=0`, `frame=150`, `frame=299` are bit-identical across two sequential benchmark runs on the same `SceneSpec` seed.
- Hard-fail CI (`perf_sla.test.ts`) if any archetype's single-scene 10s render exceeds `5,000 ms` warm or `6,500 ms` cold.

#### Independent Testability & Parallel Isolation
- Runs purely on `packages/render_catalog` with synthetic 12-motif `SceneSpec` fixtures and zero external network calls or Part 1 dependencies.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pnpm --filter @tc/render_catalog run bench:js-boil` and assert all 12 archetypes finish under `5.0s` warm (`<6.5s` cold) with `0` `<feTurbulence>` nodes.
- [ ] Verify identical frame checksums across repeated runs in `tests/perf_sla.test.ts`.
- **Acceptance:** Sub-5s Remotion re-render SLA and deterministic 6fps-in-30fps JS boil parity proven cleanly.

### Task 132: Build `render_catalog` CLI, `--mvp-4-motifs` & `--scene` Re-Render Entrypoint (`packages/render_catalog`)
- **Owner:** Developer B (Part 2) | **Milestone:** M1-P2 | **Depends on:** Task 129, Task 130, Task 131
- **Files:** `packages/render_catalog/src/cli.ts`, `packages/render_catalog/src/index.ts`, `packages/render_catalog/tests/cli_rerender.test.ts`
- **Tests:** CLI invocation tests covering full manifest render, `--mvp-4-motifs` thin-vertical-slice validation mode, `--scene <scene_id>` single-scene heal mode, and exit-code error contracts.

#### Scope And Implementation Requirements
- Expose the unified CLI and barrel export `@tc/render_catalog` consumed by Part 2 orchestrators and Agent 6 (`render-catalog --manifest <path> --out-dir <dir> --scene <id?> --mvp-4-motifs?`).
- When `--scene <scene_id>` is passed, bundle once (reusing cached webpack/rspack bundle if manifest schema version is unchanged) and render only that single `CODE_STICKMAN` clip as `CFR 30fps` + empty/PCM audio placeholder plus updated entry in `scene_grade_manifest.json`.
- When `--mvp-4-motifs` is enabled (supporting Milestone `M0.5` Thin Vertical Slice), restrict validation/pre-warm strictly to the **authoritative `MOTIF_REGISTRY_V1` 4-Motif MVP Slice (`F-16`)**: **`StickmanStage`, `AudioEvidenceCard`, `RedactedDocReveal`, and `FoiaFootageFrame`** (all 2K pan/zoom scenes are owned exclusively by Python `packages/crime_scene_2k`).
- Write structured machine-readable `render_report.json` alongside rendered MP4s summarizing scene durations, `CFR 30fps` verified frame counts, zero-SVG-filter attestation, and wall-clock ms.

#### Edge Cases And Failure Modes
- Unknown `--scene` ID passed during Agent 6 self-heal: exit with non-zero code `2` and structured JSON error without touching previously rendered sibling clips.
- Manifest mixes `CODE_STICKMAN` with `FLOW_HERO_VIDEO` / `STILL_2K_PANZOOM` scenes: filter cleanly to `engine == "CODE_STICKMAN"` without crashing on Flow-specific union fields.
- Concurrent Chromium bundle cache corruption when two Remotion processes share `/tmp/remotion-cache`: isolate bundle directory per `manifest.episode_id` + `scene_id` or lock via atomic rename.

#### Bug Prevention And Invariants
- Never modify the input `manifest.json` file; `@tc/render_catalog` treats it strictly read-only.
- Ensure every exported MP4 reports exact `r_frame_rate == "30/1"`, `avg_frame_rate == "30/1"`, and exact `nb_frames == round(duration_sec * 30)` before returning exit code `0`.

#### Independent Testability & Parallel Isolation
- Tested standalone using golden stub manifests generated in Task 004 without Part 1 Python installation.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pnpm --filter @tc/render_catalog test -- cli_rerender` verifying `--scene`, `--mvp-4-motifs`, and full batch renders.
- [ ] Confirm exit code `0` produces valid `render_report.json` and `scene_grade_manifest.json`.
- **Acceptance:** `@tc/render_catalog` CLI is production-ready for both batch rendering and `<5s` Agent 6 surgical heals.

### Task 133: Implement Monochrome PIL Stickman Parity Engine (`packages/python_motion`)
- **Owner:** Developer B (Part 2) | **Milestone:** M1-P2 | **Depends on:** Task 002, Task 004
- **Files:** `packages/python_motion/pyproject.toml`, `packages/python_motion/src/python_motion/stickman_pil.py`, `packages/python_motion/tests/test_stickman_pil.py`
- **Tests:** Pixel-visual and pose-angle unit tests verifying `CaseBible` palette adherence, zero `#C92A2A` crimson in Flow keyframes, and deterministic charcoal silhouettes.

#### Scope And Implementation Requirements
- Bootstrap `packages/python_motion` (Python 3.12, Pillow, NumPy, SciPy, OpenCV) as the deterministic raster keyframe, trajectory, wireframe animatic, and procedural SFX synthesizer for Part 2.
- Implement `StickmanRenderer` rendering crisp antialiased stick figures, detective silhouettes, posture poses (`idle`, `walking`, `pointing`, `seated`, `evidence_hold`, `doorway_entry`), and 2D spatial props onto high-res parchment `#E9E2D2` or charcoal-noir backgrounds matching `render_catalog` geometry.
- **CRITICAL AUDIT FIX (Monochrome Flow Keyframe Rule):** Enforce a strict `for_flow_keyframe: bool = True` guard that BANS `evidenceCrimsonHex` (`#C92A2A`) or any red-hue pixel clusters inside Flow Start/End PNG frames—limiting palette strictly to `#1B1B1D` ink, `#E9E2D2` parchment, muted slate blue (`#3A4F66`), and warm amber (`#B8860B`), reserving crimson exclusively for Remotion overlays and 2K still callouts.
- Output `1280x720` (`Veo/Omni` 720p target) and `1920x1080` PNGs cleanly with exact RGBA/RGB bit depths and deterministic SHA-256 checksums.

#### Edge Cases And Failure Modes
- Jagged 1px diagonal limbs at 720p causing temporal shimmer in `gemini-omni-1.2-flash`: render limbs at `2x` supersampled canvas (`2560x1440`) and Lanczos-downsample to target `1280x720`.
- Thin limbs `< 3px` vanishing during video diffusion encoding: clamp minimum stroke width to `6px` at 720p (`9px` at 1080p) matching Remotion's charcoal stroke ratio.
- Accidental crimson badge or red arrow requested inside `SceneSpec.keyframe_props` for a `FLOW_HERO_VIDEO` beat: automatically strip/remap red markers to muted slate/amber when `for_flow_keyframe=True` and log a structured warning.

#### Bug Prevention And Invariants
- Never embed text captions, watermarks, timestamps, or UI chrome inside Flow Start/End PNG frames (`Veo` and `Omni` hallucinate garbled glyphs on text-bearing keyframes).
- Assert zero pixels satisfy `R > 160 and R > G * 1.8 and R > B * 1.8` in any generated Flow keyframe PNG.

#### Independent Testability & Parallel Isolation
- Consumes frozen `CaseBible` + `SceneSpec` schemas with zero dependency on Part 1 runtime or live Google Flow APIs.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/python_motion/tests/test_stickman_pil.py` verifying zero-red pixel assertion and pose rendering across 8 poses.
- [ ] Visually inspect SSIM parity against `@tc/render_catalog` stickman PNG reference snapshot.
- **Acceptance:** Deterministic monochrome Flow Start/End keyframe generator verified clean of crimson triggers.

### Task 134: Implement Law 12 Input-Image Safety Validator (`packages/python_motion`)
- **Owner:** Developer B (Part 2) | **Milestone:** M1-P2 | **Depends on:** Task 133
- **Files:** `packages/python_motion/src/python_motion/safety_validator.py`, `packages/python_motion/tests/test_safety_validator.py`
- **Tests:** Synthetic image gauntlet testing crimson/blood pixel rejection, face/skin-tone rejection, weapon silhouette heuristic rejection, and benign monochrome approval.

#### Scope And Implementation Requirements
- Implement the pre-flight pixel & heuristic `InputImageSafetyValidator` that inspects every Start/End PNG before it is ever uploaded via Files API to `gemini-omni-1.2-flash` (or optional `VERTEX_VEO_ENTERPRISE` / `HUMAN_BATCH_DESK`) (`RULE_11` / Law 12 enforcement).
- Reject images failing any check:
  1. **Crimson / Blood-Cluster Check:** Connected-component flood scan detecting `>= 35` adjacent pixels with `(R > 140) & (R - max(G, B) > 55)` (guarantees `CaseBible` crimson accents can never slip into Flow keyframes and trigger safety blocks).
  2. **Photorealistic Skin / Face Detector:** OpenCV Haar/DNN face check + HSV skin-tone cluster ratio (`> 3%` contiguous skin pixels) to ensure strictly abstract 2D charcoal/parchment documentary silhouettes.
  3. **Forbidden Text/Artifact Check:** High-frequency horizontal glyph band detector catching accidental rendered text inside Start/End frames.
- Return a structured `ImageSafetyVerdict(passed: bool, violations: list[str], red_pixel_pct: float, skin_pixel_pct: float)`.

#### Edge Cases And Failure Modes
- Warm `#E9E2D2` parchment background triggering naive HSV skin-tone thresholds: calibrate skin mask strictly against saturated mid-value peach/tan ranges (`S in [45, 175], V in [80, 230], H in [2, 22]`) and exclude `#E9E2D2` parchment (`S < 35`) explicitly.
- Amber lamp light `#B8860B` (`R=184, G=134, B=11`) triggering red detector: require `R - G > 55` AND `G < 100` so warm amber documentary highlights pass cleanly while blood-red `#C92A2A` (`R=201, G=42, B=42`) hard-fails immediately.
- Border vignette darkness misclassified as silhouette blob: exclude outer `16px` margin from face/blob heuristics.

#### Bug Prevention And Invariants
- All three adapters (`GeminiOmniInteractionsBackend`, `VertexVeoEnterpriseBackend`, `HumanBatchDeskBackend`) MUST reject uploading/staging any keyframe lacking `ImageSafetyVerdict.passed == True`.
- Never silently auto-crop or blur a failed image; return exact violation codes so keyframe generator fixes palette cleanly or triggers `fallback_spec`.

#### Independent Testability & Parallel Isolation
- Pure Pillow/NumPy/OpenCV offline unit suite requiring no external API keys.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/python_motion/tests/test_safety_validator.py` with 100% pass across positive monochrome and adversarial crimson/skin/text fixtures.
- **Acceptance:** Automated input-image pre-flight gate prevents wasted Flow safety blocks and false positive parchment rejections.

### Task 135: Build Start/End Bookend Keyframe Pair Generator (`packages/python_motion`)
- **Owner:** Developer B (Part 2) | **Milestone:** M1-P2 | **Depends on:** Task 133, Task 134
- **Files:** `packages/python_motion/src/python_motion/bookend_generator.py`, `packages/python_motion/tests/test_bookend_generator.py`
- **Tests:** Start/End pair tests asserting camera-motion consistency, object permanence, and automatic `safety_validator` pass across all Hero motion beats.

#### Scope And Implementation Requirements
- Implement `BookendGenerator` producing tightly coupled keyframe inputs from a `FLOW_HERO_VIDEO` `SceneSpec` aligned cleanly with `flow_jobs.prompt_mode` (`F-07`):
  - `TEXT_TO_VIDEO`: returns `start_frame=None, end_frame=None` (nullable in `flow_jobs`, zero fake blank PNGs!).
  - `FIRST_FRAME`: generates validated `start_frame.png`, `end_frame=None` (`3s–15s`).
  - `FIRST_AND_LAST_FRAME`: generates spatially continuous `(start_frame.png, end_frame.png)` strictly capped at `3s–10s` per `gemini-omni-1.2-flash` Interactions API limits.
- Pass every generated PNG automatically through `InputImageSafetyValidator`; if validation fails, fail fast before reserving any USD budget.
- Write deterministic file artifacts (`<scene_id>_start.png`, `<scene_id>_end.png`, `<scene_id>_bookend_meta.json` with SHA-256 hashes and `prompt_mode`).

#### Edge Cases And Failure Modes
- Excessively large spatial jump (`> 65%` viewport width) between Start and End frame causing morph artifacts in `gemini-omni-1.2-flash`: cap actor translation delta per bucket and warn/clamp inside `bookend_meta.json`.
- Scene uses `FLOW_HERO_VIDEO` in pure `TEXT_TO_VIDEO` mode: cleanly return `start_frame=None, end_frame=None` matching `flow_jobs` nullable frame columns (`F-07`).
- Identical Start and End frame accidentally generated for static camera beat (`delta_norm == 0`): inject subtle `3%` parallax zoom or shadow length shift so the video model animates motion cleanly.

#### Bug Prevention And Invariants
- Zero red/crimson pixels (`#C92A2A`) permitted anywhere in Start or End frames.
- Output dimensions strictly match target `gemini-omni-1.2-flash` resolution bucket (`1280x720` default `720p`; `1920x1080` only when explicitly configured).

#### Independent Testability & Parallel Isolation
- Tested standalone from frozen `SceneSpec` fixtures (`fixtures/ep_golden_01.json`) without calling Veo/Omni.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/python_motion/tests/test_bookend_generator.py` asserting all golden Hero beats emit valid `safety_passed=True` pairs.
- **Acceptance:** Frames-to-Video bookend pipeline produces safe, spatially coherent Start/End PNG pairs.

### Task 136: Implement Deterministic PIL/Manim Trajectory & Map Renderer (`packages/python_motion`)
- **Owner:** Developer B (Part 2) | **Milestone:** M1-P2 | **Depends on:** Task 133
- **Files:** `packages/python_motion/src/python_motion/trajectory_engine.py`, `packages/python_motion/tests/test_trajectory_engine.py`
- **Tests:** Trajectory path math tests (Catmull-Rom splines, compass bearing overlays, cell-tower arc intersections) and 1080p30 frame-sequence determinism checks.

#### Scope And Implementation Requirements
- Implement Python-side mathematical trajectory/telemetry clip synthesis (complementing Remotion `AnimatedMapRoute` / `CellTowerTriangulation` for complex multi-node geometric diagrams or Python-native preview sequences) using deterministic NumPy + Pillow vector rasterization.
- Support smooth eased spline interpolation (`ease_in_out_cubic`), GPS/cell-tower azimuth sector cones, timestamp tick interpolation, and optional export as `CFR 30fps` raw MP4 (`yuv420p`) or transparent overlay PNG sequence.
- Enforce `CaseBible` palette (`#1B1B1D` ink lines, `#E9E2D2` parchment, `#3A4F66` slate cones, `#C92A2A` crimson target ring ONLY when `for_flow_keyframe=False`).
- Guarantee sub-pixel line smoothness via `2x` supersampled rasterization and zero external GPU dependency.

#### Edge Cases And Failure Modes
- Coincident start and end waypoints (`norm < 1e-6`) causing `ZeroDivisionError` in Catmull-Rom tangent vector normalization: return stationary pulse marker instead of crashing.
- Extremely long waypoint arrays (`> 200` points) causing O(N^2) frame draw bottlenecks: simplify polyline via Ramer-Douglas-Peucker (`epsilon = 1.5px`) prior to spline sampling.
- Frame count rounding drift (`duration_sec = 7.33s * 30 = 219.9`): compute exact `nb_frames = round(duration_sec * 30)` and normalize progress `t = frame_idx / max(1, nb_frames - 1)` so final frame always reaches `t = 1.0`.

#### Bug Prevention And Invariants
- Output video streams MUST pass `ffprobe` `30/1` CFR check (`exact nb_frames`).
- Keep Manim optional behind a clean pure-PIL fallback so headless Docker/Windows/Linux CI runners require zero heavy LaTeX/Cairo installs for core tests.

#### Independent Testability & Parallel Isolation
- Offline pure Python math/PIL tests runnable in `<2s` without GPU or external media.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/python_motion/tests/test_trajectory_engine.py` verifying spline geometry, edge-case zero-length paths, and exact `CFR 30fps` frame counts.
- **Acceptance:** Mathematical trajectory generator works portably without LaTeX bloat.

### Task 137: Build Procedural SciPy Documentary SFX WAV Synthesizer (`packages/python_motion`)
- **Owner:** Developer B (Part 2) | **Milestone:** M1-P2 | **Depends on:** Task 004
- **Files:** `packages/python_motion/src/python_motion/sfx_synth.py`, `packages/python_motion/tests/test_sfx_synth.py`
- **Tests:** Spectral, sample-rate (`48,000 Hz`), bit-depth (`PCM 16-bit`), peak-dBFS (`<= -3.0 dBFS`), and DC-offset (`< 0.001`) verification across all 10 procedural documentary SFX cues.

#### Scope And Implementation Requirements
- Implement zero-copyright procedural audio synthesis (`SciPy` + `NumPy`) generating crisp, dry, clean `48 kHz / mono or stereo / 16-bit PCM` WAV files for every `sfx_cue` referenced by `SceneSpec` manifests—removing any reliance on external copyright-encumbered SFX packs.
- Synthesize 10 foundational true-crime documentary cues parameterized by seed/duration/intensity: `typewriter_key`, `stamp_thud`, `paper_slide`, `bass_drop_hit`, `tension_drone_pulse`, `camera_shutter`, `redaction_swipe`, `map_pin_pop`, `police_beep_clean`, and `subtle_whoosh`.
- Apply deterministic attack/decay/release envelopes (`ADSR`), `20 Hz` high-pass DC-blocking filter, and `5 ms` fade-in/out ramps to eliminate digital click/pop transients.
- Cache synthesized cues deterministically by `(cue_type, variant_seed, duration_ms)` inside `workspace/sfx_cache/`.

#### Edge Cases And Failure Modes
- Ultra-short cue duration (`< 40 ms` typewriter click) with naive `20 ms` fade-in/out swallowing the transient attack: clamp fade-out dynamically to `min(5 ms, total_samples // 4)` while preserving sharp `1 ms` percussive onset.
- Low-frequency `bass_drop_hit` clipping past `0 dBFS` when additive sub-harmonics sum constructively: peak-normalize strictly to `-3.0 dBFS` (`0.7079` linear max) prior to 16-bit PCM quantization.
- Invalid or unknown `cue_type` string emitted by LLM manifest: map deterministically via semantic alias lookup table (e.g., `gavel -> stamp_thud`, `click -> typewriter_key`) with safe `paper_slide` default and structured warning log (zero pipeline crash).

#### Bug Prevention And Invariants
- Never synthesize anything resembling siren sweeps or 911 rings that could confuse viewers or conflict with authentic FOIA Track 2 audio.
- Every WAV file emitted MUST read back via `scipy.io.wavfile` / `ffprobe` as exact `pcm_s16le`, `48000 Hz`, zero NaN/Inf samples.

#### Independent Testability & Parallel Isolation
- Offline deterministic synthesis testable in `<1s` with zero external sound packs.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/python_motion/tests/test_sfx_synth.py` verifying all 10 cues + alias fallback, spectral peaks, zero DC offset, and `48 kHz PCM` headers.
- **Acceptance:** Royalty-free, copyright-safe procedural SFX library delivers deterministic 48kHz documentary cues.

### Task 138: Implement 480p Pre-Flight Animatic Wireframe Cards (`packages/python_motion`)
- **Owner:** Developer B (Part 2) | **Milestone:** M1-P2 | **Depends on:** Task 135, Task 137
- **Files:** `packages/python_motion/src/python_motion/animatic_builder.py`, `packages/python_motion/tests/test_animatic_builder.py`
- **Tests:** Full-episode 1,200s 480p pre-flight wireframe MP4 assembly test verifying `<25s` build time, scene-ID slate burn-in, and exact duration parity with `manifest.json`.

#### Scope And Implementation Requirements
- Implement the **480p Pre-Flight Animatic Generator** so creators (or CI golden tests) can review an entire 20-minute episode's pacing, audio L-cuts, FOIA timing, 2K pan bounds, and Hero clip placement in `< 25 seconds` BEFORE spending `$6.00` (Headless Veo API) or human Batch Desk shifts.
- For each scene in `manifest.json`, render a crisp `854x480` wireframe slate card displaying: `scene_id`, engine badge (`CODE` / `2K` / `FLOW_HERO` / `FOIA`), word count + kinetic timing bar, Start/End thumbnail preview (for Flow) or `10x10` red target crop preview (for 2K), and active Voice/FOIA track waveform ribbon.
- Multiplex the wireframe sequence with the segmented Track 1 Voice + Track 2 FOIA preview WAV at `CFR 30fps` using hardware/fast `-preset ultrafast` FFmpeg muxing.
- Output `artifacts/animatic/<episode_id>_preflight_480p.mp4` and machine-readable pacing telemetry (`max_code_streak_sec`, `hero_clip_count`, `total_duration_sec`).

#### Edge Cases And Failure Modes
- Rendering 180 individual micro-scenes cleanly in `< 25s`: never encode 180 separate FFmpeg child processes—stream raw RGB frames per distinct card into FFmpeg concat demuxer with exact `duration` directives, generating 1 card PNG per scene and repeating cleanly at `30 fps`.
- Missing FOIA media preview file during Part 2 standalone test: synthesize clean `48 kHz` slate tone / silence placeholder matching `duration_sec` and annotate `[FOIA STUB]` on the wireframe card.
- Duration rounding mismatch between concat demuxer floats and exact `nb_frames`: drive concat durations directly from exact integer millisecond `duration_ms` / `30 fps` frame counts.

#### Bug Prevention And Invariants
- Animatic duration MUST match `sum(scene.duration_sec)` within `+/-0.1s`.
- Zero `FLOW_HERO` API calls or credit debits may ever happen inside `animatic_builder`.

#### Independent Testability & Parallel Isolation
- Tested standalone using golden stub manifests (`ep_golden_01.json`) and local FFmpeg binary.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/python_motion/tests/test_animatic_builder.py` generating a 1,200s wireframe animatic in `<25s` and verifying `ffprobe` stream integrity.
- **Acceptance:** Fast pre-flight editorial pacing review works before any Flow spend occurs.

### Task 139: Implement SHA-256 Asset Cache & Keyframe Indexer (`packages/python_motion`)
- **Owner:** Developer B (Part 2) | **Milestone:** M1-P2 | **Depends on:** Task 135, Task 137
- **Files:** `packages/python_motion/src/python_motion/asset_cache.py`, `packages/python_motion/tests/test_asset_cache.py`
- **Tests:** Cache hit/miss, palette-hash invalidation, partial-write atomic rename, and concurrent read-safe lookup tests.

#### Scope And Implementation Requirements
- Implement content-addressed caching (`SHA-256` over normalized `SceneSpec` visual payload + `CaseBible` palette version + generator version) for Python-generated bookends, trajectory overlays, and procedural SFX WAVs.
- Enforce atomic file promotion (`write .tmp -> fsync -> os.replace`) so interrupted overnight processes or parallel worker threads never read half-written PNGs or truncated WAV headers.
- Provide `prune_stale(max_age_days=30)` and cache-hit telemetry metrics emitted to `telemetry_events` (via Python API callback or local JSON log in standalone mode).

#### Edge Cases And Failure Modes
- Upstream `CaseBible` accent color changes while scene `prompt` stays identical: include `case_bible_hash` in cache key calculation so stale palette PNGs are automatically invalidated cleanly.
- Disk full during large batch PNG write: catch `OSError` during `.tmp` write, unlink `.tmp`, and surface typed `CacheStorageError` rather than leaving corrupt cache slots.

#### Bug Prevention And Invariants
- Cache readers MUST verify file existence and magic header (`PNG` / `RIFF`) before returning a hit; treat corrupt cache files transparently as cache miss and overwrite atomically.

#### Independent Testability & Parallel Isolation
- Pure local filesystem unit tests using `pytest` `tmp_path` fixture.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/python_motion/tests/test_asset_cache.py` verifying zero corrupt reads on simulated `.tmp` crashes and 100% cache hit reuse on identical inputs.
- **Acceptance:** Atomic deterministic asset caching eliminates redundant Python rendering.

### Task 140: Write Adversarial `python_motion` Gauntlet Tests (`packages/python_motion`)
- **Owner:** Developer B (Part 2) | **Milestone:** M1-P2 | **Depends on:** Task 134, Task 135, Task 136, Task 137
- **Files:** `packages/python_motion/tests/test_adversarial_gauntlet.py`
- **Tests:** Adversarial test suite injecting forbidden crimson keyframe injections, corrupt WAV duration edges, extreme aspect/coordinate inputs, and unknown SFX cue aliases.

#### Scope And Implementation Requirements
- Build a comprehensive adversarial verification suite attacking every boundary of `packages/python_motion`:
  - Attempt to force `#C92A2A` crimson into Start/End PNGs via nested `SceneSpec` props -> verify stripping + validator rejection if raw.
  - Inject zero-duration (`0.0s`) and ultra-long (`180s`) scene edges -> verify bounded clamping or clean typed `ValueError`.
  - Test skin-tone false-positive resistance against warm parchment lighting vs actual realistic human face patch rejection.
  - Verify `500`-cue batch SFX generation memory ceiling (`< 250 MB` RSS) and deterministic byte hashes across repeated runs.

#### Edge Cases And Failure Modes
- Parallel `pytest -n auto` execution sharing a static cache folder: enforce unique `tmp_path` isolation per test function.

#### Bug Prevention And Invariants
- Zero unhandled exceptions (`KeyError`, `ZeroDivisionError`, `PIL.UnidentifiedImageError`) across the entire fuzz vector matrix.

#### Independent Testability & Parallel Isolation
- Fully self-contained offline test suite runnable in CI without external binaries beyond standard Python + FFmpeg.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/python_motion/tests/test_adversarial_gauntlet.py` with 100% pass.
- **Acceptance:** `python_motion` edge cases and safety guards hold under adversarial stress.

### Task 141: Implement Unified `python_motion` Service CLI & API (`packages/python_motion`)
- **Owner:** Developer B (Part 2) | **Milestone:** M1-P2 | **Depends on:** Task 138, Task 139, Task 140
- **Files:** `packages/python_motion/src/python_motion/service.py`, `packages/python_motion/src/python_motion/__init__.py`, `packages/python_motion/tests/test_service_e2e.py`
- **Tests:** End-to-end CLI/Python API invocation generating bookends, 10 SFX cues, trajectories, and a 480p pre-flight animatic for `ep_golden_01.json`.

#### Scope And Implementation Requirements
- Expose clean Python module API (`MotionAssetService`) and CLI (`python -m python_motion build --manifest ... --out-dir ...`) unifying bookend PNG generation, Law 12 safety checks, procedural SFX synthesis, trajectory MP4s, and optional `--animatic` output.
- Produce a structured `motion_assets_report.json` mapping every `FLOW_HERO_VIDEO` scene ID to validated Start/End PNG paths + SHA-256 checksums + `ImageSafetyVerdict`, and every `sfx_cue` to its `48 kHz PCM` WAV path.
- Ensure cleanly typed Pydantic v2 models (`contracts/schemas`) for every input/output boundary.

#### Edge Cases And Failure Modes
- Partial manifest run (`--only-sfx` or `--only-bookends`): support selective stage flags cleanly without regenerating unaffected assets.
- Relative vs absolute paths on Windows (`\`) vs Linux (`/`): normalize all emitted JSON paths consistently via `pathlib.Path.as_posix()`.

#### Bug Prevention And Invariants
- Never return exit code `0` if ANY Flow Start/End pair fails `InputImageSafetyValidator`.

#### Independent Testability & Parallel Isolation
- E2E tests execute cleanly on `fixtures/ep_golden_01.json` in Part 2 isolation.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/python_motion/tests/test_service_e2e.py` verifying complete `motion_assets_report.json` generation on golden fixture.
- **Acceptance:** Unified `python_motion` asset synthesizer cleanly integrates with Flow adapter and Agent 6.

### Task 142: Verify `python_motion` Performance & Deterministic Replay Check (`packages/python_motion`)
- **Owner:** Developer B (Part 2) | **Milestone:** M1-P2 | **Depends on:** Task 141
- **Files:** `packages/python_motion/tests/test_determinism_replay.py`
- **Tests:** Bit-for-bit replay test executing two clean runs of `MotionAssetService` across 20 scenes + 50 SFX cues and asserting identical output digests and `<15s` runtime.

#### Scope And Implementation Requirements
- Execute clean-cache replay verification proving `packages/python_motion` is 100% deterministic across runs (matching SHA-256 hashes on all PNG keyframes, WAV files, and `motion_assets_report.json` modulo execution wall-clock fields).
- Assert total execution wall-clock time for a standard episode's bookends + SFX cues + trajectories completes in `< 15 seconds` locally without GPU.
- Document exact package version pins (`Pillow`, `scipy`, `numpy`, `opencv-python-headless`) in `pyproject.toml`.

#### Edge Cases And Failure Modes
- Timestamp metadata inside PNG `tEXt` chunks or WAV `LIST/INFO` chunks breaking byte-for-byte replay checks: strip all wall-clock timestamps from binary headers on creation.

#### Bug Prevention And Invariants
- Enforce deterministic `pnginfo=None` and fixed `numpy.random.Generator(PCG64(seed))` everywhere in `python_motion`.

#### Independent Testability & Parallel Isolation
- Standalone Part 2 CI check requiring no Part 1 packages.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/python_motion/tests/test_determinism_replay.py` and confirm 100% checksum match across dual cold runs in `<15s`.
- **Acceptance:** `packages/python_motion` passes deterministic replay and latency bounds.

### Task 143: Bootstrap `crime_scene_2k` & Pre-Locked Spatial Anchor Loader (`packages/crime_scene_2k`)
- **Owner:** Developer B (Part 2) | **Milestone:** M1-P2 | **Depends on:** Task 002, Task 004
- **Files:** `packages/crime_scene_2k/pyproject.toml`, `packages/crime_scene_2k/src/crime_scene_2k/anchor_loader.py`, `packages/crime_scene_2k/tests/test_anchor_loader.py`
- **Tests:** Loader & Pydantic schema validation tests against Part 1's pre-locked `spatial_anchors` JSON schema (`col`, `row`, `span_cols`, `span_rows`, `x_px`, `y_px`, `target_zoom`).

#### Scope And Implementation Requirements
- Bootstrap `packages/crime_scene_2k` (Python 3.12, OpenCV, NumPy, Pillow) consuming Part 1's **clean 2K+ crime-scene stills** (`>= 2048px` wide) and **already-locked `spatial_anchors`** produced early right after Agent 2 (`Task 042`, **resolving Law 4 circular deadlock cleanly**).
- Validate each `SpatialAnchor` record: grid cell (`col` `A–J`, `row` `1–10`), object footprint (`span_cols` `1..10`, `span_rows` `1..10`), exact pixel center `(x_px, y_px)` relative to the clean 2K PNG dimensions `(W, H)`, and target zoom tier.
- Verify that the clean 2K PNG itself contains ZERO baked-in grid borders (`10x10` grids are rendered ONLY into external margins for VLM inspection in Agent 2, never burned into the source 2K render PNG).
- Fail cleanly with typed `AnchorBoundsError` if any anchor coordinate falls outside `[0, W] x [0, H]` or references a low-res still (`width < 1920`).

#### Edge Cases And Failure Modes
- Part 1 hands over an anchor containing `col/row` + `span_cols/span_rows` without precomputed `x_px/y_px` (or vice versa): deterministically derive missing pixel centers from cell center `((col_idx + 0.5) / 10) * W` and validate consistency within `+/-1 cell` when both are provided.
- Non-16:9 2K source still (e.g., `2560x1600` or `2048x1152`): compute aspect-normalized crop math directly from actual image `(W, H)` while keeping output frame strictly `1920x1080`.
- Missing image file or zero-byte corrupt PNG: fail fast with typed `Missing2KAssetError` before allocating OpenCV frame buffers.

#### Bug Prevention And Invariants
- `packages/crime_scene_2k` MUST remain a pure read-only consumer of Part 1's pre-locked `spatial_anchors` + clean 2K still (never re-runs VLM coordinate inference or modifies Part 1's DB ledger).
- Enforce resolution gate `W >= 1920 and H >= 1080` (`>= 2048px` preferred) before zooming so output pixels never upscale past native 1080p budget.

#### Independent Testability & Parallel Isolation
- Tested standalone using frozen golden 2K PNGs and pre-locked `spatial_anchors` fixtures from Task 004.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/crime_scene_2k/tests/test_anchor_loader.py` confirming 100% validation pass on golden `spatial_anchors` and rejection on corrupt/undersized assets.
- **Acceptance:** Law 4 early-anchor handoff contract is cleanly enforced in `crime_scene_2k`.

### Task 144: Implement External-Margin `A–J / 1–10` Inspection Overlay Utility (`packages/crime_scene_2k`)
- **Owner:** Developer B (Part 2) | **Milestone:** M1-P2 | **Depends on:** Task 143
- **Files:** `packages/crime_scene_2k/src/crime_scene_2k/margin_grid.py`, `packages/crime_scene_2k/tests/test_margin_grid.py`
- **Tests:** Margin border geometry tests verifying zero grid lines pollute inner scene pixels and accurate `A–J` / `1–10` alignment on `16:9` 2K inputs.

#### Scope And Implementation Requirements
- Implement the deterministic **External-Margin `10x10` Grid Visualizer** (`margin_grid.py`) used by automated QA, Part 2 UI inspection previews, and shared visual calibration with Agent 2 (`Task 042`).
- Pad the clean 2K PNG with a `+64px` top/bottom/left/right charcoal margin border (`W+128 x H+128`), draw crisp high-contrast `A–J` column ticks across top/bottom margins and `1–10` row ticks across left/right margins, and draw ultra-faint `12%` opacity hairlines ONLY in inspection copies—never modifying the clean render PNG on disk.
- Optionally overlay anchor bounding footprints (`span_cols x span_rows`) and target crop boxes onto the inspection copy for creator visual verification in the Batch Desk `2K Spatial Inspector` tab.

#### Edge Cases And Failure Modes
- Source PNG dimensions not cleanly divisible by 10 (e.g., `2048px / 10 = 204.8px`): compute floating-point grid intervals `(x_i = margin + round(i * W / 10))` so column `J` terminates cleanly at the exact right edge without `8px` cumulative drift.
- High-key bright parchment corner washing out white tick labels: paint solid `#1B1B1D` charcoal margin frame outside the image bounds so `#E9E2D2` labels always achieve `>= 11:1` WCAG AAA contrast.

#### Bug Prevention And Invariants
- Return a new annotated inspection image buffer/file (`*_grid_preview.png`); NEVER overwrite or mutate the clean source 2K PNG path.

#### Independent Testability & Parallel Isolation
- Offline Pillow/OpenCV pixel tests verifying interior pixel SHA-256 identity when grid margin is stripped back off.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/crime_scene_2k/tests/test_margin_grid.py` confirming pixel-exact alignment and unaltered inner clean buffer.
- **Acceptance:** External-margin grid visualization matches Part 1 Agent 2 calibration geometry cleanly.

### Task 145: Implement Span-Based `1.6x–3.8x` Zoom Sizing & Edge Crop Clamper (`packages/crime_scene_2k`)
- **Owner:** Developer B (Part 2) | **Milestone:** M1-P2 | **Depends on:** Task 143
- **Files:** `packages/crime_scene_2k/src/crime_scene_2k/crop_math.py`, `packages/crime_scene_2k/tests/test_crop_math.py`
- **Tests:** Boundary unit tests covering center cells (`E5`), extreme corners (`A1`, `J10`, `A10`, `J1`), narrow objects (`1x1` -> `3.8x` cap), and wide objects (`5x3` -> `1.6x` floor).

#### Scope And Implementation Requirements
- Implement **Span-Based Zoom Sizing & Edge Clamping** solving two classic Ken Burns bugs: zooming too tightly onto multi-cell props (clipping a table or hallway) and panning past `[0, W] x [0, H]` bounds on corner anchors (`A1`, `J10`):
  1. Compute object-derived zoom: derive ideal crop width from `span_cols` + `25%` contextual breathing margin (`crop_w = (span_cols / 10.0) * W * 1.25`, `zoom = W / crop_w`), and clamp strictly inside **`[1.6, 3.8]`** (`target_zoom` override respected if within safe native-1080p bounds `<= W / 1080` or `3.8x`).
  2. Maintain strict `16:9` crop aspect ratio (`crop_h = crop_w * 9 / 16`).
  3. **Edge-Clamped Crop Window:** Compute naive centered box `[cx - crop_w/2, cy - crop_h/2]`, then clamp cleanly so `x0 = clamp(cx - crop_w/2, 0, W - crop_w)` and `y0 = clamp(cy - crop_h/2, 0, H - crop_h)`—eliminating black out-of-bounds bars cleanly without changing zoom magnitude.

#### Edge Cases And Failure Modes
- Object spans `span_rows = 4` vertically while `span_cols = 1` horizontally (e.g., tall doorway silhouette): compute `zoom_x` from `span_cols` and `zoom_y` from `span_rows`, taking `min(zoom_x, zoom_y)` before clamping to `[1.6, 3.8]` so vertical extents never get clipped top/bottom.
- Source image smaller than `2560x1440` (e.g., `2048x1152`): allow zoom up to `3.8x` only via Lanczos resampling if `crop_w >= 540`, logging upscale factor cleanly; prefer `2K/4K` sources where `crop_w >= 720`.
- Extreme corner anchor (`A1`, pixel center `x_px=100, y_px=60`) with `zoom=3.2x`: clamping shifts the crop box inward to `(0, 0)`, leaving the target point off-center inside the clamped viewport (handled explicitly in Task 146).

#### Bug Prevention And Invariants
- Asserted invariant for every time `t in [0, 1]`: `0 <= x0 <= x0 + crop_w <= W` and `0 <= y0 <= y0 + crop_h <= H`, plus `abs((crop_w / crop_h) - (16/9)) < 1e-4`.

#### Independent Testability & Parallel Isolation
- Fast deterministic math tests (`<0.5s`) requiring zero GPU or external dependencies.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/crime_scene_2k/tests/test_crop_math.py` testing all 4 corners (`A1`, `J1`, `A10`, `J10`), narrow `1x1` spans, tall `1x4` spans, and wide `6x4` spans.
- **Acceptance:** Zero black-border crops and mathematically bounded object framing guaranteed across all anchors.

### Task 146: Implement Screen-Space Projected Callout Circles (`packages/crime_scene_2k`)
- **Owner:** Developer B (Part 2) | **Milestone:** M1-P2 | **Depends on:** Task 145
- **Files:** `packages/crime_scene_2k/src/crime_scene_2k/callout_projector.py`, `packages/crime_scene_2k/tests/test_callout_projector.py`
- **Tests:** Screen-space coordinate tests proving red/crimson focus circles track exact anchor centers (`A1`/`J10` clamped cases and mid-pan trajectories) within `<= 1.0 px` accuracy.

#### Scope And Implementation Requirements
- **CRITICAL AUDIT FIX (Edge-Clamped Callout Drift Fix):** Never hardcode red callout circles to screen center `(960, 540)`. Whenever the camera crop window `[x0(t), y0(t), crop_w(t), crop_h(t)]` clamps against an image boundary (`A1`, `J10`), the true anchor point `(anchor.x_px, anchor.y_px)` sits offset inside the frame, NOT at `(960, 540)`!
- Compute per-frame exact projection from source-pixel space to `1920x1080` screen space:
  `x_screen(t) = ((anchor.x_px - x0(t)) / crop_w(t)) * 1920.0`
  `y_screen(t) = ((anchor.y_px - y0(t)) / crop_h(t)) * 1080.0`
- Render vector-crisp documentary crimson (`#C92A2A` / `CaseBible.evidenceCrimsonHex`) animated target ring + pulsing tick bracket + optional short leader line & uppercase courier caption safely offset away from the screen border (`safe_label_x`, `safe_label_y` clamped inside `10%` title-safe margins).

#### Edge Cases And Failure Modes
- Anchor sits close to corner `A1`: target circle sits near top-left (`~180, 120` in screen space); label MUST automatically flip downward/rightward so the text caption never overflows past screen left/top margin (`RULE_07` / Safe-Zone).
- Multi-hop pan between `Anchor 1 -> Anchor 2 -> Anchor 3` inside a single `10s–18s` still tour: smoothly deactivate Callout 1 during transition travel (`fade_out 0.25s`) and activate Callout 2 upon lock-on (`draw_in 0.35s`), projecting each strictly using instantaneous `(x0(t), y0(t), crop_w(t), crop_h(t))`.
- Unclamped center anchor (`E5` far from edges): verify `x_screen == 960.0 +/- 0.5` and `y_screen == 540.0 +/- 0.5` at rest as the exact degenerate special case.

#### Bug Prevention And Invariants
- Assert every rendered screen-space callout ring center `(x_screen, y_screen)` maps back to exact source-pixel `(anchor.x_px, anchor.y_px)` within `< 1.0px` source tolerance.
- Callout caption rectangles MUST pass Task 126's Safe-Zone pixel boundaries (`margin >= 96px` horizontal, `margin >= 54px` vertical).

#### Independent Testability & Parallel Isolation
- Offline mathematical & rendered-dot pixel localization tests verifying bright crimson dot centroid matches projected `(x_screen, y_screen)` on `A1` and `J10` test plates.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/crime_scene_2k/tests/test_callout_projector.py` asserting `< 1.0px` localization accuracy on `A1`, `J1`, `A10`, `J10`, and `E5` scenes.
- **Acceptance:** Edge-clamped camera pans never detach crimson evidence circles from their true scene props.

### Task 147: Build Sub-Pixel OpenCV `INTER_LANCZOS4` Camera Engine (`packages/crime_scene_2k`)
- **Owner:** Developer B (Part 2) | **Milestone:** M1-P2 | **Depends on:** Task 145, Task 146
- **Files:** `packages/crime_scene_2k/src/crime_scene_2k/lanczos_renderer.py`, `packages/crime_scene_2k/tests/test_lanczos_renderer.py`
- **Tests:** `cv2.warpAffine(..., flags=cv2.INTER_LANCZOS4)` sub-pixel jitter benchmark, 30fps CFR MP4 validity check, and memory-footprint limit test.

#### Scope And Implementation Requirements
- Implement the sub-pixel floating-point camera pan/zoom renderer (`lanczos_renderer.py`) using OpenCV `cv2.warpAffine` with `cv2.INTER_LANCZOS4` and float32 affine crop matrices (`M`) to guarantee silky-smooth micro-pans free of integer rounding judder (`1px` stair-stepping).
- Interpolate camera center `(cx(t), cy(t))` and zoom `z(t)` using smooth C2 cubic-bezier / quintic easing between waypoints (`hold -> travel -> hold`), ensuring zero abrupt velocity discontinuities (`v(0) = 0`, `v(T) = 0`).
- Stream BGR frames directly into FFmpeg subprocess (`-f rawvideo -pix_fmt bgr24 -s 1920x1080 -r 30 -c:v libx264 -pix_fmt yuv420p -crf 15 -preset medium`) to produce clean, ungraded `CFR 30fps` intermediate MP4 clips ready for Agent 6's unified single-pass grain/vignette grade (`Task 168`).
- Overlay vector-crisp screen-space callouts (`Task 146`) on top of each warped `1920x1080` frame BEFORE piping to FFmpeg.

#### Edge Cases And Failure Modes
- Pipe deadlock (`BrokenPipeError`) when FFmpeg rejects parameters or closes early: read FFmpeg `stderr` non-blockingly / communicate cleanly and include full FFmpeg diagnostic output in `LanczosRenderError`.
- Lanczos ringing overshoot near sharp crimson callout overlays if callouts were drawn *before* `warpAffine`: strictly draw callouts AFTER `warpAffine` at native `1920x1080` resolution so text and target circles never suffer zoom blur or ringing halos.
- Frame rate jitter or missing final frame: assert `frame_idx` spans `0 .. round(duration_sec * 30) - 1` and verify `ffprobe` `nb_frames` equals expected count.

#### Bug Prevention And Invariants
- Never add film grain or vignette inside `crime_scene_2k`; emit clean ungraded `1920x1080` MP4 + `scene_grade_manifest.json` tag (`apply_grain: true`) so Agent 6 executes one unified continuous grain pass.
- Ensure pixel bounds strictly avoid OpenCV out-of-range border extrapolation (`BORDER_REPLICATE` used strictly as harmless numerical safety net because Task 145 guarantees `[0, W] x [0, H]` interior crops).

#### Independent Testability & Parallel Isolation
- Tested standalone using synthetic 2K architectural grid test plates (`2560x1440`) and local FFmpeg.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/crime_scene_2k/tests/test_lanczos_renderer.py` verifying zero integer stair-stepping (`max frame-to-frame optical flow variance smooth`) and exact `30/1` CFR stream.
- **Acceptance:** Sub-pixel Lanczos 2K camera engine delivers crisp judder-free documentary movement.

### Task 148: Build Multi-Scene 2K Spatial Tour Sequencer (`packages/crime_scene_2k`)
- **Owner:** Developer B (Part 2) | **Milestone:** M1-P2 | **Depends on:** Task 147
- **Files:** `packages/crime_scene_2k/src/crime_scene_2k/tour_sequencer.py`, `packages/crime_scene_2k/tests/test_tour_sequencer.py`
- **Tests:** 50-second multi-anchor guided still tour test (establishing wide shot -> `Anchor A` -> `Anchor B` -> `Anchor C`) checking beat synchronization and zero jarring snap cuts.

#### Scope And Implementation Requirements
- Implement `SpatialTourSequencer` translating multi-anchor `STILL_2K_PANZOOM` scene blocks (covering ~`5.67 min / 340s` per episode across 6–7 illustrative 2K stills without spending any paid video budget) into cohesive `10s–50s` animated spatial walkthroughs.
- Synchronize camera arrival timestamps (`hold_start`, `hold_end`) directly against `voice_segments` cue timestamps (`words` timestamps inside `SceneSpec`) so the camera finishes panning right as the narrator speaks the target clue phrase (`"near the entryway"`, `"beside the overturned chair"`).
- Support smooth dwell (`1.5%` ultra-slow breathing drift during narration beats so frames never look statically frozen) and cross-anchor travel curves (`0.9s–1.6s` smooth swoop).
- Emit updated `scene_grade_manifest.json` records for every generated `STILL_2K_PANZOOM` MP4.

#### Edge Cases And Failure Modes
- Narration cue arrives `0.3s` into the scene leaving insufficient travel time from initial wide overview: start initial wide zoom slightly closer or speed travel curve within `[0.45s, 2.0s]` bounds while preserving smooth velocity ease.
- Two consecutive anchors located at opposite corners (`A1` -> `J10`): optionally insert brief zoom-out apex (`1.4x -> 1.15x -> 2.6x`) mid-flight (classic parabolic Ken Burns swoop) so cross-room transitions orient the viewer geographically rather than blurring fast across the floor.
- Scene contains zero spatial anchors (pure atmospheric wide establisher): synthesize gentle slow `1.0x -> 1.18x` center-weighted documentary push cleanly.

#### Bug Prevention And Invariants
- Sum of segment frame counts MUST equal `round(scene.duration_sec * 30)` within `0` frames (`+/- 0.00s` drift).
- Never exceed `3.8x` peak zoom on any frame in the parabolic flight curve.

#### Independent Testability & Parallel Isolation
- Tested offline using golden multi-anchor fixtures (`fixtures/ep_golden_01.json`) and a single 2K placeholder diagram.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/crime_scene_2k/tests/test_tour_sequencer.py` validating a `50.0s` 4-anchor guided tour (`1,500` frames exact) and parabolic swoop math.
- **Acceptance:** Guided multi-anchor 2K spatial tours execute cleanly with exact voice-word cue sync.

### Task 149: Run Reproducible 2K Spatial Grounding & Screen-Projection Benchmark (`packages/crime_scene_2k`)
- **Owner:** Developer B (Part 2) | **Milestone:** M1-P2 | **Depends on:** Task 146, Task 148
- **Files:** `packages/crime_scene_2k/tests/test_drift_regression.py`
- **Tests:** Reproducible pixel-measured localization benchmark comparing naive directional heuristics (testing the motivating spatial-miss hypothesis) against locked `10x10` anchors + screen-space projection (`<= 1.0px` projected callout accuracy) + mandatory `ILLUSTRATIVE RECONSTRUCTION` watermark check (`F-05`, `F-21`).

#### Scope And Implementation Requirements
- Implement the reproducible verification harness (`test_drift_regression.py`) across 20 diverse illustrative 2K layouts (corner doors `A1`, cluttered desks `F4`, side windows `J6`, edge hallways `B9`), recording full machine/version/seed metadata into `artifacts/benchmarks/2k_spatial_localization.json` (`F-21`).
- Measure empirical Euclidean pixel miss distance between rendered crimson callout centroids and ground-truth synthetic marker centroids:
  - Baseline naive directional prompt (`"left side"`, `"upper corner"`): measure empirical miss rate directly (treating prior `71.7%` literature/note figure as an unverified motivating hypothesis, NOT a hardcoded claim!).
  - Locked `10x10` `spatial_anchors` + `span_cols`/`span_rows` + edge-clamped screen projection: assert **all 20 layouts** keep target inside `[0, 1920] x [0, 1080]` safe viewport with crimson circle centered within `<= 1.0px` AND verify the **`ILLUSTRATIVE RECONSTRUCTION — NOT CRIME SCENE PHOTO`** label renders inside safe margins (`F-05`).

#### Edge Cases And Failure Modes
- Non-square aspect props (`4x1` horizontal counter vs `1x4` vertical bookcase): assert zoom selection keeps 100% of prop bounding polygon inside screen bounds rather than only centering the dot.

#### Bug Prevention And Invariants
- Never hardcode passing metrics—render actual high-contrast geometric marker scenes and measure centroid pixels from rendered output frames using OpenCV contour detection!

#### Independent Testability & Parallel Isolation
- Offline pixel-measured test suite runnable directly in Part 2 CI.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/crime_scene_2k/tests/test_drift_regression.py` confirming actual OpenCV-measured crimson circle localization `< 1.0px` across all 20 ground-truth anchor layouts.
- **Acceptance:** End-to-end 2K pan accuracy and callout screen projection empirically proven on rendered pixels.

### Task 150: Build Batch Renderer & CLI for `crime_scene_2k` (`packages/crime_scene_2k`)
- **Owner:** Developer B (Part 2) | **Milestone:** M1-P2 | **Depends on:** Task 148, Task 149
- **Files:** `packages/crime_scene_2k/src/crime_scene_2k/cli.py`, `packages/crime_scene_2k/src/crime_scene_2k/__init__.py`, `packages/crime_scene_2k/tests/test_cli_batch.py`
- **Tests:** CLI batch execution tests rendering all `STILL_2K_PANZOOM` scenes from golden episode manifest, outputting `340s` cumulative clean `CFR 30fps` MP4 clips + JSON manifest + mandatory `ILLUSTRATIVE RECONSTRUCTION` watermark.

#### Scope And Implementation Requirements
- Expose `crime-scene-2k` CLI and Python `CrimeScene2KService` API consumed by Part 2 workers and Agent 6 heal/batch pipelines (`crime-scene-2k render --manifest <path> --stills-dir <dir> --out-dir <dir> --scene <id?>`).
- Parallelize frame rendering across up to `min(4, cpu_count)` worker threads/processes on independent `STILL_2K_PANZOOM` scenes while tracking wall-clock durations cleanly.
- Support `--scene <scene_id>` single-scene surgical re-render (matching `@tc/render_catalog` parity for Agent 6 `<5s` / fast heal loops).
- Emit `2k_render_report.json` summarizing rendered MP4 paths, `nb_frames`, edge-clamp flags, peak zoom applied per scene, and `scene_grade_manifest.json` contributions.

#### Edge Cases And Failure Modes
- Manifest contains `STILL_2K_PANZOOM` scene whose referenced `still_asset_id` is absent in `--stills-dir`: fail cleanly before spawning worker pool with structured missing-asset list.
- Multiple scenes referencing the same 2K master PNG simultaneously across worker processes: open source PNG cleanly read-only per worker (zero shared mutable handles).

#### Bug Prevention And Invariants
- All rendered MP4 clips MUST verify exact `30/1` CFR and `1920x1080` dimensions via `ffprobe` before reporting success.

#### Independent Testability & Parallel Isolation
- Tested standalone with `fixtures/ep_golden_01.json` in Part 2 isolation.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/crime_scene_2k/tests/test_cli_batch.py` verifying batch + single `--scene` execution and valid `2k_render_report.json`.
- **Acceptance:** `crime_scene_2k` CLI and worker API ready for Part 2 batch production.

### Task 151: Harden `crime_scene_2k` Against Extreme Resolution & Aspect Edge Cases (`packages/crime_scene_2k`)
- **Owner:** Developer B (Part 2) | **Milestone:** M1-P2 | **Depends on:** Task 150
- **Files:** `packages/crime_scene_2k/tests/test_aspect_stress.py`
- **Tests:** Stress test matrix covering `4K` (`3840x2160`), `2K` (`2560x1440`), `2048x1152`, `2048x1536` (`4:3` photo still), invalid `< 1920px` rejection, and `0.5s` micro-clip edges.

#### Scope And Implementation Requirements
- Exercise `crime_scene_2k` across diverse real-world image dimensions (standard `2560x1440`, exact `2048px`, `4:3` archival room still `2400x1800`, ultrawide panorama `3440x1440`, and `3840x2160` 4K).
- Ensure `4:3` stills automatically establish `16:9` crop windows strictly constrained within `0 <= crop_h <= H` without letterbox padding bars.
- Verify memory usage remains flat (`< 300 MB` per worker on `4K` PNG inputs) by loading source image once per scene and freeing NumPy arrays immediately upon FFmpeg pipe close.

#### Edge Cases And Failure Modes
- Ultrawide source panorama `3440x1440` where naive `W * 9/16` crop height exceeds `H` (`1935 > 1440`): compute `max_crop_w = min(W, H * 16 / 9)` as the true `zoom = 1.0x` wide ceiling before applying `[1.6, 3.8]` span zoom!
- Exif orientation tag (`Orientation=6` rotated phone still) accidentally embedded in PNG/JPG conversion: strip/apply `PIL.ImageOps.exif_transpose` cleanly at ingestion before measuring `(W, H)`.

#### Bug Prevention And Invariants
- Never letterbox or pillarbox inside `crime_scene_2k`; every output frame fills 100% of `1920x1080` pixels from real scene image content.

#### Independent Testability & Parallel Isolation
- Offline OpenCV stress suite runnable standalone in Part 2.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/crime_scene_2k/tests/test_aspect_stress.py` with 100% pass across all aspect ratios and EXIF rotations.
- **Acceptance:** `crime_scene_2k` handles varied 2K/4K/4:3/ultrawide assets safely without letterboxing or OOM.

### Task 152: Validate Milestone M1-P2 Visual Engines Exit Gate (`packages/render_catalog`, `python_motion`, `crime_scene_2k`)
- **Owner:** Developer B (Part 2) | **Milestone:** M1-P2 Exit Gate | **Depends on:** Task 132, Task 142, Task 151
- **Files:** `artifacts/milestones/M1_P2_EXIT_CHECK.md` (verification script `tools/verify_m1_p2.ps1`)
- **Tests:** Integrated Part 2 Milestone 1 check compiling `@tc/render_catalog` (all 12 motifs), `python_motion` (bookends + SFX + 480p animatic), and `crime_scene_2k` against `fixtures/ep_golden_01.json`.

#### Scope And Implementation Requirements
- Execute Milestone `M1-P2` verification gate proving Developer B's entire local visual generation stack works cohesively end-to-end on golden fixtures with ZERO live network APIs and ZERO Part 1 code dependencies:
  - `@tc/render_catalog`: 12 motifs rendered `CFR 30fps`, `<5s` JS-boil SLA, 0 `<feTurbulence>` nodes, `scene_grade_manifest.json` emitted.
  - `python_motion`: Flow Start/End PNG pairs verified monochrome (zero crimson), 10 SFX cues at `48 kHz PCM`, 480p animatic built in `<25s`.
  - `crime_scene_2k`: Guided `50s` tours rendered `CFR 30fps` cleanly from pre-locked `spatial_anchors` with `< 1.0px` projected callouts on `A1`/`J10`.
- Record exact timings, pass rates, and fixture checksums in `artifacts/milestones/M1_P2_EXIT_CHECK.md`.

#### Edge Cases And Failure Modes
- Windows vs Linux path normalization difference between TS (`@tc/render_catalog`) and Python (`crime_scene_2k`) JSON reports: verify shared POSIX path relative normalization inside `verify_m1_p2.ps1`.

#### Bug Prevention And Invariants
- Fail the Milestone gate if ANY manual edit was required to pass golden fixture compilation.

#### Independent Testability & Parallel Isolation
- 100% Developer B standalone verification before proceeding to Flow Adapter & Agent 6 (`M2-P2`).

#### Verification, Testing And Acceptance Criteria
- [ ] Run `tools/verify_m1_p2.ps1` and verify all 3 packages pass cleanly on `fixtures/ep_golden_01.json` with exit code `0`.
- **Acceptance:** Milestone `M1-P2` officially signed off cleanly.

### Task 153: Define `FlowAssetBackend` Protocol & `GeminiOmniInteractionsBackend` Primary Default (`packages/flow_adapter`)
- **Owner:** Developer B (Part 2) | **Milestone:** M0.5 / M2-P2 | **Depends on:** Task 004, Task 135
- **Files:** `packages/flow_adapter/pyproject.toml`, `packages/flow_adapter/src/flow_adapter/backend.py`, `packages/flow_adapter/src/flow_adapter/omni_interactions.py`, `packages/flow_adapter/tests/test_omni_interactions.py`
- **Tests:** Mocked `gemini-omni-1.2-flash` Interactions API + Files API unit tests validating `TEXT_TO_VIDEO` / `FIRST_FRAME` / `FIRST_AND_LAST_FRAME (<=10s)`, crash-safe `SUBMITTING -> RUNNING -> UNKNOWN_RECONCILE` reconciliation, durable `budget_reservations`, and a separate opt-in bounded live sandbox contract test (`<= $2.00` cap, `F-01`, `F-02`, `F-10`, `F-18`).

#### Scope And Implementation Requirements
- Bootstrap `packages/flow_adapter` implementing the abstract `FlowAssetBackend` interface with cleanly separated, **non-interchangeable** provider integrations selected via `providers.yaml`:
  1. **`GeminiOmniInteractionsBackend` (Primary Default, `GEMINI_OMNI_INTERACTIONS`):** Integrates directly with **`gemini-omni-1.2-flash`** via `google-genai >= 2.30.1` (`client.interactions.create` + Files API upload polled until `ACTIVE`, replacing retired Veo 3.1 Preview endpoints shut down Oct 22, 2026 — `F-01`).
     - Supports `TEXT_TO_VIDEO` (`3s–15s`, null frames), `FIRST_FRAME` (`3s–15s`), and `FIRST_AND_LAST_FRAME` (`3s–10s` max) at default `720p` (`16:9`), configurable timeout (`600s` default).
     - Enforces regional portability guard (text-to-video & image-keyframe-to-video only; flags video-upload edits/extensions as region-restricted in EEA/CH/UK/some US states).
     - **Single-Config Budget & Crash-Safe Dispatch (`F-02`, `F-10`, `F-18`):** Enforces `providers.yaml` single source of truth (`max_hero_clips = 10`, `max_hero_duration_sec = 80s`, conservative `$0.10/sec` 720p planning rate -> `$8.00` base / `$10.40` hard cap in `episodes.video_budget_cap_micro_usd`). Before calling `interactions.create`, atomically reserves micro-USD in `pipeline.db` `budget_reservations`, transitions `flow_jobs` (`UNIQUE(episode_id, scene_id)`, `idempotency_key`) to `SUBMITTING`, persists `provider_operation_id` immediately into `pipeline.db`, and reconciles `UNKNOWN_RECONCILE` operations on startup before ever retrying!
  2. **`VertexVeoEnterpriseBackend` (Separate Optional Stub/Contract, `VERTEX_VEO_ENTERPRISE`):** Documented distinct GCP IAM / Vertex AI / GCS URI adapter contract (never aliased onto the Developer API key).
  3. **`HumanBatchDeskBackend` (Separate Optional Manual Adapter, `HUMAN_BATCH_DESK`):** Implemented in `Task 155`.

#### Edge Cases And Failure Modes
- HTTP timeout or process crash after `interactions.create` dispatch before response arrives: mark `flow_jobs.state = 'UNKNOWN_RECONCILE'` and `budget_reservations.status = 'UNKNOWN_HOLD'`; startup recovery polls `provider_operation_id` to confirm terminal success/failure before permitting any retry (`F-10`).
- Safety filter returns zero output video (`total_output_tokens == 0`): settle reservation as `RELEASED` (`actual_micro_usd = 0`), increment safety strike counter, and trigger `prompt_v2_safe` or Strike-2 fallback.
- Missing `GEMINI_API_KEY`: raise explicit `MissingProviderCredentialsError` at pre-flight.

#### Bug Prevention And Invariants
- Never hardcode billing rates or model IDs; load `gemini-omni-1.2-flash` token/per-sec planning rates strictly from `providers.yaml` and confirm actual billing via bounded `M0.5` live sandbox check.
- Never dispatch a paid external video call without a committed `budget_reservations` row inside `pipeline.db`.

#### Independent Testability & Parallel Isolation
- Offline mock suite verifies all 3 `prompt_mode`s, `UNKNOWN_RECONCILE` crash recovery, and hard `$10.40` DB cap; separate `@pytest.mark.live_sandbox` contract test validates real `gemini-omni-1.2-flash` endpoint when opted in.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/flow_adapter/tests/test_omni_interactions.py` asserting crash-safe idempotency, `UNKNOWN_RECONCILE`, T2V/1-frame/2-frame schema parity, and `$10.40` DB cap.
- [ ] Execute bounded `M0.5` live sandbox check (`<= $2.00`) once before full production runs to confirm real `gemini-omni-1.2-flash` pricing/resolution/latency.
- **Acceptance:** Primary video backend runs on the live supported `gemini-omni-1.2-flash` Interactions API with crash-safe idempotency and durable USD admission control.

### Task 154: Implement Official Gemini Image API & Multi-Turn Clue Edit Adapter (`packages/flow_adapter`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 153
- **Files:** `packages/flow_adapter/src/flow_adapter/image_api.py`, `packages/flow_adapter/tests/test_image_api.py`
- **Tests:** 2K generation resolution gate (`>= 2048x1152`), multi-turn clue highlight edit (`"isolate overturned wooden chair, dim overhead light"`), and fallback mock unit tests.

#### Scope And Implementation Requirements
- Implement the unified **Official Gemini Image API & Multi-Turn Editing Adapter** (`image_api.py`, replacing the phantom Google Vids capacity pool removed in the v2 audit).
- Provide two concrete flows used seamlessly by Part 1's early Law 4 step (`Task 042` adapter contract) and Part 2 multi-turn documentary still variations:
  1. `generate_clean_2k_still(prompt, case_bible)`: generates clean atmospheric charcoal-parchment crime-scene plates at `>= 2048px` width (`16:9`), enforcing ZERO baked-in text and ZERO `10x10` grid markings on disk.
  2. `edit_still_multiturn(base_image_path, edit_instruction, seed)`: performs deterministic multi-turn clue isolation / lighting shifts (e.g., shifting hallway shadow or isolating an evidence folder on the table while keeping room architecture locked) so a single 2K still powers multiple coherent documentary reveal beats without re-rolling geometry!
- Expose clean stub/mock mode for zero-cost offline tests.

#### Edge Cases And Failure Modes
- API returns `1024x576` standard resolution image instead of `>= 2048px` 2K minimum: immediately reject or re-request `image_size="2K"` explicitly; never silently pass low-res image into `crime_scene_2k` where `3.8x` zoom would blur pixels.
- Multi-turn edit alters room furniture layout violating locked `spatial_anchors`: run fast SSIM structural check on outside-target quadrant pixels (`threshold >= 0.85`) and warn/retry if architecture shifted excessively.

#### Bug Prevention And Invariants
- Never embed crimson blood splatters or photorealistic human faces in generated stills (enforce Law 12 documentary charcoal/ink aesthetic prompt suffix automatically).

#### Independent Testability & Parallel Isolation
- Offline mock tests verify 2K resolution gate, SSIM room-lock heuristic, and exact API payload formatting.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/flow_adapter/tests/test_image_api.py` passing resolution gate, multi-turn SSIM test, and safety refusal handling.
- **Acceptance:** Official Gemini Image API + Multi-Turn editing provides scalable, high-res visual variety without phantom Vids promises.

### Task 155: Implement `HumanBatchDeskBackend` (`24h+5m` Rolling Reset Lock & 3-Episode Conveyor) (`packages/flow_adapter`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 153
- **Files:** `packages/flow_adapter/src/flow_adapter/batch_desk_backend.py`, `packages/flow_adapter/tests/test_batch_desk_backend.py`
- **Tests:** Rolling 24h+5m credit lock tests, multi-account ToS flag check, 3-episode oldest-first FIFO conveyor drain tests, and sunk-cost `>50%` saturation re-check tests.

#### Scope And Implementation Requirements
- Implement the **Optional Alternative** `HumanBatchDeskBackend` supporting creators who run manual Google Flow web accounts (`Accounts #1–#3`, 50 daily credits + 1,000/mo reserve each) instead of the Headless Gemini API default—embedding all v2 audit hardening fixes:
  1. **Explicit ToS / Policy Notice:** Emit structured configuration flag/acknowledgement warning when `providers.yaml` selects `human_batch_desk` (since rotating 3 free/Pro Google accounts may conflict with Consumer ToS; recommend dedicated API billing for commercial scale).
  2. **Exact Rolling `24h + 5m` Reset Lock:** Compute per-account `next_daily_reset_utc_ms = first_daily_spend_utc_ms + 86_400_000 + 300_000` (`24h 05m` buffer) rather than midnight resets, eliminating multi-week schedule drift and accidental monthly reserve burn when clicking 2 minutes early.
  3. **Up to 3 Episodes in `AWAITING_FLOW_BATCH` (FIFO):** Stage `x1` Job Cards strictly from the oldest pending episode first (`episode_queue_limit = 3`), keeping autonomous Part 1 busy without stalling behind a 3-day human desk shift.
  4. **Per-Shift Saturation Re-Check (`> 50%` Sunk-Cost Guard):** Before unlocking each day's Batch Desk shift on a multi-day episode, consult Saturation Re-Check: if `N_14d_wave > 3` and `< 50%` of episode credits spent -> abort & refund slot; if `spent > 50%` and `N_14d_wave <= 5` -> finish episode rather than stranding sunk credits!

#### Edge Cases And Failure Modes
- Account #1 resets at `19:03:00` while Account #2 resets at `19:14:30`: lock each tab independently by `account_id`, showing countdown timers cleanly without blocking Account #1's work.
- Creator switches mid-episode from `HumanBatchDeskBackend` to `GeminiOmniInteractionsBackend`: preserve already-ingested `clip_qa_passed` files seamlessly via shared `flow_jobs` state and render remaining `PENDING` Hero clips through Interactions API.

#### Bug Prevention And Invariants
- Never subtract credits before a valid clip or safety-fail state is confirmed on the desk action (`reserve -> commit/refund`).
- Account tab lock MUST hard-reject job-card checkout until `now_utc_ms >= next_daily_reset_utc_ms`.

#### Independent Testability & Parallel Isolation
- Pure simulated-clock unit tests testing 14-day multi-account rolling timestamps, 3-episode FIFO drains, and sunk-cost threshold branches.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/flow_adapter/tests/test_batch_desk_backend.py` asserting exact `86_700_000 ms` lock enforcement, 3-episode FIFO ordering, and `>50%` sunk-cost saturation branch.
- **Acceptance:** Optional manual Batch Desk backend operates safely without credit drift, conveyor starvation, or accidental reserve burn.

### Task 156: Build Drag-and-Drop Media Validator & Drop Ingestor (`packages/flow_adapter`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 155
- **Files:** `packages/flow_adapter/src/flow_adapter/drop_ingestor.py`, `packages/flow_adapter/tests/test_drop_ingestor.py`
- **Tests:** Drag-and-drop file ingestion tests verifying magic-byte validation, automatic duration bucket tolerance matching, stream normalization to `CFR 30fps`, and duplicate hash warnings.

#### Scope And Implementation Requirements
- Implement `FlowDropIngestor` validating raw `.mp4` / `.webm` / `.mov` files downloaded either automatically from `GeminiOmniInteractionsBackend` or dragged onto a Batch Desk Job Card by a human operator.
- Validate container & codec streams via `ffprobe`: minimum width `>= 1280px` (`720p` minimum), non-zero video frames, duration within acceptable bucket bounds (`>= 0.85 * expected_bucket_sec`), and absence of corrupt moov atoms.
- Automatically transcode/conform accepted Hero clips to unified pipeline intermediate spec (`1920x1080` Lanczos upscale if 720p, strict **`CFR 30fps`**, zero VFR drops, clean stripped or normalized stereo `48 kHz PCM` / silent audio placeholder) inside `workspace/flow_ingested/<scene_id>.mp4` so Agent 6 never hits mixed-FPS desync.
- Compute SHA-256 hash upon ingest to warn immediately if the creator accidentally dropped the same Flow MP4 onto two different scene cards (`DuplicateClipDropError`).

#### Edge Cases And Failure Modes
- Creator drags a `24fps` Veo export onto a `30fps` pipeline card: apply smooth `-vf fps=30` CFR frame conformation (`scale=1920:1080:flags=lanczos`) seamlessly during ingest.
- Truncated `0-byte` or partially downloading browser `.crdownload` / `.tmp` file dropped prematurely: reject cleanly with actionable message (`"Download incomplete — wait for browser to finish saving .mp4"`).

#### Bug Prevention And Invariants
- Never modify or delete the user's source download file; ingest into isolated `workspace/flow_ingested/` via atomic copy + transcode.
- Every ingested file passing Task 156 MUST report `1920x1080` `30/1` CFR before entering Vision QA (`Task 157`).

#### Independent Testability & Parallel Isolation
- Offline FFmpeg synthetic clip tests (`24fps 720p`, `30fps 1080p`, corrupt truncated MP4, duplicate SHA-256 drop).

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/flow_adapter/tests/test_drop_ingestor.py` verifying 24->30fps CFR conformation, duplicate rejection, and corrupt-file rejection.
- **Acceptance:** Every ingested Hero clip enters Agent 6 at verified `1920x1080 CFR 30fps`.

### Task 157: Implement Gemini Flash 2-Second Vision QA & Morph/Text Gate (`packages/flow_adapter`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 156
- **Files:** `packages/flow_adapter/src/flow_adapter/vision_qa.py`, `packages/flow_adapter/tests/test_vision_qa.py`
- **Tests:** Sampled 3-frame (`t=0.2s`, `0.5*T`, `T-0.2s`) Vision QA rubric unit tests (garbled AI text detection, extra limb/stickman duplication, color-shift failure, clean pass) with mocked Gemini Flash VLM.

#### Scope And Implementation Requirements
- Implement the `< 2.0 second` Vision QA Inspector checking every ingested Hero video clip (`Headless` OR `Human Batch Desk`) BEFORE promoting it to `qa_passed`:
  1. Extract 3 key telemetry frames (`first = 0.2s`, `mid = 50%`, `end = T - 0.2s`) in-memory via FFmpeg/OpenCV in `< 350 ms`.
  2. Perform fast deterministic heuristic pre-checks (blank/solid frame variance check, accidental crimson blood burst check, histogram flash cut check).
  3. Query Gemini Flash Vision (`< 1.5s`, mocked cleanly in offline unit tests) with structured JSON verdict rubric checking: garbled/hallucinated AI text overlays, sudden stick-figure duplication/morphing, broken silhouette anatomy, or extreme lighting flicker against the scene's Start/End bookends.
- Return `ClipVisionVerdict(passed: bool, failure_codes: list[str], confidence: float, retry_hint: str)` cleanly typed.

#### Edge Cases And Failure Modes
- Gemini Vision API transient rate-limit or outage: retry once with `500ms` backoff; if still unreachable, **FAIL CLOSED** by setting `flow_jobs.state = 'PENDING_MANUAL_SPOT_CHECK'` (and `qa_verdict = 'PENDING_MANUAL_SPOT_CHECK'`)! SQLite trigger `trg_episode_release_gate` hard-blocks `READY_TO_UPLOAD` until a human clears the spot check—zero silent fail-open exports!
- False positive on intentional documentary shadow motion: tune structured rubric to distinguish smooth silhouette lighting changes from multi-limb body-horror morphs or legible nonsense letters.

#### Bug Prevention And Invariants
- Vision QA MUST NEVER invoke expensive video-upload tokens when 3 extracted JPEG frames (`720p`) suffice cleanly in `< 2.0s`.
- Store compact QA verdict JSON + 3 thumbnail URIs for Batch Desk UI history inspection.

#### Independent Testability & Parallel Isolation
- Tested standalone using synthetic morphed/garbled-text/blank test clips + mocked Gemini Flash responses.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/flow_adapter/tests/test_vision_qa.py` proving `< 2.0s` local execution with mock VLM and accurate catching of blank/garbled/morphed failure modes.
- **Acceptance:** Fast Vision QA catches bad Flow generations immediately before mastering.

### Task 158: Implement 2-Strike Circuit Breaker & Non-Neighbor `fallback_spec` Engine (`packages/flow_adapter`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 157
- **Files:** `packages/flow_adapter/src/flow_adapter/circuit_breaker.py`, `packages/flow_adapter/tests/test_circuit_breaker.py`
- **Tests:** 2-strike escalation tests (`Attempt 1 fail -> simplified safe prompt + Amber alert -> Attempt 2 fail -> Hard Fallback`) and `RULE_05` non-neighbor engine invariant verification.

#### Scope And Implementation Requirements
- Implement the **2-Strike Circuit Breaker** protecting episode credit budgets (`MAX_FLOW_CREDITS = 300` / Headless USD cap) and preventing endless retake spirals on troublesome crime-scene actions:
  - **Strike 1 Failure (Safety block OR Vision QA fail):** Automatically rewrite/simplify prompt using ultra-neutral Law 12 motion descriptors (strip verbs, shorten to `<= 10 words`), surface **Amber Retry Alert** (`"Strike 1: Simplified motion prompt loaded"`), and deduct from Dynamic Retake Escrow (`ceil(0.4 * base)`).
  - **Strike 2 Failure (Second consecutive fail OR Escrow exhaustion):** Trip circuit breaker **HARD** (`status = 'fallback_triggered'`), halt all further Flow spend on `scene_id`, and swap seamlessly to `scene.fallback_spec`!
- **CRITICAL AUDIT FIX (Neighbor-Safe `RULE_05` Fallback Selection):** Before activating `fallback_spec` (which Part 1 pre-populated to avoid `CODE_STICKMAN` streak violations), re-verify left & right neighbor engines (`prev_scene.engine`, `next_scene.engine`):
  - If `fallback_spec.engine == 'CODE_STICKMAN'` AND merging with adjacent `CODE_STICKMAN` scenes would create a continuous Code streak `> 50.0s` (`RULE_05`), dynamically promote fallback engine to `STILL_2K_PANZOOM` (against the nearest pre-locked episode 2K still) or `ANIMATED_MAP_PLATE` so mastering NEVER inherits a hidden `RULE_05` violation!

#### Edge Cases And Failure Modes
- Episode escrow budget hits `0` on Strike 1 of another scene: skip Strike 1 retry completely and trip directly to `fallback_triggered` on remaining unstarted scenes if needed, preserving completed Hero scenes cleanly.
- Back-to-back Hero scenes both failing onto fallback: track cascading neighbor state deterministically across sequential breaker trips so two adjacent fallbacks don't both resolve to `CODE_STICKMAN` and break `50.0s`.

#### Bug Prevention And Invariants
- Hard-assert `attempt_count <= 2` for every `FLOW_HERO_VIDEO` scene across both Headless API and Human Batch Desk backends.
- Verify `max_contiguous_code_streak_sec <= 50.0` invariant holds after EVERY circuit-breaker swap!

#### Independent Testability & Parallel Isolation
- Pure Python state machine unit tests verifying Strike 1 rewrite, Strike 2 trip, escrow exhaustion, and cascading `RULE_05` non-neighbor invariant.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/flow_adapter/tests/test_circuit_breaker.py` with 100% pass across all 2-strike and neighbor-streak edge cases.
- **Acceptance:** Circuit breaker eliminates infinite retake drain while preserving strict `RULE_05` pacing guarantees.

### Task 159: Implement Durable SQLite USD Budget-Reservation Ledger & `providers.yaml` Cost Allocator (`packages/flow_adapter`)
- **Owner:** Developer B (Part 2) | **Milestone:** M0.5 / M2-P2 | **Depends on:** Task 153, Task 155, Task 158
- **Files:** `packages/flow_adapter/src/flow_adapter/budget_allocator.py`, `packages/flow_adapter/tests/test_budget_allocator.py`
- **Tests:** Durable SQLite `budget_reservations` admission-control tests (`trg_budget_cap_guard` at `$10.40` cap), crash-safe `UNKNOWN_HOLD` retention, `RELEASED` `$0` refund tests, and atomic optional Batch Desk `24h+5m` daily refill/lockout tests (`F-02`, `F-08`, `F-18`).

#### Scope And Implementation Requirements
- Implement unified durable USD & optional-credit admission control backed strictly by **`pipeline.db` (`budget_reservations` & `google_accounts`)** reading unit rates from `providers.yaml`—NEVER relying on async `telemetry.db` or in-memory-only locks for spend caps (`F-18`)!
- Enforce **Single-Config Episode Video Limits (`F-02`):**
  - In `GeminiOmniInteractionsBackend`: enforce `max_hero_clips = 10`, `max_hero_duration_sec = 80s`, `$8.00` base (`80s x $0.10/sec` conservative 720p plan) + `$2.40` dynamic retake escrow = **`$10.40` (`10_400_000` micro-USD) durable SQLite cap** enforced atomically by `trg_budget_cap_guard`.
  - In optional `HumanBatchDeskBackend`: call `atomic_refill_and_reserve_daily_account_credits` and `refund_daily_account_credits` (`schema/queries.sql`, `F-08`) atomically inside `BEGIN IMMEDIATE` transactions.
- Emit unified `BudgetSnapshot` for UI telemetry (`reserved_micro_usd`, `committed_micro_usd`, `unknown_hold_micro_usd`, `remaining_cap_micro_usd`).

#### Edge Cases And Failure Modes
- Worker crashes while holding a `RESERVED` slot: startup recovery converts it to `UNKNOWN_HOLD` (still counted against `trg_budget_cap_guard`!) until provider reconciliation proves the operation was not billed and marks it `RELEASED`.

#### Bug Prevention And Invariants
- Never allow concurrent workers or process restarts to breach `episodes.video_budget_cap_micro_usd` (enforced atomically inside SQLite `trg_budget_cap_guard`, `F-18`).

#### Independent Testability & Parallel Isolation
- Multi-process/restart SQLite concurrency tests verifying zero overspend across 16 concurrent mocked dispatch requests and simulated process restarts.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/flow_adapter/tests/test_budget_allocator.py` confirming `trg_budget_cap_guard` enforcement, `UNKNOWN_HOLD` accounting, and atomic `24h+5m` refill/lockout boundaries.
- **Acceptance:** Durable SQLite budget reservation ledger enforces hard per-episode USD caps across crashes and restarts.

### Task 160: Build Standalone `flow_adapter` Episode Orchestrator & CLI (`packages/flow_adapter`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 154, Task 157, Task 158, Task 159
- **Files:** `packages/flow_adapter/src/flow_adapter/orchestrator.py`, `packages/flow_adapter/src/flow_adapter/__init__.py`, `packages/flow_adapter/tests/test_orchestrator_e2e.py`
- **Tests:** 100% offline E2E orchestrator test running `<= 10` Hero clips (`<= 80s = 1.33m`) through `GEMINI_OMNI_INTERACTIONS` mock under simulated crash/`UNKNOWN_RECONCILE`, Strike 1 rewrite, and Strike 2 `fallback_spec` cascade cleanly on `ep_golden_01.json` (`$0.00` spend).

#### Scope And Implementation Requirements
- Implement `FlowOrchestrator` coordinating the crash-safe Hero scene fulfillment lifecycle for an episode:
  1. Reconcile any prior `SUBMITTING` / `RUNNING` / `UNKNOWN_RECONCILE` jobs (`reconcile_unknown_flow_jobs`) cleanly BEFORE dispatching new paid calls (`F-10`).
  2. Load `PLAN_APPROVED` `FLOW_HERO_VIDEO` scenes & keyframes (`TEXT_TO_VIDEO` null frames, `FIRST_FRAME`, or `FIRST_AND_LAST_FRAME <= 10s`).
  3. Reserve micro-USD in `provider_spend_reservations`, dispatch via `FlowAssetBackend`, run `FlowDropIngestor` -> `1920x1080 CFR 30fps` conformation -> fail-closed `VisionQA` -> `2-Strike Circuit Breaker`.
  4. Resolve any `fallback_triggered` scenes via `crime_scene_2k` or `@tc/render_catalog --scene`.

#### Edge Cases And Failure Modes
- Process crash/restart after completing 6 of 10 Hero clips: startup reconciliation polls saved `provider_operation_id` without ever creating a duplicate paid job (`UNIQUE(episode_id, scene_id)`).

#### Bug Prevention And Invariants
- Assert exact total Hero + fallback MP4 duration equals `sum(manifest.hero_scenes.duration_sec)` within `+/-0.00s` frame precision (`round(d * 30)` frames).

#### Independent Testability & Parallel Isolation
- Full E2E mock run on `fixtures/ep_golden_01.json` completing in `< 5s` locally without hitting Google servers.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/flow_adapter/tests/test_orchestrator_e2e.py` verifying checkpoint-resume, Strike-2 fallback fulfillment, and exact `CFR 30fps` output guarantees.
- **Acceptance:** `flow_adapter` orchestration handles failures, safety blocks, and budget ceilings autonomously.

### Task 161: Harden `flow_adapter` Against Rate Limits & Corrupt Media Streams (`packages/flow_adapter`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 160
- **Files:** `packages/flow_adapter/tests/test_resilience_chaos.py`
- **Tests:** Chaos fault-injection test simulating HTTP 429 storms, truncated half-MP4 downloads, VFR `23.97/59.94` streams, and mid-run backend toggle preservation.

#### Scope And Implementation Requirements
- Stress-test `flow_adapter` against real-world network and media degradation:
  - 5 consecutive `429 RESOURCE_EXHAUSTED` responses followed by `200 OK`.
  - Corrupt zero-duration or VFR `12fps–59fps` video payloads returned by mock endpoints.
  - Unexpected cancellation/crash midway through `15` clips + resume verification.
- Guarantee zero orphaned `.tmp` download artifacts and zero budget double-counting on network retries.

#### Edge Cases And Failure Modes
- HTTP `429` Retry-After header absent vs present: respect integer/HTTP-date `Retry-After` up to bounded `30s`, falling back to exponential full-jitter backoff cleanly.

#### Bug Prevention And Invariants
- Never bill retries triggered by `429`/`503`/socket reset against episode credit or dollar limits.

#### Independent Testability & Parallel Isolation
- Pure local pytest chaos suite.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/flow_adapter/tests/test_resilience_chaos.py` with 100% pass across all fault vectors.
- **Acceptance:** `flow_adapter` recovers gracefully from network storms and malformed video payloads.

### Task 162: Verify `flow_adapter` Performance & Telemetry Audit (`packages/flow_adapter`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 161
- **Files:** `packages/flow_adapter/tests/test_telemetry_audit.py`
- **Tests:** Audit asserting every clip attempt logs structured `cost_usd`, `latency_ms`, `provider_backend`, `safety_blocked`, and `attempt_num` records accurately.

#### Scope And Implementation Requirements
- Validate completeness and accuracy of BOTH `provider_spend_reservations` (authoritative `pipeline.db` ledger) and `telemetry.db` (`total_input_tokens >= cached_input_tokens`) across `GeminiOmniInteractionsBackend` and `HumanBatchDeskBackend` paths cleanly.
- Assert `$0.40 * 15 = $6.00` base cost calculation (`<= $8.40` w/ dynamic 40% escrow) and `$0.00` safety-block ledger accuracy.

#### Edge Cases And Failure Modes
- Partial clip fallback after 1 failed retake (`$0.40` paid Vision-QA fail + `$0` safety block + fallback): assert `total_usd` accurately counts the paid Vision-QA fail while excluding the `$0` safety block.

#### Bug Prevention And Invariants
- Telemetry logger MUST sanitize/redact any API keys or auth cookie headers before persisting events.

#### Independent Testability & Parallel Isolation
- Offline telemetry payload verification tests.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/flow_adapter/tests/test_telemetry_audit.py` verifying zero secret leakage and penny-exact USD/credit sums.
- **Acceptance:** `flow_adapter` cost and quality telemetry verified audit-ready.

### Task 163: Bootstrap `agent6_mastering` & Strict `CFR 30fps` Ingest Parities (`packages/agent6_mastering`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 002, Task 004, Task 132, Task 150, Task 160
- **Files:** `packages/agent6_mastering/pyproject.toml`, `packages/agent6_mastering/src/agent6_mastering/ingest_norm.py`, `packages/agent6_mastering/tests/test_ingest_norm.py`
- **Tests:** Stream normalization tests verifying mixed VFR FOIA (`29.97` / `23.976` / `59.94`), `CODE_STICKMAN`, `STILL_2K_PANZOOM`, and `FLOW_HERO_VIDEO` inputs normalize to identical `1920x1080 yuv420p CFR 30/1` + `48 kHz PCM`.

#### Scope And Implementation Requirements
- Bootstrap `packages/agent6_mastering` (Python 3.12, FFmpeg CLI / `ffprobe`, OpenCV, Gemini Flash Vision QA client) as the automated overnight documentary assembly, audio mastering, single-pass visual grading, Safe-Zone verification, self-heal, and upload packager.
- Implement `TimelineIngestNormalizer` verifying/conforming EVERY source media segment (`CODE_STICKMAN`, `STILL_2K_PANZOOM`, `FLOW_HERO_VIDEO`, and `FOIA_REAL_FOOTAGE` supplied by Part 1) to strict identical stream geometry before timeline concatenation:
  - Video: exact `1920x1080`, `yuv420p`, strict `CFR 30/1` (`-vf fps=30,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2`), exact `round(duration_sec * 30)` frame count.
  - Audio (Track 2 FOIA / raw segments): exact `48,000 Hz`, stereo/mono aligned `pcm_s16le` (silent track added cleanly for pure-video segments).
- Enforce `FOIA_REAL_FOOTAGE` tagging (`is_foia: true`, `exempt_from_grain: true`) inside the normalized timeline manifest.

#### Edge Cases And Failure Modes
- Concatenating a `29.97fps` FOIA bodycam clip with `30.00fps` Remotion animation via FFmpeg concat demuxer without prior normalization causes cumulative A/V drift (`~1.8s` by minute 20!): hard-reject any unnormalized input in `timeline_assembler` and normalize all inputs through `ingest_norm.py` first.
- Portrait `9:16` smartphone FOIA bystander clip (`1080x1920`): preserve crisp side pillars using dark subtle charcoal blur + crisp center framing (`1920x1080`) rather than stretching horizontally.

#### Bug Prevention And Invariants
- Never skip `ffprobe` validation after normalizing each segment; zero VFR segments (`avg_frame_rate != r_frame_rate`) permitted past ingest gate.

#### Independent Testability & Parallel Isolation
- Offline FFmpeg synthetic fixture tests (`29.97fps` bodycam stub, `60fps` CCTV stub, `30fps` Remotion clip) runnable cleanly in Part 2.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/agent6_mastering/tests/test_ingest_norm.py` verifying zero A/V sync drift across 20-minute synthetic mixed-FPS concat test (`drift < 15 ms`).
- **Acceptance:** Strict `CFR 30fps` / `48kHz PCM` ingest parity eliminates cumulative 20-minute concat desync.

### Task 164: Implement Law 6 `0.6s–1.0s` L-Cut & Multi-Track Audio Scheduler (`packages/agent6_mastering`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 163
- **Files:** `packages/agent6_mastering/src/agent6_mastering/audio_timeline.py`, `packages/agent6_mastering/tests/test_audio_timeline.py`
- **Tests:** L-Cut overlap offset math tests, `VoiceTrackManifest` segment alignment checks (Track 1 Narration + Track 2 FOIA + Twist Pads == exact `total_master_timeline_ms`), and zero-clipping boundary tests.

#### Scope And Implementation Requirements
- Implement `AudioTimelineScheduler` building the 4-track documentary audio graph from Part 1's segmented `VoiceTrackManifest` (`VoiceSegment`s + FOIA audio slots + `0.6s–1.0s` Law 6 L-Cut windows + procedural SFX cues + dark tension bed):
  - **Track 1 (Narration):** Ordered TTS speech segments aligned to their exact `timeline_start_ms` offsets (never a single blind concatenated WAV!).
  - **Track 2 (Evidence / FOIA / 911):** Raw bodycam/911 WAV clips triggered **`0.6s–1.0s` BEFORE visual cut** (Law 6 L-Cut bleed under outgoing transition, ducking Track 3 music gently while Track 1 ends cleanly).
  - **Track 3 (Music Bed):** Continuous procedural or licensed ambient dark bed spanning `[0, total_master_timeline_ms]` with scheduled duck envelopes during active speech/FOIA.
  - **Track 4 (SFX Cues):** Deterministic sample-accurate offset placements from `python_motion` `48 kHz` SFX WAVs (`sfx_cues`).
- Emit a structured `AudioMixPlan` validated so `total_master_timeline_ms == sum(scene.duration_ms)` within `+/- 1 ms`.

#### Edge Cases And Failure Modes
- Law 6 L-Cut offset at `scene[0]` (`t = 0.0s`) cannot advance `0.8s` before timestamp `0`: clamp L-Cut pre-lap cleanly to `max(0, t_start - l_cut_ms)`.
- Two consecutive FOIA clips back-to-back: keep Track 2 continuous without awkward double-fade silence gaps unless scene spec designates a deliberate pause pad.

#### Bug Prevention And Invariants
- Track 1 (`Narration`) MUST be completely muted (`0.0` gain) during exclusive Track 2 (`FOIA_REAL_FOOTAGE` / `AUDIO_EVIDENCE_CARD`) windows unless explicit commentator interjection segment is present.

#### Independent Testability & Parallel Isolation
- Pure timeline math & synthetic WAV mix plan validation tests on `fixtures/ep_golden_01.json`.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/agent6_mastering/tests/test_audio_timeline.py` asserting exact `total_master_timeline_ms` lock and Law 6 `600–1000 ms` pre-laps.
- **Acceptance:** Segmented multi-track L-Cut audio schedule honors Law 6 without triggering `RULE_01` desync.

### Task 165: Implement Per-Track Audio Pre-Normalization & Compression Chains (`packages/agent6_mastering`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 164
- **Files:** `packages/agent6_mastering/src/agent6_mastering/track_norm.py`, `packages/agent6_mastering/tests/test_track_norm.py`
- **Tests:** FFmpeg two-pass / measured LUFS per-track loudness tests asserting Track 1 `-16 LUFS` + de-esser, Track 2 `-18 LUFS` telephone/bodycam bandpass+comp, and Track 3 `-22/-36 LUFS` bed ducking.

#### Scope And Implementation Requirements
- **CRITICAL AUDIT FIX (Eliminating Whole-Mix `loudnorm` Pumping):** Before mixing the 4 audio stems together, normalize and dynamics-shape each track **independently** so dynamic single-pass `-14 LUFS` `loudnorm` never violently pumps ambient bed volume during silent pauses or whisper beats!
  - **Track 1 (TTS Narration):** High-pass `80 Hz`, gentle vocal presence EQ, gentle de-esser (`6–8 kHz`), compression (`3:1`), and normalize stem to **`-16.0 LUFS`** (`TP <= -2.0 dBTP`).
  - **Track 2 (911 / FOIA Audio):** Intelligibility telephone/bodycam bandpass (`250 Hz – 4.5 kHz` gentle shelf if telemetry flags lo-fi telephony, preserving clarity without erasing words), dynamic `4:1` leveling compressor (`-18 dB` threshold), normalized to **`-18.0 LUFS`** (`TP <= -2.0 dBTP`).
  - **Track 3 (Music Tension Bed):** Warm low-pass rolloff above `10 kHz` (keeping vocal frequencies clear), base **`-22.0 LUFS`** in sparse/tension beats, smoothly ducked **`-36.0 LUFS`** via `sidechaincompress` / envelope automation whenever Track 1 or Track 2 exceeds threshold (`attack=80ms, release=450ms`).
- Output intermediate 48kHz float/PCM pre-normalized stems (`track1_norm.wav`, `track2_norm.wav`, `track3_norm.wav`) cleanly.

#### Edge Cases And Failure Modes
- Track 2 FOIA stem is empty/silent on a non-FOIA documentary episode: short-circuit Track 2 normalization cleanly to deterministic 48kHz zero-sample stream instead of failing FFmpeg `loudnorm` on `-inf LUFS` input!
- Track 1 sparse narration segments leaving long 4-second gaps causing naive whole-file `loudnorm` measurement distortion: gate silence (`< -50 dBFS`) or run `loudnorm` measurement strictly over concatenated active speech intervals before remapping back onto timeline!

#### Bug Prevention And Invariants
- Measure actual integrated LUFS (`I`) and True Peak (`TP`) of each normalized stem using FFmpeg `ebur128` / `loudnorm=print_format=json` and assert exact target tolerances (`+/- 1.0 LU`).

#### Independent Testability & Parallel Isolation
- Offline FFmpeg synthetic sine/speech/noise WAV tests asserting measured LUFS on each stem independently.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/agent6_mastering/tests/test_track_norm.py` verifying `-16 LUFS` Track 1, `-18 LUFS` Track 2, `-22/-36 LUFS` ducked Track 3, and `-inf` silent-track handling.
- **Acceptance:** Independent per-track pre-normalization prevents pumping and keeps 911/TTS clarity crisp.

### Task 166: Implement `-filter_complex_script` SFX Bus & Linear `-14.0 LUFS` Final Pass (`packages/agent6_mastering`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 165
- **Files:** `packages/agent6_mastering/src/agent6_mastering/master_audio.py`, `packages/agent6_mastering/tests/test_master_audio.py`
- **Tests:** 500-cue Windows/Linux CLI-length-safe `-filter_complex_script` execution test asserting integrated `-14.0 LUFS` (`+/-0.3 LU`), `<= -1.0 dBTP` ceiling, zero `loudnorm` linear-mode pumping, and valid FLAC/WAV output.

#### Scope And Implementation Requirements
- Assemble all pre-normalized stems (`Track 1` `-16 LUFS`, `Track 2` `-18 LUFS`, `Track 3` ducked `-22/-36 LUFS`) plus up to `500` procedural `sfx_cues` cleanly using FFmpeg **`-filter_complex_script`** (a UTF-8 temp script file with `adelay` + `amix` batches) so Windows `32 KB` command-line limits (`WinError 206`) are never triggered.
- Normalize the Track 4 SFX sub-bus (`<= -18 LUFS` transient peak cap) prior to summing cleanly with Tracks 1–3.
- Execute a **Two-Pass Measured Linear Master (`linear=true`)** using FFmpeg `loudnorm`: Pass 1 measures `measured_I`, `measured_TP`, `measured_LRA`, `measured_thresh`; Pass 2 applies exact static linear gain (`I=-14.0:TP=-1.0:LRA=7.0:linear=true`)—preventing real-time AGC gain swelling between whisper pauses and music beds while locking YouTube broadcast compliance at **`-14.0 LUFS`**, **`<= -1.0 dBTP`**.

#### Edge Cases And Failure Modes
- Pass 1 measured LRA (`loudness range`) triggers fallback inside `loudnorm` from `linear=true` back to dynamic mode when `measured_LRA > target_LRA` or `offset` clips past `TP=-1.0`: explicitly verify `normalization_type == "linear"` in Pass 2 JSON stdout or re-run with `LRA=11` / gentle true-peak limiter (`alimiter=limit=-1.0dB`) beforehand so linear pass never reverts silently to dynamic pumping!
- Huge `500`-input single `amix=inputs=504` graph causing FFmpeg memory spike or descriptor limits: hierarchically group `sfx_cues` into sub-buses of `32` cues (`submix_0..submix_N`) summed into Track 4.

#### Bug Prevention And Invariants
- Never pass complex audio graphs inline via argv; strictly write `audio_graph.ffscript` and invoke `-filter_complex_script`.
- Assert final `master_audio.wav` `ebur128` integrated loudness reads `-14.0 +/- 0.4 LUFS` and `true_peak <= -1.0 dBTP`.

#### Independent Testability & Parallel Isolation
- Offline 500-cue stress test runnable standalone in Part 2 CI in `<8s`.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/agent6_mastering/tests/test_master_audio.py` testing 500 SFX cues, hierarchical sub-buses, `linear=true` verification, and `-14.0 LUFS / <= -1.0 dBTP` measurement.
- **Acceptance:** Final master audio hits YouTube `-14 LUFS` standard without Windows argv overflow or dynamic pumping.

### Task 167: Implement Single Continuous Non-FOIA Grain & Vignette Grading Pass (`packages/agent6_mastering`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 163
- **Files:** `packages/agent6_mastering/src/agent6_mastering/visual_grader.py`, `packages/agent6_mastering/tests/test_visual_grader.py`
- **Tests:** Temporal grain continuity tests across clip seams (`CODE_STICKMAN` -> `STILL_2K_PANZOOM` -> `FLOW_HERO_VIDEO`), raw-preservation pixel-delta test proving `FOIA_REAL_FOOTAGE` stays bit-faithful untouched, and `scene_grade_manifest.json` verification.

#### Scope And Implementation Requirements
- **CRITICAL AUDIT FIX (Single Continuous Pass, No Double Grain, Raw FOIA):** Eliminate compound double-grain noise (`Remotion grain + FFmpeg grain`) by reading `scene_grade_manifest.json` (`exempt_from_grain` / `is_foia` per segment):
  - Concatenate all normalized `1920x1080 CFR 30fps` non-FOIA segments cleanly and apply **ONE unified subtle documentary film-grain + vignette pass** (`noise=alls=4:allf=t+u`, subtle radial `vignette=PI/6`) continuously across clip boundaries so transitions (`CODE -> 2K -> FLOW`) share uninterrupted temporal grain!
  - Leave all `FOIA_REAL_FOOTAGE` and `AUDIO_EVIDENCE_CARD` raw-document segments **100% exempt from synthetic paper grain/vignette** (splicing untouched authentic bodycam/911 frames seamlessly after the graded non-FOIA tracks) so authentic archival footage preserves forensic realism cleanly.
- Emit unified `master_video_silent.mp4` (`1920x1080 CFR 30/1 yuv420p`, exact frame count parity).

#### Edge Cases And Failure Modes
- Transition between non-FOIA graded clip and raw FOIA clip (`L-Cut` entry): apply clean `6-frame` subtle dip/cross-dissolve or crisp documentary slate cut cleanly at exact integer frame indices without re-encoding grain over FOIA pixels.
- Excessive `noise=alls` bit-rate inflation at YouTube H.264 upload preset: tune subtle organic strength (`alls=3..5`) + `-crf 18 -preset medium -movflags +faststart` to balance tactile charcoal warmth against macroblock artifacts.

#### Bug Prevention And Invariants
- Assert pixel difference outside timestamp overlay on `FOIA_REAL_FOOTAGE` frames is zero-grain untouched (`PSNR >= 48 dB` across codec encode vs input FOIA clip).
- Assert zero double-grain passes by failing if `scene_grade_manifest.json` reports `remotion_grain_applied == true`.

#### Independent Testability & Parallel Isolation
- Offline FFmpeg synthetic timeline test checking FOIA segment PSNR and non-FOIA seam continuity.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/agent6_mastering/tests/test_visual_grader.py` verifying FOIA pixel integrity and single-pass continuous non-FOIA grading.
- **Acceptance:** Cohesive documentary texture achieved across all synthetic engines while authentic FOIA footage stays raw.

### Task 168: Build Final Muxer, Chapter Marker Injector & YouTube Encoding Spec (`packages/agent6_mastering`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 166, Task 167
- **Files:** `packages/agent6_mastering/src/agent6_mastering/final_muxer.py`, `packages/agent6_mastering/tests/test_final_muxer.py`
- **Tests:** Full A/V mux verification testing exact `abs(video_dur - audio_dur) <= 0.05s`, MP4 chapter metadata atoms (`FFMETADATA1`), `AAC 320kbps 48kHz`, and `+faststart` moov placement.

#### Scope And Implementation Requirements
- Combine `master_video_silent.mp4` (`1920x1080 CFR 30fps`) and `master_audio.wav` (`-14.0 LUFS 48kHz`) into final YouTube-optimized H.264/AAC MP4 (`crf=18`, `High Profile L4.1`, `bt709` color tags, `aac 320k`, `-movflags +faststart`).
- Generate and embed exact YouTube timestamp chapter metadata (`FFMETADATA1` atom + formatted `chapters.txt` description block) aligned to scene act transitions and key forensic reveals derived from `manifest.json`.
- Assert exact duration symmetry via `ffprobe`: `abs(video_duration_sec - audio_duration_sec) <= 0.05s`.

#### Edge Cases And Failure Modes
- FFmpeg AAC encoder priming delay (`~21 ms` / `1024 samples`) shifting apparent audio duration slightly past video end: pass `-shortest` ONLY alongside pre-aligned sub-50ms stems or explicitly pad `50 ms` silent tail on shorter stream before encoding so AAC framing never clips final narration word!
- Non-ASCII chapter titles (foreign city/street names) breaking `FFMETADATA1` escape rules: escape `=`, `;`, `#`, `\`, and newlines cleanly per FFmpeg metadata spec.

#### Bug Prevention And Invariants
- Verify `color_primaries=bt709`, `color_trc=bt709`, `colorspace=bt709`, `r_frame_rate=30/1`, `sample_rate=48000` on every muxed deliverable.

#### Independent Testability & Parallel Isolation
- Offline FFmpeg synthetic mux tests runnable standalone in Part 2 CI.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/agent6_mastering/tests/test_final_muxer.py` validating `ffprobe` color tags, chapter atoms, `+faststart`, and `<50ms` A/V delta.
- **Acceptance:** Broadcast-grade YouTube MP4 muxer verified with exact chapters and zero priming truncation.

### Task 169: Implement Post-Render CSS Safe-Zone Pixel Scanner (`packages/agent6_mastering`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 168
- **Files:** `packages/agent6_mastering/src/agent6_mastering/safe_zone_scanner.py`, `packages/agent6_mastering/tests/test_safe_zone_scanner.py`
- **Tests:** Automated OpenCV edge-margin detector tests catching simulated title/badge bleeds into YouTube player scrub bar (`bottom 12%`) or right/top overlays while passing clean centered documentary cards.

#### Scope And Implementation Requirements
- Implement an automated OpenCV post-render **Safe-Zone Pixel Audit** complementing Task 130's TypeScript CSS guard (`@tc/render_catalog`), checking ALL rendered scenes including `STILL_2K_PANZOOM` crimson callouts and `FLOW_HERO_VIDEO` composite overlays:
  - Sample representative frames per scene (`t=0.25, 0.5, 0.75 * duration`) across high-contrast text/callout edge bands: `y > 0.90 * H` (bottom scrub-bar hazard), `y < 0.06 * H` (top overlay hazard), `x < 0.05 * W`, and `x > 0.94 * W`.
  - Detect high-contrast vector glyph strokes or `#C92A2A` callout boxes inside forbidden border zones (`high-frequency Canny edge clusters / bright parchment/crimson text luminance contrast > 4.5:1 against background`).
  - Exempt full-bleed continuous background textures/props cleanly (low edge density / authentic 2K room walls or FOIA dashcam timestamps already tagged `exempt_safe_zone_foia`).

#### Edge Cases And Failure Modes
- Authentic FOIA bodycam burned-in Axon camera timestamp in top-right (`AXON BODY 3 2024-03-12`): explicitly exempt `FOIA_REAL_FOOTAGE` scenes from synthetic caption Safe-Zone failures (`exempt_safe_zone_foia = true`) so real evidence never triggers false heal loops!
- Bright parchment `#E9E2D2` background gradient near edge triggering naive luminance alarms: trigger solely on sharp crisp glyph-like high-contrast edge density (`Sobel/Canny` density + crimson chroma cluster) rather than uniform parchment tone.

#### Bug Prevention And Invariants
- Never modify the master MP4 inside `safe_zone_scanner.py`; return precise offending `(scene_id, margin_side, timestamp_sec)` violations to trigger surgical `<5s` re-render heals (`Task 171`).

#### Independent Testability & Parallel Isolation
- Offline OpenCV tests using synthetic clean vs corner-clipped video frames (`bottom 8% text overlap` -> caught cleanly).

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/agent6_mastering/tests/test_safe_zone_scanner.py` asserting 100% catch rate on bottom-bar/corner text collisions and 0 false alarms on parchment edges or FOIA bodycam stamps.
- **Acceptance:** Post-render pixel Safe-Zone audit protects YouTube UI overlays across all visual engines.

### Task 170: Implement Agent 6 `2x2` Contact-Sheet Vision QA (`packages/agent6_mastering`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 168
- **Files:** `packages/agent6_mastering/src/agent6_mastering/contact_sheet_qa.py`, `packages/agent6_mastering/tests/test_contact_sheet_qa.py`
- **Tests:** Contact-sheet grid compositor (`4 scenes/sheet = 1 image token call`) and mocked Gemini Flash VLM final defect verifier catching overlapping subtitles, unreadable typography, or black-frame glitches.

#### Scope And Implementation Requirements
- Implement cost-efficient **Overnight `2x2` Contact-Sheet Vision QA**:
  - Extract the midpoint visual frame from every scene (`~180` scenes / episode) and tile them cleanly 4-up (`2x2` @ `1920x1080`, labeled crisp `TL/TR/BL/BR` with `scene_id` header strips) into `~45` composite contact sheets—cutting Vision QA token calls by **75%**.
  - Submit contact sheets to Gemini Flash Vision (`< 30s` total batch via bounded concurrency, mocked cleanly in unit tests) evaluating: text legibility/overlap (`RULE_07` empirical check), visual corruption/black screens, missing `CaseBible` palette continuity, and discordant prop rendering.
  - Parse structured JSON array mapping failed quadrants directly back to exact `scene_id` + targeted fix directive (`fix_type: "text_bounds" | "2k_zoom_clamp" | "re_render_code"`).

#### Edge Cases And Failure Modes
- 179 scenes leaving the final contact sheet with 3 scenes and 1 blank slot: fill the 4th quadrant with clean solid neutral slate labeled `[EMPTY_SLOT]` and explicitly instruct VLM rubric to score ONLY populated tiles (`[EMPTY_SLOT]` ignored cleanly).
- Non-4-multiple batch ordering mismatch when parsing LLM quadrant array: key structured output explicitly by `scene_id` string echoed from the tile header strip rather than blind array index.

#### Bug Prevention And Invariants
- Never send all 180 full-res frames individually (`180` API calls); enforce `2x2` tiling batching (`ceil(N / 4)` calls).

#### Independent Testability & Parallel Isolation
- Offline Pillow grid tiling + mocked Gemini Flash VLM defect injection suite.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/agent6_mastering/tests/test_contact_sheet_qa.py` verifying `ceil(N / 4)` sheet generation, empty-slot padding, and exact `scene_id` defect attribution.
- **Acceptance:** `2x2` contact-sheet QA inspects an entire 20-minute episode overnight at 75% reduced API overhead.

### Task 171: Implement `<5s` Surgical Scene Self-Healer (`packages/agent6_mastering`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 132, Task 150, Task 169, Task 170
- **Files:** `packages/agent6_mastering/src/agent6_mastering/surgical_healer.py`, `packages/agent6_mastering/tests/test_surgical_healer.py`
- **Tests:** Surgical heal roundtrip test repairing a Safe-Zone-clipped `CODE_STICKMAN` scene in `< 5s` via `@tc/render_catalog --scene` and cleanly re-splicing into `master_video` without re-rendering untouched 19.8 minutes.

#### Scope And Implementation Requirements
- Implement the **Targeted `<5s` Self-Healer** closing the loop on `safe_zone_scanner.py` (`Task 169`) and `contact_sheet_qa.py` (`Task 170`) failures without ever re-running full-episode rendering:
  1. Receive offending `(scene_id, violation_code, margin_side)` diagnostics.
  2. Apply bounded deterministic manifest patch (`scale_typography: 0.88`, `nudge_safe_inset_px: +48`, or `2k_reclamp_zoom`) onto a transient heal copy of `SceneSpec` (never corrupting immutable Part 1 manifest).
  3. Trigger single-scene render ONLY (`render-catalog --scene <id>` in `<5s` via zero-`<feTurbulence>` JS boil, OR `crime-scene-2k --scene <id>`).
  4. Apply identical single-pass grain grade (`Task 167` matching clip params) cleanly onto the healed clip and splice/re-assemble seamlessly (re-running `safe_zone_scanner` on healed segment!).
  5. Enforce hard `MAX_HEAL_PASSES_PER_SCENE = 2` limit; escalate persistent defects to `human_review_flags` inside `ready_to_upload` manifest rather than looping forever.

#### Edge Cases And Failure Modes
- A healed `FLOW_HERO_VIDEO` scene fails final Vision QA overnight after already burning its 2-strike Flow budget: DO NOT trigger another paid Flow API call overnight! Auto-swap directly to pre-generated `fallback_spec` (`STILL_2K_PANZOOM` or neighbor-safe `CODE_STICKMAN`) so morning export NEVER surprises the creator with unbudgeted charges!

#### Bug Prevention And Invariants
- Never exceed `MAX_HEAL_PASSES_PER_SCENE = 2`.
- Re-verify `abs(healed_clip.duration_sec - original_scene.duration_sec) <= 0.01s` before splicing so A/V sync across the remaining 20 minutes remains completely undisturbed!

#### Independent Testability & Parallel Isolation
- E2E offline self-heal test patching a bad `CODE_STICKMAN` scene, invoking `@tc/render_catalog --scene`, verifying `<5s` render, and asserting final frame count matches pre-heal frame count identically.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/agent6_mastering/tests/test_surgical_healer.py` verifying `<5s` heal re-render, exact frame count preservation, zero extra Flow spend, and pass-cap breaker.
- **Acceptance:** Autonomous surgical healing repairs defects overnight in seconds without risking A/V sync or Flow budget.

### Task 172: Implement AdSense Thumbnail Policy Auditor & Brand Novelty Engine (`packages/agent6_mastering`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 004, Task 154
- **Files:** `packages/agent6_mastering/src/agent6_mastering/thumbnail_auditor.py`, `packages/agent6_mastering/tests/test_thumbnail_auditor.py`
- **Tests:** AdSense policy rejection tests (blood/weapon imagery, unreadable tiny text `< 7%` frame height, clutter `> 4` words) and brand-consistency + novelty verification against last 5 channel thumbnails.

#### Scope And Implementation Requirements
- Implement the pre-upload **Thumbnail Policy Auditor & Brand-Coherent Novelty Verifier**:
  1. **AdSense / YouTube Policy Pre-Flight (`Task 172`):** Reject candidates exhibiting blood-red pixel clusters (strictly outside crisp `#C92A2A` typographic stamp bar if present), gore/weapon outlines, shocked faces, clickbait falsehoods, or `> 4` thumbnail words / tiny illegible font (`< 72px` height at `1280x720`).
  2. **CRITICAL AUDIT FIX (Brand Coherence WITH Composition Novelty):** Enforce consistent channel brand recognition (charcoal silhouette aesthetic + weathered parchment `#E9E2D2` + documentary serif/sans lockup + readable high-contrast framing) **paired with rotational novelty** against the last 5 uploaded thumbnails (`recent_thumbnails.json`):
     - Require rotation across composition archetypes (`doorway_silhouette`, `desk_evidence_closeup`, `map_trajectory_split`, `redacted_dossier_reveal`), primary silhouette pose, and secondary accent mood (muted amber vs slate blue vs deep crimson stamp) so the channel looks unmistakably branded yet NEVER repeats boring identical layout formulas!
  3. Generate `2–3` distinct A/B candidate `1280x720` PNG variants per episode cleanly into `ready_to_upload/thumbnails/`.

#### Edge Cases And Failure Modes
- Channel has `< 5` historical thumbnails (Episode #1 cold launch): treat empty history cleanly and auto-approve first brand-compliant candidate while seeding `recent_thumbnails.json`.
- Overly aggressive perceptual hash (`pHash` hamming distance) blocking valid branded episodes because background parchment color `#E9E2D2` matches across episodes: compare structural foreground bounding-box layout + archetype ID + text-block quadrant placement rather than naive global brightness average!

#### Bug Prevention And Invariants
- Every approved thumbnail MUST pass `1280x720` dimensions, `< 2.0 MB` file size (YouTube upload limit!), `<= 4` words, and zero blood/gore/weapon hits.

#### Independent Testability & Parallel Isolation
- Offline Pillow/OpenCV thumbnail policy & novelty rotation test suite with 5 synthetic historical episode layouts.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/agent6_mastering/tests/test_thumbnail_auditor.py` confirming rejection of repeated identical archetype layouts, oversized word counts, `>2MB` PNGs, and gore hazards.
- **Acceptance:** Automated thumbnail suite balances recognizable channel brand DNA with fresh per-episode visual intrigue.

### Task 173: Build Atomic `ready_to_upload/` Package Exporter & Provenance Bundle (`packages/agent6_mastering`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 168, Task 171, Task 172
- **Files:** `packages/agent6_mastering/src/agent6_mastering/package_exporter.py`, `packages/agent6_mastering/tests/test_package_exporter.py`
- **Tests:** Atomic staging->rename exporter tests guaranteeing complete upload folder (`final_1080p30.mp4`, `thumbnails/ab_*.png`, `chapters.txt`, `seo_metadata.json`, `provenance_bundle.json`, `qa_certificate.json`).

#### Scope And Implementation Requirements
- Implement `ReadyToUploadExporter` packaging every completed episode artifact into an isolated atomic directory `ready_to_upload/<episode_slug>/`:
  - `final_1080p30.mp4` (`-14.0 LUFS`, `<= -1.0 dBTP`, `CFR 30fps`, `bt709`, `+faststart`)
  - `thumbnails/variant_a.png`, `variant_b.png`, `variant_c.png` (`< 2 MB` `1280x720` audited PNGs)
  - `chapters.txt` + `seo_metadata.json` (title variants, description, tags, altered/synthetic YouTube Studio disclosure checkbox flag!)
  - `provenance_bundle.json` (complete `Claim -> Citation -> FactLedger` grounding summary, FOIA public-domain agency receipts, procedural SFX zero-copyright attestation, and final `episode_cost_usd` breakdown)
  - `qa_certificate.json` (Safe-Zone pass status, `2x2` Vision QA verdict, `-14.0 LUFS` reading, heal count, and any remaining `human_review_flags`).
- Stage into `.staging_<slug>` and promote via atomic directory rename (`os.replace`) ONLY after verifying checksums across all artifacts.

#### Edge Cases And Failure Modes
- Partial night run interrupted mid-copy leaving half-written `ready_to_upload/<slug>` visible to creator: atomic staging prefix `.staging_` guarantees `ready_to_upload/<slug>` NEVER appears until 100% checksums and `qa_certificate.json` pass!
- YouTube altered/synthetic content flag missing when `FLOW_HERO_VIDEO` or `TTS` synthetic voices are used: hard-set `youtube_synthetic_disclosure_required = true` inside `seo_metadata.json` whenever realistic-adjacent synthetic voice/scene media is present.

#### Bug Prevention And Invariants
- Never ship an upload package without `provenance_bundle.json` and `qa_certificate.json`.

#### Independent Testability & Parallel Isolation
- Offline atomic filesystem & schema validation test suite verifying crash-safe staging rollback.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/agent6_mastering/tests/test_package_exporter.py` verifying atomic promotion, YouTube disclosure metadata, and zero stale `.staging_` leaks on simulated exceptions.
- **Acceptance:** Upload packages appear atomically complete and upload-ready every morning.

### Task 174: Implement Unattended Overnight Mastering Runner & Resume Checkpointer (`packages/agent6_mastering`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 173
- **Files:** `packages/agent6_mastering/src/agent6_mastering/overnight_runner.py`, `packages/agent6_mastering/src/agent6_mastering/__init__.py`, `packages/agent6_mastering/tests/test_overnight_runner.py`
- **Tests:** Unattended E2E mastering pipeline test across `CODE_STICKMAN` + `STILL_2K_PANZOOM` + `FLOW_HERO_VIDEO` + `FOIA_REAL_FOOTAGE` clips, including simulated kill midway through Step 4 and clean resume.

#### Scope And Implementation Requirements
- Implement `OvernightMasteringRunner` (`agent6-master run --episode-dir ...`) orchestrating the unattended overnight production pipeline end-to-end:
  1. `STAGE_INGEST`: Verify & normalize all scenes to `1920x1080 CFR 30fps` + `48kHz PCM`.
  2. `STAGE_AUDIO`: Run Track 1–3 pre-norm + `-filter_complex_script` 500-cue SFX mix + `linear=true` `-14.0 LUFS` master.
  3. `STAGE_VIDEO_GRADE`: Run single continuous grain/vignette pass (`FOIA` untouched raw).
  4. `STAGE_MUX`: Multiplex A/V + chapters into `+faststart` MP4.
  5. `STAGE_QA_HEAL`: Run Safe-Zone scanner + `2x2` Vision QA + `<5s` surgical heal loop (up to 2 passes).
  6. `STAGE_EXPORT`: Audit thumbnails + export atomic `ready_to_upload/<slug>/`.
- Persist step checkpoints cleanly (`overnight_state.json`) so unexpected reboots or OS restarts resume at the exact interrupted stage without repeating completed expensive steps.

#### Edge Cases And Failure Modes
- Missing or corrupt scene clip discovered at `STAGE_INGEST` overnight (`FLOW_HERO_VIDEO` missing file despite `hero_fulfillment_report.json`): autonomously fall back to neighbor-safe `fallback_spec` (`STILL_2K_PANZOOM` or `CODE_STICKMAN` local render) rather than halting the entire overnight run!

#### Bug Prevention And Invariants
- Never touch `pipeline.db` directly if invoked as standalone worker—emit stage status callbacks / FastAPI webhook or Python DB service interface cleanly (`Python Sole SQLite Writer` rule).

#### Independent Testability & Parallel Isolation
- End-to-end local runner test executing in `< 20s` on synthetic `ep_golden_01.json` 60-second condensed fixture + crash-resume checkpoint verification.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/agent6_mastering/tests/test_overnight_runner.py` verifying E2E mastering, mid-stage resume, and autonomous missing-clip fallback recovery.
- **Acceptance:** Overnight mastering runs reliably unattended and survives restarts cleanly.

### Task 175: Stress-Test `agent6_mastering` Full 1,200-Second Memory & Disk Footprint (`packages/agent6_mastering`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 174
- **Files:** `packages/agent6_mastering/tests/test_scale_1200s.py`
- **Tests:** 20-minute (`1,200s`, `36,000` frames, `~180` segments) scale benchmark validating wall-clock mastering speed, `< 1.5 GB` peak Python RSS memory, and temp-file cleanup (`0` leaked gigabyte WAV intermediates).

#### Scope And Implementation Requirements
- Exercise `agent6_mastering` at true 20-minute (`1,200s`) full documentary length (`180` scenes across Code + 2K + Hero + FOIA + 300 SFX cues) using fast-generated synthetic media streams.
- Assert zero OOM spikes (`RSS < 1.5 GB`), verify `-filter_complex_script` executes cleanly on Windows/Linux, verify cumulative A/V sync drift at minute `19:55` remains `< 15 ms`, and verify automatic cleanup of transient normalized WAV/YUV intermediates after atomic `ready_to_upload/` promotion!

#### Edge Cases And Failure Modes
- Temp intermediate directory ballooning past `15 GB` across 3 episodes queued concurrently: enforce immediate cleanup of `stage_tmp/` per completed stage once checksums validate cleanly, reserving raw archival files only per retention policy.

#### Bug Prevention And Invariants
- Measure actual timestamp offset between embedded visual flash marker + audio `1 kHz` sync pip at `t = 1190s` in the 20-minute stress output to empirically prove `< 15 ms` zero-drift!

#### Independent Testability & Parallel Isolation
- Self-contained Part 2 benchmark/verification test marked `@pytest.mark.slow` (also runnable directly in nightly CI).

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/agent6_mastering/tests/test_scale_1200s.py` asserting `< 15 ms` sync drift at minute `19:50`, `< 1.5 GB` RSS, and clean temp cleanup.
- **Acceptance:** Full 20-minute documentary mastering scales predictably without memory leaks or A/V drift.

### Task 176: Certify `agent6_mastering` Package Contract & Exit Report (`packages/agent6_mastering`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 175
- **Files:** `packages/agent6_mastering/README.md`, `packages/agent6_mastering/tests/test_contract_compliance.py`
- **Tests:** Contract suite validating compatibility against frozen `contracts/schemas` (`SceneSpec`, `VoiceTrackManifest`, `ReadyToUploadReport`) so Part 1 integration requires zero adapters rewrites.

#### Scope And Implementation Requirements
- Validate 100% schema fidelity between `packages/agent6_mastering` inputs/outputs and `contracts/schemas/` Pydantic models.
- Document exact CLI flags, environment variables, temp-cleanup behavior, and `-14.0 LUFS` / single-grade verification guarantees in `packages/agent6_mastering/README.md`.

#### Edge Cases And Failure Modes
- Optional fields omitted in minimal golden manifests (e.g., empty `sfx_cues = []` or zero FOIA clips): confirm zero `AttributeError` or empty-list crash across every stage.

#### Bug Prevention And Invariants
- Schema roundtrip tests must pass symmetrically against both golden Part 1 fixtures and Part 2 outputs.

#### Independent Testability & Parallel Isolation
- Offline schema & mock pipeline check in Part 2.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/agent6_mastering/tests/test_contract_compliance.py` with 100% pass.
- **Acceptance:** `agent6_mastering` officially certified against frozen Part 1/Part 2 schemas.

### Task 177: Implement Loopback-Secured FastAPI Orchestrator Bridge as Sole SQLite Writer (`apps/batch_desk_ui/api`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 003, Task 004, Task 155, Task 160
- **Files:** `apps/batch_desk_ui/api/pyproject.toml`, `apps/batch_desk_ui/api/src/desk_api/server.py`, `apps/batch_desk_ui/api/src/desk_api/db_service.py`, `apps/batch_desk_ui/api/tests/test_desk_api.py`
- **Tests:** FastAPI TestClient & WebSocket security/integration tests asserting loopback-only `127.0.0.1` binding, `X-Local-Auth-Token` enforcement, localhost-only CORS, canonical upload path containment, `SQLite >= 3.51.3` check, and `audit_log` recording (`F-19`, `F-22`).

#### Scope And Implementation Requirements
- Bootstrap `apps/batch_desk_ui` backend (`FastAPI` + `uvicorn` + `sqlite3` / repository interface) as the **SOLE SQLite writer bridge** between UI clients and `pipeline.db`.
- **Explicit Local Security Boundary (`F-19`):**
  1. Bind strictly to **`127.0.0.1`** (hard-refuse `0.0.0.0` startup unless explicit authenticated TLS mode is enabled).
  2. Generate a random 256-bit per-session bearer token written `0600` to local runtime state; enforce `X-Local-Auth-Token` header on every mutating HTTP endpoint and WebSocket handshake (rejecting unauthenticated/CSRF requests with HTTP `401`/`403`).
  3. Restrict `CORS` allowlist strictly to `http://127.0.0.1:<ui_port>` / `http://localhost:<ui_port>`.
  4. Enforce upload MIME/magic-byte validation, max size (`<= 250 MB`), and canonical path containment (`Path.resolve().is_relative_to(upload_root)`) to block path traversal.
  5. Record every backend config change, state mutation, and human release approval in `pipeline.db` **`audit_log`**.
- Expose REST + WebSocket endpoints (`/api/conveyor`, `/api/accounts`, `/api/episodes/{id}/cards`, `/api/episodes/{id}/drop`, `/api/episodes/{id}/animatic`, `/api/episodes/{id}/approvals`, `/api/config/backend`, `/ws/events`).
- **SQLite Runtime & Local Disk Guard (`F-22`):** Assert `sqlite3.sqlite_version_info >= (3, 51, 3)` and local host filesystem (no SMB/NFS/UNC paths) on startup, enforcing `PRAGMA journal_mode=WAL; PRAGMA synchronous=FULL; PRAGMA busy_timeout=5000; PRAGMA foreign_keys=ON;`.

#### Edge Cases And Failure Modes
- Concurrent drag-and-drop uploads across two open browser tabs clicking the same `scene_id` job card: serialize card claim/drop inside `BEGIN IMMEDIATE` SQLite transaction and return HTTP `409 Conflict` with live state refresh to the losing tab!
- Malformed multipart file upload (`> 500 MB` unintended file or non-video mime): stream-limit upload size and fail cleanly with HTTP `413`/`415` before touching disk.

#### Bug Prevention And Invariants
- Zero frontend JavaScript/Node process may ever open `pipeline.db` directly; every UI read and state mutation passes strictly through FastAPI endpoints.

#### Independent Testability & Parallel Isolation
- Tested standalone using FastAPI `TestClient` against ephemeral `tmp_path` SQLite DB seeded from `schema/pipeline.sql`.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest apps/batch_desk_ui/api/tests/test_desk_api.py` verifying `BEGIN IMMEDIATE` race protection, WebSocket live updates, and standalone golden seeding.
- **Acceptance:** Single-writer FastAPI service isolates UI from SQLite contention cleanly.

### Task 178: Implement 3-Episode FIFO Conveyor Ribbon & Headless API Toggle UI (`apps/batch_desk_ui/web`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 177
- **Files:** `apps/batch_desk_ui/web/package.json`, `apps/batch_desk_ui/web/src/components/ConveyorRibbon.tsx`, `apps/batch_desk_ui/web/src/components/BackendModeBanner.tsx`, `apps/batch_desk_ui/web/tests/ConveyorRibbon.test.tsx`
- **Tests:** React Testing Library / Vitest tests verifying 3-slot FIFO `AWAITING_FLOW_BATCH` queue visibility, Headless Gemini API primary-default badge/progress telemetry, and optional Batch Desk switch.

#### Scope And Implementation Requirements
- Bootstrap `apps/batch_desk_ui/web` (React 19, Vite, TypeScript, Tailwind CSS) implementing a calm, zero-clutter documentary production cockpit.
- Build **`ConveyorRibbon.tsx`** displaying the active conveyor pipeline cleanly:
  - Highlights active **`Gemini Omni Interactions API` Primary Default** mode (`gemini-omni-1.2-flash @ ~$0.10/sec` conservative 720p plan, `<= 10` clips / `80s`, `$8.00` base / **`$10.40` durable SQLite USD cap** gauge, plus `UNKNOWN_RECONCILE` / `PENDING_MANUAL_SPOT_CHECK` alerts) OR switches cleanly to optional **`Human Batch Desk`** / **`Vertex Enterprise`** mode when configured in `providers.yaml`.
  - Visualizes **up to 3 queued episodes** in `AWAITING_FLOW_BATCH` drained strictly **oldest-first (FIFO)** so creators see upstream research/rendering throughput without stalled single-slot conveyor deadlocks!
  - Displays per-shift **Saturation Re-Check badge** (`SAFE` vs `ABORTED_BEFORE_50PCT` vs `SUNK_COST_FINISH_GUARD >50%`) before authorizing Batch Desk work.

#### Edge Cases And Failure Modes
- 3 episodes queued while an unexpected copycat wave hits Episode #2 (`< 50%` sunk): update queue card immediately over WebSocket to show `"Aborted by Saturation Re-Check — Slot Freed"` without refreshing the page.

#### Bug Prevention And Invariants
- Follow modern web UI best practices: responsive semantic HTML, accessible keyboard focus states (`aria-live="polite"` status updates), and clean typography.

#### Independent Testability & Parallel Isolation
- Tested offline using mocked `/api/conveyor` JSON fixtures via Vitest + React Testing Library.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pnpm --filter @tc/batch_desk_web test -- ConveyorRibbon` verifying 3-episode FIFO display, Headless API banner, and saturation guard alerts.
- **Acceptance:** Conveyor UI clearly communicates both Headless automated execution and 3-slot FIFO Batch Desk queues.

### Task 179: Build Account Tabs `#1–#3` with `24h+5m` Rolling Reset Lockout (`apps/batch_desk_ui/web`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 177, Task 178
- **Files:** `apps/batch_desk_ui/web/src/components/AccountTabs.tsx`, `apps/batch_desk_ui/web/src/hooks/useCountdownLock.ts`, `apps/batch_desk_ui/web/tests/AccountTabs.test.tsx`
- **Tests:** Simulated clock timer tests proving Account Tabs lock completely until `next_daily_reset_utc_ms` (`first_daily_spend + 24h + 5m`), render exact `HH:MM:SS` unlock countdown, and isolate lockouts per account (`#1` locked does not lock `#2`).

#### Scope And Implementation Requirements
- Implement **`AccountTabs.tsx`** (for creators choosing the optional `HumanBatchDeskBackend` mode) managing Google Accounts `#1`, `#2`, and `#3`:
  - Show remaining daily credits (`50/50`), monthly reserve pool (`1,000/1,000`), and exact rolling reset timestamp read from `google_accounts.next_daily_reset_utc_ms` (`first_daily_spend_utc_ms + 86_400_000 + 300_000`).
  - **CRITICAL AUDIT FIX (`24h+5m` Lockout Guard):** When `daily_credits_remaining == 0` OR `now < next_daily_reset_utc_ms`, physically **LOCK** job-card generation buttons inside that account tab with a clear countdown timer (`"Daily Free Reset in 02:14:32 — Locked to protect monthly reserve"`), plus explicit ToS multi-account notice badge!
  - Auto-unlock reactively the exact second `Date.now() >= next_daily_reset_utc_ms` via client timer + server validation check.

#### Edge Cases And Failure Modes
- User's Windows system clock drifts slightly ahead of UTC server clock: derive remaining countdown strictly from `server_now_utc_ms` delta synced via WebSocket/API response header rather than naive raw `Date.now()`, preventing premature 2-minute-early clicks!
- Emergency manual override to spend Monthly Reserve (`1,000/mo`): hide strictly behind a deliberate two-step confirmation modal (`"Confirm Monthly Reserve Spend?"`) rather than allowing accidental daily-shift reserve clicks.

#### Bug Prevention And Invariants
- Even if a client tampers with disabled UI attributes, FastAPI backend (`Task 155 / 177`) enforces identical `next_daily_reset_utc_ms` lock unconditionally.

#### Independent Testability & Parallel Isolation
- Vitest fake-timers (`vi.useFakeTimers()`) suite advancing clock across `24h + 4m` (locked) -> `24h + 5m` (unlocked) boundary.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pnpm --filter @tc/batch_desk_web test -- AccountTabs` confirming exact server-delta `24h+5m` lock and multi-account independence.
- **Acceptance:** Rolling reset lock prevents multi-week evening shift drift and accidental monthly reserve depletion.

### Task 180: Implement `x1` Job Card (`1-Click Copy Safe Prompt`, Thumbnails & Dropzone) (`apps/batch_desk_ui/web`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 177, Task 179
- **Files:** `apps/batch_desk_ui/web/src/components/BatchJobCard.tsx`, `apps/batch_desk_ui/web/tests/BatchJobCard.test.tsx`
- **Tests:** Clipboard copy test (`<= 15 word` Safe Prompt), monochrome Start/End PNG thumbnail preview test, drag-and-drop MP4 upload test, and `"Open Flow in Browser"` launch link check.

#### Scope And Implementation Requirements
- Implement the ultra-streamlined **`BatchJobCard.tsx`** so human operators using optional Batch Desk mode process `1` Flow clip in `~45 seconds` with zero cognitive overload:
  - Enforces **strict `x1` card concurrency** per active tab so operator never mixes up prompts/files across clips.
  - Displays `prompt_mode` (`TEXT_TO_VIDEO` / `FIRST_FRAME` / `FIRST_AND_LAST_FRAME`), side-by-side **Start / End Bookend PNGs** (when applicable, verified crimson-free monochrome), target model badge (`manual-desk-video` + exact `3s–10s` bucket), and **1-Click `Copy Motion Prompt`**.
  - Features accessible **Drag-and-Drop MP4 Dropzone** supporting both pointer drag-drop and standard `<input type="file">` file picker cleanly for keyboard accessibility.

#### Edge Cases And Failure Modes
- Clipboard API blocked inside non-HTTPS local preview origin or older context: include automatic fallback `document.execCommand('copy')` + selectable readonly input highlight so 1-click copy never breaks silently.
- Operator drops wrong file format (`.png` or `.txt` onto MP4 dropzone): reject client-side immediately with helpful inline feedback without hitting backend disk.

#### Bug Prevention And Invariants
- Keep card layout minimal (`~1` focal job visible per active tab) with explicit confirmation feedback (`"Copied 12-word safe prompt!"`).

#### Independent Testability & Parallel Isolation
- Vitest + Testing Library unit tests simulating clipboard copy, file drag-over, and valid/invalid file drops.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pnpm --filter @tc/batch_desk_web test -- BatchJobCard` with 100% pass across clipboard, keyboard file pick, and drag-drop tests.
- **Acceptance:** Streamlined `x1` Job Card cuts manual Batch Desk friction cleanly.

### Task 181: Build Live Vision QA Status & 2-Strike Amber->Fallback Card UX (`apps/batch_desk_ui/web`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 180
- **Files:** `apps/batch_desk_ui/web/src/components/VisionQaBanner.tsx`, `apps/batch_desk_ui/web/tests/VisionQaBanner.test.tsx`
- **Tests:** State transition tests (`Uploading -> <2s Vision QA -> Strike 1 Amber Simplified Prompt -> Strike 2 Fallback Swapped Card` + `Pass` green celebration).

#### Scope And Implementation Requirements
- Implement live WebSocket-driven **`VisionQaBanner.tsx`** giving operators sub-2-second visual feedback right after dropping a clip (or watching Headless API completions stream past):
  - **Uploading / Conforming (`CFR 30fps`)** spinner with progress bar.
  - **Passed (`qa_passed`):** Clean emerald badge + auto-advance to next pending clip in oldest-first queue!
  - **Strike 1 Fail (`Amber Retry Alert`):** Displays exact failed Vision QA reason (`"Garbled text artifact at t=4.2s"`) and immediately auto-replaces prompt box with the circuit-breaker's ultra-simplified `<= 10 word` safe rewrite + `1-Click Copy Simplified Prompt` button!
  - **Strike 2 Fail (`Circuit Breaker Tripped -> Fallback Active`):** Displays clear muted slate state (`"Fallback Engaged (STILL_2K_PANZOOM) — 0 extra credits spent"`), removes card from manual queue, and advances cleanly!

#### Edge Cases And Failure Modes
- WebSocket disconnects briefly mid-QA poll: automatically fall back to `2s` interval polling on `/api/episodes/{id}/cards` until socket reconnects cleanly (`exponential reconnect`).

#### Bug Prevention And Invariants
- Never allow operator to click `"Retry"` a 3rd time once Strike 2 circuit breaker transitions a card to `fallback_triggered`.

#### Independent Testability & Parallel Isolation
- Vitest UI state tests driven by deterministic WebSocket mock events.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pnpm --filter @tc/batch_desk_web test -- VisionQaBanner` asserting all 4 telemetry states and Strike-2 hard lock.
- **Acceptance:** Real-time Strike-1 Amber guidance and Strike-2 fallback clarity keep operators safe from retake loops.

### Task 182: Add Pre-Flight 480p Animatic Player & `10x10` Margin Grid Inspector (`apps/batch_desk_ui/web`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 138, Task 144, Task 177
- **Files:** `apps/batch_desk_ui/web/src/components/PreflightAnimaticModal.tsx`, `apps/batch_desk_ui/web/src/components/SpatialGridInspector.tsx`, `apps/batch_desk_ui/web/tests/Inspectors.test.tsx`
- **Tests:** Native `<dialog>` modal accessibility tests (ESC close, focus trap), HTML5 `<video>` animatic seek + chapter list clicks, and `A–J/1–10` margin grid zoom overlay toggle tests.

#### Scope And Implementation Requirements
- Build two visual pre-flight review tools inside the cockpit (allowing creators to spot pacing or framing mistakes BEFORE triggering overnight mastering or Headless video spend):
  1. **`PreflightAnimaticModal.tsx`:** Uses native HTML5 `<dialog>` (`showModal()`) embedding the `480p` wireframe animatic (`Task 138`) with clickable scene-by-scene jump links (`[04:12] Scene S032 — STILL_2K_PANZOOM`) to audit narrative rhythm and FOIA L-Cut handoffs in `< 60 seconds`.
  2. **`SpatialGridInspector.tsx`:** Displays the `Task 144` **External-Margin `10x10` Grid** preview image for each 2K crime-scene still alongside locked anchor overlays (`span_cols x span_rows` boxes + predicted screen-space crimson circle locations on edge-clamped anchors).

#### Edge Cases And Failure Modes
- Large `480p` animatic file seeked repeatedly via HTML5 `<video>`: confirm FastAPI streaming endpoint (`FileResponse` / HTTP `206 Partial Content` byte-range support) handles scrub seeks smoothly without restarting playback at `0:00`!

#### Bug Prevention And Invariants
- Native `<dialog>` elements handle Escape dismissal and screen-reader semantics cleanly without brittle third-party modal portals.

#### Independent Testability & Parallel Isolation
- Vitest + mocked media URLs testing seek callbacks and anchor box rendering geometry.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pnpm --filter @tc/batch_desk_web test -- Inspectors` + verify FastAPI `206 Partial Content` range headers in API tests.
- **Acceptance:** Creators can inspect 480p pacing and 2K spatial crops visually before mastering.

### Task 183: Build Mandatory 5-Gate Human Release Sign-Off & Morning Upload Readiness View (`apps/batch_desk_ui/web`)
- **Owner:** Developer B (Part 2) | **Milestone:** M0.5 / M2-P2 | **Depends on:** Task 173, Task 177
- **Files:** `apps/batch_desk_ui/web/src/components/UploadReadinessView.tsx`, `apps/batch_desk_ui/web/tests/UploadReadinessView.test.tsx`
- **Tests:** Release-gate enforcement tests verifying `READY_TO_UPLOAD` remains locked until an accountable named reviewer approves ALL 5 `release_approvals` gates for `ready_bundle_sha256`, clears any fail-closed `PENDING_MANUAL_SPOT_CHECK` items, and can trigger the 24h post-publish correction/takedown log (`F-06`).

#### Scope And Implementation Requirements
- Implement **`UploadReadinessView.tsx`** as the accountable human release sign-off cockpit reviewing episodes parked in **`PENDING_HUMAN_SIGNOFF`** before promoting to `ready_to_upload/<slug>/`:
  - Renders `qa_certificate.json` pass pills: `-14.0 LUFS / <= -1.0 dBTP`, `Safe-Zone`, `2x2 Vision QA`, `Healed Scenes Count`, and exact `Unit Economics` (from `budget_reservations`).
  - **Mandatory 5-Gate Human Release Checklist (`F-06`):** Requires explicit named `reviewer_id` sign-off recorded in `release_approvals` + `audit_log` against exact `ready_bundle_sha256` across all 5 gates (`FACTUAL_ACCURACY`, `PRIVACY_PII`, `SOURCE_RIGHTS`, `SYNTHETIC_DISCLOSURE`, `ILLUSTRATIVE_LABELING`). `Promote to READY_TO_UPLOAD` stays disabled (and rejected server-side by `trg_episode_release_gate`) until ALL 5 gates are `APPROVED` and zero jobs remain in `PENDING_MANUAL_SPOT_CHECK` or `UNKNOWN_RECONCILE`!
  - Displays side-by-side **A/B/C Brand-Coherent Novel Thumbnails** (`< 2 MB`) + 1-click copy buttons for `YouTube Title`, `Description + Chapters`, `Fact Provenance Citations`, and `Synthetic Disclosure Reminder`, plus a **Post-Publish Correction / Takedown / Legal-Hold Action Panel** logging `POST_PUBLISH_CORRECTION` / `TAKEDOWN` in `audit_log`.

#### Edge Cases And Failure Modes
- Upstream case flips to `REVERSED` while episode sits in `PENDING_HUMAN_SIGNOFF`: `trg_case_disposition_quarantine` flips episode to `QUARANTINED_LEGAL_HOLD` and revokes approvals; UI immediately displays red Legal Hold banner and disables upload promotion!
- Episode has any `human_audio_review_required = 1` or `PENDING_MANUAL_SPOT_CHECK` item: surface mandatory audio/clip playback player before enabling gate approval.

#### Bug Prevention And Invariants
- Never modify `ready_to_upload/` immutable files from UI; every approval/upload/takedown mutation requires `X-Local-Auth-Token` and records an immutable row in `audit_log`.

#### Independent Testability & Parallel Isolation
- Tested standalone using golden `qa_certificate.json` + `provenance_bundle.json` fixtures.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pnpm --filter @tc/batch_desk_web test -- UploadReadinessView` verifying flag acknowledgement gate and chapter/SEO copy actions.
- **Acceptance:** Morning upload review closes the production loop safely in `< 3 minutes` per episode.

### Task 184: Implement Honest YouTube Analytics & Studio CSV Monetization Ingestor (`packages/analytics_feedback`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 003, Task 004
- **Files:** `packages/analytics_feedback/pyproject.toml`, `packages/analytics_feedback/src/analytics_feedback/yt_poller.py`, `packages/analytics_feedback/tests/test_yt_poller.py`
- **Tests:** Mocked YouTube Analytics (`youtubeAnalytics.reports.query`) & YouTube Studio CSV export ingestor tests verifying honest `adsense_status = 'UNKNOWN'` (`adsense_source = 'UNAVAILABLE'`) defaults, nullable `ctr_pct`, watch hours, and retention curves (`F-12`).

#### Scope And Implementation Requirements
- **CRITICAL AUDIT FIX (`F-12` — No Fabricated `videos.list` Monetization Field):** Bootstrap `packages/analytics_feedback` separating supported creator API metrics from Studio-exported fields cleanly:
  - Query **`youtubeAnalytics.reports.query`** strictly for supported creator-authorized metrics (`views`, `estimatedMinutesWatched` -> `watch_hours_total`, `averageViewPercentage`, and relative audience retention curve bins for 30s hook & min 6–14 dips) at `48h`, `7d`, and `30d` snapshots (`metrics_source = 'YT_ANALYTICS_API'`).
  - **Do NOT request `monetizationDetails` or yellow-icon status from `videos.list`** (the YouTube Data API `videos` resource does not expose monetization icons). Set `episode_analytics.adsense_status = 'UNKNOWN'`, `adsense_source = 'UNAVAILABLE'`, and `ctr_pct = NULL` whenever only API metrics exist!
  - Implement **`ingest_studio_csv(path)`** and manual creator entry endpoints (`POST /api/episodes/{id}/analytics-status`) to ingest verified YouTube Studio CSV exports (populating `ctr_pct`, `rpm_micro_usd`, `adsense_status`, `adsense_source = 'STUDIO_CSV_EXPORT' | 'MANUAL_CREATOR_ENTRY'`, and `adsense_checked_at` provenance cleanly).
  - Track rolling channel watch-hour runway toward YouTube Partner thresholds with freshness timestamps.

#### Edge Cases And Failure Modes
- OAuth token expired or channel not yet linked to YouTube Partner / Analytics scope: record `adsense_status = 'NOT_LINKED'` / `'UNKNOWN'` cleanly and fall back seamlessly to `ingest_studio_csv(path)` without fabricating defaults or crashing!
- Very new upload (`< 12h` old) returning sparse retention curve bins: leave `retention_30s_pct` / `retention_min6_14_pct` as `NULL` instead of recording misleading `0.0%` scores.

#### Bug Prevention And Invariants
- Never hardcode OAuth secrets or store unencrypted refresh tokens inside repo files; load via `YOUTUBE_OAUTH_CREDENTIALS_PATH` env var / OS keyring.

#### Independent Testability & Parallel Isolation
- Offline mock API & Studio CSV import tests validating exact `episode_analytics` row mappings and `8,000`-hr progress math.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/analytics_feedback/tests/test_yt_poller.py` verifying OAuth mock poll, Studio CSV fallback ingestor, and retention curve extraction.
- **Acceptance:** Post-publish CTR, retention dips, yellow-icon flags, and `8,000`-hour runway flow continuously back into system state.

### Task 185: Implement Calibration Signals for Agent 1 & Agent 4 + Analytics Dashboard Widget (`packages/analytics_feedback`, `apps/batch_desk_ui/web`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 184, Task 178
- **Files:** `packages/analytics_feedback/src/analytics_feedback/calibrator.py`, `packages/analytics_feedback/tests/test_calibrator.py`, `apps/batch_desk_ui/web/src/components/AnalyticsPulseCard.tsx`
- **Tests:** Archetype & retention calibration tests (flagging high-dip mid-roll pacing for Agent 4, flagging yellow-icon topic sensitivities for Agent 1, and thumbnail CTR winners) + UI component render tests.

#### Scope And Implementation Requirements
- Implement `FeedbackCalibrator` aggregating historical `episode_analytics` rows into structured JSON calibration advisories (`calibration_weights.json` read cleanly by Part 1 Agent 1 topic scoring and Agent 4 scene pacing without tight runtime coupling!):
  - **Yellow-Icon Alert Detector:** Automatically lowers niche risk weighting on sub-topic tags that triggered `limitedAds / yellow_icon` on `>= 2` episodes.
  - **Mid-Roll Dip Pacer:** Detects recurring retention drops in minutes `6–14` across last 5 videos and recommends tightened pattern-interrupt density (`Code <-> 2K` switch cadence) to Agent 4.
  - **Thumbnail Archetype CTR Ranker:** Reports trailing CTR performance per novelty archetype (`Task 172`) to bias thumbnail A/B ordering.
- Add compact **`AnalyticsPulseCard.tsx`** inside `apps/batch_desk_ui/web` surfacing trailing 30d CTR, 30s Hook %, Yellow-Icon Count, and `X / 8,000` Watch Hours bar.

#### Edge Cases And Failure Modes
- Cold start (`< 3` published episodes): emit neutral baseline weights (`adjustment = 0.0, confidence = "insufficient_sample"`) so early statistical noise never distorts Agent 1/4 prompts!

#### Bug Prevention And Invariants
- Calibration advisories are strictly bounded (`+/- 15%` weight shift cap) and never bypass `0`-tolerance legal/copyright hard rules.

#### Independent Testability & Parallel Isolation
- Offline fixture tests feeding 6 synthetic historical episodes (2 yellow-icon, 3 mid-roll-dip, 1 breakout high-CTR) and verifying bounded weight shifts.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/analytics_feedback/tests/test_calibrator.py` + `pnpm --filter @tc/batch_desk_web test -- AnalyticsPulseCard`.
- **Acceptance:** Automated YouTube performance telemetry feeds actionable bounded calibration back to Topic Selection and Director pacing.

### Task 186: Execute Playwright Browser E2E Suite for `batch_desk_ui` (`apps/batch_desk_ui`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 179, Task 181, Task 182, Task 183, Task 185
- **Files:** `apps/batch_desk_ui/e2e/playwright.config.ts`, `apps/batch_desk_ui/e2e/tests/batch_desk_flow.spec.ts`
- **Tests:** Real Chromium browser E2E driving FastAPI + React UI through 3-slot FIFO queue, `24h+5m` Account Tab lockout verification, Copy Safe Prompt, Strike-1 Amber -> Pass MP4 drop, Animatic modal scrub, and Morning Upload Readiness check.

#### Scope And Implementation Requirements
- Wire full end-to-end Playwright browser automation spinning up FastAPI (`uvicorn` in standalone fixture mode on ephemeral port) + built React bundle (`vite preview`) cleanly.
- Assert critical user journeys end-to-end in real headless Chromium:
  1. `3-Episode Conveyor Ribbon` lists `ep_golden_01..03` strictly oldest-first alongside `Headless API` default status banner.
  2. Locked Account Tab `#1` disables checkout until `next_daily_reset_utc_ms` while Tab `#2` remains interactive.
  3. Clicking `Copy Safe Prompt`, dropping synthetic Strike-1 test MP4 -> triggers live `<2s` WebSocket `Amber Retry Alert` with simplified prompt -> dropping clean MP4 clears card cleanly.
  4. Opening `PreflightAnimaticModal` & `SpatialGridInspector` renders `<dialog>` + margin grid without console errors.
  5. `UploadReadinessView` & `AnalyticsPulseCard` render `-14.0 LUFS` badge and `8,000-hr` tracker cleanly.

#### Edge Cases And Failure Modes
- Port collision when running Playwright alongside another local dev server: dynamically allocate ephemeral localhost port via Node `net.createServer()` helper cleanly.

#### Bug Prevention And Invariants
- Zero uncaught `pageerror` or HTTP `500` responses allowed during entire Playwright run.

#### Independent Testability & Parallel Isolation
- Tested 100% standalone inside Developer B workspace against golden Part 2 fixtures.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pnpm --filter @tc/batch_desk_e2e test` and observe 100% pass across all 5 headless Chromium user journeys.
- **Acceptance:** Full FastAPI + React Batch Desk Cockpit verified end-to-end in real Chromium.

### Task 187: Build Part 2 Golden Harness & Cross-Engine Visual Sync Fixture Suite (`tests/part2_harness`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 152, Task 162, Task 176, Task 186
- **Files:** `tests/part2_harness/run_golden_p2.py`, `tests/part2_harness/assertions.py`
- **Tests:** Automated Part 2 full-stack harness running all 4 Part 2 packages (`render_catalog`, `python_motion`, `crime_scene_2k`, `flow_adapter`, `agent6_mastering`, `analytics_feedback`) against golden stub manifests (`ep_golden_01..03.json`).

#### Scope And Implementation Requirements
- Build the unified Part 2 Golden Verification Harness running the complete Developer B visual/audio/mastering stack autonomously from frozen golden inputs (`fixtures/ep_golden_01..03.json`) without calling Part 1 code or external paid APIs:
  - Runs `@tc/render_catalog` (all 12 motifs, 0 `<feTurbulence>`, `<5s` JS-boil verified).
  - Runs `python_motion` (monochrome crimson-free Flow bookends + 48kHz SFX + 480p animatic).
  - Runs `crime_scene_2k` (pre-locked `spatial_anchors`, edge-clamped screen projection).
  - Runs `flow_adapter` (default `GeminiOmniInteractionsBackend` offline transport mock + optional `HumanBatchDeskBackend` Strike-1/Strike-2 simulation, `$0` API spend).
  - Runs `agent6_mastering` (strict `CFR 30fps`, per-track pre-norm -> `-filter_complex_script` -> `linear=true` `-14.0 LUFS`, continuous single grain leaving FOIA raw, Safe-Zone scan, `2x2` Vision QA mock, `<5s` surgical heal, Brand-Novel thumbnails, atomic `ready_to_upload/`).
- Produce structured machine-readable `part2_harness_metrics.json`.

#### Edge Cases And Failure Modes
- Non-clean cleanup leaving stale `ready_to_upload` files from earlier harness runs masking fresh assertions: clean ephemeral workdir completely per run and verify fresh SHA-256 outputs.

#### Bug Prevention And Invariants
- Zero network calls outside localhost mock FastAPI/Playwright servers allowed during golden harness execution.

#### Independent Testability & Parallel Isolation
- 100% Developer B owned and runnable offline.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `python tests/part2_harness/run_golden_p2.py` with exit code `0` across `ep_golden_01..03`.
- **Acceptance:** Part 2 full visual/audio/mastering conveyor runs autonomously end-to-end on frozen contracts.

### Task 188: Verify Single-Pass Grain, Raw FOIA & `<5s` Self-Heal Proof in Part 2 Harness (`tests/part2_harness`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 187
- **Files:** `tests/part2_harness/test_part2_invariants.py`
- **Tests:** Forensic pixel/waveform assertion suite inspecting outputs generated by `run_golden_p2.py` for Safe-Zone clip triggers, `<5s` heal completion, FOIA raw integrity, and `-14.0 LUFS / <= -1.0 dBTP` precision.

#### Scope And Implementation Requirements
- Write strict forensic post-build verification tests analyzing artifacts exported by `run_golden_p2.py`:
  - Inject an intentional bottom-bar Safe-Zone collision into `ep_golden_02.json` and assert `agent6_mastering` autonomously detects it in `safe_zone_scanner.py`, heals ONLY that scene in `< 5.0s`, preserves exact timeline frame count, and ships passing `qa_certificate.json`.
  - Verify `FOIA_REAL_FOOTAGE` clips inside `final_1080p30.mp4` show zero added paper-grain PSNR distortion while `CODE_STICKMAN` <-> `STILL_2K_PANZOOM` seams display unified grain.
  - Assert `ebur128` integrated loudness `-14.0 +/- 0.3 LUFS` and `TP <= -1.0 dBTP` across every generated MP4.

#### Edge Cases And Failure Modes
- Slight codec compression loss on exact FOIA re-encode check: validate PSNR against `crf=18` reference encode (`>= 45 dB`) vs double-grained threshold (`< 36 dB`), distinguishing cleanly between subtle H.264 encode variance and unwanted synthetic grain overlay.

#### Bug Prevention And Invariants
- Hard-fail if healed scene triggers full-episode Remotion re-render instead of single `--scene` heal (`render_count != 1`).

#### Independent Testability & Parallel Isolation
- Standalone Part 2 forensic audit test suite.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest tests/part2_harness/test_part2_invariants.py` with 100% pass across all forensic checks.
- **Acceptance:** All v2 audit rendering/audio/heal guarantees proven empirically on Part 2 exports.

### Task 189: Verify Early Offline Vertical Slice Part 2 Readiness (`Authoritative 4-Motif MVP + Omni Mock + -14 LUFS`) (`tests/part2_harness`)
- **Owner:** Developer B (Part 2) | **Milestone:** M0.5 Early Offline Slice | **Depends on:** Task 109, Task 115, Task 117, Task 118, Task 122, Task 147, Task 153, Task 168 (`F-01`, `F-17` — runs 100% offline at `$0.00` spend!)
- **Files:** `tests/part2_harness/test_mvp_vertical_slice_p2.py`
- **Tests:** Fast `<30s` strictly offline smoke suite (socket-blocked, `$0` API calls!) compiling the **authoritative `MOTIF_REGISTRY_V1` 4-Motif MVP Slice** (`StickmanStage`, `AudioEvidenceCard`, `RedactedDocReveal`, `FoiaFootageFrame`), `crime_scene_2k` (with `ILLUSTRATIVE RECONSTRUCTION` badge), mocked `gemini-omni-1.2-flash` Interactions transport (`OFFLINE_TEST`), `-14.0 LUFS` audio master, and 5-gate `release_approvals` sign-off (`F-01`, `F-16`, `F-17`).

#### Scope And Implementation Requirements
- Implement the **Early Offline Thin Vertical Slice Gate (Part 2 side)** immediately after core rendering/mastering lands—guaranteeing **`$0.00` external API spend** (any real network call fails immediately; live connectivity check deferred post-integration to `Task 200` `F-01`).

#### Edge Cases And Failure Modes
- Manifest referencing only 4 MVP motifs accidentally failing catalog balance warnings: confirm `render_report.json` cleanly respects `--mvp-4-motifs` flag without raising spurious missing-variety warnings.

#### Bug Prevention And Invariants
- Smoke slice must exercise real FFmpeg muxing and Remotion Chromium rendering (not skipped stubs).

#### Independent Testability & Parallel Isolation
- Standalone Part 2 fast smoke suite.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest tests/part2_harness/test_mvp_vertical_slice_p2.py` completing cleanly in `< 30s`.
- **Acceptance:** Part 2 Thin Vertical Slice is green and ready for early Part 1 live handshake (`Task 193`).

### Task 190: Execute Part 2 UI + API + Pipeline Concurrency Stress Test (`tests/part2_harness`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 186, Task 187
- **Files:** `tests/part2_harness/test_ui_pipeline_concurrency.py`
- **Tests:** Simultaneous load test executing overnight mastering worker background process while FastAPI + UI tabs perform 50 concurrent API/WebSocket operations with zero SQLite `database is locked` errors.

#### Scope And Implementation Requirements
- Prove zero `SQLITE_BUSY` failures when background Part 2 mastering threads report progress through FastAPI while active Batch Desk UI clients poll conveyor state, switch accounts, and drop clips concurrently under `WAL` + `busy_timeout=5000` single-writer architecture.

#### Edge Cases And Failure Modes
- Long-running write transaction holding lock past `busy_timeout`: verify all FastAPI DB mutations execute in `< 15 ms` outside media transcode I/O (`never hold SQLite transactions across FFmpeg calls!`).

#### Bug Prevention And Invariants
- Zero unhandled `sqlite3.OperationalError` exceptions across 50 concurrent operations.

#### Independent Testability & Parallel Isolation
- Self-contained Part 2 concurrency verification suite.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest tests/part2_harness/test_ui_pipeline_concurrency.py` verifying zero lock errors and `< 25 ms` P99 DB write latency.
- **Acceptance:** Single-writer FastAPI bridge remains rock-solid under mixed interactive + background load.

### Task 191: Publish Part 2 Documentation, Developer Runbook & Package Checksums (`packages/*`, `apps/*`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 | **Depends on:** Task 190
- **Files:** `docs/PART2_RUNBOOK.md`, `contracts/part2_checksums.json`
- **Tests:** Automated CLI help-text & schema-export freshness check verifying CLI docs match live parser options.

#### Scope And Implementation Requirements
- Author crisp operational documentation (`docs/PART2_RUNBOOK.md`) covering Part 2 package installation (`uv` / `pnpm`), `providers.yaml` configuration (`gemini_omni_interactions` default vs optional `vertex_veo_enterprise` / `human_batch_desk`), offline socket-blocked Playwright E2E commands, `<5s` heal target diagnostics, and `-14.0 LUFS` troubleshooting.
- Export SHA-256 contract verification manifests proving zero unapproved changes to `contracts/schemas/`.

#### Edge Cases And Failure Modes
- CLI flags diverging from README examples over final edits: run automated `--help` snapshot verification inside CI test.

#### Bug Prevention And Invariants
- Confirm zero references to obsolete phantom Google Vids pools or dual Node/Python SQLite writers anywhere in Part 2 docs.

#### Independent Testability & Parallel Isolation
- Standalone Part 2 documentation check.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `python tests/part2_harness/check_docs_and_contracts.py` passing 100%.
- **Acceptance:** Part 2 workspace cleanly documented and contract-verified.

### Task 192: Pass Standalone Part 2 Certification Gate (`PART2_CERT_REPORT.md`)
- **Owner:** Developer B (Part 2) | **Milestone:** M2-P2 Exit Gate | **Depends on:** Task 188, Task 189, Task 190, Task 191
- **Files:** `artifacts/milestones/PART2_CERT_REPORT.md`, `tools/verify_part2_cert.ps1`
- **Tests:** Master Part 2 certification runner executing EVERY unit, integration, Playwright E2E, Remotion SLA, 1,200s A/V sync, and Golden Harness suite before declaring Developer B ready to merge with Developer A (`Task 100` gate match!).

#### Scope And Implementation Requirements
- Execute Developer B's final standalone certification script (`tools/verify_part2_cert.ps1`) verifying 100% green status across `@tc/render_catalog`, `python_motion`, `crime_scene_2k`, `flow_adapter`, `agent6_mastering`, `analytics_feedback`, `apps/batch_desk_ui`, and `tests/part2_harness`.
- Generate immutable `artifacts/milestones/PART2_CERT_REPORT.md` containing exact command outputs, test counts, Remotion JS-boil P95 latency (`< 5.0s`), measured LUFS (`-14.0 LUFS`), edge-clamped `crime_scene_2k` drift (`< 1.0px`), and zero-red Flow keyframe pass counts.

#### Edge Cases And Failure Modes
- Flaky Playwright timing under heavy parallel CPU test execution: run Playwright deterministically sequentially after parallel Python unit suites finish so CPU contention never skews `<5s` Remotion SLA numbers.

#### Bug Prevention And Invariants
- Both Developer A (`Task 100` `PART1_CERT_REPORT.md`) and Developer B (`Task 192` `PART2_CERT_REPORT.md`) MUST sign green reports independently before beginning `Tasks 193–200` Merge & System Certification!

#### Independent Testability & Parallel Isolation
- 100% Developer B independent exit gate.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `tools/verify_part2_cert.ps1` achieving 100% pass across all Part 2 suites and generate `PART2_CERT_REPORT.md`.
- **Acceptance:** Developer B (Part 2) officially certified independent and merge-ready.

### Task 193: Execute Milestone M0.5 Early Minimal End-to-End Offline Vertical Slice (`Plan -> Voice/WhisperX -> Create -> Edit`)
- **Owner:** Developer A & Developer B (Joint Early Checkpoint) | **Milestone:** M0.5 Early Offline Slice | **Depends on:** Task 004, Task 042, Task 052, Task 066, Task 189 (Zero API spend — live provider check deferred to `Task 200`! `F-01`, `F-17`)
- **Files:** `packages/integration_bridge/src/integration_bridge/mvp_slice.py`, `tests/integration/test_mvp_vertical_slice.py`
- **Tests:** Strictly **offline (`$0.00` spent, outbound sockets blocked!)** minimal end-to-end 90-second documentary vertical slice piping `1` primary-record verified case (`AFFIRMED` + `anonymization_status='APPROVED'`) -> `1` clearly labeled illustrative 2K plate -> `1` approved `ScenePlan` (`PLAN_APPROVED`) -> WhisperX word-aligned voice track -> **authoritative 4-motif MVP slice** (`StickmanStage`, `AudioEvidenceCard`, `RedactedDocReveal`, `FoiaFootageFrame`) -> **mocked** `gemini-omni-1.2-flash` transport (`OFFLINE_TEST == $0`) -> `-14.0 LUFS` master -> **all 5 mandatory human release approvals**!

#### Scope And Implementation Requirements
- Execute the **Milestone M0.5 Minimal End-to-End Offline Slice (`F-01`, `F-05`, `F-17`)** at **`$0.00` external API cost** BEFORE committing engineering hours to motifs #5–#12 or the full UI:
  - Part 1 enforces the 4-stage sequential lifecycle (`ScenePlan PLAN_APPROVED` -> WhisperX word timestamps -> `ANIMATIC_APPROVED`), proving narration revision invalidates dependent visuals cleanly (`STALE_NEEDS_REAPPROVAL`).
  - Part 2 renders `--mvp-4-motifs`, `crime_scene_2k` (burning `ILLUSTRATIVE RECONSTRUCTION — NOT CRIME SCENE PHOTO`), runs mocked `gemini-omni-1.2-flash` Interactions transport (`OFFLINE_TEST == $0`), and masters `-14.0 LUFS` via Agent 6.
  - Assert `trg_episode_release_gate` blocks `READY_TO_UPLOAD` until `ScenePlan` is `EDITED_APPROVED` and all 5 human gates in `release_approvals` are `APPROVED`!

#### Edge Cases And Failure Modes
- Real API key accidentally set in test shell: repo socket-blocker & credential scrub abort immediately BEFORE making any paid network call (`F-01`)!

#### Bug Prevention And Invariants
- Bridge code MUST NOT mutate locked `CaseBible`, `FactLedger`, `spatial_anchors`, or Part 1 linter decisions.

#### Independent Testability & Parallel Isolation
- First joint integration checkpoint uniting Developer A and Developer B pipelines end-to-end cleanly.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest tests/integration/test_mvp_vertical_slice.py` producing a valid playable 90-second documentary MP4 at `-14.0 LUFS` cleanly from Part 1 -> Part 2 live handoff.
- **Acceptance:** End-to-end cross-team data path validated on thin vertical slice.

### Task 194: Connect Full 12-Motif `LivePart2RenderAdapter` & Schema Handoff Bridge (`packages/integration_bridge`)
- **Owner:** Developer A & Developer B (Joint Merge) | **Milestone:** M3-INT | **Depends on:** Task 193
- **Files:** `packages/integration_bridge/src/integration_bridge/live_adapter.py`, `packages/integration_bridge/tests/test_live_adapter.py`
- **Tests:** Full-schema handoff integration tests replacing Part 1's `StubPart2RenderAdapter` seamlessly with Part 2's live 12-motif `@tc/render_catalog` + `python_motion` + `crime_scene_2k` + `flow_adapter` + `agent6_mastering` pipeline.

#### Scope And Implementation Requirements
- Implement `LivePart2RenderAdapter` satisfying the exact `Part2RenderAdapter` protocol used in Part 1 (`Task 096`), cleanly hot-swapping out Part 1's offline stub without modifying any Agent 1–4 logic!
- Verify all 12 Remotion visual archetypes (`MOTIF_REGISTRY_V1`), full `python_motion` SFX cue library (`500`-cue `-filter_complex_script`), multi-anchor `crime_scene_2k` tours (`340s`), global `monthly_budget_ledger` USD reservations (`providers.yaml`), and `ready_to_upload/` exporter execute cleanly on real Part 1 episode bundles (all offline mocked `$0` in CI).
- Verify SQLite database ownership remains 100% single-writer Python across the merged application (Part 1 orchestrator + FastAPI `desk_api` sharing the unified Python repository layer).

#### Edge Cases And Failure Modes
- Parallel sub-process startup timing (`uvicorn` FastAPI UI vs headless overnight CLI worker touching the same episode): enforce clean `episode_lock_lease` inside SQLite so interactive Batch Desk edits never collide with automated mastering runs!

#### Bug Prevention And Invariants
- Both `StubPart2RenderAdapter` (fast CI unit testing) and `LivePart2RenderAdapter` (production) must continue passing the shared `tests/contracts/` compliance suite indefinitely.

#### Independent Testability & Parallel Isolation
- Joint integration suite runnable with mock external Gemini/YouTube network endpoints OR `--live-staging` smoke toggle.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest packages/integration_bridge/tests/test_live_adapter.py` with 100% pass across all 12 motifs, 2K tours, SFX cues, and single-writer DB handoff.
- **Acceptance:** Full 12-motif Part 1 -> Part 2 production adapter seamlessly unified.

### Task 195: Verify Live Law 4 Early-2K Anchor Flow & Pre-Flight Animatic Sync (`tests/integration`)
- **Owner:** Developer A & Developer B (Joint Merge) | **Milestone:** M3-INT | **Depends on:** Task 194
- **Files:** `tests/integration/test_law4_early2k_handoff.py`
- **Tests:** Live Law 4 resolution test proving Part 1 Agent 2's early Image API + external-margin `10x10` `spatial_anchors` propagate cleanly into Agent 3 scripts -> Agent 4 `RULE_04` -> `crime_scene_2k` projected callouts -> `python_motion` 480p pre-flight animatic with zero circular deadlocks!

#### Scope And Implementation Requirements
- Execute an integrated multi-stage proof validating every resolved Law 4 / `RULE_01` / `RULE_11–12` audit invariant across BOTH teams' live codebases:
  - Part 1 runs Agent 2 -> early `flow_adapter.image_api` 2K generation -> external-margin `10x10` anchor lock -> `spatial_anchors` persisted BEFORE Agent 3/TTS runs.
  - Agent 3 generates segmented `VoiceTrackManifest` (`Track 1` narration slots + `Track 2` FOIA L-Cut inserts + Twist pads) matching `sum(scene.duration_ms)` cleanly (`RULE_01` passes!).
  - `python_motion` builds the `<25s` 480p animatic directly from real Part 1 output, and `crime_scene_2k` zooms accurately (`1.6x–3.8x`, `<1.0px` projected callouts on edge-clamped `A1`/`J10`).

#### Edge Cases And Failure Modes
- FOIA asset clipped at tail during ASR word timing causing `VoiceTrackManifest` L-Cut delta `+/- 150 ms`: verify `manifest_linter.py` and `agent6_mastering/audio_timeline.py` agree identically on L-Cut pre-lap clamping within `1 ms`.

#### Bug Prevention And Invariants
- Zero schema warnings or fallback coercions permitted on live Agent 2 -> Agent 4 -> `crime_scene_2k` roundtrip.

#### Independent Testability & Parallel Isolation
- Automated end-to-end state-machine verification using mocked Gemini/ElevenLabs HTTP transports.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest tests/integration/test_law4_early2k_handoff.py` confirming zero deadlocks and `<1.0px` anchor accuracy end-to-end.
- **Acceptance:** Early Law 4 anchor locking + segmented voice manifest verified flawlessly across merged Part 1 + Part 2.

### Task 196: Verify Live Optional Batch Desk `24h+5m` Loop, Overnight Heal & YT Analytics Calibration (`tests/integration`)
- **Owner:** Developer A & Developer B (Joint Merge) | **Milestone:** M3-INT | **Depends on:** Task 195
- **Files:** `tests/integration/test_batch_overnight_analytics_loop.py`
- **Tests:** Cross-system loop test exercising optional `HumanBatchDeskBackend` (`24h+5m` lock, 3-slot FIFO, Chromium Playwright drop) -> overnight `agent6_mastering` (`<5s` heal) -> `analytics_feedback` ingest -> Part 1 Agent 1/4 `calibration_weights.json` consumption!

#### Scope And Implementation Requirements
- Test the complete operational production & feedback cycle with live merged code:
  1. Stage an episode cleanly into `AWAITING_FLOW_BATCH` (testing the optional `HumanBatchDeskBackend` path end-to-end through FastAPI & Playwright).
  2. Enforce `24h+5m` Account Tab lockout across simulated multi-day shifts.
  3. Trigger overnight `agent6_mastering` with an injected Safe-Zone violation (`<5s` surgical single-scene heal).
  4. Feed synthetic YouTube Analytics (`3 yellow_icon` flags + minute `9–12` dip) through `analytics_feedback` -> verify Part 1 Agent 1 & Agent 4 automatically load updated `calibration_weights.json` on the subsequent episode run!

#### Edge Cases And Failure Modes
- Part 1 Agent 1 reads `calibration_weights.json` simultaneously while `analytics_feedback` updates it overnight: atomic `.tmp -> os.replace` write guarantee verified cleanly!

#### Bug Prevention And Invariants
- Verify zero SQLite lock failures across FastAPI interactive desk + overnight mastering + calibration updates.

#### Independent Testability & Parallel Isolation
- Integrated Playwright + Python E2E verification test.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest tests/integration/test_batch_overnight_analytics_loop.py` verifying closed-loop feedback from YouTube upload telemetry back into next episode topic/pacing selection.
- **Acceptance:** Full closed-loop conveyor, overnight heal, and YouTube Analytics calibration verified live.

### Task 197: Run Full Legal, PII, Copyright, Spoken-Redaction & Policy Red-Team Gauntlet (`tests/integration`)
- **Owner:** Developer A & Developer B (Joint Merge) | **Milestone:** M4-CERT | **Depends on:** Task 196
- **Files:** `tests/integration/test_red_team_full_gauntlet.py`
- **Tests:** Adversarial cross-pipeline red-team test suite attacking every legal, copyright, privacy, FOIA audio, and AdSense guardrail simultaneously across merged Part 1 + Part 2.

#### Scope And Implementation Requirements
- Execute a brutal full-pipeline red-team audit combining all safety/legal protections across Part 1 and Part 2:
  - **Active Minor / Juvenile PII & Spoken Audio Bleep:** Inject juvenile name into bodycam transcript AND audio -> assert Agent 2/3 hard-rejects living-minor victim case OR redacts/beeps exact spoken time intervals cleanly in `agent6_mastering` AND masks text on screen!
  - **YouTube Competitor Video ToS TTL + Anti-Steal:** Attempt to transcribe/reuse YouTube audio/frames as documentary clips OR expire past 30-day TTL -> assert hard gate block + zero-reupload guarantee + automated `30-day` purge cleanup!
  - **FOIA Music/Siren Conditional Demucs + Whole-Clip Profanity:** Pass clean 911 speech (assert Demucs bypassed—zero metallic artifacts!), pass copyrighted squad-car radio song (assert conditional Demucs vocal stem extraction!), pass dirty bodycam profanity -> verify whole-clip word-timestamps scan (`not just first 30s`) + AdSense bleep placement!
  - **Law 11/12 & Crimson Isolation:** Attempt `"shooting tracking shot"` (`benign cinematography bigram`) vs real crimson Start/End frame (`hard blocked before API`), plus Thumbnail AdSense gore/word-count rejection!

#### Edge Cases And Failure Modes
- Attempt to bypass Part 1 `disposition_status` legal block directly via Part 2 mastering CLI (`agent6-master run`): assert `agent6_mastering` ALSO inspects episode disposition/claim attestation in manifest/DB and hard-refuses mastering any unapproved (`LIVING_MINOR`, `UNVERIFIED_DEFAMATION`, `COPYRIGHT_LOCKED`) episode!

#### Bug Prevention And Invariants
- Zero red-team adversarial vectors may slip through into `ready_to_upload/`.

#### Independent Testability & Parallel Isolation
- Automated offline security/legal compliance test suite runnable in CI prior to any release tag.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest tests/integration/test_red_team_full_gauntlet.py` confirming 100% red-team block/redaction catch rate across all legal, PII, ToS, Demucs, and AdSense hazards.
- **Acceptance:** Full legal, copyright, privacy, and AdSense defenses hold across the merged pipeline.

### Task 198: Run 3-Slot Conveyor & `>50%` Sunk-Cost Chaos Soak Test (`tests/integration`)
- **Owner:** Developer A & Developer B (Joint Merge) | **Milestone:** M4-CERT | **Depends on:** Task 197
- **Files:** `tests/integration/test_conveyor_chaos_soak.py`
- **Tests:** 5-episode multi-day simulated conveyor soak test exercising 3 concurrent slots in `AWAITING_FLOW_BATCH`, FIFO oldest-first draining, mid-shift copycat wave aborts (`< 50%`), `> 50%` sunk-cost completions, SQLite `WAL` stress, and crash recovery.

#### Scope And Implementation Requirements
- Stress-test the entire multi-episode production conveyor across a simulated 5-episode accelerated calendar:
  - Queue 3 episodes simultaneously into `AWAITING_FLOW_BATCH` while Episode 4 triggers Part 1 Scout & Episode 5 sits in Research—proving zero conveyor starvation!
  - Inject a viral competitor copycat wave (`N_14d_wave = 4`) before Day 2 on Episode B (`35%` Flow spent -> aborted cleanly, slot freed automatically) vs Episode C (`68%` Flow spent, `N_14d_wave = 4 <= 5` -> sunk-cost guard completes Episode C cleanly!).
  - Inject random simulated `SIGKILL`/process restart checkpoints in both Part 1 and Part 2 -> assert idempotent resume with zero corrupted SQLite records or orphaned temp gigabytes.

#### Edge Cases And Failure Modes
- All 3 queued episodes abort simultaneously via copycat wave: ensure Part 1 Scout/Evidence backlog immediately promotes clean reserve cases into `AWAITING_FLOW_BATCH` without manual restart.

#### Bug Prevention And Invariants
- Assert exact SQLite `trg_case_disposition_guard` integrity and zero orphaned `.tmp`/`.staging_` directories post-soak.

#### Independent Testability & Parallel Isolation
- Offline simulated-clock chaos soak suite (`< 60s` wall-clock).

#### Verification, Testing And Acceptance Criteria
- [ ] Run `pytest tests/integration/test_conveyor_chaos_soak.py` observing 100% conveyor recovery, FIFO precision, and sunk-cost branch correctness.
- **Acceptance:** Multi-episode conveyor belt survives copycat waves, crashes, and slot saturation gracefully.

### Task 199: Audit 10-Episode Economics Model (`$135/mo` Autonomous Cap, `gemini-omni-1.2-flash` & `providers.yaml`) (`tests/integration`)
- **Owner:** Developer A & Developer B (Joint Merge) | **Milestone:** M4-CERT | **Depends on:** Task 198
- **Files:** `tests/integration/test_economics_10ep_audit.py`, `artifacts/milestones/ECONOMICS_10EP_AUDIT.md`
- **Tests:** 10-episode production unit-economics simulation (`$0` live API calls) checking BOTH **Conservative `0%`-Cache (`~$117–$135/mo`)** AND Best-Effort Cached (`~$95–$120/mo`) cumulative spend across ALL providers (`ALL_PROVIDERS <= $135/mo`), `deepseek_chat <= $38/mo`, `gemini_omni <= $104/mo` (`<= 10` clips / `80s` = `1.33m`, `$10.40/ep` DB cap), local WhisperX (`$0` ASR), Image API, and TTS (`F-02`, `Additional Check #1`).

#### Scope And Implementation Requirements
- Validate the canonical v4 unit-economics model across a 10-episode/month run via transactional `monthly_budget_ledger` + `provider_spend_reservations`:
  - Assert **global `ALL_PROVIDERS` cap (`$135/mo`) holds across ALL providers combined even under `0%` DeepSeek KV-cache hit rate** (`$38/mo` DeepSeek cap)!
  - Verify single-source-of-truth runtime distribution: **`13.0m (780s)` Code/FOIA + `5.67m (340s)` 2K Illustrative Stills + `1.33m (80s)` Omni 1.2 Flash (`max_hero_clips = 10`) = `20.0m (1,200s)`**.
  - Emit signed `artifacts/milestones/ECONOMICS_10EP_AUDIT.md`.

#### Edge Cases And Failure Modes
- Provider rate override tested in `providers.yaml` + simultaneous DeepSeek/Omni reservations near `$135`: SQLite `trg_provider_global_budget_cap_guard` blocks excess spend atomically!

#### Bug Prevention And Invariants
- Assert zero 10-episode runs breach `max_hero_clips = 10`, `$10.40/ep` DB video cap, or `$135/mo ALL_PROVIDERS` cap under `0%`-cache conservative math.

#### Independent Testability & Parallel Isolation
- Offline deterministic budget-reservation simulator (`OFFLINE_TEST == $0`).

#### Verification, Testing And Acceptance Criteria
- [ ] Run offline `pytest tests/integration/test_economics_10ep_audit.py` verifying `$135/mo ALL_PROVIDERS` solvency even at `0%` cache hits.
- **Acceptance:** Cross-provider economics & `0%`-cache resilience verified cleanly.

### Task 200: Compile Final 1,200-Second Offline Documentary, Run Deferred Bounded Live Check & Sign `V1_RELEASE_SCORECARD.md = GO` (`tests/integration`)
- **Owner:** Developer A & Developer B (Joint Merge) | **Milestone:** M4-CERT Final Gate | **Depends on:** Task 199
- **Files:** `tools/verify_v1_release.ps1`, `artifacts/milestones/V1_RELEASE_SCORECARD.md`
- **Tests:** Master end-to-end 1,200-second offline full build + all 200-task unit/contract/injection/conveyor suites (`$0` spend), followed **strictly last** by ONE explicitly opted-in bounded live connectivity check (`--live-sandbox` + `ALLOW_PAID_SANDBOX=1`, **`<= $2.00` hard cap, 1 call, `0` retries**) to verify live `gemini-omni-1.2-flash` endpoint/billing (`F-01`, `F-08`).

#### Scope And Implementation Requirements
- Execute the final flagship certification milestone (**Wave-Merged Full Offline Matrix -> Deferred Bounded Connectivity Check -> Release Scorecard**):
  1. Run schema integrity suite (`node schema/schema-test.js` **12/12**) + Mermaid diagram merge check (`node tools/merge-diagrams.js`) + `verify-harmony.mjs` contract drift check.
  2. Run complete offline Part 1, Part 2, Playwright, Red-Team Legal/PII/Injection (`Additional Check #2`), Crash/Conveyor Soak (`<15ms` drift), and 1,200-second full documentary build (all `scene_plans` = `EDITED_APPROVED` + all 5 human `release_approvals` signed) at **`$0.00` external API spend**.
  3. **ONLY after Steps 1–2 pass 100% green**, run ONE bounded post-integration live connectivity check (`--live-sandbox`, `purpose = 'LIVE_SANDBOX'`, hard cap `<= $2.00`, `1` test call, `0` automated retries) recording real `gemini-omni-1.2-flash` latency & invoice rate against `providers.yaml` (`F-01`).
  4. Stamp `artifacts/milestones/V1_RELEASE_SCORECARD.md = GO` *(explicitly distinguishing verified runtime test results from blueprint/design specs; YouTube monetization monitored separately by human reviewers, `F-08`, `F-13`)*.

#### Edge Cases And Failure Modes
- Any single test failure, unsigned `release_approvals` gate, unresolved `PENDING_MANUAL_SPOT_CHECK`, LUFS deviation (`> 0.4 LU`), A/V drift (`> 15 ms`), leaked `.staging_` artifact, or Safe-Zone miss MUST automatically stamp `RELEASE_DECISION: NO-GO` and return non-zero exit code `1`.

#### Bug Prevention And Invariants
- Zero manual post-processing steps allowed between `Task 200` launch and final `PENDING_HUMAN_SIGNOFF` -> `ready_to_upload/v1_cert_episode/final_1080p30.mp4` inspection.

#### Independent Testability & Parallel Isolation
- Final automated V1 merge & release certification runner.

#### Verification, Testing And Acceptance Criteria
- [ ] Run `tools/verify_v1_release.ps1` and observe all unit, contract, Playwright, red-team, chaos soak, and 1,200-second build gates pass cleanly with exit code `0`.
- [ ] Verify `artifacts/milestones/V1_RELEASE_SCORECARD.md` records `RELEASE_DECISION: GO`.
- **Acceptance:** Automated True-Crime Documentary Pipeline V1 is certified end-to-end, audit-hardened, and ready for human-reviewed production operation.

---

## Out of Scope for V1 (Explicitly Deferred to V2+)

The following capabilities remain intentionally excluded from V1 implementation to protect delivery velocity, legal safety, and deterministic quality:
1. **Direct Automated YouTube Studio API Video Publishing:** V1 pauses cleanly at `PENDING_HUMAN_SIGNOFF` for mandatory 5-gate accountable reviewer sign-off (`FACTUAL_ACCURACY`, `PRIVACY_PII`, `SOURCE_RIGHTS`, `SYNTHETIC_DISCLOSURE`, `ILLUSTRATIVE_LABELING`) before promoting `ready_to_upload/<slug>/`; creators upload manually via YouTube Studio.
2. **Phantom Google Vids Capacity Pool & Retired Veo 3.1 Preview Endpoints:** Explicitly removed; primary video generation uses **`gemini-omni-1.2-flash`** via the **Gemini Interactions API** (`<= 10` clips / `80s`), while 2K illustrative stills use the Official Gemini Image API + Multi-Turn Editing (`Task 154`) and `crime_scene_2k` Lanczos tours.
3. **Autonomous Browser-Automation Bots Clicking Logged-In Web UIs:** Strictly forbidden; automated runs default cleanly to `GeminiOmniInteractionsBackend`, while optional manual workflows run strictly via human Drag-and-Drop inside `HumanBatchDeskBackend`.
4. **Full 3D Unreal / Blender Raytraced Crime Reconstructions:** V1 focuses exclusively on crisp editorial 2D parchment/charcoal typography (`@tc/render_catalog`), clearly labeled `ILLUSTRATIVE RECONSTRUCTION` 2K pans (`crime_scene_2k`), and bounded `80s` Hero beats.
5. **Automated Multi-Language Dubbing / Non-English Channels:** V1 targets English documentary narration (`en-US` ASR / TTS) with localized expansion reserved for V2.

---

## Parallel Execution, Wave Merge & Offline-First Testing Runbook (2 Developers)

### Day 1 — Shared Contract Freeze (`Tasks 001–004`)
- Pair on monorepo scaffolding, frozen Pydantic + Zod schemas (`packages/shared_contracts/`), `providers.yaml` (`gemini-omni-1.2-flash`, `max_hero_clips=10`, `$10.40/ep` video cap, **`$135/mo ALL_PROVIDERS`** cap), **`craft_rubric.yaml`** (`<= 150 lines`), executable SQLite DDL (`schema/pipeline.sql` v4 verified `12/12` via `node schema/schema-test.js`, pinned `SQLite >= 3.51.3`), single `MOTIF_REGISTRY_V1`, and 3 signed golden fixtures (`fixtures/golden_manifests/`).
- Enforce **Zero-Spend Offline Guard** across all worktrees (`pytest` socket blocker + scrubbed API keys + SQLite `trg_offline_test_zero_spend_guard`). Tag `integration/m0-frozen`.

### Days 2–4 — Milestone M0.5 Minimal End-to-End Offline Slice (`Tasks 189`, `193`)
- **Zero live paid API spend during M0.5 (`F-01`, `F-17`):** Execute one minimal episode (`1` `AFFIRMED` + `APPROVED` anonymization case, `1` illustrative 2K plate, `1` `PLAN_APPROVED` `ScenePlan`, WhisperX forced word alignment, authoritative 4-Motif MVP [`StickmanStage`, `AudioEvidenceCard`, `RedactedDocReveal`, `FoiaFootageFrame`], **mocked** Omni transport `$0`, `-14.0 LUFS` master, and 5-gate `release_approvals` block/pass test) proving end-to-end wire compatibility BEFORE building motifs #5–#12 or full UI.

### Days 5–13 — Dependency-Ordered Parallel Waves (`W1-A..W5-A` & `W1-B..W4-B`, `F-07`)
- Every worktree merges strictly into its track integration branch (`integration/part1` or `integration/part2`) by wave using `git merge --no-ff` + `node scripts/verify-harmony.mjs --wave <id>` (pinned base commit, Contract Bump PR for shared edits, `git revert -m 1` rollback on failure):
  - **Part 1 Waves:** `W1-A` (`005–014` SQLite/Budget) -> `W2-A` (`015–032` Scout) -> `W3-A` (`033–044` Evidence/Disposition/2K) -> `W4-A` (`045–072` Rights/PII & WhisperX/`<=90s` Cloud ASR) -> `W5-A` (`073–100` `ScenePlan`, Director `13.0m/5.67m/1.33m`, `RenderBackendStub` -> `PART1_CERT_REPORT.md`).
  - **Part 2 Waves:** `W1-B` (`101–115, 117–118, 122, 130–142` 4-Motif MVP & Motion) -> `W2-B` (`116, 119–121, 123–129, 143–152` +8 Vector Motifs & Sole-Owner `crime_scene_2k`) -> `W3-B` (`153–176` Crash-Safe Omni Mock + Agent 6) -> `W4-B` (`177–192` Loopback UI + 5-Gate Sign-Off + Honest Analytics -> `PART2_CERT_REPORT.md`).

### Days 14–16 — Full Merge, Offline Stress Matrix & Post-Integration Bounded Live Check (`Tasks 194–200`)
- Merge `integration/part1` + `integration/part2` -> `integration/v1-rc`, run full offline E2E, Legal/PII/Injection Red-Team Gauntlet (`Task 197`), Crash/Conveyor Soak (`Task 198`), `0%`-Cache `$135/mo` Economics Audit (`Task 199`), and full 1,200s build (`$0.00` spent).
- **Strictly Last (`Task 200`, only if 100% offline suites pass):** Opt in explicitly with `--live-sandbox` + `ALLOW_PAID_SANDBOX=1` (`<= $2.00` hard cap, 1 call, 0 retries) to verify live `gemini-omni-1.2-flash` endpoint & invoice rate before stamping `V1_RELEASE_SCORECARD.md = GO`.

---

## Summary Milestone Matrix (v4)

| Milestone | Scope | Task Range | Owner | Hard Exit Gate |
| :--- | :--- | :--- | :--- | :--- |
| **M0 — Contract Freeze** | Monorepo, `providers.yaml`, `craft_rubric.yaml`, `pipeline.sql` v4, Offline Socket Guard | `001–004` | Joint (A + B) | `schema-test.js` **12/12** pass + `$0 OFFLINE_TEST` |
| **M0.5 — Early Offline Vertical Slice** | 1 Case, 1 Illustrative 2K, 1 `ScenePlan`, WhisperX, 4 MVP Motifs, Mock Omni, 5-Gate Sign-Off | Core Subset + `189`, `193` | Joint (A + B) | Playable 90s `-14 LUFS` MP4 at **`$0.00` spent** |
| **M1-P1 — Waves `W1-A..W3-A`** | DB (`>=3.51.3`, `$135` ledger), Scout (30d full purge), Disposition+Quarantine, Illustrative 2K | `005–044` | Developer A | Offline `W1–W3` wave gates 100% green |
| **M2-P1 — Waves `W4-A..W5-A`** | Rights (`§105` narrowed), WhisperX, `ScenePlan`, Director `<=10` clips, Stub Cert | `045–100` | Developer A | `PART1_CERT_REPORT.md` 100% offline green |
| **M1-P2 — Waves `W1-B..W2-B`** | 4-Motif MVP -> 12 Vector Motifs, Monochrome Keyframes, Sole-Owner `crime_scene_2k` | `101–152` | Developer B | Local perf bench logged, `0` crimson, `<1px` callouts |
| **M2-P2 — Waves `W3-B..W4-B`** | Crash-Safe Omni Mock (`UNKNOWN_RECONCILE`), `-14 LUFS`, Loopback 5-Gate UI, Analytics | `153–192` | Developer B | Playwright E2E + `PART2_CERT_REPORT.md` offline green |
| **M3-INT — Wave Cross-Track Merge** | 12-Motif Live Adapter, `ScenePlan` Stale Invalidation, Closed-Loop Analytics | `194–196` | Joint (A + B) | Offline cross-track handoff 100% green (`$0` spent) |
| **M4-CERT — V1 Release** | Red-Team Injection/Legal Gauntlet, Soak, `0%`-Cache Audit, 1,200s Build + 1 Bounded Check | `197–200` | Joint (A + B) | Offline matrix 100% -> 1 `<= $2` check -> `GO` |
