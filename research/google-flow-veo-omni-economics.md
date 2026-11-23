# Research: Gemini Omni 1.2 Flash Pricing, Test Zero-Spend Guard & Single-Config Limits (v4 · `F-01`, `F-02`)

*Last verified: 2026-11-23*

## 1. Supported Primary Route (`gemini-omni-1.2-flash` Interactions API)
- Veo 3.1 Preview endpoints on Gemini Developer API shut down Oct 22, 2026 ([Google AI Developers Forum](https://discuss.ai.google.dev/t/request-veo-3-api-access-for-project-reviewfilm/200412)).
- `gemini-omni-1.2-flash` via Interactions API (`google-genai >= 2.30.1` + Files API) bills by tokens (~`5,792` video output tokens/sec @ `720p`, effective `~$0.07–$0.10/sec`; [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing?hl=en)).
- Supported durations: `3s–15s` (`TEXT_TO_VIDEO`, `FIRST_FRAME`), `3s–10s` (`FIRST_AND_LAST_FRAME`); video-upload inputs unavailable in EEA/CH/UK/some US states.

## 2. Single-Config Caps & Offline-First Zero-Spend Enforcement (`F-01`, `F-02`)
- **Single-Source Video Limits (`providers.yaml` + `schema/pipeline.sql` v4):** **`max_hero_clips = 10`**, **`max_hero_duration_sec = 80s`** (`1.33 min`), **`$8.00`** base / **`$10.40`** hard SQLite episode cap, rolled up with ALL other providers under `monthly_budget_ledger` **`ALL_PROVIDERS <= $135.00/mo`**.
- **Zero-Spend Tests:** Standard tests execute strictly behind transport mocks + socket-blocking guards + `trg_offline_test_zero_spend_guard`; only 1 deferred bounded connectivity check (`<= $2.00`) runs post-integration (`Task 200`, opt-in).
