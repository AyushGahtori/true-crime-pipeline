-- Automated True-Crime Pipeline · pipeline.db · schema version 3
-- Sole SQLite WAL Writer: Python Backend (apps/batch_desk_ui uses FastAPI HTTP/WS only).
--
-- Runtime & Storage Requirements (F-22):
--   * Minimum SQLite runtime version: >= 3.51.3 (fixes WAL-reset concurrency bug; verified at app startup).
--   * Must reside on local host filesystem (NTFS / ext4 / APFS); reject SMB/NFS/UNC paths at startup.
--   * Connection Pragmas:
--       PRAGMA journal_mode = WAL;
--       PRAGMA synchronous = FULL;
--       PRAGMA foreign_keys = ON;
--       PRAGMA busy_timeout = 5000;

--------------------------------------------------------------------------------
-- 0. Metadata, Audit Log & Lookup Vocabularies
--------------------------------------------------------------------------------

CREATE TABLE meta (
  key   TEXT PRIMARY KEY,
  value TEXT NOT NULL
) STRICT, WITHOUT ROWID;

INSERT INTO meta VALUES
  ('schema_version', '3'),
  ('min_sqlite_version', '3.51.3'),
  ('primary_video_model', 'gemini-omni-1.2-flash'),
  ('primary_video_api', 'gemini-interactions-api');

-- Immutable audit trail for security-sensitive mutations (F-06, F-19)
CREATE TABLE audit_log (
  audit_seq    INTEGER PRIMARY KEY AUTOINCREMENT,
  actor_id     TEXT NOT NULL,
  action_type  TEXT NOT NULL,
  entity_type  TEXT NOT NULL,
  entity_id    TEXT NOT NULL,
  detail_json  TEXT NOT NULL DEFAULT '{}',
  created_at   INTEGER NOT NULL
) STRICT;

CREATE TABLE episode_states (
  state       TEXT PRIMARY KEY,
  seq_order   INTEGER NOT NULL UNIQUE,
  is_terminal INTEGER NOT NULL DEFAULT 0 CHECK (is_terminal IN (0,1))
) STRICT, WITHOUT ROWID;

INSERT INTO episode_states VALUES
  ('QUEUED', 1, 0),
  ('SCOUTED', 2, 0),
  ('EVIDENCE_AND_2K_LOCKED', 3, 0),
  ('COMPLIANCE_PASSED', 4, 0),
  ('VOICE_READY', 5, 0),
  ('MANIFEST_LINTED', 6, 0),
  ('CODE_RENDERED', 7, 0),
  ('AWAITING_FLOW_BATCH', 8, 0),
  ('POST_FLOW_PROCESSING', 9, 0),
  ('MASTERED', 10, 0),
  ('PENDING_HUMAN_SIGNOFF', 11, 0),
  ('READY_TO_UPLOAD', 12, 0),
  ('PUBLISHED', 13, 1),
  ('QUARANTINED_LEGAL_HOLD', 89, 0),
  ('REJECTED_KILL_SWITCH', 90, 1),
  ('ABORTED_COPYCAT_WAVE', 91, 1);

CREATE TABLE visual_engines (
  engine       TEXT PRIMARY KEY,
  paid_video   INTEGER NOT NULL CHECK (paid_video IN (0,1))
) STRICT, WITHOUT ROWID;

INSERT INTO visual_engines VALUES
  ('CODE_STICKMAN', 0),
  ('STILL_2K_PANZOOM', 0),
  ('AUDIO_EVIDENCE_CARD', 0),
  ('FOIA_REAL_FOOTAGE', 0),
  ('FLOW_HERO_VIDEO', 1);

-- Explicit crash-safe lifecycle for external paid video jobs (F-10)
CREATE TABLE flow_job_states (
  state       TEXT PRIMARY KEY,
  is_terminal INTEGER NOT NULL DEFAULT 0 CHECK (is_terminal IN (0,1))
) STRICT, WITHOUT ROWID;

INSERT INTO flow_job_states VALUES
  ('PENDING', 0),
  ('SUBMITTING', 0),
  ('RUNNING', 0),
  ('UNKNOWN_RECONCILE', 0),
  ('PENDING_MANUAL_SPOT_CHECK', 0),
  ('STRIKE_1_RETRY_SAFE', 0),
  ('ACCEPTED', 1),
  ('FAILED_TERMINAL', 1),
  ('SWITCHED_TO_FALLBACK', 1);

CREATE TABLE cold_open_archetypes (
  archetype TEXT PRIMARY KEY
) STRICT, WITHOUT ROWID;

INSERT INTO cold_open_archetypes VALUES
  ('911_CALL_IN_MEDIA_RES'),
  ('SINGLE_FORENSIC_ANOMALY'),
  ('ALIBI_THAT_CRACKED'),
  ('CHRONOLOGICAL_COUNTDOWN');

-- Authoritative Motif Registry V1 (F-16: Single Source of Truth)
CREATE TABLE motif_registry (
  motif_component TEXT PRIMARY KEY,
  owner_package   TEXT NOT NULL CHECK (owner_package IN ('render_catalog','crime_scene_2k','flow_adapter')),
  is_mvp_4        INTEGER NOT NULL DEFAULT 0 CHECK (is_mvp_4 IN (0,1))
) STRICT, WITHOUT ROWID;

