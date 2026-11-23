# Research: Segmented Voice-First Timeline, WhisperX Word Alignment & Sync (v4 · `F-03`)

*Last verified: 2026-11-23*

## 1. Verified API Limits & Explicit Alignment Ownership (`F-03`)
- **DeepSeek Speech-to-Text (`https://api-docs.deepseek.com/guides/asr/`):** Hard limit of **`8 MiB` file size** and **`120 seconds` audio duration**, and its response schema **does NOT return word-level timestamps**.
  - *Math Check:* `48 kHz` 16-bit stereo PCM WAV produces `~11.52 MB/min`, immediately overflowing the `8 MiB` limit in `< 42 seconds` and overflowing `120s` on 3-minute narration chunks!
- **Canonical v4 Solution:**
  1. **Local WhisperX Forced Alignment (`whisperx-local`):** Sole owner of millisecond `WordTimestamp[]` for scripted TTS `NARRATION` segments (`$0.00` cost, no file-size or duration cap, phoneme-level forced alignment against known text).
  2. **Bounded Optional Cloud Transcription (`16 kHz` Mono FLAC `<= 90s`):** Any optional DeepSeek/Gemini cloud ASR transcription for raw unscripted FOIA/911 speech first slices and transcodes audio to `16 kHz` mono FLAC (`<= 90s`, typically `< 1.5–4.0 MiB` — well inside `8 MiB` and `120s`), and never substitutes for WhisperX forced alignment.

## 2. Segmented Timeline & Loudness Consistency
- Ordered, non-overlapping `voice_segments` (`NARRATION`, `FOIA_AUDIO_SLOT`, `-65 dBFS` `TWIST_PAD`) locked by SHA-256 to `scene_plans.narration_version_sha256`.
- Local `CFR 30 fps` / `48 kHz stereo PCM` normalization + phonetic proper-noun diff check prior to rendering.
