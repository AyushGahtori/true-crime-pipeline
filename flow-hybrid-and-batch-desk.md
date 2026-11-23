# Agent 5C & Operations: Gemini Omni Interactions Primary Backend, Crash Safety & Local Cockpit (v3)

This specification defines external video generation, crash-safe job reconciliation (`F-10`), durable USD budget reservations (`F-18`), T2V/F2V prompt modes (`F-07`), FastAPI local access security (`F-19`), and the optional manual Batch Desk workflow (`F-08`). Diagram: [flow-hybrid-and-batch-desk.mmd](flow-hybrid-and-batch-desk.mmd).

## 1. Primary Default: `GeminiOmniInteractionsBackend` (`gemini-omni-1.2-flash`) (`F-01`, `F-07`)

Because Google retired Veo 3.1 Preview endpoints on the Gemini Developer API on **October 22, 2026**, the primary production backend integrates directly with **`gemini-omni-1.2-flash`** via the **Interactions API** (`google-genai >= 2.30.1`):
- **Supported Modes (`flow_jobs.prompt_mode`):**
  1. `TEXT_TO_VIDEO`: `start_frame_png = NULL`, `end_frame_png = NULL`, duration `3s–15s` (no fake start PNGs required!).
  2. `FIRST_FRAME`: `start_frame_png` uploaded via Files API and polled until `ACTIVE`, `end_frame_png = NULL`, duration `3s–15s`.
  3. `FIRST_AND_LAST_FRAME`: both `start_frame_png` and `end_frame_png` uploaded via Files API, duration strictly **`3s–10s`** (enforced by SQLite `CHECK` constraint!).
- **Resolution & Timeout:** Default `720p` (`1280x720`, `16:9`), configurable HTTP timeout (`600s` default; extendable to `900s` for heavy jobs).
- **Regional Restriction Guard:** Video-to-video upload edits/extensions are restricted in EEA, Switzerland, UK, and some US states; V1 uses `TEXT_TO_VIDEO`, `FIRST_FRAME`, and `FIRST_AND_LAST_FRAME` (image/text inputs only) for universal regional portability, explicitly flagging video-reference workflows as region-gated.
- **Separate Enterprise Adapter (`VERTEX_VEO_ENTERPRISE`):** Vertex AI / Enterprise Veo requires separate GCP OAuth/IAM credentials, GCS output URIs, and Vertex SKUs and is strictly isolated behind a distinct adapter class—never aliased onto the Developer API client.

## 2. Crash-Safe Idempotency & Durable USD Budget Ledger (`F-10`, `F-18`)

No paid external API call may ever execute without first committing durable state in `pipeline.db`:
1. **Pre-Dispatch Transaction (`BEGIN IMMEDIATE`):**
   - Create/verify `flow_jobs` row with `UNIQUE (episode_id, scene_id)` and deterministic `idempotency_key = sha256(episode_id + scene_id + prompt_hash + attempt)`.
   - Insert `budget_reservations` row (`status = 'RESERVED'`, `estimated_micro_usd`); SQLite `trg_budget_cap_guard` atomically rejects the dispatch if `SUM(RESERVED + COMMITTED + UNKNOWN_HOLD) > episodes.video_budget_cap_micro_usd`.
   - Transition `flow_jobs.state = 'SUBMITTING'`.
2. **Dispatch & Operation Persistence:**
   - Call `client.interactions.create(...)`, immediately persist returned `provider_operation_id` into `flow_jobs.provider_operation_id` and transition to `RUNNING`.
3. **Crash / Timeout Reconciliation (`UNKNOWN_RECONCILE`):**
   - If the process crashes or HTTP times out mid-flight, startup recovery queries `reconcile_unknown_flow_jobs`, sets `UNKNOWN_RECONCILE` + `budget_reservations.status = 'UNKNOWN_HOLD'`, and polls the provider operation ID to settle as `COMMITTED` (download output) or `RELEASED` (confirmed failed/unbilled) BEFORE any retry is permitted. Zero duplicate paid scene jobs can occur on crash recovery!
4. **Vision QA Fail-Closed Policy:**
   - If Gemini Flash Vision QA is temporarily unreachable after retries, `flow_jobs.state` enters **`PENDING_MANUAL_SPOT_CHECK`** (NOT `ACCEPTED`!). SQLite trigger `trg_episode_release_gate` **hard-blocks** `READY_TO_UPLOAD` until a human clears the spot check—zero fail-open paths.

## 3. Local FastAPI Control Plane Security Boundary (`F-19`)

The FastAPI server (`apps/batch_desk_ui/api`, sole SQLite writer bridge) enforces a strict single-user local security perimeter:
- **Loopback Binding Only:** Defaults strictly to `127.0.0.1` (refuses `0.0.0.0` startup unless explicit authenticated TLS mode is configured).
- **Per-Session Auth & CSRF Protection:** Generates a random 256-bit bearer token on startup written `0600` to local runtime state; all mutating HTTP/WS calls require `X-Local-Auth-Token`, paired with strict `CORS` allowlist (`http://127.0.0.1:<ui_port>` only).
- **Upload Containment & Audit Logging:** Validates magic bytes, max upload size (`<= 250 MB`), and canonical path containment (`Path.resolve().is_relative_to(upload_root)`); logs every config/state/approval mutation to `pipeline.db` `audit_log`.

## 4. Optional `HumanBatchDeskBackend` (Atomic `24h + 5m` Reset & Sunk-Cost Guard) (`F-08`)

Retained strictly as an optional zero-API-billing fallback (with explicit multi-account consumer ToS notice):
- **Atomic Refill & Lockout SQL (`atomic_refill_and_reserve_daily_account_credits`):** Handles both `24h + 5m` window refill (`daily_credits_left = 50` when `now_ms >= next_daily_reset_utc_ms`) AND hard lockout when `daily_credits_left < credits` and `now_ms < next_daily_reset_utc_ms`, with matching `refund_daily_account_credits`.
- **Up to 3 Episodes FIFO + Per-Shift Saturation Re-Check:** Drains oldest-first (`ORDER BY e.created_at ASC`), aborting on `N_14d_wave > 3` unless `> 50%` sunk and `N_14d_wave <= 5`.
- **2-Strike Circuit Breaker:** Strike 1 -> `STRIKE_1_RETRY_SAFE` (`prompt_v2_safe`); Strike 2 -> `SWITCHED_TO_FALLBACK` routing strictly to a non-neighbor visual engine (`RULE_05` safe).
