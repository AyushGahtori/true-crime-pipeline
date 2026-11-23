# Research: Per-Track Audio Mastering, Honest ASR Disagreement & SQLite Ops (`F-15`, `F-22`)

*Last verified: 2026-11-23*

## 1. Verified External Technical Standards
- **SQLite WAL Runtime Requirement (`F-22`):** SQLite WAL mode requires all processes accessing a database to reside on the **same local host** (network filesystems such as SMB/NFS do not safely support shared-memory `-shm` WAL locking). In addition, SQLite documented a WAL-reset concurrency bug fixed in **SQLite 3.51.3**. Source: [SQLite Write-Ahead Logging Documentation](https://www.sqlite.org/wal.html).
  - *Design Impact:* Startup enforces `sqlite3.sqlite_version_info >= (3, 51, 3)`, rejects SMB/NFS/UNC paths, uses a single Python writer (`BEGIN IMMEDIATE`, `busy_timeout = 5000`), and runs verified daily `VACUUM INTO` hot backups.
- **Broadcast Loudness Target (`-14.0 LUFS`, `<= -1.0 dBTP`):** Standard YouTube loudness normalization target. Pre-normalizing Track 1 (`-16 LUFS` + de-esser), Track 2 (`-18 LUFS` telephony bandpass + comp), and Track 3 (`-22 / -36 LUFS` ducked bed) independently before a two-pass measured **`linear=true`** FFmpeg `loudnorm` pass prevents dynamic AGC pumping across quiet pauses and loud 911 audio.

## 2. Music-Gated Demucs & Honest ASR Disagreement Metric (`F-15`)
- **Why Unconditional Demucs Fails on 911 Calls:** Music source-separation models (`htdemucs`, trained on `44.1 kHz` stereo music) introduce phase distortion on narrowband `8 kHz` mono telephony speech. Invoke Demucs **only** on segments where music detection triggers (`music_detected = 1`).
- **Correction of Misnamed `delta_WER` (`F-15`):** Comparing pre-Demucs ASR text against post-Demucs ASR text is **ASR hypothesis disagreement**, NOT Word Error Rate (WER requires a manually verified ground-truth reference transcript; two ASR runs can share identical misrecognitions).
  - **Offline Benchmark Suite (`tests/audio_corpus/`):** Measures true **`labeled_corpus_wer`** against human-transcribed reference clips.
  - **Production Runtime Gate:** Logs **`asr_hypothesis_disagreement`** in `foia_media_assets`; any clip exceeding `0.10` (or low ASR token confidence) sets `human_audio_review_required = 1` for mandatory human listening before export.
