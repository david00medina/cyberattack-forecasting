# ############################################################################################################
#  Copyright (c) 2022 David Alberto Medina Medina.                                                           #
#                                                                                                            #
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software             #
#  and associated documentation files (the "Software"), to deal in the Software without restriction,         #
#   including without limitation the rights to use, copy, modify, merge, publish, distribute,                #
#    sublicense, and/or sell copies of the Software, and to permit persons to whom the Software              #
#    is furnished to do so, subject to the following conditions:                                             #
#                                                                                                            #
#  The above copyright notice and this permission notice shall be included in all copies or substantial      #
#  portions of the Software.                                                                                 #
#                                                                                                            #
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,                       #
#   INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A                            #
#   PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR                                 #
#   COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN                        #
#   AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION                          #
#   WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                                          #
# ############################################################################################################
import json
import os
from datetime import datetime
from pprint import pprint

import snscrape.modules.twitter as sntwitter
import tweepy
from pymongo import MongoClient

from Model.MongoDB.MongoTweet import MongoTweet
from Twitter.Setting.Setting import Setting
from Twitter.Twitter import Twitter


def get_credentials(json_file):
    """
    Reads the json file and start the tweeter API.
    Requires a json file with 'api_key', 'api_secret',
    'access_token' and 'access_secret'

    Argument:
    ---------
    json_file (str)
        path to the json file

    Returns:
    The tweeter API
    """
    with open(json_file) as fp:
        log = json.load(fp)
        auth = tweepy.OAuthHandler(log['api_key'], log['api_secret'])
        auth.set_access_token(log['access_token'], log['access_secret'])

    my_api = tweepy.API(auth, wait_on_rate_limit=True)

    return my_api


def snscrape_search(my_api, search_item, since='2020-01-01', until='2020-12-15', count=100):
    """
        Searchs the item in tweets and returns a Pandas DataFrame.

        Arguments:
        ----------
        search_item (str)

        Example:
        search_term = "#climate+change -filter:retweets" to avoid retweets

        """
    mysearch = f'{search_item} -filter:retweets since:{since} until:{until}'
    my_scraper = sntwitter.TwitterSearchScraper(mysearch).get_items()

    tweets_id = list()
    for i, tweet in enumerate(my_scraper):
        if i > count:
            break
        tweets_id.append(tweet.id)

    twitter = Twitter()
    twitter.auth(Setting.OAUTH_v2)
    now = datetime.now().strftime('%Y-%m-%dT%H-%M-%S.%fZ')

    lookup_tweets = []
    i = 0
    while i*100 < len(tweets_id):
        lookup_result = twitter.lookup_tweets_by_id_v2(
            ids=tweets_id[i*100:(i+1)*100],
            save_json=False,
            json_path=f'samples/search-tweet/search-tweets-debug-{now}.json'
        )
        lookup_tweets.append(lookup_result)
        i += 1
    pprint(lookup_tweets)

    user = os.environ.get("MONGO_USER")
    password = os.environ.get("MONGO_PASSWORD")
    host = os.environ.get("MONGO_HOST")
    port = os.environ.get("MONGO_PORT")

    client = MongoClient(f"mongodb://{user}:{password}@{host}:{port}")
    db = client.threat
    tweets = db.tweets

    mongo_tweets = []
    for tweet_set in lookup_tweets:
        mongo_tweet = MongoTweet.map_tweet_to_mongo(tweet_set)
        if isinstance(mongo_tweet, list):
            mongo_tweets.extend(mongo_tweet)
        else:
            mongo_tweets.append(mongo_tweet)

    result = tweets.insert_many(mongo_tweets)
    print(result.inserted_ids)

    client.close()

    return lookup_tweets


if __name__ == '__main__':
    json_file = 'twitter_keys.json'
    my_api = get_credentials(json_file)
    tweets = snscrape_search(my_api=my_api, search_item="@TheAnonMovement -filter:retweets'", since='2016-01-01',
                             until='2016-12-15', count=200)
