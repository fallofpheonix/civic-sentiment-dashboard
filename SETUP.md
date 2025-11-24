# 🚀 Deployment Setup Guide

## API Configuration

### 1. Twitter API Setup
1. Get credentials from [Twitter Developer Portal](https://developer.twitter.com/)
2. Add to `.streamlit/secrets.toml`:
```toml
TWITTER_BEARER_TOKEN = "your_bearer_token_here"
TWITTER_API_KEY = "your_api_key_here" 
TWITTER_API_SECRET = "your_api_secret_here"
2. News API Setup
Get API key from NewsAPI.org

Add to .streamlit/secrets.toml:

toml
NEWS_API_KEY = "your_news_api_key_here"
3. Streamlit Cloud Deployment
Go to share.streamlit.io

Connect your GitHub repository

Add secrets in the dashboard under "Advanced settings"

Deploy!

Local Development
bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run emotional_weather_map_pro.py
File Structure
text
civic-sentiment-dashboard/
├── app.py                          # Basic sentiment dashboard
├── emotional_weather_map.py        # Intermediate GIS version
├── emotional_weather_map_pro.py    # Complete Project #26 (MAIN APP)
├── requirements.txt               # Dependencies
├── .streamlit/secrets.toml       # API keys (NOT in git)
└── README.md                     # Documentation
Troubleshooting
If APIs fail, app falls back to realistic mock data

Check API quotas in Twitter/News developer portals

Ensure secrets.toml is in .streamlit/ folder
