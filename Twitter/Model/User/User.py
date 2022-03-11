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
from datetime import datetime
from dataclasses import dataclass, field

from Twitter.Model.Entity.Entity import Entity
from Twitter.Model.Metrics.User.UserPublicMetric import UserPublicMetric
from Twitter.Model.Misc.WithheldContent import WithheldContent


@dataclass
class User:
    id: str
    name: str
    username: str
    created_at: str = field(default=None)
    description: str = field(default=None)
    location: str = field(default=None)
    pinned_tweet_id: str = field(default=None)
    profile_image_url: str = field(default=None)
    protected: bool = field(default=None)
    public_metrics: UserPublicMetric = field(default=None)
    url: str = field(default=None)
    verified: bool = field(default=None)
    withheld: WithheldContent = field(default=None)
    entities: Entity = field(default=None)

    def __post_init__(self):
        if self.created_at:
            self.created_at = datetime.strptime(self.created_at, '%Y-%m-%dT%H:%M:%S.%fZ')

        if self.withheld:
            self.withheld = WithheldContent(**self.withheld)

        if self.entities:
            self.entities = Entity(**self.entities)

        if self.public_metrics:
            self.public_metrics = UserPublicMetric(**self.public_metrics)

    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o:
            o.__dict__ if not isinstance(o, datetime) else o.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                     sort_keys=True, indent=4))
