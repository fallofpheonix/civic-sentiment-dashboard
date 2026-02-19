# Technologies

## Runtime and Framework
- Python 3.13
- Streamlit 1.51

## Data and Analytics
- Pandas
- NumPy
- Scikit-learn (installed; minimal use in current visible flow)

## NLP
- VADER Sentiment
- TextBlob
- NLTK
- Transformers/Torch (installed; not core in current app paths)

## Visualization and GIS
- Matplotlib
- Seaborn
- Plotly (dependency available)
- Folium
- streamlit-folium

## Integrations
- Twitter API v2 via `requests`
- News API via `requests`

## Deployment/Config
- Streamlit Cloud compatible
- `.streamlit/secrets.toml` for secret injection (partially applied today)

## Technical Debt Notes
- `requirements.txt` is heavy for current usage surface.
- API integration and UI are tightly coupled in single files.
