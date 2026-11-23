-- Automated True-Crime Pipeline · telemetry.db · schema version 3
-- Non-authoritative operational telemetry ONLY (latency, cache-hit rates, render timings).
-- NEVER used as the source of truth for paid spend caps or crash-safe idempotency
-- (those live strictly in pipeline.db `provider_spend_reservations` & `flow_jobs`).
-- Never shares a transaction with pipeline.db.

CREATE TABLE api_token_usage (
  id                  INTEGER PRIMARY KEY AUTOINCREMENT,
  episode_id          TEXT,
  agent_name          TEXT NOT NULL,
  model_id            TEXT NOT NULL,
  is_off_peak         INTEGER NOT NULL DEFAULT 0 CHECK (is_off_peak IN (0,1)),
  -- Explicit semantics (Audit Security/Cost Check #3):
  -- `total_input_tokens` = total prompt input tokens (cached + uncached); therefore cached_input_tokens <= total_input_tokens ALWAYS holds.
  total_input_tokens  INTEGER NOT NULL DEFAULT 0 CHECK (total_input_tokens >= 0),
  cached_input_tokens INTEGER NOT NULL DEFAULT 0 CHECK (cached_input_tokens >= 0 AND cached_input_tokens <= total_input_tokens),
  output_tokens       INTEGER NOT NULL DEFAULT 0 CHECK (output_tokens >= 0),
  vision_image_count  INTEGER NOT NULL DEFAULT 0 CHECK (vision_image_count >= 0),
  audio_tokens        INTEGER NOT NULL DEFAULT 0 CHECK (audio_tokens >= 0),
  cost_micro_usd      INTEGER NOT NULL DEFAULT 0 CHECK (cost_micro_usd >= 0),
  latency_ms          INTEGER NOT NULL DEFAULT 0 CHECK (latency_ms >= 0),
  created_at          INTEGER NOT NULL
) STRICT;

CREATE INDEX idx_telemetry_tokens_episode ON api_token_usage(episode_id, created_at);

CREATE TABLE render_timings (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  episode_id      TEXT NOT NULL,
  scene_id        TEXT NOT NULL,
  visual_engine   TEXT NOT NULL,
  duration_ms     INTEGER NOT NULL CHECK (duration_ms >= 0),
  wall_time_ms    INTEGER NOT NULL CHECK (wall_time_ms >= 0),
  local_re_render INTEGER NOT NULL DEFAULT 0 CHECK (local_re_render IN (0,1)),
  created_at      INTEGER NOT NULL
) STRICT;

CREATE TABLE batch_desk_events (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  account_id  TEXT NOT NULL,
  flow_job_id TEXT NOT NULL,
  event_type  TEXT NOT NULL CHECK (event_type IN ('shift_open','prompt_copied','drop_received','qa_pass','qa_fail','circuit_breaker_tripped','shift_close')),
  detail_json TEXT,
  created_at  INTEGER NOT NULL
) STRICT;
