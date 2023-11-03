import requests
import json
from datetime import datetime, timedelta
from twilio.rest import Client

# Define constants
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_VANTAGE_APIKEY = "key"
NEWS_APIKEY = "key"
Triger_percentage = 1

# Create URLs using f-strings
stock_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&apikey={ALPHA_VANTAGE_APIKEY}"
news_url = f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&apiKey={NEWS_APIKEY}"

# Make an API request to Alpha Vantage and retrieve stock data
response = requests.get(stock_url)
data = json.loads(response.text)

# Extract the relevant data
stock_data = data.get("Time Series (Daily)", {})

# Calculate dates for yesterday and the day before yesterday
yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
day_before_yesterday = (datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d")

# Get closing prices for yesterday and the day before yesterday
close_price_yesterday = float(stock_data.get(yesterday, {}).get("4. close", 0.0))
close_price_day_befor_yesterday = float(stock_data.get(day_before_yesterday, {}).get("4. close", 0.0))

# Calculate the percentage difference
percentage_dif = round(((close_price_yesterday - close_price_day_befor_yesterday) / close_price_day_befor_yesterday) * 100, 2)

# Check if the percentage difference is significant
if percentage_dif >= Triger_percentage or percentage_dif <= -1 * Triger_percentage:
    imoji = "🔺" if percentage_dif > Triger_percentage else "🔻"
    percentage_dif = abs(percentage_dif) # Ensure percentage is positive

    # Make an API request to News API and retrieve news data
    response = requests.get(news_url)
    news_data = json.loads(response.text)
    articles = news_data.get("articles", [])[:3]  # Get the first 3 articles

    # Extract titles from the news articles
    titles = [article.get("title", "No Title Available") for article in articles]

    # Create the message body
    body = f"{COMPANY_NAME}: {imoji} {percentage_dif}%\n" + "\n".join(titles)

    # Send the message using Twilio
    #client = Client(account_sid, auth_token)
    #message = client.messages.create(
    #    body=body,
    #    from_="number",
    #    to="number"
    #)
#
    #print(message.status)
    print(close_price_yesterday)
    print(close_price_day_befor_yesterday)
    print(body)
