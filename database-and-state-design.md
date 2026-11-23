# Database & State Design (`pipeline.db` v4 + `telemetry.db`)

All durable state, multi-provider budget admission control, versioned `ScenePlan` contracts, offline-test `$0` guards, crash reconciliation, legal holds, and human release sign-offs live in **`pipeline.db`** (SQLite WAL mode), paired strictly with non-authoritative analytics telemetry in **`telemetry.db`**. Schema DDL: [schema/pipeline.sql](schema/pipeline.sql), [schema/telemetry.sql](schema/telemetry.sql), [schema/queries.sql](schema/queries.sql), [schema/schema-test.js](schema/schema-test.js). Diagram: [database-and-state-design.mmd](database-and-state-design.mmd).

## 1. Runtime Version Pin, Single-Host Storage & Security Boundary (`F-19`, `F-22`)

- **Minimum SQLite Version Enforced at Startup (`F-22`):** `sqlite3.sqlite_version_info >= (3, 51, 3)` (fixing SQLite's documented WAL-reset bug).
- **Local Host Filesystem Only (`F-22`):** Reject SMB/NFS/UNC paths at startup; run verified daily `VACUUM INTO` hot backups (`PRAGMA integrity_check`) + `< 25 GB` warn / `< 10 GB` pause disk watermarks.
- **Python Sole Writer & Loopback FastAPI Security (`F-19`):** Short `BEGIN IMMEDIATE` transactions (`WAL`, `synchronous=FULL`, `busy_timeout=5000`); loopback-only `127.0.0.1` FastAPI with 256-bit `X-Local-Auth-Token` (`0600`), localhost CORS, canonical upload path containment, and `audit_log`.

## 2. Canonical v4 Schema Additions (`F-01`, `F-02`, `F-05`, Additional Check #3)

| Table / Trigger | Purpose & Audit Remediation |
|---|---|
| `monthly_budget_ledger` + `provider_spend_reservations` + `trg_offline_test_zero_spend_guard` + `trg_provider_global_budget_cap_guard` | **F-01 & F-02:** Blocks ANY `OFFLINE_TEST` spend `> $0`; enforces per-episode video caps (`$10.40`), per-provider monthly caps (including conservative `$38/mo` `0%`-cache DeepSeek projection), AND the global **`$135/mo` `ALL_PROVIDERS` cap** transactionally across ALL providers! |
| `scene_plans` + `trg_scene_plan_invalidate_on_narration_edit` + updated `trg_episode_release_gate` | **F-05 & F-06:** Versioned creative/editorial contract per scene (`story_purpose`, `intended_audience_effect`, `approved_narration_text`, `cited_fact_ids_json`, `visual_concept`, `visual_prompt`, `expected_output_summary`, `transition_spec_json`, `sound_cues_json`, `edit_instructions`, `acceptance_criteria_json`, `narration_version_sha256`, `asset_version_sha256`, `plan_status`). Narration edits auto-invalidate dependent visuals (`STALE_NEEDS_REAPPROVAL`) and block release! |
| `cases`, `still_assets`, `spatial_anchors`, `foia_media_assets`, `voice_segments`, `scenes`, `flow_jobs`, `release_approvals`, `episode_analytics`, `motif_registry` | **F-03..F-20:** All v3 protections carried forward (`INSERT+UPDATE` disposition quarantine, `NOT_STARTED->APPROVED` anonymization, `DRAFT->LOCKED` anchors, illustrative reconstruction flags, non-overlap triggers, `UNIQUE(episode_id, scene_id)` + `UNKNOWN_RECONCILE`, fail-closed QA, 5 human gates, honest `UNKNOWN` analytics, non-null 30d full-field YT purge). |
| `telemetry.sql` (`total_input_tokens` + `CHECK`) | **Additional Check #3:** Clarified `total_input_tokens` semantics (`cached_input_tokens <= total_input_tokens` strictly enforced by SQL `CHECK`) so impossible accounting states fail immediately. |
