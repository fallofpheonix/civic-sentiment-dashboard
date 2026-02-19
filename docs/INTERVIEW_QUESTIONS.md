# Interview Questions

## System and Data
1. Describe end-to-end data flow from user input to map rendering.
2. How would you make mock-data generation reproducible for testing?
3. Where are bottlenecks if post volume scales from 100 to 100,000 per refresh?
4. What schema would you persist for replayable historical analysis?
5. How would you isolate source reliability by provider (Twitter vs News vs Gov)?

## NLP and Modeling
1. Why combine VADER with keyword heuristics instead of a transformer classifier?
2. What are failure modes of lexicon-based sentiment for civic text?
3. How would you calibrate sentiment thresholds per domain/topic?
4. Design a validation dataset and metrics (precision/recall/F1) for risk labels.
5. How would you detect concept drift in civic discourse over time?

## Security and Compliance
1. Identify secret-management gaps and remediation steps.
2. How should API keys rotate in local and cloud deployments?
3. Which logs must be redacted to avoid leaking sensitive tokens/content?
4. What privacy constraints apply to social-content processing pipelines?

## Reliability and Operations
1. Define SLOs for dashboard latency and ingestion freshness.
2. What retry/backoff strategy is appropriate for upstream API errors?
3. How would you implement circuit breaking when a provider degrades?
4. What observability signals would you add first (metrics, traces, structured logs)?

## Engineering Execution
1. Propose a minimal refactor to separate UI, ingestion, and analytics modules.
2. What test pyramid is appropriate for this codebase?
3. Which components should be made deterministic before CI gating?
4. How would you package this as a deployable service beyond Streamlit?
