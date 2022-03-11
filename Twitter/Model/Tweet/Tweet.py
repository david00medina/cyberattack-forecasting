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

from Twitter.Model.Attachment.Attachment import Attachment
from Twitter.Model.ContextAnnotations.ContextAnnotation import ContextAnnotation
from Twitter.Model.Entity.Entity import Entity
from Twitter.Model.Geolocation.Geolocation import Geolocation
from Twitter.Model.Metrics.Tweet.TweetNonPublicMetric import TweetNonPublicMetric
from Twitter.Model.Metrics.Tweet.TweetOrganicMetric import TweetOrganicMetric
from Twitter.Model.Metrics.Tweet.TweetPromotedMetric import TweetPromotedMetric
from Twitter.Model.Metrics.Tweet.TweetPublicMetric import TweetPublicMetric
from Twitter.Model.Misc.WithheldContent import WithheldContent


@dataclass(order=True)
class ReferencedTweet:
    id: str
    type: str


@dataclass(order=True)
class Tweet:
    id: str
    text: str
    author_id: str = field(default=None)
    conversation_id: str = field(default=None)
    created_at: datetime = field(default=None)
    geo: Geolocation = field(default=None)
    in_reply_to_user_id: str = field(default=None)
    lang: str = field(default=None)
    possibly_sensitive: bool = field(default=None)
    public_metrics: TweetPublicMetric = field(default=None)
    non_public_metrics: TweetNonPublicMetric = field(default=None)
    organic_metrics: TweetOrganicMetric = field(default=None)
    promoted_metrics: TweetPromotedMetric = field(default=None)
    reply_settings: str = field(default=None)
    source: str = field(default=None)
    withheld: WithheldContent = field(default=None)
    entities: Entity = field(default=None)
    referenced_tweets: list[ReferencedTweet] = field(default=None)
    context_annotations: list[ContextAnnotation] = field(default=None)
    attachments: Attachment = field(default=None)

    def __post_init__(self):
        if self.created_at:
            self.created_at = datetime.strptime(self.created_at, '%Y-%m-%dT%H:%M:%S.%fZ')

        if self.public_metrics:
            self.public_metrics = TweetPublicMetric(**self.public_metrics)

        if self.non_public_metrics:
            self.non_public_metrics = TweetNonPublicMetric(**self.non_public_metrics)

        if self.organic_metrics:
            self.organic_metrics = TweetOrganicMetric(**self.organic_metrics)

        if self.promoted_metrics:
            self.promoted_metrics = TweetPromotedMetric(**self.promoted_metrics)

        if self.withheld:
            self.withheld = WithheldContent(**self.withheld)

        if self.entities:
            self.entities = Entity(**self.entities)

        if self.referenced_tweets:
            self.referenced_tweets = [ReferencedTweet(**x) for x in self.referenced_tweets]

        if self.context_annotations:
            self.context_annotations = [ContextAnnotation(**x) for x in self.context_annotations]

        if self.attachments:
            self.attachments = Attachment(**self.attachments)

        if self.geo:
            self.geo = Geolocation(**self.geo)

    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o:
            o.__dict__ if not isinstance(o, datetime) else o.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                     sort_keys=True, indent=4))
