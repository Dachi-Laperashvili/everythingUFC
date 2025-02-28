import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# getting events table and making it into dataframe
url = "http://ufcstats.com/statistics/events/completed?page=all"

data = requests.get(url)

soup = BeautifulSoup(data.text)

events = pd.read_html(data.text,match="Name/date")[0]

events.to_csv("events.csv")
