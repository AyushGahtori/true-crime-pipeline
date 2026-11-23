// Executable SQLite schema verification suite (v3) using built-in node:sqlite
// Verifies SQL invariants across F-01..F-22 (not a substitute for application E2E tests).
// Run: node schema/schema-test.js

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { DatabaseSync } = require('node:sqlite');

const pipelineSql = fs.readFileSync(path.join(__dirname, 'pipeline.sql'), 'utf8');
const telemetrySql = fs.readFileSync(path.join(__dirname, 'telemetry.sql'), 'utf8');
const queriesSql = fs.readFileSync(path.join(__dirname, 'queries.sql'), 'utf8');

function extractQuery(name) {
  const re = new RegExp(`-- name: ${name}\\r?\\n([\\s\\S]*?)(?=\\r?\\n-- name:|$)`);
  const m = queriesSql.match(re);
  assert.ok(m, `Query '${name}' not found in queries.sql`);
  return m[1].trim();
}

function setupDb() {
  const db = new DatabaseSync(':memory:');
  db.exec('PRAGMA foreign_keys = ON;');
  db.exec(pipelineSql);
  return db;
}

function seedApprovedCaseAndEpisode(db, epState = 'MASTERED') {
  db.prepare(
    `INSERT INTO cases (case_id, defendant_name, incident_year, jurisdiction, docket_id, primary_record_verified, verification_source, disposition_status, conviction_confirmed, anonymization_status, anonymized_by, anonymized_at, anonymization_artifact_sha256, created_at, updated_at)
     VALUES ('case_1','John Doe',2023,'Mercer, NJ','DK-1',1,'courtlistener','AFFIRMED',1,'APPROVED','reviewer_a',1000,'sha_anon_1',1000,1000)`
  ).run();
  db.prepare(
    `INSERT INTO episodes (episode_id, case_id, state, flow_backend_mode, cold_open_archetype, total_master_ms, timeline_validated_sha256, ready_bundle_sha256, updated_at, created_at)
     VALUES ('ep_1','case_1',?,'GEMINI_OMNI_INTERACTIONS','911_CALL_IN_MEDIA_RES',1200000,'sha_tl_1','sha_bundle_1',1000,1000)`
  ).run(epState);
}

