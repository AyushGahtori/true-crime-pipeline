# Master System Architecture: Automated Hybrid True-Crime Pipeline (v3)

This document defines the end-to-end architecture, honest 20-minute (1,200-second) runtime & cost budget, non-blocking invariants, human legal/editorial approval gates, and post-publish analytics loop for a single-host local desktop workflow producing up to **10 twenty-minute true-crime documentaries per month**.

> **Status Notice:** This repository currently contains the hardened architecture design, executable SQLite DDL (`schema/pipeline.sql` v3), and 200-task implementation plan—not yet deployed runtime code. Performance and pricing figures below reflect verified November 2026 provider contracts or explicitly labeled **Design Targets** to be verified in the Early Thin Vertical Slice (`M0.5`) before full build-out.

## 1. Core Architectural Thesis & Honest 1,200-Second Runtime Split (`F-01`, `F-02`)

Google shut down the Gemini Developer API Veo 3.1 Preview endpoints (`veo-3.1-lite-generate-preview`, etc.) on **October 22, 2026**. The primary supported headless video-generation route is **`gemini-omni-1.2-flash`** via the official **Gemini Interactions API** (`google-genai >= 2.30.1` + Files API upload polled to `ACTIVE`), billed via video output tokens (`~5,792 tokens/sec` @ `720p`, conservatively budgeted at **`$0.10/sec`** until confirmed by a live sandbox invoice check in `M0.5`).

All clip counts, durations, and USD caps originate from **one single source of truth** (`providers.yaml` + `episodes.max_hero_clips = 10`, `max_hero_duration_sec = 80`, `video_budget_cap_micro_usd = 10_400_000` = `$10.40/ep`):

| Layer | Visual Engines | Episode Runtime | Paid Video / Image Allocation | DeepSeek V4 Cost | Primary Role |
|---|---|---|---|---|---|
| **1 · Code-to-Video & FOIA** | `CODE_STICKMAN`, `AUDIO_EVIDENCE_CARD`, `FOIA_REAL_FOOTAGE` | **13.0 min (780s)** | **$0** video API | ~$0.95–$1.35 peak (~$0.50–$0.70 off-peak) | Explainers, stickman dialogue (`6 fps` JS vertex-jitter), timelines, SMS, maps, redacted docs, case boards, rights-cleared FOIA |
| **2 · 2K Illustrative Stills** | `STILL_2K_PANZOOM` (`crime_scene_2k`) | **5.67 min (340s)** (~6–7 dense plates) | Official Gemini Image API (`~$0.20–$0.40/ep`) | ~$0.15–$0.30 | **Clearly labeled Illustrative Reconstructions** with external-margin `10x10` `span_cells` Lanczos zoom & projected screen-space callouts |
| **3 · AI Hero Motion** | `FLOW_HERO_VIDEO` (`gemini-omni-1.2-flash` Interactions API, `720p`, `3s–15s` T2V/1-frame or `3s–10s` 2-frame) | **1.33 min (80s)** (**`MAX_HERO_CLIPS = 10`**, e.g. `10 x 8s`) | **Primary Default:** `$8.00/ep` base + `$2.40` dynamic USD escrow (`$10.40` hard cap) | ~$0.25 | Cold-open dramatic hooks, atmospheric silhouettes, fluid camera moves (**labeled illustrative**) |
| **Total Episode** | **All 5 Engines** | **20.0 min (1,200s)** | **$8.00–$10.40 video** (`$80–$104/mo` @ 10 eps) | **~$1.35–$1.90 peak (`~$0.75–$1.05` off-peak)** | Full 1080p30 MP4 + mandatory human release sign-off + Studio analytics loop |

*(Note: Total monthly autonomous compute cap is budgeted honestly at **`$135/mo`** at 10 episodes/month to cover worst-case Omni 1.2 Flash retries + DeepSeek V4 + Image 2K + TTS/ASR. Vertex AI / Enterprise Veo [`VERTEX_VEO_ENTERPRISE`] and manual [`HUMAN_BATCH_DESK`] are treated as completely separate provider integrations with separate contracts, never interchangeable names.)*

