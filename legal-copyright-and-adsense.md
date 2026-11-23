# Agent 3: Legal, Component Rights Provenance, Spoken+Visual PII & Human Release Sign-Off (v3)

Agent 3 enforces measurable risk controls against Copyright Strikes, Reused/Inauthentic Content policy enforcement, Privacy Complaints, Defamation liability, and AdSense yellow-icon triggers—paired with a **mandatory named human release approval gate** (`F-05`, `F-06`, `F-13`, `F-14`, `F-15`). Diagram: [legal-copyright-and-adsense.mmd](legal-copyright-and-adsense.mmd). Research: [youtube-2026-policy-and-adsense.md](research/youtube-2026-policy-and-adsense.md).

> **Policy & Legal Realism (`F-13`):** Automated checks (regex, NER, YOLO, ASR, Vision QA) are **fallible risk controls**, NEVER guarantees of legal immunity or YouTube monetization approval. YouTube's Partner Program review (clarified in **July 2025** regarding inauthentic/mass-produced content) is contextual and channel-level.

## 1. Component-Level Rights Provenance (`F-14`: FOIA Access != Reuse Permission)

Domain-level whitelisting and blanket federal public-domain assumptions are legally invalid. Under **17 U.S.C. § 105** ([U.S. Copyright Office, Title 17](https://www.copyright.gov/title17/92chap1.html)), copyright exclusion applies **solely to works prepared by an officer or employee of the U.S. Government as part of that person's official duties**. A FOIA release NEVER transfers copyright in embedded third-party, bystander, contractor-produced, or news attachments!

Every record in `foia_media_assets` requires explicit asset- and component-level provenance before approval:
1. **`creator_entity` & `rights_holder`:** Identify who actually created each sub-clip or embedded file (federal employee vs. state agency vs. private contractor vs. private citizen Ring/store CCTV vs. local news clip).
2. **`license_basis` Enum:** Strictly classified into `US_FED_EMPLOYEE_17USC105`, `STATE_PUBLIC_RECORD_PERMITTED` (checked against state-specific commercial/death-record statutes such as FL Sunshine Law / WA PRA), `CC0_PUBLIC_DOMAIN` (Wikimedia API `extmetadata.LicenseShortName` verified per file—rejecting `CC BY-NC`/`CC BY-SA`), `EXPLICIT_LICENSE_GRANT`, `FAIR_USE_REVIEW_REQUIRED`, or `RESTRICTED_NO_REUSE`.
3. **Attachment Quarantine (`contains_third_party_attach`):** Private doorbell video, store CCTV, contractor footage, or newspaper scans embedded inside public FOIA ZIPs default to `RESTRICTED_NO_REUSE` and are blocked by SQLite `CHECK` constraints from being approved for reuse without explicit clearance.
4. **News Sites & Third-Party YouTube URLs:** Metadata/text leads only; zero media bytes retained.

## 2. Music-Gated Demucs + Honest ASR Disagreement & Labeled Corpus WER (`F-15`)

Running `htdemucs` unconditionally on `8 kHz` mono telephony 911 calls degrades frantic speech:
1. **Ingest Normalization First:** Normalize cleared FOIA media deterministically to **`CFR 30 fps`, `48 kHz stereo PCM`, `yuv420p`** (`normalized_cfr_30fps_48k = 1`).
2. **Music Detection Gate:** Run lightweight audio classifier across the clip; invoke Demucs **only** on intervals where background music confidence exceeds threshold (`music_detected = 1`). Clean speech bypasses Demucs completely.
3. **Honest Intelligibility Metrics (`F-15`):**
   - **Offline Labeled Test Corpus WER (`labeled_corpus_wer`):** True Word Error Rate measured strictly against **manually transcribed ground-truth reference transcripts** during QA benchmarking (`tests/audio_corpus/`).
   - **Production ASR Disagreement (`asr_hypothesis_disagreement`):** Token edit distance between pre-Demucs and post-Demucs ASR hypotheses. Because two ASR runs can share identical misrecognitions, disagreement is NEVER called WER; when `asr_hypothesis_disagreement > 0.10` (or audio confidence drops), set `human_audio_review_required = 1` so a human listens before export!

## 3. Whole-Clip Profanity Map, Visual + Spoken PII & Illustrative Labeling (`F-05`)

- **Whole-Clip Profanity Map:** Scan the entire FOIA track via word-timestamped ASR (`profanity_intervals_json`) and bleep any slice entering episode `0:00–0:30` plus severe slurs anywhere.
- **Visual & Spoken PII Scrubbing (Human-Verified):** OpenCV/YOLO face/plate blur (`sigma >= 25`) + ASR NER/regex spoken caller-name/address/phone/DOB/juvenile bleeping, explicitly verified during human release review because automated detectors are fallible.
- **Illustrative Reconstruction & Dramatization Labels (`F-05`):**
  - Every generated 2K room plate (`still_assets.is_illustrative_reconstruction = 1`) and synthetic Hero scene MUST display a persistent subtle **`ILLUSTRATIVE RECONSTRUCTION — NOT CRIME SCENE PHOTO`** label so viewers never confuse generated room geometry with forensic crime-scene photographs.
  - Every TTS-voiced transcript excerpt inside `AUDIO_EVIDENCE_CARD` MUST display **`TRANSCRIPT DRAMATIZATION`**.

## 4. Mandatory 5-Gate Human Release Sign-Off & Post-Publish Correction/Takedown SOP (`F-06`)

No episode can transition to `READY_TO_UPLOAD` or `PUBLISHED` (enforced by SQLite trigger `trg_episode_release_gate`) until an accountable named reviewer signs off ALL 5 gates in `release_approvals` against the exact `ready_bundle_sha256`:
1. `FACTUAL_ACCURACY` (every narrative allegation corroborated against primary `fact_ledger` citations + standing conviction status)
2. `PRIVACY_PII` (`cases.anonymization_status = 'APPROVED'`, spoken & visual bystander/juvenile PII verified)
3. `SOURCE_RIGHTS` (every FOIA/archival component verified `rights_review_status = 'APPROVED'`)
4. `SYNTHETIC_DISCLOSURE` (YouTube Studio Altered/Synthetic Content disclosure checkbox confirmed)
5. `ILLUSTRATIVE_LABELING` (all generated 2K stills/reconstructions clearly labeled illustrative & non-misleading)

### Post-Publish Correction, Takedown & Case-Update Procedure (`F-03`, `F-06`)
- **Automated Disposition Watch:** Updating `cases.disposition_status` to `REVERSED`, `VACATED`, `ACQUITTED`, or `PENDING` triggers `trg_case_disposition_quarantine`, immediately flipping downstream episodes to `QUARANTINED_LEGAL_HOLD` and revoking `release_approvals`.
- **Published Episode Takedown / Correction SLA:** If a published episode's underlying conviction is reversed/vacated or a factual/privacy error is reported, the accountable editor must within `24 hours`: (1) set the YouTube video to Unlisted/Private pending review (or take down immediately for defamation/privacy risk), (2) log an entry in `audit_log` (`POST_PUBLISH_CORRECTION` / `TAKEDOWN`), and (3) issue a pinned correction or re-cut release passing all 5 gates fresh.
