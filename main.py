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
from typing import Dict

from searchtweets import ResultStream, gen_request_parameters, load_credentials


if __name__ == '__main__':
    credentials = load_credentials('./twitter_keys.yaml', 'twitter_api_credentials')

    query = gen_request_parameters("snow", results_per_call=100)
    rs = ResultStream(endpoint=credentials['endpoint'], request_parameters=query,
                      bearer_token=credentials['bearer_token'], max_tweets=500, max_requests=2)

    tweets = list(rs.stream())
    print(tweets)
    [print(tweet, '\n') for tweet in tweets[0:10]]
