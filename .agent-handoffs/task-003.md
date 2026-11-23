# Task 003 — Frozen SQLite schemas v4

Branch: `task/003-frozen-sqlite-schemas`

SQL was not changed. `schema/pipeline.sql` (v4), `schema/telemetry.sql`, and `schema/queries.sql` loaded as they already existed. No statement was skipped.

## Verification

- Node `v24.16.0` has `node:sqlite`. `node schema/schema-test.js` exited 0: **12/12 schema scenarios passed.**
- Python `3.12.10` links SQLite **3.49.1**, which is older than the documented 3.51.3 WAL pin. The full DDL still loaded (`STRICT`, `RETURNING`, triggers). `python -m pytest schema/schema_test.py -q` : **12 passed** in 1.28s. `uv` is not installed on this machine, so pytest was the stdlib-adjacent `python -m pytest` run. One warning came from an unrelated `dash` plugin already on the interpreter, not from these tests.

## Assertion count

`schema/schema-test.js` executes **46** assertions:

- **42** `assert.*` calls inside the 12 scenario bodies
- **4** runs of the `extractQuery` `assert.ok` (one source line) for `reserve_provider_budget`, `atomic_refill_and_reserve_daily_account_credits`, `purge_expired_yt_api_records`, and `consume_quota_bucket`

`schema/schema_test.py` ports all **46**. It adds **4** checks the JS bodies do not make, inside the same scenario functions, because those v4 objects already exist:

- Scenario 6: `is_illustrative_reconstruction` defaults to `1`, disclaimer text is `ILLUSTRATIVE RECONSTRUCTION — NOT CRIME SCENE PHOTO`, and setting the flag to `0` is rejected
- Scenario 7: `trg_flow_two_strike_breaker` raises `LAW_3_BREAKER` once `attempts_used >= 2`

Python therefore checks **50** conditions across **12** pytest tests.

Scenario 12 matches the JS quota guard: seeded `yt_search.daily_limit` is **100** (`+60` succeeds, `+45` returns no row because 105 exceeds 100). A separate 15-call `yt_search` floor is application logic in Task 007, not a v4 table, column, or CHECK, so it was not added to the SQL and not asserted as a schema limit.

## Scenario map (12/12)

1. Telemetry `cached_input_tokens <= total_input_tokens`
2. `schema_version` 4, `gemini-omni-1.2-flash`, `whisperx-local`, offline spend cap `0`, 4 MVP motifs
3. `OFFLINE_TEST` zero-spend guard and global `$135/mo` `ALL_PROVIDERS` cap
4. ScenePlan stale-on-edit and 5-gate release
5. Disposition guard on INSERT and UPDATE, quarantine plus approval revoke
6. `anonymization_status` `NOT_STARTED`, `spatial_anchors.lock_status` `DRAFT`, illustrative watermark
7. Unique `(episode_id, scene_id)`, prompt-mode frame rules, 2-strike breaker
8. Daily account credits lock for 24h+5m, then refill
9. Voice-segment kind check and non-overlap
10. YouTube TTL required, 30-day purge, `adsense_status` `UNKNOWN`
11. `RESTRICTED_NO_REUSE` cannot be approved; ASR disagreement row is stored
12. Quota daily limit and `RULE_09` news-report hedging
