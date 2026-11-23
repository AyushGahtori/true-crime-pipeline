# Prompt Contracts: Every Model Role In The Pipeline (v3)

All LLM, Vision, Image, Video, TTS, and ASR model identifiers load from `providers.yaml` rather than hardcoded strings. Prompt prefixes follow a **3-tier byte-0 caching hierarchy** so static schemas cache across *all episodes*, `CaseBible` caches *within an episode*, and dynamic scene payloads sit at the tail.

## 1. Prompt-Cache Ordering & Security Envelope

1. **Byte 0 — Global Static Prefix:** Role instruction + 13 Laws + `MOTIF_REGISTRY_V1` Zod schema + split Forensic-to-Noir Metaphor Tables (`TEXT_TO_VIDEO` vs `FIRST_FRAME`/`FIRST_AND_LAST_FRAME`).
2. **Tier 2 — Per-Episode Static Context:** `CaseBible` Style DNA + immutable character registry + explicitly `LOCKED` `spatial_anchors` (`is_illustrative_reconstruction = 1`).
3. **Tier 3 — Dynamic Turn Payload:** Current beat/scene/document text wrapped strictly in `<data source="...">...</data>` (untrusted input boundary).

## 2. Prompt Contract Inventory (v3)

| # | Contract ID | Default Model (`providers.yaml`) | Stage / Owner | Key v3 Updates |
|---|---|---|---|---|
| 1 | `alias-expander@1` | `DeepSeek-V4.1-Flash-1017` | Agent 1 (Part 1) | 3–4 canonical search aliases |
| 2 | `comment-gap-miner@1` | `DeepSeek-V4.1-Flash-1017` | Agent 1 (Part 1) | Quality gaps + Safe-Title CTR feasibility (`LEAD_ONLY` comments) |
| 3 | `youtube-xray@3` | `gemini-3.5-flash-lite` / `3.8-flash` | Agent 1 (Part 1) | Clean-Room Seed Firewall; **authorized metadata/comments fallback only** when age-restricted (NO third-party `captions.download` scraping! `F-11`) |
| 4 | `evidence-ledger-extractor@3` | `DeepSeek-V4.1-Flash-1017` + `V4-Pro-0813` | Agent 2 (Part 1) | Standing disposition check (`AFFIRMED`/`STANDING_CONVICTION`) + living 3rd-party anonymization (`NOT_STARTED -> IN_REVIEW -> APPROVED`) |
| 5 | `that-vs-how-linter@1` | `DeepSeek-V4.1-Flash-1017` | Agent 3 (Part 1) | Forensic `"that"` rewrite + anti-legal-persona + hedging risk controls |
| 6 | `tts-director@1` | `gemini-3.8-flash-tts` | Voice-First (Part 1) | Consistent chunk style prefix + segmented `NarrationSegment`s |
| 7 | `director-manifest@3` | `DeepSeek-V4.1-Flash-1017` | Agent 4 (Part 1) | `MOTIF_REGISTRY_V1`; segmented `VoiceTrackManifest`; `prompt_mode` (`TEXT_TO_VIDEO`, `FIRST_FRAME`, `FIRST_AND_LAST_FRAME <= 10s`); **`13.0m / 5.67m / 1.33m`** (`max_hero_clips = 10`) |
| 8 | `director-repair@3` | `DeepSeek-V4.1-Flash-1017` | Agent 4 (Part 1) | Exact `RULE_01`–`RULE_13` diff repair (Act-constrained `RULE_02`, `>= 2.5s` remainder splits) |
| 9 | `grid-grounding-vision@2` | `DeepSeek-V4.1-Flash-1017` (Vision) | Agent 2 (Part 1) | Reads external-margin `A–J/1–10` illustrative 2K plate -> returns `{grid_cell, sub_quadrant, span_cols, span_rows}` (written as `DRAFT` pending lock) |
| 10 | `omni-clip-qa@2` | `gemini-3.5-flash` / `DeepSeek-V4.1-Flash` | Agent 5C (Part 2) | 3-frame safety/morph/garbled-text check; **fail-closed** to `PENDING_MANUAL_SPOT_CHECK` if API unreachable |
| 11 | `frame-spot-qa@1` | `DeepSeek-V4.1-Flash-1017` (Vision) | Agent 6 (Part 2) | `2x2` contact sheet overlap & glitch audit; fail-closed if unreachable |
| 12 | `thumbnail-auditor@2` | `DeepSeek-V4.1-Flash-1017` (Vision) | Agent 6 (Part 2) | Policy risk control + brand-coherent composition/mood novelty |

## 3. Key Output Schemas

### `grid-grounding-vision@2`
```json
{
  "anchors": [
    {
      "clue_name": "broken_table",
      "cited_fact_id": "fact_014",
      "grid_cell": "E3",
      "sub_quadrant": "C",
      "span_cols": 2.0,
      "span_rows": 1.5,
      "confidence": 0.94
    }
  ]
}
```

### `director-manifest@3` (`prompt_mode` Aligned with `flow_jobs` Schema `F-07`)
Every `FLOW_HERO_VIDEO` scene explicitly outputs `prompt_mode: "TEXT_TO_VIDEO" | "FIRST_FRAME" | "FIRST_AND_LAST_FRAME"`, validating `duration_bucket_sec in [3, 15]` (`[3, 10]` for `FIRST_AND_LAST_FRAME`) and ensuring `FIRST_FRAME` / `FIRST_AND_LAST_FRAME` prompts contain strictly motion/camera language with zero character-clothing descriptors.
