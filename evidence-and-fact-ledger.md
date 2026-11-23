# Agent 2: Evidence Harvester, INSERT+UPDATE Disposition Gate & Illustrative 2K Anchor Lock (v3)

Agent 2 eliminates hallucinated-crime contagion, appellate reversal defamation traps (`F-03`), bogus default-true anonymization flags (`F-04`), misleading generated "evidence" stills (`F-05`), and the Law 4 circular dependency. Diagram: [evidence-and-fact-ledger.mmd](evidence-and-fact-ledger.mmd).

## 1. Primary-Record & Appellate Disposition Gate (INSERT + UPDATE + Quarantine) (`F-03`)

- **Mandatory Standing Posture:** Verify BOTH case identity AND standing appellate posture (`disposition_status IN ('AFFIRMED', 'STANDING_CONVICTION')` corroborated by CourtListener + state DOC / `.gov` records). Automatically reject `REVERSED`, `VACATED`, `ACQUITTED`, `PENDING`, or unverified leads.
- **Database-Enforced Update Protection & Auto-Quarantine:** `trg_case_disposition_guard_insert` AND `trg_case_disposition_guard_update` prevent inconsistent `conviction_confirmed = 1` writes on both INSERT and UPDATE. If a later case refresh updates `disposition_status` from `AFFIRMED`/`STANDING_CONVICTION` to `REVERSED`/`VACATED`/`ACQUITTED`/`PENDING`, `trg_case_disposition_quarantine` **automatically moves all non-terminal downstream episodes to `QUARANTINED_LEGAL_HOLD` and revokes existing `release_approvals`**!

## 2. Explicit Third-Party Anonymization State Machine (`F-04`)

- `cases.anonymization_status` defaults strictly to **`'NOT_STARTED'`** (NEVER default `1`!).
- Agent 2 runs NER/regex masking of unconvicted living coworkers, neighbors, and family members into neutral role aliases (`"Witness A"`, `"Neighbor B"`), transitions status to `'IN_REVIEW'`, and records the scrubbed artifact hash.
- Transitioning to **`'APPROVED'`** requires explicit `anonymized_by`, `anonymized_at`, and `anonymization_artifact_sha256` (enforced by SQLite `CHECK`), and `trg_episode_release_gate` blocks episode export unless `anonymization_status = 'APPROVED'`.
- **Source-Tiered `TemporalFactLedger`:** Extracts `{fact_id, datetime_iso, event_summary, physical_clues[], location_text, source_type, citation_locator, hedging_required}` via `DeepSeek-V4.1-Flash-1017` + `DeepSeek-V4-Pro-0813`. `"news_report"` facts remain locked behind `trg_fact_news_hedging_insert/update`.

## 3. Early Illustrative 2K Plate Generation & Explicit Anchor Lock (`F-04`, `F-05`)

To keep Part 1 independent of Part 2 while preserving strict journalistic honesty:
1. **Clearly Labeled Illustrative Reconstruction (`F-05`):** Generated 2K charcoal-parchment room plates are stored in `still_assets` with **`is_illustrative_reconstruction = 1`** and mandatory disclaimer **`ILLUSTRATIVE RECONSTRUCTION — NOT CRIME SCENE PHOTO`**. They serve strictly as visual storytelling aids illustrating cited primary-record details—NEVER as verified forensic layouts or photographic evidence!
2. **External-Margin `10x10` Grid & Explicit Lock State (`F-04`, `F-09`):**
   - Agent 2 calls the official Gemini Image API to generate clean `>= 2048px` (`2560x1440` target) monochrome charcoal plates, stamps the temporary external-margin `A–J / 1–10` inspection border, runs `grid-grounding-vision@2`, and writes `spatial_anchors` rows starting in **`lock_status = 'DRAFT'`** referencing `still_assets(still_2k_id)` and `fact_ledger(fact_id)`.
   - After automated bounds/overlap checks and human/editorial verification (required for any scene that could be mistaken for a historical reconstruction), anchors transition explicitly `DRAFT -> IN_REVIEW -> LOCKED` with `locked_by`, `locked_at`, and `still_asset_sha256`.
3. **Topology-Safe Phrasing:** Scripts use non-misleading, record-anchored language (*"according to the affidavit, an overturned table was noted near the entryway"*) rather than implying the generated image depicts exact measured room geometry.
