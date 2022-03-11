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

from Twitter.Model.Media.Media import Media
from Twitter.Model.Place.Place import Place
from Twitter.Model.Poll.Poll import Poll
from Twitter.Model.Tweet.Tweet import Tweet
from Twitter.Model.User.User import User


@dataclass(order=True)
class Include:
    users: list[User] = field(default=None)
    tweets: list[Tweet] = field(default=None)
    media: list[Media] = field(default=None)
    places: list[Place] = field(default=None)
    polls: list[Poll] = field(default=None)

    def __post_init__(self):
        if self.users:
            self.users = [User(**x) for x in self.users]

        if self.tweets:
            self.tweets = [Tweet(**x) for x in self.tweets]

        if self.media:
            self.media = [Media(**x) for x in self.media]

        if self.places:
            self.places = [Place(**x) for x in self.places]

        if self.polls:
            self.polls = [Poll(**x) for x in self.polls]

    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o:
            o.__dict__ if not isinstance(o, datetime) else o.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                     sort_keys=True, indent=4))
