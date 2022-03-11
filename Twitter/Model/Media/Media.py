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

from Twitter.Model.Metrics.Media.MediaNonPublicMetric import MediaNonPublicMetric
from Twitter.Model.Metrics.Media.MediaOrganicMetric import MediaOrganicMetric
from Twitter.Model.Metrics.Media.MediaPromotedMetric import MediaPromotedMetric
from Twitter.Model.Metrics.Media.MediaPublicMetric import MediaPublicMetric


@dataclass
class Media:
    media_key: str = field(default=None)
    type: str = field(default=None)
    duration_ms: int = field(default=None)
    height: int = field(default=None)
    preview_image_url: str = field(default=None)
    public_metrics: MediaPublicMetric = field(default=None)
    non_public_metrics: MediaNonPublicMetric = field(default=None)
    organic_metrics: MediaOrganicMetric = field(default=None)
    promoted_metrics: MediaPromotedMetric = field(default=None)
    width: int = field(default=None)
    alt_text: str = field(default=None)
    url: str = field(default=None)

    def __post_init__(self):
        if self.public_metrics:
            self.public_metrics = MediaPublicMetric(**self.public_metrics)

        if self.non_public_metrics:
            self.non_public_metrics = MediaNonPublicMetric(**self.non_public_metrics)

        if self.organic_metrics:
            self.organic_metrics = MediaOrganicMetric(**self.organic_metrics)

        if self.promoted_metrics:
            self.promoted_metrics = MediaPromotedMetric(**self.promoted_metrics)

    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o:
            o.__dict__ if not isinstance(o, datetime) else o.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                     sort_keys=True, indent=4))
