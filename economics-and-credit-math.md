# Token, Credit & Global Across-Providers Budget Engine (v4 · `F-01`, `F-02`, Additional Check #1 & #3)

All model IDs, token rates, clip caps, and monthly ceilings load from `providers.yaml` and are enforced **transactionally across ALL providers** by `pipeline.db` (`monthly_budget_ledger` + `provider_spend_reservations` + `trg_provider_global_budget_cap_guard`). Diagram: [economics-and-credit-math.mmd](economics-and-credit-math.mmd).

## 1. Zero-Spend Test Cap & Global Across-All-Providers `$135/mo` Hard Limit (`F-01`, `F-02`)

1. **`OFFLINE_TEST` `$0.00` Trigger Guard (`F-01`):** Every test reservation carries `purpose = 'OFFLINE_TEST'`. SQLite trigger `trg_offline_test_zero_spend_guard` unconditionally aborts any `estimated_micro_usd > 0`, guaranteeing zero test credit burn alongside socket-blocking test harnesses.
2. **Global Multi-Provider Ceiling (`F-02`):** `trg_provider_global_budget_cap_guard` sums `RESERVED + UNKNOWN_HOLD + COMMITTED` rows across **ALL providers** (`gemini_omni`, `gemini_image`, `deepseek_chat`, `tts`, `vision_qa`, `vertex_veo`) for the current `year_month` and blocks ANY call that would breach:
   - Per-episode paid video cap: **`$10.40/ep`** (`10_400_000` micro-USD; `max_hero_clips = 10`, `max_hero_duration_sec = 80s`)
   - Per-provider monthly ledger cap (e.g. `deepseek_chat` `$38.00/mo`, `gemini_omni` `$104.00/mo`)
   - **Global `ALL_PROVIDERS` cap: `$135.00/mo` (`135_000_000` micro-USD)**!
   - Non-authoritative `telemetry.db` (`total_input_tokens` + `CHECK (cached_input_tokens <= total_input_tokens)`) NEVER gates spend!

## 2. Best-Effort DeepSeek Caching: Dual Conservative vs. Cached Projections (`Additional Check #1`)

Because DeepSeek documents [Context Caching](https://api-docs.deepseek.com/guides/kv_cache/) as **best-effort** rather than a contractual guarantee (and exact cache hit rates vary across restarts and batch intervals), budget projections model **both** scenarios—and the `$135/mo` global ledger stays solvent even at **0% cache hits**:

| Cost Component (`10 Episodes/Month`) | Conservative `0%` Cache Projection / Ep | Best-Effort Cached Projection / Ep | Monthly DB Ledger Cap (`monthly_budget_ledger`) |
|---|---|---|---|
| **Layer 1 · Code-to-Video & FOIA (`13.0m`)** | `$0` video | `$0` video | `$0.00/mo` |
| **Layer 2 · Illustrative 2K Plates (`Gemini Image API`, `5.67m`)** | `$0.40` | `$0.30` | `$5.00/mo` (`gemini_image`) |
| **Layer 3 · `gemini-omni-1.2-flash` `720p` (`1.33m`, `<= 10` clips)** | `$8.00` base / **`$10.40` cap** | `$8.00` base / `$10.40` cap | `$104.00/mo` (`gemini_omni`) |
| **DeepSeek V4.1 Flash / V4-Pro** (Scripts, Ledger, Manifests) | **`$2.80–$3.80`** *(0% cache worst case!)* | `~$0.75–$1.90` | **`$38.00/mo`** (`deepseek_chat`) |
| **TTS + Local WhisperX (`$0` ASR!) + Vision QA** | `$0.50` *(WhisperX offline = `$0`!)* | `$0.45` | `$5.00/mo` (`tts`) + `$2.00/mo` (`vision_qa`) |
| **Total Across ALL Providers (10 Episodes)** | **~$117–$135/mo *(Fits `ALL_PROVIDERS` `$135` Cap!)*** | **~$95–$120/mo** | **`$135.00/mo` HARD GLOBAL CAP** |

*(Note: Using local WhisperX for all word-level timing keeps production ASR cost near `$0.00/ep`. Final live connectivity/invoice verification runs strictly post-integration under an explicit `$2.00` bounded sandbox flag.)*