INSERT INTO motif_registry VALUES
  -- Authoritative 4-Motif MVP Slice (F-16)
  ('StickmanStage',          'render_catalog', 1),
  ('AudioEvidenceCard',      'render_catalog', 1),
  ('RedactedDocReveal',      'render_catalog', 1),
  ('FoiaFootageFrame',       'render_catalog', 1),
  -- Extended Remotion 2D Catalog (V1 Full 12)
  ('TimelineScrubber',       'render_catalog', 0),
  ('AnimatedMapRoute',       'render_catalog', 0),
  ('CellTowerTriangulation', 'render_catalog', 0),
  ('SplitScreenComparison',  'render_catalog', 0),
  ('CaseBoardSpine',         'render_catalog', 0),
  ('QuotePullout',           'render_catalog', 0),
  ('EvidenceGridMatrix',     'render_catalog', 0),
  ('ChapterSlateTransition', 'render_catalog', 0),
  -- Dedicated Python 2K Illustrative Reconstruction Renderer (sole owner of 2K pan/zoom + callouts)
  ('Illustrative2KPanZoom',  'crime_scene_2k', 0),
  -- Dedicated Paid Video Generation Bridge (Gemini Omni 1.2 Flash Interactions API)
  ('HeroVideoBridge',        'flow_adapter',   0);

--------------------------------------------------------------------------------
-- 1. Agent 1 · YouTube Watchlist (Strict 30-Day ToS Retention), Quotas & SI
--------------------------------------------------------------------------------

CREATE TABLE quota_buckets (
  bucket_name      TEXT PRIMARY KEY,
  daily_limit      INTEGER NOT NULL CHECK (daily_limit > 0),
  used_today       INTEGER NOT NULL DEFAULT 0 CHECK (used_today >= 0),
  window_reset_at  INTEGER NOT NULL
) STRICT, WITHOUT ROWID;

INSERT INTO quota_buckets VALUES
  ('yt_search', 100, 0, 0),
  ('yt_general', 10000, 0, 0),
  ('yt_insert', 100, 0, 0),
  ('courtlistener', 125, 0, 0);

CREATE TABLE channels_watchlist (
  channel_id          TEXT PRIMARY KEY,
  uploads_playlist_id TEXT NOT NULL,
  channel_name        TEXT NOT NULL,
  subscriber_count    INTEGER NOT NULL CHECK (subscriber_count >= 0),
  median_20_views     INTEGER NOT NULL DEFAULT 0 CHECK (median_20_views >= 0),
  last_polled_at      INTEGER NOT NULL DEFAULT 0,
  yt_ttl_expires_at   INTEGER NOT NULL, -- Non-null 30-day refresh/delete SLA (F-20)
  discovered_via      TEXT NOT NULL DEFAULT 'SEED' CHECK (discovered_via IN ('SEED','SPILLOVER')),
  is_active           INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0,1))
) STRICT, WITHOUT ROWID;

CREATE TABLE outlier_candidates (
  candidate_id           TEXT PRIMARY KEY,
  track                  TEXT NOT NULL CHECK (track IN ('TRACK_A_OUTLIER','TRACK_B_FOIA_RADAR')),
  source_video_id        TEXT,
  source_channel_id      TEXT REFERENCES channels_watchlist(channel_id),
  views_count            INTEGER,
  outlier_ratio          REAL,
  saturation_index       INTEGER NOT NULL CHECK (saturation_index BETWEEN 0 AND 100),
  n_mega_excl            INTEGER NOT NULL DEFAULT 0,
  n_recent_excl          INTEGER NOT NULL DEFAULT 0,
  n_14d_excl             INTEGER NOT NULL DEFAULT 0,
  has_90d_200k_kill      INTEGER NOT NULL DEFAULT 0 CHECK (has_90d_200k_kill IN (0,1)),
  safe_title_ctr_ok      INTEGER NOT NULL DEFAULT 0 CHECK (safe_title_ctr_ok IN (0,1)),
  upgrade_axes_json      TEXT NOT NULL DEFAULT '[]',
  composite_score        REAL NOT NULL DEFAULT 0.0,
  seed_packet_json       TEXT NOT NULL,
  raw_yt_payload_json    TEXT,
  yt_data_purged_at      INTEGER,
  yt_ttl_expires_at      INTEGER,
  policy_kill_reason     TEXT,
  status                 TEXT NOT NULL CHECK (status IN ('CANDIDATE','GREENLIT','REJECTED','CONSUMED','EXPIRED_TOS_PURGED')),
  created_at             INTEGER NOT NULL,
  -- F-20: Every YouTube-sourced row MUST carry an explicit non-null 30-day expiry timestamp
  CHECK (track != 'TRACK_A_OUTLIER' OR yt_ttl_expires_at IS NOT NULL)
) STRICT;

CREATE TABLE saturation_checks (
  check_id          TEXT PRIMARY KEY,
  candidate_id      TEXT NOT NULL REFERENCES outlier_candidates(candidate_id),
  phase             TEXT NOT NULL CHECK (phase IN ('SCOUTING','PRE_RENDER_DAILY_RECHECK')),
  aliases_json      TEXT NOT NULL,
  n_mega_excl       INTEGER NOT NULL,
  n_recent_excl     INTEGER NOT NULL,
  n_14d_wave        INTEGER NOT NULL,
  si_score          INTEGER NOT NULL,
  sunk_cost_override INTEGER NOT NULL DEFAULT 0 CHECK (sunk_cost_override IN (0,1)),
  aborted           INTEGER NOT NULL DEFAULT 0 CHECK (aborted IN (0,1)),
  checked_at        INTEGER NOT NULL
) STRICT;

CREATE TABLE courtlistener_cache (
  cache_key    TEXT PRIMARY KEY,
  docket_id    TEXT,
  payload_json TEXT NOT NULL,
  fetched_at   INTEGER NOT NULL,
  expires_at   INTEGER NOT NULL
) STRICT, WITHOUT ROWID;

--------------------------------------------------------------------------------
-- 2. Agents 2 & 3 · Disposition Gate (INSERT+UPDATE), Anonymization States, Rights
--------------------------------------------------------------------------------

