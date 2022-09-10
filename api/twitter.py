import tweepy
import sys
import os
import json
import requests
from dotenv import load_dotenv
from transformers import pipeline 
from transformers import AutoModelForSequenceClassification 
from transformers import BertJapaneseTokenizer 
import datetime as dt

load_dotenv()
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
NEWRELIC_KEY = os.getenv("NEWRELIC_KEY")
NEWRELIC_ENDPOINT = os.getenv("NEWRELIC_ENDPOINT")

client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN,
                        consumer_key=TWITTER_API_KEY,
                        consumer_secret=TWITTER_API_SECRET,
                        access_token=TWITTER_ACCESS_TOKEN,
                        access_token_secret=TWITTER_ACCESS_SECRET
                    )

model = AutoModelForSequenceClassification.from_pretrained('daigo/bert-base-japanese-sentiment') 
tokenizer = BertJapaneseTokenizer.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking') 
nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)


def get_today_datetime(fmt, now):
    return dt.datetime.strftime(now, fmt)

def get_yesterday_datetime(fmt, now):
    return dt.datetime.strftime((now - dt.timedelta(days=1)), fmt)

def output_tweet_data():

    fmt = "%Y-%m-%dT00:00:00Z"
    JST = dt.timezone(dt.timedelta(hours=+9), 'JST')
    now = dt.datetime.now(JST)
    today = get_today_datetime(fmt, now)
    yesterday = get_yesterday_datetime(fmt, now)

    user = client.get_me()
    tweets = client.get_users_tweets(id = user.data.id,
                                    exclude=("replies"),
                                    start_time=yesterday,
                                    end_time=today
                                    )
    tweets_data = tweets.data

    result = []
    if tweets_data != None:
        for tweet in tweets_data:
            em = nlp(tweet.text)
            d = {}
            d["eventType"] = "test_twitter"
            d["score"] = em[0]["score"]
            d["label"] = em[0]["label"]
            d["tweet"] = tweet.text
            result.append(d)

    # jsonファイルを生成
    json_file = open("./twitter.json", mode="w")
    json.dump(result, json_file, indent=2, ensure_ascii=False)
    json_file.close()

    # Newrelicにpost
    headers = {"X-Insert-Key": NEWRELIC_KEY}
    res = requests.post(NEWRELIC_ENDPOINT, headers=headers, json=result)
    print(res)

output_tweet_data()




