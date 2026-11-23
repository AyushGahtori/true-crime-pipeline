# Research: Code-to-Video LLM Roles, Cache Non-Guarantee & Craft Rubric (v4)

*Last verified: 2026-11-23*

## 1. DeepSeek Context Caching: Best-Effort Estimate, Not Guaranteed (`Additional Check #1`)
- DeepSeek documents [Context Caching](https://api-docs.deepseek.com/guides/kv_cache/) as **best-effort** (`cached_input_tokens <= total_input_tokens`). Byte-0 prefix ordering improves hit probability across sequential requests within a session, but **cache hits are NEVER guaranteed**.
- **Budgeting Rule:** Economics planning carries both a **Conservative `0%`-Cache Projection (`~$2.80–$3.80/ep` = `$28–$38/mo`)** reserved cleanly inside `monthly_budget_ledger` (`deepseek_chat: $38/mo`) AND a best-effort cached projection (`~$0.75–$1.90/ep`). Global `$135/mo` (`ALL_PROVIDERS`) solvency holds even with **0% cache hits**.

## 2. Config-Driven Model Roles & Craft Modularity (`F-05`, `F-06`)
- Model checkpoints load strictly from `providers.yaml` (`DeepSeek-V4.1-Flash-1017` scripting/ledger/manifest, `DeepSeek-V4-Pro-0813` contradiction reasoning).
- Prompt inputs separate concise `craft_rubric.yaml` (`<= 150 lines`, clear documentary pacing checks) -> episode research -> typed `ScenePlan` rows (`scene_plans`), eliminating brittle 4,000-line prompts.
- External untrusted text extraction runs **tool-less**, schema-constrained (`extra="forbid"`), and delimiter-sanitized (`Additional Check #2`).
