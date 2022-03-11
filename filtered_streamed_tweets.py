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
from pprint import pprint
from datetime import datetime

from pymongo import MongoClient
from searchtweets import ResultStream, gen_request_parameters, load_credentials
from twitter_scraper import get_tweets

from Model.MongoDB.MongoTweet import MongoTweet
from Twitter.Setting.Setting import Setting
from Twitter.Twitter import Twitter


def twitter_test():
    credentials = load_credentials('./twitter_keys.yaml', 'twitter_api_credentials')

    query = gen_request_parameters("snow", results_per_call=100)
    rs = ResultStream(endpoint=credentials['endpoint'], request_parameters=query,
                      bearer_token=credentials['bearer_token'], max_tweets=500, max_requests=2)

    tweets = list(rs.stream())
    print(tweets)
    [print(tweet, '\n') for tweet in tweets[0:10]]


def twitter_scraper():
    for tweet in get_tweets('hello', pages=20):
        print(tweet)


def add_default_stream_rules(twitter):
    r = twitter.update_stream_rules_v2(
        add_rule_values=("hack", "war", "carding", "ddos"),
        tags=("class_1", "class_2", "class_3", "class_4"))
    pprint(r)
    return r


def delete_default_stream_rules(twitter, twitter_rules):
    rule_ids = [x.id for x in twitter_rules.data]
    r = twitter.update_stream_rules_v2(delete_rule_ids=rule_ids)
    pprint(r)
    return r


def get_twitter_rules():
    rules = twitter.get_stream_rules_v2()
    pprint(rules)
    return rules


if __name__ == '__main__':
    # ================================================================================
    # twitter_test()
    # twitter_scraper()
    # =================================================================================
    twitter = Twitter()
    twitter.auth(Setting.OAUTH_v2)
    now = datetime.now().strftime('%Y-%m-%dT%H-%M-%S.%fZ')

    # =================================================================================
    # search_tweets = twitter.search_tweets_v2(
    #     'hack',
    #     save_json=True,
    #     json_path=f'samples/search-tweet/search-tweets-debug-{datetime.now()}.json'
    # )
    # =================================================================================

    twitter_rules = get_twitter_rules()

    # =================================================================================
    # response_add = add_default_stream_rules(twitter)
    # twitter_rules = get_twitter_rules()
    # =================================================================================
    # response_delete = delete_default_stream_rules(twitter, twitter_rules)
    # twitter_rules = get_twitter_rules()
    # =================================================================================

    filtered_tweets = twitter.search_filtered_stream_tweets_v2(
        max_tweets=2,
        save_json=True,
        json_path=f'samples/filtered-stream-tweet/streamed-tweets-debug-{now}.json'
    )
    pprint(filtered_tweets)

    user = os.environ.get("MONGO_USER")
    password = os.environ.get("MONGO_PASSWORD")
    host = os.environ.get("MONGO_HOST")
    port = os.environ.get("MONGO_PORT")

    client = MongoClient(f"mongodb://{user}:{password}@{host}:{port}")
    db = client.threat
    tweets = db.tweets

    mongo_tweets = []
    for tweet in filtered_tweets:
        mongo_tweet = MongoTweet.map_tweet_to_mongo(tweet)
        if isinstance(mongo_tweet, list):
            mongo_tweets.extend(mongo_tweet)
        else:
            mongo_tweets.append(mongo_tweet)
    result = tweets.insert_many(mongo_tweets)
    print(result.inserted_ids)

    client.close()
