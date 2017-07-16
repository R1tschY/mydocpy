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

import ast

from typing import Text, Match


class SourceLocation(object):
    """
    Location in a source
    """

    __slots__ = ("line", "col")

    def __init__(self, line=None, col=None):
        # type: (int, int) -> None
        self.line = line  # type: int
        self.col = col  # type: int

    def next_line(self):
        # type: () -> SourceLocation
        return SourceLocation(self.line + 1, 0)

    def __add__(self, other):
        # type: (SourceDistance) -> SourceLocation
        lines = self.line + other.lines
        cols = self.col if other.lines else self.col + other.cols
        return SourceLocation(lines, cols)

    def __sub__(self, other):
        # type: (SourceLocation) -> SourceDistance
        lines = self.line - other.line
        cols = self.col if lines else self.col - other.col
        return SourceDistance(lines, cols)

    @classmethod
    def from_node(cls, node):  # type: (ast.AST) -> SourceLocation
        return cls(node.lineno - 1, node.col_offset)

    @classmethod
    def from_text_pos(cls, text, pos):  # type: (Text, int) -> SourceLocation
        """
        get line number (starting at 0) and column offset of ``pos`` in ``text``
        """
        last_nl = text.rfind('\n', 0, pos)
        if last_nl < 0:
            return SourceLocation(0, pos)

        return SourceLocation(text[:pos].count('\n'), pos - (last_nl + 1))

    def __repr__(self):
        return "SourceLocation(line={}, col={})".format(
            repr(self.line), repr(self.col)
        )

    def _keys(self):
        return (self.line, self.col)

    def __eq__(self, other):
        return type(self) == type(other) and self._keys() == other._keys()


class SourceDistance(object):
    """
    Distance in source
    """

    __slots__ = ("lines", "cols")

    def __init__(self, line=None, col=None):
        # type: (int, int) -> None
        self.lines = line  # type: int
        self.cols = col  # type: int

    def next_line(self):
        # type: () -> SourceLocation
        return SourceLocation(self.lines + 1, 0)

    def __add__(self, other):
        # type: (SourceDistance) -> SourceDistance
        lines = self.lines + other.line
        cols = self.cols if other.line else self.cols + other.col
        return SourceLocation(lines, cols)

    def __sub__(self, other):
        # type: (SourceDistance) -> SourceDistance
        lines = self.lines - other.line
        cols = self.cols if lines else self.cols - other.col
        return SourceLocation(lines, cols)

    def __repr__(self):
        return "SourceDistance(lines={}, cols={})".format(
            repr(self.lines), repr(self.cols)
        )

    def _keys(self):
        return (self.lines, self.cols)

    def __eq__(self, other):
        return type(self) == type(other) and self._keys() == other._keys()


class SourceRange(object):
    __slots__ = ("start", "length")

    def __init__(self, start=None, length=None):
        # type: (SourceLocation, int, int) -> None
        self.start = start  # type: SourceLocation
        self.length = length  # type: SourceDistance

    @property
    def end(self):
        return self.start + self.length

    def __repr__(self):
        return "SourceRange(start={}, length={})".format(
                    repr(self.start), repr(self.length)
               )

    @classmethod
    def from_match(cls, text, match):  # type: (Text, Match) -> SourceRange
        start = SourceLocation.from_text_pos(text, match.start(0))
        end = SourceLocation.from_text_pos(text, match.end(0))
        return cls(start, end - start)

    @classmethod
    def from_location(cls, location):  # type: (SourceLocation) -> SourceRange
        return cls(location, SourceDistance(0, 0))

    def _keys(self):
        return (self.start, self.length)

    def __eq__(self, other):
        return type(self) == type(other) and self._keys() == other._keys()
