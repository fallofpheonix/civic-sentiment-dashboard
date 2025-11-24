import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import folium_static
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import random
from datetime import datetime, timedelta
import numpy as np

# Configure the page for full-width emotional weather map
st.set_page_config(
    page_title="Emotional Weather Map",
    page_icon="🌤️",
    layout="wide"
)

# Custom CSS for weather-themed styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E90FF;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #1E90FF, #00BFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .weather-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem;
        color: white;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    .emotion-sunny { background: linear-gradient(135deg, #FFD700, #FFA500); }
    .emotion-cloudy { background: linear-gradient(135deg, #B0C4DE, #778899); }
    .emotion-rainy { background: linear-gradient(135deg, #4682B4, #5F9EA0); }
    .emotion-stormy { background: linear-gradient(135deg, #8B0000, #B22222); }
    .emotion-calm { background: linear-gradient(135deg, #98FB98, #32CD32); }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    .region-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 5px solid #1E90FF;
    }
</style>
""", unsafe_allow_html=True)

# Initialize VADER sentiment analyzer
vader_analyzer = SentimentIntensityAnalyzer()

# Title with weather theme
st.markdown('<h1 class="main-header">🌤️ Emotional Weather Map</h1>', unsafe_allow_html=True)
st.markdown("### Real-time Civic Sentiment & Emotion Forecasting")

# Sidebar configuration
st.sidebar.header("🌍 Map Configuration")

# City selection
cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", 
          "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville"]
selected_city = st.sidebar.selectbox("Select City:", cities)

# Analysis focus
focus_areas = ["Education", "Healthcare", "Transportation", "Environment", "Housing", "Public Safety"]
selected_focus = st.sidebar.multiselect("Focus Areas:", focus_areas, default=["Education", "Healthcare"])

# Time range
time_range = st.sidebar.selectbox("Time Range:", ["Last 24 hours", "Last 7 days", "Last 30 days"])

# Advanced settings
st.sidebar.header("⚙️ Advanced Settings")
show_heatmap = st.sidebar.checkbox("Show Emotion Heatmap", True)
show_forecast = st.sidebar.checkbox("Show 7-day Emotion Forecast", True)
alert_threshold = st.sidebar.slider("Alert Threshold (% Negative):", 30, 80, 50)

# Generate mock geographic data for the selected city
def generate_city_regions(city, count=8):
    """Generate realistic neighborhood/region data for a city"""
    base_coords = {
        "New York": (40.7128, -74.0060),
        "Los Angeles": (34.0522, -118.2437),
        "Chicago": (41.8781, -87.6298),
        "Houston": (29.7604, -95.3698),
        "Phoenix": (33.4484, -112.0740),
        "Philadelphia": (39.9526, -75.1652),
        "San Antonio": (29.4241, -98.4936),
        "San Diego": (32.7157, -117.1611),
        "Dallas": (32.7767, -96.7970),
        "San Jose": (37.3382, -121.8863),
        "Austin": (30.2672, -97.7431),
        "Jacksonville": (30.3322, -81.6557)
    }
    
    base_lat, base_lng = base_coords.get(city, (40.7128, -74.0060))
    
    regions = []
    neighborhood_names = [
        "Downtown", "Uptown", "East Side", "West End", "North Hills", 
        "South Park", "Central District", "Riverfront", "Metro Center",
        "University District", "Historic Quarter", "Business Park"
    ]
    
    for i in range(count):
        # Create geographic variation around the city center
        lat_variation = random.uniform(-0.2, 0.2)
        lng_variation = random.uniform(-0.2, 0.2)
        
        regions.append({
            "region_id": i + 1,
            "name": f"{neighborhood_names[i % len(neighborhood_names)]}",
            "latitude": base_lat + lat_variation,
            "longitude": base_lng + lng_variation,
            "population": random.randint(5000, 50000),
            "income_level": random.choice(["Low", "Medium", "High"]),
            "post_count": random.randint(50, 500)
        })
    
    return regions

# Enhanced emotion detection beyond basic sentiment
def analyze_advanced_emotions(text):
    """Analyze text for specific emotions beyond positive/negative"""
    scores = vader_analyzer.polarity_scores(text)
    compound = scores['compound']
    
    # Enhanced emotion classification
    if compound >= 0.5:
        primary_emotion = "Joy"
        emotion_icon = "😊"
        weather_analogy = "Sunny"
    elif compound >= 0.1:
        primary_emotion = "Content"
        emotion_icon = "🙂"
        weather_analogy = "Partly Cloudy"
    elif compound >= -0.1:
        primary_emotion = "Neutral"
        emotion_icon = "😐"
        weather_analogy = "Cloudy"
    elif compound >= -0.5:
        primary_emotion = "Concerned"
        emotion_icon = "😟"
        weather_analogy = "Rainy"
    else:
        primary_emotion = "Angry"
        emotion_icon = "😠"
        weather_analogy = "Stormy"
    
    # Secondary emotions based on text content
    text_lower = text.lower()
    secondary_emotions = []
    
    if any(word in text_lower for word in ['happy', 'great', 'excellent', 'love', 'amazing']):
        secondary_emotions.append("Excited")
    if any(word in text_lower for word in ['worried', 'concerned', 'anxious', 'nervous']):
        secondary_emotions.append("Anxious")
    if any(word in text_lower for word in ['angry', 'frustrated', 'mad', 'outrage']):
        secondary_emotions.append("Frustrated")
    if any(word in text_lower for word in ['sad', 'disappointed', 'unhappy', 'terrible']):
        secondary_emotions.append("Disappointed")
    if any(word in text_lower for word in ['hope', 'optimistic', 'looking forward', 'better']):
        secondary_emotions.append("Hopeful")
    
    return {
        "primary_emotion": primary_emotion,
        "emotion_icon": emotion_icon,
        "weather_analogy": weather_analogy,
        "sentiment_score": compound,
        "secondary_emotions": secondary_emotions[:2],  # Limit to top 2
        "intensity": abs(compound)  # Emotion intensity
    }

# Generate mock civic discourse data with geographic and emotional context
def generate_emotional_data(city, regions, focus_areas, post_count=100):
    """Generate realistic civic discourse with emotional and geographic context"""
    
    civic_topics = {
        "Education": [
            "School funding needs serious improvement in our district",
            "Teachers are doing amazing work despite challenges",
            "Concerned about classroom sizes and resources",
            "Proud of our students' achievements this year",
            "Need better after-school programs for our kids"
        ],
        "Healthcare": [
            "Hospital wait times are becoming unacceptable",
            "Grateful for our healthcare workers' dedication",
            "Mental health services need more funding",
            "New clinic opening brings hope to our community",
            "Frustrated with insurance coverage limitations"
        ],
        "Transportation": [
            "Public transit delays are affecting daily commute",
            "Excited about new bike lane installations",
            "Road repairs needed urgently in our neighborhood",
            "Traffic congestion getting worse every day",
            "Appreciate the improved bus schedules"
        ],
        "Environment": [
            "Air quality concerns in industrial areas",
            "Community garden project bringing people together",
            "Need more recycling facilities in our area",
            "Park maintenance has improved significantly",
            "Worried about pollution levels in local rivers"
        ],
        "Housing": [
            "Rent prices becoming unaffordable for families",
            "New affordable housing project gives hope",
            "Homelessness crisis needs immediate attention",
            "Neighborhood revitalization showing positive results",
            "Frustrated with lack of rental protections"
        ],
        "Public Safety": [
            "Police response times need improvement",
            "Community watch program making streets safer",
            "Concerned about recent crime spike",
            "Fire department doing excellent work in our area",
            "Need better street lighting in residential areas"
        ]
    }
    
    posts = []
    
    for i in range(post_count):
        # Select random focus area and region
        focus = random.choice(focus_areas)
        region = random.choice(regions)
        
        # Get appropriate text samples
        text_options = civic_topics.get(focus, ["Community discussion about local issues"])
        text = random.choice(text_options)
        
        # Add geographic/local context
        text = f"{text} in {region['name']}"
        
        # Advanced emotion analysis
        emotion_data = analyze_advanced_emotions(text)
        
        posts.append({
            "post_id": i + 1,
            "text": text,
            "focus_area": focus,
            "region": region['name'],
            "latitude": region['latitude'],
            "longitude": region['longitude'],
            "user": f"resident_{random.randint(1000, 9999)}",
            "created_at": datetime.now() - timedelta(hours=random.randint(1, 168)),
            "sentiment_score": emotion_data["sentiment_score"],
            "primary_emotion": emotion_data["primary_emotion"],
            "emotion_icon": emotion_data["emotion_icon"],
            "weather_analogy": emotion_data["weather_analogy"],
            "secondary_emotions": emotion_data["secondary_emotions"],
            "emotion_intensity": emotion_data["intensity"],
            "engagement": random.randint(5, 200)
        })
    
    return posts

# Create emotional weather map using Folium
def create_emotional_weather_map(city, posts, regions):
    """Create an interactive map showing emotional weather across regions"""
    
    base_coords = {
        "New York": (40.7128, -74.0060),
        "Los Angeles": (34.0522, -118.2437),
        "Chicago": (41.8781, -87.6298),
        "Houston": (29.7604, -95.3698),
        "Phoenix": (33.4484, -112.0740)
    }
    
    center_lat, center_lng = base_coords.get(city, (39.8283, -98.5795))
    
    # Create base map
    m = folium.Map(location=[center_lat, center_lng], zoom_start=10)
    
    # Weather analogy colors
    weather_colors = {
        "Sunny": "orange",
        "Partly Cloudy": "lightblue", 
        "Cloudy": "gray",
        "Rainy": "blue",
        "Stormy": "red"
    }
    
    # Emotion icons
    emotion_icons = {
        "Joy": "😊",
        "Content": "🙂", 
        "Neutral": "😐",
        "Concerned": "😟",
        "Angry": "😠"
    }
    
    # Add region markers with emotional data
    for region in regions:
        region_posts = [p for p in posts if p['region'] == region['name']]
        
        if region_posts:
            # Calculate regional emotion metrics
            avg_sentiment = np.mean([p['sentiment_score'] for p in region_posts])
            dominant_emotion = max(set([p['primary_emotion'] for p in region_posts]), 
                                 key=[p['primary_emotion'] for p in region_posts].count)
            post_count = len(region_posts)
            
            # Determine marker color based on average sentiment
            if avg_sentiment > 0.1:
                color = 'green'
            elif avg_sentiment > -0.1:
                color = 'orange'
            else:
                color = 'red'
            
            # Create popup content
            popup_text = f"""
            <b>{region['name']}</b><br>
            Emotion: {emotion_icons.get(dominant_emotion, '😐')} {dominant_emotion}<br>
            Avg Sentiment: {avg_sentiment:.2f}<br>
            Posts: {post_count}<br>
            Population: {region['population']:,}
            """
            
            folium.CircleMarker(
                location=[region['latitude'], region['longitude']],
                radius=15 + (post_count / 20),  # Size based on post volume
                popup=folium.Popup(popup_text, max_width=300),
                color=color,
                fillColor=color,
                fillOpacity=0.6,
                weight=2
            ).add_to(m)
    
    return m

# Generate emotion forecast
def generate_emotion_forecast(current_data, days=7):
    """Generate a 7-day emotion forecast based on current trends"""
    forecast = []
    
    current_emotions = [post['primary_emotion'] for post in current_data]
    emotion_counts = {emotion: current_emotions.count(emotion) for emotion in set(current_emotions)}
    total_posts = len(current_emotions)
    
    base_date = datetime.now()
    
    for day in range(days):
        forecast_date = base_date + timedelta(days=day+1)
        
        # Simulate emotion trends with some randomness
        day_emotions = {}
        for emotion, count in emotion_counts.items():
            # Add some variation to simulate trends
            variation = random.uniform(0.8, 1.2)
            day_emotions[emotion] = int(count * variation)
        
        forecast.append({
            "date": forecast_date,
            "emotions": day_emotions,
            "dominant_emotion": max(day_emotions, key=day_emotions.get),
            "outlook": random.choice(["Improving", "Stable", "Concerning", "Positive"])
        })
    
    return forecast

# Main application
def main():
    # Generate data based on user selection
    regions = generate_city_regions(selected_city)
    posts = generate_emotional_data(selected_city, regions, selected_focus, 150)
    
    # Convert to DataFrame for analysis
    df = pd.DataFrame(posts)
    
    # Overall metrics
    st.header("🌡️ City Emotional Climate")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_sentiment = df['sentiment_score'].mean()
        emotion_color = "emotion-sunny" if avg_sentiment > 0.1 else "emotion-cloudy" if avg_sentiment > -0.1 else "emotion-rainy"
        st.markdown(f'<div class="weather-card {emotion_color}">', unsafe_allow_html=True)
        st.markdown('<div class="metric-value">' + f"{avg_sentiment:.2f}" + '</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Avg Sentiment Score</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        dominant_emotion = df['primary_emotion'].mode()[0] if not df.empty else "Neutral"
        st.markdown(f'<div class="weather-card emotion-calm">', unsafe_allow_html=True)
        st.markdown('<div class="metric-value">' + f"{dominant_emotion}" + '</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Dominant Emotion</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        total_posts = len(df)
        st.markdown(f'<div class="weather-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-value">' + f"{total_posts}" + '</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Civic Posts Analyzed</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        negative_pct = len(df[df['sentiment_score'] < -0.1]) / len(df) * 100 if len(df) > 0 else 0
        alert_color = "emotion-stormy" if negative_pct > alert_threshold else ""
        st.markdown(f'<div class="weather-card {alert_color}">', unsafe_allow_html=True)
        st.markdown('<div class="metric-value">' + f"{negative_pct:.1f}%" + '</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Concern Level</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Emotional Weather Map
    st.header("🗺️ Emotional Weather Map")
    
    if show_heatmap:
        emotional_map = create_emotional_weather_map(selected_city, posts, regions)
        folium_static(emotional_map, width=1000, height=500)
    
    # Emotion Analysis by Region
    st.header("🏘️ Regional Emotion Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Emotion Distribution by Region")
        
        # Create emotion distribution chart
        region_emotion = df.groupby(['region', 'primary_emotion']).size().unstack(fill_value=0)
        if not region_emotion.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            region_emotion.plot(kind='bar', stacked=True, ax=ax, 
                              color=['#FFD700', '#98FB98', '#B0C4DE', '#4682B4', '#8B0000'])
            ax.set_title('Emotion Distribution Across Regions')
            ax.set_xlabel('Region')
            ax.set_ylabel('Number of Posts')
            plt.xticks(rotation=45)
            st.pyplot(fig)
    
    with col2:
        st.subheader("Focus Area Sentiment")
        
        # Sentiment by focus area
        focus_sentiment = df.groupby('focus_area')['sentiment_score'].mean().sort_values()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['red' if x < 0 else 'green' for x in focus_sentiment.values]
        focus_sentiment.plot(kind='barh', color=colors, ax=ax)
        ax.set_title('Average Sentiment by Focus Area')
        ax.set_xlabel('Sentiment Score')
        ax.axvline(x=0, color='black', linestyle='--', alpha=0.3)
        st.pyplot(fig)
    
    # Emotion Forecast
    if show_forecast:
        st.header("📈 7-Day Emotion Forecast")
        
        forecast = generate_emotion_forecast(posts)
        
        forecast_cols = st.columns(7)
        for i, day_forecast in enumerate(forecast):
            with forecast_cols[i]:
                date_str = day_forecast['date'].strftime('%b %d')
                dominant = day_forecast['dominant_emotion']
                outlook = day_forecast['outlook']
                
                # Weather icons based on outlook
                outlook_icons = {
                    "Improving": "🌤️",
                    "Stable": "⛅", 
                    "Concerning": "🌧️",
                    "Positive": "☀️"
                }
                
                st.metric(
                    label=f"{date_str} {outlook_icons.get(outlook, '🌤️')}",
                    value=dominant,
                    delta=outlook
                )
    
    # Civic Alerts
    st.header("🚨 Civic Attention Needed")
    
    # Identify areas with high negative sentiment
    negative_hotspots = []
    for region in regions:
        region_posts = [p for p in posts if p['region'] == region['name']]
        if region_posts:
            negative_count = len([p for p in region_posts if p['sentiment_score'] < -0.1])
            negative_pct = (negative_count / len(region_posts)) * 100
            
            if negative_pct > alert_threshold:
                negative_hotspots.append({
                    'region': region['name'],
                    'negative_pct': negative_pct,
                    'total_posts': len(region_posts),
                    'dominant_issue': max(set([p['focus_area'] for p in region_posts]), 
                                        key=[p['focus_area'] for p in region_posts].count)
                })
    
    if negative_hotspots:
        for hotspot in sorted(negative_hotspots, key=lambda x: x['negative_pct'], reverse=True):
            st.warning(
                f"**{hotspot['region']}**: {hotspot['negative_pct']:.1f}% negative sentiment "
                f"({hotspot['total_posts']} posts). Primary concern: {hotspot['dominant_issue']}"
            )
    else:
        st.success("No critical alerts at this time. Civic sentiment is generally stable.")
    
    # Raw data exploration
    with st.expander("🔍 Explore Raw Civic Data"):
        st.dataframe(df[['region', 'focus_area', 'text', 'primary_emotion', 'sentiment_score', 'created_at']])

if __name__ == "__main__":
    main()
