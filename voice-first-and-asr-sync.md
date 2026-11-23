# Voice-First Segmented Timeline, WhisperX Word Alignment & Proper-Noun Gate (v4)

To align visuals to spoken audio within milliseconds without triggering `RULE_01` collisions on silent-TTS FOIA segments—and to match **real documented ASR API limits** (`F-03`)—Voice-First separates audio synthesis, **local forced word alignment**, and optional bounded cloud transcription cleanly. Diagram: [voice-first-and-asr-sync.mmd](voice-first-and-asr-sync.mmd).

## 1. Config-Driven TTS Providers & Per-Chunk Loudness/EQ Consistency

- **Provider Registry (`providers.yaml`):** Model IDs, token rates, and RPM caps load from `providers.yaml`.
- **1–3 Minute Chunking & Consistency:** Split approved `scene_plans` narration into coherent chunks (`1–3 min`), inject an identical directing style prefix per call, normalize locally to `48 kHz stereo PCM` for mastering, and apply per-chunk `-16.0 LUFS` + spectral tilt matching.

## 2. Explicit Word-Timestamp Ownership: Local WhisperX Forced Aligner (`F-03`)

DeepSeek's Speech-to-Text API ([DeepSeek Speech-to-Text Docs](https://api-docs.deepseek.com/guides/asr/)) documents a hard **`8 MiB` max file size**, **`120 seconds` max audio duration**, and **does NOT provide word-level millisecond timestamps**. Feeding 1–3 minute `48 kHz` stereo PCM WAVs (`~11.5 MB/min`) to DeepSeek ASR and expecting word-level timestamps fails immediately!

Therefore, ownership is split explicitly:
1. **Sole Word-Level Timestamp Owner (`Task 066`):** Local **`WhisperX` forced aligner** (`whisperx-local` + Phoneme Wav2Vec2 alignment) runs offline ($0 API cost!) against the already-synthesized `NARRATION` audio + known script text, emitting exact millisecond `WordTimestamp[]` mapped onto global `total_master_ms`.
2. **Optional Cloud ASR Transcription (`Task 067` — Raw FOIA / Unscripted Audio Only):** If Gemini Transcribe or DeepSeek Speech-to-Text is ever called for unscripted raw FOIA/911 speech-to-text, audio MUST first be transcoded via FFmpeg into **`16 kHz` mono FLAC sliced strictly `<= 90 seconds` (`< 4 MiB`, guaranteeing `< 8 MiB` & `<= 120s` limits!)**, followed by WhisperX forced alignment if word timestamps are needed.
3. **Proper-Noun Pronunciation Gate (`Task 068`):** Compare un-forced local Whisper ASR hypotheses against ground-truth suspect, victim, street, and county names (`Metaphone` + edit distance). Trigger phonetic respelling retry BEFORE rendering any paid visuals!

## 3. Segmented `VoiceTrackManifest` (`Narration` + `FOIA Slots` + `Twist Pads`)

1. **`NARRATION` Segments (`audio_path NOT NULL`):** TTS speech linked by SHA-256 to `scene_plans.narration_version_sha256`.
2. **`TWIST_PAD` Segments (`0.45s–0.75s`):** Room-tone noise floor (`-65 dBFS`, never digital zero).
3. **`FOIA_AUDIO_SLOT` Segments (`foia_asset_id NOT NULL`):** Silent Track-1 intervals matching Track-2 FOIA audio + L-cuts (`0.6s–1.0s`).
4. **Non-Overlapping Integrity:** SQLite triggers `trg_voice_segments_no_overlap_insert/update` forbid gaps or overlaps within an episode.
