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
from datetime import datetime
import json
from dataclasses import dataclass, field

from Twitter.Model.FilteredStream.StreamRule import StreamRule
from Twitter.Model.Misc.Include import Include
from Twitter.Model.Tweet.FilteredStreamTweet import FilteredStreamTweet
from Twitter.Model.Tweet.SearchTweetResponse import SearchTweetResponse
from Twitter.Model.Tweet.Tweet import Tweet


@dataclass
class MongoTweet:
    data: Tweet
    includes: Include = field(default=None)
    matching_rules: list[StreamRule] = field(default=None)

    def __post_init__(self):
        if self.data:
            self.data = Tweet(**self.data)

        if self.includes:
            self.includes = Include(**self.includes)

        if self.matching_rules:
            self.matching_rules = [StreamRule(**x) for x in self.matching_rules]

    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o:
            o.__dict__ if not isinstance(o, datetime) else o.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                     sort_keys=True, indent=4))

    @staticmethod
    def map_tweet_to_mongo(tweet: SearchTweetResponse | FilteredStreamTweet):
        if isinstance(tweet, FilteredStreamTweet):
            mongo_filtered_stream_tweet = MongoTweet.__map_filtered_stream_tweet_to_mongo(tweet)
            return mongo_filtered_stream_tweet

        elif isinstance(tweet, SearchTweetResponse):
            mongo_search_tweet_list = MongoTweet.__map_search_tweet_to_mongo(tweet)
            return mongo_search_tweet_list

    @staticmethod
    def __map_search_tweet_to_mongo(tweet: SearchTweetResponse | FilteredStreamTweet):
        tweet_list = []
        for tweet_data in tweet.data:
            data = tweet_data.toJSON()
            tweets = None
            users = None
            places = None
            media = None
            polls = None
            if tweet.includes.tweets and tweet_data.referenced_tweets:
                tweets = [x.toJSON() for x in tweet.includes.tweets if x.id in [y.id for y in tweet_data.referenced_tweets]]
            if tweet.includes.users and tweet_data.author_id:
                users = [x.toJSON() for x in tweet.includes.users if x.id == tweet_data.author_id]
            if tweet.includes.places and tweet_data.geo and tweet_data.geo.place_id:
                places = [x.toJSON() for x in tweet.includes.places if x.id == tweet_data.geo.place_id]
            if tweet.includes.media and tweet_data.attachments and tweet_data.attachments.media_keys:
                media = [x.toJSON() for x in tweet.includes.media if
                         x.media_key in [y for y in tweet_data.attachments.media_keys]]
            if tweet.includes.polls and tweet_data.attachments and tweet_data.attachments.poll_ids:
                polls = [x.toJSON() for x in tweet.includes.polls if x.id in [y for y in tweet_data.attachments.poll_ids]]

            includes = Include(users, tweets, media, places, polls).toJSON()
            mongo_item = MongoTweet(data, includes)
            tweet_list.append(mongo_item.toJSON())
        return tweet_list

    @staticmethod
    def __map_filtered_stream_tweet_to_mongo(tweet: SearchTweetResponse | FilteredStreamTweet):
        data = tweet.data.toJSON()

        tweets = None
        users = None
        places = None
        media = None
        polls = None
        matching_rules = None
        if tweet.includes.tweets:
            tweets = [tweet.toJSON() for tweet in tweet.includes.tweets]

        if tweet.includes.users:
            users = [user.toJSON() for user in tweet.includes.users]

        if tweet.includes.places:
            places = [place.toJSON() for place in tweet.includes.places]

        if tweet.includes.media:
            media = [media_record.toJSON() for media_record in tweet.includes.media]

        if tweet.includes.polls:
            polls = [poll.toJSON() for poll in tweet.includes.polls]

        if tweet.matching_rules:
            matching_rules = [rule.toJSON() for rule in tweet.matching_rules]

        includes = Include(users, tweets, media, places, polls).toJSON()
        return MongoTweet(data, includes, matching_rules).toJSON()
