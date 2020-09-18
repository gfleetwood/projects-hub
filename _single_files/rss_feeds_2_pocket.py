import feedparser
import requests
import time
from functools import reduce
from time import mktime
import pandas as pd
import os

pocket_key = os.environ['POCKETKEY']
pocket_token = os.environ['POCKETTOKEN']

def add_to_pocket(link):

    params = {"url": link, "consumer_key": pocket_key, "access_token": pocket_token}
    requests.post("https://getpocket.com/v3/add", data = params)

def process_feed(feed_date):

    fd = feed_date["feed"]
    dt = feed_date["last_updated"]
    feed_entries = feedparser.parse(fd).entries

    if dt == 0:
        add_to_pocket(feed_entries[0].link)
    else:
        for entry in feed_entries:
            if mktime(entry.published_parsed) >= dt:
                add_to_pocket(entry.link)

    result = {fd: time.time()}

    return(result)


if __name__=='__main__':

    feeds = pd.read_csv("feeds.csv").to_dict('records')

    feeds_updated = list(map(process_feed, feeds))
    feeds_updated_dict = reduce(lambda a, b: dict(a, **b), feeds_updated)
    feeds_new = pd.DataFrame({'feed': list(feeds_updated_dict.keys()), 'last_updated': list(feeds_updated_dict.values())})
    feeds_new.to_csv("feeds.csv", index = False)

    print("Done")
