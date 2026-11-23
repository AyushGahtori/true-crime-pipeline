# Research Evidence Notes (Audited & Cited — 2026-11-23)

Each note explicitly separates **Verified External Facts** (with direct source URLs and review dates) from **Design Targets / Hypotheses** (performance, latency, and accuracy targets that remain hypotheses until reproducible local benchmarks run on the target machine with recorded hardware, OS, model ID, dataset, and script outputs — see `F-21`).

| Topic | Architecture Spec | Research Note |
|---|---|---|
| DeepSeek V4.1 Flash / V4-Pro code animation & spatial grounding hypothesis | [code-animation-catalog.md](../code-animation-catalog.md) · [economics-and-credit-math.md](../economics-and-credit-math.md) | [deepseek-v4-code-animation.md](deepseek-v4-code-animation.md) |
| Gemini Omni 1.2 Flash Interactions API pricing vs retired Veo 3.1 Lite & optional Batch Desk | [economics-and-credit-math.md](../economics-and-credit-math.md) · [flow-hybrid-and-batch-desk.md](../flow-hybrid-and-batch-desk.md) | [google-flow-veo-omni-economics.md](google-flow-veo-omni-economics.md) |
| YouTube July 2025 YPP clarification, 17 U.S.C. § 105 scope, rights & PII risk controls | [legal-copyright-and-adsense.md](../legal-copyright-and-adsense.md) | [youtube-2026-policy-and-adsense.md](youtube-2026-policy-and-adsense.md) |
| Authorized YouTube Data/Analytics APIs, 30-day retention, CourtListener caps & SI | [scout-and-saturation.md](../scout-and-saturation.md) · [evidence-and-fact-ledger.md](../evidence-and-fact-ledger.md) | [youtube-and-foia-mining.md](youtube-and-foia-mining.md) |
| Segmented Voice-First timeline, ASR alignment & proper-noun diffing | [voice-first-and-asr-sync.md](../voice-first-and-asr-sync.md) | [voice-first-tts-asr-sync.md](voice-first-tts-asr-sync.md) |
| Remotion JS vertex-jitter boil hypothesis, CSS Safe-Zones & 2K illustrative grid engine | [code-animation-catalog.md](../code-animation-catalog.md) · [crime-scene-2k-grid-engine.md](../crime-scene-2k-grid-engine.md) | [remotion-json-catalog-and-2k-grid.md](remotion-json-catalog-and-2k-grid.md) |
| Per-track `-14 LUFS` audio mastering, honest ASR disagreement & SQLite `>= 3.51.3` ops | [mastering-loudness-and-qa.md](../mastering-loudness-and-qa.md) · [database-and-state-design.md](../database-and-state-design.md) | [audio-mastering-and-conveyor-ops.md](audio-mastering-and-conveyor-ops.md) |

## Reproducible Benchmark Protocol (`F-21`)
Every local benchmark artifact emitted during implementation (`artifacts/benchmarks/*.json`) MUST record:
- `measured_at_utc`, `git_commit_sha`, `os_version`, `cpu_model`, `ram_gb`, `node_version`, `python_version`, `sqlite_version`, `ffmpeg_version`
- `model_id` (if external API), `input_fixture_sha256`, `command_line`, `sample_size`, `p50_ms`, `p95_ms`, `raw_measurements[]`.
