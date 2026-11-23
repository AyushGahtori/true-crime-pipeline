# Parallel Two-Developer Architecture: Part 1, Part 2 & M0.5 Offline Slice (v4)

This project is engineered so **Developer A (Part 1)** and **Developer B (Part 2)** build and test **100% independently in parallel** against frozen `contracts/schemas/`, `providers.yaml`, `craft_rubric.yaml`, and `schema/pipeline.sql` v4 using **strictly offline zero-spend transport mocks (`F-01`)**, merging cleanly in dependency-ordered waves (`F-07`). Diagram: [parallel-part1-part2-architecture.mmd](parallel-part1-part2-architecture.mmd).

## 1. Zero-Spend Offline Testing vs. Deferred Post-Integration Live Check (`F-01`)

- **All Ordinary & CI Tests (`Tasks 001–199`) Run 100% Offline ($0.00):** Provider SDKs/HTTP transports are replaced at the boundary by deterministic fakes; outbound sockets (`!= 127.0.0.1`) fail tests immediately, API keys are absent from CI/worktree shells, and `trg_offline_test_zero_spend_guard` aborts on any `OFFLINE_TEST` reservation `> $0`.
- **Single Bounded Post-Integration Live Check (`Task 200` Only):** Real network connectivity + invoice rate verification against `gemini-omni-1.2-flash` Interactions API happens **strictly after full Part 1 + Part 2 offline integration passes**, under an explicit `--live-sandbox` + `ALLOW_PAID_SANDBOX=1` opt-in capped at `<= $2.00` (max `1–2` calls, `0` unbounded retries).

## 2. Authoritative Stage Sequence (`Plan First -> Voice -> Create -> Edit`) (`F-05`)

1. **Plan First (`SCENE_PLAN_APPROVED`):** Part 1 generates and locks `scene_plans` (story purpose, intended effect, approved narration text + SHA-256, `fact_ledger` citations, visual prompt, expected result, SFX/edit instructions, acceptance criteria) alongside clearly labeled illustrative 2K plates (`still_assets.is_illustrative_reconstruction = 1`).
2. **Voice & Animatic Second (`VOICE_READY` -> `ANIMATIC_APPROVED`):** Part 1 synthesizes segmented narration, aligns exact word timings locally via **WhisperX** (`F-03`), compiles `ProductionManifest` (`MOTIF_REGISTRY_V1`), and renders a 480p preflight animatic for human pacing approval BEFORE paid visual generation!
3. **Create Third (`CODE_RENDERED` -> `POST_FLOW_PROCESSING`):** Part 2 renders `@tc/render_catalog`, `crime_scene_2k`, and `gemini-omni-1.2-flash` clips (`budget_reservations` + `UNKNOWN_RECONCILE`) strictly tied to locked `narration_version_sha256`. Any script edit invalidates affected `scene_plans` (`STALE_NEEDS_REAPPROVAL`).
4. **Edit & Sign Off Last (`MASTERED` -> `PENDING_HUMAN_SIGNOFF` -> `READY_TO_UPLOAD`):** Agent 6 masters `-14.0 LUFS` linear audio + single non-FOIA grain and pauses for mandatory 5-gate human release approval (`trg_episode_release_gate`).

## 3. Single SQLite Writer & Disjoint Ownership
- **Python Sole Writer (`SQLite >= 3.51.3`, Local Disk Only):** Python owns all writes to `pipeline.db`. `apps/batch_desk_ui` communicates solely via loopback `127.0.0.1` FastAPI + `X-Local-Auth-Token`.
- **Wave Merge Runbook:** Both developers merge completed waves sequentially onto `integration/part1` and `integration/part2` per [CONTRIBUTING_AGENTS.md](CONTRIBUTING_AGENTS.md) before cross-track integration.