const scenarios = [
  ['1. Telemetry schema loads cleanly in STRICT mode', () => {
    const tdb = new DatabaseSync(':memory:');
    tdb.exec(telemetrySql);
    tdb.prepare(
      `INSERT INTO api_token_usage (episode_id, agent_name, model_id, is_off_peak, input_tokens, cached_input_tokens, output_tokens, cost_micro_usd, created_at)
       VALUES ('ep_01','agent4','DeepSeek-V4.1-Flash-1017',1,10000,25000,12000,15000,1700000000000)`
    ).run();
    assert.equal(tdb.prepare('SELECT COUNT(*) AS c FROM api_token_usage').get().c, 1);
    tdb.close();
  }],

  ['2. Lookup tables seed v3 metadata, 16 states, 9 flow job states, authoritative 4-motif MVP registry', () => {
    const db = setupDb();
    assert.equal(db.prepare("SELECT value FROM meta WHERE key='schema_version'").get().value, '3');
    assert.equal(db.prepare("SELECT value FROM meta WHERE key='primary_video_model'").get().value, 'gemini-omni-1.2-flash');
    assert.equal(db.prepare('SELECT COUNT(*) AS c FROM episode_states').get().c, 16);
    assert.equal(db.prepare('SELECT COUNT(*) AS c FROM flow_job_states').get().c, 9);
    assert.equal(db.prepare('SELECT COUNT(*) AS c FROM motif_registry WHERE is_mvp_4 = 1').get().c, 4);
    db.close();
  }],

  ['3. F-03: Case disposition guard protects BOTH INSERT and UPDATE + auto-quarantines downstream episodes', () => {
    const db = setupDb();
    // INSERT rejected when REVERSED + conviction_confirmed = 1
    assert.throws(() => {
      db.prepare(`INSERT INTO cases (case_id,defendant_name,incident_year,jurisdiction,verification_source,disposition_status,conviction_confirmed,created_at,updated_at)
                  VALUES ('case_rev','Jane Doe',2023,'Mercer, NJ','courtlistener','REVERSED',1,1000,1000)`).run();
    }, /LEGAL_DISPOSITION/);

    seedApprovedCaseAndEpisode(db, 'PENDING_HUMAN_SIGNOFF');
    // Seed an approval to verify auto-revocation on disposition reversal
    db.prepare(`INSERT INTO release_approvals VALUES ('ap_1','ep_1','FACTUAL_ACCURACY','sha_bundle_1','APPROVED','rev_1',1001,'ok')`).run();

    // UPDATE rejected if leaving conviction_confirmed = 1 while flipping to REVERSED
    assert.throws(() => {
      db.prepare(`UPDATE cases SET disposition_status = 'REVERSED', updated_at = 2000 WHERE case_id = 'case_1'`).run();
    }, /LEGAL_DISPOSITION/);

    // Valid UPDATE flipping conviction_confirmed = 0 & disposition_status = REVERSED auto-quarantines episode & revokes approval!
    db.prepare(`UPDATE cases SET disposition_status = 'REVERSED', conviction_confirmed = 0, updated_at = 2000 WHERE case_id = 'case_1'`).run();
    assert.equal(db.prepare(`SELECT state FROM episodes WHERE episode_id = 'ep_1'`).get().state, 'QUARANTINED_LEGAL_HOLD');
    assert.equal(db.prepare(`SELECT status FROM release_approvals WHERE approval_id = 'ap_1'`).get().status, 'REVOKED');
    db.close();
  }],

  ['4. F-04: Anonymization and spatial anchor locking default to NOT_STARTED / DRAFT and require provenance to approve/lock', () => {
    const db = setupDb();
    db.prepare(`INSERT INTO cases (case_id,defendant_name,incident_year,jurisdiction,verification_source,disposition_status,conviction_confirmed,created_at,updated_at)
                VALUES ('case_raw','John Doe',2023,'Mercer, NJ','courtlistener','AFFIRMED',1,1000,1000)`).run();
    assert.equal(db.prepare(`SELECT anonymization_status FROM cases WHERE case_id = 'case_raw'`).get().anonymization_status, 'NOT_STARTED');

    // Cannot mark APPROVED without reviewer + timestamp + sha256
    assert.throws(() => {
      db.prepare(`UPDATE cases SET anonymization_status = 'APPROVED' WHERE case_id = 'case_raw'`).run();
    });

    db.prepare(`INSERT INTO episodes (episode_id,case_id,state,cold_open_archetype,updated_at,created_at)
                VALUES ('ep_raw','case_raw','EVIDENCE_AND_2K_LOCKED','ALIBI_THAT_CRACKED',1000,1000)`).run();
    db.prepare(`INSERT INTO still_assets (still_2k_id,episode_id,asset_path,asset_sha256,width_px,height_px,created_at)
                VALUES ('st_1','ep_raw','room.png','sha_room',2560,1440,1000)`).run();
    db.prepare(`INSERT INTO spatial_anchors (anchor_id,episode_id,still_2k_id,clue_name,grid_cell,x_px,y_px)
                VALUES ('anc_1','ep_raw','st_1','broken_chair','E5',1280,720)`).run();
    assert.equal(db.prepare(`SELECT lock_status FROM spatial_anchors WHERE anchor_id = 'anc_1'`).get().lock_status, 'DRAFT');

    // Cannot mark LOCKED without locked_by/locked_at/still_asset_sha256
    assert.throws(() => {
      db.prepare(`UPDATE spatial_anchors SET lock_status = 'LOCKED' WHERE anchor_id = 'anc_1'`).run();
    });
    // Invalid grid cell rejected
    assert.throws(() => {
      db.prepare(`INSERT INTO spatial_anchors (anchor_id,episode_id,still_2k_id,clue_name,grid_cell,x_px,y_px)
                  VALUES ('anc_bad','ep_raw','st_1','x','Z99',100,100)`).run();
    });
    db.close();
  }],

  ['5. F-06 & Vision QA Fail-Closed: READY_TO_UPLOAD requires all 5 human release approvals + settled jobs', () => {
    const db = setupDb();
    seedApprovedCaseAndEpisode(db, 'PENDING_HUMAN_SIGNOFF');

    // Missing all 5 approvals -> blocked!
    assert.throws(() => {
      db.prepare(`UPDATE episodes SET state = 'READY_TO_UPLOAD' WHERE episode_id = 'ep_1'`).run();
    }, /RELEASE_GATE_BLOCKED/);

    // Approve all 5 gates for sha_bundle_1
    const gates = ['FACTUAL_ACCURACY', 'PRIVACY_PII', 'SOURCE_RIGHTS', 'SYNTHETIC_DISCLOSURE', 'ILLUSTRATIVE_LABELING'];
    gates.forEach((g, idx) => {
      db.prepare(`INSERT INTO release_approvals VALUES (?, 'ep_1', ?, 'sha_bundle_1', 'APPROVED', 'editor_jane', 2000, 'verified')`).run(`ap_${idx}`, g);
    });

    // Add a flow_job stuck in PENDING_MANUAL_SPOT_CHECK -> MUST fail closed!
    db.prepare(`INSERT INTO scenes (scene_id,episode_id,seq_index,act_number,visual_engine,motif_component,start_ms,end_ms,timeline_spec_json)
                VALUES ('sc_1','ep_1',1,1,'FLOW_HERO_VIDEO','HeroVideoBridge',0,8000,'{}')`).run();
    db.prepare(`INSERT INTO flow_jobs (flow_job_id,episode_id,scene_id,idempotency_key,prompt_mode,duration_bucket_sec,prompt_v1,prompt_v2_safe,fallback_spec_json,state,updated_at)
                VALUES ('fj_1','ep_1','sc_1','idem_ep1_sc1','TEXT_TO_VIDEO',8,'p1','p2','{}','PENDING_MANUAL_SPOT_CHECK',2000)`).run();
    assert.throws(() => {
      db.prepare(`UPDATE episodes SET state = 'READY_TO_UPLOAD' WHERE episode_id = 'ep_1'`).run();
    }, /RELEASE_GATE_BLOCKED/);

    // Once manual spot check resolves job to ACCEPTED -> READY_TO_UPLOAD succeeds!
    db.prepare(`UPDATE flow_jobs SET state = 'ACCEPTED' WHERE flow_job_id = 'fj_1'`).run();
    db.prepare(`UPDATE episodes SET state = 'READY_TO_UPLOAD' WHERE episode_id = 'ep_1'`).run();
    assert.equal(db.prepare(`SELECT state FROM episodes WHERE episode_id = 'ep_1'`).get().state, 'READY_TO_UPLOAD');
    db.close();
  }],

  ['6. F-07: flow_jobs supports TEXT_TO_VIDEO (null frames), FIRST_FRAME, and FIRST_AND_LAST_FRAME (<=10s)', () => {
    const db = setupDb();
    seedApprovedCaseAndEpisode(db, 'AWAITING_FLOW_BATCH');
    db.prepare(`INSERT INTO scenes (scene_id,episode_id,seq_index,act_number,visual_engine,motif_component,start_ms,end_ms,timeline_spec_json) VALUES ('s1','ep_1',1,1,'FLOW_HERO_VIDEO','HeroVideoBridge',0,12000,'{}')`).run();
    db.prepare(`INSERT INTO scenes (scene_id,episode_id,seq_index,act_number,visual_engine,motif_component,start_ms,end_ms,timeline_spec_json) VALUES ('s2','ep_1',2,1,'FLOW_HERO_VIDEO','HeroVideoBridge',12000,20000,'{}')`).run();
    db.prepare(`INSERT INTO scenes (scene_id,episode_id,seq_index,act_number,visual_engine,motif_component,start_ms,end_ms,timeline_spec_json) VALUES ('s3','ep_1',3,1,'FLOW_HERO_VIDEO','HeroVideoBridge',20000,28000,'{}')`).run();

    // Valid TEXT_TO_VIDEO with NULL frames (12s supported by Omni 1.2 Flash!)
    db.prepare(`INSERT INTO flow_jobs (flow_job_id,episode_id,scene_id,idempotency_key,prompt_mode,duration_bucket_sec,start_frame_png,end_frame_png,prompt_v1,prompt_v2_safe,fallback_spec_json,updated_at)
                VALUES ('fj_t2v','ep_1','s1','idem_1','TEXT_TO_VIDEO',12,NULL,NULL,'p1','p2','{}',1000)`).run();

    // FIRST_FRAME without start_frame_png rejected
    assert.throws(() => {
      db.prepare(`INSERT INTO flow_jobs (flow_job_id,episode_id,scene_id,idempotency_key,prompt_mode,duration_bucket_sec,start_frame_png,end_frame_png,prompt_v1,prompt_v2_safe,fallback_spec_json,updated_at)
                  VALUES ('fj_bad1','ep_1','s2','idem_2','FIRST_FRAME',8,NULL,NULL,'p1','p2','{}',1000)`).run();
    });

    // FIRST_AND_LAST_FRAME with duration > 10s (Omni 1.2 Flash limit) rejected
    assert.throws(() => {
      db.prepare(`INSERT INTO flow_jobs (flow_job_id,episode_id,scene_id,idempotency_key,prompt_mode,duration_bucket_sec,start_frame_png,end_frame_png,prompt_v1,prompt_v2_safe,fallback_spec_json,updated_at)
                  VALUES ('fj_bad2','ep_1','s2','idem_3','FIRST_AND_LAST_FRAME',12,'a.png','b.png','p1','p2','{}',1000)`).run();
    });

    // Valid FIRST_AND_LAST_FRAME (8s) succeeds
    db.prepare(`INSERT INTO flow_jobs (flow_job_id,episode_id,scene_id,idempotency_key,prompt_mode,duration_bucket_sec,start_frame_png,end_frame_png,prompt_v1,prompt_v2_safe,fallback_spec_json,updated_at)
                VALUES ('fj_f2v','ep_1','s3','idem_4','FIRST_AND_LAST_FRAME',8,'a.png','b.png','p1','p2','{}',1000)`).run();
    assert.equal(db.prepare('SELECT COUNT(*) AS c FROM flow_jobs').get().c, 2);
    db.close();
  }],

  ['7. F-08: Atomic daily credit query enforces 24h+5m lockout before reset and refills cleanly at/after reset', () => {
    const db = setupDb();
    const reserveSql = extractQuery('atomic_refill_and_reserve_daily_account_credits');
    const stmt = db.prepare(reserveSql);

    const t0 = 1_700_000_000_000;
    const expectedReset = t0 + 86_400_000 + 300_000;

    // Spend 30 then 20 -> exhausts 50/50 daily pool
    let r = stmt.get({ ':account_id': 'acct_1', ':credits': 30, ':now_ms': t0 });
    assert.equal(r.daily_credits_left, 20);
    assert.equal(r.next_daily_reset_utc_ms, expectedReset);

    r = stmt.get({ ':account_id': 'acct_1', ':credits': 20, ':now_ms': t0 + 60_000 });
    assert.equal(r.daily_credits_left, 0);

    // Just-before reset (expectedReset - 1 ms): MUST reject!
    assert.equal(stmt.get({ ':account_id': 'acct_1', ':credits': 10, ':now_ms': expectedReset - 1 }), undefined);

    // Exact-at reset (expectedReset): atomically refills to 50 and deducts 10 -> 40 left with new reset window!
    r = stmt.get({ ':account_id': 'acct_1', ':credits': 10, ':now_ms': expectedReset });
    assert.equal(r.daily_credits_left, 40);
    assert.equal(r.next_daily_reset_utc_ms, expectedReset + 86_400_000 + 300_000);
    db.close();
  }],

  ['8. F-09: Timeline non-overlap triggers & segment kind media requirements enforced by schema', () => {
    const db = setupDb();
    seedApprovedCaseAndEpisode(db, 'VOICE_READY');

    // NARRATION with NULL audio_path rejected
    assert.throws(() => {
      db.prepare(`INSERT INTO voice_segments VALUES ('vs_bad','ep_1',1,'NARRATION',0,5000,NULL,NULL)`).run();
    });
    // FOIA_AUDIO_SLOT with NULL foia_asset_id rejected
    assert.throws(() => {
      db.prepare(`INSERT INTO voice_segments VALUES ('vs_bad2','ep_1',1,'FOIA_AUDIO_SLOT',0,5000,NULL,NULL)`).run();
    });

    db.prepare(`INSERT INTO voice_segments VALUES ('vs_1','ep_1',1,'NARRATION',0,10000,'s1.wav',NULL)`).run();
    // Overlapping segment rejected
    assert.throws(() => {
      db.prepare(`INSERT INTO voice_segments VALUES ('vs_ov','ep_1',2,'NARRATION',9500,15000,'s2.wav',NULL)`).run();
    }, /TIMELINE_OVERLAP/);

    // Contiguous segment succeeds
    db.prepare(`INSERT INTO voice_segments VALUES ('vs_2','ep_1',2,'TWIST_PAD',10000,10600,NULL,NULL)`).run();
    assert.equal(db.prepare('SELECT COUNT(*) AS c FROM voice_segments').get().c, 2);
    db.close();
  }],

  ['9. F-10 & F-18: Unique (episode_id, scene_id) prevents duplicate paid jobs & durable USD budget cap blocks overspend', () => {
    const db = setupDb();
    seedApprovedCaseAndEpisode(db, 'AWAITING_FLOW_BATCH');
    // Set tight $1.50 cap (1_500_000 micro-USD)
    db.prepare(`UPDATE episodes SET video_budget_cap_micro_usd = 1500000 WHERE episode_id = 'ep_1'`).run();
    db.prepare(`INSERT INTO scenes (scene_id,episode_id,seq_index,act_number,visual_engine,motif_component,start_ms,end_ms,timeline_spec_json) VALUES ('s1','ep_1',1,1,'FLOW_HERO_VIDEO','HeroVideoBridge',0,8000,'{}')`).run();
    db.prepare(`INSERT INTO scenes (scene_id,episode_id,seq_index,act_number,visual_engine,motif_component,start_ms,end_ms,timeline_spec_json) VALUES ('s2','ep_1',2,1,'FLOW_HERO_VIDEO','HeroVideoBridge',8000,16000,'{}')`).run();

    db.prepare(`INSERT INTO flow_jobs (flow_job_id,episode_id,scene_id,idempotency_key,prompt_mode,duration_bucket_sec,prompt_v1,prompt_v2_safe,fallback_spec_json,provider_operation_id,state,updated_at)
                VALUES ('fj_1','ep_1','s1','idem_1','TEXT_TO_VIDEO',8,'p1','p2','{}','op_123','UNKNOWN_RECONCILE',1000)`).run();

    // Duplicate (episode_id, scene_id) rejected!
    assert.throws(() => {
      db.prepare(`INSERT INTO flow_jobs (flow_job_id,episode_id,scene_id,idempotency_key,prompt_mode,duration_bucket_sec,prompt_v1,prompt_v2_safe,fallback_spec_json,updated_at)
                  VALUES ('fj_dup','ep_1','s1','idem_dup','TEXT_TO_VIDEO',8,'p1','p2','{}',1001)`).run();
    });

    // Reserve $0.80 (800_000 micro-USD) for fj_1 -> OK
    db.prepare(`INSERT INTO budget_reservations VALUES ('res_1','ep_1','fj_1',1,800000,NULL,'UNKNOWN_HOLD',1000,NULL)`).run();

    // Reserve another $0.80 for fj_2 -> total $1.60 > $1.50 cap -> BLOCKED!
    db.prepare(`INSERT INTO flow_jobs (flow_job_id,episode_id,scene_id,idempotency_key,prompt_mode,duration_bucket_sec,prompt_v1,prompt_v2_safe,fallback_spec_json,updated_at)
                VALUES ('fj_2','ep_1','s2','idem_2','TEXT_TO_VIDEO',8,'p1','p2','{}',1002)`).run();
    assert.throws(() => {
      db.prepare(`INSERT INTO budget_reservations VALUES ('res_2','ep_1','fj_2',1,800000,NULL,'RESERVED',1002,NULL)`).run();
    }, /BUDGET_CAP_EXCEEDED/);

    // Release res_1 (e.g. $0 safety block) -> now fj_2 reservation succeeds!
    db.prepare(`UPDATE budget_reservations SET status = 'RELEASED', actual_micro_usd = 0, settled_at = 1003 WHERE reservation_id = 'res_1'`).run();
    db.prepare(`INSERT INTO budget_reservations VALUES ('res_2','ep_1','fj_2',1,800000,NULL,'RESERVED',1004,NULL)`).run();
    assert.equal(db.prepare('SELECT COUNT(*) AS c FROM budget_reservations').get().c, 2);
    db.close();
  }],

  ['10. F-12 & F-20: Honest analytics UNKNOWN defaults + non-null YouTube 30-day TTL full-field purge', () => {
    const db = setupDb();
    // TRACK_A_OUTLIER with NULL yt_ttl_expires_at rejected!
    assert.throws(() => {
      db.prepare(`INSERT INTO outlier_candidates (candidate_id,track,source_video_id,views_count,outlier_ratio,saturation_index,seed_packet_json,raw_yt_payload_json,yt_ttl_expires_at,status,created_at)
                  VALUES ('c_bad','TRACK_A_OUTLIER','v1',50000,10.0,20,'{}','{"raw":1}',NULL,'CANDIDATE',1000)`).run();
    });

    db.prepare(`INSERT INTO outlier_candidates (candidate_id,track,source_video_id,views_count,outlier_ratio,saturation_index,seed_packet_json,raw_yt_payload_json,yt_ttl_expires_at,status,created_at)
                VALUES ('c_ok','TRACK_A_OUTLIER','v1',50000,10.0,20,'{"yt_title":"x"}','{"raw":1}',2000,'GREENLIT',1000)`).run();
    const purgeSql = extractQuery('purge_expired_yt_api_records');
    db.prepare(purgeSql).run({ ':now_ms': 2500 });
    const purged = db.prepare(`SELECT views_count, outlier_ratio, raw_yt_payload_json, status FROM outlier_candidates WHERE candidate_id='c_ok'`).get();
    assert.equal(purged.views_count, null);
    assert.equal(purged.outlier_ratio, null);
    assert.equal(purged.raw_yt_payload_json, null);
    assert.equal(purged.status, 'EXPIRED_TOS_PURGED');

    seedApprovedCaseAndEpisode(db, 'PUBLISHED');
    db.prepare(`INSERT INTO episode_analytics (snapshot_id,episode_id,days_since_publish,watch_hours_total,captured_at)
                VALUES ('an_1','ep_1',2,180.5,5000)`).run();
    const an = db.prepare(`SELECT adsense_status, adsense_source, ctr_pct FROM episode_analytics WHERE snapshot_id='an_1'`).get();
    assert.equal(an.adsense_status, 'UNKNOWN');
    assert.equal(an.adsense_source, 'UNAVAILABLE');
    assert.equal(an.ctr_pct, null);
    db.close();
  }],

  ['11. F-14 & F-15: Per-asset rights provenance blocks RESTRICTED_NO_REUSE approval & tracks honest ASR disagreement', () => {
    const db = setupDb();
    seedApprovedCaseAndEpisode(db, 'EVIDENCE_AND_2K_LOCKED');

    // Cannot approve a RESTRICTED_NO_REUSE asset
    assert.throws(() => {
      db.prepare(`INSERT INTO foia_media_assets (asset_id,case_id,source_domain,source_url,creator_entity,rights_holder,license_basis,rights_review_status,rights_reviewed_by,rights_reviewed_at,media_kind,raw_path)
                  VALUES ('fa_bad','case_1','muckrock.com','https://muckrock.com/1','Bystander','Private Citizen','RESTRICTED_NO_REUSE','APPROVED','rev_1',1000,'bodycam_mp4','raw.mp4')`).run();
    });

    db.prepare(`INSERT INTO foia_media_assets (asset_id,case_id,source_domain,source_url,creator_entity,rights_holder,license_basis,rights_review_status,rights_reviewed_by,rights_reviewed_at,media_kind,raw_path,asr_hypothesis_disagreement,human_audio_review_required)
                VALUES ('fa_ok','case_1','fbi.gov','https://fbi.gov/1','US Federal Employee','Public Domain (17 USC 105)','US_FED_EMPLOYEE_17USC105','APPROVED','rev_1',1000,'call_911_wav','911.wav',0.14,1)`).run();
    assert.equal(db.prepare(`SELECT human_audio_review_required FROM foia_media_assets WHERE asset_id='fa_ok'`).get().human_audio_review_required, 1);
    db.close();
  }],

  ['12. Quota bucket & RULE_09 news_report hedging triggers remain strictly enforced', () => {
    const db = setupDb();
    const stmt = db.prepare(extractQuery('consume_quota_bucket'));
    assert.equal(stmt.get({ ':bucket_name': 'yt_search', ':units': 60 }).used_today, 60);
    assert.equal(stmt.get({ ':bucket_name': 'yt_search', ':units': 45 }), undefined);

    seedApprovedCaseAndEpisode(db, 'SCOUTED');
    db.prepare(`INSERT INTO primary_documents VALUES ('doc_1','case_1','example.com','https://example.com/1','news_text_only','abc','/tmp/1.txt',1000)`).run();
    assert.throws(() => {
      db.prepare(`INSERT INTO fact_ledger VALUES ('f1','case_1','2023-11-04T22:00:00Z','Suspect seen','[]','Route 9','news_report','doc_1','p.1',0,'[]')`).run();
    }, /RULE_09/);
    db.close();
  }],
];

let passed = 0;
for (const [name, fn] of scenarios) {
  fn();
  console.log(`PASS: ${name}`);
  passed++;
}
console.log(`\n${passed}/${scenarios.length} schema scenarios passed.`);