CREATE TABLE cases (
  case_id                       TEXT PRIMARY KEY,
  candidate_id                  TEXT REFERENCES outlier_candidates(candidate_id),
  defendant_name                TEXT NOT NULL,
  incident_year                 INTEGER NOT NULL,
  jurisdiction                  TEXT NOT NULL,
  docket_id                     TEXT,
  primary_record_verified       INTEGER NOT NULL DEFAULT 0 CHECK (primary_record_verified IN (0,1)),
  verification_source           TEXT NOT NULL,
  disposition_status            TEXT NOT NULL CHECK (disposition_status IN ('AFFIRMED','STANDING_CONVICTION','REVERSED','VACATED','ACQUITTED','PENDING')),
  conviction_confirmed          INTEGER NOT NULL DEFAULT 0 CHECK (conviction_confirmed IN (0,1)),
  -- F-04: Explicit reviewable anonymization state (NEVER default-approved!)
  anonymization_status          TEXT NOT NULL DEFAULT 'NOT_STARTED' CHECK (anonymization_status IN ('NOT_STARTED','IN_REVIEW','APPROVED')),
  anonymized_by                 TEXT,
  anonymized_at                 INTEGER,
  anonymization_artifact_sha256 TEXT,
  created_at                    INTEGER NOT NULL,
  updated_at                    INTEGER NOT NULL,
  CHECK (anonymization_status != 'APPROVED' OR (anonymized_by IS NOT NULL AND anonymized_at IS NOT NULL AND anonymization_artifact_sha256 IS NOT NULL))
) STRICT;

-- F-03: Guard conviction confirmation on BOTH INSERT and UPDATE
CREATE TRIGGER trg_case_disposition_guard_insert
BEFORE INSERT ON cases
WHEN NEW.conviction_confirmed = 1 AND NEW.disposition_status NOT IN ('AFFIRMED','STANDING_CONVICTION')
BEGIN
  SELECT RAISE(ABORT, 'LEGAL_DISPOSITION: Cannot confirm conviction when appellate disposition is not AFFIRMED or STANDING_CONVICTION');
END;

CREATE TRIGGER trg_case_disposition_guard_update
BEFORE UPDATE OF disposition_status, conviction_confirmed ON cases
WHEN NEW.conviction_confirmed = 1 AND NEW.disposition_status NOT IN ('AFFIRMED','STANDING_CONVICTION')
BEGIN
  SELECT RAISE(ABORT, 'LEGAL_DISPOSITION: Cannot keep conviction_confirmed=1 after disposition_status changed outside AFFIRMED/STANDING_CONVICTION');
END;

-- F-03: Automatically quarantine downstream episodes & revoke approvals if a case status flips adversely
CREATE TRIGGER trg_case_disposition_quarantine
AFTER UPDATE OF disposition_status ON cases
WHEN NEW.disposition_status IN ('REVERSED','VACATED','ACQUITTED','PENDING')
  AND OLD.disposition_status IN ('AFFIRMED','STANDING_CONVICTION')
BEGIN
  UPDATE episodes
  SET state = 'QUARANTINED_LEGAL_HOLD',
      updated_at = NEW.updated_at
  WHERE case_id = NEW.case_id
    AND state NOT IN ('REJECTED_KILL_SWITCH','ABORTED_COPYCAT_WAVE');

  UPDATE release_approvals
  SET status = 'REVOKED',
      notes = 'Auto-revoked: upstream case disposition changed to ' || NEW.disposition_status
  WHERE episode_id IN (SELECT episode_id FROM episodes WHERE case_id = NEW.case_id)
    AND status = 'APPROVED';
END;

CREATE TABLE primary_documents (
  doc_id           TEXT PRIMARY KEY,
  case_id          TEXT NOT NULL REFERENCES cases(case_id),
  source_domain    TEXT NOT NULL,
  source_url       TEXT NOT NULL,
  doc_type         TEXT NOT NULL CHECK (doc_type IN ('court_ruling','police_affidavit','foia_package','gov_release','news_text_only')),
  raw_text_sha256  TEXT NOT NULL,
  local_text_path  TEXT NOT NULL,
  fetched_at       INTEGER NOT NULL
) STRICT;

CREATE TABLE fact_ledger (
  fact_id             TEXT PRIMARY KEY,
  case_id             TEXT NOT NULL REFERENCES cases(case_id),
  datetime_iso        TEXT NOT NULL,
  event_summary       TEXT NOT NULL,
  physical_clues_json TEXT NOT NULL DEFAULT '[]',
  location_text       TEXT NOT NULL,
  source_type         TEXT NOT NULL CHECK (source_type IN ('court_ruling','police_affidavit','news_report')),
  source_doc_id       TEXT NOT NULL REFERENCES primary_documents(doc_id),
  citation_locator    TEXT NOT NULL,
  hedging_required    INTEGER NOT NULL CHECK (hedging_required IN (0,1)),
  contradicts_json    TEXT NOT NULL DEFAULT '[]'
) STRICT;

CREATE TRIGGER trg_fact_news_hedging_insert
BEFORE INSERT ON fact_ledger
WHEN NEW.source_type = 'news_report' AND NEW.hedging_required = 0
BEGIN
  SELECT RAISE(ABORT, 'RULE_09: news_report fact must have hedging_required = 1');
END;

CREATE TRIGGER trg_fact_news_hedging_update
BEFORE UPDATE ON fact_ledger
WHEN NEW.source_type = 'news_report' AND NEW.hedging_required = 0
BEGIN
  SELECT RAISE(ABORT, 'RULE_09: news_report fact must keep hedging_required = 1');
END;

