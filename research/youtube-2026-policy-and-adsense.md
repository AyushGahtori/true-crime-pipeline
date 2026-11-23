# Research: YouTube YPP Policy, Component Rights (`17 U.S.C. § 105`) & PII Risk Controls (`F-13`, `F-14`, `F-15`)

*Last verified: 2026-11-23*

## 1. Verified External Policy & Legal Sources
- **YouTube Partner Program (YPP) Inauthentic/Repetitious Content Policy Clarification (July 2025):** Clarified enforcement against mass-produced, templated, or repetitious content (note: previously misdated as "July 2026" in v1/v2 drafts — corrected here). Source: [YouTube Official Blog — July 2025 YPP Clarification](https://support.google.com/youtube/blog/356734251/response-to-creator-questions-about-ypp-policies-july-2025?hl=en-AS).
  - **Key Engineering Principle (`F-13`):** YouTube monetization evaluation is contextual and channel-level. Automated checks ("That vs. How" linter, profanity bleeping, visual variety) are **risk controls**, NEVER deterministic guarantees of green AdSense icons!
- **Scope of 17 U.S.C. § 105 (Federal Works):** Excludes from U.S. copyright protection *only* works prepared by an officer or employee of the U.S. Government as part of that person's official duties. A FOIA release does **not** convey reuse rights for contractor-produced media, third-party Ring/store CCTV, or copyrighted attachments inside a public dossier. Source: [U.S. Copyright Office — Title 17, Chapter 1](https://www.copyright.gov/title17/92chap1.html).
- **YouTube API Services Developer Policies (30-Day Retention):** Requires refreshing or deleting stored YouTube API data on documented retention intervals. Source: [YouTube API Services Developer Policies](https://developers.google.com/youtube/terms/developer-policies/).

## 2. Pipeline Risk Controls & Mandatory Human Sign-Off
- **Component-Level Rights Provenance (`foia_media_assets`):** Every asset records `creator_entity`, `rights_holder`, `license_basis`, `contains_third_party_attach`, and `rights_review_status` (`RESTRICTED_NO_REUSE` blocked by SQLite `CHECK`). Wikimedia files require per-file `extmetadata.LicenseShortName` verification (`CC0` / `Public Domain` only).
- **Standing Disposition & Auto-Quarantine:** `trg_case_disposition_guard_insert/update` + `trg_case_disposition_quarantine` block non-affirmed convictions on both INSERT and UPDATE and automatically quarantine downstream episodes if a conviction is later reversed/vacated.
- **Fallible Detectors + Mandatory 5-Gate Human Release Approval:** Automated face/plate blur, spoken PII NER, profanity mapping, and illustrative labels are fallible aids; an accountable named reviewer MUST approve all 5 `release_approvals` gates (`FACTUAL_ACCURACY`, `PRIVACY_PII`, `SOURCE_RIGHTS`, `SYNTHETIC_DISCLOSURE`, `ILLUSTRATIVE_LABELING`) before export.
- **Honest Labeling (`F-05`):** Generated 2K stills carry `ILLUSTRATIVE RECONSTRUCTION — NOT CRIME SCENE PHOTO`; TTS-voiced quotes carry `TRANSCRIPT DRAMATIZATION`.
