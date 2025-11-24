import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import folium_static
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
import json
from datetime import datetime, timedelta
import numpy as np
import time
import random  # Missing import!

# Configure the page for professional deployment
st.set_page_config(
    page_title="Emotional Weather Map Pro",
    page_icon="🌤️",
    layout="wide"
)

# Enhanced CSS for professional appearance
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(90deg, #1E90FF, #00BFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem;
        color: white;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    .alert-card {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 5px solid #ff3838;
    }
    .data-source-badge {
        background: #2ecc71;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Initialize analyzer
vader_analyzer = SentimentIntensityAnalyzer()

# Title
st.markdown('<h1 class="main-header">🌤️ Emotional Weather Map Pro</h1>', unsafe_allow_html=True)
st.markdown("### Real-time Civic Intelligence Platform with Multi-Source Data Integration")

# Sidebar with enhanced configuration
st.sidebar.header("🌍 Platform Configuration")

# Data source selection
data_sources = st.sidebar.multiselect(
    "Data Sources:",
    ["Mock Civic Data", "Twitter API", "News API", "Open Government Data"],
    default=["Mock Civic Data", "Twitter API"]
)

# City and analysis configuration
cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia"]
selected_city = st.sidebar.selectbox("Target City:", cities)

focus_areas = ["Education", "Healthcare", "Transportation", "Environment", "Housing", "Public Safety"]
selected_focus = st.sidebar.multiselect("Policy Focus Areas:", focus_areas, default=focus_areas)

# Advanced analytics
st.sidebar.header("🔮 Predictive Analytics")
enable_forecasting = st.sidebar.checkbox("Enable Civil Unrest Prediction", True)
enable_needs_detection = st.sidebar.checkbox("Enable Community Needs Detection", True)

# Real-time settings
st.sidebar.header("⚡ Real-time Processing")
update_frequency = st.sidebar.selectbox("Update Frequency:", ["5 minutes", "15 minutes", "1 hour", "Manual"])
auto_refresh = st.sidebar.checkbox("Auto-refresh Dashboard", False)

# Mock API functions (replace with real APIs in production)
def fetch_twitter_data(city, topics, count=50):
    """Real Twitter API v2 with proper error handling"""
    try:
        # Get from Streamlit secrets (secure)
        bearer_token = st.secrets.get("TWITTER_BEARER_TOKEN", "")
        
        if not bearer_token:
            st.sidebar.warning("🐦 Twitter API not configured - using mock data")
            return generate_mock_social_data(city, topics, count, "Twitter")
        
        # Build smart search query based on topics
        topic_queries = {
            "Education": "(school OR teacher OR education OR student)",
            "Healthcare": "(hospital OR health OR medical OR doctor)", 
            "Transportation": "(transit OR traffic OR commute OR transportation)",
            "Environment": "(environment OR climate OR pollution OR green)",
            "Housing": "(housing OR rent OR apartment OR homeless)",
            "Public Safety": "(safety OR police OR crime OR emergency)"
        }
        
        # Combine selected topics
        topic_filters = []
        for topic in topics:
            if topic in topic_queries:
                topic_filters.append(topic_queries[topic])
        
        if not topic_filters:
            topic_filters = ["(community OR city OR local)"]
        
        query = f"({' OR '.join(topic_filters)}) ({city}) lang:en -is:retweet -is:reply"
        
        headers = {"Authorization": f"Bearer {bearer_token}"}
        params = {
            "query": query,
            "max_results": min(count, 50),  # Increased from 10 to 50
            "tweet.fields": "created_at,public_metrics,context_annotations,author_id",
            "expansions": "author_id"
        }
        
        st.sidebar.info(f"🐦 Searching Twitter for: {', '.join(topics)} in {city}...")
        
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/recent",
            headers=headers,
            params=params
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('data'):
                processed_tweets = process_twitter_data(data, city, topics)
                if processed_tweets:
                    st.sidebar.success(f"✅ Fetched {len(processed_tweets)} real tweets!")
                    return processed_tweets
        
        # If no tweets found or error
        st.sidebar.warning(f"🔍 No tweets found for current filters - using mock data")
        return generate_mock_social_data(city, topics, count, "Twitter")
            
    except Exception as e:
        st.sidebar.error(f"🐦 Twitter API error: {str(e)[:100]}...")
        return generate_mock_social_data(city, topics, count, "Twitter")


def process_twitter_data(twitter_response, city, topics):
    """Process raw Twitter API response into our format"""
    processed = []
    
    # Get user data if available
    users = {}
    if 'includes' in twitter_response and 'users' in twitter_response['includes']:
        for user in twitter_response['includes']['users']:
            users[user['id']] = user
    
    for tweet in twitter_response['data']:
        # Get user info if available
        author_info = users.get(tweet.get('author_id', ''), {})
        
        emotion_data = analyze_advanced_emotions(tweet['text'])
        
        # Truncate long tweets for display
        display_text = tweet['text']
        if len(display_text) > 280:
            display_text = display_text[:277] + "..."
        
        processed.append({
            "id": f"twitter_{tweet['id']}",
            "text": display_text,
            "source": "Twitter",
            "topic": classify_topic(tweet['text'], topics),
            "city": city,
            "timestamp": datetime.fromisoformat(tweet['created_at'].replace('Z', '+00:00')),
            "sentiment_score": emotion_data["sentiment_score"],
            "primary_emotion": emotion_data["primary_emotion"],
            "engagement": tweet['public_metrics']['like_count'] + tweet['public_metrics']['retweet_count'],
            "verified": author_info.get('verified', False),
            "risk_level": emotion_data["risk_level"],
            "urgency_level": emotion_data["urgency_level"],
            "user_followers": author_info.get('public_metrics', {}).get('followers_count', 0),
            "retweet_count": tweet['public_metrics']['retweet_count'],
            "like_count": tweet['public_metrics']['like_count']
        })
    
    return processed

def fetch_news_data(city, topics, count=30):
    """Real News API integration"""
    try:
        # Use your actual News API key
        api_key = "37cbeae280284824a36609781595ff4f"
        
        # Build query - search for topics in the city
        query_terms = " OR ".join([f'"{topic}"' for topic in topics])
        query = f"({query_terms}) AND ({city})"
        
        # News API endpoint
        url = f"https://newsapi.org/v2/everything?q={query}&pageSize={min(count, 30)}&sortBy=publishedAt&language=en&apiKey={api_key}"
        
        st.sidebar.info(f"📰 Fetching news about {', '.join(topics)} in {city}...")
        
        response = requests.get(url)
        data = response.json()
        
        if data.get('status') == 'ok' and data.get('articles'):
            processed_articles = []
            for article in data['articles']:
                # Combine title and description for sentiment analysis
                article_text = f"{article['title']} - {article.get('description', '')}"
                
                emotion_data = analyze_advanced_emotions(article_text)
                
                processed_articles.append({
                    "id": f"news_{article.get('publishedAt', '')}_{hash(article_text)}",
                    "text": f"{article['title']} - {article.get('description', 'No description')}",
                    "source": "News",
                    "topic": classify_topic(article['title'], topics),
                    "city": city,
                    "timestamp": datetime.fromisoformat(article['publishedAt'].replace('Z', '+00:00')) if article.get('publishedAt') else datetime.now(),
                    "sentiment_score": emotion_data["sentiment_score"],
                    "primary_emotion": emotion_data["primary_emotion"],
                    "engagement": 0,  # News articles don't have engagement metrics
                    "verified": True,
                    "risk_level": emotion_data["risk_level"],
                    "urgency_level": emotion_data["urgency_level"],
                    "url": article.get('url', ''),
                    "source_name": article.get('source', {}).get('name', 'Unknown')
                })
            
            st.sidebar.success(f"✅ Fetched {len(processed_articles)} real news articles")
            return processed_articles
        else:
            st.sidebar.warning(f"No news articles found for: {query}")
            # Fallback to mock data if no real articles found
            return generate_mock_social_data(city, topics, count, "News")
            
    except Exception as e:
        st.sidebar.error(f"News API Error: {e}")
        # Fallback to mock data on error
        return generate_mock_social_data(city, topics, count, "News")

def fetch_government_data(city, count=20):
    """Simulate Open Government Data API"""
    st.sidebar.info(f"🏛️ Fetching {count} civic reports from {city} open data portal")
    
    time.sleep(1)
    
    return generate_mock_government_data(city, count)

def generate_mock_social_data(city, topics, count, source):
    """Generate realistic social media and news data"""
    posts = []
    
    civic_issues = {
        "Education": [
            f"School funding debate heats up in {city}",
            f"{city} teachers demand better resources",
            f"New education initiative announced for {city} schools",
            f"Parent concerns about {city} school safety",
            f"Student achievements celebrated across {city}"
        ],
        "Healthcare": [
            f"Hospital capacity concerns in {city}",
            f"New healthcare clinic opens in {city}",
            f"{city} residents struggle with medical costs",
            f"Mental health services expand in {city}",
            f"Healthcare workers protest in {city}"
        ],
        "Transportation": [
            f"Public transit improvements needed in {city}",
            f"{city} commuters face daily traffic challenges",
            f"New bike lanes welcomed in {city}",
            f"Infrastructure projects underway across {city}",
            f"Transportation access issues in {city} neighborhoods"
        ],
        "Environment": [
            f"Air quality concerns raised in {city}",
            f"{city} launches new sustainability initiative",
            f"Community gardens thriving across {city}",
            f"Environmental protection efforts in {city}",
            f"Green space preservation in {city}"
        ],
        "Housing": [
            f"Affordable housing crisis in {city}",
            f"New housing developments in {city}",
            f"Rent control discussions in {city} council",
            f"Housing accessibility issues in {city}",
            f"Community housing projects in {city}"
        ],
        "Public Safety": [
            f"Public safety initiatives in {city}",
            f"Community policing efforts in {city}",
            f"Emergency response improvements in {city}",
            f"Neighborhood watch programs in {city}",
            f"Public safety concerns addressed in {city}"
        ]
    }
    
    for i in range(count):
        topic = random.choice(topics)
        text_options = civic_issues.get(topic, [f"Community discussion in {city}"])
        text = random.choice(text_options)
        
        emotion_data = analyze_advanced_emotions(text)
        
        posts.append({
            "id": f"{source.lower()}_{i}",
            "text": text,
            "source": source,
            "topic": topic,
            "city": city,
            "timestamp": datetime.now() - timedelta(hours=random.randint(0, 72)),
            "sentiment_score": emotion_data["sentiment_score"],
            "primary_emotion": emotion_data["primary_emotion"],
            "engagement": random.randint(10, 1000) if source == "Twitter" else random.randint(5, 100),
            "verified": random.choice([True, False]) if source == "Twitter" else True,
            "risk_level": emotion_data["risk_level"],
            "urgency_level": emotion_data["urgency_level"]
        })
    
    return posts


def classify_topic(title, topics):
    """Heuristic topic classifier for news titles.

    Returns the first topic that appears in the title (case-insensitive),
    otherwise returns a random topic from the provided list or 'General'.
    """
    if not title:
        return topics[0] if topics else "General"

    title_lower = title.lower()
    for t in topics:
        if t.lower() in title_lower:
            return t

    return random.choice(topics) if topics else "General"

def classify_topic(text, available_topics):
    """Classify text into one of the available topics based on keywords"""
    if not text:
        return random.choice(available_topics) if available_topics else "General"
    
    text_lower = text.lower()
    
    # Topic keywords mapping
    topic_keywords = {
        "Education": ['school', 'teacher', 'student', 'education', 'university', 'college', 'campus', 'tuition'],
        "Healthcare": ['hospital', 'health', 'medical', 'doctor', 'clinic', 'healthcare', 'medicine', 'patient'],
        "Transportation": ['transit', 'bus', 'train', 'traffic', 'transportation', 'commute', 'subway', 'highway'],
        "Environment": ['environment', 'pollution', 'green', 'sustainability', 'climate', 'recycling', 'clean energy'],
        "Housing": ['housing', 'rent', 'apartment', 'homeless', 'affordable', 'eviction', 'mortgage'],
        "Public Safety": ['safety', 'police', 'crime', 'emergency', 'fire', 'security', 'law enforcement']
    }
    
    # Count keyword matches for each topic
    topic_scores = {}
    for topic in available_topics:
        if topic in topic_keywords:
            score = sum(1 for keyword in topic_keywords[topic] if keyword in text_lower)
            topic_scores[topic] = score
    
    # Return topic with highest score, or random if no matches
    if topic_scores and max(topic_scores.values()) > 0:
        return max(topic_scores, key=topic_scores.get)
    else:
        return random.choice(available_topics) if available_topics else "General"

def generate_mock_government_data(city, count):
    """Generate realistic government open data"""
    reports = []
    
    report_types = [
        "Infrastructure Maintenance Request",
        "Public Safety Incident Report", 
        "Environmental Quality Alert",
        "Community Service Announcement",
        "Public Works Project Update"
    ]
    
    for i in range(count):
        report_type = random.choice(report_types)
        
        reports.append({
            "id": f"gov_{i}",
            "type": report_type,
            "city": city,
            "description": f"{report_type} in {city} - Status: {random.choice(['Open', 'In Progress', 'Resolved'])}",
            "priority": random.choice(["Low", "Medium", "High", "Critical"]),
            "timestamp": datetime.now() - timedelta(days=random.randint(0, 30))
        })
    
    return reports

def analyze_advanced_emotions(text):
    """Enhanced emotion detection with civil unrest indicators"""
    scores = vader_analyzer.polarity_scores(text)
    compound = scores['compound']
    
    # Civil unrest indicators
    unrest_keywords = ['protest', 'rally', 'demonstration', 'strike', 'outrage', 'anger', 'frustrated']
    urgency_keywords = ['urgent', 'emergency', 'crisis', 'immediate', 'now']
    
    text_lower = text.lower()
    unrest_risk = any(keyword in text_lower for keyword in unrest_keywords)
    urgency_level = any(keyword in text_lower for keyword in urgency_keywords)
    
    # Enhanced emotion classification
    if unrest_risk and compound < -0.3:
        primary_emotion = "Civil Unrest Risk"
        risk_level = "High"
    elif compound >= 0.5:
        primary_emotion = "Community Satisfaction"
        risk_level = "Low"
    elif compound >= 0.1:
        primary_emotion = "General Contentment" 
        risk_level = "Low"
    elif compound >= -0.1:
        primary_emotion = "Neutral Discussion"
        risk_level = "Low"
    elif compound >= -0.5:
        primary_emotion = "Community Concerns"
        risk_level = "Medium"
    else:
        primary_emotion = "Public Frustration"
        risk_level = "High"
    
    return {
        "primary_emotion": primary_emotion,
        "sentiment_score": compound,
        "unrest_risk": unrest_risk,
        "urgency_level": urgency_level,
        "risk_level": risk_level,
        "emotion_intensity": abs(compound)
    }

def predict_civil_unrest_risk(data):
    """Predict civil unrest risk based on emotional data"""
    if not data:
        return {"risk_level": "Low", "confidence": 0.0, "factors": []}
    
    high_risk_posts = [p for p in data if p.get('risk_level') == 'High']
    medium_risk_posts = [p for p in data if p.get('risk_level') == 'Medium']
    
    risk_ratio = len(high_risk_posts) / len(data) if data else 0
    urgency_count = len([p for p in data if p.get('urgency_level')])
    
    if risk_ratio > 0.3:
        risk_level = "High"
        confidence = min(risk_ratio * 2, 0.95)
    elif risk_ratio > 0.15:
        risk_level = "Medium"
        confidence = risk_ratio * 1.5
    else:
        risk_level = "Low" 
        confidence = 1 - risk_ratio
    
    factors = []
    if risk_ratio > 0.2:
        factors.append("High volume of negative sentiment")
    if urgency_count > 5:
        factors.append("Multiple urgent community concerns")
    if len(high_risk_posts) > 10:
        factors.append("Significant civil unrest indicators")
    
    return {
        "risk_level": risk_level,
        "confidence": confidence,
        "factors": factors,
        "high_risk_count": len(high_risk_posts),
        "total_posts": len(data)
    }

def detect_community_needs(data):
    """Detect specific community needs from data"""
    if not data:
        return []
    
    # Analyze by topic and sentiment
    topic_sentiment = {}
    for post in data:
        topic = post.get('topic', 'General')
        sentiment = post.get('sentiment_score', 0)
        
        if topic not in topic_sentiment:
            topic_sentiment[topic] = []
        topic_sentiment[topic].append(sentiment)
    
    # Identify needs (topics with high negative sentiment)
    needs = []
    for topic, sentiments in topic_sentiment.items():
        avg_sentiment = np.mean(sentiments)
        if avg_sentiment < -0.2 and len(sentiments) > 5:
            severity = "High" if avg_sentiment < -0.4 else "Medium"
            needs.append({
                "topic": topic,
                "severity": severity,
                "avg_sentiment": avg_sentiment,
                "post_count": len(sentiments),
                "recommendation": f"Address {topic.lower()} concerns in community outreach"
            })
    
    return sorted(needs, key=lambda x: x['avg_sentiment'])[:5]  # Top 5 needs

# Main application
def main():
    # Data collection from multiple sources
    all_data = []
    
    if "Mock Civic Data" in data_sources:
        mock_data = generate_mock_social_data(selected_city, selected_focus, 100, "Civic Platform")
        all_data.extend(mock_data)
    
    if "Twitter API" in data_sources:
        twitter_data = fetch_twitter_data(selected_city, selected_focus, 50)
        all_data.extend(twitter_data)
    
    if "News API" in data_sources:
        news_data = fetch_news_data(selected_city, selected_focus, 30)
        all_data.extend(news_data)
    
    if "Open Government Data" in data_sources:
        gov_data = fetch_government_data(selected_city, 20)
        # Government data needs different processing
        st.sidebar.info(f"📊 Processed {len(gov_data)} government reports")
    
    # Convert to DataFrame
    df = pd.DataFrame(all_data)
    
    # Real-time dashboard header
    st.header("🌡️ Real-time Civic Intelligence Dashboard")
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_posts = len(df)
        st.metric("Total Posts Analyzed", f"{total_posts:,}", "Multi-source")
    
    with col2:
        data_sources_count = len(set(df['source'].unique())) if not df.empty else 0
        st.metric("Data Sources", data_sources_count, "Integrated")
    
    with col3:
        if not df.empty:
            avg_sentiment = df['sentiment_score'].mean()
            st.metric("Avg Community Sentiment", f"{avg_sentiment:.2f}", 
                     "Positive" if avg_sentiment > 0 else "Needs Attention")
        else:
            st.metric("Avg Community Sentiment", "N/A", "No data")
    
    with col4:
        last_update = datetime.now().strftime("%H:%M:%S")
        st.metric("Last Update", last_update, "Real-time")
    
    # Civil Unrest Prediction
    if enable_forecasting and not df.empty:
        st.header("🚨 Civil Unrest Risk Assessment")
        
        unrest_prediction = predict_civil_unrest_risk(all_data)
        
        risk_col1, risk_col2, risk_col3 = st.columns(3)
        
        with risk_col1:
            risk_level = unrest_prediction["risk_level"]
            delta_color = "normal" if risk_level == "Low" else "inverse"
            st.metric(
                "Unrest Risk Level", 
                risk_level,
                f"{unrest_prediction['confidence']:.0%} confidence",
                delta_color=delta_color
            )
        
        with risk_col2:
            st.metric("High-Risk Indicators", unrest_prediction["high_risk_count"], "Posts")
        
        with risk_col3:
            st.metric("Total Monitoring", unrest_prediction["total_posts"], "Active")
        
        # Display risk factors
        if unrest_prediction["factors"]:
            st.warning("**Risk Factors Identified:**")
            for factor in unrest_prediction["factors"]:
                st.write(f"• {factor}")
        else:
            st.success("No significant risk factors detected.")
    
    # Community Needs Detection
    if enable_needs_detection and not df.empty:
        st.header("🏘️ Community Needs Assessment")
        
        community_needs = detect_community_needs(all_data)
        
        if community_needs:
            for need in community_needs:
                severity_color = {"High": "red", "Medium": "orange"}[need["severity"]]
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{need['topic']}** - {need['recommendation']}")
                with col2:
                    st.metric("Severity", need["severity"], f"{need['avg_sentiment']:.2f} sentiment")
        else:
            st.success("No critical community needs detected at this time.")
    
    # Data source breakdown
    st.header("📊 Data Source Analysis")
    
    if not df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Posts by Source")
            source_counts = df['source'].value_counts()
            fig, ax = plt.subplots(figsize=(8, 6))
            source_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax)
            ax.set_ylabel('')
            st.pyplot(fig)
        
        with col2:
            st.subheader("Sentiment by Topic")
            topic_sentiment = df.groupby('topic')['sentiment_score'].mean().sort_values()
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = ['red' if x < 0 else 'green' for x in topic_sentiment.values]
            topic_sentiment.plot(kind='barh', color=colors, ax=ax)
            ax.axvline(x=0, color='black', linestyle='--', alpha=0.3)
            ax.set_xlabel('Average Sentiment Score')
            st.pyplot(fig)
    
    # Real-time data table
    with st.expander("🔍 View Raw Multi-Source Data"):
        if not df.empty:
            st.dataframe(df[['source', 'topic', 'text', 'primary_emotion', 'sentiment_score', 'timestamp']])
        else:
            st.info("No data available from selected sources")
    
    # Auto-refresh simulation
    if auto_refresh:
        st.sidebar.info("🔄 Auto-refresh enabled")
        time.sleep(2)  # Simulate processing time
        st.rerun()

if __name__ == "__main__":
    main()