-- F-14 & F-15: Per-asset component rights provenance (FOIA access != reuse permission) + honest ASR disagreement metric
CREATE TABLE foia_media_assets (
  asset_id                    TEXT PRIMARY KEY,
  case_id                     TEXT NOT NULL REFERENCES cases(case_id),
  source_domain               TEXT NOT NULL,
  source_url                  TEXT NOT NULL,
  creator_entity              TEXT NOT NULL,
  rights_holder               TEXT NOT NULL,
  license_basis               TEXT NOT NULL CHECK (license_basis IN (
                                'US_FED_EMPLOYEE_17USC105',
                                'STATE_PUBLIC_RECORD_PERMITTED',
                                'CC0_PUBLIC_DOMAIN',
                                'EXPLICIT_LICENSE_GRANT',
                                'FAIR_USE_REVIEW_REQUIRED',
                                'RESTRICTED_NO_REUSE'
                              )),
  permitted_uses_json         TEXT NOT NULL DEFAULT '[]',
  contains_third_party_attach INTEGER NOT NULL DEFAULT 0 CHECK (contains_third_party_attach IN (0,1)),
  rights_review_status        TEXT NOT NULL DEFAULT 'NOT_STARTED' CHECK (rights_review_status IN ('NOT_STARTED','IN_REVIEW','APPROVED','REJECTED')),
  rights_reviewed_by          TEXT,
  rights_reviewed_at          INTEGER,
  media_kind                  TEXT NOT NULL CHECK (media_kind IN ('bodycam_mp4','dashcam_mp4','court_mp4','call_911_wav','interrogation_wav','photo_cc0')),
  raw_path                    TEXT NOT NULL,
  scrubbed_path               TEXT,
  normalized_cfr_30fps_48k    INTEGER NOT NULL DEFAULT 0 CHECK (normalized_cfr_30fps_48k IN (0,1)),
  music_detected              INTEGER NOT NULL DEFAULT 0 CHECK (music_detected IN (0,1)),
  demucs_applied              INTEGER NOT NULL DEFAULT 0 CHECK (demucs_applied IN (0,1)),
  asr_hypothesis_disagreement REAL NOT NULL DEFAULT 0.0 CHECK (asr_hypothesis_disagreement >= 0.0),
  human_audio_review_required INTEGER NOT NULL DEFAULT 0 CHECK (human_audio_review_required IN (0,1)),
  watermark_clean             INTEGER NOT NULL DEFAULT 0 CHECK (watermark_clean IN (0,1)),
  visual_pii_blurred          INTEGER NOT NULL DEFAULT 0 CHECK (visual_pii_blurred IN (0,1)),
  spoken_pii_bleeped          INTEGER NOT NULL DEFAULT 0 CHECK (spoken_pii_bleeped IN (0,1)),
  profanity_intervals_json    TEXT NOT NULL DEFAULT '[]',
  sha256                      TEXT,
  CHECK (rights_review_status != 'APPROVED' OR (rights_reviewed_by IS NOT NULL AND rights_reviewed_at IS NOT NULL AND license_basis != 'RESTRICTED_NO_REUSE'))
) STRICT;

CREATE TABLE compliance_audits (
  audit_id                   TEXT PRIMARY KEY,
  case_id                    TEXT NOT NULL REFERENCES cases(case_id),
  provenance_whitelist_ok    INTEGER NOT NULL CHECK (provenance_whitelist_ok IN (0,1)),
  that_vs_how_passed         INTEGER NOT NULL CHECK (that_vs_how_passed IN (0,1)),
  anti_legal_persona_passed  INTEGER NOT NULL CHECK (anti_legal_persona_passed IN (0,1)),
  first_30s_adsense_safe     INTEGER NOT NULL CHECK (first_30s_adsense_safe IN (0,1)),
  spoken_pii_audit_passed    INTEGER NOT NULL CHECK (spoken_pii_audit_passed IN (0,1)),
  altered_content_disclosure INTEGER NOT NULL CHECK (altered_content_disclosure IN (0,1)),
  audited_at                 INTEGER NOT NULL
) STRICT;

--------------------------------------------------------------------------------
-- 3. Conveyor Episodes, Illustrative 2K Stills, Anchors, Segmented Voice & Scenes
--------------------------------------------------------------------------------

CREATE TABLE episodes (
  episode_id                 TEXT PRIMARY KEY,
  case_id                    TEXT NOT NULL REFERENCES cases(case_id),
  state                      TEXT NOT NULL REFERENCES episode_states(state),
  flow_backend_mode          TEXT NOT NULL DEFAULT 'GEMINI_OMNI_INTERACTIONS'
                             CHECK (flow_backend_mode IN ('GEMINI_OMNI_INTERACTIONS','VERTEX_VEO_ENTERPRISE','HUMAN_BATCH_DESK')),
  cold_open_archetype        TEXT NOT NULL REFERENCES cold_open_archetypes(archetype),
  turning_point_count        INTEGER NOT NULL DEFAULT 0,
  target_duration_ms         INTEGER NOT NULL DEFAULT 1200000,
  total_master_ms            INTEGER NOT NULL DEFAULT 0,
  -- F-02 & F-18: Durable USD budget cap in micro-USD (default $10.40 = $8.00 base + $2.40 dynamic escrow for 10x8s Omni 1.2 Flash 720p)
  video_budget_cap_micro_usd INTEGER NOT NULL DEFAULT 10400000 CHECK (video_budget_cap_micro_usd >= 0),
  max_hero_clips             INTEGER NOT NULL DEFAULT 10 CHECK (max_hero_clips BETWEEN 0 AND 10),
  max_hero_duration_sec      INTEGER NOT NULL DEFAULT 80 CHECK (max_hero_duration_sec BETWEEN 0 AND 80),
  timeline_validated_sha256  TEXT,
  altered_content_disclosure INTEGER NOT NULL DEFAULT 1 CHECK (altered_content_disclosure IN (0,1)),
  thumbnail_mood_vec         TEXT,
  ready_pack_dir             TEXT,
  ready_bundle_sha256        TEXT,
  updated_at                 INTEGER NOT NULL,
  created_at                 INTEGER NOT NULL
) STRICT;

