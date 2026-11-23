# Task 004 handoff

Branch `task/004-golden-fixture-packs`. Not merged. Not pushed.

## What landed

Three self-contained v4 packs under `fixtures/golden_manifests/`:

- `ep_golden_01_20min` — 10 accepted hero jobs
- `ep_golden_02_2strike_fallback` — one `STRIKE_1_RETRY_SAFE` job and one `SWITCHED_TO_FALLBACK` job (`attempts_used = 2`, verdicts `FAIL_MORPH` then `FAIL_DURATION_RES`)
- `ep_golden_03_2k_grid_heavy` — same 20-minute timeline, 100 locked `A1`–`J10` anchors

Each pack is `1200000 ms`: `780000` code/FOIA (`13.0 min`), `340000` `STILL_2K_PANZOOM` (`5.67 min`), `80000` `FLOW_HERO_VIDEO` (`1.33 min`). `max_hero_clips = 10`, `max_hero_duration_sec = 80`. Scene plans are `EDITED_APPROVED`.

`prompt_mode` on `FLOW_HERO_VIDEO` and `flow_job_cards` is only `TEXT_TO_VIDEO` (4), `FIRST_FRAME` (3), or `FIRST_AND_LAST_FRAME` (3). Non-paid scene plans use `NONE`, which is the v4 `scene_plans` CHECK value for engines that are not video jobs. Retired ids (`FRAMES_MOTION_ONLY`, `VEO_3_1_LITE`, `CrimeScenePanZoom`) are absent.

Code/FOIA motifs are the `MOTIF_REGISTRY_V1` MVP four: `StickmanStage`, `AudioEvidenceCard`, `RedactedDocReveal`, `FoiaFootageFrame`. 2K plates use `Illustrative2KPanZoom` with `is_illustrative_reconstruction = 1`, `lock_status = LOCKED`, and the label `ILLUSTRATIVE RECONSTRUCTION — NOT CRIME SCENE PHOTO`. Hero fallbacks are `STILL_2K_PANZOOM` and are never adjacent to a 2K neighbor. Same-engine streaks stay at or under `50.0 s`.

`episode_analytics.adsense_status` is `UNKNOWN` and `adsense_source` is `UNAVAILABLE`. CTR, retention, and RPM are null. No monetization field is present. Spend reservations are `OFFLINE_TEST` at `$0`.

`packages/shared_contracts` is not in this worktree. `fixtures/validate_golden.py` checks the packs against `fixtures/golden_pack.schema.json` (field names from `schema/pipeline.sql` v4 and the Task 002 contract list) plus the runtime invariants. Stdlib only.

## Synthetic media

ffmpeg/x264 are not installed. The bodycam file is a real ISO-BMFF MP4 (`ftyp`/`moov`/`mdat`) with 16-bit PCM `sowt` audio, written by the Python stdlib. The 0:42 profanity locus is `profanity_intervals_json.start_ms = 42000` on the FOIA asset. The 8 s excerpt also has a 1440 Hz marker at 2.0 s. See `fixtures/synthetic_media/media_notes.json`.

| File | Bytes | Duration |
|---|---:|---:|
| `fixtures/synthetic_media/911_8khz_distorted.wav` | 96044 | 6.000 s @ 8000 Hz |
| `fixtures/synthetic_media/911_spoken_pii.wav` | 160044 | 5.000 s @ 16000 Hz |
| `fixtures/synthetic_media/bodycam_440hz_music_042profanity.mp4` | 128549 | 8.000 s @ 8000 Hz PCM |
| `fixtures/synthetic_media/keyframes/hero_start_charcoal.png` | 231 | monochrome, 0 crimson |
| `fixtures/synthetic_media/keyframes/hero_end_slate_amber.png` | 233 | monochrome, 0 crimson |
| `fixtures/synthetic_media/plates/plate_00.png` … `plate_06.png` | 8677–8727 | 1920×1080, 0 crimson |

Spoken-PII transcript (`406-555-0142`, `18 Fixture Lane`) stays in `911_spoken_pii.transcript.json` and is not copied into scene plans. Recorded API mocks have no live calls and no keys. `fixtures/recorded_apis/adversarial_prompt_injection.json` contains `</data>` breakouts.

## Validator

```
python fixtures/validate_golden.py
```

```
GOLDEN FIXTURE VALIDATOR v4
schema: fixtures/golden_pack.schema.json
PASS ep_golden_01_20min scenes=36 anchors=14 heroes=10 runtime_ms=780000/340000/80000
PASS ep_golden_02_2strike_fallback scenes=36 anchors=14 heroes=10 runtime_ms=780000/340000/80000
PASS ep_golden_03_2k_grid_heavy scenes=36 anchors=100 heroes=10 runtime_ms=780000/340000/80000
PASS recorded_apis youtube_videos_list.json courtlistener_search.json muckrock_foia_requests.json adversarial_prompt_injection.json
PASS media 911_8khz_distorted.wav bytes=96044 duration_s=6.000 rate=8000
PASS media 911_spoken_pii.wav bytes=160044 duration_s=5.000 rate=16000
PASS media bodycam_440hz_music_042profanity.mp4 bytes=128549 duration_s=8.000 rate=8000 coding=sowt
PASS keyframes_and_plates crimson_pixels=0
RESULT pass=3 packs + recorded_apis + synthetic_media fail=0
```

Narration PCM under `fixtures/synthetic_media/voice_slots/` and the `sources/*.txt` paths inside primary documents are logical references. They are not generated binaries.
