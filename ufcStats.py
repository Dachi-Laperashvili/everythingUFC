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

# getting fighters table

fighters_link = "http://ufcstats.com/statistics/fighters"

fighters_data = requests.get(fighters_link)

fighters_soup = BeautifulSoup(fighters_data.text)

links = [l.get("href") for l in fighters_soup.find_all("a")]
links = [l for l in links if l and "/statistics/fighters?char" in l]

letter_urls = [f"http://ufcstats.com{l}&page=all" for l in links]

all_fighters = []

for letter_url in letter_urls:
    try:
        fighters_data = requests.get(letter_url)
        fighters = pd.read_html(fighters_data.text,match="First")[0]

        all_fighters.append(fighters)
        time.sleep(5)
    except requests.exceptions.RequestException as e:
        print(e)
        continue


fighters_df = pd.concat(all_fighters)

fighters_df.to_csv("fighters.csv")
