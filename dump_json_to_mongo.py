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
import glob
import json
import os
from typing import Union, Type, List

from pymongo import MongoClient

from Model.MongoDB.MongoTweet import MongoTweet
from Twitter.Model.Tweet.FilteredStreamTweet import FilteredStreamTweet
from Twitter.Model.Tweet.SearchTweetResponse import SearchTweetResponse


def tweet_parser_from_file(file_path: str = '',
                           response_class: Union[Type[SearchTweetResponse], Type[FilteredStreamTweet]]
                           = SearchTweetResponse) -> SearchTweetResponse | FilteredStreamTweet:
    with open(file_path) as json_file:
        data = json.load(json_file)
        print(*data)

    if isinstance(data, list):
        tweet = []
        for record in data:
            tweet.append(response_class(**record))
    else:
        tweet = response_class(**data)

    return tweet


def tweet_parser_from_folder(path_pattern: str = '',
                             response_class: Union[Type[SearchTweetResponse], Type[FilteredStreamTweet]]
                             = SearchTweetResponse) -> List[SearchTweetResponse | FilteredStreamTweet]:
    tweet_list = []
    tweet_files = glob.glob(path_pattern)
    for file_path in tweet_files:
        parsed_tweet = tweet_parser_from_file(file_path, response_class=response_class)
        if isinstance(parsed_tweet, list):
            tweet_list.extend(parsed_tweet)
        else:
            tweet_list.append(parsed_tweet)

    return tweet_list


if __name__ == '__main__':
    tweet_list = tweet_parser_from_folder('./samples/filtered-stream-tweet/*.json', response_class=FilteredStreamTweet)
    tweet_list.extend(tweet_parser_from_folder('./samples/search-tweet/*.json'))

    user = os.environ.get("MONGO_USER")
    password = os.environ.get("MONGO_PASSWORD")
    host = os.environ.get("MONGO_HOST")
    port = os.environ.get("MONGO_PORT")

    client = MongoClient(f"mongodb://{user}:{password}@{host}:{port}")
    db = client.threat
    tweets = db.tweets

    mongo_tweets = []
    for tweet in tweet_list:
        mongo_tweet = MongoTweet.map_tweet_to_mongo(tweet)
        if isinstance(mongo_tweet, list):
            mongo_tweets.extend(mongo_tweet)
        else:
            mongo_tweets.append(mongo_tweet)

    result = tweets.insert_many(mongo_tweets)
    print(result.inserted_ids)

    client.close()
