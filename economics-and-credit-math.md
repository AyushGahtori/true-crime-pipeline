# Token, Credit & Quota Economics Engine (v3 Config-Driven Registry)

All model IDs, token rates, clip limits, and USD caps live in **one single source of truth** (`providers.yaml`), enforced durably at runtime by `pipeline.db`'s `budget_reservations` table and `trg_budget_cap_guard` trigger (`F-02`, `F-18`). Diagram: [economics-and-credit-math.mmd](economics-and-credit-math.mmd).

> **Important Provider Update (`F-01`, verified 2026-11-23):** Google shut down the Gemini Developer API Veo 3.1 Preview endpoints (`veo-3.1-lite-generate-preview`, `veo-3.1-fast-generate-preview`, `veo-3.1-generate-preview`) on **October 22, 2026**. All previous `$0.05/sec` (`$6/episode`) Veo 3.1 Lite figures are retired and replaced below.

## 1. Primary Default: `gemini-omni-1.2-flash` (Gemini Interactions API)

- **Endpoint & Auth:** Official Gemini Developer API via `google-genai >= 2.30.1` (`client.interactions.create`, Files API upload polled until `ACTIVE`, `GEMINI_API_KEY`).
- **Pricing Model (Paid Tier, token-billed):** `gemini-omni-1.2-flash` bills granularly by tokens (~`5,792` video output tokens/sec @ `720p`, yielding an effective **`~$0.07–$0.10/sec`** depending on prompt/reference density; see [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing?hl=en)).
- **Conservative Planning Rate (`providers.yaml`):** We budget conservatively at **`$0.10/sec` @ 720p** (`$0.80` per `8s` clip) and mandate a **live sandbox billing verification in `M0.5`** before locking production rates.
- **Single-Source Clip & Duration Cap (`F-02`):** Eliminates the old 15-vs-16 mismatch completely:
  - `max_hero_clips = 10` (hard ceiling in `providers.yaml`, `manifest_linter.py`, and `episodes.max_hero_clips`)
  - `max_hero_duration_sec = 80` (`1.33 min`, e.g., `10 x 8s` or mixed `3s–10s` buckets; `<= 10s` max for 2-frame transitions)
  - **Base Episode Video Spend:** `80s × $0.10/sec = $8.00/episode`
  - **Dynamic Retake Escrow (`30%`):** `$2.40/episode` (3 full 8s retakes; safety blocks where output tokens = 0 release reservation immediately)
  - **Hard Episode Video Cap (`episodes.video_budget_cap_micro_usd`):** **`$10.40/episode`** (`10_400_000` micro-USD) enforced atomically inside SQLite `trg_budget_cap_guard`.

## 2. Distinct Separate Provider Integrations (Never Interchangeable)

| Backend Route (`provider_route`) | Auth & API Contract | Use Case & Policy Constraints |
|---|---|---|
| **`GEMINI_OMNI_INTERACTIONS`** *(Primary Default)* | `GEMINI_API_KEY` + Interactions API (`gemini-omni-1.2-flash`) | Primary headless 24/7 generation (`$8.00–$10.40/ep`). Note regional restriction: video-input edits/extensions unavailable in EEA/CH/UK/some US states (text-to-video & image-keyframe-to-video unaffected). |
| **`VERTEX_VEO_ENTERPRISE`** *(Separate Opt-In Adapter)* | GCP Project + Vertex AI OAuth / Service Account + Predict Long-Running API | Enterprise-tier alternative with distinct endpoint, GCS URI output contract, quotas, and Vertex billing SKU—implemented only as an isolated adapter if an operator holds GCP Enterprise access. |
| **`HUMAN_BATCH_DESK`** *(Optional Manual Fallback)* | Local React UI (`apps/batch_desk_ui`) + atomic `google_accounts` credit ledger | Optional manual drag-and-drop workflow with explicit multi-account consumer ToS notice and atomic `24h + 5m` refill/lockout SQL (`atomic_refill_and_reserve_daily_account_credits`). |

## 3. Honest 20-Minute (1,200-Second) Episode & Monthly Budget (`10 Episodes/Month`)

| Cost Component | Episode Runtime / Usage | Base / Episode | Worst-Case Cap / Episode | 10-Episode Monthly Total |
|---|---|---|---|---|
| **Layer 1 · Code-to-Video & FOIA** | **13.0 min (780s)** | `$0.00` video | `$0.00` video | `$0.00` |
| **Layer 2 · 2K Illustrative Stills** (`Gemini Image API`) | **5.67 min (340s)** (`~6–7` plates) | `~$0.30` | `~$0.50` | `~$3.00–$5.00` |
| **Layer 3 · Hero Video** (`gemini-omni-1.2-flash` `720p`) | **1.33 min (80s)** (`<= 10` clips) | **`$8.00`** | **`$10.40`** (hard DB cap) | **`$80.00–$104.00`** |
| **DeepSeek V4.1 Flash / V4-Pro** (Scripts, Ledger, Manifests) | Full 20-min episode | `~$1.35` peak (`~$0.75` off-peak) | `~$1.90` peak | `~$7.50–$19.00` |
| **TTS + ASR Alignment + Flash Vision QA** | ~16 min narration + 2x2 QA | `~$0.45` | `~$0.70` | `~$4.50–$7.00` |
| **Total Autonomous Compute** | **20.0 min (1,200s)** | **`~$10.10/ep`** | **`~$13.50/ep`** | **`~$95–$135/mo` (Hard Monthly Cap: `$135/mo`)** |

*(Note: Worst-case 10-episode production with full retry headroom fits cleanly inside the revised **`$135/mo`** autonomous cap. All dollar admission control is enforced transactionally in `pipeline.db` `budget_reservations`, NEVER in async `telemetry.db`.)*