CREATE TABLE case_bibles (
  episode_id        TEXT PRIMARY KEY REFERENCES episodes(episode_id),
  style_dna_json    TEXT NOT NULL,
  characters_json   TEXT NOT NULL,
  locked_at         INTEGER NOT NULL
) STRICT, WITHOUT ROWID;

-- F-05 & F-09: Dedicated 2K still assets table enforcing illustrative-reconstruction labeling & FK target
CREATE TABLE still_assets (
  still_2k_id                    TEXT PRIMARY KEY,
  episode_id                     TEXT NOT NULL REFERENCES episodes(episode_id),
  asset_path                     TEXT NOT NULL,
  asset_sha256                   TEXT NOT NULL,
  width_px                       INTEGER NOT NULL CHECK (width_px >= 1920),
  height_px                      INTEGER NOT NULL CHECK (height_px >= 1080),
  is_illustrative_reconstruction INTEGER NOT NULL DEFAULT 1 CHECK (is_illustrative_reconstruction = 1),
  disclaimer_label_text          TEXT NOT NULL DEFAULT 'ILLUSTRATIVE RECONSTRUCTION — NOT CRIME SCENE PHOTO',
  created_at                     INTEGER NOT NULL
) STRICT;

-- F-04 & F-09: Explicit lock workflow + FK to still_assets + strict A1..J10 grid_cell CHECK
CREATE TABLE spatial_anchors (
  anchor_id            TEXT PRIMARY KEY,
  episode_id           TEXT NOT NULL REFERENCES episodes(episode_id),
  still_2k_id          TEXT NOT NULL REFERENCES still_assets(still_2k_id),
  clue_name            TEXT NOT NULL,
  cited_fact_id        TEXT REFERENCES fact_ledger(fact_id),
  grid_cell            TEXT NOT NULL CHECK (grid_cell GLOB '[A-J][1-9]' OR grid_cell GLOB '[A-J]10'),
  span_cols            REAL NOT NULL DEFAULT 1.0 CHECK (span_cols > 0.0 AND span_cols <= 10.0),
  span_rows            REAL NOT NULL DEFAULT 1.0 CHECK (span_rows > 0.0 AND span_rows <= 10.0),
  x_px                 INTEGER NOT NULL CHECK (x_px >= 0),
  y_px                 INTEGER NOT NULL CHECK (y_px >= 0),
  target_zoom          REAL NOT NULL DEFAULT 2.5 CHECK (target_zoom BETWEEN 1.0 AND 3.8),
  travel_axis          TEXT CHECK (travel_axis IN ('L_TO_R','R_TO_L','STATIC')),
  lock_status          TEXT NOT NULL DEFAULT 'DRAFT' CHECK (lock_status IN ('DRAFT','IN_REVIEW','LOCKED')),
  locked_by            TEXT,
  locked_at            INTEGER,
  still_asset_sha256   TEXT,
  CHECK (lock_status != 'LOCKED' OR (locked_by IS NOT NULL AND locked_at IS NOT NULL AND still_asset_sha256 IS NOT NULL))
) STRICT;

-- F-09: Kind-specific media requirements & non-overlap triggers on voice_segments
CREATE TABLE voice_segments (
  segment_id      TEXT PRIMARY KEY,
  episode_id      TEXT NOT NULL REFERENCES episodes(episode_id),
  seq_index       INTEGER NOT NULL CHECK (seq_index >= 1),
  segment_kind    TEXT NOT NULL CHECK (segment_kind IN ('NARRATION','FOIA_AUDIO_SLOT','TWIST_PAD')),
  start_ms        INTEGER NOT NULL CHECK (start_ms >= 0),
  end_ms          INTEGER NOT NULL CHECK (end_ms > start_ms),
  audio_path      TEXT,
  foia_asset_id   TEXT REFERENCES foia_media_assets(asset_id),
  UNIQUE (episode_id, seq_index),
  CHECK (
    (segment_kind = 'NARRATION' AND audio_path IS NOT NULL)
    OR (segment_kind = 'FOIA_AUDIO_SLOT' AND foia_asset_id IS NOT NULL)
    OR (segment_kind = 'TWIST_PAD')
  )
) STRICT;

CREATE TRIGGER trg_voice_segments_no_overlap_insert
BEFORE INSERT ON voice_segments
WHEN EXISTS (
  SELECT 1 FROM voice_segments vs
  WHERE vs.episode_id = NEW.episode_id
    AND NEW.start_ms < vs.end_ms
    AND NEW.end_ms > vs.start_ms
)
BEGIN
  SELECT RAISE(ABORT, 'TIMELINE_OVERLAP: voice_segments intervals must not overlap within an episode');
END;

CREATE TRIGGER trg_voice_segments_no_overlap_update
BEFORE UPDATE OF start_ms, end_ms, episode_id ON voice_segments
WHEN EXISTS (
  SELECT 1 FROM voice_segments vs
  WHERE vs.episode_id = NEW.episode_id
    AND vs.segment_id != NEW.segment_id
    AND NEW.start_ms < vs.end_ms
    AND NEW.end_ms > vs.start_ms
)
BEGIN
  SELECT RAISE(ABORT, 'TIMELINE_OVERLAP: updated voice_segments interval overlaps an existing segment');
END;

CREATE TABLE scenes (
  scene_id             TEXT PRIMARY KEY,
  episode_id           TEXT NOT NULL REFERENCES episodes(episode_id),
  seq_index            INTEGER NOT NULL CHECK (seq_index >= 1),
  act_number           INTEGER NOT NULL CHECK (act_number IN (1,2,3)),
  visual_engine        TEXT NOT NULL REFERENCES visual_engines(engine),
  motif_component      TEXT NOT NULL REFERENCES motif_registry(motif_component),
  start_ms             INTEGER NOT NULL CHECK (start_ms >= 0),
  end_ms               INTEGER NOT NULL CHECK (end_ms > start_ms),
  emotional_peak_score REAL NOT NULL DEFAULT 0.0,
  timeline_spec_json   TEXT NOT NULL,
  fallback_spec_json   TEXT,
  rendered_mp4_path    TEXT,
  rendered_sha256      TEXT,
  UNIQUE (episode_id, seq_index)
) STRICT;

