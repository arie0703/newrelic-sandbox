import sys
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
NEWRELIC_KEY = os.getenv("NEWRELIC_KEY")
NEWRELIC_ENDPOINT = os.getenv("NEWRELIC_ENDPOINT")

def post_calories_data(intake, consumption, sleep_time, count_coffee, weight):
    headers = {"X-Insert-Key": NEWRELIC_KEY}
    d = {}
    d["eventType"] = "test"
    d["intake"] = int(intake)
    d["consumption"] = int(consumption)
    d["sleep_time"] = float(sleep_time)
    d["count_coffee"] = int(count_coffee)
    d["weight"] = float(weight)
    res = requests.post(NEWRELIC_ENDPOINT, headers=headers, json=d)
    print(200)
    return res

print("摂取カロリー / 消費カロリー / 睡眠時間 / コーヒー摂取数 / 体重　を入力してね！")
data = input().split()
if len(data) != 5:
    raise Exception

post_calories_data(data[0], data[1], data[2], data[3], data[4])