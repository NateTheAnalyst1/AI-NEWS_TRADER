import requests
from bs4 import BeautifulSoup
import openai
from textblob import TextBlob

# Set your OpenAI API key
openai.api_key = 'your-openai-api-key'

# Function to scrape articles from the economist website (for example)
def scrape_economist_stock_news():
    # URL for the stock-related articles (adjust accordingly)
    url = "https://www.economist.com/finance-and-economics"
    
    # Send HTTP request and get the page content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find articles (this is an example, modify based on actual page structure)
    articles = []
    for article in soup.find_all('article', class_='teaser'):
        title = article.find('h3').text.strip()
        description = article.find('p').text.strip()
        link = article.find('a')['href']
        
        # For the purpose of this example, we'll just make up a dummy price
        price = 100  # Modify this based on the content
        
        articles.append({
            "title": title,
            "description": description,
            "url": link,
            "price": price
        })
    
    return articles

# Function for sentiment analysis using TextBlob
def analyze_sentiment(description):
    blob = TextBlob(description)
    sentiment = blob.sentiment.polarity
    sentiment_label = "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
    return sentiment_label, sentiment

# Function to get AI-driven recommendation from OpenAI
def get_ai_recommendation(description):
    # Use the OpenAI API to analyze the description
    prompt = f"Based on the following stock description, should I buy or sell? \n\n{description}"
    
    response = openai.Completion.create(
        engine="text-davinci-003",  # Choose the right engine for your use case
        prompt=prompt,
        max_tokens=50,
        temperature=0.7
    )
    
    # Get recommendation (e.g., 'Buy', 'Sell', 'Hold')
    recommendation = response.choices[0].text.strip()
    return recommendation

# Main function to scrape, analyze sentiment, and get recommendations
def process_articles():
    # Scrape stock news articles
    articles = scrape_economist_stock_news()
    
    analyzed_articles = []
    
    for article in articles:
        title = article['title']
        description = article['description']
        price = article['price']
        
        # Analyze sentiment using TextBlob
        sentiment_label, sentiment = analyze_sentiment(description)
        
        # Get AI recommendation
        recommendation = get_ai_recommendation(description)
        
        analyzed_articles.append({
            "title": title,
            "description": description,
            "price": price,
            "sentiment": sentiment_label,
            "ai_recommendation": recommendation
        })
    
    return analyzed_articles

# Call the process_articles function to scrape and analyze
if __name__ == "__main__":
    articles = process_articles()
    
    # Print the analyzed articles (for testing purposes)
    for i, article in enumerate(articles):
        print(f"{i+1}. {article['title']}")
        print(f"  Description: {article['description']}")
        print(f"  Price: {article['price']}")
        print(f"  Sentiment: {article['sentiment']}")
        print(f"  AI Recommendation: {article['ai_recommendation']}")
        print("\n")
