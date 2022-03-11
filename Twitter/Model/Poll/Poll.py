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

from Twitter.Model.Poll.Option import Option


@dataclass
class Poll:
    id: str = field(default=None)
    options: list[Option] = field(default=None)
    duration_minutes: int = field(default=None)
    end_datetime: datetime = field(default=None)
    voting_status: str = field(default=None)

    def __post_init__(self):
        if self.end_datetime:
            self.end_datetime = datetime.strptime(self.end_datetime, '%Y-%m-%dT%H:%M:%S.%fZ')

        if self.options:
            self.options = [Option(**x) for x in self.options]

    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o:
            o.__dict__ if not isinstance(o, datetime) else o.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                     sort_keys=True, indent=4))
