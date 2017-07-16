# -*- coding=utf-8 -*-
#
# Copyright 2017 Richard Liebscher
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import shutil
from itertools import islice

from typing import Iterable, TextIO, Tuple, NamedTuple, Text

from mydocpy.source import SourceLocation, SourceDistance, SourceRange
from mydocpy.utils.iterutils import consume


SourceReplacement = NamedTuple(
    "SourceReplacement",
    [
        ("source_range", SourceRange),
        ("replacement", Text)
    ]
)


class _ReplacementApplier(object):

    def __init__(self, srcfile, destfile, source_replacements):
        # type: (TextIO, TextIO, Iterable[SourceReplacement]) -> None
        self.srcfile = srcfile
        self.destfile = destfile
        self.source_replacements = source_replacements
        self.srcpos = SourceLocation(0, 0)

    def _write(self, diff):
        # type: (SourceDistance) -> None
        if diff.lines > 0:
            self.destfile.writelines(islice(self.srcfile, diff.lines))

        if diff.cols:
            self.destfile.write(self.srcfile.read(diff.cols))

    def _skip(self, diff):
        # type: (SourceDistance) -> None
        if diff.lines > 0:
            consume(islice(self.srcfile, diff.lines))

        if diff.cols:
            self.srcfile.read(diff.cols)

    def execute(self):
        # type: () -> None

        for source_replacement in self.source_replacements:
            start = source_replacement.source_range.start
            length = source_replacement.source_range.length

            self._write(start - self.srcpos)
            self._skip(length)

            self.destfile.write(source_replacement.replacement)

            self.srcpos = start + length

        # write rest
        shutil.copyfileobj(self.srcfile, self.destfile)


def apply(srcfile, destfile, source_replacements):
    # type: (TextIO, TextIO, Iterable[SourceReplacement]) -> None

    source_replacements = list(source_replacements)
    source_replacements.sort(
        key=lambda x: x.source_range.start.line
    )
    # TODO: use itertools.groupby
    # TODO: find conflicts

    applier = _ReplacementApplier(srcfile, destfile, source_replacements)
    applier.execute()
