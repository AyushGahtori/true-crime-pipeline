# Agent 6: Per-Track Audio Mastering, Single Grade, Fail-Closed QA & Honest Analytics (v3)

Agent 6 performs sample-accurate video/audio mastering, eliminates `loudnorm` pumping, prevents double-grading, enforces fail-closed QA (`PENDING_MANUAL_SPOT_CHECK`), requires **5-gate human release approval** (`F-06`), and ingests **honest creator-authorized YouTube Analytics** (`F-12`). Diagram: [mastering-loudness-and-qa.mmd](mastering-loudness-and-qa.mmd).

## 1. Per-Track Loudness Pre-Normalization -> Linear `-14.0 LUFS` Master

1. **Strict Ingest Parity:** All video segments arrive pre-normalized (`CFR 30 fps`, `1920x1080`, `yuv420p`) and audio streams at `48 kHz stereo PCM`.
2. **Per-Track Independent Pre-Normalization:**
   - **Track 1 (`NarrationSegments` + `TwistPads`):** High-pass `80 Hz` + de-esser (`6–8 kHz`) + `3:1` compression -> **`-16.0 LUFS`** (`TP <= -2.0 dBTP`).
   - **Track 2 (`Scrubbed FOIA / 911`):** Intelligibility bandpass (`250 Hz–4.5 kHz` gentle shelf where lo-fi telephony flagged) + `4:1` leveling -> **`-18.0 LUFS`**, preceded by `0.6s–1.0s` visual L-cuts.
   - **Track 3 (`Music Bed`):** **`-22.0 LUFS`** baseline ducked smoothly to **`-36.0 LUFS`** under active Track 1/2 speech.
   - **Track 4 (`Procedural SFX`):** Hierarchical 32-cue sub-buses via **`-filter_complex_script`** (Windows 32 KB CLI safe), capped `<= -18 LUFS`.
3. **Final Master Pass (`linear=true`):** Two-pass measured linear `loudnorm` targeting **`-14.0 LUFS (+/- 0.4 LU)`**, **`TP <= -1.0 dBTP`**, verifying `normalization_type == "linear"` so dynamic pumping never triggers silently.

## 2. Single Continuous Non-FOIA Grading Pass (Zero Double-Grading)

- Neither `@tc/render_catalog` nor `crime_scene_2k` applies paper grain or vignette. Agent 6 reads `scene_grade_manifest.json` and applies **one continuous grain + radial vignette pass** across all non-FOIA segments while keeping **`FOIA_REAL_FOOTAGE` raw and un-grained**.

## 3. Fail-Closed QA, Mandatory 5-Gate Human Sign-Off (`F-06`) & Honest Analytics (`F-12`)

- **`2x2` Contact-Sheet Vision QA & Pixel Safe-Zone Scan:** Audits rendered frames and triggers single-scene `--scene` heals (bounded `MAX_HEAL_PASSES = 2`; never spends extra paid video API budget overnight). If Vision QA is unreachable, `qa_reports.vision_frame_qa_status = 'PENDING_MANUAL_SPOT_CHECK'` **blocks export (`fail-closed`)** until human review completes!
- **Mandatory 5-Gate Human Release Sign-Off (`F-06`):** Overnight mastering transitions episodes strictly to **`PENDING_HUMAN_SIGNOFF`** (NEVER directly to `READY_TO_UPLOAD`!). `trg_episode_release_gate` requires a named human reviewer to approve all 5 gates in `release_approvals` (`FACTUAL_ACCURACY`, `PRIVACY_PII`, `SOURCE_RIGHTS`, `SYNTHETIC_DISCLOSURE`, `ILLUSTRATIVE_LABELING`) for the exact `ready_bundle_sha256` before atomic `ready_to_upload/` unlock.
- **Brand-Coherent Thumbnail Policy Controls:** Preserves recognizable typography/framing while rotating composition/silhouette/accent mood; rejects gore/blood/clutter/`> 2 MB` as measurable risk controls.
- **Honest YouTube Analytics Feedback (`F-12`, `packages/analytics_feedback`):**
  - Uses **`youtubeAnalytics.reports.query`** strictly for supported creator-authorized metrics (`views`, `estimatedMinutesWatched` -> `watch_hours_total`, `averageViewPercentage`, audience retention curve bins).
  - **Does NOT query `videos.list` for monetization/yellow-icon status** (the YouTube Data API `videos` resource exposes no such field — see [YouTube Videos Resource docs](https://developers.google.com/youtube/v3/docs/videos)).
  - `episode_analytics.adsense_status` defaults strictly to **`'UNKNOWN'`** (`adsense_source = 'UNAVAILABLE'`), updated solely from reviewed **YouTube Studio CSV exports** or explicit manual creator entry alongside CTR (`ctr_pct` nullable until Studio CSV import).