CREATE TRIGGER trg_scenes_no_overlap_insert
BEFORE INSERT ON scenes
WHEN EXISTS (
  SELECT 1 FROM scenes s
  WHERE s.episode_id = NEW.episode_id
    AND NEW.start_ms < s.end_ms
    AND NEW.end_ms > s.start_ms
)
BEGIN
  SELECT RAISE(ABORT, 'TIMELINE_OVERLAP: scenes intervals must not overlap within an episode');
END;

CREATE TRIGGER trg_scenes_no_overlap_update
BEFORE UPDATE OF start_ms, end_ms, episode_id ON scenes
WHEN EXISTS (
  SELECT 1 FROM scenes s
  WHERE s.episode_id = NEW.episode_id
    AND s.scene_id != NEW.scene_id
    AND NEW.start_ms < s.end_ms
    AND NEW.end_ms > s.start_ms
)
BEGIN
  SELECT RAISE(ABORT, 'TIMELINE_OVERLAP: updated scene interval overlaps an existing scene');
END;

CREATE TABLE published_entropy_history (
  episode_id            TEXT PRIMARY KEY REFERENCES episodes(episode_id),
  cold_open_archetype   TEXT NOT NULL REFERENCES cold_open_archetypes(archetype),
  turning_point_count   INTEGER NOT NULL CHECK (turning_point_count >= 3),
  thumbnail_mood_vec    TEXT NOT NULL,
  published_at          INTEGER NOT NULL
) STRICT, WITHOUT ROWID;

--------------------------------------------------------------------------------
-- 4. External Video Jobs (Idempotent, T2V/F2V, Crash-Safe), Budget Reservations & Optional Accounts
--------------------------------------------------------------------------------

CREATE TABLE google_accounts (
  account_id               TEXT PRIMARY KEY,
  label                    TEXT NOT NULL,
  monthly_credits_left     INTEGER NOT NULL DEFAULT 1000 CHECK (monthly_credits_left >= 0),
  daily_credits_cap        INTEGER NOT NULL DEFAULT 50 CHECK (daily_credits_cap > 0),
  daily_credits_left       INTEGER NOT NULL DEFAULT 50 CHECK (daily_credits_left >= 0),
  first_daily_spend_utc_ms INTEGER NOT NULL DEFAULT 0,
  next_daily_reset_utc_ms  INTEGER NOT NULL DEFAULT 0, -- first_daily_spend + 86400000 + 300000 (24h+5m guard)
  nano_pro_daily_left      INTEGER NOT NULL DEFAULT 100 CHECK (nano_pro_daily_left >= 0),
  upscale_2k_daily_left    INTEGER NOT NULL DEFAULT 200 CHECK (upscale_2k_daily_left >= 0)
) STRICT, WITHOUT ROWID;

INSERT INTO google_accounts VALUES
  ('acct_1', 'Optional Pro #1', 1000, 50, 50, 0, 0, 100, 200),
  ('acct_2', 'Optional Pro #2', 1000, 50, 50, 0, 0, 100, 200),
  ('acct_3', 'Optional Pro #3', 1000, 50, 50, 0, 0, 100, 200);

-- F-01, F-07, F-10: Supported Gemini Omni 1.2 Flash + nullable frames by prompt_mode + UNIQUE(episode_id, scene_id) + idempotency_key
CREATE TABLE flow_jobs (
  flow_job_id           TEXT PRIMARY KEY,
  episode_id            TEXT NOT NULL REFERENCES episodes(episode_id),
  scene_id              TEXT NOT NULL REFERENCES scenes(scene_id),
  idempotency_key       TEXT NOT NULL UNIQUE,
  assigned_account_id   TEXT REFERENCES google_accounts(account_id), -- Nullable for Headless API runs
  provider_route        TEXT NOT NULL DEFAULT 'GEMINI_OMNI_INTERACTIONS'
                        CHECK (provider_route IN ('GEMINI_OMNI_INTERACTIONS','VERTEX_VEO_ENTERPRISE','HUMAN_BATCH_DESK')),
  engine_model          TEXT NOT NULL DEFAULT 'gemini-omni-1.2-flash'
                        CHECK (engine_model IN ('gemini-omni-1.2-flash','vertex-veo-enterprise','manual-desk-video')),
  prompt_mode           TEXT NOT NULL CHECK (prompt_mode IN ('TEXT_TO_VIDEO','FIRST_FRAME','FIRST_AND_LAST_FRAME')),
  resolution            TEXT NOT NULL DEFAULT '720p' CHECK (resolution IN ('360p','720p','1080p','4k')),
  duration_bucket_sec   INTEGER NOT NULL CHECK (duration_bucket_sec BETWEEN 3 AND 15),
  variations            INTEGER NOT NULL DEFAULT 1 CHECK (variations = 1),
  estimated_micro_usd   INTEGER NOT NULL DEFAULT 800000 CHECK (estimated_micro_usd >= 0),
  estimated_credits     INTEGER NOT NULL DEFAULT 0 CHECK (estimated_credits >= 0),
  start_frame_png       TEXT,
  end_frame_png         TEXT,
  prompt_v1             TEXT NOT NULL,
  prompt_v2_safe        TEXT NOT NULL,
  fallback_spec_json    TEXT NOT NULL,
  provider_operation_id TEXT, -- Persisted in pipeline.db immediately upon dispatch for crash reconciliation (F-10)
  attempts_used         INTEGER NOT NULL DEFAULT 0 CHECK (attempts_used BETWEEN 0 AND 2),
  state                 TEXT NOT NULL DEFAULT 'PENDING' REFERENCES flow_job_states(state),
  output_asset_path     TEXT,
  updated_at            INTEGER NOT NULL,
  UNIQUE (episode_id, scene_id),
  -- F-07: Enforce frame presence strictly by prompt_mode & Omni 1.2 Flash 3..10s limit on 2-frame transitions
  CHECK (
    (prompt_mode = 'TEXT_TO_VIDEO' AND start_frame_png IS NULL AND end_frame_png IS NULL)
    OR (prompt_mode = 'FIRST_FRAME' AND start_frame_png IS NOT NULL AND end_frame_png IS NULL)
    OR (prompt_mode = 'FIRST_AND_LAST_FRAME' AND start_frame_png IS NOT NULL AND end_frame_png IS NOT NULL AND duration_bucket_sec BETWEEN 3 AND 10)
  )
) STRICT;

