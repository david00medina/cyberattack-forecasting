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
import csv
import os
import time

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
    file = open('datasets/cyberbulling1-twitter/cyberbulling1-twitter.csv')
    csvreader = csv.reader(file)

    headers = next(csvreader)
    csv_content = []
    tweet_ids = []
    for row in csvreader:
        content = {}
        for i, value in enumerate(row):
            value = int(value)
            if i == 0:
                tweet_ids.append(value)
            content[headers[i]] = value

        csv_content.append(content)

    twitter = Twitter()
    twitter.auth(Setting.OAUTH_v2, file_credentials='credentials.yaml', credential_key='twitter_api_credentials')

    batches = len(tweet_ids) // 100 if len(tweet_ids) % 100 == 0 else len(tweet_ids) // 100 + 1
    tweets = []
    for batch in range(batches):
        tweets_batch = tweet_ids[batch*100:(batch+1)*100]
        lookup_tweets = twitter.lookup_tweets_by_id_v2(
            ids=tweets_batch,
        )
        while isinstance(lookup_tweets, dict):
            time.sleep(180)
            lookup_tweets = twitter.lookup_tweets_by_id_v2(
                ids=tweets_batch,
            )

        tweets.extend(MongoTweet.map_tweet_to_mongo(lookup_tweets))

    for tweet in tweets:
        for content in csv_content:
            csv_id = content['Id']
            tweet_id = int(tweet['data']['id'])
            if csv_id == tweet_id:
                tweet['Cyberbullying'] = content['Cyberbullying']
                tweet['Insult'] = content['Insult']
                tweet['Profanity'] = content['Profanity']
                tweet['Sarcasm'] = content['Sarcasm']
                tweet['Threat'] = content['Threat']
                tweet['Exclusion'] = content['Exclusion']
                tweet['Pornography'] = content['Pornography']
                tweet['Spam'] = content['Spam']
                break

    host, password, port, user = load_mongo_credentials(file_credentials='credentials.yaml',
                                                        credential_key='mongodb_cyberbulling_credentials')

    client = MongoClient(f"mongodb://{user}:{password}@{host}:{port}")
    db = client.cyberbulling
    tweets_collection = db.tweets

    result = tweets_collection.insert_many(tweets)
    print(result.inserted_ids)

    client.close()
