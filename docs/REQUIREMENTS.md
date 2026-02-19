# Requirements

## Functional Requirements
- Topic-based civic sentiment analysis.
- Region/city filtering and map visualization.
- Multi-source ingestion with graceful fallback.
- Emotion and risk indicators for decision support.
- Exportable and reviewable analysis outputs.

## Non-Functional Requirements
- Response latency suitable for interactive dashboard use.
- Deterministic test mode for CI.
- Secure secret handling for all API credentials.
- Fault tolerance for source outages/timeouts.
- Traceable logs for incident diagnosis.

## Environment Requirements
- Python 3.13 runtime.
- Streamlit-compatible host (local or cloud).
- Network egress for external APIs.
- `.streamlit/secrets.toml` for credentials.

## Current Gaps
- Full credential externalization not complete.
- CI test and quality gates not defined in repository.
- No persistent data layer for historical analytics.