-- F-18: Durable, atomic USD budget-reservation ledger inside the single-writer state DB
CREATE TABLE budget_reservations (
  reservation_id      TEXT PRIMARY KEY,
  episode_id          TEXT NOT NULL REFERENCES episodes(episode_id),
  flow_job_id         TEXT NOT NULL REFERENCES flow_jobs(flow_job_id),
  attempt_number      INTEGER NOT NULL CHECK (attempt_number IN (1,2)),
  estimated_micro_usd INTEGER NOT NULL CHECK (estimated_micro_usd >= 0),
  actual_micro_usd    INTEGER CHECK (actual_micro_usd >= 0),
  status              TEXT NOT NULL CHECK (status IN ('RESERVED','COMMITTED','RELEASED','UNKNOWN_HOLD')),
  created_at          INTEGER NOT NULL,
  settled_at          INTEGER,
  UNIQUE (flow_job_id, attempt_number)
) STRICT;

-- F-18: Atomically block any new paid reservation that would breach episode video_budget_cap_micro_usd
CREATE TRIGGER trg_budget_cap_guard
BEFORE INSERT ON budget_reservations
WHEN (
  SELECT COALESCE(SUM(
    CASE
      WHEN status = 'COMMITTED' THEN COALESCE(actual_micro_usd, estimated_micro_usd)
      WHEN status IN ('RESERVED','UNKNOWN_HOLD') THEN estimated_micro_usd
      ELSE 0
    END
  ), 0)
  FROM budget_reservations
  WHERE episode_id = NEW.episode_id
) + NEW.estimated_micro_usd > (
  SELECT video_budget_cap_micro_usd FROM episodes WHERE episode_id = NEW.episode_id
)
BEGIN
  SELECT RAISE(ABORT, 'BUDGET_CAP_EXCEEDED: Episode durable USD reservation cap reached');
END;

CREATE TABLE flow_job_attempts (
  attempt_id            TEXT PRIMARY KEY,
  flow_job_id           TEXT NOT NULL REFERENCES flow_jobs(flow_job_id),
  attempt_number        INTEGER NOT NULL CHECK (attempt_number IN (1,2)),
  provider_operation_id TEXT,
  prompt_used           TEXT NOT NULL,
  cost_micro_usd        INTEGER NOT NULL DEFAULT 0 CHECK (cost_micro_usd >= 0),
  credits_charged       INTEGER NOT NULL DEFAULT 0 CHECK (credits_charged >= 0),
  pool_source           TEXT NOT NULL CHECK (pool_source IN ('GEMINI_API_USD','VERTEX_USD','DAILY_CREDITS','MONTHLY_CREDITS')),
  qa_verdict            TEXT NOT NULL CHECK (qa_verdict IN ('PASS','PENDING_MANUAL_SPOT_CHECK','FAIL_SAFETY_BLOCK','FAIL_MORPH','FAIL_DURATION_RES','UNKNOWN_TIMEOUT')),
  qa_notes              TEXT,
  created_at            INTEGER NOT NULL,
  UNIQUE (flow_job_id, attempt_number)
) STRICT;

CREATE TRIGGER trg_flow_two_strike_breaker
BEFORE INSERT ON flow_job_attempts
WHEN (SELECT attempts_used FROM flow_jobs WHERE flow_job_id = NEW.flow_job_id) >= 2
BEGIN
  SELECT RAISE(ABORT, 'LAW_3_BREAKER: 2-Strike Circuit Breaker tripped; must switch to fallback_spec');
END;

--------------------------------------------------------------------------------
-- 5. Mandatory Human Release Sign-Off Gate (F-06), QA Reports & Honest Analytics (F-12)
--------------------------------------------------------------------------------

CREATE TABLE release_approvals (
  approval_id            TEXT PRIMARY KEY,
  episode_id             TEXT NOT NULL REFERENCES episodes(episode_id),
  gate_name              TEXT NOT NULL CHECK (gate_name IN (
                           'FACTUAL_ACCURACY',
                           'PRIVACY_PII',
                           'SOURCE_RIGHTS',
                           'SYNTHETIC_DISCLOSURE',
                           'ILLUSTRATIVE_LABELING'
                         )),
  artifact_bundle_sha256 TEXT NOT NULL,
  status                 TEXT NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING','APPROVED','REJECTED','REVOKED')),
  reviewer_id            TEXT,
  reviewed_at            INTEGER,
  notes                  TEXT,
  UNIQUE (episode_id, gate_name, artifact_bundle_sha256),
  CHECK (status NOT IN ('APPROVED','REJECTED') OR (reviewer_id IS NOT NULL AND reviewed_at IS NOT NULL))
) STRICT;

