# Research: Remotion JS Line-Boil Hypothesis, CSS Safe-Zones & 2K Illustrative Grid (`F-05`, `F-16`, `F-21`)

*Last verified: 2026-11-23*

## 1. Engineering Hypotheses & Design Targets (Pending Reproducible Local Benchmarks — `F-21`)
The figures below represent **architectural design targets and hypotheses** motivated by Chromium filter rasterization behavior; they MUST NOT be treated as verified production SLAs until measured on target hardware via `packages/render_catalog/benchmarks/js_boil_bench.ts` (`Task 131`) and `packages/crime_scene_2k/tests/test_drift_regression.py` (`Task 149`) with recorded CPU/OS/Chromium specs:
- **SVG `<feTurbulence>` vs. JS `6 fps` Polyline Vertex-Jitter:**
  - *Hypothesis:* Headless Chromium rasterizing per-frame SVG `<feTurbulence>` + `<feDisplacementMap>` at 1080p can stall CPU rendering substantially (often seconds per frame), threatening rapid single-scene surgical heals. Replacing SVG noise filters with deterministic JS polyline vertex-jitter quantized to `6 fps` (`Math.floor(frame / 5)` at `30 fps`) avoids SVG filter rasterization overhead completely.
  - *Target to Verify in `Task 131`:* `< 5.0s` warm single-scene 10s render latency on target workstation (exact `p50`/`p95` and hardware spec saved to `artifacts/benchmarks/remotion_js_boil_perf.json`).
- **Single-Pass Continuous Grain:** Emitting clean un-grained frames + `scene_grade_manifest.json` from `@tc/render_catalog` and `crime_scene_2k` lets Agent 6 execute one continuous grain/vignette pass across non-FOIA clips while keeping `FOIA_REAL_FOOTAGE` raw.

## 2. Clear Package Ownership & Illustrative 2K Grounding (`F-05`, `F-16`)
- **`@tc/render_catalog` (Remotion):** Owns strictly 2D vector motifs (Authoritative 4-Motif MVP: `StickmanStage`, `AudioEvidenceCard`, `RedactedDocReveal`, `FoiaFootageFrame`; extended 12-motif full catalog). Enforces YouTube UI exclusion zones via CSS Flexbox/Grid containment.
- **`packages/crime_scene_2k` (Python OpenCV `INTER_LANCZOS4`):** Sole owner of `STILL_2K_PANZOOM` (`Illustrative2KPanZoom`). Uses external-margin `A–J / 1–10` grid overlays (never burned into clean render plates), `span_cols`/`span_rows` `[1.6x, 3.8x]` zoom clamping, edge-clamped crops, screen-space projected crimson callouts, and mandatory **`ILLUSTRATIVE RECONSTRUCTION — NOT CRIME SCENE PHOTO`** labeling.
  - *Target to Verify in `Task 149`:* Empirically measure pixel localization error (`<= 1.0px` projected circle error on clamped `A1`/`J10` plates) against a reproducible synthetic ground-truth benchmark suite.
