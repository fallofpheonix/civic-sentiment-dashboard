# Tasks

## Current Backlog

## Security and Compliance
- [ ] Remove hardcoded News API key from `emotional_weather_map_pro.py`.
- [ ] Read `NEWS_API_KEY` only from `.streamlit/secrets.toml`.
- [ ] Add startup check to fail closed when secure mode is required.

## Engineering Quality
- [ ] Refactor duplicated logic across `app.py`, `emotional_weather_map.py`, `emotional_weather_map_pro.py`.
- [ ] Add deterministic mock-data mode for reproducible tests.
- [ ] Extract pure functions for analysis to improve testability.

## Testing
- [ ] Add unit tests for sentiment/emotion/risk classification.
- [ ] Add integration tests for Twitter/News parsing and fallbacks.
- [ ] Add smoke test for Streamlit app startup.

## Observability
- [ ] Add structured logs for provider calls and failure causes.
- [ ] Add metrics counters for source success/error/timeout.

## Documentation
- [ ] Keep changelog synchronized with merges.
- [ ] Fix Markdown formatting issues in `SETUP.md`.

## Suggested Order
1. Security fixes.
2. Test harness.
3. Refactor.
4. Observability and performance tuning.