## 2. Core Design Guarantees (v3 Audit-Hardened)

1. **Truthful State & Mandatory Human Release Sign-Off (`F-03`, `F-04`, `F-06`):**
   - `cases.anonymization_status` defaults to `'NOT_STARTED'` (never default-approved) and `spatial_anchors.lock_status` defaults to `'DRAFT'` (never default-locked); transitioning to `APPROVED` / `LOCKED` requires reviewer ID, timestamp, and artifact SHA-256.
   - `trg_case_disposition_guard_insert` AND `trg_case_disposition_guard_update` protect `cases` on both writes; flipping an `AFFIRMED` case to `REVERSED`/`VACATED`/`ACQUITTED`/`PENDING` automatically **quarantines** downstream episodes (`QUARANTINED_LEGAL_HOLD`) and **revokes** existing release approvals!
   - `trg_episode_release_gate` hard-blocks entering `READY_TO_UPLOAD` or `PUBLISHED` unless **all 5 mandatory human gates** (`FACTUAL_ACCURACY`, `PRIVACY_PII`, `SOURCE_RIGHTS`, `SYNTHETIC_DISCLOSURE`, `ILLUSTRATIVE_LABELING`) are explicitly `APPROVED` for the exact `ready_bundle_sha256`.
2. **Illustrative Reconstruction Labeling (`F-05`):**
   - Generated 2K stills (`still_assets.is_illustrative_reconstruction = 1`) and synthetic Hero clips are **never** presented as verified forensic crime-scene photographs; `crime_scene_2k` and Remotion render a persistent subtle **`ILLUSTRATIVE RECONSTRUCTION — NOT CRIME SCENE PHOTO`** label while factual claims remain anchored solely to cited `fact_ledger` primary records.
3. **Crash-Safe Idempotency & Durable USD Budget Admission (`F-10`, `F-18`):**
   - Every paid video job carries `UNIQUE (episode_id, scene_id)`, a stable `idempotency_key`, persisted `provider_operation_id` inside `pipeline.db` (not async `telemetry.db`), and explicit crash states (`SUBMITTING`, `RUNNING`, `UNKNOWN_RECONCILE`, `PENDING_MANUAL_SPOT_CHECK`).
   - Paid dispatch MUST reserve micro-USD atomically inside `budget_reservations` (`trg_budget_cap_guard`) BEFORE calling the provider; `telemetry.db` is strictly read-only analytics, never admission control.
4. **Segmented `VoiceTrackManifest` & Non-Overlap Timeline Invariants (`F-09`):**
   - `voice_segments` (`NARRATION`, `FOIA_AUDIO_SLOT`, `TWIST_PAD`) and `scenes` enforce kind-specific media non-null checks and `BEFORE INSERT/UPDATE` non-overlap triggers, plus transactional continuity validation (`timeline_validated_sha256`).
5. **Local Security Boundary & Pinned SQLite Runtime (`F-19`, `F-22`):**
   - Python is the sole writer to `pipeline.db` (`WAL`, `busy_timeout = 5000`, local host filesystem only—reject SMB/NFS/UNC paths, enforce **`SQLite >= 3.51.3`** at startup).
   - FastAPI control plane binds strictly to `127.0.0.1` with per-session `X-Local-Auth-Token` (`0600`), strict localhost CORS, path-traversal upload containment, and immutable `audit_log`.
6. **Honest YouTube Data & Analytics Integration (`F-11`, `F-12`, `F-20`):**
   - No unsupported `captions.download` scraping on third-party videos; no fabricated `videos.list` monetization fields (`episode_analytics.adsense_status` defaults to `'UNKNOWN'` and reads monetization/CTR strictly from creator-authorized Studio CSV export or manual entry alongside `youtubeAnalytics.reports.query` watch-time/retention metrics).
   - Every YouTube-sourced `outlier_candidates` row requires a non-null 30-day `yt_ttl_expires_at` purging ALL YouTube API-derived fields (`raw_yt_payload_json`, `views_count`, `outlier_ratio`, YT seed excerpts) on expiry.
