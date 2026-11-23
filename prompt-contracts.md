# Prompt Contracts, Versioned `ScenePlan`, Craft Rubric & Injection Boundaries (v4 · `F-05`, `F-06`)

All LLM/Vision/Image/Video/TTS identifiers load strictly from `providers.yaml`. Prompts follow **structural separation**: crisp global rules + modular `craft_rubric.yaml` (`<= 150 lines`—NEVER a bloated 3,000–4,000-line prompt!), case research ledger, and versioned per-scene **`ScenePlan`** rows (`F-05`, `F-06`).

## 1. Anti-Prompt-Injection Security Envelope (`Additional Check #2`)

Wrapping raw transcripts or comments in `<data>` tags is **NOT** sufficient against delimiter-breaking prompt injections (`</data>` followed by fake instructions). Every extractor processing external text enforces 4 layered controls:
1. **Control-Tag & Delimiter Sanitization:** Strip/escape XML-like delimiter strings inside raw external documents and encapsulate inside unique random per-call nonces (`<untrusted_source_7f9a>...</untrusted_source_7f9a>`).
2. **Tool-Less Extraction Isolation:** Models parsing external YouTube comments, court PDFs, or FOIA transcripts receive **ZERO function/tool-calling privileges**, **ZERO database write access**, and **ZERO shell/filesystem tools**.
3. **Strict Schema Decoding (`extra="forbid"`):** Outputs must pass deterministic Pydantic validation referencing ONLY pre-indexed local `doc_id` / `fact_id` keys (rejecting invented URLs or ungrounded directives).
4. **Adversarial Injection Regression Fixtures:** `tests/` includes synthetic transcripts containing fake `"IGNORE PREVIOUS INSTRUCTIONS"` and `"</data>"` breakouts asserting `0` unauthorized instructions propagate into `fact_ledger` or prompts.

## 2. Modular Prompt Layers & Versioned `ScenePlan` Contract (`F-05`, `F-06`)

Instead of one unwieldy 4,000-line prompt, Agent 4 and reviewers operate on **four clean, independently versioned layers**:
1. **`craft_rubric.yaml` (Global Concise Documentary Standard, `<= 150 lines`):** General original craft principles (`"interactive"` defined strictly as **engaging visual documentary pacing**: clear opening question within `0:00–0:20`, clean beat shifts `<= 6s` on static plates, crisp Safe-Zone callouts, clear title/chapter transitions, verifiable claim-to-citation traceability—NEVER copying competitor scripts, assets, or branding!).
2. **`CaseBible` + `TemporalFactLedger` + Locked `still_assets`/`spatial_anchors` (`is_illustrative_reconstruction = 1`).**
3. **Per-Scene Versioned `ScenePlan` (`scene_plans` table in `schema/pipeline.sql` v4):** Must be approved (`PLAN_APPROVED`) *before* expensive asset generation (`ASSETS_CREATED`) and re-verified before final assembly (`EDITED_APPROVED`):
   - `story_purpose` & `intended_audience_effect`
   - `approved_narration_text` + `narration_version_sha256` + `cited_fact_ids_json`
   - `visual_concept`, `prompt_mode` (`NONE` | `TEXT_TO_VIDEO` | `FIRST_FRAME` | `FIRST_AND_LAST_FRAME`), `visual_prompt`, `keyframe_refs_json`, `expected_output_summary`
   - `timing_start_ms` / `timing_end_ms`, `transition_spec_json`, `sound_cues_json`, `edit_instructions`
   - `acceptance_criteria_json` (semantic match: *"Does visual match approved narration and cited evidence without misleading viewer?"* + technical checks)
   - Upstream narration change automatically flips `plan_status` -> `STALE_NEEDS_REAPPROVAL` via `trg_scene_plan_invalidate_on_narration_edit`!

## 3. Canonical Prompt Contract Inventory (v4)

| # | Contract ID | Default Model (`providers.yaml`) | Owner & Bounds |
|---|---|---|---|
| 1–2 | `alias-expander@1`, `comment-gap-miner@1` | `DeepSeek-V4.1-Flash-1017` | Part 1 (`LEAD_ONLY` extraction, zero tools) |
| 3 | `youtube-xray@3` | `gemini-3.5-flash-lite` / `3.8-flash` | Part 1 (authorized `videos.list` + comments ONLY; no 3P `captions.download`) |
| 4 | `evidence-ledger-extractor@3` | `DeepSeek-V4.1-Flash-1017` + `V4-Pro-0813` | Part 1 (`disposition_status` check + `anonymization_status` `NOT_STARTED -> IN_REVIEW -> APPROVED`) |
| 5 | `that-vs-how-linter@1` | `DeepSeek-V4.1-Flash-1017` | Part 1 (policy risk controls & hedging verification) |
| 6 | `tts-director@1` | `gemini-3.8-flash-tts` | Part 1 (word alignment owned downstream by local WhisperX `F-03`) |
| 7 | `scene-planner@1` | `DeepSeek-V4.1-Flash-1017` | Part 1 (proposes typed `ScenePlan[]` guided by `craft_rubric.yaml` BEFORE voice/render!) |
| 8–9 | `director-manifest@4`, `director-repair@4` | `DeepSeek-V4.1-Flash-1017` | Part 1 (compiles approved `ScenePlan[]` against `MOTIF_REGISTRY_V1`; **`13.0m / 5.67m / 1.33m`**, `max_hero_clips = 10`, `prompt_mode in {TEXT_TO_VIDEO, FIRST_FRAME, FIRST_AND_LAST_FRAME <= 10s}`) |
| 10 | `grid-grounding-vision@2` | `DeepSeek-V4.1-Flash-1017` (Vision) | Part 1 (external-margin `A–J/1–10` on illustrative 2K plates; `DRAFT -> LOCKED`) |
| 11–13 | `omni-clip-qa@2`, `frame-spot-qa@1`, `thumbnail-auditor@2` | `gemini-3.5-flash` / `DeepSeek-V4.1-Flash` | Part 2 (fail-closed -> `PENDING_MANUAL_SPOT_CHECK` if API unreachable) |
