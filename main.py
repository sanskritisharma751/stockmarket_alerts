import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


## STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and
# the day before yesterday then print("Get News").
#HINT 1: Get the closing price for yesterday and
# the day before yesterday. Find the positive difference between the two prices.
# e.g. 40 - 20 = -20, but the positive difference is 20.
#HINT 2: Work out the value of 5% of yerstday's closing stock price.
parameters1={
    'function':'TIME_SERIES_DAILY',
    'symbol':STOCK,
    'apikey':'N1X18X9PG0Z9T9SF',
}

stock_response = requests.get(STOCK_ENDPOINT,params=parameters1)
stock_response.raise_for_status()
stock_price = stock_response.json()['Time Series (Daily)']
data1=[values for (key,values) in stock_price.items()]
print(data1)
day1_stock_price=data1[0]['4. close']
day2_stock_price=data1[1]['4. close']
stock_difference=float(day1_stock_price)-float(day2_stock_price)
print(stock_difference)
percent=(stock_difference/float(day1_stock_price))*100
print(percent)


parameters={
    'q':COMPANY_NAME,
    'language':'en',
    'pagesize':'100',
    'apiKey':'24009442b53943f68d1482f91cc0904b',
}
news=[]
response = requests.get(NEWS_ENDPOINT, params=parameters)
response.raise_for_status()
data=response.json()
for i in range(3):
  news.append(f"Headline: {data['articles'][i]['title']}\nBrief: {data['articles'][i]['description']}")
#  print(news)
## STEP 2: Use https://newsapi.org/docs/endpoints/everything
# Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME. 
#HINT 1: Think about using the Python Slice Operator
if percent >0:
    symbol='🔺'
else:
    symbol='🔻'


## STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number. 
#HINT 1: Consider using a List Comprehension.
if percent >5 or percent <5:
    with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        connection.starttls()
        connection.login("sanskritisharma751@gmail.com", "yymf xtuq rrkr emmq")
        msg = MIMEMultipart()
        msg['From'] = "sanskritisharma751@gmail.com"
        msg['To'] = "sanskritisharma751@gmail.com"
        msg['Subject'] = f"{COMPANY_NAME}'s stock price"
        body = f"{STOCK}:{symbol} {abs(percent)}%\n{news[0]}\n{news[1]}\n{news[2]}"
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        connection.sendmail(
            from_addr="<sanskritisharma751@gmail.com>",
            to_addrs="<sanskritisharma751@gmail.com>",
            msg=msg.as_string()
        )

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

