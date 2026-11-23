# Agent 4: Two-Layer Director & Conflict-Resolved 13 Deterministic Laws (v3)

Agent 4 acts as a two-layer compiler: **Layer 1 (`DeepSeek-V4.1-Flash-1017`)** proposes `ProductionManifest` + `TimelineSpec`, and **Layer 2 (`manifest_linter.py`)** enforces all 13 deterministic laws cleanly with zero inter-rule deadlocks against `providers.yaml` and `MOTIF_REGISTRY_V1`. Diagram: [director-and-13-laws.mmd](director-and-13-laws.mmd).

## 1. Byte-0 Static Prompt Caching & Honest 1,200s Split (`F-01`, `F-02`, `F-16`)

- **Cache-Optimal Prefix Ordering:** Byte `0` holds **global static rules** (13 Laws, `MOTIF_REGISTRY_V1` Zod schema, split Forensic-to-Noir Metaphor Tables); `CaseBible` sits second; dynamic beat/ASR/anchor inputs sit last.
- **Honest 20-Min Split (Single Source of Truth in `providers.yaml`):** **`13.0 min (780s)`** Code/Cards/FOIA + **`5.67 min (340s)`** 2K Illustrative Stills (`crime_scene_2k`) + **`1.33 min (80s)`** `gemini-omni-1.2-flash` Hero Video (**`MAX_HERO_CLIPS = 10`**, `max_hero_duration_sec = 80s`, zero 15-vs-16 mismatch!).

## 2. Conflict-Resolved 13-Law Specification (`manifest_linter.py`)

| Rule / Law | Resolved Deterministic Specification (v3) |
|---|---|
| **`RULE_01` (Law 1)** | `abs(sum(scene_durations_ms) - VoiceTrackManifest.total_master_ms) <= 250 ms` (sums contiguous, non-overlapping `NarrationSegments + FoiaAudioSlots + TwistPads`; transactional `timeline_validated_sha256` required before mastering). Speed-ramping outside `0.85x–1.15x` banned. |
| **`RULE_02` (Law 3)** | **Single-Config Cap & Act-Constrained Downgrade (`F-02`):** Enforces `providers.yaml` limits (`MAX_HERO_CLIPS = 10`, `max_hero_duration_sec = 80s`, `$8.00` base / `$10.40` durable SQLite USD cap via `budget_reservations`). Auto-downgrade trims lowest-score scenes **while protecting Act 2's `>= 2` peaks (`RULE_06`)** and Cold Open! |
| **`RULE_03` (Law 1)** | `FLOW_HERO_VIDEO` fits valid `gemini-omni-1.2-flash` durations (`3s–15s` for `TEXT_TO_VIDEO` / `FIRST_FRAME`; **`3s–10s` max** for `FIRST_AND_LAST_FRAME` transitions). Beats requiring a remainder split ensure `remainder >= 2.5s` (e.g., `6.0s Flow + 3.2s Code` instead of `8.0s + 1.2s`) so `RULE_07` hold time (`>= 1.0 + 0.3*words`) fits cleanly. |
| **`RULE_04` (Law 3)** | Every Hero scene carries a zero-video-API `fallback_spec` whose **`engine != prev_scene.engine` (and `!= next_scene.engine` when possible)**—typically `STILL_2K_PANZOOM` between `CODE_STICKMAN` scenes—preventing `> 50s` `RULE_05` streaks on fallback! |
| **`RULE_05` (Interrupts)** | Static/2K scenes require micro-beat motion/callouts `<= 6.0s`; continuous `FLOW_HERO_VIDEO` (`<= 10.0s`) is exempt from the 6.0s cut clock. Single engine streak `<= 50.0s`. **`CaseBoardSpine`** triggers inside a **flexible `210s–270s` window snapped to the nearest completed sentence/scene boundary**. |
| **`RULE_06` (Law 8)** | Act 1 (`0:00–5:00`) `<= 40%` Hero budget; Act 2 (`6:00–14:00`) `>= 2` Hero/FOIA peaks; 1 Open Loop every `3.5–4.5` min. |
| **`RULE_07` (Law 7)** | `<= 12` non-caption words, held `>= 1.0 + 0.3*words` sec. Remotion CSS layout constraints enforce Safe-Zone margins (`bottom 18%`, `top 10%`, `bottom-right 22%x14%`, `final 20s`), verified post-render on pixels by Agent 6. |
| **`RULE_08` (Law 5)** | Last-5 SQLite Cold-Open rotation, `>= 3` Turning Points, and brand-coherent thumbnail composition/mood novelty. |
| **`RULE_09` & `RULE_10`** | Zero unhedged `news_report` claims, zero AI legal advice, zero distress tags, mandatory `altered_content_disclosure = 1`, `"TRANSCRIPT DRAMATIZATION"` badge on voiced quotes, and **`ILLUSTRATIVE RECONSTRUCTION — NOT CRIME SCENE PHOTO`** on generated scenes (`F-05`). |
| **`RULE_11` & `RULE_12` (Aligned!)** | **Explicit `prompt_mode` (`F-07`):** `TEXT_TO_VIDEO` (`start_frame_png = NULL, end_frame_png = NULL`) allows atmospheric `"dark charcoal stick silhouettes"`; `FIRST_FRAME` / `FIRST_AND_LAST_FRAME` strip clothing/identity words (`"hooded"`, `"detective"`, `"charcoal"`) and describe strictly motion + camera path (`15–30 words` Omni 1.2 Flash). **Cinematography Bigram Whitelist:** Protect `tracking shot`, `static shot`, `dolly shot`, `wide shot` BEFORE Stage 1 regex checks `"shoot"`/`"shot"`. **Keyframes:** Zero `evidenceCrimsonHex` (`#C92A2A`) in Start/End PNGs. |
| **`RULE_13` & `Laws 2, 4, 6`** | Both `prompt_v1` + `prompt_v2_safe` pre-compiled (`RULE_13`); `CaseBible` locked (`Law 2`); `spatial_anchors` explicitly `LOCKED` (`lock_status = 'LOCKED'`) with cited `fact_id` + `travel_axis` consistent (`Law 4`); L-cuts `0.6–1.0s` + `-22 -> -36 LUFS` duck + room-tone twist pads (`Law 6`). |
