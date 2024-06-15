import requests
from twilio.rest import Client
import datetime
import os

current_date = datetime.datetime.now().date()
yesterday_date = current_date - datetime.timedelta(days=1)
previous_date = current_date - datetime.timedelta(days=2)

VIRTUAL_TWILIO_NUMBER = "your virtual twilio number"
VERIFIED_NUMBER = "your own phone number verified with Twilio"

STOCK_MARKET_API_KEY = os.environ.get("STOCK_MARKET_API")
NEWS_API_KEY = os.environ.get("NEWS_API")

ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
PLACEHOLDER_VALUE = 5

news_params = {
    "q": COMPANY_NAME,
    "language": "en",
    "sortBy": "relevancy",
    "from": previous_date,
    "to": yesterday_date,
    "apiKey": NEWS_API_KEY,
}
response_news = requests.get(url='https://newsapi.org/v2/everything', params=news_params)

# Headline and description from the news source
response_news.raise_for_status()
news_data = response_news.json()

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_MARKET_API_KEY
}
response_stock = requests.get(url="https://www.alphavantage.co/query", params=stock_params)
response_stock.raise_for_status()
stock_data = response_stock.json()
stock_price_yesterday = float(stock_data['Time Series (Daily)'][f'{previous_date}']['4. close'])
stock_price_daybefore = float(stock_data['Time Series (Daily)'][f'{yesterday_date}']['4. close'])
percentage_difference = round((((stock_price_yesterday - stock_price_daybefore) / stock_price_yesterday) * 100), 2)
print(percentage_difference)

for i in range(0, 3):
    top_news_title = news_data["articles"][i]['title']
    top_news_description = news_data["articles"][i]['description']
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    if percentage_difference >= +0.26:
        print(f"{STOCK}:📈{percentage_difference}% \nHeadline: {top_news_title} \nBrief: {top_news_description}")
        message = client.messages \
            .create(
            from_= VIRTUAL_TWILIO_NUMBER,
            body=f"{STOCK}:📈{percentage_difference}% \nHeadline: {top_news_title} \nBrief: {top_news_description}",
            to=VERIFIED_NUMBER
        )
        print(message.status)
    elif percentage_difference <= -0.26:
        print(f"{STOCK}:📉{percentage_difference}% \nHeadline: {top_news_title} \nBrief: {top_news_description}")
        message = client.messages \
            .create(
            from_='+17655176234',
            body=f"{STOCK}:📉{percentage_difference}% \nHeadline: {top_news_title} \nBrief: {top_news_description}",
            to='+27698244193',
        )
        print(message.status)










