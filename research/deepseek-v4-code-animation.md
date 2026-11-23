# Research: Code-to-Video LLM Roles, Token Estimates & Spatial Grounding Hypothesis (`F-01`, `F-21`)

*Last verified: 2026-11-23*

## 1. Config-Driven Model Roles (`providers.yaml`)
All LLM checkpoints, pricing rates, and context limits are loaded from `providers.yaml` rather than hardcoded constants, and verified via a bounded sandbox check in `M0.5`:
- **Primary Scripting / Manifest / Vision-QA Role (configured default e.g. `DeepSeek-V4.1-Flash-1017`):** Used for long-context primary-document extraction (`TemporalFactLedger`), `TimelineSpec` JSON compilation against `MOTIF_REGISTRY_V1`, and `2x2` contact-sheet Vision QA.
- **Deep Contradiction Reasoning Role (configured default e.g. `DeepSeek-V4-Pro-0813`):** Reserved strictly for resolving multi-document factual contradictions in Agent 2.

## 2. Rationale for Code-to-Video Majority Runtime (`13.0 min` Code/FOIA + `5.67 min` 2K + `1.33 min` Video API)
1. **Stroke Consistency & Typography Precision:** Parametric React/Remotion/SVG coordinates keep stick-figure ink strokes, `CaseBible` palette colors, and cited primary-document quotes crisp at 1080p without video-diffusion text hallucination or limb shimmer.
2. **Economic Control After Veo 3.1 Preview Shutdown (`F-01`, `F-02`):** Delegating fluid cinematic acting/camera beats strictly to `gemini-omni-1.2-flash` (`<= 10` clips, `<= 80s` = `$8.00` base / `$10.40` hard DB cap per episode @ conservative `$0.10/sec` 720p estimate) keeps full 20-minute episodes viable inside the `$135/mo` autonomous compute cap.
3. **Token Pricing Verification Note (`F-21`):** Historical planning estimates (`~$0.30/1M` peak input, `~$1.20/1M` peak output, `98%` prompt-cache discount, `50%` off-peak discount -> `~$0.75–$1.90/episode`) are **planning assumptions** that must be confirmed against current provider billing docs and updated in `providers.yaml` prior to production spend.

## 3. Spatial Grounding Hypothesis (`F-05`, `F-21`)
- Raw VLM pixel-coordinate guessing frequently misses small visual objects on wide 2K plates (prior literature/project notes cited an unverified `71.7%` naive miss rate—treated strictly as a **motivating hypothesis**, NOT an established project measurement, until `Task 149` runs its reproducible 20-layout OpenCV benchmark on actual generated plates).
- Every 2K plate generated from text is strictly an **Illustrative Reconstruction** (`still_assets.is_illustrative_reconstruction = 1`), NEVER verified crime-scene spatial evidence.
