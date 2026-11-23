# Research: Gemini Omni 1.2 Flash Interactions API vs Retired Veo 3.1 Preview (`F-01`, `F-02`)

*Last verified: 2026-11-23*

## 1. Verified External Provider Facts
- **Veo 3.1 Preview Shutdown (October 22, 2026):** Google shut down the Gemini Developer API Veo 3.1 Preview endpoints (`veo-3.1-generate-preview`, `veo-3.1-fast-generate-preview`, `veo-3.1-lite-generate-preview`) on October 22, 2026. Source: [Google AI Developers Forum](https://discuss.ai.google.dev/t/request-veo-3-api-access-for-project-reviewfilm/200412).
- **Current Supported Gemini Developer API Video Model (`gemini-omni-1.2-flash`):** Served through the official **Interactions API** (`google-genai >= 2.30.1`, `client.interactions.create`) + Files API media uploads polled until `ACTIVE`.
  - Supported modes: Text-to-Video (`3s–15s`), First-Frame-to-Video (`3s–15s`), First-and-Last-Frame Transition (`3s–10s` max), Image-referenced R2V (up to 6 images), resolutions `360p` / `720p` (default) / `1080p` / `4k`, configurable timeout (`600s` default).
  - **Regional Restriction:** Uploading videos for video edits, extensions, or video references is unavailable in the EEA, Switzerland, UK, and some US states. V1 uses text-to-video and image-keyframe-to-video only.
  - Reference: [Gemini Omni Flash Docs](https://aistudio.google.com/docs/omni.md) · [Interactions API](https://aistudio.google.com/docs/interactions-overview.md) · [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing?hl=en).
- **Pricing Structure:** Token-billed video output (~`5,792` video output tokens/sec @ `720p`, yielding an effective **`~$0.07–$0.10/sec`** depending on version/density).

## 2. Planning Assumptions (To Be Confirmed via M0.5 Live Sandbox Invoice)
- **Conservative Planning Rate:** `$0.10/sec` @ `720p` (`$0.80` per `8s` clip).
- **Single-Source Budget Envelope:** `MAX_HERO_CLIPS = 10`, `max_hero_duration_sec = 80s` (`1.33 min`), Base `$8.00/ep`, Hard SQLite DB Cap `$10.40/ep` (`$80–$104/mo` video + DeepSeek/TTS/Image = **`<= $135/mo`** @ 10 eps).
- **Separate Adapters:** `VERTEX_VEO_ENTERPRISE` (GCP Vertex AI IAM/GCS contract) and `HUMAN_BATCH_DESK` (optional manual UI with explicit multi-account ToS notice and atomic `24h + 5m` refill/lockout SQL) are completely distinct provider routes—never interchangeable aliases.
