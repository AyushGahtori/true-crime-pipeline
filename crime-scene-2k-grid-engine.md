# Agent 5B: Illustrative 2K Grid Engine & Screen-Space Cubic Pan/Zoom (`packages/crime_scene_2k`) (v3)

`packages/crime_scene_2k` is the **sole owner** of all `STILL_2K_PANZOOM` (`Illustrative2KPanZoom`) rendering in the pipeline (`F-16`—not duplicated inside Remotion `@tc/render_catalog`), consuming Part 1's clean 2K plates (`still_assets`) and explicitly locked `spatial_anchors` (`lock_status = 'LOCKED'`). Diagram: [crime-scene-2k-grid-engine.mmd](crime-scene-2k-grid-engine.mmd).

## 1. Mandatory Illustrative Reconstruction Labeling (`F-05`)

Because 2K room plates are AI-generated visual aids derived from text descriptions rather than crime-scene photographs or scaled forensic surveys:
- Every output clip rendered by `crime_scene_2k` automatically burns a crisp, subtle, Safe-Zone-compliant editorial badge (`ILLUSTRATIVE RECONSTRUCTION — NOT CRIME SCENE PHOTO`, read from `still_assets.disclaimer_label_text`) in the upper-left safe band (`y = 68px`, `x = 110px`, muted parchment/charcoal contrast) so viewers never mistake generated geometry for actual evidence!
- Every callout label MUST link back to a cited `fact_ledger(fact_id)` excerpt rather than inventing unverified room measurements.

## 2. Non-Occluding External-Margin `10x10` Grid & `span_cells` (`F-09`)

- **External Margin Border Labels:** Rather than stamping 100 labels inside the scene pixels, inspection copies pad a `64 px` charcoal outer border printing `A–J` columns and `1–10` rows outside the artwork (`grid_cell` validated by SQLite `GLOB '[A-J][1-9]' OR '[A-J]10'`). The clean source 2K PNG on disk is never modified.
- **Clue Bounding Span (`span_cols`, `span_rows`):** Target magnification is derived from clue span (`crop_w = (span_cols / 10.0) * W * 1.25`, clamped strictly to `[1.6, 3.8]` and `min(zoom_x, zoom_y)` so tall vertical objects never clip).

## 3. Edge-Clamped Crops & Screen-Space Projected Callouts

- **Edge Viewport Clamping:** When zooming onto corner/edge cells (`A1`, `J10`), the `16:9` crop box clamps strictly inside `[0, W] x [0, H]` (`max_crop_w = min(W, H * 16 / 9)` handling `4:3` and ultrawide plates cleanly with zero black bars or letterboxing).
- **Screen-Space Callout Projection:** Because edge clamping shifts the viewport center away from the anchor, crimson callout circles (`#C92A2A`) and Safe-Zone-clamped captions are projected mathematically from world `(x_px, y_px)` through the instantaneous clamped camera window `(x0(t), y0(t), crop_w(t), crop_h(t))` to exact `1920x1080` screen coordinates AFTER `cv2.warpAffine(..., flags=cv2.INTER_LANCZOS4)` so vector text/rings stay razor-sharp without Lanczos ringing.
- **Single-Pass Grading Parity:** `crime_scene_2k` outputs clean un-grained `1920x1080 CFR 30fps` MP4 clips and registers them in `scene_grade_manifest.json` so Agent 6 applies continuous paper grain & vignette strictly ONCE.
