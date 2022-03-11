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

from Twitter.Model.Annotation.Annotation import Annotation
from Twitter.Model.Hashtag.Hashtag import Hashtag
from Twitter.Model.Mention.Mention import Mention
from Twitter.Model.URL.URL import URL


@dataclass
class WrapperURL:
    urls: List[URL] = field(default=None)

    def __post_init__(self):
        if self.urls:
            self.urls = [URL(**x) for x in self.urls]


@dataclass
class Description:
    urls: List[URL] = field(default=None)
    mentions: List[Mention] = field(default=None)
    hashtags: List[Hashtag] = field(default=None)
    cashtags: List[Hashtag] = field(default=None)

    def __post_init__(self):
        if self.urls:
            self.urls = [URL(**x) for x in self.urls]

        if self.mentions:
            self.mentions = [Mention(**x) for x in self.mentions]

        if self.hashtags:
            self.hashtags = [Hashtag(**x) for x in self.hashtags]

        if self.cashtags:
            self.cashtags = [Hashtag(**x) for x in self.cashtags]


@dataclass
class Entity:
    url: WrapperURL = field(default=None)
    description: Description = field(default=None)
    urls: List[URL] = field(default=None)
    mentions: List[Mention] = field(default=None)
    hashtags: List[Hashtag] = field(default=None)
    cashtags: List[Hashtag] = field(default=None)
    annotations: List[Annotation] = field(default=None)

    def __post_init__(self):
        if self.url:
            self.url = WrapperURL(**self.url)

        if self.description:
            self.description = Description(**self.description)

        if self.urls:
            self.urls = [URL(**x) for x in self.urls]

        if self.mentions:
            self.mentions = [Mention(**x) for x in self.mentions]

        if self.hashtags:
            self.hashtags = [Hashtag(**x) for x in self.hashtags]

        if self.cashtags:
            self.cashtags = [Hashtag(**x) for x in self.cashtags]

        if self.annotations:
            self.annotations = [Annotation(**x) for x in self.annotations]

    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o:
            o.__dict__ if not isinstance(o, datetime) else o.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                     sort_keys=True, indent=4))
