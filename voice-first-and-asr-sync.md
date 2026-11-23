# Voice-First Segmented Timeline, Proper-Noun Check & Millisecond ASR Sync

To prevent `RULE_01` from colliding with Law 6 silent-TTS FOIA playback slots, the Voice-First stage models audio as a **segmented timeline** (`NarrationSegment` + `FoiaAudioSlot` + room-tone `TwistPad`) rather than one monolithic continuous TTS file. Diagram: [voice-first-and-asr-sync.mmd](voice-first-and-asr-sync.mmd).

## 1. Config-Driven TTS Providers & Per-Chunk Loudness/EQ Consistency

- **Provider Registry (`providers.yaml`):** Model IDs (`gemini-3.8-flash-tts`, `gemini-3.8-flash-lite-tts`, `deepseek-tts`), token rates (`25 audio tok/sec`), and RPM caps load from config rather than hardcoded constants.
- **1–3 Minute Chunking & Consistency:** Split narration into `1–3 min` segments (`<= 4,500` audio tokens, safely under `16,384` cap), inject an identical directing style prefix per call, normalize each chunk to `48 kHz stereo PCM`, and apply **per-chunk LUFS (`-16 LUFS`) + spectral tilt matching** so acoustic energy never shifts across chunk seams!

## 2. Segmented `VoiceTrackManifest` (`Narration` + `FOIA Slots` + Room-Tone `Twist Pads`)

1. **`NARRATION` Segments:** Synthesized TTS chunks containing `word_timestamps[]` and `amplitude_envelope[]` (`30 fps`).
2. **`TWIST_PAD` Segments (`0.45s–0.75s`):** Spliced low-level room-tone noise floor (`-65 dBFS`, **never digital zero silence**, avoiding audio-dropout feel) after `is_plot_twist: true` beats.
3. **`FOIA_AUDIO_SLOT` Segments:** Explicit silent Track-1 intervals reserved deterministically for Track-2 Demucs-cleaned 911/bodycam playback (plus `0.6s–1.0s` L-cut visual lead-in!).
4. **`total_master_ms`:** Computed as `sum(NARRATION) + sum(FOIA_AUDIO_SLOT) + sum(TWIST_PAD)`. `RULE_01` validates `abs(sum(scene_durations_ms) - total_master_ms) <= 250 ms`!

## 3. Millisecond ASR Sync & Free Proper-Noun Pronunciation Diff

- Run DeepSeek Speech-to-Text ASR (`$0.116/hr` / `$0.058` promo) or local WhisperX on every synthesized narration segment to extract exact `word_timestamps[]`.
- **Proper-Noun Phonetic Diff Check:** Compare ASR transcript tokens against ground-truth suspect names, victim names, streets, and towns using phonetic similarity (Metaphone/Soundex + edit distance). Flag mangled pronunciations (`"Krzysztof"` -> `"Kristoff"` or garbled town names) and trigger phonetic respelling retry BEFORE spending any render compute!
