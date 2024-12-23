from flask import Flask, render_template, request, jsonify
import requests
from textblob import TextBlob
import sqlite3

app = Flask(__name__)

# Replace with your NewsAPI Key
NEWS_API_KEY = 'YOUR_NEWSAPI_KEY'


# Function to fetch news articles from NewsAPI
def fetch_news(query):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    news_data = response.json()
    return news_data['articles']  # Returning list of articles


# Function to analyze sentiment of a news article
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity  # Returns a value between -1 (negative) and 1 (positive)
    return sentiment


# Function to check for potential risk factors
def extract_risk_factors(text):
    risk_keywords = ['lawsuit', 'debt', 'uncertainty', 'crisis', 'fraud', 'regulatory']
    risks = [keyword for keyword in risk_keywords if keyword in text.lower()]
    return risks


# Route to display the homepage with search form
@app.route('/')
def home():
    return render_template('index.html')


# Route to handle search query and fetch data
@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    articles = fetch_news(query)
    
    analyzed_articles = []
    for article in articles:
        title = article['title']
        description = article['description']
        sentiment = analyze_sentiment(description)
        risks = extract_risk_factors(description)
        
        analyzed_articles.append({
            'title': title,
            'description': description,
            'sentiment': sentiment,
            'risks': risks
        })
    
    return render_template('index.html', query=query, articles=analyzed_articles)


# Running the app
if __name__ == '__main__':
    app.run(debug=True)
