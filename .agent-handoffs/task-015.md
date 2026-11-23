# Task 015 Handoff

- Task: 015 Dynamic watchlist seeder & weekly spillover discovery/pruning
- Branch: `task/015-agent1-dynamic-watchlist`
- Worktree: `../tc-wt/task-015-agent1-dynamic-watchlist`
- Track: Part 1
- Status: committed on the task branch only
- Owned paths touched: `packages/agent1_scout/src/agent1_scout/watchlist.py`, `packages/agent1_scout/tests/test_watchlist.py`, `.agent-handoffs/task-015.md`
- Dependencies added: none (stdlib only)
- Verification: see below
- Incomplete: persistence into `channels_watchlist` SQLite rows is left to the pipeline layer; this module is an offline manager with in-memory state.
- Notes for the next agent: Task 016 `NightlyZeroSearchPoller` should consume `WatchlistManager.snapshot()` active rows. Task 019 spillover dicts (`channel_id`, `subscriber_count`) feed `discover_spillover_channels`.

Commit only on the task branch. Do not merge, push, or change git config.

```
TC-Task-ID: 015
TC-Track: Part 1
TC-Never-Merge: true
```

## What landed

`WatchlistManager` in `packages/agent1_scout/src/agent1_scout/watchlist.py`.

- Seeding calls injected `channels.list` only, batches up to 50 channel ids per call, maps `UC…` → `UU…` uploads playlists, stamps `yt_ttl_expires_at = now_ms + 30d`, and records `discovered_via = 'SEED'`. Any `search.list` route raises `SearchListForbiddenError` (ledger must stay at zero search calls).
- Active band admission requires `subscriber_count` in **2000–120000** inclusive plus a true-crime topic match (Freebase crime topic ids and/or crime keywords, with pop-culture keyword rejection).
- `discover_spillover_channels(search_results)` batch-checks unknown channels via `channels.list`, re-validates the subscriber band and topic match, then inspects the last 10 uploads via `playlistItems.list` + `videos.list`. Promotion requires **≥ 3** long-form (`duration >= 600s`, no `#shorts` tag) crime-titled videos; Shorts farms and pop-culture channels fail this gate. Promoted rows use `discovered_via = 'SPILLOVER'`. Spillover stops when active count reaches the 400 ceiling.
- `prune(now_ms)` deactivates dormant channels with `last_upload_at_ms` older than 180 days and graduated channels whose refreshed `subscriber_count` exceeds 120000.

## Tests

From the task worktree:

```text
python -m venv .venv
.\.venv\Scripts\python -m pip install pytest
$env:PYTHONPATH='packages/agent1_scout/src'
.\.venv\Scripts\python -m pytest packages/agent1_scout/tests/test_watchlist.py
```

Covered: UC→UU mapping, 50-id batching, zero `search.list` on seed, subscriber band edges, pop-culture rejection, spillover promotion, Shorts-farm rejection, insufficient long-form crime rejection, dormant and graduated pruning.