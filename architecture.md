# Master System Architecture: Automated Hybrid True-Crime Pipeline (v4)

This document defines the canonical v4 architecture, offline-first test barrier, cross-provider global USD budget ledger, versioned **Plan -> Voice -> Create -> Edit** `ScenePlan` workflow, legal/rights/human release gates, and analytics loop for a single-host desktop pipeline targeting up to **10 twenty-minute (1,200-second) documentaries per month**.

> **Scope Notice (`F-08`):** This folder contains the verified blueprint and executable SQLite v4 schema (`schema/pipeline.sql`)—not yet deployed application source packages. Production behavior is validated only once runtime code, mocked test matrices, and the final bounded connectivity check pass.

## 1. Honest 1,200-Second Runtime Split & Global Multi-Provider Economics (`F-01`, `F-02`)

Primary supported video provider: **`gemini-omni-1.2-flash`** via the **Gemini Interactions API** (`google-genai >= 2.30.1` + Files API, `TEXT_TO_VIDEO` / `FIRST_FRAME` `3s–15s`, `FIRST_AND_LAST_FRAME` **`3s–10s`**). All clip counts, durations, and USD limits derive from **one canonical configuration** (`providers.yaml` + `schema/pipeline.sql` v4):

| Layer | Visual Engines | Episode Runtime | Paid Budget Allocation | Role |
|---|---|---|---|---|
| **1 · Code-to-Video & FOIA** | `CODE_STICKMAN`, `AUDIO_EVIDENCE_CARD`, `FOIA_REAL_FOOTAGE` | **13.0 min (780s)** | **$0** video API | Explainers, stickman dialogue (`6 fps` JS vertex-jitter), timelines, SMS, maps, redacted docs, case boards, rights-cleared FOIA |
| **2 · 2K Illustrative Stills** | `STILL_2K_PANZOOM` (`crime_scene_2k` sole owner) | **5.67 min (340s)** (~6–7 plates) | `~$0.30–$0.50/ep` Image API | **Clearly labeled `ILLUSTRATIVE RECONSTRUCTION — NOT CRIME SCENE PHOTO`** with margin `10x10` `span_cells` zoom & screen-space projected callouts |
| **3 · AI Hero Motion** | `FLOW_HERO_VIDEO` (`gemini-omni-1.2-flash`, `720p`) | **1.33 min (80s)** (`MAX_HERO_CLIPS = 10`) | **$8.00/ep** base / **`$10.40/ep` DB cap** | Cold-open hooks, atmospheric silhouettes, fluid camera motion (`TEXT_TO_VIDEO` / `FIRST_FRAME` / `FIRST_AND_LAST_FRAME <= 10s`) |
| **Total Episode** | **All 5 Engines** | **20.0 min (1,200s)** | **All Providers <= `$135/mo`** *(even @ 0% cache hits)* | Plan First -> Voice Lock -> Asset Create -> Final Edit -> 5-Gate Human Release Approval |

## 2. Canonical v4 Architectural Guarantees (`F-01`–`F-08` & Earlier `F-01`–`F-22`)

1. **Offline-by-Default Zero-Spend Testing (`F-01`):** All unit/integration tests run behind HTTP/SDK transport mocks, socket blockers, and scrubbed env credentials. `trg_offline_test_zero_spend_guard` rejects any `OFFLINE_TEST` reservation `> $0`. Only a single bounded live check (`<= $2.00`) is permitted **post-integration** (`Task 200`, opt-in `--live-sandbox` + `ALLOW_PAID_SANDBOX=1`).
2. **Global Multi-Provider Transactional Budget Ledger (`F-02`):** `provider_spend_reservations` + `monthly_budget_ledger` enforce per-episode video limits (`$10.40`), per-provider monthly caps (`deepseek_chat` budgeted at `$38/mo` conservative **0%-cache** projection because DeepSeek KV caching is best-effort), AND the global **`$135/mo` `ALL_PROVIDERS` ceiling** inside `pipeline.db`! (`telemetry.db` is strictly non-authoritative analytics.)
3. **Versioned `ScenePlan` & Mandatory Four-Stage Creative Workflow (`F-05`, `F-06`):**
   - **Stage 1 · Plan First (`SCENE_PLAN_APPROVED`):** Create & review `scene_plans` rows guided by concise **`craft_rubric.yaml`** (`<= 150 lines`, clarifying "interactive" = engaging visual documentary pacing—NOT brittle 4,000-line prompts!). Ties `story_purpose`, `intended_audience_effect`, `approved_narration_text`, cited `fact_ledger` IDs, visual prompt, expected result, sound cues, edits, and acceptance criteria.
   - **Stage 2 · Voice & Timing Lock (`VOICE_READY` -> `ANIMATIC_APPROVED`):** Synthesize `voice_segments`, obtain exact word timestamps via **local WhisperX forced alignment** (`F-03` — not size/timestamp-incompatible DeepSeek ASR), review 480p animatic + storyboards before spending video API money.
   - **Stage 3 · Creation Second (`CODE_RENDERED` -> `POST_FLOW_PROCESSING`):** Render `@tc/render_catalog`, `crime_scene_2k`, and crash-safe `gemini-omni-1.2-flash` clips (`budget_reservations`, `UNKNOWN_RECONCILE`, fail-closed QA) strictly against locked `narration_version_sha256`. Any narration revision triggers `trg_scene_plan_invalidate_on_narration_edit` (`STALE_NEEDS_REAPPROVAL`).
   - **Stage 4 · Editing Last (`MASTERED` -> `PENDING_HUMAN_SIGNOFF` -> `READY_TO_UPLOAD`):** Assemble per-track `-14.0 LUFS` linear audio + single non-FOIA grain + surgical heals, then enforce `trg_episode_release_gate` (all `scene_plans` = `EDITED_APPROVED` + all 5 human `release_approvals`).
4. **Defense Against Prompt Injection (`Additional Check #2`):** Untrusted external documents/transcripts/comments wrapped in sanitized `<data>` blocks are extracted strictly by **tool-less** schema-constrained extractors (`extra="forbid"`) with zero execution/DB-write authority, verified via adversarial injection tests.
