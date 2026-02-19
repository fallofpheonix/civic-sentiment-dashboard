# Future Changes

## Priority 0 (Security/Correctness)
- Move News API key to secrets manager and remove hardcoded key from code.
- Add input/output validation around all external API payloads.
- Add deterministic mode for mock-data generation (seed control).

## Priority 1 (Architecture)
- Split monolithic scripts into modules:
  - `ingestion/`
  - `analysis/`
  - `mapping/`
  - `ui/`
- Centralize config and thresholds in one typed settings object.

## Priority 2 (Reliability)
- Add structured logging and request-level correlation IDs.
- Add retries with exponential backoff and jitter.
- Cache source calls with TTL to control rate-limit pressure.

## Priority 3 (Quality)
- Add unit tests for sentiment/emotion/risk functions.
- Add integration tests with recorded API fixtures.
- Add static analysis (`ruff`, `mypy`) and CI gate.
