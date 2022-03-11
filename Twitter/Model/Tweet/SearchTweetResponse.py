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
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from Twitter.Model.Misc.Error import Error
from Twitter.Model.Misc.Include import Include
from Twitter.Model.Tweet.Tweet import Tweet


@dataclass(order=True)
class TweetMeta:
    newest_id: str
    oldest_id: str
    result_count: int
    next_token: str


@dataclass(order=True)
class SearchTweetResponse:
    meta: TweetMeta = field(default=None)
    includes: Include = field(default=None)
    data: List[Tweet] = field(default_factory=list)
    errors: List[Error] = field(default=None)

    def __post_init__(self):
        self.data = [Tweet(**tweet) for tweet in self.data]

        if self.includes:
            self.includes = Include(**self.includes)

        if self.meta:
            self.meta = TweetMeta(**self.meta)

        if self.errors:
            self.errors = [Error(**error) for error in self.errors]

    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o:
            o.__dict__ if not isinstance(o, datetime.datetime) else o.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                     sort_keys=True, indent=4))