-- F-04, F-06, F-09, Vision QA Fail-Closed: Hard-block READY_TO_UPLOAD / PUBLISHED unless ALL safeguards are proven
CREATE TRIGGER trg_episode_release_gate
BEFORE UPDATE OF state ON episodes
WHEN NEW.state IN ('READY_TO_UPLOAD','PUBLISHED')
  AND (
    -- 1. Case must be AFFIRMED/STANDING_CONVICTION and explicitly anonymized
    NOT EXISTS (
      SELECT 1 FROM cases c
      WHERE c.case_id = NEW.case_id
        AND c.disposition_status IN ('AFFIRMED','STANDING_CONVICTION')
        AND c.anonymization_status = 'APPROVED'
    )
    -- 2. Timeline must have transactional validation hash & ready_bundle_sha256
    OR NEW.timeline_validated_sha256 IS NULL
    OR NEW.ready_bundle_sha256 IS NULL
    -- 3. No flow jobs left in fail-closed PENDING_MANUAL_SPOT_CHECK or UNKNOWN_RECONCILE
    OR EXISTS (
      SELECT 1 FROM flow_jobs fj
      WHERE fj.episode_id = NEW.episode_id
        AND fj.state IN ('PENDING','SUBMITTING','RUNNING','UNKNOWN_RECONCILE','PENDING_MANUAL_SPOT_CHECK','STRIKE_1_RETRY_SAFE')
    )
    -- 4. All 5 mandatory human approval gates MUST be APPROVED for this exact ready_bundle_sha256
    OR (
      SELECT COUNT(DISTINCT gate_name)
      FROM release_approvals ra
      WHERE ra.episode_id = NEW.episode_id
        AND ra.artifact_bundle_sha256 = NEW.ready_bundle_sha256
        AND ra.status = 'APPROVED'
    ) < 5
  )
BEGIN
  SELECT RAISE(ABORT, 'RELEASE_GATE_BLOCKED: Cannot mark READY_TO_UPLOAD/PUBLISHED without APPROVED case anonymization, valid disposition, settled jobs, validated timeline, and all 5 human release approvals');
END;

CREATE TABLE qa_reports (
  qa_id                    TEXT PRIMARY KEY,
  episode_id               TEXT NOT NULL REFERENCES episodes(episode_id),
  integrated_lufs          REAL NOT NULL,
  true_peak_dbtp           REAL NOT NULL,
  lufs_passed              INTEGER NOT NULL CHECK (lufs_passed IN (0,1)),
  safe_zone_passed         INTEGER NOT NULL CHECK (safe_zone_passed IN (0,1)),
  vision_frame_qa_status   TEXT NOT NULL CHECK (vision_frame_qa_status IN ('PASSED','FAILED','PENDING_MANUAL_SPOT_CHECK')),
  thumbnail_brand_passed   INTEGER NOT NULL CHECK (thumbnail_brand_passed IN (0,1)),
  final_mp4_path           TEXT NOT NULL,
  final_mp4_sha256         TEXT NOT NULL,
  created_at               INTEGER NOT NULL
) STRICT;

-- F-12: Explicit UNKNOWN / PENDING / NOT_LINKED states + provenance source (no fabricated videos.list monetization field!)
CREATE TABLE episode_analytics (
  snapshot_id            TEXT PRIMARY KEY,
  episode_id             TEXT NOT NULL REFERENCES episodes(episode_id),
  days_since_publish     INTEGER NOT NULL CHECK (days_since_publish >= 1),
  ctr_pct                REAL, -- Nullable when only Data/Analytics API ran without Studio CSV
  retention_30s_pct      REAL,
  retention_min6_14_pct  REAL,
  avd_pct                REAL,
  watch_hours_total      REAL NOT NULL DEFAULT 0.0,
  rpm_micro_usd          INTEGER,
  adsense_status         TEXT NOT NULL DEFAULT 'UNKNOWN'
                         CHECK (adsense_status IN ('UNKNOWN','PENDING','NOT_LINKED','GREEN_FULL_ADS','YELLOW_LIMITED','NONE')),
  adsense_source         TEXT NOT NULL DEFAULT 'UNAVAILABLE'
                         CHECK (adsense_source IN ('STUDIO_CSV_EXPORT','MANUAL_CREATOR_ENTRY','UNAVAILABLE')),
  adsense_checked_at     INTEGER,
  metrics_source         TEXT NOT NULL DEFAULT 'YT_ANALYTICS_API'
                         CHECK (metrics_source IN ('YT_ANALYTICS_API','STUDIO_CSV_EXPORT','COMBINED')),
  captured_at            INTEGER NOT NULL
) STRICT;

--------------------------------------------------------------------------------
-- 6. Views for Conveyor Monitoring (Up to 3 Episodes Oldest-First)
--------------------------------------------------------------------------------

CREATE VIEW v_active_conveyor AS
SELECT
  e.episode_id,
  e.state,
  e.flow_backend_mode,
  e.video_budget_cap_micro_usd,
  COALESCE((
    SELECT SUM(CASE WHEN br.status = 'COMMITTED' THEN COALESCE(br.actual_micro_usd, br.estimated_micro_usd)
                    WHEN br.status IN ('RESERVED','UNKNOWN_HOLD') THEN br.estimated_micro_usd ELSE 0 END)
    FROM budget_reservations br WHERE br.episode_id = e.episode_id
  ), 0) AS reserved_or_spent_micro_usd,
  COUNT(fj.flow_job_id) AS total_flow_jobs,
  SUM(CASE WHEN fj.state IN ('ACCEPTED','SWITCHED_TO_FALLBACK') THEN 1 ELSE 0 END) AS completed_flow_jobs
FROM episodes e
LEFT JOIN flow_jobs fj ON fj.episode_id = e.episode_id
WHERE e.state NOT IN ('PUBLISHED','REJECTED_KILL_SWITCH','ABORTED_COPYCAT_WAVE')
GROUP BY e.episode_id
ORDER BY e.created_at ASC;
