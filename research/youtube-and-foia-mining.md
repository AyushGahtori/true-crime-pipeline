# Research: Authorized YouTube APIs, 30-Day Retention, CourtListener Caps & Scouting (`F-11`, `F-12`, `F-20`)

*Last verified: 2026-11-23*

## 1. Verified External API Capabilities & Limits
- **YouTube `captions.download` Restriction (`F-11`):** Downloading captions via the YouTube Data API requires authorization/edit permissions on the target video and cannot download transcripts for arbitrary public third-party videos. Source: [YouTube Data API `captions.download`](https://developers.google.com/youtube/v3/docs/captions/download).
  - *Design Impact:* Track A scouting uses **strictly authorized `videos.list` metadata (`title`, `description`, `tags`) + `commentThreads.list` public questions**, labeled `LEAD_ONLY` (never factual evidence). Third-party transcripts are treated as optional/unavailable.
- **YouTube `videos.list` Resource Fields (`F-12`):** The `videos` resource does **not** expose `monetizationDetails` or AdSense yellow-icon status. Source: [YouTube Data API `videos` Resource](https://developers.google.com/youtube/v3/docs/videos).
  - *Design Impact:* `packages/analytics_feedback` queries `youtubeAnalytics.reports.query` strictly for supported creator metrics (views, watch hours, AVD, retention curves), sets `episode_analytics.adsense_status = 'UNKNOWN'` (`adsense_source = 'UNAVAILABLE'`) by default, and imports monetization/CTR solely from reviewed YouTube Studio CSV exports or manual creator entry.
- **YouTube 30-Day Retention Scope (`F-20`):** `outlier_candidates` enforces non-null `yt_ttl_expires_at` on `TRACK_A_OUTLIER` rows and purges ALL YouTube API-derived fields (`raw_yt_payload_json`, `views_count`, `outlier_ratio`, YT seed excerpts) on expiry (`purge_expired_yt_api_records`). Source: [YouTube API Services Developer Policies](https://developers.google.com/youtube/terms/developer-policies/).

## 2. Scouting Heuristics (Design Hypotheses To Calibrate via `episode_analytics`)
- **Mutually Exclusive Saturation Index (`SI`) + 90-Day `>200K` Kill:** Deduplicated videos across 3–4 aliases enter strictly one highest-priority bucket (`N_14d_excl`, decayed `N_mega_excl`, `N_recent_excl`); any `> 200K` upload within 90 days triggers immediate `HARD_KILL_RECENT_DEMAND_EXHAUSTED`. Threshold weights (`SI <= 35` target, `>= 55` kill) are initial heuristics calibrated over time using actual channel analytics.
- **CourtListener Quota Guard:** Respects `courtlistener` daily bucket (`125/day`, `5/min`, `50/hr`) with local `courtlistener_cache` reuse.
