# Parallel Two-Developer Architecture: Part 1 & Part 2 Seam (v3)

This project is engineered so **Developer A (Part 1)** and **Developer B (Part 2)** build and test **100% independently in parallel** against frozen `contracts/schemas/`, `providers.yaml`, and `schema/pipeline.sql` v3, validated first by a **genuine Milestone M0.5 Minimal End-to-End Thin Vertical Slice** (`F-17`) before full 12-motif / 3-conveyor expansion. Diagram: [parallel-part1-part2-architecture.mmd](parallel-part1-part2-architecture.mmd).

## 1. Resolving the Law 4 Seam Deadlock & Illustrative Labeling Boundary (`F-04`, `F-05`, `F-16`)

1. **Part 1 (`packages/agent2_evidence`):** Calls the official Gemini Image API during Agent 2 to generate clean 2K **Illustrative Reconstruction** plates (`still_assets.is_illustrative_reconstruction = 1`), stamps the temporary external-margin `10x10` grid (`A–J`, `1–10`), runs `grid-grounding-vision@2`, and transitions `spatial_anchors` explicitly through `DRAFT -> IN_REVIEW -> LOCKED` (with `locked_by`, `locked_at`, `still_asset_sha256`, and `cited_fact_id`) BEFORE Agent 3/4 scripting.
2. **Part 2 (`packages/crime_scene_2k` — Sole Owner of `STILL_2K_PANZOOM`):** Consumes the clean 2K PNG + locked `spatial_anchors` to compute `1.6x–3.8x` span zoom, clamp edge crops inside `[0, W] x [0, H]`, render Lanczos cubic pan/zoom + screen-space projected crimson callouts, and burn the mandatory **`ILLUSTRATIVE RECONSTRUCTION — NOT CRIME SCENE PHOTO`** badge cleanly. (`@tc/render_catalog` does NOT duplicate 2K pan/zoom!)

## 2. Single-Host SQLite Writer, Local Security & Disjoint Ownership (`F-19`, `F-22`)

- **Python Sole Writer (`SQLite >= 3.51.3`, Local Disk Only):** Python owns all writes to `pipeline.db` (`WAL`, `BEGIN IMMEDIATE`). `apps/batch_desk_ui` (React) communicates strictly via loopback-only FastAPI (`127.0.0.1` + `X-Local-Auth-Token` + localhost CORS + `audit_log`).
- **Disjoint Write Subtrees:**
  - **Part 1 (Developer A):** `packages/db`, `packages/agent1_scout`, `packages/agent2_evidence`, `packages/agent3_gatekeeper`, `packages/voice_sync`, `packages/agent4_director`, `packages/orchestrator`.
  - **Part 2 (Developer B):** `packages/render_catalog` (authoritative 4-motif MVP -> 12-motif 2D Remotion catalog), `packages/python_motion`, `packages/crime_scene_2k`, `packages/flow_adapter` (`GeminiOmniInteractionsBackend` + crash-safe `budget_reservations` / `UNKNOWN_RECONCILE`), `packages/agent6_mastering`, `packages/analytics_feedback`, `apps/batch_desk_ui`.

## 3. Standalone Testing + Bounded Live Provider Sandbox Check

- **Offline Unit & Harness Tests (Both Developers):** Deterministic offline tests against `RenderBackendStub` (Part 1) and `fixtures/ep_golden_01..03.json` (Part 2) validate internal logic rapidly at `$0` cost.
- **Bounded Live Provider Contract Check (`M0.5` & CI-Manual):** Because offline mocks only test our own assumptions (not real live provider APIs), an explicit low-budget live sandbox check (`<= $2.00` cap) verifies the real `gemini-omni-1.2-flash` Interactions API request/response schema, resolution, billing rate, and quota behavior separately from deterministic offline CI!
