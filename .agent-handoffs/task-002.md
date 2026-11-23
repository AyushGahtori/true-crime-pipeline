# Task 002 — Frozen v4 shared contracts

## Branch
`task/002-frozen-shared-contracts`

## Delivered
- `packages/shared_contracts` — Pydantic v2 models (`extra="forbid"`), JSON Schema export, `grid_cell_to_pixel_and_zoom`, loader/render ports
- `packages/shared-contracts-ts` — matching Zod `.strict()` models
- `packages/shared_contracts/fixtures/vectors.json` — 60 valid + 60 adversarial payloads plus grid cases, shared by both runtimes
- `packages/shared_contracts/schema/contracts-v4.json` — exported JSON Schema (`contract_version` `v4`)

## Contract version
`v4` (`CONTRACT_VERSION`). SQL `schema_version` stays `'4'` and was not edited.

## Verify
From this worktree, offline, no provider calls:

```powershell
py -3 -m pytest packages/shared_contracts -q
npm --prefix packages/shared-contracts-ts test
```

The TypeScript suite is `node --experimental-strip-types --test` (Node 24). Vitest is not required. Zod and `yaml` are dependencies of `@tc/shared-contracts-ts` only.

`estimated_micro_usd` has no code default. Provider prices are read from a mapping or a YAML path. The only sample rates live in `packages/shared_contracts/tests/fixtures/providers.yaml`.

## Inferred shapes
Fields that are not a single SQL column are documented in the commit that freezes this branch. Column names that do exist (`scene_plans`, `spatial_anchors`, `flow_jobs`, `episode_analytics`, `fact_ledger`, `compliance_audits`, `case_bibles`) are the JSON keys. `*_json` keys carry parsed JSON, not a second-encoded string. Boolean flags are JSON booleans.

`ScenePlan.prompt_mode` includes `NONE` because `scene_plans` does. `TimelineSpec.prompt_mode` and `FlowJobCard.prompt_mode` are only `TEXT_TO_VIDEO | FIRST_FRAME | FIRST_AND_LAST_FRAME`.

`MOTIF_REGISTRY_V1` is exactly `StickmanStage`, `AudioEvidenceCard`, `RedactedDocReveal`, `FoiaFootageFrame` (`render_catalog`). `Illustrative2KPanZoom` remains a `crime_scene_2k` catalog motif on `ScenePlan` and is rejected on `TimelineSpec`. `CrimeScenePanZoom`, `FRAMES_MOTION_ONLY`, and `VEO_3_1_LITE` are rejected anywhere they appear in a payload.

`grid_cell_to_pixel_and_zoom` uses the Task 145 crop: `zoom = clamp(min(8/span_cols, 8/span_rows), 1.6, 3.8)` and the cell-center pixel `(2*index+1)*size/20`, half-up. Stored `spatial_anchors.target_zoom` still allows the SQL range `1.0..3.8`.

## Dependencies
Package-local only: `pydantic`, `PyYAML` (Python) and `zod`, `yaml` (TypeScript). No root `pyproject.toml` or `providers.yaml`.
