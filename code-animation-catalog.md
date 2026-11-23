# Agent 5A: Code-Animation Engine & Authoritative Motif Registry V1 (`F-16`)

Part 2 compiles DeepSeek's compact `TimelineSpec` JSON through a permanent typed Remotion + Zod catalog (`@tc/render_catalog`) locked to **`1920x1080 @ 30 fps`**. Crucially, this architecture replaces slow Chromium SVG `<feTurbulence>` with `6 fps` JS vertex-jitter, avoids double-grading across scene boundaries, and establishes **one single authoritative motif registry (`MOTIF_REGISTRY_V1`)** with clean package ownership boundaries. Diagram: [code-animation-catalog.mmd](code-animation-catalog.mmd).

## 1. Layer 1 — Parametric `StickFigure` Rig (`6 fps` JS Vertex-Jitter)

- **No SVG `<feTurbulence>` Filters:** SVG `<feTurbulence>` + `<feDisplacementMap>` filters are banned in `@tc/render_catalog` because Chromium CPU filter rasterization degrades single-scene heal turnaround. Instead, `StickFigure` applies **deterministic JS polyline vertex-jitter** quantized to **`6 fps` ticks (`Math.floor(frame / 5)` at `30 fps`)**.
  - *Design Target (to be verified empirically on target hardware in `Task 131`):* `< 5.0s` warm single-scene 10s re-render latency.
- **Locked Proportions & `CaseBible`:** Mathematical limb ratios, 14 enum poses, 10 enum emotions, `amplitude_envelope[]` head-nod sync, and `CaseBible` props.
- **CSS Layout Safe-Zone Enforcement:** Remotion motif layouts enforce YouTube UI exclusion zones directly via CSS Flexbox/Grid containment (`paddingBottom: 194px`, `paddingTop: 108px`, bottom-right exclusion box, final-20s card guard), audited post-render on pixels by Agent 6.

## 2. Authoritative Motif Registry V1 & Package Ownership (`F-16`)

To eliminate cross-document naming drift and clarify renderer ownership, `schema/pipeline.sql` (`motif_registry`) is the single source of truth:

### A. Authoritative 4-Motif MVP Slice (`--mvp-4-motifs`, Milestone `M0.5` & `M1-P2`)
Owned strictly by **`@tc/render_catalog`** (`is_mvp_4 = 1`):
1. **`StickmanStage`** — Primary narrative dialogue, investigative walkthroughs, and stick-figure staging (`~35%` runtime).
2. **`AudioEvidenceCard`** — Waveform / dossier visualizer for 911 calls & interrogation quotes (**mandatory `"TRANSCRIPT DRAMATIZATION"` badge on any non-archival TTS quote**).
3. **`RedactedDocReveal`** — Primary court ruling / police affidavit excerpts with animated highlighter sweep & source citation footer.
4. **`FoiaFootageFrame`** — Rights-cleared, PII-scrubbed `CFR 30fps` FOIA bodycam/dashcam/court video frame + clean editorial HUD (exempt from synthetic paper grain!).

### B. Extended Remotion 2D Catalog (`M2-Full`, `@tc/render_catalog` Motifs #5–#12)
5. **`TimelineScrubber`** — Chronological date/hour scrubber across multi-day case events.
6. **`AnimatedMapRoute`** — Stylized parchment vector street/highway route & timestamp trace.
7. **`CellTowerTriangulation`** — Abstract azimuth sector cones and ping timeline visualization.
8. **`SplitScreenComparison`** — Side-by-side alibi statement vs. cited primary-record contradiction.
9. **`CaseBoardSpine`** — Flexible `210s–270s` boundary-snapped corkboard thread recap.
10. **`QuotePullout`** — High-contrast primary-document or witness quote typography card.
11. **`EvidenceGridMatrix`** — Multi-clue dossier overview grid linking cited `fact_ledger` IDs.
12. **`ChapterSlateTransition`** — Crisp documentary act/chapter divider card + subtle timestamp index.

*(Plus Layer 4 escape hatch: declarative SVG-primitive `CustomDiagramScene` for bespoke 2D vector diagrams.)*

### C. Clear Ownership Boundary for 2K Stills & Paid Hero Video (`F-16`)
- **`Illustrative2KPanZoom` (`STILL_2K_PANZOOM`) — Owned SOLELY by Python `packages/crime_scene_2k`:** OpenCV `INTER_LANCZOS4` sub-pixel camera pans, edge-clamped crops, screen-space projected crimson callouts, and mandatory **`ILLUSTRATIVE RECONSTRUCTION — NOT CRIME SCENE PHOTO`** label live strictly in `crime_scene_2k` (NOT duplicated in Remotion!).
- **`HeroVideoBridge` (`FLOW_HERO_VIDEO`) — Owned SOLELY by `packages/flow_adapter`:** Generated via `gemini-omni-1.2-flash` Interactions API, conformed to `1920x1080 CFR 30fps`, and swapped on 2-strike failure to a non-neighbor fallback engine.

## 3. Single-Pass Grading & Monochrome Flow Keyframes

- **Zero Remotion Grain/Vignette (No Double-Grading):** `@tc/render_catalog` outputs clean un-grained frames and writes `scene_grade_manifest.json`. **Agent 6 applies continuous paper grain & vignette strictly ONCE** across all non-FOIA segments, leaving `FOIA_REAL_FOOTAGE` raw.
- **Zero Crimson in Video Keyframes:** Python PIL Start/End PNGs for `FIRST_FRAME` / `FIRST_AND_LAST_FRAME` video jobs render strictly in monochrome charcoal + muted slate/amber (`evidenceCrimsonHex` `#C92A2A` banned inside video input keyframes).
