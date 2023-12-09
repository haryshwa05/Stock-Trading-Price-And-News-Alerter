import requests
from twilio.rest import Client

STOCK_NAME = "TSLA" #Enter company stock name
COMPANY_NAME = "Tesla Inc" #Enter company name

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "" #Enter stock price api key
NEWS_API_KEY = "" #Enter News api key
TWILIO_SID = "" #Enter Twilio SID
TWILIO_AUTH_TOKEN = "" #Enter TWILIO Authorization token

stock_params = {
    "function" : "TIME_SERIES_DAILY",
    "symbol" : STOCK_NAME,
    "apikey" : STOCK_API_KEY,
}



response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()['Time Series (Daily)']

data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])
print(f"Yesterday's stock closing price was: {round(yesterday_closing_price, 2)}$")


daybefore_yesterday_data = data_list[1]
daybefore_yesterday_closing_price = float(daybefore_yesterday_data["4. close"])
print(f"Day before yesterday's stock closing price was: {round(daybefore_yesterday_closing_price, 2)}$")


difference = (yesterday_closing_price) - (daybefore_yesterday_closing_price)
positive_difference = round(abs(difference), 1)
print(f"The positive difference is {positive_difference}")

up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down= "🔻"

difference_percentage = (difference / float(yesterday_closing_price)) * 100
print(f"The difference percentage is: {round(difference_percentage, 2)}%")


news_params = {
        "apikey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME


    }


news_response = requests.get(NEWS_ENDPOINT, params=news_params)
articles = news_response.json()["articles"]
three_articles = articles[:3]


formatted_articles = [f"{STOCK_NAME}: {up_down}{difference_percentage}%Headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]


for article in formatted_articles:
    print(article)



client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

for article in formatted_articles:
    message = client.message.create(
        body= article,
        from_="", #Enter your twilio phone number
        to="" #Enter your personal phone number to send the stock details to
    )


