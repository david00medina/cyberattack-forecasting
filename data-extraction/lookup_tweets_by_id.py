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
import os
from datetime import datetime
from pprint import pprint

import yaml
from pymongo import MongoClient

from Model.MongoDB.MongoTweet import MongoTweet
from Twitter.Setting.Setting import Setting
from Twitter.Twitter import Twitter


def load_mongo_credentials(file_credentials=None, credential_key=None):
    if file_credentials and credential_key:
        with open(file_credentials) as stream:
            try:
                credentials = yaml.safe_load(stream)[credential_key]
                user = credentials['user']
                password = credentials['password']
                host = credentials['host']
                port = credentials['port']
            except yaml.YAMLError as e:
                print(e)
    else:
        user = os.environ.get("MONGO_USER")
        password = os.environ.get("MONGO_PASSWORD")
        host = os.environ.get("MONGO_HOST")
        port = os.environ.get("MONGO_PORT")

    return host, password, port, user


if __name__ == '__main__':
    twitter = Twitter()
    twitter.auth(Setting.OAUTH_v2, file_credentials='credentials.yaml', credential_key='twitter_api_credentials')
    now = datetime.now().strftime('%Y-%m-%dT%H-%M-%S.%fZ')

    lookup_tweets = twitter.lookup_tweets_by_id_v2(
        ids=[1035317883067281408],
        save_json=True,
        json_path=f'samples/search-tweet/search-tweets-debug-{now}.json'
    )

    pprint(lookup_tweets)

    host, password, port, user = load_mongo_credentials(file_credentials='credentials.yaml',
                                                        credential_key='mongodb_credentials')

    client = MongoClient(f"mongodb://{user}:{password}@{host}:{port}")
    db = client.threat
    tweets = db.tweets

    mongo_tweets = []
    mongo_tweet = MongoTweet.map_tweet_to_mongo(lookup_tweets)
    if isinstance(mongo_tweet, list):
        mongo_tweets.extend(mongo_tweet)
    else:
        mongo_tweets.append(mongo_tweet)

    result = tweets.insert_many(mongo_tweets)
    print(result.inserted_ids)

    client.close()
