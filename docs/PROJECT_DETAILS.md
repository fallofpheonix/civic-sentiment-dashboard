# Project Details

## Name
`civic-sentiment-dashboard`

## Objective
Provide civic sentiment intelligence from social/news/government-like signals, with geographic emotion visualization and risk-oriented indicators.

## Scope
- Sentiment and emotion analysis of civic discourse.
- Dashboard delivery through Streamlit.
- GIS visualization through Folium.
- Multi-source ingestion (`Mock`, `Twitter API`, `News API`, simulated government feed).
- Forecast and risk/urgency features in Pro variant.

## Implemented Applications
- `app.py`: baseline sentiment dashboard (TextBlob + VADER).
- `emotional_weather_map.py`: GIS emotional map with forecast and weather analogies.
- `emotional_weather_map_pro.py`: multi-source, risk metrics, and production-oriented UI.

## Primary Data Flow
1. User selects city/topics/data sources.
2. App fetches live or mock data.
3. Text is scored (VADER + keyword heuristics for advanced emotion metadata).
4. Records are aggregated by region/topic/time.
5. KPIs, maps, alerts, and trends are rendered.

## Non-Functional Characteristics
- Runtime: interactive Streamlit session.
- Failure behavior: partial graceful fallback to mock data.
- Determinism: low (randomized mock generation without fixed seed).
- Security posture: mixed (Twitter token via secrets; News key currently hardcoded in Pro file).
