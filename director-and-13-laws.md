# Agent 4: Two-Layer Director, Craft Rubric & 13 Deterministic Laws (v4 · `F-05`, `F-06`)

Agent 4 separates **concise global documentary craft principles (`craft_rubric.yaml`)**, **typed per-scene contracts (`ScenePlan` / `scene_plans`)**, and **deterministic rule validation (`manifest_linter.py`)**—replacing vague aspirations or bloated monolithic prompts with measurable scene-by-scene checks (`F-05`, `F-06`). Diagram: [director-and-13-laws.mmd](director-and-13-laws.mmd).

## 1. Translating Visual Craft Into `craft_rubric.yaml` (`<= 150 Lines`) & `ScenePlan` (`F-06`)

- **What "Interactive" Means Here (`F-06`):** Strictly **high-engagement visual documentary rhythm and viewer curiosity hooks** (NOT clickable player widgets!).
- **Modular 3-Input Separation (`craft_rubric.yaml` -> Episode Research -> `ScenePlan`):**
  1. Opening hook raises an explicit primary-record curiosity question inside `0:00–0:20` with clean AdSense compliance.
  2. Visual variation changes framing or graphic motif `<= 6.0s` on static/2K beats and switches macro engines before `<= 50.0s`.
  3. Legible location, timestamp, and action callouts obey CSS Safe-Zones (`<= 12` words, `>= 1.0 + 0.3*words` sec) and cite `fact_ledger` IDs.
  4. **Stage 1 (`PLAN_APPROVED`)** validates story purpose, audience effect, approved narration, visual concept, expected output, edit cues, and semantic acceptance criteria BEFORE voice locking and paid asset generation!

## 2. Canonical v4 Limits & 13-Law Specification (`manifest_linter.py`)

- **Honest Single-Config Runtime Split (`providers.yaml`):** **`13.0 min (780s)`** Code/Cards/FOIA + **`5.67 min (340s)`** 2K Illustrative Stills (`crime_scene_2k`) + **`1.33 min (80s)`** `gemini-omni-1.2-flash` Hero Video (**`MAX_HERO_CLIPS = 10`**, `max_hero_duration_sec = 80s`, `$8.00` base / `$10.40` episode DB cap).
- **Explicit `prompt_mode` Alignment (`F-04`, `F-07`):** Strictly `TEXT_TO_VIDEO` (`3s–15s`, null frames), `FIRST_FRAME` (`3s–15s`, 1 keyframe, motion/camera prompt), or `FIRST_AND_LAST_FRAME` (**`3s–10s` max**, 2 keyframes, motion/camera prompt). Zero references to retired `FRAMES_MOTION_ONLY` or `Veo 3.1 Lite`!
- **`RULE_01`–`RULE_13` Highlights:**
  - `RULE_01`: Non-overlapping `voice_segments` (`sum == total_master_ms +/- 250ms`) + `ScenePlan` `narration_version_sha256` match!
  - `RULE_02`: Checks BOTH per-episode `$10.40` cap AND global monthly `$135/mo` `ALL_PROVIDERS` headroom (`Act 2 >= 2 peaks` preserved during Act-constrained downgrade).
  - `RULE_03`: Remainder beats `>= 2.5s` (`6s + 3.2s` for `9.2s` beat) and `<= 10s` cap when `FIRST_AND_LAST_FRAME`.
  - `RULE_04`/`05`: Non-neighbor `fallback_spec`, continuous Hero motion exempt from 6s cut clock, `210–270s` boundary-snapped `CaseBoardSpine`.
  - `RULE_07`–`RULE_13`: CSS Safe-Zones, cold-open entropy, `fact_ledger` citations & `"TRANSCRIPT DRAMATIZATION"` / `"ILLUSTRATIVE RECONSTRUCTION"` labels, cinematography bigram whitelist (`tracking shot`), zero `#C92A2A` crimson inside video Start/End PNGs.
