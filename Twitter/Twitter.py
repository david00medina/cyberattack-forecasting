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

from requests import Response, Session
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth1
from typing import Dict, List, Tuple, Union
import datetime
import json
import os

from Twitter.Model.FilteredStream.StreamRuleResponse import StreamRuleResponse
from Twitter.Model.Tweet.FilteredStreamTweet import FilteredStreamTweet
from Twitter.Model.Tweet.SearchTweetResponse import SearchTweetResponse
from Twitter.Setting.Setting import Setting


class Twitter:
    def __init__(self):
        self.__session = Session()
        self.__BASE_URL = "https://api.twitter.com"

    def auth(self, mode=Setting.OAUTH_v1, api_key=None, api_secret_key=None, bearer_token=None, access_token=None,
             access_token_secret=None, file_credentials=None):
        if api_key is None:
            api_key = os.environ.get("TWITTER_API_KEY")

        if api_secret_key is None:
            api_secret_key = os.environ.get("TWITTER_API_SECRET_KEY")

        if bearer_token is None:
            bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")

        if access_token is None:
            access_token = os.environ.get("TWITTER_ACCESS_TOKEN")

        if access_token_secret is None:
            access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

        if mode == Setting.OAUTH_v1:
            self.__session.auth = OAuth1(api_key, api_secret_key, access_token, access_token_secret)
            auth_data = self.__session.auth.client
            return {
                'api_key': auth_data.client_key,
                'api_secret_key': auth_data.client_secret,
                'access_token': auth_data.resource_owner_key,
                'access_token_secret': auth_data.resource_owner_secret
            }

        elif mode == Setting.OAUTH_v2:
            basic_auth = HTTPBasicAuth(api_key, api_secret_key)
            return self.__get_bearer_token(basic_auth)

        elif mode == Setting.BASIC_AUTH:
            self.__session.auth = HTTPBasicAuth(api_key, api_secret_key)
            auth_data = self.__session.auth
            return {
                'username': auth_data.username,
                'password': auth_data.password
            }

    def __get(self, url: str = '', headers: Dict = None, params: Dict = None, data: Dict = None, files: Dict = None,
              payload: Dict = None, hooks: Dict = None, auth=None, stream: bool = False) -> Response:
        return self.__session.get(
            url=self.__BASE_URL + url,
            headers=headers,
            params=params,
            data=data,
            files=files,
            json=payload,
            hooks=hooks,
            auth=auth,
            stream=stream
        )

    def __post(self, url: str = '', headers: Dict = None, params: Dict = None, data: Dict = None, files: Dict = None,
               payload: Dict = None, hooks: Dict = None, auth=None, stream: bool = False) -> Response:
        return self.__session.post(
            url=self.__BASE_URL + url,
            headers=headers,
            params=params,
            data=data,
            files=files,
            json=payload,
            hooks=hooks,
            auth=auth,
            stream=stream
        )

    def __get_bearer_token(self, auth):
        self.__session.auth = auth
        response = self.__session.post(f"{self.__BASE_URL}/oauth2/token", params={'grant_type': 'client_credentials'})
        self.__session.auth = None
        if response.status_code == 200:
            response = response.json()
            access_token = response['access_token']
            self.__session.headers = {'Authorization': f'Bearer {access_token}'}
            return response
        else:
            return json.loads(response.text)

    @staticmethod
    def __set_expansion_fields(expansions: Dict = None, media_fields: Dict = None, place_fields: Dict = None,
                               poll_fields: Dict = None, tweet_fields: Dict = None, user_fields: Dict = None):
        if expansions is None:
            expansions = 'attachments.poll_ids,attachments.media_keys,author_id,entities.mentions.username,' \
                         'geo.place_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id'

        if media_fields is None:
            media_fields = 'duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics,' \
                           'non_public_metrics,organic_metrics,promoted_metrics,alt_text'

        if place_fields is None:
            place_fields = 'contained_within,country,country_code,full_name,geo,id,name,place_type'

        if poll_fields is None:
            poll_fields = 'duration_minutes,end_datetime,id,options,voting_status'

        if tweet_fields is None:
            tweet_fields = 'attachments,author_id,context_annotations,conversation_id,created_at,entities,' \
                           'geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,' \
                           'reply_settings,source,text,withheld'

        if user_fields is None:
            user_fields = 'created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,' \
                          'protected,public_metrics,url,username,verified,withheld'

        return {
            'expansions': expansions,
            'media.fields': media_fields,
            'place.fields': place_fields,
            'poll.fields': poll_fields,
            'tweet.fields': tweet_fields,
            'user.fields': user_fields
        }

    def __save_json(self, file_path: str = '', tweet_list: List = []):
        with open(file_path, 'w') as out_file:
            json.dump(tweet_list, out_file, indent=4, separators=(',', ': '))

    def lookup_tweets_by_id_v2(self, ids: List[int] = [], expansions: Dict = None, media_fields: Dict = None,
                               place_fields: Dict = None, poll_fields: Dict = None, tweet_fields: Dict = None,
                               user_fields: Dict = None, save_json: bool = False, json_path: str = 'tweets.json',
                               **kwargs):
        if len(ids) > 0 and len(ids) <= 100:
            expansion_fields = \
                self.__set_expansion_fields(
                    expansions,
                    media_fields,
                    place_fields,
                    poll_fields,
                    tweet_fields,
                    user_fields
                )

            params = {
                'ids': ",".join(map(str, ids)),
                **expansion_fields,
                **kwargs
            }

            response = self.__get("/2/tweets", params=params)
            if response.status_code == 200:
                data = response.json()

                if save_json:
                    self.__save_json(json_path, data)

                return SearchTweetResponse(**data)
            else:
                return json.loads(response.text)


    def search_tweets_v2(self, query: str, start_time: datetime.date = None, end_time: datetime.date = None,
                         max_results: int = 10, next_token: str = None, expansions: Dict = None,
                         media_fields: Dict = None, place_fields: Dict = None, poll_fields: Dict = None,
                         tweet_fields: Dict = None, user_fields: Dict = None, since_id: int = None,
                         until_id: int = None, save_json: bool = False, json_path: str = 'tweets.json',
                         **kwargs) -> SearchTweetResponse:
        if start_time is not None:
            start_time = (datetime.datetime.now() - datetime.timedelta(days=7))
            start_time = start_time.replace(microsecond=0).isoformat() + "Z"
        if end_time is not None:
            end_time = (datetime.datetime.now() + datetime.timedelta(seconds=1))
            end_time = end_time.replace(microsecond=0).isoformat() + "Z"

        expansion_fields = \
            self.__set_expansion_fields(
                expansions,
                media_fields,
                place_fields,
                poll_fields,
                tweet_fields,
                user_fields
            )

        params = {
            'query': query,
            'start_time': start_time,
            'end_time': end_time,
            'max_results': max_results,
            'next_token': next_token,
            **expansion_fields,
            'since_id': since_id,
            'until_id': until_id,
            **kwargs
        }

        response = self.__get("/2/tweets/search/recent", params=params)
        if response.status_code == 200:
            data = response.json()

            if save_json:
                self.__save_json(json_path, data)

            return SearchTweetResponse(**data)
        else:
            return json.loads(response.text)

    def search_filtered_stream_tweets_v2(self, max_tweets: int = 10, backfill_minutes: int = None, expansions: Dict = None,
                                         media_fields: Dict = None, place_fields: Dict = None, poll_fields: Dict = None,
                                         tweet_fields: Dict = None, user_fields: Dict = None, save_json: bool = False,
                                         json_path: str = 'tweets.json', **kwargs):
        expansion_fields = \
            self.__set_expansion_fields(
                expansions,
                media_fields,
                place_fields,
                poll_fields,
                tweet_fields,
                user_fields
            )

        params = {
            'backfill_minutes': backfill_minutes,
            **expansion_fields,
            **kwargs
        }

        with self.__get("/2/tweets/search/stream", params=params, stream=True) as response:

            if response.encoding is None:
                response.encoding = 'utf-8'

            tweets = response.iter_lines(decode_unicode=True)

            tweet_list = []
            tweet_file_list = []
            status_code = 400

            try:
                for tweet in tweets:
                    tweet_data = json.loads(tweet)
                    tweet_file_list.append(tweet_data)
                    tweet_data = FilteredStreamTweet(**tweet_data)
                    tweet_list.append(tweet_data)

                    if save_json:
                        self.__save_json(json_path, tweet_file_list)

                    if len(tweet_list) == max_tweets:
                        status_code = response.status_code
                        response.close()

            except AttributeError:
                if status_code == 200:
                    return tweet_list
                else:
                    return tweet_list

    def get_stream_rules_v2(self, ids: str = None) -> StreamRuleResponse:
        response = self.__get("/2/tweets/search/stream/rules", params={ids: ids})
        data = response.json()
        if response.status_code == 200:
            return StreamRuleResponse(**data)
        else:
            return json.loads(response.text)

    def update_stream_rules_v2(self, add_rule_values: Union[List, Tuple] = None,
                               delete_rule_ids: Union[List, Tuple] = None,
                               tags: Union[List, Tuple] = None,
                               dry_run: bool = False) -> Union[StreamRuleResponse, None]:
        if add_rule_values and tags and len(add_rule_values) != len(tags):
            return None
        rules = self.__generate_rule_payload(add_rule_values, delete_rule_ids, tags)

        response = self.__post("/2/tweets/search/stream/rules", params={dry_run: dry_run}, payload=rules)
        data = response.json()
        if response.status_code == 200:
            return StreamRuleResponse(**data)
        elif response.status_code == 201:
            return StreamRuleResponse(**data)
        else:
            return json.loads(response.text)

    @staticmethod
    def __generate_rule_payload(add_rule_values: Union[List, Tuple] = None, delete_rule_ids: Union[List, Tuple] = None,
                                tags: Union[List, Tuple] = None) -> Dict:
        rule_payload = {}
        rules = []
        if add_rule_values:
            for value, tag in zip(add_rule_values, tags):
                rules.append({
                    "value": value,
                    "tag": tag
                })
            rule_payload['add'] = rules

        elif delete_rule_ids:
            for rule_id in delete_rule_ids:
                rules.append(rule_id)
            rule_payload['delete'] = {
                "ids": rules
            }

        return rule_payload
