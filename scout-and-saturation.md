# Agent 1 v3: Dual-Track Saturation Detector, Authorized Leads & Strict 30-Day Retention

Agent 1 v3 balances small-creator outlier discovery (`Track A`) with direct primary-record FOIA/appellate feeds (`Track B`) while respecting CourtListener's **125 requests/day** (`5/min`, `50/hr`) cap, YouTube Data API v3 authorization rules (`F-11`), and strict 30-day YouTube API data retention (`F-20`). Diagram: [scout-and-saturation.mmd](scout-and-saturation.mmd). Research: [youtube-and-foia-mining.md](research/youtube-and-foia-mining.md).

## 1. Dual-Track Sourcing & Strict 30-Day YouTube API Data Lifecycle (`F-20`)

- **70/30 Split:** 70% Track A (Small-Creator Outlier Mining, `2K–120K` subs) + 30% Track B (MuckRock FOIA drops & CourtListener appellate rulings).
- **Dynamic Weekly Watchlist Discovery & Pruning:** Refreshes active `2K–120K` true-crime channels weekly (`channels_watchlist.yt_ttl_expires_at` mandatory non-null 30-day refresh/purge SLA).
- **Strict 30-Day YouTube API Services Retention Rule (`F-20`):**
  - Per [YouTube API Services Developer Policies](https://developers.google.com/youtube/terms/developer-policies/), EVERY YouTube-sourced row (`TRACK_A_OUTLIER`) requires a **non-null `yt_ttl_expires_at = created_at + 30 days`** (`CHECK` constraint in `schema/pipeline.sql`).
  - Every YouTube-derived field is explicitly inventoried: `raw_yt_payload_json`, `views_count`, `outlier_ratio`, and YT metadata excerpts inside `seed_packet_json`. At 30 days (unless actively refreshed from the API), `purge_expired_yt_api_records` clears **all** YouTube-derived fields on the record and transitions unconsumed rows to `EXPIRED_TOS_PURGED`. Only independently verified primary-record court/FOIA entities stored in `cases` and `primary_documents` persist permanently.

## 2. Zero-Search Polling & Mutually Exclusive Saturation Index (`SI`)

1. **Nightly Zero-Search Polling (`~450` `yt_general` units/day, `0 search.list`):** Poll `UU...` uploads playlists + 50-ID `videos.list` batches; compute `OR = views / 20_video_median` (`>= 3.5x`, `>= 20K` views, `<= 12 mo`).
2. **Mutually Exclusive Saturation Index (`SI`) + 90-Day `>200K` Instant Kill:**
   Every deduplicated video across 3–4 canonical aliases belongs to **strictly one highest-priority bucket**:
   - **90-Day Recency Hard Kill:** Any single upload `> 200,000` views within the last 90 days triggers immediate `HARD_KILL_RECENT_DEMAND_EXHAUSTED`.
   - `N_14d_excl`: New uploads within last 14 days (`weight = 8`).
   - `N_mega_excl`: Videos `> 500K` views or Tier-1 channels not in `N_14d_excl`, with time decay (`1.0` for `0–18 mo`, `0.5` for `18–36 mo`).
   - `N_recent_excl`: Remaining videos `> 50K` views in last 18 months (`weight = 12`).
   ```text
   SI = min(100, round(25 * N_mega_decayed + 12 * N_recent_excl + 8 * N_14d_excl))
   ```
   Hard Kill if `SI >= 55`; Sweet Spot requires `SI <= 35`.
3. **Safe-Title CTR Feasibility Check:** Verifies that an editorial, non-sensationalized documentary title remains compelling (`safe_title_ctr_ok = 1`).

## 3. Authorized Metadata Lead Extraction & Clean-Room Seed Firewall (`F-11`)

- **No Unsupported Third-Party Caption Scraping (`F-11`):** The YouTube Data API `captions.download` endpoint requires edit permission on the video ([YouTube captions.download docs](https://developers.google.com/youtube/v3/docs/captions/download)) and CANNOT download captions from arbitrary competitor videos. Agent 1 NEVER attempts unauthorized caption scraping or third-party MP4 downloads.
- **Permitted Lead Sources (Strictly Labeled `LEAD_ONLY`, Never Evidence):**
  1. Official YouTube `videos.list` metadata (`title`, `description`, `tags`) + `commentThreads.list` public viewer questions (`LEAD_ONLY`).
  2. Optional Gemini URL inspection strictly where playback is permitted; if `PLAYBACK_RESTRICTED` / age-restricted, proceed cleanly using **authorized metadata + comment leads only** (treating transcripts as optional/unavailable unless owner-authorized).
- **Clean-Room Seed Firewall:** Output `SeedPacket` contains ONLY factual lookup keys (`suspect_names`, `victim_names`, `incident_date_or_year`, `county_state`, `docket_ids`, `unanswered_comment_questions`) to locate **primary court/FOIA documents** in Agent 2. No YouTube comment or description text may ever be cited as factual evidence in `fact_ledger`.
- **Per-Day Pre-Render Re-Check + Sunk-Cost Guard:** Runs `search.list` re-check before multi-day paid shifts; aborts if `N_14d_wave > 3`, unless `> 50%` of episode budget is already committed AND `N_14d_wave <= 5`.
