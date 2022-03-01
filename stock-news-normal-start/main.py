import requests
from datetime import datetime
from twilio.rest import Client


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

alpha_api_key = "MP2CCDUX75N2MWJM"
news_api_key = "2af42c45fbbb4198b2c5a8e1dbb1853b"
TWILIO_SID = ""
TWILIO_AUTH_TOKEN = ""

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
alpha_api_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "interval": "5min",
    "apikey": alpha_api_key
}


stock_response = requests.get(STOCK_ENDPOINT, params=alpha_api_parameters)
stock_response.raise_for_status()
stock = stock_response.json()["Time Series (Daily)"]
print(stock)


#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
#yesterday_stock = [new_value for (key, value) in dictionary.items()]
stock_value =[value for (key, value) in stock.items()]
yesterday_stock = stock_value[0]['4. close']
print(yesterday_stock)


#TODO 2. - Get the day before yesterday's closing stock price
day_before = stock_value[1]['4. close']
print(day_before)


#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp

difference = float(yesterday_stock) - float(day_before)
print(difference)
up_down = None
if difference > 0:
    up_down = "✅"
elif difference < 0:
    up_down = "🔺"

#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percentage_change = round(difference / float(day_before)) * 100

print(percentage_change)


#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
if abs(percentage_change) > 5:
    print("Get News")
    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
news_api_parameters = {
    "q": STOCK_NAME,
    "from": "2022-01-07",
    "sortBy": "publishedAt",
    "apiKey": news_api_key
}

news_response = requests.get(NEWS_ENDPOINT, params=news_api_parameters)
news_response.raise_for_status()
news_data = news_response.json()['articles']
print(news_data)
#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.


#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
three_articles = news_data[:3]

print(three_articles)

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
formatted_articles = [f"{STOCK_NAME} : {up_down}{percentage_change}% \nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
print(formatted_articles)


#TODO 9. - Send each article as a separate message via Twilio. 
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)


#Optional TODO: Format the message like this:
# for article in formatted_articles:
#     message = client.messages \
#         .create(
#             body=article,
#             from= 'Twilio number',
#             to= 'Coreys number'
# )

"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

