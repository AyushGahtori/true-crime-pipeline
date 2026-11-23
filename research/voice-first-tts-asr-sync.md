# Research: Segmented Voice-First Timeline, Proper-Noun Diff & Ingest Sync (`F-09`)

*Last verified: 2026-11-23*

- **Segmented Timeline Model (`voice_segments`):** Modeling Track 1 as ordered, non-overlapping `NARRATION` (requiring `audio_path`), `FOIA_AUDIO_SLOT` (requiring `foia_asset_id`), and `TWIST_PAD` segments (`sum == episodes.total_master_ms`) eliminates `RULE_01` conflicts during raw 911/bodycam playback. SQLite `BEFORE INSERT/UPDATE` triggers reject interval overlaps immediately.
- **Per-Chunk Consistency & Room-Tone Pads:** Matching per-chunk loudness (`-16.0 LUFS`) across `1–3 min` TTS segments prevents volume jumps; low-level room tone (`-65 dBFS`) prevents jarring digital silence cutouts.
- **ASR Proper-Noun Pronunciation Check:** Running phonetic diffing (`Metaphone` + edit distance) between ASR output and ground-truth suspect/location names flags TTS mispronunciations before rendering begins (treated as a fallible detector supplemented by human review).
- **Strict Ingest Parity:** All TTS and rights-cleared FOIA media normalize deterministically to `CFR 30 fps` (`1920x1080 yuv420p`) and `48 kHz stereo PCM` at ingest to prevent cumulative 20-minute concat drift.
