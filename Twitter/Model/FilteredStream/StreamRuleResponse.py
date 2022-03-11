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

from dataclasses import dataclass, field
from typing import List

from Twitter.Model.FilteredStream.StreamRule import StreamRule


@dataclass
class RuleStreamSummary:
    created: int = field(default=None)
    not_created: int = field(default=None)
    deleted: int = field(default=None)
    not_deleted: int = field(default=None)
    valid: int = field(default=None)
    invalid: int = field(default=None)


@dataclass
class RuleStreamMeta:
    sent: int = field(default=None)
    summary: RuleStreamSummary = field(default=None)
    result_count: int = field(default=None)

    def __post_init__(self):
        if self.summary:
            self.summary = RuleStreamSummary(**self.summary)


@dataclass
class StreamRuleError:
    id: str
    value: str
    title: str
    type: str


@dataclass
class StreamRuleResponse:
    data: List[StreamRule] = field(default_factory=list)
    meta: RuleStreamMeta = field(default=None)
    errors: List[StreamRuleError] = field(default=list)

    def __post_init__(self):
        if self.data:
            self.data = [StreamRule(**x) for x in self.data]

        if self.meta:
            self.meta = RuleStreamMeta(**self.meta)
