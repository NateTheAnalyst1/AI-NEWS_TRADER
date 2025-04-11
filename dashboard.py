import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from textblob import TextBlob
import openai

# Set OpenAI API key (make sure to replace with your key)
openai.api_key = 'your-openai-api-key'

# Set page config for dark mode and smooth layout
st.set_page_config(page_title="AI Stock Tracker", layout="wide")

# Custom CSS for Wall Street office look
st.markdown(
    """
    <style>
    body {
        background-color: #121212;
        color: white;
        font-family: 'Arial', sans-serif;
    }

    .stApp {
        background-color: #121212;
    }

    .css-1d391kg {
        color: #00FF00;  /* Green for positive sentiment */
    }

    .css-1d391kg:hover {
        background-color: #333333;
    }

    .stButton>button {
        background-color: #0073e6; /* Blue for buttons */
        color: white;
        font-weight: bold;
        border-radius: 5px;
    }

    .stButton>button:hover {
        background-color: #005bb5; /* Hover effect */
    }

    .stSlider>div>div {
        background-color: #333333;
    }

    .stRadio>div>div>label {
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Stock News", "Position Tracker"])

# Placeholder for holding scraped articles
if "scraped_articles" not in st.session_state:
    st.session_state.scraped_articles = []

# Function for scraping stock news and analyzing sentiment
def scrape_and_analyze_articles(num_articles):
    # Here, implement the scraping logic (using Selenium, etc.)
    # For demo purposes, here's a sample list
    sample_articles = [
        {"title": "Apple stock on the rise", "description": "Apple's stock has surged after great earnings report.", "url": "https://www.economist.com/apple-stock", "price": 150},
        {"title": "Tesla faces challenges", "description": "Tesla shares are struggling due to market concerns.", "url": "https://www.economist.com/tesla-stock", "price": 800}
    ]
    
    analyzed_articles = []
    for article in sample_articles[:num_articles]:
        # Perform sentiment analysis using TextBlob
        blob = TextBlob(article['description'])
        sentiment = blob.sentiment.polarity
        sentiment_label = "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
        
        # AI-powered recommendation (for demo purposes)
        recommendation = "Buy" if sentiment > 0 else "Sell"
        
        analyzed_articles.append({
            "title": article['title'],
            "description": article['description'],
            "sentiment": sentiment_label,
            "price": article['price'],
            "analysis": recommendation
        })
    
    return analyzed_articles

# Stock News Page (scraping and AI analysis)
def display_stock_news():
    st.title("📈 AI-Powered Stock News Scraper")
    
    num_articles = st.slider("How many articles to scrape?", 1, 10, 5)

    if st.button("Run Scraper"):
        with st.spinner("Scraping and analyzing..."):
            results = scrape_and_analyze_articles(num_articles)
            st.session_state.scraped_articles = results
        
        for i, article in enumerate(results):
            st.subheader(f"{i+1}. {article['title']}")
            st.write(f"📝 **Description:** {article['description']}")
            st.write(f"📊 **AI Recommendation:** {article['analysis']}")
            st.write(f"💬 **Sentiment:** {article['sentiment']}")

            if st.button(f"Track Position for {article['title']}"):
                st.session_state.positions.append({
                    "title": article['title'],
                    "sentiment": article['sentiment'],
                    "ai_recommendation": article['analysis']
                })
                st.success(f"Position for '{article['title']}' has been added!")

# Position Tracker Page (for managing portfolio)
def display_position_tracker():
    st.title("📊 Track Your Positions")

    # Create positions dataframe if it doesn't exist
    if "positions" not in st.session_state:
        st.session_state.positions = []

    # Display positions as a DataFrame
    if st.session_state.positions:
        positions_df = pd.DataFrame(st.session_state.positions)
        st.write(positions_df)
    else:
        st.write("No positions tracked yet.")

    # Add position management options
    if st.session_state.positions:
        position_to_remove = st.selectbox("Select a position to remove", positions_df["title"].tolist(), index=0)
        if st.button("Remove Position"):
            st.session_state.positions = [pos for pos in st.session_state.positions if pos["title"] != position_to_remove]
            st.success(f"Position for '{position_to_remove}' has been removed!")

    # Track new positions
    st.subheader("Track New Position")

    selected_title = st.selectbox("Select a stock to track", [article["title"] for article in st.session_state.get("scraped_articles", [])])
    position_action = st.selectbox("Action", ["Buy", "Sell", "Hold"])
    investment_size = st.number_input("Enter the amount to invest ($)", min_value=0.0, format="%.2f")

    if st.button("Add Position"):
        article = next(article for article in st.session_state.get("scraped_articles", []) if article["title"] == selected_title)
        
        # Add the new position to session state
        st.session_state.positions.append({
            "title": article['title'],
            "action": position_action,
            "investment_size": investment_size,
            "sentiment": article['sentiment'],
            "ai_recommendation": article['analysis']
        })
        st.success(f"Position for '{article['title']}' has been added!")

# Show the correct page based on navigation
if page == "Stock News":
    display_stock_news()
else:
    display_position_tracker()

# Display a scrolling ticker at the top
ticker_data = [
    "AAPL +1.5% | TSLA -2.1% | MSFT +0.8% | AMZN +3.0% | NVDA -1.2% |",
    "FB +0.5% | SPY +1.2% | NFLX +4.5% | GOOGLE +2.7% |",
]

# Create a moving ticker effect
def ticker():
    while True:
        for data in ticker_data:
            st.markdown(f"<h1 style='color: green; text-align:center'>{data}</h1>", unsafe_allow_html=True)
            time.sleep(2)

# Run the ticker function in a Streamlit component (this simulates the Wall Street style)
if st.sidebar.button("Show Live Ticker"):
    ticker()
