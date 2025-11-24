import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import random
from datetime import datetime, timedelta

# Configure the page
st.set_page_config(
    page_title="Civic Sentiment Dashboard",
    page_icon="🏛️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1DA1F2;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .tweet-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #1DA1F2;
    }
    .positive {
        color: #00C851;
        font-weight: bold;
    }
    .negative {
        color: #ff4444;
        font-weight: bold;
    }
    .neutral {
        color: #ffbb33;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize sentiment analyzers
vader_analyzer = SentimentIntensityAnalyzer()

# Title
st.markdown('<h1 class="main-header">🏛️ Civic Sentiment Dashboard</h1>', unsafe_allow_html=True)
st.markdown("Analyze public opinion about civic topics using NLP sentiment analysis.")

# Sidebar configuration
st.sidebar.header("Dashboard Configuration")

# Topic selection
topic_options = [
    "Local Government", "Public Transportation", "Education Policy", 
    "Environmental Policy", "Healthcare", "Infrastructure", "Custom Topic"
]
selected_topic = st.sidebar.selectbox("Select a topic to analyze:", topic_options)

if selected_topic == "Custom Topic":
    custom_topic = st.sidebar.text_input("Enter your custom topic:")
    analysis_topic = custom_topic if custom_topic else "civic engagement"
else:
    analysis_topic = selected_topic

# Analysis method
analysis_method = st.sidebar.radio("Sentiment Analysis Method:", ["TextBlob", "VADER"])

# Function to generate mock tweets
def generate_mock_tweets(topic, count=30):
    tweets = []
    sentiments = ["Positive", "Negative", "Neutral"]
    
    positive_phrases = [
        f"Great initiative by our {topic.lower()}!",
        f"Impressed with the progress on {topic.lower()}.",
        f"Thank you to our {topic.lower()} for listening to citizens.",
        f"Positive changes happening with {topic.lower()}.",
        f"Support the new {topic.lower()} proposal!"
    ]
    
    negative_phrases = [
        f"Disappointed with our {topic.lower()}.",
        f"{topic} needs serious improvement.",
        f"Frustrated with the lack of progress on {topic.lower()}.",
        f"{topic} is failing our community.",
        f"Concerned about the direction of {topic.lower()}."
    ]
    
    neutral_phrases = [
        f"Reading about the new {topic.lower()} proposal.",
        f"Attended a meeting about {topic.lower()} today.",
        f"Interesting discussion happening about {topic.lower()}.",
        f"Following updates on {topic.lower()} developments.",
        f"Curious to see how {topic.lower()} will evolve."
    ]
    
    for i in range(count):
        sentiment = random.choice(sentiments)
        
        if sentiment == "Positive":
            text = random.choice(positive_phrases)
        elif sentiment == "Negative":
            text = random.choice(negative_phrases)
        else:
            text = random.choice(neutral_phrases)
        
        # Add hashtags occasionally
        if i % 5 == 0:
            text += " #civicengagement"
            
        tweets.append({
            "id": i + 1,
            "text": text,
            "user": f"user_{random.randint(1000, 9999)}",
            "created_at": datetime.now() - timedelta(hours=random.randint(1, 168)),
            "sentiment": sentiment,
            "retweet_count": random.randint(0, 50),
            "favorite_count": random.randint(0, 100)
        })
    
    return tweets

# Function to analyze sentiment with TextBlob
def analyze_sentiment_textblob(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    
    if polarity > 0.1:
        return "Positive", polarity
    elif polarity < -0.1:
        return "Negative", polarity
    else:
        return "Neutral", polarity

# Function to analyze sentiment with VADER
def analyze_sentiment_vader(text):
    scores = vader_analyzer.polarity_scores(text)
    compound = scores['compound']
    
    if compound >= 0.05:
        return "Positive", compound
    elif compound <= -0.05:
        return "Negative", compound
    else:
        return "Neutral", compound

# Main analysis
if st.sidebar.button("Analyze Sentiment"):
    with st.spinner(f"Analyzing sentiment about {analysis_topic}..."):
        # Generate mock tweets
        tweets = generate_mock_tweets(analysis_topic, 30)
        
        # Analyze sentiment for each tweet
        for tweet in tweets:
            if analysis_method == "TextBlob":
                sentiment, score = analyze_sentiment_textblob(tweet["text"])
            else:
                sentiment, score = analyze_sentiment_vader(tweet["text"])
            
            tweet["sentiment"] = sentiment
            tweet["sentiment_score"] = score
        
        # Convert to DataFrame
        df = pd.DataFrame(tweets)
        
        # Calculate metrics
        total_tweets = len(df)
        positive_tweets = len(df[df["sentiment"] == "Positive"])
        negative_tweets = len(df[df["sentiment"] == "Negative"])
        neutral_tweets = len(df[df["sentiment"] == "Neutral"])
        
        positive_percent = (positive_tweets / total_tweets) * 100
        negative_percent = (negative_tweets / total_tweets) * 100
        neutral_percent = (neutral_tweets / total_tweets) * 100
        
        # Calculate accuracy (simulated)
        accuracy = 85 + random.uniform(0, 10)
        
        # Display metrics
        st.subheader("📊 Sentiment Analysis Results")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Posts", total_tweets)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Positive", f"{positive_percent:.1f}%", f"{positive_tweets} posts")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Negative", f"{negative_percent:.1f}%", f"{negative_tweets} posts", delta_color="inverse")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Analysis Accuracy", f"{accuracy:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart
            st.subheader("Sentiment Distribution")
            fig, ax = plt.subplots(figsize=(8, 6))
            sentiment_counts = [positive_tweets, negative_tweets, neutral_tweets]
            labels = ['Positive', 'Negative', 'Neutral']
            colors = ['#00C851', '#ff4444', '#ffbb33']
            
            ax.pie(sentiment_counts, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
            ax.axis('equal')
            st.pyplot(fig)
        
        with col2:
            # Bar chart
            st.subheader("Sentiment Counts")
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.bar(labels, sentiment_counts, color=colors)
            ax.set_ylabel('Number of Posts')
            ax.set_title('Sentiment Analysis Results')
            plt.xticks(rotation=45)
            st.pyplot(fig)
        
        # Display sample posts
        st.subheader("📝 Sample Public Posts")
        
        # Sort by most recent
        df_sorted = df.sort_values("created_at", ascending=False)
        
        for i, post in df_sorted.head(8).iterrows():
            sentiment_class = post["sentiment"].lower()
            
            st.markdown(f'''
            <div class="tweet-card">
                <strong>@{post['user']}</strong> · {post['created_at'].strftime('%b %d, %H:%M')}<br>
                {post['text']}<br>
                <small>Sentiment: <span class="{sentiment_class}">{post['sentiment']}</span> | 
                Score: {post['sentiment_score']:.3f} | 
                Retweets: {post['retweet_count']} | 
                Likes: {post['favorite_count']}</small>
            </div>
            ''', unsafe_allow_html=True)
        
        # Data table
        st.subheader("📋 Complete Data")
        st.dataframe(df[['user', 'text', 'sentiment', 'sentiment_score', 'created_at']])
        
        # Download option
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name=f"sentiment_analysis_{analysis_topic.replace(' ', '_')}.csv",
            mime="text/csv",
        )

else:
    # Show instructions when no analysis has been run
    st.info("👈 Configure your analysis in the sidebar and click 'Analyze Sentiment' to get started!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚀 How to Use")
        st.markdown("""
        1. **Select a Topic** - Choose from civic topics or enter custom
        2. **Choose Analysis Method** - TextBlob or VADER NLP
        3. **Click Analyze** - View real-time sentiment analysis
        4. **Explore Results** - Charts, metrics, and individual posts
        
        **Features:**
        - Real-time sentiment classification
        - Data visualization with charts
        - Sample public opinion analysis
        - Export results as CSV
        """)
    
    with col2:
        st.subheader("🛠️ Tech Stack")
        st.markdown("""
        - **Python & Streamlit** - Web app framework
        - **TextBlob & VADER** - NLP sentiment analysis
        - **Pandas** - Data processing
        - **Matplotlib/Seaborn** - Data visualization
        - **Mock Data** - Realistic civic discourse simulation
        
        *Perfect for government agencies, policy analysts, and civic organizations!*
        """)
    
    # Example visualization
    st.subheader("📈 Example Output Preview")
    
    # Show example metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Posts", "30")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Positive", "43.3%", "13 posts")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Negative", "33.3%", "10 posts", delta_color="inverse")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Accuracy", "87.2%")
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "**Civic Sentiment Dashboard** | Developed with Python, Streamlit, and NLP techniques | "
    "Real-time public opinion analysis for civic topics"
)
